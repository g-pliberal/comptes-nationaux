#!/usr/bin/env python3
"""Inscrit dans la base les comptes de chaque collectivité que publie data.ofgl.fr, le portail de l'Observatoire des
finances et de la gestion publique locales (OFGL), à partir des copies archivées de ses exports.

    python3 outils/importer_ofgl_collectivites.py --requetes <source_id> <exercice>   # les requêtes à archiver
    python3 outils/importer_ofgl_collectivites.py <fichier_id>

Les jeux de données des comptes consolidés de l'OFGL donnent, pour chaque collectivité, chaque exercice et chaque agrégat
financier, le montant de son budget principal, celui de ses budgets annexes, les flux croisés entre eux et le montant
consolidé (budget principal plus budgets annexes moins flux croisés), en euros, calculés d'après les balances comptables
de la DGFiP. Trois exports d'un jeu sont archivés, compressés, et s'importent dans cet ordre :
- l'inventaire : le nombre de lignes de chaque exercice du jeu ;
- pour chaque exercice, les montants : une ligne par collectivité et par agrégat ;
- pour chaque exercice, les collectivités : nom, catégorie, territoire et population.
Ces copies sont les chiffres eux-mêmes : la base ne les recopie pas, elle les lit. L'import vérifie chaque ligne
(agrégat connu de tables/agregats_ofgl.csv, montants numériques, une seule ligne par collectivité et par agrégat),
que les montants ont le nombre de lignes de l'inventaire et que la liste des collectivités est celle des montants, puis
inscrit la copie dans tables/fichiers_collectivites.csv. La version d'une copie est la date de modification du jeu de
données qu'annonce le portail ; la copie qui en contrôle une autre est la plus récente de même source dont la version ne
la dépasse pas. Le dernier exercice de l'inventaire est provisoire, les autres définitifs.
"""

import collections
import math
import re
import sys
import urllib.parse

from commun import BASE, champs, ecrire, lire, lire_export_ofgl

PORTAIL = "https://data.ofgl.fr/api/explore/v2.1/catalog/datasets/"
# Jeux de données lus : source → (jeu de données du portail, champs de la liste des collectivités).
JEUX = {
    "ofgl.base-gfp-consolidee": ("ofgl-base-gfp-consolidee", ["siren", "lbudg", "categ", "nat_juridique",
                                                              "mode_financement", "dep_code", "reg_code", "ptot"]),
    "ofgl.base-communes-consolidee": ("ofgl-base-communes-consolidee", ["siren", "insee", "com_code", "lbudg", "categ",
                                                                        "dep_code", "reg_code", "epci_code", "ptot"]),
}
MONTANTS = ["siren", "agregat", "montant_bp", "montant_ba", "montant_flux", "montant"]
INVENTAIRE = ["exer", "lignes"]
# Champs qu'une collectivité peut avoir plusieurs fois, une ligne par valeur : un groupement s'étend sur plusieurs
# départements, voire plusieurs régions.
MULTIPLES = {"dep_code", "reg_code"}
SIRENS = {}  # copie de montants → numéros Siren qu'elle porte, pour contrôler la liste des collectivités sans la relire


def requete(jeu, **parametres):
    return PORTAIL + jeu + "/exports/csv?" + urllib.parse.urlencode(parametres, quote_via=urllib.parse.quote, safe=",*()")


def requetes(source_id, exercice):
    """Les trois exports à archiver pour un exercice d'un jeu de données : inventaire, montants, collectivités."""
    jeu, champs_collectivites = JEUX[source_id]
    filtre = f"exer=date'{exercice}'"
    return {"inventaire": requete(jeu, select="exer,count(*) as lignes", group_by="exer", order_by="exer"),
            "montants": requete(jeu, select=",".join(MONTANTS), where=filtre, order_by="siren,agregat"),
            "collectivites": requete(jeu, select=",".join(champs_collectivites), where=filtre,
                                     group_by=",".join(champs_collectivites), order_by=",".join(champs_collectivites))}


