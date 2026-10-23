#!/usr/bin/env python3
"""Contrôle la cohérence des chiffres enregistrés et écrit controles/coherence.md.

    python3 outils/controler_coherence.py

Le contrôle de la base (valider.py) garantit que chaque chiffre est celui de sa source. Celui-ci
vérifie ce que disent les sources elles-mêmes :
1. les sommes comptables (un total égale la somme de ses composantes) ;
2. les ventilations par fonction (l'ensemble égale la somme des fonctions, chaque fonction celle de ses
   groupes ; pour le budget de l'État, chaque mission celle de ses programmes) ;
3. l'additivité des sous-secteurs, pour les soldes, les prélèvements obligatoires et les dépenses
   consolidées de l'ensemble ;
4. les passerelles entre tableaux qui présentent autrement les mêmes grandeurs ;
5. les ratios, qu'on doit retrouver à partir de leur dénominateur ;
6. les écarts entre sources pour une même grandeur.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la
demi-unité de la dernière décimale de chaque valeur en jeu. Une incohérence trouvée ici n'est pas une
erreur de la base : c'est un constat sur la source, publié tel quel. Le rapport ne contient aucune date
d'exécution, pour qu'un rapport à jour ne change pas.
"""

import collections
import itertools
import math
import re

from commun import RACINE, lire, ressources_chiffres

RAPPORT = RACINE / "controles" / "coherence.md"

# Identités comptables : total = somme signée des composantes. Viennent d'abord celles des tableaux 3.201
# à 3.214 de l'Insee, puis celle de ses tableaux de dépenses par fonction (3.301 à 3.306), enfin celles de
# ses tableaux de prélèvements obligatoires (3.216 et 3.217).
IDENTITES = [
    ("INSEE_APU.DEP_FONCTIONNEMENT", ["SEC2010.P2", "SEC2010.D1PAY", "SEC2010.D29PAY", "SEC2010.D4_HORS_D41PAY", "SEC2010.D5PAY"]),
    ("INSEE_APU.DEP_PRESTATIONS_TRANSFERTS", ["SEC2010.D62PAY", "SEC2010.D632PAY", "SEC2010.D3PAY", "SEC2010.D73PAY",
                                              "SEC2010.D7_HORS_D73PAY", "SEC2010.D9_HORS_D995PAY"]),
    ("INSEE_APU.DEP_ACTIFS_NON_FINANCIERS", ["SEC2010.P51G", "SEC2010.P52_P53_NP"]),
    ("SEC2010.TE", ["INSEE_APU.DEP_FONCTIONNEMENT", "SEC2010.D41PAY", "INSEE_APU.DEP_PRESTATIONS_TRANSFERTS",
                    "INSEE_APU.DEP_ACTIFS_NON_FINANCIERS"]),
    ("INSEE_APU.DEP_HORS_ELEMENTS_IMPUTES", ["SEC2010.TE", "-SEC2010.D122PAY", "-INSEE_APU.DEP_PRODUCTION_COMPTE_PROPRE",
                                             "-INSEE_APU.DEP_CREDITS_IMPOT"]),
    ("INSEE_APU.REC_PRODUCTION", ["SEC2010.P11", "SEC2010.P12", "INSEE_APU.REC_PAIEMENTS_PARTIELS", "SEC2010.D39REC"]),
    ("INSEE_APU.REC_REVENUS_PROPRIETE", ["SEC2010.D41REC", "SEC2010.D4_HORS_D41REC"]),
    ("INSEE_APU.REC_IMPOTS_COTISATIONS", ["SEC2010.D2REC", "SEC2010.D5REC", "SEC2010.D91REC", "SEC2010.D733REC",
                                          "SEC2010.D61REC", "SEC2010.D995REC"]),
    ("INSEE_APU.REC_AUTRES_TRANSFERTS", ["SEC2010.D73_HORS_D733REC", "SEC2010.D7_HORS_D73REC", "SEC2010.D9_HORS_D91_D995REC"]),
    ("SEC2010.TR", ["INSEE_APU.REC_PRODUCTION", "INSEE_APU.REC_REVENUS_PROPRIETE", "INSEE_APU.REC_IMPOTS_COTISATIONS",
                    "INSEE_APU.REC_AUTRES_TRANSFERTS"]),
    ("INSEE_APU.REC_HORS_ELEMENTS_IMPUTES", ["SEC2010.TR", "-SEC2010.D612REC", "-SEC2010.P12", "-INSEE_APU.REC_CREDITS_IMPOT"]),
    ("SEC2010.B9", ["SEC2010.TR", "-SEC2010.TE"]),
    ("SEC2010.TE", ["SEC2010.D1PAY", "SEC2010.P2", "SEC2010.D29_D5_D8PAY", "SEC2010.D3PAY", "SEC2010.D4PAY", "SEC2010.D62PAY",
                    "SEC2010.D632PAY", "SEC2010.D7PAY", "SEC2010.D9_HORS_D995PAY", "INSEE_APU.DEP_ACTIFS_NON_FINANCIERS"]),
    ("INSEE_PO.IMPOTS_ET_COTISATIONS", ["SEC2010.D211REC", "SEC2010.D212REC", "SEC2010.D214REC", "SEC2010.D291REC",
                                        "SEC2010.D292REC", "SEC2010.D51REC", "SEC2010.D59REC", "SEC2010.D91REC",
                                        "SEC2010.D61REC"]),
    ("SEC2010.D61REC", ["INSEE_PO.COTISATIONS_EFFECTIVES", "SEC2010.D612REC"]),
    ("INSEE_PO.AJUSTEMENT_COTISATIONS_IMPUTEES", ["-SEC2010.D612REC"]),
    ("INSEE_PO.AJUSTEMENT_CREDITS_IMPOT", ["INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_IMPUTES", "INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_RESTITUES"]),
    ("INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_IMPUTES", ["INSEE_PO.CI_IRPP_IMPUTES", "INSEE_PO.CI_IS_IMPUTES"]),
    ("INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_RESTITUES", ["INSEE_PO.CI_IRPP_RESTITUES", "INSEE_PO.CI_IS_RESTITUES"]),
    ("INSEE_PO.PO", ["INSEE_PO.IMPOTS_ET_COTISATIONS", "SEC2010.D995REC", "INSEE_PO.AJUSTEMENT_COTISATIONS_IMPUTEES",
                     "INSEE_PO.AJUSTEMENT_CREDITS_IMPOT"]),
    ("INSEE_PO.PO", ["INSEE_PO.PO_IMPOTS", "INSEE_PO.PO_COTISATIONS"]),
    ("INSEE_PO.TAXE_FONCIERE", ["INSEE_PO.TAXE_FONCIERE_MENAGES", "INSEE_PO.TAXE_FONCIERE_HORS_MENAGES"]),
    ("INSEE_PO.DMTG", ["INSEE_PO.DMTG_DONATIONS", "INSEE_PO.DMTG_SUCCESSIONS"]),
    ("LOLF.RESULTAT_EXECUTION", ["LOLF.SOLDE_BUDGET_GENERAL", "LOLF.SOLDE_COMPTES_SPECIAUX"]),
    ("SEC2010.B9", ["COMPTES_SECU.RESULTAT_COMPTABLE", "INSEE_PASSAGES.SECU_CORRECTIONS"]),
]


