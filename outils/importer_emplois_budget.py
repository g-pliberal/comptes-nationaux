#!/usr/bin/env python3
"""Enregistre dans la base les emplois de l'État consommés de 2018 à 2020, en équivalents temps plein travaillé (ETPT),
tels que la direction du budget les publie sur data.economie.gouv.fr avec les données des projets de loi de règlement.

    python3 outils/importer_emplois_budget.py <fichier_id>

Deux sortes de copies :

- pour 2018 (budget.emplois-plr2018), l'export csv du jeu « Projet de loi de règlement 2018 (PLR 2018) » qui donne,
  programme par programme, les crédits et les emplois consommés (colonne « exec_etpt_2018_rap_2018 ») : une ligne par
  programme du budget général ou d'un budget annexe qui en a, sans total ni somme par mission ;
- pour 2019 et 2020 (budget.emplois-plr2019, budget.emplois-plr2020), la feuille « Emplois » du classeur de synthèse des
  rapports annuels de performances (« RAP_synthese_2019.xls », « RAP2020_synthese.xls ») : une ligne par budget (budget
  général, budgets annexes), par mission, par programme et par catégorie d'emploi, avec, pour les « emplois rémunérés par
  le programme », la réalisation de l'année précédente et ses transferts de gestion, puis, pour l'année, le plafond de la
  loi de finances initiale et des lois rectificatives (« LFI + LFR »), les transferts de gestion, la réalisation et
  l'écart de la réalisation à ce plafond corrigé des transferts. L'import lit la réalisation de l'année et son écart au
  plafond pour chaque budget, chaque mission et chaque programme (pas les catégories d'emploi), et la réalisation de
  l'année précédente pour chaque budget seulement : la synthèse la reprend à sa manière, qui n'est pas toujours le
  chiffre que publie la synthèse de cette année-là (1 919 313,81 ETPT au budget général en 2019 dans la synthèse de
  2020, 1 919 294,81 dans celle de 2019), et la base enregistre les deux. Le classeur « PLR2019-emplois.xls » ou
  « PLR2020-emplois.xls » du même jeu, archivé dans la même source, donne la réalisation de l'année programme par
  programme : chacune doit être celle de la synthèse, sinon l'import s'arrête ; il n'en enregistre pas de chiffre.

Une mission est la fonction LOLF.<mission>, un programme la fonction LOLF.<mission>.<programme>, formées de leurs
libellés comme dans les lois de finances (importer_lois_resultats.code_lolf), créées s'il le faut. Un budget annexe a
pour concepts ceux des budgets annexes (LOLF.BA_…), le budget général ceux du budget général (LOLF.BG_…). Une case vide
ne donne pas de chiffre. Les en-têtes de la feuille, ses années et les intitulés de ses colonnes doivent être ceux
qu'attend l'import, sinon il s'arrête. Le plafond « LFI + LFR » de chaque budget doit être celui que la base lit dans la
dernière loi de finances de l'année qui le fixe (loi rectificative, à défaut loi initiale), sauf écart déclaré
(PLAFONDS_DIFFERENTS), et il ne s'enregistre pas. Les valeurs sont celles que gardent les cellules, débarrassées des
artefacts de la virgule flottante (commun.nombre) : le classeur garde les ETPT au centième. La période d'un chiffre est
l'année des emplois, sa version la date de modification du jeu de données.
"""

import itertools
import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_export_ofgl,
                    lire_xls, nombre, ressources_chiffres, table_des_chiffres)
from importer_lois_resultats import code_lolf

SOURCE = re.compile(r"budget\.emplois-plr([0-9]{4})")
CONCEPTS = {"BG": ("LOLF.BG_EMPLOIS_CONSOMMES", "LOLF.BG_EMPLOIS_ECART_PLAFOND", "LOLF.BG_PLAFOND_EMPLOIS"),
            "BA": ("LOLF.BA_EMPLOIS_CONSOMMES", "LOLF.BA_EMPLOIS_ECART_PLAFOND", "LOLF.BA_PLAFOND_EMPLOIS")}