def nature(fichier):
    """(contenu, exercice) de la requête qui a produit la copie : l'une de celles que cet import sait lire."""
    if fichier["source_id"] not in JEUX:
        sys.exit(f"{fichier['id']} : la source {fichier['source_id']} n'est pas lue par cet import")
    trouve = re.search(r"where=exer%3Ddate%27([0-9]{4})%27", fichier["url"])
    exercice = trouve.group(1) if trouve else "0000"
    for contenu, url in requetes(fichier["source_id"], exercice).items():
        if url == fichier["url"]:
            return contenu, "" if contenu == "inventaire" else exercice
    sys.exit(f"{fichier['id']} : requête que cet import ne sait pas lire ({fichier['url']})")


def montant(texte, lieu):
    try:
        valeur = float(texte)
    except ValueError:
        sys.exit(f"{lieu} : montant illisible « {texte} »")
    if not math.isfinite(valeur):
        sys.exit(f"{lieu} : montant illisible « {texte} »")
    return valeur


def lignes(fichier, attendu):
    """Les lignes d'une copie, après contrôle de son en-tête."""
    entete, contenu = lire_export_ofgl(BASE / fichier["chemin"])
    if entete != attendu:
        sys.exit(f"{fichier['id']} : en-tête {entete}, attendu {attendu}")
    for n, ligne in enumerate(contenu, start=2):
        if len(ligne) != len(attendu):
            sys.exit(f"{fichier['id']}, ligne {n} : {len(ligne)} champs au lieu de {len(attendu)}")
    return contenu


def inventaire(fichier):
    """{exercice: nombre de lignes}. Le portail regroupe les exercices par date : « 2024-01-01 00:00:00+00:00 »."""
    resultat = {}
    for n, (exer, nombre) in enumerate(lignes(fichier, INVENTAIRE), start=2):
        annee = re.fullmatch(r"([0-9]{4})(?:-01-01 00:00:00\+00:00)?", exer)
        if annee is None or annee.group(1) in resultat or not nombre.isdigit():
            sys.exit(f"{fichier['id']}, ligne {n} : ligne d'inventaire illisible")
        resultat[annee.group(1)] = int(nombre)
    if not resultat:
        sys.exit(f"{fichier['id']} : inventaire vide")
    return resultat


def marge(texte):
    """Demi-unité de la dernière décimale d'un montant publié, sans les zéros finaux (« 1103074315.0 » est un montant
    à l'euro), au centime au plus fin : les montants de 2022 n'ont que dix chiffres significatifs, ceux des autres
    exercices portent parfois des décimales de calcul au-delà du centime. Un montant nul est exact."""
    if "e" in texte.lower() or float(texte) == 0:
        return 0.005
    decimales = len(texte.split(".")[1].rstrip("0")) if "." in texte else 0
    return 0.5 * 10 ** -min(decimales, 2)


