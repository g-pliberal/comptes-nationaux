#!/usr/bin/env python3
"""Contrôle la cohérence des chiffres enregistrés et écrit controles/coherence.md.

    python3 outils/controler_coherence.py

Le contrôle de la base (valider.py) garantit que chaque chiffre est celui de sa source. Celui-ci
vérifie ce que disent les sources elles-mêmes :
1. les sommes comptables (un total égale la somme de ses composantes) ;
2. les ventilations par fonction (l'ensemble égale la somme des fonctions, chaque fonction celle de ses
   groupes ; pour le budget de l'État, chaque mission celle de ses programmes) ;
3. l'additivité des sous-secteurs, pour les soldes, les prélèvements obligatoires et les dépenses
   consolidées de l'ensemble, et celle des niveaux de collectivités locales, pour tous leurs montants et
   leurs nombres de budgets ;
4. les passerelles entre tableaux qui présentent autrement les mêmes grandeurs, dont les grandeurs que la
   consolidation des comptes des collectivités locales laisse inchangées ;
5. les ratios, qu'on doit retrouver à partir de leur dénominateur ;
6. les écarts entre sources pour une même grandeur ;
7. les comptes de chaque collectivité : montant consolidé, identités comptables de chacune, comptes d'une même
   collectivité dans deux jeux de données, somme des collectivités contre les totaux publiés, et chaque
   département et chaque région contre sa fiche de la DGCL.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la
demi-unité de la dernière décimale de chaque valeur en jeu, ou l'unité entière pour une source qui tronque
ses montants ; un nombre (de budgets) n'est pas arrondi. Une incohérence trouvée ici n'est pas une
erreur de la base : c'est un constat sur la source, publié tel quel. Le rapport ne contient aucune date
d'exécution, pour qu'un rapport à jour ne change pas.
"""

import collections
import itertools
import math
import re

import importer_ofgl_collectivites as ofgl
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
# Budgets annexes et comptes spéciaux, compte par compte (articles 5 et 6) : les regroupements de catégories, et le
# solde des comptes de commerce de l'article 1er. Dans ces tableaux, une case vide vaut « rien » (les comptes
# d'affectation spéciale n'ont pas de solde débiteur) : chaque regroupement s'écrit aussi avec chaque partie de ses
# catégories, et la règle des identités prolongées ne garde que la plus complète que la source publie.
def _regroupement(total, composantes):
    return [(total, list(parties)) for n in range(1, len(composantes) + 1)
            for parties in itertools.combinations(composantes, n)]


_A_CREDITS = ["AE_CONSOMMEES", "AE_OUVERTURES", "AE_ANNULATIONS", "DEPENSES", "RECETTES", "CP_OUVERTURES", "CP_ANNULATIONS",
              "SOLDES_DEBITEURS", "SOLDES_CREDITEURS"]
_A_DECOUVERT = ["DEPENSES", "RECETTES", "MAJORATIONS_DECOUVERT", "SOLDES_DEBITEURS", "SOLDES_CREDITEURS"]
for _m in _A_CREDITS:
    IDENTITES += _regroupement(f"LOLF.CS_A_CREDITS_{_m}", [f"LOLF.CAS_{_m}", f"LOLF.CCF_{_m}"])
for _m in _A_DECOUVERT:
    IDENTITES += _regroupement(f"LOLF.CS_A_DECOUVERT_{_m}", [f"LOLF.COMPTES_COMMERCE_{_m}", f"LOLF.OPERATIONS_MONETAIRES_{_m}"])
for _m in ("SOLDES_DEBITEURS", "SOLDES_CREDITEURS"):
    IDENTITES += _regroupement(f"LOLF.CS_ENSEMBLE_{_m}", [f"LOLF.CS_A_CREDITS_{_m}", f"LOLF.CS_A_DECOUVERT_{_m}"])
    IDENTITES += _regroupement(f"LOLF.CS_ENSEMBLE_{_m}", [f"LOLF.CAS_{_m}", f"LOLF.CCF_{_m}", f"LOLF.COMPTES_COMMERCE_{_m}",
                                                          f"LOLF.OPERATIONS_MONETAIRES_{_m}"])
IDENTITES += [("LOLF.COMPTES_COMMERCE_SOLDE", ["LOLF.COMPTES_COMMERCE_RECETTES", "-LOLF.COMPTES_COMMERCE_DEPENSES"])]
# Années où un compte spécial est clos et arrêté à part : les totaux de l'article 6 (hors comptes clos) et ceux des
# comptes clos se rapprochent de l'article 1er.
_CLOS = "_COMPTES_CLOS"
_HORS = "_HORS_COMPTES_CLOS"
IDENTITES += [(f"LOLF.{c}_{m}{_HORS}", [f"LOLF.{c}_{m}", f"-LOLF.{c}_{m}{_CLOS}"])
              for c in ("CAS", "CCF") for m in ("DEPENSES", "RECETTES")]  # l'article 1er ne donne que ces totaux
IDENTITES += [(f"LOLF.CS_A_CREDITS_{m}{_HORS}", [f"LOLF.CAS_{m}", f"LOLF.CCF_{m}", f"-LOLF.CS_A_CREDITS_{m}{_CLOS}"])
              for m in ("DEPENSES", "RECETTES")]
IDENTITES += [("LOLF.COMPTES_COMMERCE_SOLDE", [f"LOLF.COMPTES_COMMERCE_RECETTES{_HORS}", f"-LOLF.COMPTES_COMMERCE_DEPENSES{_HORS}",
                                              f"LOLF.COMPTES_COMMERCE_RECETTES{_CLOS}", f"-LOLF.COMPTES_COMMERCE_DEPENSES{_CLOS}"])]

# Articles liminaire, 2 et 3 des lois d'approbation des comptes : tableau de financement, compte de résultat et bilan
# de l'État, soldes structurel et effectif. Leurs lignes changent d'une année à l'autre et une case vide y vaut
# « rien » : une composante marquée « ? » peut manquer. Une identité ne s'applique pas quand la source publie une
# composante marquée « ! », qui réunit alors certaines des autres.
def _facultatives(prefixe, total, composantes, exclues=()):
    return (prefixe + total, ["?" + ("-" if c.startswith("-") else "") + prefixe + c.lstrip("-") for c in composantes]
            + ["!" + prefixe + c for c in exclues])


_TF = [("BESOIN_FINANCEMENT", ["AMORTISSEMENT_DETTE_LT", "AMORTISSEMENT_DETTE_MT", "AMORTISSEMENT_DETTES_REPRISES",
                               "ENGAGEMENTS_ETAT", "IMPACT_TRESORERIE_SOLDE_GESTION", "VARIATION_DEPOTS_GARANTIE",
                               "VARIATION_AUTRES_BESOINS_TRESORERIE"], ["AMORTISSEMENT_DETTE_MLT"]),
       ("BESOIN_FINANCEMENT", ["AMORTISSEMENT_DETTE_MLT", "AMORTISSEMENT_SNCF_RESEAU", "AMORTISSEMENT_AUTRES_DETTES",
                               "DEFICIT_A_FINANCER", "AUTRES_BESOINS_TRESORERIE"], []),
       ("AMORTISSEMENT_DETTE_MLT", ["AMORTISSEMENT_DETTE_LT", "AMORTISSEMENT_DETTE_MT", "AMORTISSEMENT_DETTE_NOMINAL",
                                    "SUPPLEMENTS_INDEXATION"], []),
       ("DEFICIT_A_FINANCER", ["DEFICIT_A_FINANCER_DEFICIT_BUDGETAIRE", "DEFICIT_A_FINANCER_DOTATION_PIA"], []),
       ("RESSOURCES_FINANCEMENT", ["EMISSIONS_DETTE_MLT", "ANNULATION_TITRES_CDP", "RESSOURCES_CDP",
                                   "VARIATION_TITRES_COURT_TERME", "VARIATION_DEPOTS_CORRESPONDANTS",
                                   "VARIATION_AVANCES_TRESORERIE", "VARIATION_COMPTE_TRESOR",
                                   "VARIATION_DISPONIBILITES_TRESOR", "AUTRES_RESSOURCES_TRESORERIE"], [])]