def _rubrique(total, code_norme):
    """Identité d'un tableau de passage : une rubrique égale la somme des corrections que la table des concepts y range."""
    return total, sorted(c["id"] for c in lire("tables/concepts.csv") if c["code_norme"] == code_norme and c["id"] != total)


# Budget de l'État : article 1er du projet de loi d'approbation des comptes, et situation mensuelle budgétaire.
IDENTITES += [
    ("LOLF.BG_RECETTES_FISCALES_NETTES", ["LOLF.BG_RECETTES_FISCALES_BRUTES", "-LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS"]),
    ("LOLF.BG_RECETTES_NETTES_HORS_FDC", ["LOLF.BG_RECETTES_FISCALES_NETTES", "LOLF.BG_RECETTES_NON_FISCALES"]),
    ("LOLF.BG_RECETTES_NETTES_HORS_PSR", ["LOLF.BG_RECETTES_NETTES_HORS_FDC", "-LOLF.BG_PRELEVEMENTS_SUR_RECETTES"]),
    ("LOLF.BG_RECETTES_NETTES", ["LOLF.BG_RECETTES_NETTES_HORS_PSR", "LOLF.BG_FONDS_DE_CONCOURS_RECETTES"]),
    ("LOLF.BG_DEPENSES_NETTES_HORS_FDC", ["LOLF.BG_DEPENSES_BRUTES_HORS_FDC", "-LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS"]),
    ("LOLF.BG_DEPENSES_NETTES", ["LOLF.BG_DEPENSES_NETTES_HORS_FDC", "LOLF.BG_FONDS_DE_CONCOURS_DEPENSES"]),
    ("LOLF.BG_DEPENSES_BRUTES", ["LOLF.BG_DEPENSES_BRUTES_HORS_FDC", "LOLF.BG_FONDS_DE_CONCOURS_DEPENSES"]),
    ("LOLF.SOLDE_BUDGET_GENERAL", ["LOLF.BG_RECETTES_NETTES", "-LOLF.BG_DEPENSES_NETTES"]),
    ("LOLF.BA_SOLDE_HORS_FDC", ["LOLF.BA_RECETTES_HORS_FDC", "-LOLF.BA_DEPENSES_HORS_FDC"]),
    ("LOLF.BA_FDC_SOLDE", ["LOLF.BA_FDC_RECETTES", "-LOLF.BA_FDC_DEPENSES"]),
    ("LOLF.SOLDE_BUDGETS_ANNEXES", ["LOLF.BA_RECETTES", "-LOLF.BA_DEPENSES"]),
    ("LOLF.CAS_SOLDE", ["LOLF.CAS_RECETTES", "-LOLF.CAS_DEPENSES"]),
    ("LOLF.CCF_SOLDE", ["LOLF.CCF_RECETTES", "-LOLF.CCF_DEPENSES"]),
    ("LOLF.COMPTES_COMMERCE_SOLDE", ["-LOLF.COMPTES_COMMERCE_SOLDE_EN_DEPENSES"]),
    ("LOLF.OPERATIONS_MONETAIRES_SOLDE", ["-LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_DEPENSES"]),
    ("LOLF.COMPTES_COMMERCE_SOLDE", ["LOLF.COMPTES_COMMERCE_SOLDE_EN_RECETTES"]),  # présentation des comptes de 2006
    ("LOLF.OPERATIONS_MONETAIRES_SOLDE", ["LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_RECETTES"]),
    ("LOLF.CS_DEPENSES", ["LOLF.CAS_DEPENSES", "LOLF.CCF_DEPENSES", "LOLF.COMPTES_COMMERCE_SOLDE_EN_DEPENSES",
                          "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_DEPENSES"]),
    ("LOLF.CS_RECETTES", ["LOLF.CAS_RECETTES", "LOLF.CCF_RECETTES"]),
    ("LOLF.CS_RECETTES", ["LOLF.CAS_RECETTES", "LOLF.CCF_RECETTES", "LOLF.COMPTES_COMMERCE_SOLDE_EN_RECETTES",
                          "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_RECETTES"]),
    ("LOLF.SOLDE_COMPTES_SPECIAUX", ["LOLF.CS_RECETTES", "-LOLF.CS_DEPENSES"]),
    ("LOLF.RESULTAT_BUDGETAIRE", ["LOLF.SOLDE_BUDGET_GENERAL", "LOLF.SOLDE_BUDGETS_ANNEXES", "LOLF.SOLDE_COMPTES_SPECIAUX"]),
    ("LOLF.SOLDE_BUDGET_GENERAL_HORS_REGULARISATION_PENSIONS",
     ["LOLF.BG_RECETTES_NETTES", "-LOLF.BG_DEPENSES_NETTES_HORS_REGULARISATION_PENSIONS"]),
    ("LOLF.RESULTAT_EXECUTION_HORS_REGULARISATION_PENSIONS",
     ["LOLF.SOLDE_BUDGET_GENERAL_HORS_REGULARISATION_PENSIONS", "LOLF.SOLDE_COMPTES_SPECIAUX"]),
    ("LOLF.RESULTAT_EXECUTION", ["LOLF.BG_RECETTES_AVANT_PSR", "-LOLF.BG_DEPENSES_Y_COMPRIS_PSR",
                                 "LOLF.SOLDE_COMPTES_SPECIAUX"]),
]
IDENTITES += [_rubrique("INSEE_PASSAGES.ETAT_OPERATIONS_FINANCIERES", "rubrique (1) du tableau 3.107"),
              _rubrique("INSEE_PASSAGES.ETAT_DROITS_CONSTATES", "rubrique (2) du tableau 3.107"),
              _rubrique("INSEE_PASSAGES.ETAT_NON_BUDGETAIRES", "rubrique (3) du tableau 3.107"),
              _rubrique("INSEE_PASSAGES.SECU_CORRECTIONS", "rubrique (1) du tableau 3.108")]

