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
budgétaires de l'exercice ; pour chaque budget, la somme des soldes débiteurs est celle des soldes créditeurs. Quelques
budgets des syndicats et des établissements publics locaux ne s'équilibrent pas, tels que la DGFiP les publie : l'import
en inscrit le nombre, que cite le rapport de cohérence. Les lignes d'un budget se suivent : la lecture le vérifie, et
lit les balances budget par budget, sans les garder entières en mémoire.
L'import des formules de l'OFGL vérifie que chacune se lit (outils/formules_ofgl.py) et marque celles qui s'appliquent à
la même collectivité qu'une autre pour un agrégat, un exercice, une sorte de calcul, une sorte de budget et une
nomenclature. Chaque copie est inscrite dans tables/fichiers_balances_collectivites.csv. Ces copies sont les chiffres
eux-mêmes : la base ne les recopie pas, elle les lit. La version d'une copie est la date de modification du jeu de
données qu'annonce le portail, ou, pour une archive zip, la date la plus récente des fichiers qu'elle porte. Les balances
des communes, des groupements à fiscalité propre, des syndicats et des établissements publics locaux sont rangées dans
la Release « archives » du dépôt GitHub (archiver.py --release) ; celles de 2016 des trois dernières sont des archives
RAR, que l'import décompresse lui-même (outils/rar.py), après contrôle de leur taille et de leur CRC-32.
"""

import io
import re
import sys
import zipfile

import rar

import formules_ofgl
from commun import BASE, champs, ecrire, lire, ouvrir_copie

PORTAIL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
# Jeux de données des balances : source → (jeu, {exercice: fichier joint}). Les fichiers joints n'ont pas de nom régulier.
# Les communes ont un jeu par exercice.
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
    "dgfip.balances-communes": ("balances-comptables-des-communes-en-{exercice}", {
        "2010": "balancecommune_2010_zip", "2011": "balancecommune_2011_zip", "2012": "balancecommune_2012_zip",
        "2013": "balancecommune_2013_zip", "2014": "balancecommune_2014_zip", "2015": "balancecommune_2015_zip",
        "2016": "balance_commune_2016_zip", "2017": "balancecommune_2017_zip",
        "2018": "balance_commune_2018_dec2019_zip", "2019": "balance_commune_2019_dec2020_zip",
        "2020": "balance_commune_2020_dec2021_zip", "2021": "balance_commune_2021_dec2022_zip",
        "2022": "balance_commune_2022_dec2023_zip", "2023": "balance_commune_2023_dec2024_zip",
        "2024": "balance_commune_2024_dec2025_zip", "2025": "balance_commune_2025_juil2026zip"}),
    "dgfip.balances-gfp": ("balances-comptables-des-groupements-a-fiscalite-propre-depuis-2010", {
        "2010": "balancegfp_2010_zip", "2011": "balancegfp_2011_zip", "2012": "balancegfp_2012_zip",
        "2013": "balancegfp_2013_zip", "2014": "balancegfp_2014_zip", "2015": "balancegfp_2015_zip",
        "2016": "balance_gfp_2016_rar", "2017": "balance_gfp_2017_zip", "2018": "balance_gfpeptml_2018_dec2019_csv",
        "2019": "balance_gfpeptml_2019_dec2020_zip", "2020": "balance_gfpeptml_2020_dec2021_zip",
        "2021": "balance_gfpeptml_2021_dec2022_zip", "2022": "balance_gfpeptml_2022_dec2023_zip",
        "2023": "balance_gfpeptml_2023_dec2024_zip", "2024": "balance_gfpeptml_2024_dec2025_zip",
        "2025": "balance_gfpeptml_2025_juil2026zip"}),
    "dgfip.balances-syndicats": ("balances-comptables-des-syndicats-depuis-2010", {
        "2010": "balancesynd_2010_zip", "2011": "balancesynd_2011_zip", "2012": "balancesynd_2012_zip",
        "2013": "balancesynd_2013_zip", "2014": "balancesynd_2014_zip", "2015": "balancesynd_2015_zip",
        "2016": "balance_synd_2016_rar", "2017": "balance_synd_2017_zip", "2018": "balance_synd_2018_dec2019_zip",
        "2019": "balance_synd_2019_dec2020_zip", "2020": "balance_synd_2020_dec2021_zip",
        "2021": "balance_synd_2021_dec2022_zip", "2022": "balance_synd_2022_dec2023_zip",
        "2023": "balance_synd_2023_dec2024_zip", "2024": "balance_synd_2024_dec2025_zip",
        "2025": "balance_synd_2025_juil2026zip"}),
    "dgfip.balances-epl": ("balances-comptables-des-etablissements-publics-locaux-depuis-2010", {
        "2010": "balanceepl_2010_zip", "2011": "balanceepl_2011_zip", "2012": "balanceepl_2012_zip",
        "2013": "balanceepl_2013_zip", "2014": "balanceepl_2014_zip", "2015": "balanceepl_2015_zip",
        "2016": "balance_epl_2016_rar", "2017": "balance_epl_2017_zip", "2018": "balance_epl_2018_dec2019_zip",
        "2019": "balance_epl_2019_dec2020_zip", "2020": "balance_epl_2020_dec2021_zip",
        "2021": "balance_epl_2021_dec2022_zip", "2022": "balance_epl_2022_dec2023_zip",
        "2023": "balance_epl_2023_dec2024_zip", "2024": "balance_epl_2024_dec2025_zip",
        "2025": "balance_epl_2025_juil2026zip"}),
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
MONTANTS_LIGNE = re.compile(r"(?:-?[0-9]+(?:,[0-9]{1,2})?;){%d}-?[0-9]+(?:,[0-9]{1,2})?" % (len(MONTANTS) - 1))
# Un compte : son numéro, parfois suivi d'un suffixe (« 4513 LOT », « 4518 BAT » dans la balance des communes de 2015).
COMPTE = re.compile(r"[0-9]{1,10}[A-Z0-9]{0,4}(?: [A-Z]{1,4})?")
FICHE = ["siren", "nom", "type_budget", "nomenclature", "categorie", "departement", "region"]


def requetes(source_id):
    """Les adresses à archiver pour une source : {adresse: (contenu, exercice)}."""
    if source_id == FORMULES:
        return {URL_FORMULES: ("formules", "")}
    if source_id not in JEUX:
        sys.exit(f"source que cet import ne lit pas : {source_id}")
    jeu, joints = JEUX[source_id]
    return {f"{PORTAIL}{jeu.format(exercice=exercice)}/attachments/{joint}": ("balance", exercice)
            for exercice, joint in joints.items()}


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


def centimes(texte, fichier_id, n):
    """Un montant écrit à la française (« 1234,56 ») en centimes ; la ligne `n` du fichier le porte."""
    if not MONTANT.fullmatch(texte):
        sys.exit(f"{fichier_id}, ligne {n} : montant illisible « {texte} »")
    entier, _, decimales = texte.partition(",")
    signe = -1 if entier.startswith("-") else 1
    return signe * (abs(int(entier)) * 100 + int((decimales + "00")[:2]))


def vite(texte):
    """Un montant déjà reconnu bien écrit (MONTANTS_LIGNE) en centimes : la lecture rapide des balances de millions de
    lignes."""
    virgule = texte.find(",")
    if virgule < 0:
        return int(texte) * 100
    valeur = int(texte[:virgule] + texte[virgule + 1:])
    return valeur * 10 if len(texte) - virgule == 2 else valeur


def lignes_copie(chemin):
    """Les lignes de texte d'une copie de balance : celles du fichier csv, ou du seul fichier csv d'une archive zip ou
    RAR. Les fichiers de la DGFiP sont en UTF-8 ou, pour certains exercices, en Latin-1 : une ligne qui ne se lit pas en
    UTF-8 se lit en Latin-1."""
    with ouvrir_copie(chemin) as f:
        if str(chemin).endswith(".zip"):
            archive = zipfile.ZipFile(f)
            membres = [m for m in archive.infolist() if not m.is_dir()]
            if len(membres) != 1 or not membres[0].filename.lower().endswith(".csv"):
                sys.exit(f"{chemin} : l'archive devait porter un seul fichier csv, elle porte "
                         f"{[m.filename for m in membres]}")
            flux = archive.open(membres[0])
        elif str(chemin).endswith(".rar"):
            try:
                nom, contenu = rar.extraire(chemin)
            except rar.ErreurRar as e:
                sys.exit(f"{chemin} : {e}")
            if not nom.lower().endswith(".csv"):
                sys.exit(f"{chemin} : l'archive devait porter un fichier csv, elle porte {nom}")
            flux = io.BytesIO(contenu)
        else:
            flux = f
        with flux:
            for n, octets in enumerate(flux):
                try:
                    texte = octets.decode("utf-8")
                except UnicodeDecodeError:
                    texte = octets.decode("latin-1")
                yield texte.lstrip("\ufeff") if n == 0 else texte


def budgets(fichier, desequilibres=None):
    """Les budgets d'une copie de balance, dans l'ordre du fichier : (budget, fiche, {compte: montants en centimes}).
    La fiche d'un budget donne le numéro Siren de sa collectivité, son libellé, son type (« principal » ou
    « annexe »), sa nomenclature, la catégorie de sa collectivité, son département et sa région. Les lignes d'un
    budget se suivent dans les fichiers de la DGFiP : la lecture le vérifie, et contrôle chaque budget dès sa dernière
    ligne lue, sans garder les autres (une balance des communes a plusieurs millions de lignes). Un budget dont les
    soldes débiteurs ne sont pas égaux aux soldes créditeurs arrête la lecture, sauf si une liste `desequilibres` est
    donnée : il y est ajouté, (budget, écart en centimes)."""
    contenu, exercice = nature(fichier)
    if contenu != "balance":
        sys.exit(f"{fichier['id']} : copie de {contenu}, pas de balance")
    lignes = lignes_copie(BASE / fichier["chemin"])
    entete = next(lignes, "").rstrip("\r\n").split(";")
    forme = next((f for f, (attendu, _) in ENTETES.items() if entete == attendu), None)
    if forme is None:
        sys.exit(f"{fichier['id']} : en-tête inattendu {entete}")
    retenus = ENTETES[forme][1]
    rangs = {nom: entete.index(champ) for champ, nom in retenus.items()}
    rangs.setdefault("categorie", None)
    champs_fiche = ["exercice", "budget", "siren", "nom", "type_budget", "nomenclature", "categorie", "departement",
                    "region"]
    rang_compte, debut, largeur = rangs["compte"], len(entete) - len(MONTANTS), len(entete)
    vus, principaux = set(), set()
    courant, brut, comptes, solde = None, None, {}, 0

    def fin_de_budget():
        if solde and desequilibres is not None:
            desequilibres.append((courant, solde))
        elif solde:
            sys.exit(f"{fichier['id']} : les soldes débiteurs du budget {courant} ne sont pas égaux à ses soldes "
                     f"créditeurs ({solde / 100:.2f} €)")
        return courant, fiche, comptes

    n = 1
    for n, ligne in enumerate(lignes, start=2):
        valeurs = ligne.rstrip("\r\n").split(";")
        if len(valeurs) != largeur:
            sys.exit(f"{fichier['id']}, ligne {n} : {len(valeurs)} champs au lieu de {largeur}")
        cle = tuple(valeurs[rangs[c]].strip() if rangs[c] is not None else "" for c in champs_fiche)
        if cle != brut:
            lieu = f"{fichier['id']}, ligne {n}"
            v = dict(zip(champs_fiche, cle))
            if v["budget"] == courant:
                sys.exit(f"{lieu} : le budget {courant} a une autre fiche que sur ses lignes précédentes ({brut}, "
                         f"ici {cle})")
            if courant is not None:
                yield fin_de_budget()
            if v["budget"] in vus:
                sys.exit(f"{lieu} : les lignes du budget {v['budget']} ne se suivent pas")
            if v["exercice"] != exercice:
                sys.exit(f"{lieu} : exercice « {v['exercice']} » au lieu de {exercice}")
            if not re.fullmatch(r"[0-9]{9}", v["siren"]) or not re.fullmatch(v["siren"] + r"[0-9]{5}", v["budget"]):
                sys.exit(f"{lieu} : numéro Siren ou SIRET du budget illisible « {v['siren']} », « {v['budget']} »")
            if v["type_budget"] not in PRINCIPAL | ANNEXES:
                sys.exit(f"{lieu} : type de budget inattendu « {v['type_budget']} »")
            if v["type_budget"] in PRINCIPAL:
                if v["siren"] in principaux:
                    sys.exit(f"{lieu} : la collectivité {v['siren']} a plusieurs budgets principaux")
                principaux.add(v["siren"])
            vus.add(v["budget"])
            courant, brut, comptes, solde = v["budget"], cle, {}, 0
            fiche = {"siren": v["siren"], "nom": v["nom"],
                     "type_budget": "principal" if v["type_budget"] in PRINCIPAL else "annexe",
                     "nomenclature": v["nomenclature"], "categorie": v["categorie"],
                     "departement": v["departement"], "region": v["region"]}
        compte = valeurs[rang_compte].strip()
        if not COMPTE.fullmatch(compte):
            sys.exit(f"{fichier['id']}, ligne {n} : compte illisible « {compte} »")
        if compte in comptes:
            sys.exit(f"{fichier['id']}, ligne {n} : deuxième ligne pour le compte {compte} du budget {courant}")
        if MONTANTS_LIGNE.fullmatch(";".join(valeurs[debut:])):
            m = [vite(t) for t in valeurs[debut:]]
        else:
            m = [centimes(t.strip(), fichier["id"], n) for t in valeurs[debut:]]
        bedeb, becre, obnetdeb, obnetcre, onbdeb, onbcre, _, _, sd, sc = m
        if sd - sc != bedeb - becre + obnetdeb - obnetcre + onbdeb - onbcre:
            sys.exit(f"{fichier['id']}, ligne {n} : le solde de sortie n'est pas la balance d'entrée plus les "
                     f"opérations de l'exercice")
        solde += sd - sc
        comptes[compte] = m
    if courant is None:
        sys.exit(f"{fichier['id']} : balance vide")
    yield fin_de_budget()


def sirens_disperses(fichier):
    """(numéros Siren des collectivités dont les budgets ne se suivent pas dans une copie de balance, ceux de toutes ses
    collectivités) : une lecture rapide, sans contrôle. Les budgets de quelques établissements publics locaux sont
    dispersés."""
    lignes = lignes_copie(BASE / fichier["chemin"])
    entete = next(lignes, "").rstrip("\r\n").split(";")
    rang = entete.index("SIREN" if "SIREN" in entete else "siren")
    vus, disperses, courant = set(), set(), None
    for ligne in lignes:
        siren = ligne.split(";", rang + 1)[rang].strip()
        if siren != courant:
            if siren in vus:
                disperses.add(siren)
            vus.add(siren)
            courant = siren
    return disperses, vus


def balance(fichier):
    """(exercice, {budget: fiche}, [(budget, compte, montants en centimes…)]) d'une copie de balance, toute en mémoire :
    pour les balances des départements et des régions, de quelques centaines de milliers de lignes."""
    fiches, resultat = {}, []
    for budget, fiche, comptes in budgets(fichier, []):
        fiches[budget] = fiche
        resultat += [(budget, compte, *m) for compte, m in comptes.items()]
    return nature(fichier)[1], fiches, resultat


def inscription(fichier, *_):
    """La ligne de tables/fichiers_balances_collectivites.csv d'une copie, après contrôle de son contenu."""
    contenu, exercice = nature(fichier)
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas la date de modification du jeu de données")
    ligne = {"fichier_id": fichier["id"], "source_id": fichier["source_id"], "contenu": contenu, "exercice": exercice,
             "version": version, "statut": "", "lignes": "", "budgets": "", "collectivites": "",
             "desequilibres": ""}
    if contenu == "formules":
        ligne["lignes"] = str(len(formules_ofgl.formules(fichier)))
        return ligne
    n_lignes = n_budgets = 0
    sirens, desequilibres = set(), []
    for _, fiche, comptes in budgets(fichier, desequilibres):
        n_lignes += len(comptes)
        n_budgets += 1
        sirens.add(fiche["siren"])
    ligne.update(statut=statut(fichier), lignes=str(n_lignes), budgets=str(n_budgets), collectivites=str(len(sirens)),
                 desequilibres=str(len(desequilibres)))
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