IDENTITES += [_facultatives("LOLF.", t, c, e) for t, c, e in _TF]
IDENTITES += [("LOLF.RESSOURCES_FINANCEMENT", ["LOLF.BESOIN_FINANCEMENT"])]
_RESULTAT = [
    ("CHARGES_FONCTIONNEMENT_DIRECT", ["CHARGES_PERSONNEL", "ACHATS_PRESTATIONS_EXTERNES", "DOTATIONS_FONCTIONNEMENT",
                                       "AUTRES_CHARGES_FONCTIONNEMENT"]),
    ("CHARGES_FONCTIONNEMENT_INDIRECT", ["SUBVENTIONS_CHARGES_SERVICE_PUBLIC", "DOTATIONS_FONCTIONNEMENT_INDIRECT",
                                         "AUTRES_CHARGES_FONCTIONNEMENT_INDIRECT"]),
    ("CHARGES_FONCTIONNEMENT", ["CHARGES_FONCTIONNEMENT_DIRECT", "CHARGES_FONCTIONNEMENT_INDIRECT"]),
    ("PRODUITS_FONCTIONNEMENT", ["VENTES_PRESTATIONS", "PRODUCTION_STOCKEE_IMMOBILISEE", "REPRISES_FONCTIONNEMENT",
                                 "AUTRES_PRODUITS_FONCTIONNEMENT"]),
    ("CHARGES_FONCTIONNEMENT_NETTES", ["CHARGES_FONCTIONNEMENT", "-PRODUITS_FONCTIONNEMENT"]),
    ("CHARGES_INTERVENTION", ["TRANSFERTS_MENAGES", "TRANSFERTS_ENTREPRISES", "TRANSFERTS_COLLECTIVITES_TERRITORIALES",
                              "TRANSFERTS_AUTRES_COLLECTIVITES", "CHARGES_GARANTIES", "DOTATIONS_INTERVENTION"]),
    ("PRODUITS_INTERVENTION", ["CONTRIBUTIONS_TIERS", "REPRISES_INTERVENTION"]),
    ("CHARGES_INTERVENTION_NETTES", ["CHARGES_INTERVENTION", "-PRODUITS_INTERVENTION"]),
    ("CHARGES_FINANCIERES", ["INTERETS", "PERTES_CHANGE", "DOTATIONS_FINANCIERES", "AUTRES_CHARGES_FINANCIERES"]),
    ("PRODUITS_FINANCIERS", ["PRODUITS_CREANCES_ACTIF_IMMOBILISE", "PRODUITS_IMMOBILISATIONS_FINANCIERES", "GAINS_CHANGE",
                             "REPRISES_FINANCIERES", "AUTRES_INTERETS_PRODUITS"]),
    ("CHARGES_FINANCIERES_NETTES", ["CHARGES_FINANCIERES", "-PRODUITS_FINANCIERS"]),
    ("CHARGES_NETTES", ["CHARGES_FONCTIONNEMENT_NETTES", "CHARGES_INTERVENTION_NETTES", "CHARGES_FINANCIERES_NETTES"]),
    ("PRODUITS_FISCAUX_NETS", ["IMPOT_REVENU", "IMPOT_SOCIETES", "TAXE_SALAIRES", "TICPE", "TVA", "ENREGISTREMENT_TIMBRE",
                               "AUTRES_PRODUITS_FISCAUX"]),
    ("AUTRES_PRODUITS_REGALIENS_NETS", ["AMENDES"]),
    ("RESSOURCES_PROPRES_UE", ["RESSOURCE_PROPRE_UE_RNB", "RESSOURCE_PROPRE_UE_TVA"]),
    # Les ressources propres de l'Union européenne sont présentées en montant négatif.
    ("PRODUITS_REGALIENS_NETS", ["PRODUITS_FISCAUX_NETS", "AUTRES_PRODUITS_REGALIENS_NETS", "RESSOURCES_PROPRES_UE"]),
    ("SOLDE_OPERATIONS_EXERCICE", ["PRODUITS_REGALIENS_NETS", "-CHARGES_NETTES"]),
]
IDENTITES += [_facultatives("COMPTES_ETAT.", t, c) for t, c in _RESULTAT]
_ACTIF = [("ACTIF_IMMOBILISE", ["IMMOBILISATIONS_INCORPORELLES", "IMMOBILISATIONS_CORPORELLES", "IMMOBILISATIONS_FINANCIERES"]),
          ("CREANCES", ["CREANCES_REDEVABLES", "CREANCES_CLIENTS", "AUTRES_CREANCES"]),
          ("ACTIF_CIRCULANT", ["STOCKS", "CREANCES", "CHARGES_CONSTATEES_AVANCE"]),
          ("TRESORERIE_ACTIF", ["DISPONIBILITES", "FONDS_BANCAIRES_CAISSE", "VALEURS_ESCOMPTEES",
                                "AUTRES_COMPOSANTES_TRESORERIE", "EQUIVALENTS_TRESORERIE", "VALEURS_MOBILIERES_PLACEMENT"]),
          ("ACTIF", ["ACTIF_IMMOBILISE", "ACTIF_CIRCULANT", "TRESORERIE_ACTIF", "COMPTES_REGULARISATION_ACTIF"])]
_LIGNES_ACTIF = sorted({t for t, _ in _ACTIF} | {c for _, cs in _ACTIF for c in cs})
IDENTITES += [_facultatives("COMPTES_ETAT.", t + s, [c + s for c in cs]) for t, cs in _ACTIF
              for s in ("", "_BRUT", "_AMORTISSEMENTS")]
IDENTITES += [(f"COMPTES_ETAT.{x}", [f"COMPTES_ETAT.{x}_BRUT", f"?-COMPTES_ETAT.{x}_AMORTISSEMENTS"]) for x in _LIGNES_ACTIF]
_PASSIF = [("DETTES_FINANCIERES", ["TITRES_NEGOCIABLES", "TITRES_NON_NEGOCIABLES", "AUTRES_EMPRUNTS",
                                   "DETTES_FINANCIERES_AUTRES_EMPRUNTS"]),
           ("DETTES_NON_FINANCIERES", ["DETTES_FONCTIONNEMENT", "DETTES_INTERVENTION", "PRODUITS_CONSTATES_AVANCE",
                                       "AUTRES_DETTES_NON_FINANCIERES"]),
           ("PROVISIONS_RISQUES_CHARGES", ["PROVISIONS_RISQUES", "PROVISIONS_CHARGES"]),
           ("TRESORERIE_PASSIF", ["CORRESPONDANTS_TRESOR", "AUTRES_TRESORERIE_PASSIF"]),
           ("PASSIF", ["DETTES_FINANCIERES", "DETTES_NON_FINANCIERES", "PROVISIONS_RISQUES_CHARGES", "AUTRES_PASSIFS",
                       "TRESORERIE_PASSIF", "COMPTES_REGULARISATION_PASSIF"]),
           ("SITUATION_NETTE", ["REPORT_EXERCICES_ANTERIEURS", "SOLDE_EXERCICES_ANTERIEURS_ATTENTE",
                                "ECARTS_REEVALUATION_INTEGRATION", "SOLDE_EXERCICE_BILAN"])]
IDENTITES += [_facultatives("COMPTES_ETAT.", t, cs) for t, cs in _PASSIF]
IDENTITES += [("COMPTES_ETAT.SITUATION_NETTE", ["COMPTES_ETAT.ACTIF", "-COMPTES_ETAT.PASSIF"])]
# Article liminaire, en points de PIB : le solde effectif (au sens de Maastricht) est la somme des soldes structurel et
# conjoncturel et des mesures ponctuelles et temporaires.
IDENTITES += [("SEC2010.B9", ["PFP.SOLDE_STRUCTUREL", "PFP.SOLDE_CONJONCTUREL", "PFP.MESURES_PONCTUELLES_TEMPORAIRES"])]
# Tableaux d'équilibre des lois de financement de la sécurité sociale : le solde est la différence des recettes et des
# dépenses, pour chaque branche comme pour l'ensemble.
IDENTITES += [("COMPTES_SECU.RESULTAT_COMPTABLE", ["COMPTES_SECU.RECETTES", "-COMPTES_SECU.DEPENSES"])]
# Situation patrimoniale de la sécurité sociale (annexe A des lois de financement) : chaque agrégat est la somme des
# postes que le tableau présente cette année-là ; le résultat de l'exercice, au bilan, est celui des tableaux
# d'équilibre et du tableau d'évolution du passif net ; le passif net, les fonds propres ; l'endettement financier
# net, l'actif financier moins le passif financier.
_BILAN_SECU = [("TOTAL_ACTIF", ["IMMOBILISATIONS", "ACTIF_FINANCIER", "ACTIF_CIRCULANT"], False),
               ("IMMOBILISATIONS", ["IMMOBILISATIONS_NON_FINANCIERES", "PRETS_DEPOTS_GARANTIE", "AVANCES_SPHERE_SOCIALE"], True),
               ("ACTIF_FINANCIER", ["VALEURS_MOBILIERES", "ENCOURS_BANCAIRE", "CREANCES_INSTRUMENTS_FINANCIERS"], True),
               ("ACTIF_CIRCULANT", ["CREANCES_PRESTATIONS", "CREANCES_ET_PRODUITS_A_RECEVOIR_COTISATIONS",
                                    "CREANCES_COTISATIONS", "PRODUITS_A_RECEVOIR_COTISATIONS",
                                    "CREANCES_ET_PRODUITS_A_RECEVOIR_ENTITES_PUBLIQUES", "CREANCES_ENTITES_PUBLIQUES",
                                    "PRODUITS_A_RECEVOIR_ETAT", "AUTRES_ACTIFS"], True),
               ("TOTAL_PASSIF", ["FONDS_PROPRES", "PROVISIONS_RISQUES_CHARGES", "PASSIF_FINANCIER", "PASSIF_CIRCULANT"], False),
               ("FONDS_PROPRES", ["DOTATIONS", "RESERVES", "REPORT_A_NOUVEAU", "RESULTAT_EXERCICE_BILAN",
                                  "RESULTAT_EN_INSTANCE_AFFECTATION", "ECART_ESTIMATION_FRR", "AUTRES_FONDS_PROPRES"], True),
               ("PASSIF_FINANCIER", ["DETTES_REPRESENTEES_PAR_UN_TITRE", "DETTES_ETABLISSEMENTS_CREDIT", "DEPOTS_RECUS",
                                     "DETTES_INSTRUMENTS_FINANCIERS", "AUTRES_DETTES_FINANCIERES"], True),
               ("PASSIF_CIRCULANT", ["DETTES_BENEFICIAIRES", "DETTES_COTISANTS", "DETTES_ENTITES_PUBLIQUES",
                                     "AUTRES_PASSIFS"], True),
               ("TOTAL_PASSIF", ["TOTAL_ACTIF"], False), ("PASSIF_NET", ["FONDS_PROPRES"], False),
               ("ENDETTEMENT_FINANCIER_NET", ["ACTIF_FINANCIER", "-PASSIF_FINANCIER"], False),
               ("RESULTAT_COMPTABLE", ["RESULTAT_EXERCICE_BILAN"], False)]
IDENTITES += [_facultatives("COMPTES_SECU.", t, c) if f else (f"COMPTES_SECU.{t}", [("-" if x.startswith("-") else "")
                                                                                  + "COMPTES_SECU." + x.lstrip("-")
                                                                                  for x in c])
              for t, c, f in _BILAN_SECU]