# Export csv de 2018 : le type de budget de chaque ligne qui porte des emplois (les comptes spéciaux n’en ont pas).
BUDGETS_CSV = {"Budget général": "BG", "Budgets annexes": "BA"}
# Feuille « Emplois » de la synthèse : (colonne, intitulé de la ligne 2, décalage de l'année de la ligne 3).
COLONNES = [("E", "Transferts de gestion (1)", -1), ("F", "Réalisation (2)", -1), ("G", "LFI + LFR (3)", 0),
            ("H", "Transferts de gestion (4)", 0), ("I", "Réalisation (5)", 0),
            ("J", "Ecart à LFI + LFR après transferts de gestion (5- (3+4)", 0)]
ENTETE = {"A2": "Nature de la", "B2": "Budget", "C2": "Code", "D2": "Libellé de la mission Libellé du programme",
          "E1": "Emplois rémunérés par le programme", "A3": "ligne", "D3": "Libellé de la catégorie d'emploi"}
NATURES = {"Budget", "Mission", "Programme", "Catégorie d'emploi"}
LIBELLES_BUDGETS = {"BG": "Budget Général", "BA": "Budget Annexe"}
# (année, budget, code du programme) → note : les programmes dont la synthèse ne donne pas la réalisation que donne le
# classeur des emplois du même jeu ; la note va au total du budget dans la synthèse.
PROGRAMMES_ABSENTS = {
    ("2019", "BG", 147): "La synthèse ne compte pas le programme 147 « Politique de la ville », que le classeur des "
                         "emplois du même jeu (« PLR2019-emplois.xls ») dit avoir consommé 19 ETPT, ni dans le budget "
                         "général ni dans la mission « Cohésion des territoires » : la synthèse de 2020 donne pour 2019 "
                         "1 919 313,81 ETPT au budget général, et 270,4 à cette mission, 19 de plus.",
}
# (année de la synthèse, budget) → note sur la réalisation de l'année précédente qu'elle reprend.
NOTES_RAPPEL = {
    ("2019", "BG"): "La synthèse ne compte pas non plus en 2018 le programme 147 « Politique de la ville », qui a "
                    "consommé 33 ETPT d'après les données du projet de loi de règlement pour 2018 "
                    "(budget.emplois-plr2018) : la somme de leurs programmes du budget général fait 1 912 239 ETPT.",
}
# (année, budget) → (plafond « LFI + LFR » de la synthèse, note) : les plafonds qui ne sont pas ceux de la base.
PLAFONDS_DIFFERENTS = {
    ("2019", "BG"): (1942303, "La synthèse de 2019 donne au budget général un plafond « LFI + LFR » de 1 942 303 ETPT, "
                              "quand la loi de finances initiale pour 2019 en fixe 1 942 308 et la loi rectificative "
                              "1 942 602 : le classeur ne dit pas d'où vient l'écart."),
}


def propre(valeur):
    return " ".join(str(valeur if valeur is not None else "").split())


def plafonds_de_la_base():
    """{(concept sans suffixe, année): plafond} : celui de la dernière loi rectificative de l'année qui le fixe, à défaut
    celui de la loi de finances initiale."""
    initiaux, revises = {}, {}
    for r in ressources_chiffres():
        if not re.match(r"tables/chiffres/(an|senat)/", r["path"]):
            continue
        for l in lire(r["path"]):
            if l["fonction_id"] or not l["concept_id"].endswith(("_PLAFOND_EMPLOIS_LFI", "_PLAFOND_EMPLOIS_LFR_REVISE")):
                continue
            base, suffixe = l["concept_id"].split("_PLAFOND_EMPLOIS_")
            cle = (base + "_PLAFOND_EMPLOIS", l["periode"])
            if suffixe == "LFI":
                initiaux[cle] = int(float(l["valeur"]))
            elif cle not in revises or l["version"] > revises[cle][0]:
                revises[cle] = (l["version"], int(float(l["valeur"])))
    return {**initiaux, **{k: v for k, (_, v) in revises.items()}}


def chiffre(fichier, emplacement, concept_, fonction, annee, valeur, note=""):
    texte, decimales = nombre(valeur)
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement,
        "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept_, "fonction_id": fonction, "traitements": "",
        "unite_id": "ETPT", "periode": annee, "valeur": texte, "decimales": decimales, "statut": "definitif",
        "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10],
        "consolidation": "non_consolide",
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def fonction_lolf(fonctions, libelle, parent=""):
    """La fonction d'une mission (sans parent) ou d'un programme (sous sa mission), créée s'il le faut ; l'apostrophe
    droite des libellés devient l'apostrophe typographique des lois de finances (« de l'État » → « de l’État »)."""
    libelle = libelle.replace("'", "’")
    identifiant_ = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
    fonctions.setdefault(identifiant_, {"id": identifiant_, "libelle": libelle, "norme_id": "LOLF", "parent_id": parent})
    return identifiant_