# Ensembles et leurs parties. S'additionnent : les soldes et les prélèvements obligatoires (concepts
# ADDITIFS), et les parts des sous-secteurs dans la dépense consolidée de l'ensemble des administrations
# publiques (consolidation « consolide_apu »).
DECOMPOSITIONS = [("S13", ["S1311", "S1313", "S1314"]), ("S1311", ["S13111", "S13112"]), ("S1313", ["S13131", "S13132"]),
                  ("S1314", ["S13141", "S13142"]), ("S13131", ["S131311", "S131312", "S131313", "S131314"]),
                  ("S13_S212", ["S13", "S212"]), ("S13_S212", ["S1311", "S1313", "S1314", "S212"]),
                  ("S1314", ["REGIME_GENERAL", "S1314_HORS_RG"]),
                  ("S1314_HORS_RG", ["CADES", "FRR", "AUTRES_REGIMES_SECU", "S13142"])]
ADDITIFS = {"SEC2010.B9", "INSEE_PO.PO"}

# Passerelles entre tableaux qui présentent autrement les mêmes grandeurs : (libellé, termes de gauche, termes
# de droite), chaque terme étant (source, périmètre, concept, signe) et, au besoin, (modèle de période, traitement),
# en montant, pour l'ensemble des fonctions. Une source terminée par « * » désigne toute source qui commence ainsi :
# les termes d'un même préfixe viennent d'une même source, l'une après l'autre s'il y en a plusieurs.
_LOI = "senat.pjl*"  # projets de loi d'approbation des comptes (de règlement, puis relatifs aux résultats de la
#                       gestion) publiés par le Sénat
_DECEMBRE = ("{annee}-12", "cumul_depuis_janvier")  # situation mensuelle budgétaire, cumul à fin décembre
_SMB = "insee.bdm-comptes-etat"
_IMPOTS_PRODUCTION_3217 = [("insee.t3217", "S13_S212", f"SEC2010.{c}REC", 1) for c in ("D211", "D212", "D214", "D291", "D292")]
PASSERELLES = [
    ("Cotisations sociales : tableau 3.217 contre tableau 3.201",
     [("insee.t3217", "S13_S212", "SEC2010.D61REC", 1)], [("insee.t3201", "S13", "SEC2010.D61REC", 1)]),
    ("Cotisations sociales imputées : tableau 3.217 contre tableau 3.201",
     [("insee.t3217", "S13_S212", "SEC2010.D612REC", 1)], [("insee.t3201", "S13", "SEC2010.D612REC", 1)]),
    ("Impôts et cotisations dus non recouvrables : tableau 3.217 contre tableau 3.201",
     [("insee.t3217", "S13_S212", "SEC2010.D995REC", 1)], [("insee.t3201", "S13", "SEC2010.D995REC", 1)]),
    ("Impôts en capital : tableau 3.217 contre tableau 3.201",
     [("insee.t3217", "S13_S212", "SEC2010.D91REC", 1)], [("insee.t3201", "S13", "SEC2010.D91REC", 1)]),
    ("Impôts courants sur le revenu et le patrimoine : D.51 + D.59 du tableau 3.217 contre D.5 du tableau 3.201",
     [("insee.t3217", "S13_S212", "SEC2010.D51REC", 1), ("insee.t3217", "S13_S212", "SEC2010.D59REC", 1)],
     [("insee.t3201", "S13", "SEC2010.D5REC", 1)]),
    ("Impôts sur la production et les importations reçus par les administrations publiques : D.211 + D.212 + D.214 + "
     "D.291 + D.292 du tableau 3.217, moins les impôts de l'Union européenne du tableau 3.216, contre D.2 du tableau 3.201",
     _IMPOTS_PRODUCTION_3217 + [("insee.t3216", "S212", "INSEE_PO.PO", -1)], [("insee.t3201", "S13", "SEC2010.D2REC", 1)]),
    ("Même passerelle, avec les impôts de l'Union européenne du tableau 3.217",
     _IMPOTS_PRODUCTION_3217 + [("insee.t3217", "S212", "INSEE_PO.PO", -1)], [("insee.t3201", "S13", "SEC2010.D2REC", 1)]),
    ("Crédits d'impôt retranchés des prélèvements obligatoires (3.217) contre crédits d'impôt enregistrés en recettes "
     "(3.201), de signe opposé",
     [("insee.t3217", "S13_S212", "INSEE_PO.AJUSTEMENT_CREDITS_IMPOT", 1)],
     [("insee.t3201", "S13", "INSEE_APU.REC_CREDITS_IMPOT", -1)]),
    ("Prélèvements obligatoires des administrations publiques : impôts nationaux du tableau 3.217 contre somme des "
     "sous-secteurs du tableau 3.216",
     [("insee.t3217", "S13", "INSEE_PO.PO", 1)], [("insee.t3216", p, "INSEE_PO.PO", 1) for p in ("S1311", "S1313", "S1314")]),
    ("Solde général d'exécution à fin décembre (situation mensuelle) contre soldes du budget général et des comptes "
     "spéciaux du projet de loi d'approbation des comptes",
     [(_SMB, "ETAT_LF", "LOLF.RESULTAT_EXECUTION", 1, *_DECEMBRE)],
     [(_LOI, "ETAT_LF", "LOLF.SOLDE_BUDGET_GENERAL", 1), (_LOI, "ETAT_LF", "LOLF.SOLDE_COMPTES_SPECIAUX", 1)]),
    ("Solde des comptes spéciaux à fin décembre (situation mensuelle) contre projet de loi d'approbation des comptes",
     [(_SMB, "ETAT_LF", "LOLF.SOLDE_COMPTES_SPECIAUX", 1, *_DECEMBRE)], [(_LOI, "ETAT_LF", "LOLF.SOLDE_COMPTES_SPECIAUX", 1)]),
    ("Dépenses du budget général à fin décembre (situation mensuelle) contre dépenses nettes plus prélèvements sur "
     "recettes du projet de loi d'approbation des comptes",
     [(_SMB, "ETAT_LF", "LOLF.BG_DEPENSES_Y_COMPRIS_PSR", 1, *_DECEMBRE)],
     [(_LOI, "ETAT_LF", "LOLF.BG_DEPENSES_NETTES", 1), (_LOI, "ETAT_LF", "LOLF.BG_PRELEVEMENTS_SUR_RECETTES", 1)]),
    ("Recettes du budget général à fin décembre (situation mensuelle) contre recettes nettes plus prélèvements sur "
     "recettes du projet de loi d'approbation des comptes",
     [(_SMB, "ETAT_LF", "LOLF.BG_RECETTES_AVANT_PSR", 1, *_DECEMBRE)],
     [(_LOI, "ETAT_LF", "LOLF.BG_RECETTES_NETTES", 1), (_LOI, "ETAT_LF", "LOLF.BG_PRELEVEMENTS_SUR_RECETTES", 1)]),
    ("Solde général d'exécution à fin décembre (situation mensuelle) contre résultat d'exécution des lois de finances "
     "du tableau 3.107",
     [(_SMB, "ETAT_LF", "LOLF.RESULTAT_EXECUTION", 1, *_DECEMBRE)], [("insee.t3107", "ETAT_LF", "LOLF.RESULTAT_EXECUTION", 1)]),
    ("Solde du budget général à fin décembre (situation mensuelle : recettes moins dépenses) contre tableau 3.107",
     [(_SMB, "ETAT_LF", "LOLF.BG_RECETTES_AVANT_PSR", 1, *_DECEMBRE),
      (_SMB, "ETAT_LF", "LOLF.BG_DEPENSES_Y_COMPRIS_PSR", -1, *_DECEMBRE)],
     [("insee.t3107", "ETAT_LF", "LOLF.SOLDE_BUDGET_GENERAL", 1)]),
    ("Solde des comptes spéciaux à fin décembre (situation mensuelle) contre tableau 3.107",
     [(_SMB, "ETAT_LF", "LOLF.SOLDE_COMPTES_SPECIAUX", 1, *_DECEMBRE)],
     [("insee.t3107", "ETAT_LF", "LOLF.SOLDE_COMPTES_SPECIAUX", 1)]),
    ("Déficit de l'État au sens de Maastricht contre résultat d'exécution des lois de finances plus corrections (1), (2) "
     "et (3), dans le tableau 3.107",
     [("insee.t3107", "S13111", "SEC2010.B9", 1)],
     [("insee.t3107", "ETAT_LF", "LOLF.RESULTAT_EXECUTION", 1)]
     + [("insee.t3107", "S13111", f"INSEE_PASSAGES.ETAT_{c}", 1) for c in ("OPERATIONS_FINANCIERES", "DROITS_CONSTATES",
                                                                           "NON_BUDGETAIRES")]),
]