# Comptes des collectivités locales (agrégats de la DGCL, annexe 2A des rapports de l'OFGL) : chaque agrégat est la somme
# de ses composantes, chaque solde la différence de ses termes.
_LOCAUX = [("DEP_FONCTIONNEMENT", ["ACHATS_CHARGES_EXTERNES", "FRAIS_PERSONNEL", "CHARGES_FINANCIERES",
                                   "DEPENSES_INTERVENTION", "AUTRES_DEP_FONCTIONNEMENT"]),
           ("REC_FONCTIONNEMENT", ["IMPOTS_TAXES", "CONCOURS_ETAT", "SUBVENTIONS_PARTICIPATIONS_RECUES",
                                   "VENTES_BIENS_SERVICES", "AUTRES_REC_FONCTIONNEMENT"]),
           ("IMPOTS_TAXES", ["IMPOTS_LOCAUX", "AUTRES_IMPOTS_TAXES"]),
           ("CONCOURS_ETAT", ["DGF", "AUTRES_DOTATIONS", "PEREQUATIONS_COMPENSATIONS"]),
           ("EPARGNE_BRUTE", ["REC_FONCTIONNEMENT", "-DEP_FONCTIONNEMENT"]),
           ("EPARGNE_NETTE", ["EPARGNE_BRUTE", "-REMBOURSEMENTS_DETTE"]),
           ("DEP_INVESTISSEMENT", ["DEPENSES_EQUIPEMENT", "SUBVENTIONS_EQUIPEMENT_VERSEES", "AUTRES_DEP_INVESTISSEMENT"]),
           ("REC_INVESTISSEMENT", ["FCTVA", "DOTATIONS_SUBVENTIONS_INVESTISSEMENT", "AUTRES_REC_INVESTISSEMENT"]),
           ("DEP_TOTALES_HORS_REMBOURSEMENTS", ["DEP_FONCTIONNEMENT", "DEP_INVESTISSEMENT"]),
           ("REC_TOTALES_HORS_EMPRUNTS", ["REC_FONCTIONNEMENT", "REC_INVESTISSEMENT"]),
           ("CAPACITE_BESOIN_FINANCEMENT", ["REC_TOTALES_HORS_EMPRUNTS", "-DEP_TOTALES_HORS_REMBOURSEMENTS"]),
           ("FLUX_NET_DETTE", ["EMPRUNTS", "-REMBOURSEMENTS_DETTE"]),
           ("DEP_TOTALES", ["DEP_TOTALES_HORS_REMBOURSEMENTS", "REMBOURSEMENTS_DETTE"]),
           ("REC_TOTALES", ["REC_TOTALES_HORS_EMPRUNTS", "EMPRUNTS"]),
           ("VARIATION_FONDS_ROULEMENT", ["REC_TOTALES", "-DEP_TOTALES"])]
# Les publications de la DGCL par collectivité détaillent les impôts sans leur total, et présentent les soldes de gestion :
# l'épargne de gestion, puis l'épargne brute après charges financières ; l'annuité réunit remboursements et intérêts.
_LOCAUX += [("REC_FONCTIONNEMENT", ["IMPOTS_LOCAUX", "AUTRES_IMPOTS_TAXES", "CONCOURS_ETAT",
                                    "SUBVENTIONS_PARTICIPATIONS_RECUES", "VENTES_BIENS_SERVICES",
                                    "AUTRES_REC_FONCTIONNEMENT"]),
            ("DEPENSES_GESTION", ["DEP_FONCTIONNEMENT", "-CHARGES_FINANCIERES"]),
            ("EPARGNE_GESTION", ["REC_FONCTIONNEMENT", "-DEPENSES_GESTION"]),
            ("EPARGNE_BRUTE", ["EPARGNE_GESTION", "-CHARGES_FINANCIERES"]),
            ("ANNUITE_DETTE", ["REMBOURSEMENTS_DETTE", "INTERETS_DETTE"])]
# Les comptes de chaque collectivité publiés par l'OFGL ajoutent les dépenses et les recettes d'investissement
# remboursements et emprunts compris, et une annuité qui compte les charges financières plutôt que les seuls intérêts.
_LOCAUX += [("DEP_INVESTISSEMENT_REMBOURSEMENTS_COMPRIS", ["DEP_INVESTISSEMENT", "REMBOURSEMENTS_DETTE"]),
            ("REC_INVESTISSEMENT_EMPRUNTS_COMPRIS", ["REC_INVESTISSEMENT", "EMPRUNTS"]),
            ("DEP_TOTALES", ["DEP_FONCTIONNEMENT", "DEP_INVESTISSEMENT_REMBOURSEMENTS_COMPRIS"]),
            ("REC_TOTALES", ["REC_FONCTIONNEMENT", "REC_INVESTISSEMENT_EMPRUNTS_COMPRIS"]),
            ("ANNUITE_DETTE_CHARGES_FINANCIERES", ["REMBOURSEMENTS_DETTE", "CHARGES_FINANCIERES"])]
# Ceux des départements et des régions donnent aussi les droits de mutation après péréquation, qui ajoutent aux droits
# perçus les attributions des fonds de péréquation et en retirent les prélèvements, et l'épargne brute avant travaux en
# régie, qui ajoute ces travaux à l'épargne brute ; une collectivité sans attribution, prélèvement ou travaux en régie
# n'en a pas de ligne (« ? » : peut manquer).
_LOCAUX += [("DMTO_APRES_PEREQUATION", ["DMTO", "?ATTRIBUTIONS_PEREQUATION_DMTO", "?-PRELEVEMENTS_PEREQUATION_DMTO"]),
            ("EPARGNE_BRUTE_AVANT_TRAVAUX_REGIE", ["EPARGNE_BRUTE", "?TRAVAUX_REGIE"])]
# Ceux des SDIS détaillent leurs dépenses d'équipement, leurs frais de personnel, les participations et les subventions
# d'investissement qu'ils reçoivent : l'OFGL calcule par différence la partie « autre » de chaque total, et une partie
# nulle n'a pas de ligne. Les participations des communes figurent aussi dans les comptes des centres d'action sociale,
# sans les autres parties : cette identité-là ne s'applique qu'avec la partie « autre ».
_LOCAUX += [("DEPENSES_EQUIPEMENT", ["?EQUIPEMENT_CONSTRUCTION", "?EQUIPEMENT_VEHICULES", "?EQUIPEMENT_MATERIEL",
                                     "?EQUIPEMENT_INFORMATIQUE", "?EQUIPEMENT_AVANCES", "?AUTRES_DEPENSES_EQUIPEMENT"]),
            ("FRAIS_PERSONNEL", ["?REMUNERATIONS_TITULAIRES", "?REMUNERATIONS_VACATAIRES",
                                 "?REMUNERATIONS_AUTRES_PERSONNELS", "?AUTRES_FRAIS_PERSONNEL"]),
            ("SUBVENTIONS_PARTICIPATIONS_RECUES", ["?PARTICIPATIONS_DEPARTEMENTS", "?PARTICIPATIONS_COMMUNES",
                                                   "?PARTICIPATIONS_GFP", "?PARTICIPATIONS_REGIONS",
                                                   "AUTRES_PARTICIPATIONS_FONCTIONNEMENT"]),
            ("DOTATIONS_SUBVENTIONS_INVESTISSEMENT", ["?SUBVENTIONS_INVESTISSEMENT_BLOC_COMMUNAL",
                                                      "?SUBVENTIONS_INVESTISSEMENT_DEPARTEMENTS",
                                                      "?SUBVENTIONS_INVESTISSEMENT_REGIONS",
                                                      "?SUBVENTIONS_INVESTISSEMENT_ETAT",
                                                      "?SUBVENTIONS_INVESTISSEMENT_EUROPE",
                                                      "?SUBVENTIONS_INVESTISSEMENT_AUTRES"])]


def _local(composante):
    """Le concept d'une composante, sa marque (« ? ») et son signe gardés."""
    marque = composante[0] if composante[0] in "?!" else ""
    terme = composante[len(marque):]
    return marque + ("-" if terme.startswith("-") else "") + "COMPTES_LOCAUX." + terme.lstrip("-")


IDENTITES += [(f"COMPTES_LOCAUX.{t}", [_local(c) for c in cs]) for t, cs in _LOCAUX]

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
                  ("S1314_HORS_RG", ["CADES", "FRR", "AUTRES_REGIMES_SECU", "S13142"]),
                  ("REGIME_GENERAL", ["REGIME_GENERAL_HORS_FSV", "FSV"]), ("ROBSS_FSV", ["ROBSS", "FSV"])]
ADDITIFS = {"SEC2010.B9", "INSEE_PO.PO", "COMPTES_SECU.RESULTAT_COMPTABLE"}
# Situation patrimoniale de la sécurité sociale : un poste de l'ensemble contre la somme des lignes de ses entités, que
# le tableau ne détaille que pour certains postes et n'y donne que pour les entités concernées (« ? » : peut manquer).
DECOMPOSITIONS_PAR_CONCEPT = {f"COMPTES_SECU.{c}": [("SECU_LFSS", ["?REGIME_GENERAL_HORS_FSV", "?ACOSS", "?ROBSS",
                                                                   "?AUTRES_REGIMES_BASE", "?FSV", "?CADES", "?FRR"])]
                              for t, cs, _ in _BILAN_SECU[:8] for c in [t] + cs}