def lignes_export(fichier, annee, fonctions):
    """Les emplois consommés de chaque programme, d'après l'export csv du jeu de 2018."""
    entete, lignes = lire_export_ofgl(BASE / fichier["chemin"])
    colonne = f"exec_etpt_{annee}_rap_{annee}"
    attendues = {"annee_rap", "type_de_budget", "mission", "programme", colonne}
    if not attendues <= set(entete):
        sys.exit(f"{fichier['id']} : colonnes absentes de l'export : {sorted(attendues - set(entete))}")
    rang = {c: entete.index(c) for c in attendues}
    for n, valeurs in enumerate(lignes, start=2):
        v = lambda c: valeurs[rang[c]].strip()
        if v("annee_rap") != annee:
            sys.exit(f"{fichier['id']}, ligne {n} : année {v('annee_rap')}, attendu {annee}")
        if not v(colonne):
            continue
        if v("type_de_budget") not in BUDGETS_CSV:
            sys.exit(f"{fichier['id']}, ligne {n} : des emplois pour un budget inattendu : {v('type_de_budget')}")
        mission = fonction_lolf(fonctions, v("mission"))
        programme = fonction_lolf(fonctions, v("programme"), mission)
        yield chiffre(fichier, f"ligne={n};colonne={colonne}", CONCEPTS[BUDGETS_CSV[v('type_de_budget')]][0],
                      programme, annee, float(v(colonne)))


def emplois_par_programme(fichier, annee):
    """{(budget, code du programme): ETPT} du classeur « PLR<année>-emplois.xls »."""
    _, cellules = lire_xls(BASE / fichier["chemin"], "Emplois")
    attendu = ["exercice", "loi", "typeBudget", "ministere", "mission", "programme", "ETPT EXEC"]
    if [propre(cellules.get(f"{c}1")) for c in "ABCDEFG"] != attendu:
        sys.exit(f"{fichier['id']} : en-tête inattendu")
    emplois, n = {}, 2
    while f"A{n}" in cellules:
        if propre(cellules[f"A{n}"]).replace(".0", "") != annee or propre(cellules.get(f"B{n}")) != "PLR":
            sys.exit(f"{fichier['id']}, ligne {n} : exercice ou loi inattendus")
        budget, code = propre(cellules.get(f"C{n}")), int(float(cellules[f"F{n}"]))
        if budget not in CONCEPTS or (budget, code) in emplois:
            sys.exit(f"{fichier['id']}, ligne {n} : budget inattendu ou programme en double ({budget}, {code})")
        emplois[(budget, code)] = float(cellules[f"G{n}"])
        n += 1
    return emplois