# Unités comparables entre elles une fois converties ; les autres ne se comparent qu'à elles-mêmes.
FAMILLES = {"EUR": ("euros", 1), "MIO_EUR": ("euros", 1e6), "MD_EUR": ("euros", 1e9),
            "MIO_ECU_EUR": ("écus puis euros", 1e6)}
NOMS_RATIOS = {"PC_PIB": "% du PIB", "PC_DEPENSE": "% de la dépense totale"}
REGLES = {"indique": "le PIB indiqué par la source, dans le même tableau",
          "depense": "la dépense totale du même périmètre, chez la même source",
          "libre": "non indiqué par la source : chaque série de PIB enregistrée pour l'année est essayée"}
# Deux chiffres consolidés différemment ne mesurent pas la même chose ; « sans objet » se compare à tout.
CONSOLIDATIONS_EXCLUSIVES = {"consolide", "consolide_apu", "non_consolide"}
# Statuts d'un chiffre que sa source peut encore réviser.
REVISABLES = {"provisoire", "semi_definitif", "estimation", "prevision"}


def charger():
    """Pour chaque chiffre, sa version la plus récente chez sa source."""
    derniers = {}
    for r in ressources_chiffres():
        for l in lire(r["path"]):
            cle = (l["source_id"], l["zone"], l["perimetre_id"], l["concept_id"], l["fonction_id"], l["traitements"],
                   l["unite_id"], l["periode"])
            if cle not in derniers or l["version"] > derniers[cle]["version"]:
                derniers[cle] = l
    return derniers


def valeur(ligne):
    """(valeur dans l'unité de base de sa famille, demi-unité de sa dernière décimale, famille d'unités)."""
    nom, echelle = FAMILLES.get(ligne["unite_id"], (ligne["unite_id"], 1))
    return float(ligne["valeur"]) * echelle, 0.5 * 10 ** -int(ligne["decimales"]) * echelle, nom


def depasse(ecart, marge):
    """Vrai si l'écart dépasse la marge des arrondis, au-delà des imprécisions du calcul en virgule flottante."""
    return abs(ecart) > marge * (1 + 1e-9) + 1e-9


def montant(derniers, cle):
    """Le chiffre de même fiche que `cle`, exprimé en euros : le numérateur d'un ratio."""
    for unite in ("MD_EUR", "MIO_EUR", "EUR"):
        ligne = derniers.get(cle[:6] + (unite, cle[7]))
        if ligne:
            return valeur(ligne)
    return None


# --- Les contrôles -------------------------------------------------------------------------------------

def comparer(total, parties):
    """Contrôle d'une somme : total et parties sont des lignes de la base ; une partie est (signe, ligne)."""
    t, pt, _ = valeur(total)
    somme = sum(s * valeur(l)[0] for s, l in parties)
    return {"valeur": t, "somme": somme, "juste": not depasse(t - somme, pt + sum(valeur(l)[1] for _, l in parties))}


def sommes(derniers):
    """Identités comptables, pour chaque source, périmètre, fonction et année. Une identité ne s'applique qu'à
    une source qui publie, pour ce périmètre, le total et chacune des composantes ; quand certaines manquent
    pour une fonction ou une année, la somme est dite partielle. Une identité dont une autre, du même total,
    prolonge les composantes s'efface devant elle quand la source publie aussi les composantes ajoutées."""
    groupes, publies = collections.defaultdict(dict), collections.defaultdict(set)
    for k, l in derniers.items():
        if valeur(l)[2] == "euros":
            groupes[k[:3] + k[4:]][k[3]] = l
            publies[(k[0], k[2])].add(k[3])
    resultats = []
    for (source, zone, perimetre, fonction, traitements, unite, periode), concepts in sorted(groupes.items()):
        for total, composantes in IDENTITES:
            noms = {c.lstrip("-") for c in composantes}
            parties = [(-1 if c.startswith("-") else 1, concepts[c.lstrip("-")]) for c in composantes if c.lstrip("-") in concepts]
            if total not in concepts or not parties or not noms <= publies[(source, perimetre)]:
                continue
            if any(t == total and noms < {c.lstrip("-") for c in autres} <= publies[(source, perimetre)]
                   for t, autres in IDENTITES):
                continue
            resultats.append({"source": source, "perimetre": perimetre, "fonction": fonction, "periode": periode,
                              "total": total, "complet": len(parties) == len(composantes),
                              **comparer(concepts[total], parties)})
    return resultats