# Comptes des collectivités locales, que la source ne consolide pas entre niveaux, budgets principaux (annexe 2A) comme
# budgets annexes (2B) : chaque montant d'un niveau contre la somme de ceux des niveaux qui le composent, celui des
# groupements à fiscalité propre contre la somme de leurs types ; le nombre de budgets de l'ensemble des collectivités
# contre la somme de ceux des cinq niveaux, que la feuille « Poids des budgets annexes » donne sans les niveaux
# intermédiaires (« ! » : ne s'applique pas si la source publie ce périmètre). Les budgets principaux et annexes
# consolidés (2C, 2D) ne s'additionnent pas d'un niveau à l'autre : les flux croisés entre niveaux en sont retirés.
_NIVEAUX = [("SECTEUR_COMMUNAL", ["COMMUNES", "GFP"]),
            ("COLLECTIVITES_TERRITORIALES_GFP", ["SECTEUR_COMMUNAL", "DEPARTEMENTS", "REGIONS_CTU"]),
            ("COLLECTIVITES_TERRITORIALES_GFP", ["COMMUNES", "GFP", "DEPARTEMENTS", "REGIONS_CTU"]),
            ("COLLECTIVITES_LOCALES", ["COLLECTIVITES_TERRITORIALES_GFP", "SYNDICATS"]),
            ("COLLECTIVITES_LOCALES", ["COMMUNES", "GFP", "DEPARTEMENTS", "REGIONS_CTU", "SYNDICATS",
                                       "!COLLECTIVITES_TERRITORIALES_GFP"])]
_NIVEAUX_LOCAUX = [(f"{t}_{b}", [f"{p}_{b}" for p in ps]) for b in ("BP", "BA") for t, ps in _NIVEAUX]
_NIVEAUX_LOCAUX += [("GFP_BP", ["GFP_METROPOLES_BP", "GFP_CU_BP", "GFP_CA_BP", "GFP_CC_BP"])]
# Les totaux des publications de la DGCL par collectivité : chacun contre la somme des collectivités que la table des
# périmètres range sous lui (« ? » : une collectivité n'existe pas toutes les années, comme la Collectivité européenne
# d'Alsace, créée en 2021), puis contre celle des totaux qu'il réunit.
_SOUS = collections.defaultdict(list)
for _p in lire("tables/perimetres.csv"):
    _SOUS[_p["parent_id"]].append(_p["id"])
_ENTITES_LOCALES = [(t, ["?" + p for p in sorted(_SOUS[t])])
                    for t in ("DEPARTEMENTS_METROPOLE_BP", "DEPARTEMENTS_OUTRE_MER_BP", "REGIONS_METROPOLE_HORS_IDF_BP",
                              "REGIONS_OUTRE_MER_BP")]
_ENTITES_LOCALES += [("DEPARTEMENTS_BP", ["DEPARTEMENTS_METROPOLE_BP", "DEPARTEMENTS_OUTRE_MER_BP"]),
                     ("DEPARTEMENTS_CTU_BP", ["DEPARTEMENTS_BP", "METROPOLE_LYON_BP", "VILLE_DE_PARIS_BP",
                                              "COLLECTIVITE_DE_CORSE_BP", "CTU_MARTINIQUE_BP", "CTU_GUYANE_BP"]),
                     ("REGIONS_METROPOLE_BP", ["REGIONS_METROPOLE_HORS_IDF_BP", "REG_11_BP"]),
                     ("REGIONS_BP", ["REGIONS_METROPOLE_BP", "REGIONS_OUTRE_MER_BP"]),
                     ("REGIONS_CTU_BP", ["REGIONS_BP", "COLLECTIVITE_DE_CORSE_BP", "CTU_MARTINIQUE_BP", "CTU_GUYANE_BP"])]
DECOMPOSITIONS_PAR_CONCEPT.update({c["id"]: _NIVEAUX_LOCAUX + _ENTITES_LOCALES for c in lire("tables/concepts.csv")
                                   if c["norme_id"] == "COMPTES_LOCAUX"})

# Passerelles entre tableaux qui présentent autrement les mêmes grandeurs : (libellé, termes de gauche, termes
# de droite), chaque terme étant (source, périmètre, concept, signe) et, au besoin, (modèle de période, traitement),
# en montant, pour l'ensemble des fonctions. Une source terminée par « * » désigne toute source qui commence ainsi :
# les termes d'un même préfixe viennent d'une même source, l'une après l'autre s'il y en a plusieurs.
_LOI = "senat.pjl*"  # projets de loi d'approbation des comptes (de règlement, puis relatifs aux résultats de la
#                       gestion) publiés par le Sénat
_DECEMBRE = ("{annee}-12", "cumul_depuis_janvier")  # situation mensuelle budgétaire, cumul à fin décembre
_SMB = "insee.bdm-comptes-etat"
_SECU = "senat.*"  # lois de financement et projets de loi d'approbation des comptes de la sécurité sociale
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
    ("Déficit à financer du tableau de financement contre résultat budgétaire de l'État, de signe opposé, dans le projet "
     "de loi d'approbation des comptes",
     [(_LOI, "ETAT_LF", "LOLF.DEFICIT_A_FINANCER", 1)], [(_LOI, "ETAT_LF", "LOLF.RESULTAT_BUDGETAIRE", -1)]),
    ("Résultat comptable du régime général, Fonds de solidarité vieillesse compris (tableau 3.108), contre soldes du "
     "régime général et du FSV approuvés par la loi de financement de la sécurité sociale",
     [("insee.t3108", "REGIME_GENERAL", "COMPTES_SECU.RESULTAT_COMPTABLE", 1)],
     [(_SECU, "REGIME_GENERAL_HORS_FSV", "COMPTES_SECU.RESULTAT_COMPTABLE", 1),
      (_SECU, "FSV", "COMPTES_SECU.RESULTAT_COMPTABLE", 1)]),
    ("Dette amortie par la CADES, qu'approuve la loi de financement de la sécurité sociale, contre son résultat de "
     "l'exercice dans la situation patrimoniale (annexe A)",
     [(_SECU, "CADES", "LFSS.CADES_DETTE_AMORTIE", 1)], [(_SECU, "CADES", "COMPTES_SECU.RESULTAT_EXERCICE_BILAN", 1)]),
    ("Déficit de l'État au sens de Maastricht contre résultat d'exécution des lois de finances plus corrections (1), (2) "
     "et (3), dans le tableau 3.107",
     [("insee.t3107", "S13111", "SEC2010.B9", 1)],
     [("insee.t3107", "ETAT_LF", "LOLF.RESULTAT_EXECUTION", 1)]
     + [("insee.t3107", "S13111", f"INSEE_PASSAGES.ETAT_{c}", 1) for c in ("OPERATIONS_FINANCIERES", "DROITS_CONSTATES",
                                                                           "NON_BUDGETAIRES")]),
]

# Comptes consolidés des collectivités locales : la consolidation retire chaque flux croisé, entre les budgets d'un niveau
# (annexe 2C) ou entre niveaux (2D), des recettes comme des dépenses de la même section ; elle laisse donc inchangées la
# variation du fonds de roulement et l'épargne brute, comme la dette et la trésorerie. Pas la capacité de financement ni
# les emprunts : un prêt d'un budget à un autre est une dépense d'investissement du prêteur et un emprunt de l'autre.
_INVARIANTS_LOCAUX = {"VARIATION_FONDS_ROULEMENT": "variation du fonds de roulement", "EPARGNE_BRUTE": "épargne brute",
                      "DETTE": "dette au 31 décembre", "TRESORERIE_NETTE": "trésorerie nette au 31 décembre"}
_NIVEAUX_CONSOLIDES = {"COMMUNES": "communes", "GFP": "groupements à fiscalité propre", "DEPARTEMENTS": "départements",
                       "REGIONS_CTU": "régions et CTU", "SYNDICATS": "syndicats"}
for _code, _nom in _INVARIANTS_LOCAUX.items():
    _c = f"COMPTES_LOCAUX.{_code}"
    PASSERELLES += [(f"Collectivités locales, {_nom} : {_n}, budgets principaux et annexes consolidés (annexe 2C de "
                     f"l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B)",
                     [("ofgl.annexe-2c", f"{_p}_BP_BA", _c, 1)],
                     [("ofgl.annexe-2a", f"{_p}_BP", _c, 1), ("ofgl.annexe-2b", f"{_p}_BA", _c, 1)])
                    for _p, _n in _NIVEAUX_CONSOLIDES.items()]
    PASSERELLES += [(f"Collectivités locales, {_nom} : bloc communal consolidé (annexe 2D) contre communes plus "
                     "groupements à fiscalité propre consolidés (2C)",
                     [("ofgl.annexe-2d", "SECTEUR_COMMUNAL_BP_BA", _c, 1)],
                     [("ofgl.annexe-2c", f"{_p}_BP_BA", _c, 1) for _p in ("COMMUNES", "GFP")]),
                    (f"Collectivités locales, {_nom} : ensemble des collectivités consolidé (annexe 2D) contre ses cinq "
                     "niveaux consolidés (2C)",
                     [("ofgl.annexe-2d", "COLLECTIVITES_LOCALES_BP_BA", _c, 1)],
                     [("ofgl.annexe-2c", f"{_p}_BP_BA", _c, 1) for _p in _NIVEAUX_CONSOLIDES])]

# Ratios qui s'additionnent chez une même source pour une même année : leur dénominateur est le même.
RATIOS_ADDITIFS = {"PC_PIB", "PC_PIB_POTENTIEL"}
# Sources dont les montants ne sont exacts qu'à une unité près de leur dernière décimale, et non à une demi-unité :
# l'OFGL arrondit ou tronque selon les cas ses montants à l'euro, comme le montre leur comparaison aux montants au
# centime des publications de la DGCL ; dans ses tableaux des budgets annexes, un total s'écarte de 4 € de la somme de
# ses cinq composantes, quand l'arrondi à l'euro le plus proche en permet au plus 3.
A_UNE_UNITE_PRES = {"ofgl.annexe-2a", "ofgl.annexe-2b", "ofgl.annexe-2c", "ofgl.annexe-2d"}
# Unités de dénombrement : un nombre n'est pas arrondi, il ne laisse aucune marge.
DENOMBREMENTS = {u["id"] for u in lire("tables/unites.csv") if u["type"] == "nombre"}
# Unités comparables entre elles une fois converties ; les autres ne se comparent qu'à elles-mêmes.
FAMILLES = {"EUR": ("euros", 1), "MIO_EUR": ("euros", 1e6), "MD_EUR": ("euros", 1e9),
            "MIO_ECU_EUR": ("écus puis euros", 1e6)}