def lignes_synthese(fichier, annee, fonctions, fichiers):
    _, cellules = lire_xls(BASE / fichier["chemin"], "Emplois")
    for ref, texte in ENTETE.items():
        if propre(cellules.get(ref)) != texte:
            sys.exit(f"{fichier['id']} : en-tête {ref} « {propre(cellules.get(ref))} », attendu « {texte} »")
    for col, intitule, decalage in COLONNES:
        lu, an = propre(cellules.get(f"{col}2")), cellules.get(f"{col}3")
        if lu != intitule or an != float(int(annee) + decalage):
            sys.exit(f"{fichier['id']} : colonne {col} « {lu} » ({an}), attendu « {intitule} » ({int(annee) + decalage})")
    precedente, plafonds = str(int(annee) - 1), plafonds_de_la_base()
    programmes, mission, vus = {}, None, set()
    for n in itertools.count(4):
        if f"A{n}" not in cellules:
            break
        nature, budget, code, libelle = (propre(cellules.get(f"{c}{n}")) for c in "ABCD")
        if nature not in NATURES or budget not in CONCEPTS:
            sys.exit(f"{fichier['id']}, ligne {n} : nature « {nature} » ou budget « {budget} » inattendus")
        consomme, ecart, plafond = CONCEPTS[budget]
        valeur = lambda col: cellules.get(f"{col}{n}")
        lieu = lambda col: f"feuille=Emplois;cellule={col}{n}"
        if nature == "Budget":
            if libelle != LIBELLES_BUDGETS[budget] or budget in vus:
                sys.exit(f"{fichier['id']}, ligne {n} : budget « {libelle} » inattendu ou en double")
            vus.add(budget)
            vote = plafonds.get((plafond, annee))
            if valeur("G") != vote and PLAFONDS_DIFFERENTS.get((annee, budget), (None,))[0] != valeur("G"):
                sys.exit(f"{fichier['id']}, ligne {n} : plafond « LFI + LFR » {valeur('G')}, la base lit {vote} "
                         f"({plafond}, {annee})")
            if isinstance(valeur("F"), float):
                yield chiffre(fichier, lieu("F"), consomme, "", precedente, valeur("F"),
                              " ".join([f"Réalisation de {precedente}, que reprend la synthèse des rapports annuels "
                                        f"de performances de {annee}."] + [NOTES_RAPPEL.get((annee, budget), "")]).strip())
            notes = {"I": " ".join(t for (a, b, _), t in PROGRAMMES_ABSENTS.items() if (a, b) == (annee, budget)),
                     "J": PLAFONDS_DIFFERENTS.get((annee, budget), (None, ""))[1]}
            for col, concept_ in (("I", consomme), ("J", ecart)):
                if isinstance(valeur(col), float):
                    yield chiffre(fichier, lieu(col), concept_, "", annee, valeur(col), notes[col])
            continue
        if nature == "Mission":
            mission = fonction_lolf(fonctions, libelle)
            fonction = mission
        elif nature == "Programme":
            if mission is None:
                sys.exit(f"{fichier['id']}, ligne {n} : programme sans mission")
            fonction = fonction_lolf(fonctions, libelle, mission)
            programmes[(budget, int(float(cellules[f"C{n}"])))] = valeur("I")
        else:
            continue
        for col, concept_ in (("I", consomme), ("J", ecart)):
            if isinstance(valeur(col), float):
                yield chiffre(fichier, lieu(col), concept_, fonction, annee, valeur(col))
    if vus != set(CONCEPTS):
        sys.exit(f"{fichier['id']} : budgets lus {sorted(vus)}, attendu {sorted(CONCEPTS)}")
    # La réalisation de chaque programme, contre le classeur des emplois du même jeu.
    classeurs = [f for f in fichiers if f["source_id"] == fichier["source_id"] and f["url"].endswith("emplois_xls")]
    if len(classeurs) != 1:
        sys.exit(f"{fichier['id']} : {len(classeurs)} classeurs des emplois dans la source, il en faut un")
    emplois = emplois_par_programme(classeurs[0], annee)
    for cle in sorted(set(emplois) | {k for k, v in programmes.items() if isinstance(v, float)}):
        synthese = programmes.get(cle)
        synthese = synthese if isinstance(synthese, float) else 0.0
        if abs(emplois.get(cle, 0.0) - synthese) > 0.005 and (annee, *cle) not in PROGRAMMES_ABSENTS:
            sys.exit(f"{fichier['id']} : programme {cle[1]} ({cle[0]}), {synthese} ETPT dans la synthèse, "
                     f"{emplois.get(cle)} dans {classeurs[0]['id']}")


def lignes_du_fichier(fichier, fonctions, fichiers):
    trouve = SOURCE.fullmatch(fichier["source_id"])
    if trouve is None:
        sys.exit(f"{fichier['id']} : source inattendue (attendu budget.emplois-plr<année>)")
    annee = trouve.group(1)
    if fichier["chemin"].endswith(".csv"):
        return list(lignes_export(fichier, annee, fonctions))
    if fichier["chemin"].endswith(".xls") and "synthese" in fichier["url"]:
        return list(lignes_synthese(fichier, annee, fonctions, fichiers))
    sys.exit(f"{fichier['id']} : copie qui ne se lit pas ici (le classeur des emplois se lit avec la synthèse)")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = lire("tables/fichiers.csv")
    fichier = next((f for f in fichiers if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    avant = set(fonctions)
    ajoutes, inchanges = fusionner(existants, lignes_du_fichier(fichier, fonctions, fichiers), fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte "
          f"{len(existants)} ; {len(set(fonctions) - avant)} fonctions créées")
    for f in sorted(set(fonctions) - avant):
        print(f"  fonction créée : {f}")


if __name__ == "__main__":
    main()
