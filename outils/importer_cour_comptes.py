#!/usr/bin/env python3
"""Enregistre dans la base les emplois de l'État consommés chaque année, en équivalents temps plein travaillé (ETPT),
tels que les donne le rapport de la Cour des comptes sur les résultats et la gestion budgétaire de l'État de l'année
(article 58, 4° de la loi organique relative aux lois de finances), dans le PDF archivé de ce rapport.

    python3 outils/importer_cour_comptes.py <fichier_id>

Les textes des projets de loi de règlement, puis relatifs aux résultats de la gestion, que la base lit pour 2006 à 2025
ne donnent pas d'emplois (ni « ETPT » ni « emplois » dans aucun) ; les rapports annuels de performances qui leur sont
annexés, et qui les donnent par ministère, ne sont pas accessibles ici (budget.gouv.fr refuse les robots). Le rapport de
la Cour donne ces emplois dans son texte, d'une année à l'autre en d'autres termes : pour le budget général seul, ou
pour l'ensemble de l'État, budgets annexes compris. Chaque chiffre se déclare donc dans EMPLOIS, par la page et
l'extrait de la phrase qui le donne, sa grandeur et son année ; l'extrait ne porte qu'un nombre et doit figurer une
seule fois dans le texte de la page (commun.nombre_phrase_pdf), où valider le relit (« page=42;phrase=… »). Un plafond
que la Cour cite (PLAFONDS_CITES) doit être celui que la base lit dans la loi de finances initiale ou rectificative de
l'année, et ne s'enregistre pas : la Cour et la base parlent alors du même plafond, qui dit, quand la Cour lui compare
un chiffre, ce que ce chiffre mesure (budget général seul ou budgets annexes compris). Une phrase introuvable, deux fois
dans sa page ou qui ne porte pas un nombre entier, comme un plafond cité qui n'est pas celui de la base, arrête
l'import.

Les rapports sur 2007, 2008, 2010, 2011, 2016, 2018 et 2020 ne donnent pas d'ensemble des emplois consommés ; ceux sur
2017 et 2019 ne se lisent pas (des polices composites dont le lecteur ne sait pas rendre les caractères) ; pour 2006,
la page de la Cour qui annonce le rapport ne renvoie qu'à son rapport de certification des comptes. La base n'a donc
pas de chiffre de la Cour pour ces années, sinon celui qu'un rapport suivant rappelle (2008, dans le rapport sur 2009).
Les tableaux des effectifs en milliers des rapports sur 2023 et 2024, depuis 2007, et sur 2025, depuis 2022, ne sont
pas lus : ils ne donnent pas toujours le millier le plus proche du nombre du texte (1 954 921 ETPT en 2024 y font 1 954
milliers). La période d'un chiffre est l'année des emplois, sa version la date de modification du PDF.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_pdf,
                    nombre_phrase_pdf, ressources_chiffres, table_des_chiffres)

BG, ETAT = "LOLF.BG_EMPLOIS_CONSOMMES", "LOLF.EMPLOIS_CONSOMMES"
# Rapport → [(page, extrait, année, concept, note)] : les emplois consommés que donne chaque rapport.
EMPLOIS = {
    "ccomptes.rbde-2009": [
        (42, "le nombre d’ETPT s’est établi à 2.088.767 ETPT", "2009", BG, ""),
        (42, "(contre 2.166.900", "2008", BG,
         "Rappel, dans le rapport sur 2009, des emplois de 2008, que le rapport sur 2008 ne donne pas."),
    ],
    "ccomptes.rbde-2012": [
        (134, "Pour l’ensemble de l’État, la consommation d’ETPT a ème été de 1 908 739", "2012", ETAT,
         "« Pour l'ensemble de l'État », face au plafond de la deuxième loi de finances rectificative pour 2012, "
         "budgets annexes compris ; le lecteur de PDF rend l'exposant de « 2ème » (« ème ») à côté de sa ligne, d'où "
         "sa place dans l'extrait."),
    ],
    "ccomptes.rbde-2013": [(154, "avec une consommation de 1 883 713 ETPT", "2013", ETAT, "")],
    "ccomptes.rbde-2014": [(134, "(1 877 359 ETPT contre", "2014", ETAT, "")],
    "ccomptes.rbde-2015": [(115, "(1 880 633 ETPT observés", "2015", ETAT, "")],
    "ccomptes.rbde-2021": [(121, "s’est établi en définitive à 1 914 026 ETPT", "2021", BG, "")],
    "ccomptes.rbde-2022": [(114, "budget général s’est établi à 1 903 930 ETPT", "2022", BG, "")],
    "ccomptes.rbde-2023": [
        (125, "se sont établis à 1 913 444 ETPT", "2023", BG, ""),
        (125, "(1 924 138 ETPT en intégrant les budgets annexes)", "2023", ETAT, ""),
    ],
    "ccomptes.rbde-2024": [
        (101, "1 954 921 ETPT (", "2024", BG, ""),
        (101, "(1 965 629 ETPT en intégrant les budgets annexes)", "2024", ETAT, ""),
    ],
    "ccomptes.rbde-2025": [(108, "qui s’établissent à 1 974 568 ETPT (hors budgets annexes)", "2025", BG, "")],
}
# Rapport → [(page, extrait, année, concept du plafond dans la base)] : les plafonds que citent les passages lus, en
# regard des emplois consommés ou pour rappeler celui de l'année d'avant.
PLAFONDS_CITES = {
    "ccomptes.rbde-2009": [(42, "2.108.123 ETPT, en retrait", "2009", "LOLF.BG_PLAFOND_EMPLOIS_LFI"),
                           (42, "2.120.830 ETPT en incluant les budgets annexes", "2009", "LOLF.PLAFOND_EMPLOIS_LFI")],
    "ccomptes.rbde-2012": [(134, "LFR à 1 936 014 ETPT", "2012", "LOLF.PLAFOND_EMPLOIS_LFR_REVISE")],
    "ccomptes.rbde-2013": [(153, "(sur 1 914 921 ETPT, budgets annexes", "2013", "LOLF.PLAFOND_EMPLOIS_LFI"),
                           (153, "(1 936 014 ETPT)", "2012", "LOLF.PLAFOND_EMPLOIS_LFR_REVISE")],
    "ccomptes.rbde-2014": [(134, "contre 1 906 424 prévus en LFI, budgets annexes compris", "2014",
                            "LOLF.PLAFOND_EMPLOIS_LFI")],
    "ccomptes.rbde-2015": [(115, "a été porté à 1 903 724 en LFR", "2015", "LOLF.PLAFOND_EMPLOIS_LFR_REVISE"),
                           (115, "contre 1 901 099 prévus initialement", "2015", "LOLF.PLAFOND_EMPLOIS_LFI")],
    "ccomptes.rbde-2025": [(109, "une autorisation à 2 008 200 ETPT", "2025", "LOLF.PLAFOND_EMPLOIS_LFI")],
}


def plafonds_de_la_base():
    """{(concept, année): {valeur}} des plafonds des emplois que la base lit dans les lois de finances."""
    plafonds = {}
    for r in ressources_chiffres():
        if not re.match(r"tables/chiffres/(an|senat)/", r["path"]):
            continue
        for l in lire(r["path"]):
            if "PLAFOND_EMPLOIS" in l["concept_id"] and not l["fonction_id"]:
                plafonds.setdefault((l["concept_id"], l["periode"]), set()).add(int(float(l["valeur"])))
    return plafonds


def chiffre(fichier, annee, concept_, nombre, emplacement, note):
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement,
        "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept_, "fonction_id": "", "traitements": "",
        "unite_id": "ETPT", "periode": annee, "valeur": nombre[0], "decimales": nombre[1], "statut": "definitif",
        "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": "non_consolide",
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def lignes_du_fichier(fichier):
    """Les chiffres d'une copie archivée d'un rapport de la Cour."""
    source = fichier["source_id"]
    if source not in EMPLOIS:
        sys.exit(f"{fichier['id']} : rapport sans emplois déclarés (EMPLOIS)")
    if not fichier["chemin"].endswith(".pdf"):
        sys.exit(f"{fichier['id']} : copie qui n'est pas un PDF")
    pages = lire_pdf(BASE / fichier["chemin"])
    plafonds = plafonds_de_la_base()
    for page, extrait, annee, concept_ in PLAFONDS_CITES.get(source, []):
        nombre = nombre_phrase_pdf(pages, page, extrait)
        if nombre is None:
            sys.exit(f"{fichier['id']}, page {page} : plafond cité introuvable, deux fois, ou illisible : "
                     f"« {extrait} »")
        if int(nombre[0]) not in plafonds.get((concept_, annee), set()):
            sys.exit(f"{fichier['id']}, page {page} : plafond cité {nombre[0]}, la base lit "
                     f"{sorted(plafonds.get((concept_, annee), set())) or 'aucun'} ({concept_}, {annee})")
    for page, extrait, annee, concept_, note in EMPLOIS[source]:
        nombre = nombre_phrase_pdf(pages, page, extrait)
        if nombre is None or nombre[1]:
            sys.exit(f"{fichier['id']}, page {page} : phrase introuvable, deux fois, ou qui ne porte pas un nombre "
                     f"entier : « {extrait} »")
        yield chiffre(fichier, annee, concept_, nombre, f"page={page};phrase={extrait}", note)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, list(lignes_du_fichier(fichier)), fichier["id"])
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; "
          f"{cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