NOMS_RATIOS = {"PC_PIB": "% du PIB", "PC_DEPENSE": "% de la dépense totale"}  # ratios que l'on recalcule
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
    """(valeur dans l'unité de base de sa famille, demi-unité de sa dernière décimale, ou unité entière pour une source
    qui tronque, ou rien pour un nombre, famille d'unités)."""
    nom, echelle = FAMILLES.get(ligne["unite_id"], (ligne["unite_id"], 1))
    marge = (0 if ligne["unite_id"] in DENOMBREMENTS else 1 if ligne["source_id"] in A_UNE_UNITE_PRES else 0.5) \
        * 10 ** -int(ligne["decimales"]) * echelle
    return float(ligne["valeur"]) * echelle, marge, nom


def depasse(ecart, marge):
    """Vrai si l'écart dépasse la marge des arrondis, au-delà des imprécisions du calcul en virgule flottante."""
    return abs(ecart) > marge * (1 + 1e-9) + 1e-9


def retenu(ligne, deja):
    """Vrai si `ligne` remplace `deja` : une source peut donner une même grandeur dans deux unités d'une même famille,
    dans deux tableaux (l'annexe 2A de l'OFGL donne l'ensemble des groupements à fiscalité propre en milliards d'euros,
    et dans le tableau de leurs types, pour la dernière année de chaque rapport, en millions) ; on retient sa version la
    plus récente, puis la plus précise."""
    return deja is None or (ligne["version"], -valeur(ligne)[1]) > (deja["version"], -valeur(deja)[1])


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
    """Identités comptables, pour chaque source, périmètre, fonction et année, en montant ou dans un ratio qui
    s'additionne (RATIOS_ADDITIFS). Une identité ne s'applique qu'à une source qui publie, pour ce périmètre et dans
    cette famille d'unités, le total et chacune des composantes obligatoires ; quand certaines manquent pour une
    fonction ou une année, la somme est dite partielle. Une identité dont une autre, du même total, prolonge les
    composantes s'efface devant elle quand la source publie aussi les composantes obligatoires de celle-ci."""
    groupes, publies = collections.defaultdict(dict), collections.defaultdict(set)
    for k, l in derniers.items():
        if valeur(l)[2] == "euros" or k[6] in RATIOS_ADDITIFS:
            groupes[k[:3] + k[4:]][k[3]] = l
            publies[(k[0], k[2], valeur(l)[2])].add(k[3])

    def termes(composantes):  # (obligatoires, facultatives, exclues), sans leurs marques
        return ([c for c in composantes if c[0] not in "?!"], [c[1:] for c in composantes if c[0] == "?"],
                {c[1:] for c in composantes if c[0] == "!"})

    resultats = []
    for (source, zone, perimetre, fonction, traitements, unite, periode), concepts in sorted(groupes.items()):
        publies_ = publies[(source, perimetre, FAMILLES.get(unite, (unite,))[0])]
        for total, composantes in IDENTITES:
            obligatoires, facultatives, exclues = termes(composantes)
            noms = {c.lstrip("-") for c in obligatoires + facultatives}
            parties = [(-1 if c.startswith("-") else 1, concepts[c.lstrip("-")]) for c in obligatoires + facultatives
                       if c.lstrip("-") in concepts]
            if total not in concepts or not parties or not {c.lstrip("-") for c in obligatoires} <= publies_ or \
                    exclues & set(concepts):
                continue
            if any(t == total and noms < {c.lstrip("-") for o, f, _ in [termes(autres)] for c in o + f} and
                   {c.lstrip("-") for c in termes(autres)[0]} <= publies_ for t, autres in IDENTITES):
                continue
            resultats.append({"source": source, "perimetre": perimetre, "fonction": fonction, "periode": periode,
                              "total": total, "unite": valeur(concepts[total])[2],
                              "complet": all(c.lstrip("-") in concepts for c in obligatoires),
                              **comparer(concepts[total], parties)})
    return resultats


def ventilations(derniers):
    """Un ensemble contre la somme de ses parties, selon la hiérarchie de la table des fonctions : l'ensemble des
    fonctions contre les divisions de la COFOG, les missions du budget général de l'État ou ses comptes (budgets
    annexes, comptes spéciaux), ou les branches de la sécurité sociale, chaque division contre ses groupes, chaque
    mission ou compte contre ses programmes. Les parties d'un ensemble sont celles que la source publie, pour cette
    grandeur, au moins une année ; s'il en manque une année, la ventilation est partielle. Un ensemble consolidé ne se
    compare pas à des parties qui ne le sont pas (les recettes de l'ensemble des branches, hors transferts entre
    branches) : seul s'additionne alors le solde."""
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
            if len({par_fonction[f]["consolidation"] for f in [parent] + presents} & CONSOLIDATIONS_EXCLUSIVES) > 1:
                continue  # l'ensemble et ses parties ne mesurent pas la même chose
            resultats.append({"source": source, "perimetre": perimetre, "concept": concept, "fonction": parent,
                              "periode": periode, "complet": len(presents) == len(fils),
                              **comparer(par_fonction[parent], [(1, par_fonction[f]) for f in presents])})
    return resultats


def additivite(derniers):
    """Le solde d'un ensemble, ou sa part de la dépense consolidée de l'ensemble des administrations publiques,
    égale la somme de ceux de ses parties ; de même, un poste de la situation patrimoniale de la sécurité sociale
    égale la somme de ses lignes par entité, et un montant d'un niveau de collectivités locales la somme de ceux des
    niveaux qui le composent, en montant comme en nombre de budgets."""
    apu = {k[0] for k, l in derniers.items() if l["consolidation"] == "consolide_apu"}
    par_annee = collections.defaultdict(dict)
    for k, l in derniers.items():
        if valeur(l)[2] != "euros" and k[6] not in DENOMBREMENTS:
            continue
        if k[3] in ADDITIFS:
            # Les tableaux 3.201 à 3.214 de l'Insee publient un sous-secteur chacun : on les réunit.
            famille = "insee.t3201 à t3214" if re.fullmatch(r"insee\.t32(0[1-9]|1[0-4])", k[0]) else k[0]
        elif k[3] in DECOMPOSITIONS_PAR_CONCEPT:
            famille = k[0]
        elif k[0] in apu and (l["consolidation"] == "consolide_apu" or k[2] == "S13"):
            famille = k[0]
        else:
            continue
        par_annee[(famille, k[3], k[4], k[6], k[7])][k[2]] = valeur(l)[:2] + (k[0],)
    controles, ecarts = 0, []
    for (famille, concept, fonction, unite, periode), valeurs in sorted(par_annee.items()):
        for ensemble, parties in DECOMPOSITIONS_PAR_CONCEPT.get(concept, DECOMPOSITIONS):
            if any(p[1:] in valeurs for p in parties if p[0] == "!"):
                continue
            parties = [p for p in parties if p[0] not in "?!"] + [p[1:] for p in parties if p[0] == "?" and p[1:] in valeurs]
            if ensemble in valeurs and parties and all(p in valeurs for p in parties):
                controles += 1
                ecart = valeurs[ensemble][0] - sum(valeurs[p][0] for p in parties)
                if depasse(ecart, valeurs[ensemble][1] + sum(valeurs[p][1] for p in parties)):
                    tableaux = sorted({valeurs[p][2] for p in [ensemble] + parties})
                    ecarts.append((famille, concept, fonction, periode, ensemble, parties, tableaux, ecart,
                                   unite if unite in DENOMBREMENTS else "euros"))
    return controles, ecarts


def passerelles(derniers):
    """Chaque passerelle, pour chaque année où figurent tous ses termes : écart entre les deux côtés, marge des
    arrondis, et si l'un des chiffres est encore révisable."""
    index = collections.defaultdict(dict)  # (périmètre, concept, traitement, période) → {source: ligne}, en montant
    for k, l in derniers.items():
        if k[1] == "FR" and k[4] == "" and valeur(l)[2] == "euros" and retenu(l, index[(k[2], k[3], k[5], k[7])].get(k[0])):
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
    retenues = {}
    for k, l in derniers.items():
        v, precision, unite = valeur(l)
        if unite != "écus puis euros" and retenu(l, retenues.get(k[:6] + (unite, k[7]))):
            retenues[k[:6] + (unite, k[7])] = l
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


# Comptes de chaque collectivité (data.ofgl.fr) : le niveau des annexes de l'OFGL auquel se compare la somme des
# collectivités de chaque jeu de données, et les catégories de collectivités qu'il compte (toutes si rien) : les annexes
# comptent la métropole de Lyon (« ML ») avec les groupements à fiscalité propre et la Ville de Paris (« PARIS ») avec
# les communes, que le jeu des départements donne aussi ; les quatre montants de chaque ligne, avec l'annexe et le
# suffixe de périmètre du total auquel se compare leur somme.
NIVEAUX_COLLECTIVITES = {"ofgl.base-gfp-consolidee": ("GFP", None), "ofgl.base-communes-consolidee": ("COMMUNES", None),
                         "ofgl.base-departements-consolidee": ("DEPARTEMENTS", {"DEPT"}),
                         "ofgl.base-regions-consolidee": ("REGIONS_CTU", None),
                         "ofgl.base-syndicats-consolidee": ("SYNDICATS", None)}
