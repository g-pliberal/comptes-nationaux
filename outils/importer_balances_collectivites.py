#!/usr/bin/env python3
"""Inscrit dans la base les balances comptables des collectivités que publie la DGFiP sur data.economie.gouv.fr, et les
formules par lesquelles l'OFGL en tire ses agrégats financiers, à partir des copies archivées des fichiers joints aux
jeux de données et de l'export du jeu des formules.

    python3 outils/importer_balances_collectivites.py --requetes <source_id>   # les adresses à archiver
    python3 outils/importer_balances_collectivites.py <fichier_id>

La balance comptable d'une collectivité est la liste de ses comptes, budget par budget, telle que la tient son comptable
public : pour chaque budget, principal ou annexe, désigné par son numéro SIRET, et chaque compte de sa nomenclature
budgétaire et comptable, la balance d'entrée, les opérations budgétaires de l'exercice, nettes des annulations et
opérations d'ordre budgétaires comprises, les opérations non budgétaires, les opérations d'ordre budgétaires, chacune au
débit et au crédit, et le solde de sortie, débiteur ou créditeur. La DGFiP joint à chaque jeu de données un fichier par
exercice, depuis 2010 ; le dernier est provisoire, publié en juillet de l'année suivante, les autres définitifs, publiés
en décembre.

L'import d'une balance vérifie son en-tête (les fichiers de 2010 à 2015 et ceux d'après 2016 n'ont pas les mêmes
colonnes), que chaque ligne est de l'exercice, que son budget est désigné par un SIRET qui prolonge le numéro Siren de sa
collectivité, que chaque budget n'a qu'un type (principal ou annexe), qu'une nomenclature, un libellé et une
collectivité, que chaque compte n'y figure qu'une fois, que chaque montant est au centime, et deux identités comptables,
au centime près : pour chaque ligne, le solde de sortie est la balance d'entrée plus les opérations budgétaires et non
budgétaires de l'exercice ; pour chaque budget, la somme des soldes débiteurs est celle des soldes créditeurs.
L'import des formules de l'OFGL vérifie que chacune se lit (outils/formules_ofgl.py) et qu'une seule formule s'applique à
chaque collectivité pour un agrégat, un exercice, une sorte de calcul, une sorte de budget et une nomenclature. Chaque
copie est inscrite dans tables/fichiers_balances_collectivites.csv. Ces copies sont les chiffres eux-mêmes : la base ne
les recopie pas, elle les lit. La version d'une copie est la date de modification du jeu de données qu'annonce le
portail.
"""

import collections
import io
import re
import sys

import formules_ofgl
from commun import BASE, champs, ecrire, lire, ouvrir_copie

PORTAIL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
# Jeux de données des balances : source → (jeu, {exercice: fichier joint}). Les fichiers joints n'ont pas de nom régulier.
JEUX = {
    "dgfip.balances-departements": ("balances-comptables-des-departements", {
        "2010": "balancedept_2010_csv", "2011": "balancedept_2011_csv", "2012": "balancedept_2012_csv",
        "2013": "balancedept_2013_csv", "2014": "balancedept_2014_csv", "2015": "balancedept_2015_csv",
        "2016": "balance_dept_2016_csv", "2017": "balance_deptctu_2017_dec2018_csv",
        "2018": "balance_deptctu_2018_dec2019_csv", "2019": "balance_deptctu_2019_dec2020_csv",
        "2020": "balance_deptctu_2020_dec2021_csv", "2021": "balance_deptctu_2021_dec2022_csv",
        "2022": "balance_deptctu_2022_dec2023_csv", "2023": "balance_deptctu_2023_dec2024_csv",
        "2024": "balance_deptctu_2024_dec2025_csv", "2025": "balance_deptctu_2025_juil2026csv"}),
    "dgfip.balances-regions": ("balances-comptables-des-regions-", {
        "2010": "balancereg_2010_csv", "2011": "balancereg_2011_csv", "2012": "balancereg_2012_csv",
        "2013": "balancereg_2013_csv", "2014": "balancereg_2014_csv", "2015": "balancereg_2015_csv",
        "2016": "balance_reg_2016_csv", "2017": "balance_reg_2017_dec2018_csv", "2018": "balance_reg_2018_dec2019_csv",
        "2019": "balance_reg_2019_dec2020_csv", "2020": "balance_reg_2020_dec2021_csv",
        "2021": "balance_reg_2021_dec2022_csv", "2022": "balance_reg_2022_dec2023_csv",
        "2023": "balance_reg_2023_dec2024_csv", "2024": "balance_reg_2024_dec2025_csv",
        "2025": "balance_reg_2025_juil2026csv"}),
}
FORMULES = "ofgl.formules-agregats"
URL_FORMULES = ("https://data.ofgl.fr/api/explore/v2.1/catalog/datasets/methodologie-ofgl-formules-des-agregats-financiers"
                "/exports/csv?select=type_collectivite,annee,agregat,type_calcul,budgets,nomenclatures,"
                "ensemble_collectivites,remarques,formule&order_by=type_collectivite,annee,agregat,type_calcul,budgets,"
                "nomenclatures,remarques")