def ventilations(derniers):
    """Un ensemble contre la somme de ses parties, selon la hiérarchie de la table des fonctions : l'ensemble des
    fonctions contre les divisions de la COFOG ou les missions du budget de l'État, chaque division contre ses groupes,
    chaque mission contre ses programmes. Les parties d'un ensemble sont celles que la source publie, pour cette
    grandeur, au moins une année ; s'il en manque une année, la ventilation est partielle."""
    enfants = collections.defaultdict(list)
    for f in lire("tables/fonctions.csv"):
        if "+" not in f["id"]:
            enfants[f["parent_id"]].append(f["id"])
    groupes, publiees = collections.defaultdict(dict), collections.defaultdict(set)
    for k, l in derniers.items():
        if l["unite_id"] in FAMILLES:
            groupes[k[:4] + k[5:]][k[4]] = l
            publiees[k[:4] + k[5:7]].add(k[4])
    resultats = []
    for cle, par_fonction in sorted(groupes.items()):
        source, zone, perimetre, concept, traitements, unite, periode = cle
        for parent, fils in sorted(enfants.items()):
            fils = [f for f in fils if f in publiees[cle[:6]]]
            presents = [f for f in fils if f in par_fonction]
            if parent not in par_fonction or not presents:
                continue  # pas de ventilation publiée
            resultats.append({"source": source, "perimetre": perimetre, "concept": concept, "fonction": parent,
                              "periode": periode, "complet": len(presents) == len(fils),
                              **comparer(par_fonction[parent], [(1, par_fonction[f]) for f in presents])})
    return resultats


def additivite(derniers):
    """Le solde d'un ensemble, ou sa part de la dépense consolidée de l'ensemble des administrations publiques,
    égale la somme de ceux de ses parties."""
    apu = {k[0] for k, l in derniers.items() if l["consolidation"] == "consolide_apu"}
    par_annee = collections.defaultdict(dict)
    for k, l in derniers.items():
        if valeur(l)[2] != "euros":
            continue
        if k[3] in ADDITIFS:
            # Les tableaux 3.201 à 3.214 de l'Insee publient un sous-secteur chacun : on les réunit.
            famille = "insee.t3201 à t3214" if re.fullmatch(r"insee\.t32(0[1-9]|1[0-4])", k[0]) else k[0]
        elif k[0] in apu and (l["consolidation"] == "consolide_apu" or k[2] == "S13"):
            famille = k[0]
        else:
            continue
        par_annee[(famille, k[3], k[4], k[6], k[7])][k[2]] = valeur(l)[:2] + (k[0],)
    controles, ecarts = 0, []
    for (famille, concept, fonction, unite, periode), valeurs in sorted(par_annee.items()):
        for ensemble, parties in DECOMPOSITIONS:
            if ensemble in valeurs and all(p in valeurs for p in parties):
                controles += 1
                ecart = valeurs[ensemble][0] - sum(valeurs[p][0] for p in parties)
                if depasse(ecart, valeurs[ensemble][1] + sum(valeurs[p][1] for p in parties)):
                    tableaux = sorted({valeurs[p][2] for p in [ensemble] + parties})
                    ecarts.append((famille, concept, fonction, periode, ensemble, parties, tableaux, ecart))
    return controles, ecarts


def passerelles(derniers):
    """Chaque passerelle, pour chaque année où figurent tous ses termes : écart entre les deux côtés, marge des
    arrondis, et si l'un des chiffres est encore révisable."""
    index = collections.defaultdict(dict)  # (périmètre, concept, traitement, période) → {source: ligne}, en montant
    for k, l in derniers.items():
        if k[1] == "FR" and k[4] == "" and valeur(l)[2] == "euros":
            index[(k[2], k[3], k[5], k[7])][k[0]] = l
    annees = sorted({k[7][:4] for k in derniers})

    def lignes(terme, annee):
        source, perimetre, concept = terme[:3]
        modele, traitement = terme[4:6] if len(terme) > 4 else ("{annee}", "")
        trouvees = index.get((perimetre, concept, traitement, modele.format(annee=annee)), {})
        return {s: l for s, l in trouvees.items() if (s.startswith(source[:-1]) if source.endswith("*") else s == source)}

    resultats = []
    for libelle, gauche, droite in PASSERELLES:
        termes = gauche + droite
        for annee in annees:
            candidats = [lignes(t, annee) for t in termes]
            if not all(candidats):
                continue
            # Les termes d'un même préfixe viennent d'une même source : une évaluation par source commune.
            prefixes = sorted({t[0] for t in termes if t[0].endswith("*")})
            communes = [sorted(set.intersection(*(set(c) for t, c in zip(termes, candidats) if t[0] == p))) for p in prefixes]
            for choix in itertools.product(*communes):
                retenue = dict(zip(prefixes, choix))
                choisies = [c[retenue.get(t[0], t[0])] for t, c in zip(termes, candidats)]
                ecarts = [t[3] * valeur(l)[0] * (1 if i < len(gauche) else -1) for i, (t, l) in enumerate(zip(termes, choisies))]
                marge = sum(valeur(l)[1] for l in choisies)
                resultats.append({"libelle": libelle, "annee": annee, "ecart": sum(ecarts),
                                  "revisable": any(l["statut"] in REVISABLES for l in choisies),
                                  "juste": not depasse(sum(ecarts), marge)})
    return resultats


def ratios(derniers):
    """Recalcule chaque ratio : le même chiffre en montant, divisé par chacun de ses dénominateurs possibles."""
    par_id = {l["id"]: l for l in derniers.values()}
    pib = collections.defaultdict(dict)  # (zone, année) → {source: (valeur, précision)}
    for k, l in derniers.items():
        if k[3] == "SEC2010.B1GQ" and valeur(l)[2] == "euros":
            pib[(k[1], k[7])][k[0]] = valeur(l)[:2]
    resultats = []
    for k, l in sorted(derniers.items()):
        numerateur = montant(derniers, k) if k[6] in NOMS_RATIOS else None
        if numerateur is None:
            continue
        indique = par_id.get(l["denominateur_id"])
        if indique:
            regle, attendu, candidats = "indique", indique["source_id"], dict(pib[(k[1], k[7])])
            candidats[attendu] = valeur(indique)[:2]
        elif k[6] == "PC_DEPENSE":
            total = montant(derniers, k[:4] + ("",) + k[5:])
            regle, attendu, candidats = "depense", k[0], {k[0]: total[:2]} if total else {}
        else:
            regle, attendu, candidats = "libre", None, dict(pib[(k[1], k[7])])
        (n, pn), r, pr = numerateur[:2], float(l["valeur"]), 0.5 * 10 ** -int(l["decimales"])
        par = sorted(s for s, (d, pd) in candidats.items()
                     if d and not depasse(100 * n / d - r, pr + 100 * (pn / d + abs(n) * pd / d ** 2)))
        # Les dénominateurs qui donneraient le ratio publié, arrondis compris.
        implicite = (100 * max(abs(n) - pn, 0) / (abs(r) + pr), 100 * (abs(n) + pn) / (abs(r) - pr)) if abs(r) > pr else None
        resultats.append({"cle": k, "regle": regle, "attendu": attendu, "par": par,
                          "retrouve": attendu in par if attendu else bool(par), "implicite": implicite,
                          "pib": pib[(k[1], k[7])] if k[6] == "PC_PIB" else {}})
    return resultats