# Les annexes ne donnent pas de total des établissements publics locaux, des SDIS ni des centres d'action sociale.
NIVEAUX_COLLECTIVITES.update({s: (None, None) for s in ("ofgl.base-epl-consolidee", "ofgl.base-sdis", "ofgl.base-ccas-cias")})
BUDGETS = [("budget principal", "ofgl.annexe-2a", "_BP"), ("budgets annexes", "ofgl.annexe-2b", "_BA"),
           ("flux croisés", None, None), ("consolidé", "ofgl.annexe-2c", "_BP_BA")]
BUDGET_SEUL = "budget par budget"  # le seul montant d'une ligne d'un jeu publié budget par budget
# Grandeurs des annexes que les comptes de chaque collectivité ne donnent qu'en parties : la trésorerie nette est la
# différence des dépôts au Trésor et des crédits de trésorerie.
EN_PARTIES = {"COMPTES_LOCAUX.TRESORERIE_NETTE": [(1, "COMPTES_LOCAUX.DEPOTS_TRESOR"),
                                                  (-1, "COMPTES_LOCAUX.CREDITS_TRESORERIE")]}
# Chaque département et chaque région contre sa fiche dans les publications de la DGCL, qui donnent leurs budgets
# principaux : la publication et le périmètre de chaque collectivité, d'après son code de département ou de région, sauf
# celles qui ont leur propre fiche et celles que le portail ne code pas ainsi (« 67A » pour le Bas-Rhin, le Haut-Rhin et
# la Collectivité européenne d'Alsace).
FICHES_DGCL = {"ofgl.base-departements-consolidee": ("dgcl.finances-departements", "DEP_{dep_code}_BP"),
               "ofgl.base-regions-consolidee": ("dgcl.finances-regions", "REG_{reg_code}_BP")}
PERIMETRES_DGCL = {"226700011": "DEP_67_BP", "226800019": "DEP_68_BP", "200094332": "CEA_BP",
                   "200046977": "METROPOLE_LYON_BP", "217500016": "VILLE_DE_PARIS_BP",
                   "200076958": "COLLECTIVITE_DE_CORSE_BP", "200055507": "CTU_MARTINIQUE_BP",
                   "200052678": "CTU_GUYANE_BP"}


def listes_collectivites():
    """{(source, exercice): {siren: fiche}} : la liste la plus récente des collectivités de chaque exercice."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    retenues = {}
    for i in lire("tables/fichiers_collectivites.csv"):
        cle = (i["source_id"], i["exercice"])
        if i["contenu"] == "collectivites" and (cle not in retenues or i["version"] > retenues[cle]["version"]):
            retenues[cle] = i
    return {cle: ofgl.collectivites(fichiers[i["fichier_id"]])[0] for cle, i in sorted(retenues.items())}


def identites_comptables(controles, identites, source, exercice, cle, montants, lus):
    """Les identités comptables d'une collectivité, ou d'un budget (`cle`), sur ses montants {concept: valeurs} : `lus`
    donne, pour chacun des montants d'une ligne, son libellé et la place de sa valeur et de sa marge d'arrondi. Une
    identité dont aucune partie n'a de ligne ne s'applique pas."""
    for total, composantes in identites:
        obligatoires = [c for c in composantes if c[0] not in "?!"]
        if total not in montants or any(c.lstrip("-") not in montants for c in obligatoires) or \
                any(c[1:] in montants for c in composantes if c[0] == "!"):
            continue
        parties = [(-1 if c.startswith("-") else 1, c.lstrip("-")) for c in
                   obligatoires + [c[1:] for c in composantes if c[0] == "?"] if c.lstrip("-") in montants]
        if not parties:
            continue
        for budget, k, m in lus:
            ecart = montants[total][k] - sum(s * montants[c][k] for s, c in parties)
            entree = controles[(source, total, tuple(c for _, c in parties), budget)]
            entree[0] += 1
            if depasse(ecart, montants[total][m] + sum(montants[c][m] for _, c in parties)):
                entree[1] += 1
                if entree[2] is None or abs(ecart) > abs(entree[2][0]):
                    entree[2] = (ecart, cle, exercice)


def collectivites(derniers, listes):
    """Pour chaque jeu des comptes de chaque collectivité et chaque exercice, dans sa version la plus récente : les lignes
    dont le montant consolidé n'est pas le budget principal plus les budgets annexes moins les flux croisés ; les
    identités comptables de chaque collectivité, pour chacun des quatre montants ; les comptes d'une collectivité que
    deux jeux donnent ; la somme des collectivités contre les totaux des annexes 2A (budgets principaux), 2B (budgets
    annexes) et 2C (consolidés) des rapports de l'OFGL ; le budget principal de chaque département et de chaque région
    contre sa fiche de la DGCL. Pour un jeu publié budget par budget : les identités comptables de chaque budget."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    agregats = {a["agregat"]: a for a in lire("tables/agregats_ofgl.csv")}
    retenus = {}
    for i in lire("tables/fichiers_collectivites.csv"):
        cle = (i["source_id"], i["exercice"])
        if i["contenu"] == "montants" and (cle not in retenus or i["version"] > retenus[cle]["version"]):
            retenus[cle] = i
    presences = collections.defaultdict(list)  # (exercice, siren) → jeux dont la liste porte la collectivité
    for (source, exercice), fiches in listes.items():
        for siren in sorted({f["siren"] for f in fiches.values()}) if source in ofgl.PAR_BUDGET else fiches:
            presences[(exercice, siren)].append(source)
    doubles = {cle: jeux for cle, jeux in presences.items() if len(jeux) > 1}
    identites = [(t, c) for t, c in IDENTITES if t.startswith("COMPTES_LOCAUX.")]
    exercices, sommes_controlees, fiches_controlees, comptes_doubles = [], [], [], {}
    controles = collections.defaultdict(lambda: [0, 0, None])  # (source, total, budget) → [vérifiées, en écart, pire]
    for (source, exercice), inscrit in sorted(retenus.items()):
        niveau, categories = NIVEAUX_COLLECTIVITES[source]
        fiches = listes.get((source, exercice))  # sans liste, ni catégories ni codes : pas de somme triée ni de fiche
        if source in ofgl.PAR_BUDGET:
            # Un jeu publié budget par budget : un montant par ligne, ni consolidation, ni total publié.
            par_budget, sirens = collections.defaultdict(dict), set()
            for siren, budget, agregat, montant_, marge_ in ofgl.montants_budgets(fichiers[inscrit["fichier_id"]],
                                                                                  agregats, marges=True):
                par_budget[budget][agregats[agregat]["concept_id"]] = (montant_, marge_)
                sirens.add(siren)
            exercices.append((source, exercice, inscrit["version"], inscrit["statut"], len(sirens),
                              int(inscrit["lignes"]), None))
            for budget, montants in par_budget.items():
                identites_comptables(controles, identites, source, exercice, budget, montants, [(BUDGET_SEUL, 0, 1)])
            continue
        par_siren, lignes_en_ecart = collections.defaultdict(dict), 0
        sommes = collections.defaultdict(lambda: [0.0] * 8)  # quatre montants, puis leurs marges d'arrondi
        for siren, agregat, *montants in ofgl.montants(fichiers[inscrit["fichier_id"]], agregats, marges=True):
            concept = agregats[agregat]["concept_id"]
            par_siren[siren][concept] = montants
            lignes_en_ecart += depasse(montants[0] + montants[1] - montants[2] - montants[3], sum(montants[4:]))
            if categories is None or fiches is not None and fiches.get(siren, {}).get("categ") in categories:
                for k in range(8):
                    sommes[concept][k] += montants[k]
        exercices.append((source, exercice, inscrit["version"], inscrit["statut"], len(par_siren), int(inscrit["lignes"]),
                          lignes_en_ecart))
        comptes_doubles.update({(source, exercice, s): par_siren[s] for s in par_siren if (exercice, s) in doubles})
        if source in FICHES_DGCL and fiches is not None:
            # Un agrégat que le jeu publie pour d'autres collectivités de l'exercice, mais pas pour celle-ci, y vaut zéro.
            publication, modele = FICHES_DGCL[source]
            publies = sorted(set().union(*par_siren.values()))
            for siren, montants in par_siren.items():
                if siren not in fiches:
                    continue
                perimetre = PERIMETRES_DGCL.get(siren) or modele.format(**fiches[siren])
                for concept in publies:
                    m = montants.get(concept, [0.0] * 8)
                    publie = derniers.get((publication, "FR", perimetre, concept, "", "", "MIO_EUR", exercice))
                    if publie is not None:
                        v, marge, _ = valeur(publie)
                        fiches_controlees.append((source, concept, exercice, siren, m[0] - v,
                                                  not depasse(m[0] - v, marge + m[4]),
                                                  inscrit["statut"] == "provisoire" or publie["statut"] in REVISABLES))
        for siren, montants in par_siren.items():
            identites_comptables(controles, identites, source, exercice, siren, montants,
                                 [(budget, k, 4 + k) for k, (budget, _, _) in enumerate(BUDGETS)])
        if niveau is None:
            continue
        for concept, parties in EN_PARTIES.items():
            if concept not in sommes and all(c in sommes for _, c in parties):
                sommes[concept] = ([sum(s * sommes[c][k] for s, c in parties) for k in range(4)]
                                   + [sum(sommes[c][k] for _, c in parties) for k in range(4, 8)])
        for concept, somme in sorted(sommes.items()):
            for k, (budget, annexe, suffixe) in enumerate(BUDGETS):
                publie = derniers.get((annexe, "FR", f"{niveau}{suffixe}", concept, "", "", "MD_EUR", exercice))
                if publie is None:
                    continue
                v, marge, _ = valeur(publie)
                ecart = somme[k] - v
                sommes_controlees.append((source, budget, concept, exercice, ecart,
                                          not depasse(ecart, marge + somme[4 + k]),
                                          inscrit["statut"] == "provisoire" or publie["statut"] in REVISABLES))
    # Une collectivité que deux jeux donnent, comme la métropole de Lyon et la Ville de Paris : pour chaque agrégat
    # qu'ils ont en commun, les quatre montants de l'un contre ceux de l'autre.
    # (exercice, siren, deux jeux, montants comparés, écarts [(concept, montant, écart)], agrégats du seul premier jeu,
    # agrégats du seul second)
    memes = []
    for (exercice, siren), jeux in sorted(doubles.items()):
        for ja, jb in itertools.combinations(sorted(jeux), 2):
            a, b = comptes_doubles.get((ja, exercice, siren)), comptes_doubles.get((jb, exercice, siren))
            if a is None or b is None:  # un jeu publié budget par budget : présente, sans montants comparables
                memes.append((exercice, siren, (ja, jb), 0, [], set(), set()))
                continue
            communs = sorted(set(a) & set(b))
            ecarts = [(c, BUDGETS[k][0], a[c][k] - b[c][k]) for c in communs for k in range(4)
                      if depasse(a[c][k] - b[c][k], a[c][4 + k] + b[c][4 + k])]
            memes.append((exercice, siren, (ja, jb), 4 * len(communs), ecarts, set(a) - set(b), set(b) - set(a)))
    return exercices, controles, sommes_controlees, memes, fiches_controlees