# Les montants d'une ligne, dans l'ordre des fichiers : balance d'entrée, opérations budgétaires (nettes des annulations,
# opérations d'ordre budgétaires comprises), opérations non budgétaires, opérations d'ordre budgétaires, au débit et au
# crédit, puis solde de sortie débiteur et créditeur.
MONTANTS = ["bedeb", "becre", "obnetdeb", "obnetcre", "onbdeb", "onbcre", "oobdeb", "oobcre", "sd", "sc"]
# Les en-têtes des fichiers : champ du fichier → nom retenu par la base, les montants en minuscules.
ENTETES = {
    # 2010 à 2015 : le type de budget est « BP » ou « BA », la catégorie de collectivité est « TYPE ».
    "ancien": (["EXER", "IDENT", "NDEPT", "LBUDG", "INSEE", "BUDGET", "NOMEN", "FINESS", "SIREN", "CREGI", "TYPE", "TYPEC",
                "BAL", "COMPTE"] + [m.upper() for m in MONTANTS],
               {"EXER": "exercice", "IDENT": "budget", "NDEPT": "departement", "LBUDG": "nom", "BUDGET": "type_budget",
                "NOMEN": "nomenclature", "SIREN": "siren", "CREGI": "region", "TYPE": "categorie", "COMPTE": "compte"}),
    # 2016 : le type de budget est un code (« 1 » pour le budget principal) ; pas de catégorie de collectivité.
    "2016": (["EXER", "IDENT", "NDEPT", "LBUDG", "INSEE", "SIREN", "CREGI", "NOMEN", "CTYPE", "CSTYP", "CACTI", "FINESS",
              "SECTEUR", "CBUDG", "CODBUD1", "COMPTE"] + [m.upper() for m in MONTANTS],
             {"EXER": "exercice", "IDENT": "budget", "NDEPT": "departement", "LBUDG": "nom", "CBUDG": "type_budget",
              "NOMEN": "nomenclature", "SIREN": "siren", "CREGI": "region", "COMPTE": "compte"}),
    # Depuis 2017 : le type de budget est un code (« 1 » pour le budget principal), la catégorie « CATEG ».
    "nouveau": (["EXER", "IDENT", "NDEPT", "LBUDG", "INSEE", "CBUDG", "CTYPE", "CSTYP", "NOMEN", "siren", "CREGI", "CACTI",
                 "SECTEUR", "FINESS", "CODBUD1", "CATEG", "BAL", "COMPTE"] + [m.upper() for m in MONTANTS],
                {"EXER": "exercice", "IDENT": "budget", "NDEPT": "departement", "LBUDG": "nom", "CBUDG": "type_budget",
                 "NOMEN": "nomenclature", "siren": "siren", "CREGI": "region", "CATEG": "categorie", "COMPTE": "compte"}),
}
PRINCIPAL = {"BP", "1"}  # type du budget principal ; tout autre est annexe
ANNEXES = {"BA", "2", "3"}
MONTANT = re.compile(r"-?[0-9]+(?:,[0-9]{1,2})?")
COMPTE = re.compile(r"[0-9]{1,10}[A-Z0-9]{0,4}")
FICHE = ["siren", "nom", "type_budget", "nomenclature", "categorie", "departement", "region"]