def concordances(derniers):
    """Compare, pour une même grandeur dans la même famille d'unités, les valeurs de sources différentes."""
    groupes = collections.defaultdict(lambda: collections.defaultdict(dict))
    for k, l in derniers.items():
        v, precision, unite = valeur(l)
        if unite != "écus puis euros":
            groupes[k[1:6] + (unite,)][k[7]][k[0]] = (v, precision, l["consolidation"], l["statut"])
    paires = collections.defaultdict(lambda: {"comparaisons": 0, "ecarts": []})
    for grandeur, annees in groupes.items():
        for annee, sources in annees.items():
            noms = sorted(sources)
            for i, a in enumerate(noms):
                for b in noms[i + 1:]:
                    (va, pa, ca, sa), (vb, pb, cb, sb) = sources[a], sources[b]
                    if ca != cb and {ca, cb} <= CONSOLIDATIONS_EXCLUSIVES:
                        continue  # pas la même grandeur
                    p = paires[(a, b, grandeur)]
                    p["comparaisons"] += 1
                    if depasse(va - vb, pa + pb):
                        p["ecarts"].append((annee, va - vb, sa in REVISABLES or sb in REVISABLES))
    return paires


# --- Le rapport ----------------------------------------------------------------------------------------

def fr(x, decimales, signe=False):
    texte = format(x, f"{'+' if signe else ''},.{decimales}f")
    return texte.replace(",", " ").replace(".", ",").replace("-", "−")


def ecart_lisible(ecart, unite):
    if unite == "euros":
        return f"{fr(ecart / 1e6, 1, True)} M€"
    nom = {"PC_PIB": "de PIB", "PC_DEPENSE": "de dépense"}.get(unite, unite)
    return f"{fr(ecart, 1, True)} point{'s' if abs(ecart) >= 2 else ''} {nom}"


def plage(annees):
    annees = sorted(set(annees))
    if len(annees) <= 4:
        return annees[0] if len(annees) == 1 else ", ".join(annees[:-1]) + " et " + annees[-1]
    return f"{len(annees)} années entre {annees[0]} et {annees[-1]}"


def plus_grand(liste, cle=lambda e: e):
    return max(liste, key=lambda e: abs(cle(e)))


def partie_sources(derniers):
    titres = {s["id"]: s["titre"] for s in lire("tables/sources.csv")}
    versions = collections.defaultdict(str)
    for l in derniers.values():
        versions[l["source_id"]] = max(versions[l["source_id"]], l["version"])
    nombre = collections.Counter(k[0] for k in derniers)
    lignes = ["## Les sources contrôlées", "",
              "Pour chaque chiffre, la version la plus récente enregistrée chez sa source.", "",
              "| Source | Titre | Version la plus récente | Chiffres |", "|---|---|---|---|"]
    lignes += [f"| {s} | {titres.get(s, '')} | {versions[s]} | {nombre[s]} |" for s in sorted(nombre)]
    return lignes + [""]


def partielles(resultats, quoi):
    """Paragraphe sur les sommes dont des parties ne sont pas diffusées."""
    partiels = [r for r in resultats if not r["complet"]]
    if not partiels:
        return []
    ok = sum(r["juste"] for r in partiels)
    texte = (f"{len(partiels)} {quoi} ont des parties que la source ne diffuse pas (cellule vide ou marquée non "
             f"disponible). ")
    if ok == len(partiels):
        return [texte + "Pour toutes, les parties diffusées suffisent à retrouver le total à l'arrondi près : les "
                "parties absentes y sont nulles ou négligeables.", ""]
    lignes = [texte + f"Pour {ok} d'entre elles, les parties diffusées suffisent à retrouver le total à l'arrondi près : "
              f"les parties absentes y sont nulles ou négligeables. Pour les {len(partiels) - ok} autres, elles ne "
              "suffisent pas : des parties absentes ne sont pas nulles.", "",
              "| Source | Périmètre | Total | Fonction | Années | Plus grand reste (total − parties diffusées) |",
              "|---|---|---|---|---|---|"]
    regroupes = collections.defaultdict(list)
    for r in partiels:
        if not r["juste"]:
            regroupes[(r["source"], r["perimetre"], r.get("total") or r["concept"], r["fonction"])].append(r)
    for (source, perimetre, total, fonction), liste in sorted(regroupes.items()):
        r = plus_grand(liste, lambda x: x["valeur"] - x["somme"])
        lignes.append(f"| {source} | {perimetre} | {total} | {fonction or 'ensemble'} | "
                      f"{plage([x['periode'] for x in liste])} | {ecart_lisible(r['valeur'] - r['somme'], 'euros')} "
                      f"en {r['periode']} |")
    return lignes + [""]


def partie_sommes(derniers):
    resultats = sommes(derniers)
    complets = [r for r in resultats if r["complet"]]
    ecarts = [r for r in complets if not r["juste"]]
    lignes = ["## 1. Sommes comptables", "",
              "Un total contre la somme de ses composantes, pour chaque source, périmètre, fonction et année.", "",
              f"{len(complets)} sommes vérifiées avec toutes leurs composantes : {len(complets) - len(ecarts)} justes, "
              f"{len(ecarts)} en écart.", ""]
    if ecarts:
        lignes += ["| Source | Périmètre | Fonction | Année | Total | Total publié (Md€) | Somme des composantes (Md€) | Écart |",
                   "|---|---|---|---|---|---|---|---|"]
        lignes += [f"| {r['source']} | {r['perimetre']} | {r['fonction'] or 'ensemble'} | {r['periode']} | {r['total']} | "
                   f"{fr(r['valeur'] / 1e9, 4)} | {fr(r['somme'] / 1e9, 4)} | {ecart_lisible(r['valeur'] - r['somme'], 'euros')} |"
                   for r in ecarts]
        lignes.append("")
    return lignes + partielles(resultats, "sommes")