# --- Le rapport ----------------------------------------------------------------------------------------

def fr(x, decimales, signe=False):
    texte = format(x, f"{'+' if signe else ''},.{decimales}f")
    return texte.replace(",", " ").replace(".", ",").replace("-", "−")


def ecart_lisible(ecart, unite):
    if unite in DENOMBREMENTS:
        return fr(ecart, 0, True)
    if unite == "euros":
        # Un écart de moins de 50 000 euros s'écrirait « 0,0 M€ » : il s'écrit en euros, en centimes sous l'euro.
        if abs(ecart) < 1:
            return f"{fr(ecart, 2, True)} €"
        return f"{fr(ecart / 1e6, 1, True)} M€" if abs(ecart) >= 5e4 else f"{fr(ecart, 0, True)} €"
    nom = {"PC_PIB": "de PIB", "PC_PIB_POTENTIEL": "de PIB potentiel", "PC_DEPENSE": "de dépense"}.get(unite, unite)
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
              "Un total contre la somme de ses composantes, pour chaque source, périmètre, fonction et année : en "
              "montant, ou en % du PIB quand la source y donne aussi ses composantes. Les tableaux des lois "
              "d'approbation des comptes changent de lignes d'une année à l'autre, et une case vide y vaut « rien » : "
              "une composante qu'ils ne présentent pas une année y compte pour zéro.", "",
              f"{len(complets)} sommes vérifiées avec toutes leurs composantes : {len(complets) - len(ecarts)} justes, "
              f"{len(ecarts)} en écart.", ""]

    def montant_lisible(x, unite):
        noms = {**NOMS_RATIOS, "PC_PIB_POTENTIEL": "% du PIB potentiel"}
        return f"{fr(x / 1e9, 4)} Md€" if unite == "euros" else f"{fr(x, 1)} {noms.get(unite, unite)}"

    if ecarts:
        lignes += ["| Source | Périmètre | Fonction | Année | Total | Total publié | Somme des composantes | Écart |",
                   "|---|---|---|---|---|---|---|---|"]
        lignes += [f"| {r['source']} | {r['perimetre']} | {r['fonction'] or 'ensemble'} | {r['periode']} | {r['total']} | "
                   f"{montant_lisible(r['valeur'], r['unite'])} | {montant_lisible(r['somme'], r['unite'])} | "
                   f"{ecart_lisible(r['valeur'] - r['somme'], r['unite'])} |" for r in ecarts]
        lignes.append("")
    return lignes + partielles(resultats, "sommes")


def partie_ventilations(derniers):
    resultats = ventilations(derniers)
    complets = [r for r in resultats if r["complet"]]
    ecarts = [r for r in complets if not r["juste"]]
    lignes = ["## 2. Ventilations par fonction", "",
              "Pour une même grandeur, l'ensemble des fonctions contre la somme des divisions de la COFOG, des missions "
              "du budget général de l'État ou de ses comptes (budgets annexes, comptes spéciaux), ou des branches de la "
              "sécurité sociale, chaque division contre la somme de ses groupes, chaque mission ou compte contre celle de "
              "ses programmes. Pour les branches, seul le solde s'additionne : les recettes et les dépenses de l'ensemble "
              "des branches excluent les transferts entre elles, que comptent celles de chaque branche.", "",
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
              "des administrations publiques (tableau 3.307 de l'Insee), contre la somme de ceux de ses parties ; pour "
              "la sécurité sociale, le résultat du régime général et celui des régimes de base, Fonds de solidarité "
              "vieillesse compris, contre la somme des leurs et de celui du FSV, et chaque poste de la situation "
              "patrimoniale (annexe A des lois de financement) contre la somme de ses lignes par entité ; pour les "
              "collectivités locales, dont la source ne consolide pas les montants entre niveaux, chaque montant d'un "
              "niveau contre la somme de ceux des niveaux qui le composent, et celui des groupements à fiscalité propre "
              "contre la somme de leurs types (annexes 2A et 2B des rapports de l'OFGL, budgets principaux et budgets "
              "annexes), le nombre de budgets de l'ensemble des collectivités contre la somme de ceux de ses niveaux, "
              "chaque total des publications de la DGCL contre la somme de ses départements ou de ses régions.", "",
              f"{n} additions vérifiées : {n - len(ecarts)} justes, {len(ecarts)} en écart.", ""]
    regroupes = collections.defaultdict(list)
    for famille, concept, fonction, annee, ensemble, parties, tableaux, ecart, unite in ecarts:
        regroupes[(famille, concept, ensemble, tuple(parties), unite)].append((annee, ecart, tableaux, fonction))
    if regroupes:
        lignes += ["| Tableaux | Grandeur | Ensemble | Parties | Fonctions | Années en écart | Plus grand écart |",
                   "|---|---|---|---|---|---|---|"]
        for (famille, concept, ensemble, parties, unite), liste in sorted(regroupes.items()):
            annee, ecart, _, fonction = plus_grand(liste, lambda e: e[1])
            tableaux = ", ".join(sorted({t for _, _, ts, _ in liste for t in ts}))
            fonctions = sorted({f or "ensemble" for _, _, _, f in liste})
            lignes.append(f"| {tableaux} | {concept} | {ensemble} | {parties_lisibles(parties)} | "
                          f"{', '.join(fonctions) if len(fonctions) <= 3 else f'{len(fonctions)} fonctions'} | "
                          f"{plage([a for a, _, _, _ in liste])} | {ecart_lisible(ecart, unite)} en {annee}"
                          f"{'' if fonction == '' else f' ({fonction})'} |")
        lignes.append("")
    return lignes


def parties_lisibles(parties):
    """Les parties d'une addition ; au-delà de six, leur nombre, la première et la dernière."""
    return " + ".join(parties) if len(parties) <= 6 else f"ses {len(parties)} parties ({parties[0]} … {parties[-1]})"


