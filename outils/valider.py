#!/usr/bin/env python3
"""Contrôle la base avant tout usage.

Vérifie que chaque table respecte son schéma, que chaque référence existe, que chaque
identifiant de chiffre correspond à sa fiche et que chaque copie archivée est intacte ; relit
chaque copie des comptes de chaque collectivité, qui doit donner son inscription.

    python3 outils/valider.py
"""

import datetime
import math
import re
import sys

import importer_ofgl_collectivites as ofgl
from commun import (BASE, empreinte_et_taille, identifiant, lire, lire_jsonstat, lire_sdmx, lire_tableaux_html, lire_xlsx,
                    nombre_de_phrase, nombre_texte, paquet, ressources_chiffres, texte_html)


def erreur_de_type(type_, texte):
    try:
        if type_ == "integer":
            int(texte)
        elif type_ == "number":
            if not math.isfinite(float(texte)):
                raise ValueError
        elif type_ == "date":
            datetime.date.fromisoformat(texte)
        elif type_ == "datetime":
            datetime.datetime.fromisoformat(texte.replace("Z", "+00:00"))
    except ValueError:
        return f"« {texte} » n'est pas du type {type_}"
    return None


def controler_schemas(ressources, tables, erreurs):
    for r in ressources:
        noms = [c["name"] for c in r["schema"]["fields"]]
        chemin = BASE / r["path"]
        if not chemin.exists():
            erreurs.append(f"{r['path']} : fichier absent")
            continue
        with chemin.open(encoding="utf-8") as f:
            entete = f.readline().rstrip("\n").split(",")
        if entete != noms:
            erreurs.append(f"{r['path']} : colonnes {entete}, attendues {noms}")
            continue
        for n, ligne in enumerate(tables[r["name"]], start=2):
            for champ in r["schema"]["fields"]:
                valeur, contraintes = ligne[champ["name"]], champ.get("constraints", {})
                lieu = f"{r['path']}, ligne {n}, {champ['name']}"
                if not valeur:
                    if contraintes.get("required"):
                        erreurs.append(f"{lieu} : valeur obligatoire manquante")
                    continue
                if message := erreur_de_type(champ.get("type", "string"), valeur):
                    erreurs.append(f"{lieu} : {message}")
                if "enum" in contraintes and valeur not in contraintes["enum"]:
                    erreurs.append(f"{lieu} : « {valeur} » n'est pas parmi {contraintes['enum']}")
                if "pattern" in contraintes and not re.fullmatch(contraintes["pattern"], valeur):
                    erreurs.append(f"{lieu} : « {valeur} » ne respecte pas le format {contraintes['pattern']}")
        cle = r["schema"].get("primaryKey", [])
        vues = {}
        for n, ligne in enumerate(tables[r["name"]], start=2):
            k = tuple(ligne[c] for c in cle)
            if cle and k in vues:
                erreurs.append(f"{r['path']}, ligne {n} : identifiant {k[0] if len(k) == 1 else k} déjà présent ligne {vues[k]}")
            vues[k] = n


def controler_references(ressources, tables, erreurs):
    for r in ressources:
        for ref in r["schema"].get("foreignKeys", []):
            cible = ref["reference"]["resource"] or r["name"]
            connues = {tuple(l[c] for c in ref["reference"]["fields"]) for l in tables[cible]}
            for n, ligne in enumerate(tables[r["name"]], start=2):
                k = tuple(ligne[c] for c in ref["fields"])
                if all(k) and k not in connues:
                    erreurs.append(f"{r['path']}, ligne {n} : {', '.join(ref['fields'])} « {', '.join(k)} » "
                                   f"absent de la table {cible}")