def requetes(source_id):
    """Les adresses à archiver pour une source : {adresse: (contenu, exercice)}."""
    if source_id == FORMULES:
        return {URL_FORMULES: ("formules", "")}
    if source_id not in JEUX:
        sys.exit(f"source que cet import ne lit pas : {source_id}")
    jeu, joints = JEUX[source_id]
    return {f"{PORTAIL}{jeu}/attachments/{joint}": ("balance", exercice) for exercice, joint in joints.items()}


def statut(fichier):
    """« provisoire » pour la balance publiée en juillet de l'année qui suit l'exercice, « definitif » pour celle publiée
    en décembre, qui la remplace : le nom du fichier joint le dit."""
    return "provisoire" if "juil" in fichier["url"].rsplit("/", 1)[-1] else "definitif"


def nature(fichier):
    """(contenu, exercice) de la copie : l'une de celles que cet import sait lire."""
    if fichier["source_id"] not in JEUX and fichier["source_id"] != FORMULES:
        sys.exit(f"{fichier['id']} : la source {fichier['source_id']} n'est pas lue par cet import")
    connues = requetes(fichier["source_id"])
    if fichier["url"] not in connues:
        sys.exit(f"{fichier['id']} : adresse que cet import ne sait pas lire ({fichier['url']})")
    return connues[fichier["url"]]


def centimes(texte, lieu):
    """Un montant écrit à la française (« 1234,56 ») en centimes."""
    if not MONTANT.fullmatch(texte):
        sys.exit(f"{lieu} : montant illisible « {texte} »")
    entier, _, decimales = texte.partition(",")
    signe = -1 if entier.startswith("-") else 1
    return signe * (abs(int(entier)) * 100 + int((decimales + "00")[:2]))


def texte_copie(chemin):
    """Le texte d'une copie : les fichiers de la DGFiP sont en UTF-8 ou, pour certains exercices, en Latin-1."""
    with ouvrir_copie(chemin) as f:
        octets = f.read()
    try:
        return octets.decode("utf-8-sig")
    except UnicodeDecodeError:
        return octets.decode("latin-1")