def partie_ventilations(derniers):
    resultats = ventilations(derniers)
    complets = [r for r in resultats if r["complet"]]
    ecarts = [r for r in complets if not r["juste"]]
    lignes = ["## 2. Ventilations par fonction", "",
              "Pour une même grandeur, l'ensemble des fonctions contre la somme des divisions de la COFOG ou des missions "
              "du budget de l'État, chaque division contre la somme de ses groupes, chaque mission contre celle de ses "
              "programmes.", "",
              f"{len(complets)} ventilations vérifiées avec toutes leurs parties : {len(complets) - len(ecarts)} justes, "
              f"{len(ecarts)} en écart.", ""]
    regroupes = collections.defaultdict(list)
    for r in ecarts:
        regroupes[(r["source"], r["perimetre"], r["concept"], r["fonction"])].append((r["periode"], r["valeur"] - r["somme"]))
    if regroupes:
        lignes += ["| Source | Périmètre | Grandeur | Fonction | Années en écart | Plus grand écart (total − somme) |",
                   "|---|---|---|---|---|---|"]
        for (source, perimetre, concept, parent), liste in sorted(regroupes.items()):
            annee, ecart = plus_grand(liste, lambda e: e[1])
            lignes.append(f"| {source} | {perimetre} | {concept} | {parent or 'ensemble'} | "
                          f"{plage([a for a, _ in liste])} | {ecart_lisible(ecart, 'euros')} en {annee} |")
        lignes.append("")
    return lignes + partielles(resultats, "ventilations")


def partie_additivite(derniers):
    n, ecarts = additivite(derniers)
    lignes = ["## 3. Additivité des sous-secteurs", "",
              "Le solde d'un ensemble, ses prélèvements obligatoires, ou sa dépense consolidée au niveau de l'ensemble "
              "des administrations publiques (tableau 3.307 de l'Insee), contre la somme de ceux de ses parties.", "",
              f"{n} additions vérifiées : {n - len(ecarts)} justes, {len(ecarts)} en écart.", ""]
    regroupes = collections.defaultdict(list)
    for famille, concept, fonction, annee, ensemble, parties, tableaux, ecart in ecarts:
        regroupes[(famille, concept, ensemble, tuple(parties))].append((annee, ecart, tableaux, fonction))
    if regroupes:
        lignes += ["| Tableaux | Grandeur | Ensemble | Parties | Fonctions | Années en écart | Plus grand écart |",
                   "|---|---|---|---|---|---|---|"]
        for (famille, concept, ensemble, parties), liste in sorted(regroupes.items()):
            annee, ecart, _, fonction = plus_grand(liste, lambda e: e[1])
            tableaux = ", ".join(sorted({t for _, _, ts, _ in liste for t in ts}))
            fonctions = sorted({f or "ensemble" for _, _, _, f in liste})
            lignes.append(f"| {tableaux} | {concept} | {ensemble} | {' + '.join(parties)} | "
                          f"{', '.join(fonctions) if len(fonctions) <= 3 else f'{len(fonctions)} fonctions'} | "
                          f"{plage([a for a, _, _, _ in liste])} | {ecart_lisible(ecart, 'euros')} en {annee}"
                          f"{'' if fonction == '' else f' ({fonction})'} |")
        lignes.append("")
    return lignes


def partie_passerelles(derniers):
    resultats = passerelles(derniers)
    lignes = ["## 4. Passerelles entre tableaux", "",
              "Des tableaux différents présentent autrement les mêmes grandeurs. Chaque passerelle vérifie qu'ils "
              "concordent, à l'arrondi près, pour chaque année où figurent tous ses termes.", "",
              "| Passerelle | Années vérifiées | Années en écart | dont hors chiffres révisables | "
              "Plus grand écart (gauche − droite) |", "|---|---|---|---|---|"]
    par_passerelle = collections.defaultdict(list)
    for r in resultats:
        par_passerelle[r["libelle"]].append(r)
    for libelle, _, _ in PASSERELLES:
        liste = par_passerelle.get(libelle)
        if not liste:
            continue
        ecarts = [r for r in liste if not r["juste"]]
        fermes = [r["annee"] for r in ecarts if not r["revisable"]]
        plus = plus_grand(ecarts, lambda x: x["ecart"]) if ecarts else None
        texte = f"{ecart_lisible(plus['ecart'], 'euros')} en {plus['annee']}" if plus else "aucun"
        lignes.append(f"| {libelle} | {plage([r['annee'] for r in liste])} | "
                      f"{plage([r['annee'] for r in ecarts]) if ecarts else 'aucune'} | "
                      f"{plage(fermes) if fermes else 'aucune'} | {texte} |")
    return lignes + [""]


def partie_ratios(derniers):
    resultats = ratios(derniers)
    lignes = ["## 5. Ratios", "",
              "Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé "
              "si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.", "",
              "| Dénominateur | Ratios | Retrouvés | Non retrouvés |", "|---|---|---|---|"]
    for regle, texte in REGLES.items():
        liste = [x for x in resultats if x["regle"] == regle]
        if liste:
            ok = sum(x["retrouve"] for x in liste)
            lignes.append(f"| {texte} | {len(liste)} | {ok} | {len(liste) - ok} |")
    lignes.append("")
    groupes = collections.defaultdict(list)
    for x in resultats:
        if not x["retrouve"]:
            k = x["cle"]
            groupes[(k[0], k[3], k[2], k[6], x["regle"], x["attendu"])].append(x)
    if groupes:
        lignes += ["Ratios non retrouvés :", ""]
    for (source, concept, perimetre, unite, regle, attendu), liste in sorted(groupes.items()):
        fonctions = {x["cle"][4] for x in liste}
        detail = ""
        if fonctions - {""}:
            detail = f" ({'ensemble des fonctions et ' if '' in fonctions else ''}{len(fonctions - {''})} fonctions COFOG)"
        un = len(liste) == 1
        ratio = f"{len(liste)} ratio{'' if un else 's'}{detail}"
        constat = {"indique": f"{'n’est' if un else 'ne sont'} pas retrouvé{'' if un else 's'} avec le PIB indiqué, celui de {attendu}",
                   "depense": f"{'n’est' if un else 'ne sont'} pas retrouvé{'' if un else 's'} avec la dépense totale de la même source",
                   "libre": f"{'n’est' if un else 'ne sont'} retrouvé{'' if un else 's'} avec aucune des séries de PIB enregistrées"}[regle]
        lignes.append(f"- **{source}, {concept}, {perimetre}, en {NOMS_RATIOS[unite]}** : {ratio} {constat}, "
                      f"pour {plage([x['cle'][7] for x in liste])}.")
        for s, compte in collections.Counter(s for x in liste for s in x["par"]).most_common():
            lignes.append(f"  Avec le PIB de {s}, {compte} {'est retrouvé' if compte == 1 else 'sont retrouvés'}.")
        aucun = collections.defaultdict(list)
        for x in liste:
            if not x["par"] and x["implicite"]:
                aucun[x["cle"][7]].append(x)
        for annee, xs in sorted(aucun.items()):
            bas, haut = max(x["implicite"][0] for x in xs), min(x["implicite"][1] for x in xs)
            pronom = "le" if len(xs) == 1 else "les"
            if bas > haut:
                texte = f"aucun dénominateur unique ne {pronom} reproduit"
            else:
                denominateur = "un PIB" if unite == "PC_PIB" else "une dépense totale"
                # Bornes arrondies vers l'extérieur, au million d'euros : l'intervalle affiché contient le vrai.
                texte = (f"il faudrait {denominateur} compris entre {fr(math.floor(bas / 1e6) / 1e3, 3)} et "
                         f"{fr(math.ceil(haut / 1e6) / 1e3, 3)} Md€")
            enregistres = " ; ".join(f"{s} {fr(v / 1e9, 3)} Md€" for s, (v, _) in sorted(xs[0]["pib"].items()))
            lignes.append(f"  En {annee}, aucune série enregistrée ne {pronom} retrouve ; {texte}"
                          + (f" (PIB enregistrés : {enregistres})." if enregistres else "."))
    return lignes + [""]