def controler_chiffres(tables, erreurs):
    chiffres = [(r["path"], n, l) for r in ressources_chiffres() for n, l in enumerate(tables[r["name"]], start=2)]
    ids, traitements = {}, {t["id"] for t in tables["traitements"]}
    fichiers = {f["id"]: f for f in tables["fichiers"]}
    for chemin, n, ligne in chiffres:
        lieu = f"{chemin}, ligne {n}"
        if ligne["id"] in ids:
            erreurs.append(f"{lieu} : identifiant déjà présent ({ids[ligne['id']]})")
        ids[ligne["id"]] = lieu
        if ligne["id"] != identifiant(ligne):
            erreurs.append(f"{lieu} : l'identifiant ne correspond pas à la fiche (attendu {identifiant(ligne)})")
        for t in filter(None, ligne["traitements"].split(";")):
            if t not in traitements:
                erreurs.append(f"{lieu} : traitement « {t} » absent de la table traitements")
        if (ligne["nature"] == "calcule") != bool(ligne["calcul_id"]):
            erreurs.append(f"{lieu} : un chiffre calculé a une recette de calcul, et lui seul")
        if ligne["nature"] == "publie" and not ligne["fichier_id"]:
            erreurs.append(f"{lieu} : un chiffre publié par une source doit renvoyer à une copie archivée")
        fichier = fichiers.get(ligne["fichier_id"])
        if fichier and fichier["source_id"] != ligne["source_id"]:
            erreurs.append(f"{lieu} : la copie archivée {fichier['id']} vient d'une autre source")
    for chemin, n, ligne in chiffres:
        if ligne["denominateur_id"] and ligne["denominateur_id"] not in ids:
            erreurs.append(f"{chemin}, ligne {n} : dénominateur {ligne['denominateur_id']} absent de la base")
    for n, calcul in enumerate(tables["calculs"], start=2):
        for entree in filter(None, calcul["entrees"].split(";")):
            if entree not in ids:
                erreurs.append(f"tables/calculs.csv, ligne {n} : chiffre d'entrée {entree} absent de la base")
    for n, correction in enumerate(tables["corrections"], start=2):
        if correction["chiffre_id"] not in ids:
            erreurs.append(f"tables/corrections.csv, ligne {n} : chiffre {correction['chiffre_id']} absent de la base")
    return len(chiffres)


def valeur_archivee(fichier, emplacement, copies):
    """(valeur, indicateur) lus dans la copie archivée à l'emplacement indiqué, None si introuvable,
    ou « sans lecteur » pour un format que le contrôle ne sait pas encore lire."""
    chemin = BASE / fichier["chemin"]
    if fichier["chemin"].endswith(".json"):
        if fichier["id"] not in copies:
            dims, valeurs, _ = lire_jsonstat(chemin)
            copies[fichier["id"]] = (dims, valeurs)
        dims, valeurs = copies[fichier["id"]]
        coordonnees = dict(p.split("=", 1) for p in emplacement.split(";"))
        return valeurs.get(tuple(coordonnees.get(d) for d in dims))
    if fichier["chemin"].endswith(".xlsx"):
        trouve = re.match(r"feuille=([^;]+);cellule=([A-Z]+[0-9]+)", emplacement)
        if trouve is None:
            return None
        feuille, cellule = trouve.groups()
        if (fichier["id"], feuille) not in copies:
            copies[(fichier["id"], feuille)] = lire_xlsx(chemin, feuille)[1]
        valeur = copies[(fichier["id"], feuille)].get(cellule)
        return (valeur, "") if isinstance(valeur, float) else None
    if fichier["chemin"].endswith(".html") and emplacement.startswith("phrase="):
        # Un montant énoncé dans le texte : la phrase doit figurer telle quelle dans la page.
        if (fichier["id"], "texte") not in copies:
            copies[(fichier["id"], "texte")] = texte_html(chemin.read_text(encoding="utf-8"))
        phrase = emplacement[len("phrase="):]
        nombre = nombre_de_phrase(phrase) if phrase in copies[(fichier["id"], "texte")] else None
        return (float(nombre[0]), "") if nombre else None
    if fichier["chemin"].endswith(".html"):
        trouve = re.match(r"tableau=([0-9]+);ligne=([0-9]+);colonne=([0-9]+)", emplacement)
        if trouve is None:
            return None
        if fichier["id"] not in copies:
            copies[fichier["id"]] = lire_tableaux_html(chemin)
        t, r, c = (int(x) for x in trouve.groups())
        try:
            nombre = nombre_texte(copies[fichier["id"]][t][r][c])
        except IndexError:
            return None
        return (float(nombre[0]), "") if nombre else None
    if fichier["chemin"].endswith(".xml"):
        trouve = re.match(r"idbank=([0-9]+);periode=([0-9T-]+)", emplacement)
        if trouve is None:
            return None
        if fichier["id"] not in copies:
            copies[fichier["id"]] = lire_sdmx(chemin)
        serie = copies[fichier["id"]].get(trouve.group(1))
        observation = serie[1].get(trouve.group(2)) if serie else None
        if observation is None or nombre_texte(observation.get("OBS_VALUE", "")) is None:
            return None
        return float(observation["OBS_VALUE"]), observation.get("OBS_QUAL", "")
    return "sans lecteur"


