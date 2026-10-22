#!/usr/bin/env python3
"""Contrôle la base avant tout usage.

Vérifie que chaque table respecte son schéma, que chaque référence existe, que chaque
identifiant de chiffre correspond à sa fiche et que chaque copie archivée est intacte.

    python3 outils/valider.py
"""

import datetime
import math
import re
import sys

from commun import BASE, empreinte, identifiant, lire, lire_jsonstat, paquet, ressources_chiffres


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


def controler_valeurs(tables, erreurs):
    """Relit chaque chiffre publié dans sa copie archivée, à son emplacement, et compare.

    Renvoie le nombre de chiffres relus et celui des chiffres dont la copie n'a pas encore de lecteur
    automatique (formats autres que JSON-stat)."""
    fichiers = {f["id"]: f for f in tables["fichiers"]}
    copies, relus, sans_lecteur = {}, 0, 0
    for r in ressources_chiffres():
        for n, ligne in enumerate(tables[r["name"]], start=2):
            fichier = fichiers.get(ligne["fichier_id"])
            if ligne["nature"] != "publie" or fichier is None or not (BASE / fichier["chemin"]).exists():
                continue
            if not fichier["chemin"].endswith(".json"):
                sans_lecteur += 1
                continue
            if fichier["id"] not in copies:
                dims, valeurs, _ = lire_jsonstat(BASE / fichier["chemin"])
                copies[fichier["id"]] = (dims, valeurs)
            dims, valeurs = copies[fichier["id"]]
            coordonnees = dict(p.split("=", 1) for p in ligne["emplacement"].split(";"))
            archive = valeurs.get(tuple(coordonnees.get(d) for d in dims))
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
        elif empreinte(chemin) != f["sha256"] or str(chemin.stat().st_size) != f["octets"]:
            erreurs.append(f"tables/fichiers.csv, ligne {n} : la copie {f['chemin']} a été modifiée")


def main():
    ressources = paquet()["resources"]
    tables = {r["name"]: lire(r["path"]) for r in ressources}
    erreurs = []
    controler_schemas(ressources, tables, erreurs)
    controler_references(ressources, tables, erreurs)
    nombre = controler_chiffres(tables, erreurs)
    controler_archives(tables, erreurs)
    relus, sans_lecteur = controler_valeurs(tables, erreurs)
    for e in erreurs:
        print(e)
    if erreurs:
        sys.exit(f"{len(erreurs)} erreur(s) : base non conforme.")
    print(f"Base conforme : {nombre} chiffres, {len(tables['fichiers'])} copies archivées intactes, "
          f"{relus} chiffres publiés relus dans leur copie archivée"
          + (f", {sans_lecteur} sans lecteur automatique." if sans_lecteur else "."))


if __name__ == "__main__":
    main()