def balance(fichier):
    """(exercice, {budget: fiche}, [(budget, compte, montants en centimes…)]) d'une copie de balance. La fiche d'un
    budget donne le numéro Siren de sa collectivité, son libellé, son type (« principal » ou « annexe »), sa
    nomenclature, la catégorie de sa collectivité, son département et sa région."""
    contenu, exercice = nature(fichier)
    if contenu != "balance":
        sys.exit(f"{fichier['id']} : copie de {contenu}, pas de balance")
    lignes = texte_copie(BASE / fichier["chemin"]).splitlines()
    entete = lignes[0].split(";") if lignes else []
    forme = next((f for f, (attendu, _) in ENTETES.items() if entete == attendu), None)
    if forme is None:
        sys.exit(f"{fichier['id']} : en-tête inattendu {entete}")
    retenus = ENTETES[forme][1]
    rangs = {nom: entete.index(champ) for champ, nom in retenus.items()}
    debut = len(entete) - len(MONTANTS)
    fiches, resultat, vues = {}, [], set()
    soldes = collections.Counter()
    for n, ligne in enumerate(lignes[1:], start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        valeurs = ligne.split(";")
        if len(valeurs) != len(entete):
            sys.exit(f"{lieu} : {len(valeurs)} champs au lieu de {len(entete)}")
        v = {nom: valeurs[rang].strip() for nom, rang in rangs.items()}
        v.setdefault("categorie", "")
        if v["exercice"] != exercice:
            sys.exit(f"{lieu} : exercice « {v['exercice']} » au lieu de {exercice}")
        if not re.fullmatch(r"[0-9]{9}", v["siren"]) or not re.fullmatch(v["siren"] + r"[0-9]{5}", v["budget"]):
            sys.exit(f"{lieu} : numéro Siren ou SIRET du budget illisible « {v['siren']} », « {v['budget']} »")
        if v["type_budget"] not in PRINCIPAL | ANNEXES:
            sys.exit(f"{lieu} : type de budget inattendu « {v['type_budget']} »")
        if not COMPTE.fullmatch(v["compte"]):
            sys.exit(f"{lieu} : compte illisible « {v['compte']} »")
        fiche = {"siren": v["siren"], "nom": v["nom"],
                 "type_budget": "principal" if v["type_budget"] in PRINCIPAL else "annexe",
                 "nomenclature": v["nomenclature"], "categorie": v["categorie"], "departement": v["departement"],
                 "region": v["region"]}
        if fiches.setdefault(v["budget"], fiche) != fiche:
            sys.exit(f"{lieu} : le budget {v['budget']} a une autre fiche que sur ses lignes précédentes "
                     f"({fiches[v['budget']]}, ici {fiche})")
        if (v["budget"], v["compte"]) in vues:
            sys.exit(f"{lieu} : deuxième ligne pour le compte {v['compte']} du budget {v['budget']}")
        vues.add((v["budget"], v["compte"]))
        m = [centimes(t.strip(), lieu) for t in valeurs[debut:]]
        bedeb, becre, obnetdeb, obnetcre, onbdeb, onbcre, _, _, sd, sc = m
        if sd - sc != bedeb - becre + obnetdeb - obnetcre + onbdeb - onbcre:
            sys.exit(f"{lieu} : le solde de sortie n'est pas la balance d'entrée plus les opérations de l'exercice")
        soldes[v["budget"]] += sd - sc
        resultat.append((v["budget"], v["compte"], *m))
    if not resultat:
        sys.exit(f"{fichier['id']} : balance vide")
    desequilibres = [b for b, s in soldes.items() if s]
    if desequilibres:
        sys.exit(f"{fichier['id']} : {len(desequilibres)} budgets dont les soldes débiteurs ne sont pas égaux aux soldes "
                 f"créditeurs, dont {desequilibres[0]} ({soldes[desequilibres[0]] / 100:.2f} €)")
    if len({f["siren"] for f in fiches.values() if f["type_budget"] == "principal"}) != \
            sum(1 for f in fiches.values() if f["type_budget"] == "principal"):
        sys.exit(f"{fichier['id']} : une collectivité a plusieurs budgets principaux")
    return exercice, fiches, resultat


def inscription(fichier, *_):
    """La ligne de tables/fichiers_balances_collectivites.csv d'une copie, après contrôle de son contenu."""
    contenu, exercice = nature(fichier)
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas la date de modification du jeu de données")
    ligne = {"fichier_id": fichier["id"], "source_id": fichier["source_id"], "contenu": contenu, "exercice": exercice,
             "version": version, "statut": "", "lignes": "", "budgets": "", "collectivites": ""}
    if contenu == "formules":
        ligne["lignes"] = str(len(formules_ofgl.formules(fichier)))
        return ligne
    _, fiches, lignes = balance(fichier)
    ligne.update(statut=statut(fichier), lignes=str(len(lignes)), budgets=str(len(fiches)),
                 collectivites=str(len({f["siren"] for f in fiches.values()})))
    return ligne


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--requetes":
        for url in requetes(sys.argv[2]):
            print(url)
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    inscrits = [i for i in lire("tables/fichiers_balances_collectivites.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]])
    ecrire("tables/fichiers_balances_collectivites.csv", champs("fichiers_balances_collectivites"), inscrits + [ligne],
           cle="fichier_id")
    print(f"{ligne['fichier_id']} : {ligne['contenu']} {ligne['exercice']} ({ligne['version']}"
          + (f", {ligne['statut']}" if ligne["statut"] else "") + f"), {ligne['lignes']} lignes"
          + (f", {ligne['budgets']} budgets, {ligne['collectivites']} collectivités" if ligne["budgets"] else ""))


if __name__ == "__main__":
    main()