def controler_valeurs(tables, erreurs):
    """Relit chaque chiffre publié dans sa copie archivée, à son emplacement, et compare.

    Renvoie le nombre de chiffres relus et celui des chiffres dont la copie n'a pas encore de lecteur
    automatique."""
    fichiers = {f["id"]: f for f in tables["fichiers"]}
    copies, relus, sans_lecteur = {}, 0, 0
    for r in ressources_chiffres():
        for n, ligne in enumerate(tables[r["name"]], start=2):
            fichier = fichiers.get(ligne["fichier_id"])
            if ligne["nature"] != "publie" or fichier is None or not (BASE / fichier["chemin"]).exists():
                continue
            archive = valeur_archivee(fichier, ligne["emplacement"], copies)
            if archive == "sans lecteur":
                sans_lecteur += 1
                continue
            lieu = f"{r['path']}, ligne {n}"
            if archive is None:
                erreurs.append(f"{lieu} : emplacement {ligne['emplacement']} introuvable dans {fichier['chemin']}")
            elif not math.isclose(float(ligne["valeur"]), archive[0], rel_tol=1e-12, abs_tol=1e-9):
                erreurs.append(f"{lieu} : valeur {ligne['valeur']} différente de la copie archivée ({archive[0]})")
            elif ligne["drapeau_source"] != archive[1]:
                erreurs.append(f"{lieu} : indicateur « {ligne['drapeau_source']} » différent de la copie archivée "
                               f"(« {archive[1]} »)")
            relus += 1
    return relus, sans_lecteur


def controler_archives(tables, erreurs):
    for n, f in enumerate(tables["fichiers"], start=2):
        chemin = BASE / f["chemin"]
        if not chemin.exists():
            erreurs.append(f"tables/fichiers.csv, ligne {n} : copie absente ({f['chemin']})")
        elif empreinte_et_taille(chemin) != (f["sha256"], int(f["octets"])):
            erreurs.append(f"tables/fichiers.csv, ligne {n} : la copie {f['chemin']} a été modifiée")


def controler_collectivites(tables, erreurs):
    """Relit chaque copie inscrite dans fichiers_collectivites.csv : son contenu doit donner son inscription. Renvoie
    le nombre de lignes de montants relues."""
    fichiers = {f["id"]: f for f in tables["fichiers"]}
    agregats = {a["agregat"]: a for a in tables["agregats_ofgl"]}
    inscrits = tables["fichiers_collectivites"]
    ordre = {"inventaire": 0, "montants": 1, "collectivites": 2}
    relues = 0
    for n, inscrit in sorted(enumerate(inscrits, start=2), key=lambda e: (ordre.get(e[1]["contenu"], 3), e[0])):
        lieu = f"tables/fichiers_collectivites.csv, ligne {n}"
        if inscrit["fichier_id"] not in fichiers:
            continue  # référence déjà signalée
        try:
            attendue = ofgl.inscription(fichiers[inscrit["fichier_id"]], [i for i in inscrits if i is not inscrit],
                                        fichiers, agregats)
        except SystemExit as e:
            erreurs.append(f"{lieu} : {e}")
            continue
        if attendue != inscrit:
            erreurs.append(f"{lieu} : la copie donne une autre inscription ({attendue})")
        relues += int(inscrit["lignes"]) if inscrit["contenu"] == "montants" else 0
    return relues


def main():
    ressources = paquet()["resources"]
    tables = {r["name"]: lire(r["path"]) for r in ressources}
    erreurs = []
    controler_schemas(ressources, tables, erreurs)
    controler_references(ressources, tables, erreurs)
    nombre = controler_chiffres(tables, erreurs)
    controler_archives(tables, erreurs)
    relus, sans_lecteur = controler_valeurs(tables, erreurs)
    montants = controler_collectivites(tables, erreurs)
    for e in erreurs:
        print(e)
    if erreurs:
        sys.exit(f"{len(erreurs)} erreur(s) : base non conforme.")
    print(f"Base conforme : {nombre} chiffres, {len(tables['fichiers'])} copies archivées intactes, "
          f"{relus} chiffres publiés relus dans leur copie archivée"
          + (f", {sans_lecteur} sans lecteur automatique" if sans_lecteur else "")
          + (f" ; {montants} lignes de comptes de collectivités relues dans les leurs." if montants else "."))


if __name__ == "__main__":
    main()