def montants(fichier, agregats, marges=False):
    """Les lignes de montants : [(siren, agrégat, budget principal, budgets annexes, flux croisés, consolidé)], et, si
    `marges`, la marge d'arrondi de chacun des quatre montants à la suite."""
    resultat, vues = [], set()
    for n, (siren, agregat, *valeurs) in enumerate(lignes(fichier, MONTANTS), start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        if not re.fullmatch(r"[0-9]{9}", siren):
            sys.exit(f"{lieu} : numéro Siren illisible « {siren} »")
        if agregat not in agregats:
            sys.exit(f"{lieu} : agrégat inconnu « {agregat} » (le déclarer dans tables/agregats_ofgl.csv)")
        if (siren, agregat) in vues:
            sys.exit(f"{lieu} : deuxième ligne pour {siren} et « {agregat} »")
        vues.add((siren, agregat))
        resultat.append((siren, agregat, *(montant(v, lieu) for v in valeurs))
                        + (tuple(marge(v) for v in valeurs) if marges else ()))
    return resultat


def collectivites(fichier):
    """({siren: {champ: valeur}}, nombre de lignes), les valeurs d'un champ multiple réunies, triées, séparées par
    « ; »."""
    champs_ = JEUX[fichier["source_id"]][1]
    par_siren = collections.defaultdict(list)
    contenu = lignes(fichier, champs_)
    for n, ligne in enumerate(contenu, start=2):
        valeurs = dict(zip(champs_, ligne))
        if not re.fullmatch(r"[0-9]{9}", valeurs["siren"]):
            sys.exit(f"{fichier['id']}, ligne {n} : numéro Siren illisible « {valeurs['siren']} »")
        if valeurs.get("ptot") and not valeurs["ptot"].isdigit():
            sys.exit(f"{fichier['id']}, ligne {n} : population illisible « {valeurs['ptot']} »")
        par_siren[valeurs["siren"]].append(valeurs)
    resultat = {}
    for siren, liste in par_siren.items():
        fiche = {}
        for c in champs_:
            distinctes = sorted({v[c] for v in liste})
            if len(distinctes) > 1 and c not in MULTIPLES:
                sys.exit(f"{fichier['id']} : {siren} a plusieurs valeurs de {c} ({distinctes})")
            fiche[c] = ";".join(distinctes)
        resultat[siren] = fiche
    return resultat, len(contenu)


def controleur(fichier, inscrits, contenu, exercice=""):
    """La copie inscrite qui en contrôle une autre : de même source, du contenu demandé (et du même exercice), la plus
    récente dont la version ne dépasse pas la sienne."""
    version = fichier["mis_a_jour_source"][:10]
    candidats = [i for i in inscrits if i["source_id"] == fichier["source_id"] and i["contenu"] == contenu
                 and i["exercice"] == exercice and i["version"] <= version]
    if not candidats:
        sys.exit(f"{fichier['id']} : aucune copie de {contenu} {exercice} inscrite pour cette source à cette version "
                 "(l'importer d'abord)")
    return max(candidats, key=lambda i: i["version"])["fichier_id"]


def inscription(fichier, inscrits, fichiers, agregats):
    """La ligne de tables/fichiers_collectivites.csv d'une copie, après contrôle de son contenu ; `inscrits` est la
    table déjà écrite, où l'on cherche les copies qui la contrôlent."""
    contenu, exercice = nature(fichier)
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas la date de modification du jeu de données")
    ligne = {"fichier_id": fichier["id"], "source_id": fichier["source_id"], "contenu": contenu, "exercice": exercice,
             "version": version, "statut": "", "lignes": "", "collectivites": ""}
    if contenu == "inventaire":
        ligne["lignes"] = str(len(inventaire(fichier)))
        return ligne
    exercices = inventaire(fichiers[controleur(fichier, inscrits, "inventaire")])
    if exercice not in exercices:
        sys.exit(f"{fichier['id']} : l'exercice {exercice} manque à l'inventaire")
    if contenu == "montants":
        lues = montants(fichier, agregats)
        if len(lues) != exercices[exercice]:
            sys.exit(f"{fichier['id']} : {len(lues)} lignes, l'inventaire en annonce {exercices[exercice]}")
        nombre, sirens = len(lues), {l[0] for l in lues}
        SIRENS[fichier["id"]] = sirens
    else:
        fiches, nombre = collectivites(fichier)
        sirens = set(fiches)
        temoin = controleur(fichier, inscrits, "montants", exercice)
        if temoin not in SIRENS:
            SIRENS[temoin] = {l[0] for l in montants(fichiers[temoin], agregats)}
        attendus = SIRENS[temoin]
        if sirens != attendus:
            sys.exit(f"{fichier['id']} : la liste des collectivités n'est pas celle des montants "
                     f"({len(sirens - attendus)} en plus, {len(attendus - sirens)} en moins)")
    ligne.update(statut="provisoire" if exercice == max(exercices) else "definitif", lignes=str(nombre),
                 collectivites=str(len(sirens)))
    return ligne


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--requetes":
        for url in requetes(sys.argv[2], sys.argv[3]).values():
            print(url)
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    agregats = {a["agregat"]: a for a in lire("tables/agregats_ofgl.csv")}
    inscrits = [i for i in lire("tables/fichiers_collectivites.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]], inscrits, fichiers, agregats)
    ecrire("tables/fichiers_collectivites.csv", champs("fichiers_collectivites"), inscrits + [ligne], cle="fichier_id")
    print(f"{ligne['fichier_id']} : {ligne['contenu']} {ligne['exercice']} ({ligne['version']}, {ligne['statut'] or '—'}), "
          f"{ligne['lignes']} lignes" + (f", {ligne['collectivites']} collectivités" if ligne["collectivites"] else ""))


if __name__ == "__main__":
    main()