def partie_concordances(derniers):
    paires = concordances(derniers)
    lignes = ["## 6. Écarts entre sources pour une même grandeur", "",
              "Même concept, même périmètre, même fonction, même consolidation, même année, montants convertis dans la "
              "même unité. Les montants d'Eurostat convertis en écus avant 1999 ne sont pas comparés : ce sont les mêmes "
              "données que ses montants en euros, converties autrement.", "",
              "Un chiffre que sa source présente comme provisoire, semi-définitif, estimé ou prévu peut encore être "
              "révisé : un écart qui en touche un peut venir d'une révision entre deux versions. Les écarts « hors "
              "chiffres révisables » sont ceux où aucune des deux sources ne présente son chiffre ainsi.", "",
              "| Source A | Source B | Comparaisons | Écarts | dont hors chiffres révisables | "
              "Plus grand écart hors chiffres révisables (A − B) | Plus grand écart (A − B) |",
              "|---|---|---|---|---|---|---|"]
    resume = collections.defaultdict(lambda: {"comparaisons": 0, "ecarts": collections.defaultdict(list)})
    for (a, b, grandeur), p in paires.items():
        resume[(a, b)]["comparaisons"] += p["comparaisons"]
        resume[(a, b)]["ecarts"][grandeur[5]] += p["ecarts"]

    def textes(ecarts_par_unite, filtre):
        resultat = []
        for unite, liste in sorted(ecarts_par_unite.items()):
            liste = [e for e in liste if filtre(e)]
            if liste:
                annee, ecart, _ = plus_grand(liste, lambda e: e[1])
                resultat.append(f"{ecart_lisible(ecart, unite)} en {annee}")
        return " ; ".join(resultat) or "aucun"

    for (a, b), r in sorted(resume.items()):
        tous = [e for liste in r["ecarts"].values() for e in liste]
        fermes = [e for e in tous if not e[2]]
        lignes.append(f"| {a} | {b} | {r['comparaisons']} | {len(tous)} | {len(fermes)} | "
                      f"{textes(r['ecarts'], lambda e: not e[2])} | {textes(r['ecarts'], lambda e: True)} |")
    lignes += ["", "Détail des grandeurs en écart :", "",
               "| Source A | Source B | Grandeur | Fonctions en écart | Années en écart | dont hors chiffres révisables | "
               "Plus grand écart (A − B) |", "|---|---|---|---|---|---|---|"]
    details = collections.defaultdict(list)
    for (a, b, grandeur), p in paires.items():
        zone, perimetre, concept, fonction, traitements, unite = grandeur
        details[(a, b, zone, perimetre, concept, traitements, unite)] += [(fonction,) + e for e in p["ecarts"]]
    for (a, b, zone, perimetre, concept, traitements, unite), liste in sorted(details.items()):
        if not liste:
            continue
        fonction, annee, ecart, _ = plus_grand(liste, lambda e: e[2])
        fonctions = {e[0] for e in liste}
        fermes = [e[1] for e in liste if not e[3]]
        libelle = " ".join(x for x in (zone, perimetre, concept, traitements) if x)
        libelle += f", en {NOMS_RATIOS[unite]}" if unite in NOMS_RATIOS else ""
        ou = f" ({fonction or 'ensemble'})" if len(fonctions) > 1 else ""
        lignes.append(f"| {a} | {b} | {libelle} | {liste_de_fonctions(fonctions)} | {plage([e[1] for e in liste])} | "
                      f"{plage(fermes) if fermes else 'aucune'} | {ecart_lisible(ecart, unite)} en {annee}{ou} |")
    return lignes + [""]


def liste_de_fonctions(fonctions):
    """« ensemble », « GF01 et GF04 », ou « ensemble, 10 divisions et 42 groupes »."""
    if fonctions == {""}:
        return "ensemble"
    nommees = sorted(fonctions - {""})
    if len(nommees) <= 3:
        noms = (["ensemble"] if "" in fonctions else []) + nommees
        return noms[0] if len(noms) == 1 else ", ".join(noms[:-1]) + " et " + noms[-1]
    divisions = sum(1 for f in nommees if len(f) == 4)
    parties = (["ensemble"] if "" in fonctions else []) + [f"{n} {nom}{'s' if n > 1 else ''}" for n, nom in
                                                            ((divisions, "division"), (len(nommees) - divisions, "groupe")) if n]
    return parties[0] if len(parties) == 1 else ", ".join(parties[:-1]) + " et " + parties[-1]


def ecrire_rapport(derniers):
    lignes = ["# Cohérence des chiffres enregistrés", "",
              "Fichier généré par `outils/controler_coherence.py` à partir de la base : ne pas le modifier à la main.", "",
              "Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la "
              "demi-unité de la dernière décimale de chaque valeur en jeu. Une incohérence signalée ici est un constat "
              "sur la source, pas une erreur d'enregistrement : chaque chiffre a été relu dans sa copie archivée.", ""]
    lignes += partie_sources(derniers) + partie_sommes(derniers) + partie_ventilations(derniers)
    lignes += partie_additivite(derniers) + partie_passerelles(derniers) + partie_ratios(derniers)
    lignes += partie_concordances(derniers)
    RAPPORT.parent.mkdir(exist_ok=True)
    RAPPORT.write_text("\n".join(lignes).rstrip("\n") + "\n", encoding="utf-8")
    print(f"écrit : {RAPPORT.relative_to(RACINE)}")


if __name__ == "__main__":
    ecrire_rapport(charger())