def partie_passerelles(derniers):
    resultats = passerelles(derniers)
    lignes = ["## 4. Passerelles entre tableaux", "",
              "Des tableaux différents présentent autrement les mêmes grandeurs. Chaque passerelle vérifie qu'ils "
              "concordent, à l'arrondi près, pour chaque année où figurent tous ses termes. Pour les collectivités "
              "locales, la consolidation des budgets principaux et annexes retire chaque flux croisé des recettes comme "
              "des dépenses de la même section : la variation du fonds de roulement, l'épargne brute, la dette et la "
              "trésorerie d'un ensemble consolidé égalent la somme de celles de ses parties.", "",
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


def nom(listes, source, exercice, siren):
    """Le libellé d'une collectivité dans la liste la plus récente de l'exercice."""
    return listes.get((source, exercice), {}).get(siren, {}).get("lbudg", "")


def partie_collectivites(derniers):
    listes = listes_collectivites()
    exercices, controles, sommes, memes, fiches = collectivites(derniers, listes)
    if not exercices:
        return []
    lignes = ["## 7. Comptes de chaque collectivité", "",
              "Les comptes que l'OFGL publie collectivité par collectivité sur data.ofgl.fr, dans la version la plus "
              "récente de chaque exercice. Chaque ligne donne, pour une collectivité et un agrégat, le montant de son "
              "budget principal, celui de ses budgets annexes, les flux croisés entre eux et le montant consolidé : "
              "celui-ci doit être la somme des deux premiers moins le troisième, à l'arrondi près : la demi-unité de "
              "la dernière décimale publiée de chaque montant, au centime au plus fin (les montants de 2022 n'ont que "
              "dix chiffres significatifs). Pour chaque "
              "collectivité, les identités comptables de la section 1 s'appliquent à chacun des quatre montants. La "
              "somme des collectivités se compare aux totaux des annexes des rapports de l'OFGL : 2A pour les budgets "
              "principaux, 2B pour les budgets annexes, 2C pour les comptes consolidés ; celle des départements sans la "
              "métropole de Lyon ni la Ville de Paris, que les annexes comptent avec les groupements à fiscalité propre "
              "et avec les communes. Le budget principal de chaque département et de chaque région se compare aussi à sa "
              "fiche dans les publications de la DGCL. Les SDIS et les centres d'action sociale ne sont publiés que "
              "budget par budget, sans consolidation : chaque ligne donne le montant d'un budget, auquel s'appliquent "
              "les identités comptables. Les annexes ne donnent de total ni pour eux, ni pour les établissements publics "
              "locaux.", "",
              "| Jeu de données | Exercices | Collectivités au dernier exercice | Lignes | "
              "Lignes dont le consolidé n'est pas BP + BA − flux |", "|---|---|---|---|---|"]
    par_source = collections.defaultdict(list)
    for e in exercices:
        par_source[e[0]].append(e)
    for source, liste in sorted(par_source.items()):
        dernier = max(liste, key=lambda e: e[1])
        consolides = "sans objet" if source in ofgl.PAR_BUDGET else fr(sum(e[6] for e in liste), 0)
        lignes.append(f"| {source} | {plage([e[1] for e in liste])} | {fr(dernier[4], 0)} | "
                      f"{fr(sum(e[5] for e in liste), 0)} | {consolides} |")
    n, faux = sum(v[0] for v in controles.values()), sum(v[1] for v in controles.values())
    lignes += ["", f"Identités comptables de chaque collectivité, ou de chaque budget pour les jeux publiés budget par "
               f"budget : {fr(n, 0)} vérifiées, {fr(n - faux, 0)} justes, {fr(faux, 0)} en écart.", ""]
    en_ecart = [(k, v) for k, v in sorted(controles.items()) if v[1]]
    if en_ecart:
        lignes += ["| Jeu de données | Total | Parties | Montant | En écart | Plus grand écart |",
                   "|---|---|---|---|---|---|"]
        for (source, total, parties, budget), (verifiees, nombre, (ecart, siren, exercice)) in en_ecart:
            lignes.append(f"| {source} | {total} | {parties_lisibles(list(parties))} | {budget} | "
                          f"{fr(nombre, 0)} sur {fr(verifiees, 0)} | {ecart_lisible(ecart, 'euros')} : "
                          f"{nom(listes, source, exercice, siren)} ({siren}), {exercice} |")
        lignes.append("")
    lignes += partie_memes_collectivites(listes, memes)
    justes = sum(1 for s in sommes if s[5])
    lignes += [f"Somme des collectivités contre les totaux des annexes : {fr(len(sommes), 0)} comparaisons, "
               f"{fr(justes, 0)} justes, {fr(len(sommes) - justes, 0)} en écart. Le dernier exercice d'un jeu est "
               "provisoire, et les annexes d'un rapport ne sont pas toujours établies sur la même version des comptes "
               "que le portail : un écart qui touche un chiffre révisable peut venir de là.", ""]
    par_budget = collections.defaultdict(list)
    for s in sommes:
        par_budget[(s[0], s[1])].append(s)
    lignes += ["| Jeu de données | Montant | Comparaisons | En écart | dont hors chiffres révisables | "
               "Plus grand écart hors chiffres révisables (somme − annexe) | Plus grand écart (somme − annexe) |",
               "|---|---|---|---|---|---|---|"]

    def texte(liste):
        if not liste:
            return "aucun"
        source, budget, concept, exercice, ecart, _, _ = plus_grand(liste, lambda e: e[4])
        return f"{ecart_lisible(ecart, 'euros')} en {exercice} ({concept})"

    for (source, budget), liste in sorted(par_budget.items(), key=lambda e: (e[0][0], [b[0] for b in BUDGETS].index(e[0][1]))):
        fausses = [s for s in liste if not s[5]]
        fermes = [s for s in fausses if not s[6]]
        lignes.append(f"| {source} | {budget} | {fr(len(liste), 0)} | {fr(len(fausses), 0)} | {fr(len(fermes), 0)} | "
                      f"{texte(fermes)} | {texte(fausses)} |")
    lignes.append("")
    fermes = [s for s in sommes if not s[5] and not s[6]]
    if fermes:
        lignes += ["Écarts hors chiffres révisables :", "",
                   "| Jeu de données | Montant | Grandeur | Années en écart | Plus grand écart (somme − annexe) |",
                   "|---|---|---|---|---|"]
        regroupes = collections.defaultdict(list)
        for s in fermes:
            regroupes[(s[0], s[1], s[2])].append(s)
        for (source, budget, concept), liste in sorted(regroupes.items()):
            e = plus_grand(liste, lambda x: x[4])
            lignes.append(f"| {source} | {budget} | {concept} | {plage([x[3] for x in liste])} | "
                          f"{ecart_lisible(e[4], 'euros')} en {e[3]} |")
        lignes.append("")
    return lignes + partie_fiches_dgcl(listes, fiches)


def concepts_lisibles(concepts):
    """Une liste de concepts, sans le préfixe de leur norme quand c'est celle des comptes locaux."""
    noms = [c.removeprefix("COMPTES_LOCAUX.") for c in concepts]
    return ", ".join(noms) if noms else "aucun"


def partie_memes_collectivites(listes, memes):
    """Les collectivités que deux jeux donnent : leurs comptes dans l'un contre leurs comptes dans l'autre."""
    if not memes:
        return []
    comparees, en_ecart = sum(m[3] for m in memes), sum(len(m[4]) for m in memes)
    lignes = [f"Collectivités que deux jeux de données donnent : {fr(comparees, 0)} montants comparés de l'un à l'autre, "
              f"{fr(comparees - en_ecart, 0)} égaux, {fr(en_ecart, 0)} en écart. Les agrégats qu'un seul des deux jeux "
              "publie, désignés par leur concept de la norme COMPTES_LOCAUX, ne se comparent pas.", "",
              "| Premier jeu | Second jeu | Collectivités | Exercices | Montants comparés | En écart | "
              "Agrégats du seul premier jeu | Agrégats du seul second |", "|---|---|---|---|---|---|---|---|"]
    regroupes = collections.defaultdict(list)
    for m in memes:
        regroupes[m[2]].append(m)
    for (ja, jb), liste in sorted(regroupes.items()):
        derniers = {}  # siren → dernier exercice où les deux jeux le donnent
        for m in liste:
            derniers[m[1]] = max(derniers.get(m[1], ""), m[0])
        qui = (", ".join(f"{nom(listes, ja, e, s)} ({s})" for s, e in sorted(derniers.items())) if len(derniers) <= 3
               else f"{fr(len(derniers), 0)} collectivités")
        seuls = [sorted(set().union(*(m[k] for m in liste))) for k in (5, 6)]
        lignes.append(f"| {ja} | {jb} | {qui} | {plage([m[0] for m in liste])} | {fr(sum(m[3] for m in liste), 0)} | "
                      f"{fr(sum(len(m[4]) for m in liste), 0)} | {concepts_lisibles(seuls[0])} | "
                      f"{concepts_lisibles(seuls[1])} |")
    lignes.append("")
    ecarts = [(m[1], m[2], m[0], *e) for m in memes for e in m[4]]
    if ecarts:
        lignes += ["| Collectivité | Exercice | Grandeur | Montant | Écart (premier jeu − second) |", "|---|---|---|---|---|"]
        for siren, (ja, _), exercice, concept, budget, ecart in sorted(ecarts):
            lignes.append(f"| {nom(listes, ja, exercice, siren)} ({siren}) | {exercice} | {concept} | {budget} | "
                          f"{ecart_lisible(ecart, 'euros')} |")
        lignes.append("")
    return lignes


def partie_fiches_dgcl(listes, fiches):
    """Le budget principal de chaque département et de chaque région contre sa fiche de la DGCL."""
    if not fiches:
        return []
    justes = sum(1 for f in fiches if f[5])
    lignes = [f"Budget principal de chaque département et de chaque région contre sa fiche dans les publications de la "
              f"DGCL (« Les finances des départements », « Les finances des régions ») : {fr(len(fiches), 0)} "
              f"comparaisons, {fr(justes, 0)} justes, {fr(len(fiches) - justes, 0)} en écart.", ""]
    regroupes = collections.defaultdict(list)
    for f in fiches:
        regroupes[(f[0], f[1])].append(f)
    en_ecart = {cle: [f for f in liste if not f[5]] for cle, liste in sorted(regroupes.items())}
    if any(en_ecart.values()):
        lignes += ["| Jeu de données | Grandeur | Comparaisons | En écart | Années en écart | "
                   "Plus grand écart (OFGL − DGCL) |", "|---|---|---|---|---|---|"]
        for (source, concept), fausses in en_ecart.items():
            if fausses:
                _, _, exercice, siren, ecart, _, _ = plus_grand(fausses, lambda f: f[4])
                lignes.append(f"| {source} | {concept} | {fr(len(regroupes[(source, concept)]), 0)} | "
                              f"{fr(len(fausses), 0)} | {plage([f[2] for f in fausses])} | "
                              f"{ecart_lisible(ecart, 'euros')} : {nom(listes, source, exercice, siren)} ({siren}), "
                              f"{exercice} |")
        lignes.append("")
    return lignes


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
              "demi-unité de la dernière décimale de chaque valeur en jeu, ou l'unité entière pour l'OFGL, qui arrondit "
              "ou tronque selon les cas ses montants à l'euro ; un nombre de budgets n'est pas arrondi et doit être "
              "exact. Une incohérence signalée ici est un constat "
              "sur la source, pas une erreur d'enregistrement : chaque chiffre a été relu dans sa copie archivée.", ""]
    lignes += partie_sources(derniers) + partie_sommes(derniers) + partie_ventilations(derniers)
    lignes += partie_additivite(derniers) + partie_passerelles(derniers) + partie_ratios(derniers)
    lignes += partie_concordances(derniers) + partie_collectivites(derniers)
    RAPPORT.parent.mkdir(exist_ok=True)
    RAPPORT.write_text("\n".join(lignes).rstrip("\n") + "\n", encoding="utf-8")
    print(f"écrit : {RAPPORT.relative_to(RACINE)}")


if __name__ == "__main__":
    ecrire_rapport(charger())
