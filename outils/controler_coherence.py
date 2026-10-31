#!/usr/bin/env python3
"""Contrôle la cohérence des chiffres enregistrés et écrit controles/coherence.md.

    python3 outils/controler_coherence.py

Le contrôle de la base (valider.py) garantit que chaque chiffre est celui de sa source. Celui-ci
vérifie ce que disent les sources elles-mêmes :
1. les sommes comptables (un total égale la somme de ses composantes) ;
2. les ventilations par fonction (l'ensemble égale la somme des fonctions, chaque fonction celle de ses
   groupes ; pour le budget de l'État, chaque mission celle de ses programmes) ;
3. l'additivité des sous-secteurs, pour les soldes, les prélèvements obligatoires, la dette et les dépenses
   consolidées de l'ensemble, et pour tous les montants des comptes complets, et celle des niveaux de collectivités
   locales, pour tous leurs montants et leurs nombres de budgets, et celle des catégories d'organismes et de
   collectivités dans leurs décomptes ;
4. les passerelles entre tableaux qui présentent autrement les mêmes grandeurs, dont les grandeurs que la
   consolidation des comptes des collectivités locales laisse inchangées, la dette trimestrielle contre la dette de fin
   d'année, et les comptes complets contre les dépenses et recettes ;
5. les ratios, qu'on doit retrouver à partir de leur dénominateur ;
6. les écarts entre sources pour une même grandeur ;
7. les comptes de chaque collectivité : montant consolidé, identités comptables de chacune, comptes d'une même
   collectivité dans deux jeux de données, somme des collectivités contre les totaux publiés, et chaque
   département et chaque région contre sa fiche de la DGCL ;
8. les flux entre administrations : ce que l'une déclare verser à une autre contre ce que celle-ci déclare
   recevoir, pour la dotation globale de fonctionnement que l'État notifie à chaque collectivité et pour les
   contributions des départements aux SDIS ;
9. les dépenses de chaque département par fonction : chaque fonction contre la somme de ses sous-fonctions,
   les identités comptables dans chaque fonction, et les fonctions réunies contre les comptes consolidés ;
10. la fiscalité directe locale de chaque commune : le produit de chaque taxe contre sa base multipliée par son
   taux, le taux net contre le taux voté, et la taxe d'enlèvement des ordures ménagères recensée contre celle des
   comptes ;
11. le recensement des éléments d'imposition de la DGFiP : le produit de chaque imposition contre sa base
   multipliée par son taux, la base simplifiée de l'OFGL contre le recensement dont elle est tirée, commune par
   commune, le produit de chaque taxe et de chaque niveau qui perçoit, et la taxe d'enlèvement des ordures
   ménagères recensée de chaque niveau contre celle de ses comptes ;
12. les organismes publics : les listes et décomptes officiels des unités publiques, de l'Insee et de la DGCL, contre
   les unités dont la base a les comptes une à une ;
13. les comptes individuels de la DGFiP : les identités que leurs maquettes énoncent, collectivité par collectivité, et
   chaque collectivité contre ses comptes de l'OFGL, pour les agrégats de même objet ;
14. les balances des comptes de l'État : l'équilibre de chacune, celui des engagements hors bilan, et le bilan et le
   compte de résultat qu'on en tire contre ceux des lois d'approbation des comptes, ligne par ligne ;
15. la dette négociable de l'État : son encours de chaque mois contre les variations publiées avec lui, le tableau de
   financement des lois d'approbation des comptes, et les titres négociables de la balance et du bilan de l'État ;
16. les comptes de la protection sociale de la DREES : les prestations de chaque groupe de secteurs dans son classeur
   contre celles de ses secteurs dans l'export, et l'écart de l'ensemble des régimes contre le double compte d'un
   secteur ;
17. le budget voté contre le budget exécuté : les crédits qu'ouvre chaque loi de finances initiale, au total et mission
   par mission, contre les dépenses et les engagements que constate la loi d'approbation des comptes de l'année ;
18. les recettes votées et le solde voté : les recettes qu'évalue chaque loi de finances initiale et les soldes que
   fixe son article d'équilibre, contre ceux que constate la loi d'approbation des comptes de l'année, au total et
   compte par compte ;
19. le financement voté : le besoin de financement et les émissions de dette que prévoit chaque loi de finances
   initiale, et le plafond qu'elle fixe à la variation de la dette négociable à plus d'un an, contre le tableau de
   financement que constate la loi d'approbation des comptes de l'année ;
20. les plafonds d'emplois votés : celui des emplois de l'État que fixe l'article d'équilibre de chaque loi de finances
   initiale, contre sa répartition par ministère et par budget annexe, et ceux des opérateurs, des établissements à
   autonomie financière et des autorités publiques indépendantes.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la
demi-unité de la dernière décimale de chaque valeur en jeu, ou l'unité entière pour une source qui tronque
ses montants ; un nombre (de budgets) n'est pas arrondi. Une incohérence trouvée ici n'est pas une
erreur de la base : c'est un constat sur la source, publié tel quel. Le rapport ne contient aucune date
d'exécution, pour qu'un rapport à jour ne change pas.
"""

import collections
import decimal
import itertools
import math
import re

import importer_balances_etat as balances
import importer_comptes_individuels as individuels
import importer_drees_cps as cps
import importer_ofgl_collectivites as ofgl
import importer_organismes as organismes
import importer_rei as rei
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
# Dette négociable de l'État (Agence France Trésor) : l'encours est la somme de ses parts en euros et en devises, et celle
# de ses parts à taux fixe et indexée sur l'inflation ; chaque part en euros ou en devises, la somme de ses parts à court
# terme et à moyen et long terme.
_DETTE_NEGOCIABLE = [("ENCOURS", ["ENCOURS_EUROS", "ENCOURS_DEVISES"]), ("ENCOURS", ["TAUX_FIXE", "INDEXEE_INFLATION"]),
                     ("ENCOURS_EUROS", ["COURT_TERME_EUROS", "MOYEN_LONG_TERME_EUROS"]),
                     ("ENCOURS_DEVISES", ["COURT_TERME_DEVISES", "MOYEN_LONG_TERME_DEVISES"])]
IDENTITES += [(f"DETTE_NEGOCIABLE.{t}", [f"DETTE_NEGOCIABLE.{c}" for c in cs]) for t, cs in _DETTE_NEGOCIABLE]
# Comptes de la protection sociale (DREES) : les emplois hors transferts entre régimes sont la somme de leurs lignes, sans
# l'ajustement comptable, que le classeur présente parmi eux sans le compter dans leur total ; les ressources, la somme
# des leurs ; les prestations, celle des prestations en espèces et en nature. Les lignes changent selon les années et
# les groupes de régimes (« ? » : peut manquer).
_CPS_EMPLOIS = ["PRESTATIONS_ESPECES", "PRESTATIONS_NATURE", "FRAIS_NON_FINANCIERS", "FRAIS_FINANCIERS",
                "FRAIS_FINANCIERS_AUTRES_EMPLOIS", "AUTRES_EMPLOIS", "EMPLOIS_CAPITAL"]
_CPS_RESSOURCES = ["COTISATIONS_EMPLOYEURS", "COTISATIONS_SALARIES", "AUTRES_COTISATIONS", "COTISATIONS_IMPUTEES",
                   "IMPOTS_TAXES_AFFECTES", "CONTRIBUTIONS_PUBLIQUES", "PRODUITS_FINANCIERS",
                   "PRODUITS_FINANCIERS_AUTRES_RECETTES", "AUTRES_RECETTES", "RECETTES_CAPITAL"]
IDENTITES += [("CPS.EMPLOIS", ["?CPS." + c for c in _CPS_EMPLOIS]),
              ("CPS.RESSOURCES", ["?CPS." + c for c in _CPS_RESSOURCES]),
              ("CPS.PRESTATIONS", ["?CPS.PRESTATIONS_ESPECES", "?CPS.PRESTATIONS_NATURE"])]
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


def _prefixee(prefixe, composante):
    """Le concept d'une composante, sa marque (« ? », « ! ») et son signe gardés."""
    marque = composante[0] if composante[0] in "?!" else ""
    terme = composante[len(marque):]
    return marque + ("-" if terme.startswith("-") else "") + prefixe + terme.lstrip("-")


def _local(composante):
    return _prefixee("COMPTES_LOCAUX.", composante)


IDENTITES += [(f"COMPTES_LOCAUX.{t}", [_local(c) for c in cs]) for t, cs in _LOCAUX]

IDENTITES += [_rubrique("INSEE_PASSAGES.ETAT_OPERATIONS_FINANCIERES", "rubrique (1) du tableau 3.107"),
              _rubrique("INSEE_PASSAGES.ETAT_DROITS_CONSTATES", "rubrique (2) du tableau 3.107"),
              _rubrique("INSEE_PASSAGES.ETAT_NON_BUDGETAIRES", "rubrique (3) du tableau 3.107"),
              _rubrique("INSEE_PASSAGES.SECU_CORRECTIONS", "rubrique (1) du tableau 3.108")]

# Dette au sens de Maastricht : la somme de ses instruments, que le tableau 3.102 donne sans le total des crédits et sans
# les dépôts des administrations de sécurité sociale (« ? » : peuvent manquer) ; le passage du total des passifs à la
# dette (tableau 3.104) et du déficit à la variation de la dette (3.105), chaque rubrique contre la somme de ses lignes.
IDENTITES += [("PDE.GD", ["?PDE.GD_F2", "PDE.GD_F3", "PDE.GD_F4"]), ("PDE.GD", ["?PDE.GD_F2", "PDE.GD_F3", "PDE.GD_F41",
                                                                              "PDE.GD_F42"]),
              ("PDE.GD_F3", ["PDE.GD_F31", "PDE.GD_F32"]), ("PDE.GD_F4", ["PDE.GD_F41", "PDE.GD_F42"])]
_DETTE = [("GD", ["TOTAL_PASSIFS", "-DIFFERENCE_CHAMP", "-PASSAGE_DETTE_CONSOLIDEE", "-PASSAGE_VALEUR_NOMINALE"]),
          ("DIFFERENCE_CHAMP", ["COMPTES_A_PAYER_DERIVES", "DEPOTS_GARANTIE"]),
          ("PASSAGE_DETTE_CONSOLIDEE", ["CONSOLIDATION_DEPOTS", "CONSOLIDATION_TITRES", "CONSOLIDATION_CREDITS"]),
          ("PASSAGE_VALEUR_NOMINALE", ["ICNE_DEPOTS", "ECART_VALORISATION_OBLIGATIONS", "ICNE_CREDITS"]),
          ("VARIATION_DETTE", ["DEFICIT", "ACQUISITIONS_NETTES_ACTIFS", "VARIATION_PASSIF_HORS_DETTE",
                               "CHANGEMENTS_VOLUME", "SOLDE_AUTRES_COMPTES", "ECART_STATISTIQUE"]),
          ("ACQUISITIONS_NETTES_ACTIFS", ["ACQUISITIONS_F2", "ACQUISITIONS_F3", "ACQUISITIONS_F4", "ACQUISITIONS_F5",
                                          "ACQUISITIONS_F71", "ACQUISITIONS_F6"]),
          ("VARIATION_PASSIF_HORS_DETTE", ["VARIATION_ICNE", "VARIATION_AUTRES_PASSIFS"]),
          ("CHANGEMENTS_VOLUME", ["RECLASSEMENTS", "VALORISATION_DEVISES", "RACHATS_TITRES"])]
IDENTITES += [(("PDE." if t == "GD" else "INSEE_DETTE.") + t, [_prefixee("INSEE_DETTE.", c) for c in cs])
              for t, cs in _DETTE]

# Comptes complets des administrations publiques (tableaux 7.301 à 7.306) : le solde de chaque compte est la différence
# de ses ressources et de ses emplois, chaque opération la somme de ses détails. Les subventions et les transferts en
# capital versés y sont inscrits en ressources avec un signe négatif, les subventions reçues en emplois avec un signe
# négatif : ils s'ajoutent. Pour les administrations, la dépense de consommation individuelle est égale aux transferts
# sociaux en nature, et la consommation finale effective à la dépense de consommation collective. De 1949 à 1977,
# l'Insee ne ventile pas les transferts courants entre administrations publiques (« ? » : peuvent manquer) ; les
# sous-secteurs en donnent alors le solde, et les autres transferts courants comptés avec lui (D.7S), qui prennent la
# place des autres transferts courants dans le revenu disponible (« ! » : l'identité qui ne les compte pas ne
# s'applique pas les années où ils sont publiés, ni l'autre celles où les transferts entre administrations le sont).
_COMPTES = [("P1", ["P11", "P12", "P13"]), ("B1G", ["P1", "-P2"]), ("B1N", ["B1G", "-P51C"]),
            ("D1PAY", ["D11PAY", "D12PAY"]), ("D12PAY", ["D121PAY", "D122PAY"]), ("D29PAY", ["D291PAY", "D292PAY"]),
            ("B2G", ["B1G", "-D1PAY", "-D29PAY", "-D39REC_EN_EMPLOIS"]), ("B2N", ["B2G", "-P51C"]),
            ("D2REC", ["D21REC", "D29REC"]), ("D21REC", ["D211REC", "D212REC", "D214REC"]),
            ("D29REC", ["D291REC", "D292REC"]),
            ("D3PAY_EN_RESSOURCES", ["D31PAY_EN_RESSOURCES", "D39PAY_EN_RESSOURCES"]),
            ("D39PAY_EN_RESSOURCES", ["D391PAY_EN_RESSOURCES", "D392PAY_EN_RESSOURCES", "D399PAY_EN_RESSOURCES"]),
            ("D4REC", ["D41REC", "D42REC", "D43REC", "D44REC", "D45REC"]),
            ("D4PAY", ["D41PAY", "D42PAY", "D43PAY", "D44PAY", "D45PAY"]),
            ("D42REC", ["D421REC", "D422REC"]), ("D42PAY", ["D421PAY", "D422PAY"]),
            ("B5G", ["B2G", "D2REC", "D3PAY_EN_RESSOURCES", "D4REC", "-D4PAY"]), ("B5N", ["B5G", "-P51C"]),
            ("D5REC", ["D51REC", "D59REC"]), ("D5PAY", ["D51PAY", "D59PAY"]),
            ("D61REC", ["D611REC", "D612REC", "D613REC"]), ("D613REC", ["D613CEREC", "D613NSIREC"]),
            ("D62PAY", ["D621PAY", "D622PAY", "D623PAY"]),
            ("D7REC", ["D71REC", "D72REC", "?D73REC", "D74REC", "D75REC", "D76REC"]),
            ("D7PAY", ["D71PAY", "D72PAY", "?D73PAY", "D74PAY", "D75PAY", "D76PAY"]),
            ("D7SREC", ["D71REC", "D72REC", "D73S", "D74REC", "D75REC", "D76REC"]),
            ("D7SPAY", ["D71PAY", "D72PAY", "D74PAY", "D75PAY", "D76PAY"]),
            ("D73REC", ["D731REC", "D732REC", "?D733REC"]), ("D73PAY", ["D731PAY", "D732PAY", "?D733PAY"]),
            ("D75REC", ["D751REC", "D759REC"]), ("D75PAY", ["D751PAY", "D759PAY"]),
            ("B6G", ["B5G", "D5REC", "D61REC", "D7REC", "-D5PAY", "-D62PAY", "-D7PAY", "!D7SREC"]),
            ("B6G", ["B5G", "D5REC", "D61REC", "D7SREC", "-D5PAY", "-D62PAY", "-D7SPAY", "!D73REC"]),
            ("B6N", ["B6G", "-P51C"]),
            ("P3", ["P31", "P32"]), ("B8G", ["B6G", "-P3"]), ("B8N", ["B8G", "-P51C"]),
            ("D63PAY", ["D631PAY", "D632PAY"]), ("P31", ["D63PAY"]), ("B7G", ["B6G", "-D63PAY"]), ("B7N", ["B7G", "-P51C"]),
            ("P4", ["P32"]), ("B8G", ["B7G", "-P4"]),
            ("D9REC", ["D91REC", "D92REC", "D99REC"]),
            ("D9PAY_EN_RESSOURCES", ["D91PAY_EN_RESSOURCES", "D92PAY_EN_RESSOURCES", "D99PAY_EN_RESSOURCES"]),
            ("P5", ["P51G", "P52"]), ("B9", ["B8G", "D9REC", "D9PAY_EN_RESSOURCES", "-P5", "-NP"])]
IDENTITES += [(f"SEC2010.{t}", [_prefixee("SEC2010.", c) for c in cs]) for t, cs in _COMPTES]

# Ensembles et leurs parties. S'additionnent : les soldes et les prélèvements obligatoires (concepts
# ADDITIFS), la dette au sens de Maastricht d'un sous-secteur, qui est sa contribution à la dette consolidée de
# l'ensemble, comme sa dette nette ; les parts des sous-secteurs dans la dépense consolidée de l'ensemble des
# administrations publiques (consolidation « consolide_apu ») ; tous les montants des comptes complets (tableaux 7.301
# à 7.306), qui ne sont pas consolidés.
DECOMPOSITIONS = [("S13", ["S1311", "S1313", "S1314"]), ("S1311", ["S13111", "S13112"]), ("S1313", ["S13131", "S13132"]),
                  ("S1314", ["S13141", "S13142"]), ("S13131", ["S131311", "S131312", "S131313", "S131314"]),
                  ("S13_S212", ["S13", "S212"]), ("S13_S212", ["S1311", "S1313", "S1314", "S212"]),
                  ("S1314", ["REGIME_GENERAL", "S1314_HORS_RG"]),
                  ("S1314_HORS_RG", ["CADES", "FRR", "AUTRES_REGIMES_SECU", "S13142"]),
                  ("REGIME_GENERAL", ["REGIME_GENERAL_HORS_FSV", "FSV"]), ("ROBSS_FSV", ["ROBSS", "FSV"]),
                  # La dette trimestrielle donne l'État et les organismes divers d'administration centrale, sans leur
                  # ensemble (« ! » : ne s'applique pas si la source publie ce périmètre).
                  ("S13", ["S13111", "S13112", "S1313", "S1314", "!S1311"])]
ADDITIFS = {"SEC2010.B9", "INSEE_PO.PO", "COMPTES_SECU.RESULTAT_COMPTABLE", "INSEE_DETTE.DETTE_NETTE",
            "INSEE_DETTE.AUTRES_ACTIFS_LIQUIDES"} | {f"PDE.GD{i}" for i in ("", "_F2", "_F3", "_F31", "_F32", "_F4", "_F41",
                                                                          "_F42")}
# Tableaux de l'Insee qui publient chacun un sous-secteur et qu'on réunit pour les additionner ; les comptes complets ne
# sont pas consolidés : tous leurs montants s'additionnent.
FAMILLES_INSEE = {r"insee\.t32(0[1-9]|1[0-4])": "insee.t3201 à t3214", r"insee\.t730[1-6]": "insee.t7301 à t7306"}
COMPTES_COMPLETS = r"insee\.t730[1-6]"
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
# Nombres d'organismes et de collectivités : chaque catégorie contre la somme de celles que la table des périmètres range
# sous elle, et le nombre d'organismes divers d'administration locale contre la somme de leurs catégories.
_UNITES = {p["id"] for p in lire("tables/perimetres.csv") if p["norme_id"] == "UNITES_PUBLIQUES"}
_CATEGORIES = [(t, sorted(p for p in _SOUS[t] if p in _UNITES)) for t in sorted(_UNITES | {"S13132"})
               if any(p in _UNITES for p in _SOUS[t])]
DECOMPOSITIONS_PAR_CONCEPT.update({c["id"]: _CATEGORIES for c in lire("tables/concepts.csv")
                                   if c["norme_id"] == "UNITES_PUBLIQUES"})
# Comptes de la protection sociale (DREES) : les prestations de l'ensemble des régimes contre la somme de celles des
# secteurs, celles de chaque secteur contre la somme de celles de ses régimes (« ? » : un secteur ou un régime n'existe
# pas toutes les années) ; les emplois et les ressources de l'ensemble contre la somme de ceux des groupes de secteurs,
# dont une ligne peut manquer.
_CPS_SECTEURS = sorted(p for _, p in cps.SECTEURS.values())
DECOMPOSITIONS_PAR_CONCEPT[cps.PRESTATIONS] = ([("CPS_ENSEMBLE", ["?" + s for s in _CPS_SECTEURS])]
                                               + [(s, ["?" + r for r in sorted(_SOUS[s])]) for s in _CPS_SECTEURS])
DECOMPOSITIONS_PAR_CONCEPT.update({c["id"]: [("CPS_ENSEMBLE", ["?CPS_SF_SNF", "?CPS_S15", "?CPS_ASSO", "?CPS_APUC_APUL"])]
                                   for c in lire("tables/concepts.csv")
                                   if c["norme_id"] == "CPS" and c["id"] != cps.PRESTATIONS})

# Passerelles entre tableaux qui présentent autrement les mêmes grandeurs : (libellé, termes de gauche, termes
# de droite), chaque terme étant (source, périmètre, concept, signe) et, au besoin, (modèle de période, traitement),
# en montant, pour l'ensemble des fonctions ; le modèle de période nomme l'année vérifiée {annee}, la précédente
# {precedente}. Une source terminée par « * » désigne toute source qui commence ainsi :
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
    ("Déficit des administrations publiques du tableau 3.105 contre leur capacité de financement au sens de Maastricht "
     "(tableau 3.106), de signe opposé",
     [("insee.t3105", "S13", "INSEE_DETTE.DEFICIT", 1)], [("insee.t3106", "S13", "SEC2010.B9", -1)]),
    ("Variation de la dette au sens de Maastricht (tableau 3.105) contre l'écart entre la dette de fin d'année et celle "
     "de l'année précédente (tableau 3.101)",
     [("insee.t3105", "S13", "INSEE_DETTE.VARIATION_DETTE", 1)],
     [("insee.t3101", "S13", "PDE.GD", 1), ("insee.t3101", "S13", "PDE.GD", -1, "{precedente}", "")]),
]
# Dette trimestrielle : l'encours à la fin du quatrième trimestre est celui de la fin de l'année, que donnent les
# tableaux 3.101 (par sous-secteur), 3.102 (par instrument) et 3.103 (dette nette et actifs liquides).
_T4 = ("{annee}-T4", "")
_TRIM = "insee.bdm-dette-trim-apu"
PASSERELLES += [(f"Dette au sens de Maastricht {nom}, au quatrième trimestre (série trimestrielle), contre la dette de "
                 "fin d'année du tableau 3.101", [(_TRIM, p, "PDE.GD", 1, *_T4)], [("insee.t3101", p, "PDE.GD", 1)])
                for p, nom in (("S13", "des administrations publiques"), ("S13111", "de l'État"),
                               ("S13112", "des organismes divers d'administration centrale"),
                               ("S1313", "des administrations publiques locales"),
                               ("S1314", "des administrations de sécurité sociale"))]
PASSERELLES += [(f"Dette au sens de Maastricht des administrations publiques, {nom}, au quatrième trimestre (série "
                 "trimestrielle), contre le tableau 3.102", [(_TRIM, "S13", c, 1, *_T4)], [("insee.t3102", "S13", c, 1)])
                for c, nom in (("PDE.GD_F2", "dépôts"), ("PDE.GD_F3", "titres de créance"),
                               ("PDE.GD_F31", "titres de créance à court terme"),
                               ("PDE.GD_F32", "titres de créance à long terme"), ("PDE.GD_F41", "crédits à court terme"),
                               ("PDE.GD_F42", "crédits à long terme"))]
PASSERELLES += [(f"{nom}, au quatrième trimestre (série trimestrielle), contre le tableau 3.103",
                 [(_TRIM, "S13", c, 1, *_T4)], [("insee.t3103", "S13", c, 1)])
                for c, nom in (("INSEE_DETTE.DETTE_NETTE", "Dette nette des administrations publiques"),
                               ("INSEE_DETTE.AUTRES_ACTIFS_LIQUIDES", "Actions cotées et parts de fonds d'investissement "
                                                                       "détenues par les administrations publiques"))]

# Comptes complets (tableaux 7.301 à 7.306) contre dépenses et recettes (3.201 à 3.214), sous-secteur par sous-secteur :
# (concept des comptes complets, concept des dépenses et recettes, signe). Les seconds consolident les revenus de la
# propriété et les transferts entre administrations, que les premiers ne consolident pas : ces opérations ne se
# comparent pas. Les autres doivent être égales ; les subventions, que les comptes complets inscrivent avec un signe
# négatif, de signe opposé.
COMPTES_ET_TABLEAUX = {"S13": ("insee.t7301", "insee.t3201"), "S1311": ("insee.t7302", "insee.t3202"),
                       "S13111": ("insee.t7303", "insee.t3203"), "S13112": ("insee.t7304", "insee.t3204"),
                       "S1313": ("insee.t7305", "insee.t3205"), "S1314": ("insee.t7306", "insee.t3212")}
OPERATIONS_COMMUNES = [("SEC2010.P11", "SEC2010.P11", 1), ("SEC2010.P12", "SEC2010.P12", 1), ("SEC2010.P2", "SEC2010.P2", 1),
                       ("SEC2010.D1PAY", "SEC2010.D1PAY", 1), ("SEC2010.D122PAY", "SEC2010.D122PAY", 1),
                       ("SEC2010.D29PAY", "SEC2010.D29PAY", 1), ("SEC2010.D39REC_EN_EMPLOIS", "SEC2010.D39REC", -1),
                       ("SEC2010.D2REC", "SEC2010.D2REC", 1), ("SEC2010.D3PAY_EN_RESSOURCES", "SEC2010.D3PAY", -1),
                       ("SEC2010.D5REC", "SEC2010.D5REC", 1), ("SEC2010.D5PAY", "SEC2010.D5PAY", 1),
                       ("SEC2010.D61REC", "SEC2010.D61REC", 1), ("SEC2010.D612REC", "SEC2010.D612REC", 1),
                       ("SEC2010.D62PAY", "SEC2010.D62PAY", 1), ("SEC2010.D632PAY", "SEC2010.D632PAY", 1),
                       ("SEC2010.D91REC", "SEC2010.D91REC", 1), ("SEC2010.P51G", "SEC2010.P51G", 1)]

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
# Unités comparables entre elles une fois converties ; les autres ne se comparent qu'à elles-mêmes. Seules ces familles
# se ventilent par fonction : les montants, et les emplois des plafonds votés.
FAMILLES = {"EUR": ("euros", 1), "K_EUR": ("euros", 1e3), "MIO_EUR": ("euros", 1e6), "MD_EUR": ("euros", 1e9),
            "MIO_ECU_EUR": ("écus puis euros", 1e6), "ETPT": ("équivalents temps plein travaillé", 1),
            "ETP": ("équivalents temps plein", 1)}
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
                              "traitements": traitements, "total": total, "unite": valeur(concepts[total])[2],
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
    """Le solde d'un ensemble, sa dette, ou sa part de la dépense consolidée de l'ensemble des administrations
    publiques, égale la somme de ceux de ses parties, comme chaque montant de ses comptes complets ; de même, un poste
    de la situation patrimoniale de la sécurité sociale égale la somme de ses lignes par entité, et un montant d'un
    niveau de collectivités locales la somme de ceux des niveaux qui le composent, en montant comme en nombre de
    budgets."""
    apu = {k[0] for k, l in derniers.items() if l["consolidation"] == "consolide_apu"}
    par_annee = collections.defaultdict(dict)
    for k, l in derniers.items():
        if valeur(l)[2] != "euros" and k[6] not in DENOMBREMENTS:
            continue
        if k[3] in ADDITIFS or re.fullmatch(COMPTES_COMPLETS, k[0]):
            famille = next((f for motif, f in FAMILLES_INSEE.items() if re.fullmatch(motif, k[0])), k[0])
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
        periode = modele.format(annee=annee, precedente=str(int(annee) - 1))
        trouvees = index.get((perimetre, concept, traitement, periode), {})
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


def comptes_complets(derniers):
    """Pour chaque opération commune, chaque sous-secteur et chaque année : le montant des comptes complets contre celui
    des tableaux des dépenses et recettes, au signe près."""
    index = {(k[0], k[2], k[3], k[7]): l for k, l in derniers.items()
             if k[1] == "FR" and not k[4] and not k[5] and k[6] == "MD_EUR"}
    resultats = collections.defaultdict(list)
    for (source, perimetre, concept, periode), l in sorted(index.items()):
        if COMPTES_ET_TABLEAUX.get(perimetre, ("",))[0] != source:
            continue
        for complets, tableau, signe in OPERATIONS_COMMUNES:
            autre = index.get((COMPTES_ET_TABLEAUX[perimetre][1], perimetre, tableau, periode))
            if concept != complets or autre is None:
                continue
            ecart = valeur(l)[0] - signe * valeur(autre)[0]
            resultats[(complets, tableau, signe)].append({
                "perimetre": perimetre, "annee": periode, "ecart": ecart,
                "juste": not depasse(ecart, valeur(l)[1] + valeur(autre)[1]),
                "revisable": l["statut"] in REVISABLES or autre["statut"] in REVISABLES})
    return resultats


def periode_du_pib(periode):
    """La période du PIB qui sert de dénominateur : l'année, pour un ratio de la fin du quatrième trimestre ; aucune
    pour un autre trimestre, que l'Insee rapporte au cumul du PIB trimestriel, corrigé des variations saisonnières et
    des jours ouvrables, des quatre derniers trimestres, que la base n'a pas."""
    if re.fullmatch(r"[0-9]{4}-T[1-3]", periode):
        return None
    return periode[:4] if re.fullmatch(r"[0-9]{4}-T4", periode) else periode


def ratios(derniers):
    """Recalcule chaque ratio : le même chiffre en montant, divisé par chacun de ses dénominateurs possibles."""
    par_id = {l["id"]: l for l in derniers.values()}
    pib = collections.defaultdict(dict)  # (zone, année) → {source: (valeur, précision)}
    for k, l in derniers.items():
        if k[3] == "SEC2010.B1GQ" and valeur(l)[2] == "euros":
            pib[(k[1], k[7])][k[0]] = valeur(l)[:2]
    resultats = []
    for k, l in sorted(derniers.items()):
        periode = periode_du_pib(k[7])
        numerateur = montant(derniers, k) if k[6] in NOMS_RATIOS and periode else None
        if numerateur is None:
            continue
        indique = par_id.get(l["denominateur_id"])
        if indique:
            regle, attendu, candidats = "indique", indique["source_id"], dict(pib[(k[1], periode)])
            candidats[attendu] = valeur(indique)[:2]
        elif k[6] == "PC_DEPENSE":
            total = montant(derniers, k[:4] + ("",) + k[5:])
            regle, attendu, candidats = "depense", k[0], {k[0]: total[:2]} if total else {}
        else:
            regle, attendu, candidats = "libre", None, dict(pib[(k[1], periode)])
        (n, pn), r, pr = numerateur[:2], float(l["valeur"]), 0.5 * 10 ** -int(l["decimales"])
        par = sorted(s for s, (d, pd) in candidats.items()
                     if d and not depasse(100 * n / d - r, pr + 100 * (pn / d + abs(n) * pd / d ** 2)))
        # Les dénominateurs qui donneraient le ratio publié, arrondis compris.
        implicite = (100 * max(abs(n) - pn, 0) / (abs(r) + pr), 100 * (abs(n) + pn) / (abs(r) - pr)) if abs(r) > pr else None
        resultats.append({"cle": k, "regle": regle, "attendu": attendu, "par": par,
                          "retrouve": attendu in par if attendu else bool(par), "implicite": implicite,
                          "pib": pib[(k[1], periode)] if k[6] == "PC_PIB" else {}})
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
# La dotation globale de fonctionnement que l'État notifie à chaque collectivité, d'après les fichiers de répartition de
# la DGCL, contre celle que la collectivité inscrit à ses comptes (agrégat « Dotation globale de fonctionnement », tous
# budgets). La commune se retrouve par son code Insee de l'exercice, le groupement par son numéro Siren, le département
# par son code, le Bas-Rhin et le Haut-Rhin avec la Collectivité européenne d'Alsace, que les comptes codent tous
# « 67A ». La métropole de Lyon et la Ville de Paris, que deux jeux des comptes donnent, se comparent une fois, avec les
# deux parts de leur dotation : celles d'un groupement et d'un département, celles d'une commune et d'un département. La
# collectivité de Corse et les collectivités territoriales uniques de Martinique et de Guyane ont leurs comptes dans le
# jeu des régions, les syndicats touristiques du jeu des dotations des groupements, dans celui des syndicats.
COMMUNES, GFP, SYNDICATS = "ofgl.base-communes-consolidee", "ofgl.base-gfp-consolidee", "ofgl.base-syndicats-consolidee"
DEPARTEMENTS, REGIONS = "ofgl.base-departements-consolidee", "ofgl.base-regions-consolidee"
DGF = "COMPTES_LOCAUX.DGF"
COMPTES_DES_DOTATIONS = {"ofgl.dotations-communes": COMMUNES, "ofgl.dotations-gfp": GFP,
                         "ofgl.dotations-departements": DEPARTEMENTS}
UNITES_DGF = {"MET69": (GFP, "200046977"), "75": (COMMUNES, "217500016"), "20": (REGIONS, "200076958"),
              "972": (REGIONS, "200055507"), "973": (REGIONS, "200052678")}
TERRITOIRES_DGF = {"67": "67A", "68": "67A"}
NIVEAUX_DGF = {COMMUNES: "communes", GFP: "groupements à fiscalité propre", SYNDICATS: "syndicats",
               DEPARTEMENTS: "départements", REGIONS: "collectivités uniques"}
# Ce que chaque collectivité de niveau départemental déclare verser au SDIS de son territoire, contre ce que celui-ci
# déclare recevoir à son budget principal. Le jeu des départements désigne par « 67A » le Bas-Rhin, le Haut-Rhin puis
# la Collectivité européenne d'Alsace, et par « 691 » la métropole de Lyon ; Paris, les Hauts-de-Seine, la
# Seine-Saint-Denis et le Val-de-Marne n'ont pas de SDIS, la brigade de sapeurs-pompiers de Paris y tenant ce rôle. Dans
# le jeu des régions, la collectivité de Corse et les collectivités territoriales uniques de Martinique et de Guyane ont
# les compétences d'un département.
SDIS = "ofgl.base-sdis"
PAYEURS_SDIS = {"ofgl.base-departements-consolidee", "ofgl.base-regions-consolidee"}
CONTRIBUTIONS_SDIS = "COMPTES_LOCAUX.CONTRIBUTIONS_SDIS"
TERRITOIRES_SDIS = {"67A": ("67", "68"), "691": ("69",)}
SANS_SDIS = {"75", "92", "93", "94"}
SDIS_DES_REGIONS = {"200076958": ("2A", "2B"), "200055507": ("972",), "200052678": ("973",)}
# Rubriques du SDIS où se lit la contribution : les participations des départements, sauf pour la métropole de Lyon et
# les collectivités territoriales uniques, que leur SDIS inscrit parmi les autres participations, puis parmi celles
# des groupements à fiscalité propre ; les collectivités territoriales uniques se comparent aussi aux participations
# des départements, que le SDIS de Martinique emploie en 2016.
_DEP, _GFP, _AUTRES = (f"COMPTES_LOCAUX.{c}" for c in ("PARTICIPATIONS_DEPARTEMENTS", "PARTICIPATIONS_GFP",
                                                       "AUTRES_PARTICIPATIONS_FONCTIONNEMENT"))
RUBRIQUES_SDIS = {"200046977": (_GFP, _AUTRES), "200055507": (_DEP, _GFP, _AUTRES), "200052678": (_DEP, _GFP, _AUTRES)}
# Dépenses de chaque département par fonction (présentation fonctionnelle) : chaque montant y figure à chacun des niveaux
# de sa fonction, d'un à quatre chiffres, et un montant nul n'a pas de ligne. Pour chaque budget et chaque agrégat, une
# fonction se compare à la somme de ses sous-fonctions ; dans chaque fonction s'appliquent les identités comptables
# dont le jeu publie tous les termes ; la somme des fonctions de premier niveau du budget principal de chaque
# collectivité, puis celle de ses budgets annexes réunis, se compare à ses comptes consolidés.
FONCTIONNELLE = "ofgl.base-departements-fonctionnelle"
BUDGET_PRINCIPAL = "1"  # « cbudg » du budget principal, « 3 » pour un budget annexe
# Fiscalité directe locale (fichier REI de la DGFiP, d'après l'OFGL) : le produit de chaque ligne qui donne sa base et
# son taux net contre leur produit ; le taux net contre le taux voté ; la taxe d'enlèvement des ordures ménagères
# recensée sur l'ensemble des communes contre celle qu'inscrivent les comptes consolidés des communes, des groupements
# à fiscalité propre et des syndicats, le REI ne disant pas lequel la perçoit.
FISCALE = "ofgl.base-fiscale-simplifiee"
TEOM = "COMPTES_LOCAUX.TEOM"
COMPTES_TEOM = (COMMUNES, GFP, SYNDICATS)
SEUIL_PRODUIT = 0.01  # écart relatif du produit à la base multipliée par le taux au-delà duquel une ligne est citée


def listes_collectivites():
    """{(source, exercice): {siren: fiche}} : la liste la plus récente des collectivités de chaque exercice."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    retenues = {}
    for i in lire("tables/fichiers_collectivites.csv"):
        cle = (i["source_id"], i["exercice"])
        if i["contenu"] == "collectivites" and (cle not in retenues or i["version"] > retenues[cle]["version"]):
            retenues[cle] = i
    return {cle: ofgl.collectivites(fichiers[i["fichier_id"]])[0] for cle, i in sorted(retenues.items())}


def montants_retenus():
    """{(source, exercice): inscription} : la copie des montants la plus récente de chaque exercice de chaque jeu."""
    retenus = {}
    for i in lire("tables/fichiers_collectivites.csv"):
        cle = (i["source_id"], i["exercice"])
        if i["contenu"] == "montants" and (cle not in retenus or i["version"] > retenus[cle]["version"]):
            retenus[cle] = i
    return retenus


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
    contre sa fiche de la DGCL. Pour un jeu publié budget par budget : les identités comptables de chaque budget. Enfin,
    les contributions des collectivités de niveau départemental aux SDIS contre les participations que ceux-ci
    reçoivent."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    agregats = {a["agregat"]: a for a in lire("tables/agregats_ofgl.csv")}
    # Le jeu fonctionnel des départements et celui de la fiscalité directe locale ont leurs propres contrôles
    # (fonctions_departements, fiscalite_locale).
    a_part = ofgl.PAR_FONCTION | ofgl.FISCALITE
    retenus = {cle: i for cle, i in montants_retenus().items() if cle[0] not in a_part}
    presences = collections.defaultdict(list)  # (exercice, siren) → jeux dont la liste porte la collectivité
    for (source, exercice), fiches in listes.items():
        if source in ofgl.DOTATIONS or source in a_part:
            continue
        for siren in sorted({f["siren"] for f in fiches.values()}) if source in ofgl.PAR_BUDGET else fiches:
            presences[(exercice, siren)].append(source)
    doubles = {cle: jeux for cle, jeux in presences.items() if len(jeux) > 1}
    identites = [(t, c) for t, c in IDENTITES if t.startswith("COMPTES_LOCAUX.")]
    exercices, sommes_controlees, fiches_controlees, comptes_doubles = [], [], [], {}
    controles = collections.defaultdict(lambda: [0, 0, None])  # (source, total, budget) → [vérifiées, en écart, pire]
    contributions = {}  # (exercice, source, siren) → (contribution aux SDIS, tous budgets, marge d'arrondi)
    teom = collections.defaultdict(lambda: [0.0, 0.0])  # (exercice, source) → [TEOM, tous budgets, marge d'arrondi]
    # (exercice, département du SDIS, concept) → [participation reçue au budget principal, marge] ; (exercice,
    # département) → nom du SDIS
    participations, noms_sdis = collections.defaultdict(lambda: [0.0, 0.0]), {}
    # (exercice, jeu des dotations, collectivité) → {variable: (montant notifié, marge)} ; (exercice, jeu des comptes,
    # siren) → (dotation globale de fonctionnement inscrite, tous budgets, marge)
    notifiees, inscrites = collections.defaultdict(dict), {}
    for (source, exercice), inscrit in sorted(retenus.items()):
        if source in ofgl.DOTATIONS:
            for code, variable, montant_, marge_ in ofgl.montants_dotations(fichiers[inscrit["fichier_id"]], marges=True):
                notifiees[(exercice, source, code)][variable] = (montant_, marge_)
            continue
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
                fiche = (fiches or {}).get(budget)
                if source == SDIS and fiche is not None and fiche["cbudg"] == "1":
                    noms_sdis[(exercice, fiche["code_dep"])] = fiche["lbudg"]
                    for concept in (_DEP, _GFP, _AUTRES):
                        if concept in montants:
                            cellule = participations[(exercice, fiche["code_dep"], concept)]
                            cellule[0] += montants[concept][0]
                            cellule[1] += montants[concept][1]
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
        if source in PAYEURS_SDIS:
            contributions.update({(exercice, source, s): (m[CONTRIBUTIONS_SDIS][3], m[CONTRIBUTIONS_SDIS][7])
                                  for s, m in par_siren.items() if CONTRIBUTIONS_SDIS in m})
        inscrites.update({(exercice, source, s): (m[DGF][3], m[DGF][7]) for s, m in par_siren.items() if DGF in m})
        if source in COMPTES_TEOM:
            for m in par_siren.values():
                if TEOM in m:
                    teom[(exercice, source)][0] += m[TEOM][3]
                    teom[(exercice, source)][1] += m[TEOM][7]
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
    return (exercices, controles, sommes_controlees, memes, fiches_controlees,
            (dotations_dgf(listes, notifiees, inscrites), flux_sdis(listes, contributions, participations, noms_sdis)),
            teom)


def unite_dgf(listes, insee, exercice, source, code):
    """Les comptes auxquels se compare la dotation notifiée à une collectivité : (jeu des comptes, numéro Siren), ou pour
    un département (jeu des départements, code de département) ; rien si elle n'a pas de comptes dans ces jeux. Un code
    du jeu des départements désigne un département des comptes s'il en est un, sinon la collectivité qui en tient lieu
    (la Ville de Paris depuis 2019)."""
    if source == "ofgl.dotations-communes":
        siren = insee.get((exercice, code))
        return (COMMUNES, siren) if siren else None
    if source == "ofgl.dotations-gfp":
        return next(((jeu, code) for jeu in (GFP, SYNDICATS) if code in listes.get((jeu, exercice), {})), None)
    departement = TERRITOIRES_DGF.get(code, code)
    if any(f["dep_code"] == departement and f["categ"] == "DEPT" for f in listes.get((DEPARTEMENTS, exercice), {}).values()):
        return (DEPARTEMENTS, departement)
    if code in UNITES_DGF:
        jeu, siren = UNITES_DGF[code]
        return (jeu, siren) if siren in listes.get((jeu, exercice), {}) else None
    return None


def sirens_dgf(listes, exercice, unite):
    """Les collectivités dont les comptes forment une unité : une seule, ou les départements d'un même code."""
    jeu, cle = unite
    if jeu != DEPARTEMENTS:
        return [cle]
    return sorted(s for s, f in listes.get((jeu, exercice), {}).items() if f["dep_code"] == cle and f["categ"] == "DEPT")


def dotations_dgf(listes, notifiees, inscrites):
    """La dotation globale de fonctionnement que l'État notifie contre celle que chaque collectivité inscrit à ses
    comptes : les identités de la dotation notifiée {(source, total, parties, montant): [vérifiées, en écart, pire]}, les
    comparaisons [(exercice, unité, dotations [(source, code)], notifié, inscrit, égaux à l'arrondi près)], les
    dotations notifiées à une collectivité sans comptes [(exercice, source, code, notifié)], les dotations inscrites
    sans notification [(exercice, jeu des comptes, siren, inscrit)], pour les exercices dont on a les deux, et les
    dotations notifiées en parties seulement, sans total [(exercice, source, code)], qui ne se comparent pas."""
    identites = collections.defaultdict(lambda: [0, 0, None])
    insee = {(exercice, f["insee"]): s for (jeu, exercice), fiches in listes.items() if jeu == COMMUNES
             for s, f in fiches.items()}
    unites = collections.defaultdict(lambda: [[], 0.0, 0.0])  # (exercice, unité) → [dotations, notifié, marge]
    sans_comptes, sans_total, exercices = [], [], collections.defaultdict(set)  # jeu des comptes → exercices comparés
    lues = set()  # comptes auxquels se compare une dotation, ou qu'une dotation sans total laisse sans comparaison
    for (exercice, source, code), montants in sorted(notifiees.items()):
        total, *parties = ofgl.DOTATIONS[source][2]
        identites_comptables(identites, [(total, ["?" + p for p in parties])], source, exercice, code, montants,
                             [(BUDGET_SEUL, 0, 1)])
        if total not in montants:
            sans_total.append((exercice, source, code))
        if (COMPTES_DES_DOTATIONS[source], exercice) not in listes:
            continue
        exercices[COMPTES_DES_DOTATIONS[source]].add(exercice)
        unite = unite_dgf(listes, insee, exercice, source, code)
        if total not in montants:
            if unite is not None:
                lues.update((exercice, unite[0], s) for s in sirens_dgf(listes, exercice, unite))
            continue
        if unite is None:
            sans_comptes.append((exercice, source, code, montants[total][0]))
            continue
        groupe = unites[(exercice, unite)]
        groupe[0].append((source, code))
        groupe[1] += montants[total][0]
        groupe[2] += montants[total][1]
    comparaisons = []
    for (exercice, unite), (dotations, notifie, marge) in sorted(unites.items()):
        sirens = sirens_dgf(listes, exercice, unite)
        cellules = [inscrites.get((exercice, unite[0], s), (0.0, 0.0)) for s in sirens]
        lues.update((exercice, unite[0], s) for s in sirens)
        inscrit, marge_inscrit = sum(c[0] for c in cellules), sum(c[1] for c in cellules)
        comparaisons.append((exercice, unite, dotations, notifie, inscrit,
                             not depasse(notifie - inscrit, marge + marge_inscrit)))
    # Une dotation inscrite que rien ne notifie, dans un jeu et un exercice comparés : le jeu des départements ne compte
    # que ses départements, la métropole de Lyon et la Ville de Paris se comparant avec les groupements et les communes.
    exercices[REGIONS], exercices[SYNDICATS] = exercices[DEPARTEMENTS], exercices[GFP]
    sans_notification = [(exercice, jeu, siren, m) for (exercice, jeu, siren), (m, _) in sorted(inscrites.items())
                         if exercice in exercices.get(jeu, ()) and (exercice, jeu, siren) not in lues and m
                         and (jeu != DEPARTEMENTS or listes.get((jeu, exercice), {}).get(siren, {}).get("categ") == "DEPT")]
    return identites, comparaisons, sans_comptes, sans_notification, sans_total


def flux_sdis(listes, contributions, participations, noms_sdis):
    """Les contributions aux SDIS contre les participations reçues : les comparaisons [(exercice, payeurs [(source,
    siren)], départements des SDIS, rubriques, noms des SDIS, versé, reçu, égaux à l'arrondi près)], les contributions
    sans SDIS [(exercice, source, siren, versé, territoire reconnu)], et les participations des départements
    qu'aucune contribution ne déclare [(exercice, département du SDIS, nom du SDIS, reçu)]."""
    groupes = collections.defaultdict(lambda: [[], 0.0, 0.0])  # (exercice, SDIS, rubriques) → [payeurs, versé, marge]
    sans_sdis = []
    for (exercice, source, siren), (verse, marge) in sorted(contributions.items()):
        if source == "ofgl.base-regions-consolidee":
            codes = SDIS_DES_REGIONS.get(siren)
        else:
            dep = listes.get((source, exercice), {}).get(siren, {}).get("dep_code")
            codes = () if dep in SANS_SDIS else TERRITOIRES_SDIS.get(dep, (dep,)) if dep else None
        if not codes:
            sans_sdis.append((exercice, source, siren, verse, codes is not None))
            continue
        groupe = groupes[(exercice, codes, RUBRIQUES_SDIS.get(siren, (_DEP,)))]
        groupe[0].append((source, siren))
        groupe[1] += verse
        groupe[2] += marge
    comparaisons, lues = [], set()
    for (exercice, codes, rubriques), (payeurs, verse, marge) in sorted(groupes.items()):
        cellules = [participations.get((exercice, code, r), [0.0, 0.0]) for code in codes for r in rubriques]
        lues.update((exercice, code, r) for code in codes for r in rubriques)
        recu, marge_recu = sum(c[0] for c in cellules), sum(c[1] for c in cellules)
        nom_sdis = " et ".join(noms_sdis.get((exercice, code), code) for code in codes)
        comparaisons.append((exercice, payeurs, codes, rubriques, nom_sdis, verse, recu,
                             not depasse(verse - recu, marge + marge_recu)))
    orphelines = [(exercice, code, noms_sdis.get((exercice, code), code), m) for (exercice, code, r), (m, _) in
                  sorted(participations.items()) if r == _DEP and (exercice, code, r) not in lues and m]
    return comparaisons, sans_sdis, orphelines


def termes_identite(composantes):
    """[(signe, concept)] des composantes d'une identité, sans leurs marques."""
    termes = [c.lstrip("?!") for c in composantes]
    return [(-1 if t.startswith("-") else 1, t.lstrip("-")) for t in termes]


def fonctions_departements(listes):
    """Pour chaque exercice du jeu fonctionnel des départements, dans sa version la plus récente : les budgets de chaque
    nomenclature ; chaque fonction contre la somme de ses sous-fonctions, pour chaque budget et chaque agrégat ; les
    identités comptables dans chaque fonction de chaque budget, une partie sans ligne valant zéro ; la somme des
    fonctions de premier niveau de chaque collectivité contre ses comptes consolidés, budget principal puis budgets
    annexes. Pour l'ensemble des exercices : les libellés de chaque fonction et les regroupements du portail."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    agregats = {a["agregat"]: a for a in lire("tables/agregats_ofgl.csv")}
    retenus = montants_retenus()
    identites_locales = [(t, termes_identite(cs)) for t, cs in IDENTITES if t.startswith("COMPTES_LOCAUX.")]
    exercices = []  # (exercice, version, statut, {(nomenclature, type de budget): budgets}, lignes)
    sous_fonctions = [0, 0]  # fonctions comparées à leurs sous-fonctions, égales
    # (exercice, siren, budget, nomenclature, concept, fonction, libellé, montant, somme des sous-fonctions)
    ecarts_sous_fonctions = []
    identites = collections.defaultdict(lambda: [0, 0, None])  # (total, parties) → [vérifiées, en écart, pire]
    consolides = []  # (exercice, siren, budgets, concept, somme des fonctions, consolidé, égaux)
    absents = []  # (exercice, siren, jeu qui ne le donne pas)
    # (nomenclature, fonction) → {libellé: exercices}
    libelles = collections.defaultdict(lambda: collections.defaultdict(set))
    regroupements = collections.defaultdict(set)  # (nomenclature, fonction) → regroupements
    for (source, exercice), inscrit in sorted(retenus.items()):
        if source != FONCTIONNELLE:
            continue
        fiches = listes.get((FONCTIONNELLE, exercice), {})
        par_agregat = collections.defaultdict(dict)  # (budget, concept) → {fonction: (montant, marge)}
        par_fonction = collections.defaultdict(dict)  # (budget, fonction) → {concept: (montant, marge)}
        sirens, nomenclatures, publies, noms = {}, {}, set(), {}  # noms : (nomenclature, fonction) → premier libellé
        for siren, budget, nomen, fonction, libelle, regroupement, agregat, montant_, marge_ in \
                ofgl.montants_fonctions(fichiers[inscrit["fichier_id"]], agregats, marges=True):
            concept = agregats[agregat]["concept_id"]
            par_agregat[(budget, concept)][fonction] = (montant_, marge_)
            par_fonction[(budget, fonction)][concept] = (montant_, marge_)
            sirens[budget], nomenclatures[budget] = siren, nomen
            publies.add(concept)
            libelles[(nomen, fonction)][libelle].add(exercice)
            noms.setdefault((nomen, fonction), libelle)
            regroupements[(nomen, fonction)].add(regroupement)
        # Le type de chaque budget, d'après sa fiche (« ? » sans fiche) ; les collectivités du jeu.
        types = {b: "?" if b not in fiches else "BP" if fiches[b]["cbudg"] == BUDGET_PRINCIPAL else "BA" for b in sirens}
        collectivites_ = set(sirens.values())
        exercices.append((exercice, inscrit["version"], inscrit["statut"],
                          collections.Counter((nomenclatures[b], types[b]) for b in sirens), int(inscrit["lignes"])))
        # Chaque fonction dont une sous-fonction a une ligne contre la somme de ses sous-fonctions.
        for (budget, concept), par_code in par_agregat.items():
            enfants = collections.defaultdict(list)  # fonction → ses sous-fonctions qui ont une ligne
            for f in par_code:
                if len(f) > 1:
                    enfants[f[:-1]].append(f)
            for parent, liste in sorted(enfants.items()):
                m, marge_ = par_code.get(parent, (0.0, 0.0))
                somme = sum(par_code[f][0] for f in liste)
                sous_fonctions[0] += 1
                if depasse(m - somme, marge_ + sum(par_code[f][1] for f in liste)):
                    ecarts_sous_fonctions.append((exercice, sirens[budget], budget, nomenclatures[budget], concept,
                                                  parent, noms.get((nomenclatures[budget], parent), ""), m, somme))
                else:
                    sous_fonctions[1] += 1
        # Les identités dont le jeu publie, cet exercice, le total et toutes les parties.
        applicables = [(t, p) for t, p in identites_locales if t in publies and all(c in publies for _, c in p)]
        for (budget, fonction), montants in par_fonction.items():
            for total, parties in applicables:
                if total not in montants and not any(c in montants for _, c in parties):
                    continue
                termes = {c: montants.get(c, (0.0, 0.0)) for c in [total] + [c for _, c in parties]}
                ecart = termes[total][0] - sum(s * termes[c][0] for s, c in parties)
                entree = identites[(total, tuple(c for _, c in parties))]
                entree[0] += 1
                if depasse(ecart, sum(v[1] for v in termes.values())):
                    entree[1] += 1
                    if entree[2] is None or abs(ecart) > abs(entree[2][0]):
                        entree[2] = (ecart, exercice, budget, fonction)
        # La somme des fonctions de premier niveau, budget principal puis budgets annexes réunis, contre les comptes
        # consolidés de la collectivité.
        sommes = collections.defaultdict(lambda: [0.0, 0.0])  # (siren, budgets, concept) → [somme, marge]
        for (budget, concept), par_code in par_agregat.items():
            if types[budget] == "?":
                continue
            cellule = sommes[(sirens[budget], types[budget], concept)]
            for f, (m, marge_) in par_code.items():
                if len(f) == 1:
                    cellule[0] += m
                    cellule[1] += marge_
        temoin = retenus.get((DEPARTEMENTS, exercice))
        if temoin is None or not fiches:  # sans liste, le type de chaque budget n'est pas connu
            continue
        comptes = {}  # (siren, budgets, concept) → (montant, marge)
        for siren, agregat, bp, ba, _, _, marge_bp, marge_ba, _, _ in ofgl.montants(fichiers[temoin["fichier_id"]],
                                                                                    agregats, marges=True):
            concept = agregats[agregat]["concept_id"]
            if concept in publies:
                comptes[(siren, "BP", concept)] = (bp, marge_bp)
                comptes[(siren, "BA", concept)] = (ba, marge_ba)
        a_comptes = {cle[0] for cle in comptes}
        absents += [(exercice, s, DEPARTEMENTS) for s in sorted(collectivites_ - a_comptes)]
        absents += [(exercice, s, FONCTIONNELLE) for s in sorted(a_comptes - collectivites_)]
        for cle in sorted(set(sommes) | set(comptes)):
            if cle[0] not in a_comptes or cle[0] not in collectivites_:
                continue
            somme, marge_somme = sommes.get(cle, (0.0, 0.0))
            publie, marge_publie = comptes.get(cle, (0.0, 0.0))
            if somme or publie:
                consolides.append((exercice, *cle, somme, publie, not depasse(somme - publie, marge_somme + marge_publie)))
    return (exercices, sous_fonctions, ecarts_sous_fonctions, identites, consolides, absents, libelles,
            regroupements)


def fiscalite_locale():
    """Pour chaque exercice du jeu de la fiscalité directe locale, dans sa version la plus récente : les communes, les
    lignes et celles que masque le secret statistique ; pour chaque taxe et chaque bénéficiaire, le produit contre la
    base multipliée par le taux net, et le taux net contre le taux voté ; la taxe d'enlèvement des ordures ménagères
    recensée sur l'ensemble des communes."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    exercices = []  # (exercice, version, statut, communes, lignes, lignes sous secret statistique)
    # (taxe, bénéficiaire) → [lignes comparées, égales à l'arrondi près, écart de moins de SEUIL_PRODUIT, au-delà, pire
    # écart au-delà (écart, base multipliée par le taux, exercice, commune)]
    produits = collections.defaultdict(lambda: [0, 0, 0, 0, None])
    taux = collections.Counter()  # (taxe, bénéficiaire) → lignes dont le taux net n'est pas le taux voté
    teom = collections.defaultdict(lambda: [0.0, 0.0])  # exercice → [TEOM recensée, marge d'arrondi]
    for (source, exercice), inscrit in sorted(montants_retenus().items()):
        if source != FISCALE:
            continue
        lues = ofgl.montants_fiscalite(fichiers[inscrit["fichier_id"]], marges=True)
        exercices.append((exercice, inscrit["version"], inscrit["statut"], len({l[0] for l in lues}), len(lues),
                          sum(1 for l in lues if l[7])))
        for commune, taxe, destinataire, base, net, vote, produit, _, marge_base, marge_taux, marge_produit in lues:
            if taxe == "TEOM" and produit is not None:
                teom[exercice][0] += produit
                teom[exercice][1] += marge_produit
            if net is not None and vote is not None and depasse(net - vote, 1e-6):
                taux[(taxe, destinataire)] += 1
            if base is None or net is None or produit is None:
                continue
            calcule = base * net / 100
            ecart = produit - calcule
            entree = produits[(taxe, destinataire)]
            entree[0] += 1
            if not depasse(ecart, marge_produit + base * marge_taux / 100 + net * marge_base / 100):
                entree[1] += 1
            elif abs(ecart) < SEUIL_PRODUIT * abs(calcule):
                entree[2] += 1
            else:
                entree[3] += 1
                if entree[4] is None or abs(ecart) > abs(entree[4][0]):
                    entree[4] = (ecart, calcule, exercice, commune)
    return exercices, produits, taux, teom


# Les impositions de la base simplifiée de l'OFGL (taxe, bénéficiaires) et les destinataires du REI dont elle les tire :
# la part intercommunale de la CFE se compare toutes zones réunies, l'OFGL ne la répartissant pas entre les régimes
# fiscaux comme le REI ; l'effet du coefficient correcteur, que l'OFGL range dans la TFPB des communes, n'est pas un
# impôt.
COMPARAISONS_REI = [
    ("TFPB", ("Commune",), ("commune",)), ("TFPB", ("Syndicat",), ("syndicats",)), ("TFPB", ("GFP",), ("groupement",)),
    ("TFPB", ("Département",), ("département",)), ("TFPB", ("Région (TASA)",), ("région Île-de-France (TASA)",)),
    ("TFPB", ("GFP (GEMAPI)",), ("groupement (GEMAPI)",)),
    ("TFPNB", ("Commune",), ("commune",)), ("TFPNB", ("Syndicat",), ("syndicats",)), ("TFPNB", ("GFP",), ("groupement",)),
    ("TFPNB", ("GFP (GEMAPI)",), ("groupement (GEMAPI)",)),
    ("CFE", ("Commune",), ("commune",)), ("CFE", ("Syndicat",), ("syndicats",)),
    ("CFE", ("GFP / hors zone", "GFP / en ZAE", "GFP / en zone éolienne"),
     ("groupement, fiscalité additionnelle ou de zone, hors zone", "groupement, fiscalité unique ou zone d'activités",
      "groupement, zone éolienne")),
    ("CFE", ("Région (TASA)",), ("région Île-de-France (TASA)",)), ("CFE", ("GFP (GEMAPI)",), ("groupement (GEMAPI)",)),
    ("TEOM", ("Divers / zone taux plein",), ("zone à taux plein",)),
    ("TEOM", ("Divers / zone taux réduit A",), ("zone à taux réduit A",)),
    ("TEOM", ("Divers / zone taux réduit B",), ("zone à taux réduit B",)),
    ("TEOM", ("Divers / zone taux réduit C",), ("zone à taux réduit C",)),
    ("TEOM", ("Divers / zone taux réduit D",), ("zone à taux réduit D",))]
# Le niveau qui perçoit chaque part, d'après son destinataire ; pour la part fixe de la TEOM, que le REI donne par zone de
# taux, d'après le niveau que la fiche de la commune dit la percevoir.
NIVEAUX_REI = [(r"zone à ", None), (r"(part incitative, )?commune", "communes"),
               (r"(part incitative, )?syndicats", "syndicats"),
               (r"(part incitative, )?groupement|métropole du Grand Paris", "groupements"), (r"département", "départements"),
               (r"région", "régions"), (r"État", "État"), (r"", "organismes")]
NIVEAUX_TEOM = {"1": "communes", "2": "syndicats", "3": "groupements"}
ORDRE_NIVEAUX = ["communes", "syndicats", "groupements", "départements", "régions", "organismes", "État", "non dit"]
NIVEAUX_COMPTES_TEOM = [("communes", COMMUNES), ("groupements", GFP), ("syndicats", SYNDICATS)]


def niveau_rei(destinataire, teom_niveau):
    for motif, niveau in NIVEAUX_REI:
        if re.match(motif, destinataire):
            return NIVEAUX_TEOM.get(teom_niveau, "non dit") if niveau is None else niveau


def copies_rei():
    """{exercice: inscription} : la copie du REI la plus récente de chaque année."""
    retenues = {}
    for i in lire("tables/fichiers_rei.csv"):
        if i["exercice"] not in retenues or i["version"] > retenues[i["exercice"]]["version"]:
            retenues[i["exercice"]] = i
    return retenues


def recensement():
    """Pour chaque année du REI, dans sa copie la plus récente : son inscription et le nombre d'impositions retenues ;
    pour chaque taxe et chaque destinataire, le produit contre la base multipliée par le taux net ; chaque imposition de
    la base simplifiée de l'OFGL contre celles du REI dont elle est tirée, commune par commune ; le produit de chaque
    taxe, celui de chaque niveau de collectivité ou d'organisme, et la TEOM de chaque niveau, chaque année."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/variables_rei.csv")
    simplifiee = montants_retenus()
    annees = []  # (inscription, impositions retenues)
    # (taxe, destinataire) → [lignes comparées, égales à l'arrondi près, écart de moins de SEUIL_PRODUIT, au-delà, pire
    # écart au-delà (écart, base multipliée par le taux, exercice, commune, nom)]
    produits = collections.defaultdict(lambda: [0, 0, 0, 0, None])
    # (taxe, bénéficiaires de l'OFGL) → [exercices, communes comparées, égales, en écart, sous secret statistique dans
    # la base simplifiée, produit de la base simplifiée, produit du REI, pire écart (écart, exercice, commune, nom)]
    comparaisons = collections.defaultdict(lambda: [set(), 0, 0, 0, 0, 0.0, 0.0, None])
    par_taxe = collections.defaultdict(float)  # (taxe, exercice) → produit
    communes_taxe = collections.defaultdict(set)  # (taxe, exercice) → communes où le REI donne un produit de la taxe
    par_niveau = collections.defaultdict(float)  # (niveau, exercice) → produit
    teom = collections.defaultdict(float)  # (niveau, exercice) → TEOM, part fixe et part incitative
    for exercice, inscrit in sorted(copies_rei().items()):
        _, variables, _, lignes = rei.lignes_communes(fichiers[inscrit["fichier_id"]])
        retenus = rei.postes(exercice, variables, referentiel, inscrit["fichier_id"])
        recenses, noms, nombre = {}, {}, 0  # (commune, taxe, destinataire) → produit ; commune → nom
        for commune, valeurs in lignes:
            noms[commune] = valeurs["LIBCOM"].strip()
            teom_niveau = valeurs.get("F71", "").strip()
            for taxe, destinataire, base, net, _, produit, m_base, m_net, _, m_produit in rei.impositions(
                    valeurs, retenus, marges=True):
                nombre += 1
                if produit is None:
                    continue
                recenses[(commune, taxe, destinataire)] = produit
                niveau = niveau_rei(destinataire, teom_niveau)
                par_taxe[(taxe, exercice)] += produit
                communes_taxe[(taxe, exercice)].add(commune)
                par_niveau[(niveau, exercice)] += produit
                if taxe == "TEOM":
                    teom[(niveau, exercice)] += produit
                if base is None or net is None:
                    continue
                calcule = base * net / 100
                ecart = produit - calcule
                entree = produits[(taxe, destinataire)]
                entree[0] += 1
                if not depasse(ecart, m_produit + base * m_net / 100 + net * m_base / 100):
                    entree[1] += 1
                elif abs(ecart) < SEUIL_PRODUIT * abs(calcule):
                    entree[2] += 1
                else:
                    entree[3] += 1
                    if entree[4] is None or abs(ecart) > abs(entree[4][0]):
                        entree[4] = (ecart, calcule, exercice, commune, noms[commune])
        annees.append((inscrit, nombre))
        inscrit_ofgl = simplifiee.get((FISCALE, exercice))
        if not inscrit_ofgl:
            continue
        publies = {(c, taxe, b): produit for c, taxe, b, _, _, _, produit, _
                   in ofgl.montants_fiscalite(fichiers[inscrit_ofgl["fichier_id"]])}
        communes = {c for c, _, _ in publies} | {c for c, _, _ in recenses}
        for taxe, beneficiaires, destinataires in COMPARAISONS_REI:
            entree = comparaisons[(taxe, beneficiaires)]
            for commune in communes:
                o = [publies.get((commune, taxe, b), 0.0) for b in beneficiaires]
                r = sum(recenses.get((commune, taxe, d), 0.0) for d in destinataires)
                if not r and not any(o):
                    continue
                entree[0].add(exercice)
                if None in o:
                    entree[4] += 1
                    continue
                ecart = r - sum(o)
                entree[1] += 1
                entree[5] += sum(o)
                entree[6] += r
                if depasse(ecart, 0.5 * (len(beneficiaires) + len(destinataires))):
                    entree[3] += 1
                    if entree[7] is None or abs(ecart) > abs(entree[7][0]):
                        entree[7] = (ecart, exercice, commune, noms.get(commune, ""))
                else:
                    entree[2] += 1
    return annees, produits, comparaisons, par_taxe, {k: len(v) for k, v in communes_taxe.items()}, par_niveau, teom


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

    # Un total qu'un traitement définit (un cumul, une variation) le dit, pour qu'on ne le prenne pas pour un encours.
    libelles = {t["id"]: t["libelle"][0].lower() + t["libelle"][1:] for t in lire("tables/traitements.csv")}

    def total_lisible(r):
        traitements = [libelles[t] for t in r["traitements"].split(";") if t]
        return r["total"] + (f" ({', '.join(traitements)})" if traitements else "")

    if ecarts:
        lignes += ["| Source | Périmètre | Fonction | Année | Total | Total publié | Somme des composantes | Écart |",
                   "|---|---|---|---|---|---|---|---|"]
        lignes += [f"| {r['source']} | {r['perimetre']} | {r['fonction'] or 'ensemble'} | {r['periode']} | {total_lisible(r)} | "
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
              "des administrations publiques (tableau 3.307 de l'Insee), contre la somme de ceux de ses parties ; de "
              "même sa dette au sens de Maastricht, ses instruments et sa dette nette, celles d'un sous-secteur étant "
              "sa contribution à la dette consolidée de l'ensemble (tableaux 3.101 à 3.104 et dette trimestrielle), "
              "et chaque montant de ses comptes complets, qui ne sont pas consolidés (tableaux 7.301 à 7.306) ; pour "
              "la sécurité sociale, le résultat du régime général et celui des régimes de base, Fonds de solidarité "
              "vieillesse compris, contre la somme des leurs et de celui du FSV, et chaque poste de la situation "
              "patrimoniale (annexe A des lois de financement) contre la somme de ses lignes par entité ; pour les "
              "collectivités locales, dont la source ne consolide pas les montants entre niveaux, chaque montant d'un "
              "niveau contre la somme de ceux des niveaux qui le composent, et celui des groupements à fiscalité propre "
              "contre la somme de leurs types (annexes 2A et 2B des rapports de l'OFGL, budgets principaux et budgets "
              "annexes), le nombre de budgets de l'ensemble des collectivités contre la somme de ceux de ses niveaux, "
              "chaque total des publications de la DGCL contre la somme de ses départements ou de ses régions ; pour "
              "les décomptes d'organismes et de collectivités, chaque catégorie contre la somme de ses sous-catégories "
              "(organismes divers d'administration locale de l'Insee, collectivités et groupements de la DGCL).", "",
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
              "trésorerie d'un ensemble consolidé égalent la somme de celles de ses parties. La dette à la fin du "
              "quatrième trimestre est celle de la fin de l'année.", "",
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
    lignes.append("")
    complets = comptes_complets(derniers)
    if complets:
        lignes += ["Les comptes complets des tableaux 7.301 à 7.306 et les dépenses et recettes des tableaux 3.201 à 3.214 "
                   "présentent les mêmes opérations, sous-secteur par sous-secteur. Les premiers ne sont pas consolidés ; "
                   "les seconds consolident les revenus de la propriété et les transferts entre administrations, qui ne "
                   "se comparent donc pas. Les autres opérations doivent être égales ; les subventions, que les comptes "
                   "complets inscrivent avec un signe négatif, de signe opposé. L'épargne brute et la capacité de "
                   "financement, que la consolidation ne change pas, se comparent à la section 6.", "",
                   "| Comptes complets | Dépenses et recettes | Comparaisons | En écart | dont hors chiffres révisables | "
                   "Plus grand écart (comptes complets − dépenses et recettes) |", "|---|---|---|---|---|---|"]
        for operation in OPERATIONS_COMMUNES:
            liste = complets.get(operation)
            if not liste:
                continue
            ecarts = [r for r in liste if not r["juste"]]
            fermes = [r for r in ecarts if not r["revisable"]]
            plus = plus_grand(ecarts, lambda x: x["ecart"]) if ecarts else None
            texte = (f"{ecart_lisible(plus['ecart'], 'euros')} ({plus['perimetre']}, {plus['annee']})" if plus
                     else "aucun")
            lignes.append(f"| {operation[0]} | {'−' if operation[2] < 0 else ''}{operation[1]} | {len(liste)} | "
                          f"{len(ecarts)} | {len(fermes)} | {texte} |")
        lignes.append("")
    return lignes


def partie_ratios(derniers):
    resultats = ratios(derniers)
    lignes = ["## 5. Ratios", "",
              "Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé "
              "si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.", ""]
    trimestriels = sum(1 for k in derniers if k[6] in NOMS_RATIOS and periode_du_pib(k[7]) is None)
    if trimestriels:
        lignes += [f"La dette trimestrielle en % du PIB rapporte l'encours, à la fin du quatrième trimestre, au PIB de "
                   f"l'année, et les autres trimestres au cumul du PIB trimestriel, corrigé des variations saisonnières "
                   f"et des jours ouvrables, des quatre derniers trimestres, que la base n'enregistre pas : ces "
                   f"{trimestriels} ratios-là ne sont pas recalculés.", ""]
    lignes += ["| Dénominateur | Ratios | Retrouvés | Non retrouvés |", "|---|---|---|---|"]
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
    """Le libellé d'une collectivité dans la liste la plus récente de l'exercice, ou son nom dans celle d'un jeu des
    dotations ou de la fiscalité directe locale."""
    fiche = listes.get((source, exercice), {}).get(siren, {})
    return next((fiche[c] for c in ("lbudg", "commune", "nom_epci", "nom_departement", "nom") if fiche.get(c)), "")


def partie_collectivites(derniers, listes):
    exercices, controles, sommes, memes, fiches, flux, teom = collectivites(derniers, listes)
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
    return (lignes + partie_fiches_dgcl(listes, fiches) + partie_flux(listes, flux) + partie_fonctions(listes)
            + partie_fiscalite(listes, teom) + partie_rei(teom))


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


def un_pour_cent(verse, recu):
    """Vrai si l'écart, non nul, atteint 1 % du plus grand des deux montants."""
    return verse != recu and abs(verse - recu) >= 0.01 * max(abs(verse), abs(recu))


def millions(x):
    return f"{fr(x / 1e6, 1)} M€"


def pour_cent(part):
    """Une part en pour cent, à une décimale ; « moins de 0,1 % » si elle s'arrondirait à zéro."""
    return f"{fr(100 * part, 1, True)} %" if round(100 * part, 1) else "moins de 0,1 %"


def partie_flux(listes, flux):
    """Les flux entre administrations : ce que l'une déclare verser à une autre contre ce que celle-ci déclare
    recevoir."""
    dgf, sdis = flux
    lignes = partie_dgf(listes, dgf) + partie_sdis(listes, sdis)
    if not lignes:
        return []
    return ["## 8. Flux entre administrations", "",
            "Ce qu'une administration déclare verser à une autre doit se retrouver dans les comptes de celle qui le "
            "reçoit. Deux flux se lisent ainsi des deux côtés : la dotation globale de fonctionnement, que l'État notifie "
            "à chaque collectivité et que celle-ci inscrit à ses comptes, et la contribution des départements aux "
            "services départementaux d'incendie et de secours (SDIS). Les comptes des communes et des groupements à "
            "fiscalité propre ne détaillent ni leurs contributions aux SDIS, ni leurs subventions aux centres d'action "
            "sociale : ces flux ne se lisent que chez qui les reçoit.", ""] + lignes


def nom_unite(listes, exercice, unite):
    """Le nom et le numéro Siren, ou le code de département, des comptes auxquels se compare une dotation."""
    jeu, cle = unite
    return f"{' et '.join(nom(listes, jeu, exercice, s) for s in sirens_dgf(listes, exercice, unite))} ({cle})"


def partie_dgf(listes, dgf):
    """La dotation globale de fonctionnement que l'État notifie contre celle qu'inscrit chaque collectivité."""
    identites, comparaisons, sans_comptes, sans_notification, sans_total = dgf
    if not comparaisons:
        return []
    annees = sorted({c[0] for c in comparaisons})
    n, faux = sum(v[0] for v in identites.values()), sum(v[1] for v in identites.values())
    egales = sum(1 for c in comparaisons if c[5])
    lignes = ["### La dotation globale de fonctionnement", "",
              "L'État notifie à chaque commune, à chaque groupement à fiscalité propre et à chaque département le montant "
              "de sa dotation globale de fonctionnement, d'après les fichiers de répartition de la DGCL ; la collectivité "
              "l'inscrit à ses comptes (agrégat « Dotation globale de fonctionnement », compte 741, tous budgets). La "
              "commune se retrouve par son code Insee de l'exercice, le groupement par son numéro Siren, le département par "
              "son code ; le Bas-Rhin et le Haut-Rhin se comparent avec la Collectivité européenne d'Alsace, que les "
              "comptes codent tous 67A. La métropole de Lyon et la Ville de Paris, que deux jeux des comptes donnent, se "
              "comparent une fois, avec les deux parts de leur dotation : de groupement et de département pour la "
              "première, de commune et de département pour la seconde. La collectivité de Corse et les collectivités "
              "territoriales uniques de Martinique et de Guyane se comparent à leurs comptes du jeu des régions, les "
              "syndicats touristiques, auxquels le jeu des groupements notifie la dotation des groupements "
              "touristiques, aux leurs du jeu des syndicats. Le dernier exercice des comptes est provisoire.", "",
              f"Dotation notifiée : pour chaque collectivité et chaque exercice, son total égale la somme de ses parts : "
              f"{fr(n, 0)} identités vérifiées, {fr(n - faux, 0)} justes, {fr(faux, 0)} en écart."
              + (" Dotations notifiées en parties seulement, sans total, qui ne se vérifient ni ne se comparent : "
                 + ", ".join(f"{nom(listes, s, e, c)} ({c}), {e}" for e, s, c in sans_total) + "." if sans_total else ""),
              ""]
    if faux:
        lignes += ["| Jeu de données | Total | Parties | En écart | Plus grand écart |", "|---|---|---|---|---|"]
        for (source, total, parties, _), (verifiees, nombre, pire) in sorted(identites.items()):
            if nombre:
                ecart, code, exercice = pire
                lignes.append(f"| {source} | {total} | {', '.join(parties)} | {fr(nombre, 0)} sur {fr(verifiees, 0)} | "
                              f"{ecart_lisible(ecart, 'euros')} : {nom(listes, source, exercice, code)} ({code}), "
                              f"{exercice} |")
        lignes.append("")
    lignes += [f"Dotation notifiée contre dotation inscrite : {fr(len(comparaisons), 0)} comparaisons de {annees[0]} à "
               f"{annees[-1]}, {fr(egales, 0)} égales à l'arrondi près, {fr(len(comparaisons) - egales, 0)} en écart, "
               f"dont {fr(sum(1 for c in comparaisons if not c[5] and un_pour_cent(c[3], c[4])), 0)} de 1 % ou plus.", "",
               "| Niveau | Exercice | Comparaisons | Égales | En écart | dont de 1 % ou plus | Notifié | Inscrit | "
               "Écart (notifié − inscrit) |", "|---|---|---|---|---|---|---|---|---|"]
    for jeu, niveau in NIVEAUX_DGF.items():
        for annee in annees:
            liste = [c for c in comparaisons if c[0] == annee and c[1][0] == jeu]
            if not liste:
                continue
            notifie, inscrit = sum(c[3] for c in liste), sum(c[4] for c in liste)
            fausses = [c for c in liste if not c[5]]
            lignes.append(f"| {niveau} | {annee} | {fr(len(liste), 0)} | {fr(len(liste) - len(fausses), 0)} | "
                          f"{fr(len(fausses), 0)} | {fr(sum(1 for c in fausses if un_pour_cent(c[3], c[4])), 0)} | "
                          f"{millions(notifie)} | {millions(inscrit)} | {ecart_lisible(notifie - inscrit, 'euros')} |")
    lignes.append("")
    fausses = sorted((c for c in comparaisons if not c[5]), key=lambda c: (-abs(c[3] - c[4]), c[0], c[1]))
    if fausses:
        lignes += [f"Les {fr(min(20, len(fausses)), 0)} plus grands écarts :", "",
                   "| Collectivité | Niveau | Exercice | Notifié | Inscrit | Écart (notifié − inscrit) |",
                   "|---|---|---|---|---|---|"]
        for exercice, unite, _, notifie, inscrit, _ in fausses[:20]:
            part = (notifie - inscrit) / max(abs(notifie), abs(inscrit))
            lignes.append(f"| {nom_unite(listes, exercice, unite)} | {NIVEAUX_DGF[unite[0]]} | {exercice} | "
                          f"{millions(notifie)} | {millions(inscrit)} | {ecart_lisible(notifie - inscrit, 'euros')} "
                          f"({pour_cent(part)}) |")
        lignes.append("")
    if sans_comptes:
        lignes += ["Dotations notifiées à des collectivités qui n'ont pas de comptes dans ces jeux, comme les communes et "
                   "les collectivités d'outre-mer hors du champ des balances comptables de la DGFiP (Saint-Pierre-et-"
                   "Miquelon, Saint-Martin, Wallis-et-Futuna, Polynésie française…) :", "",
                   "| Jeu des dotations | Exercices | Collectivités au dernier exercice | Notifié au dernier exercice | "
                   "Les plus grandes au dernier exercice |", "|---|---|---|---|---|"]
        par_jeu = collections.defaultdict(list)
        for s in sans_comptes:
            par_jeu[s[1]].append(s)
        for source, liste in sorted(par_jeu.items()):
            dernier = max(s[0] for s in liste)
            derniers = sorted((s for s in liste if s[0] == dernier), key=lambda s: (-s[3], s[2]))
            tete = ", ".join(f"{nom(listes, source, dernier, s[2])} ({s[2]})" for s in derniers[:3])
            lignes.append(f"| {source} | {plage([s[0] for s in liste])} | {fr(len(derniers), 0)} | "
                          f"{millions(sum(s[3] for s in derniers))} | {tete} |")
        lignes.append("")
    if sans_notification:
        lignes += ["Dotations inscrites aux comptes de collectivités auxquelles les fichiers de répartition ne notifient "
                   "rien :", "", "| Niveau | Exercices | Collectivités au dernier exercice | Inscrit au dernier exercice | "
                   "Les plus grandes au dernier exercice |", "|---|---|---|---|---|"]
        par_jeu = collections.defaultdict(list)
        for s in sans_notification:
            par_jeu[s[1]].append(s)
        for jeu, liste in sorted(par_jeu.items(), key=lambda e: list(NIVEAUX_DGF).index(e[0])):
            dernier = max(s[0] for s in liste)
            derniers = sorted((s for s in liste if s[0] == dernier), key=lambda s: (-abs(s[3]), s[2]))
            tete = ", ".join(f"{nom(listes, jeu, dernier, s[2])} ({s[2]})" for s in derniers[:3])
            lignes.append(f"| {NIVEAUX_DGF[jeu]} | {plage([s[0] for s in liste])} | {fr(len(derniers), 0)} | "
                          f"{millions(sum(s[3] for s in derniers))} | {tete} |")
        lignes.append("")
    return lignes


def partie_sdis(listes, sdis):
    """Les contributions des départements aux SDIS contre les participations que ceux-ci déclarent recevoir."""
    comparaisons, sans_sdis, orphelines = sdis
    if not comparaisons:
        return []
    annees = sorted({c[0] for c in comparaisons})
    egales = sum(1 for c in comparaisons if c[7])
    lignes = ["### Les contributions des départements aux SDIS", "",
              "Les départements publient leur contribution aux SDIS sous l'agrégat « Contributions aux SDIS », que les "
              "SDIS comptent parmi les participations qu'ils reçoivent. "
              "Chaque département se compare au SDIS de son territoire : sa contribution, tous budgets, contre les "
              "participations des départements que le SDIS inscrit à son budget principal. Le Bas-Rhin, le Haut-Rhin "
              "puis la Collectivité européenne d'Alsace, que le jeu des départements désigne tous par le code 67A, se "
              "comparent aux SDIS du Bas-Rhin et du Haut-Rhin ensemble, comme la collectivité de Corse, depuis 2018, à "
              "ceux de Corse-du-Sud et de Haute-Corse. Le SDIS du Rhône inscrit la contribution de la métropole de "
              "Lyon, depuis 2015, et ceux de Martinique et de Guyane celle de leur collectivité territoriale unique, "
              "depuis 2016, parmi les autres participations, puis parmi celles des groupements à fiscalité propre : "
              "la métropole se compare à ces deux rubriques, chaque collectivité territoriale unique à ces deux "
              "rubriques et aux participations des départements, que le SDIS de Martinique emploie en 2016 ; ces "
              "rubriques peuvent compter d'autres participations que la sienne. Le dernier exercice est provisoire.", "",
              f"{fr(len(comparaisons), 0)} comparaisons de {annees[0]} à {annees[-1]} : {fr(egales, 0)} égales à "
              f"l'arrondi près, {fr(len(comparaisons) - egales, 0)} en écart, dont "
              f"{fr(sum(1 for c in comparaisons if not c[7] and un_pour_cent(c[5], c[6])), 0)} de 1 % ou plus.", "",
              "| Exercice | Comparaisons | Égales | En écart | dont de 1 % ou plus | Versé | Reçu | Écart (versé − reçu) |",
              "|---|---|---|---|---|---|---|---|"]
    for annee in annees:
        liste = [c for c in comparaisons if c[0] == annee]
        verse, recu = sum(c[5] for c in liste), sum(c[6] for c in liste)
        fausses = [c for c in liste if not c[7]]
        lignes.append(f"| {annee} | {fr(len(liste), 0)} | {fr(len(liste) - len(fausses), 0)} | {fr(len(fausses), 0)} | "
                      f"{fr(sum(1 for c in fausses if un_pour_cent(c[5], c[6])), 0)} | {millions(verse)} | "
                      f"{millions(recu)} | {ecart_lisible(verse - recu, 'euros')} |")
    lignes.append("")
    regroupes = collections.defaultdict(list)  # (départements des SDIS, rubriques) → comparaisons
    for c in comparaisons:
        regroupes[(c[2], c[3])].append(c)
    en_ecart = {cle: liste for cle, liste in regroupes.items() if any(not c[7] for c in liste)}
    if en_ecart:
        lignes += ["Comparaisons en écart, territoire par territoire, sous le nom le plus récent de chacun :", "",
                   "| Collectivité | SDIS | Exercices en écart | dont de 1 % ou plus | "
                   "Plus grand écart (versé − reçu) |", "|---|---|---|---|---|"]
        for (codes, _), liste in sorted(en_ecart.items(), key=lambda e: (e[0][0], len(e[0][1]))):
            dernier = max(liste, key=lambda c: c[0])
            payeurs = " et ".join(nom(listes, s, dernier[0], siren) for s, siren in dernier[1])
            fausses = [c for c in liste if not c[7]]
            fortes = [c[0] for c in fausses if un_pour_cent(c[5], c[6])]
            pire = plus_grand(fausses, lambda c: c[5] - c[6])
            part = (pire[5] - pire[6]) / max(abs(pire[5]), abs(pire[6]))
            lignes.append(f"| {payeurs} | {dernier[4]} | {plage([c[0] for c in fausses])} | "
                          f"{plage(fortes) if fortes else 'aucun'} | {ecart_lisible(pire[5] - pire[6], 'euros')} en "
                          f"{pire[0]} ({pour_cent(part)}) |")
        lignes.append("")
    if sans_sdis:
        reconnues = [s for s in sans_sdis if s[4]]
        deps = {listes.get((s[1], s[0]), {}).get(s[2], {}).get("dep_code") for s in reconnues}
        departements = listes.get(("ofgl.base-departements-consolidee", annees[-1]), {}).values()
        muets = sorted(f"{f['lbudg']} ({f['siren']})" for f in departements if f.get("dep_code") in SANS_SDIS - deps)
        lignes += ["Contributions sans SDIS à qui les comparer. Paris et les départements de la petite couronne n'ont pas "
                   "de SDIS : la brigade de sapeurs-pompiers de Paris, unité militaire, y tient ce rôle, et ses comptes ne "
                   "figurent pas dans ces jeux" + (f" ; aucune contribution n'est publiée sous cet agrégat pour "
                                                  f"{', '.join(muets)}" if muets else "") + ".", "",
                   "| Collectivité | Exercices | Contribution au dernier exercice |", "|---|---|---|"]
        par_payeur = collections.defaultdict(list)
        for s in sans_sdis:
            par_payeur[(s[1], s[2], s[4])].append(s)
        for (source, siren, reconnue), liste in sorted(par_payeur.items(), key=lambda e: not e[0][2]):
            dernier = max(liste, key=lambda s: s[0])
            lignes.append(f"| {nom(listes, source, dernier[0], siren)} ({siren}){'' if reconnue else ', territoire non reconnu'}"
                          f" | {plage([s[0] for s in liste])} | {millions(dernier[3])} en {dernier[0]} |")
        lignes.append("")
    if orphelines:
        lignes += ["Participations des départements qu'un SDIS déclare recevoir sans que son département publie de "
                   "contribution sous cet agrégat :", "",
                   "| SDIS | Exercices | Plus grande participation |", "|---|---|---|"]
        par_sdis = collections.defaultdict(list)
        for o in orphelines:
            par_sdis[o[1]].append(o)
        for code, liste in sorted(par_sdis.items()):
            pire = max(liste, key=lambda o: abs(o[3]))
            lignes.append(f"| {max(liste, key=lambda o: o[0])[2]} | {plage([o[0] for o in liste])} | "
                          f"{millions(pire[3])} en {pire[0]} |")
        lignes.append("")
    return lignes


def nom_budget(listes, exercice, budget):
    """Le libellé d'un budget du jeu fonctionnel et son SIRET."""
    return f"{listes.get((FONCTIONNELLE, exercice), {}).get(budget, {}).get('lbudg', '')} ({budget})"


def partie_fonctions(listes):
    """Les dépenses de chaque département par fonction : budgets de chaque nomenclature, fonctions contre leurs
    sous-fonctions, identités comptables dans chaque fonction, fonctions de premier niveau contre les comptes
    consolidés, libellés des fonctions et regroupements du portail."""
    (exercices, sous_fonctions, ecarts_sous_fonctions, identites, consolides, absents, libelles,
     regroupements) = fonctions_departements(listes)
    if not exercices:
        return []
    lignes = ["## 9. Dépenses de chaque département par fonction", "",
              "La présentation fonctionnelle des comptes des départements, que l'OFGL publie sur data.ofgl.fr, ventile "
              "les dépenses de chaque budget des départements, de la métropole de Lyon et de la Ville de Paris entre "
              "les fonctions de la nomenclature de son instruction budgétaire et comptable : la M52, puis la M57, que "
              "les départements adoptent l'un après l'autre et dont les fonctions ne se correspondent pas toutes ; le "
              "jeu ne porte que sur les dépenses. Chaque montant y figure à chacun des niveaux de sa fonction, d'un à "
              "quatre chiffres, et un montant nul n'a pas de ligne : une fonction doit valoir la somme de ses "
              "sous-fonctions, et les fonctions de premier niveau réunies, le total du budget. Dans chaque fonction "
              "s'appliquent les identités comptables des agrégats de dépenses, une partie sans ligne valant zéro. La "
              "somme des fonctions de premier niveau du budget principal de chaque collectivité se compare au montant "
              "de son budget principal dans le jeu de ses comptes consolidés, celle de ses budgets annexes réunis au "
              "montant de ses budgets annexes. Le dernier exercice est provisoire.", "",
              "| Exercice | Version | Statut | Budgets principaux en M52 | Budgets principaux en M57 | "
              "Budgets annexes | Lignes |", "|---|---|---|---|---|---|---|"]
    for exercice, version, statut, budgets, nombre in exercices:
        annexes = sum(n for (_, t), n in budgets.items() if t == "BA")
        sans_fiche = sum(n for (_, t), n in budgets.items() if t == "?")
        lignes.append(f"| {exercice} | {version} | {statut} | {fr(budgets[('M52', 'BP')], 0)} | "
                      f"{fr(budgets[('M57', 'BP')], 0)} | {fr(annexes, 0)}"
                      f"{f', et {fr(sans_fiche, 0)} sans fiche' if sans_fiche else ''} | {fr(nombre, 0)} |")
    comparees, egales = sous_fonctions
    lignes += ["", f"Fonctions comparées à la somme de leurs sous-fonctions, pour chaque budget et chaque agrégat : "
               f"{fr(comparees, 0)}, dont {fr(egales, 0)} égales à l'arrondi près et {fr(comparees - egales, 0)} en "
               "écart. Un écart peut venir d'un montant que le budget classe dans la fonction sans le ventiler entre ses "
               "sous-fonctions : il se retrouve alors dans chacun des agrégats qui comptent ce montant.", ""]
    if ecarts_sous_fonctions:
        regroupes = collections.defaultdict(list)  # (nomenclature, fonction) → écarts
        for e in ecarts_sous_fonctions:
            regroupes[(e[3], e[5])].append(e)
        lignes += ["| Fonction | Exercices en écart | Budgets en écart, chaque exercice compté | "
                   "Plus grand écart (fonction − sous-fonctions) |", "|---|---|---|---|"]
        for (nomen, fonction), ecarts in sorted(regroupes.items()):
            exercice, _, budget, _, concept, _, libelle, m, somme = plus_grand(ecarts, lambda e: e[7] - e[8])
            lignes.append(f"| {fonction} de la {nomen}{f' ({libelle})' if libelle else ''} | "
                          f"{plage([e[0] for e in ecarts])} | {fr(len({(e[0], e[2]) for e in ecarts}), 0)} | "
                          f"{ecart_lisible(m - somme, 'euros')} ({concept.removeprefix('COMPTES_LOCAUX.')}) : "
                          f"{nom_budget(listes, exercice, budget)}, {exercice} |")
        lignes.append("")
    n, faux = sum(v[0] for v in identites.values()), sum(v[1] for v in identites.values())
    lignes += [f"Identités comptables dans chaque fonction de chaque budget : {fr(n, 0)} vérifiées, {fr(n - faux, 0)} "
               f"justes, {fr(faux, 0)} en écart.", "",
               "| Total | Parties | Vérifiées | En écart | Plus grand écart |", "|---|---|---|---|---|"]
    for (total, parties), (verifiees, nombre, pire) in sorted(identites.items()):
        texte = (f"{ecart_lisible(pire[0], 'euros')} : {nom_budget(listes, pire[1], pire[2])}, fonction {pire[3]}, "
                 f"{pire[1]}" if pire else "aucun")
        lignes.append(f"| {total.removeprefix('COMPTES_LOCAUX.')} | {concepts_lisibles(parties)} | {fr(verifiees, 0)} | "
                      f"{fr(nombre, 0)} | {texte} |")
    lignes.append("")
    principaux = [c for c in consolides if c[2] == "BP"]
    fausses = [c for c in principaux if not c[6]]
    lignes += [f"Fonctions de premier niveau du budget principal de chaque collectivité, réunies, contre le montant de son "
               f"budget principal dans ses comptes consolidés : {fr(len(principaux), 0)} comparaisons, "
               f"{fr(len(principaux) - len(fausses), 0)} égales à l'arrondi près, {fr(len(fausses), 0)} en écart.", ""]
    if fausses:
        lignes += ["| Collectivité | Agrégat | Exercices en écart | Plus grand écart (fonctions − comptes consolidés) |",
                   "|---|---|---|---|"]
        regroupees = collections.defaultdict(list)
        for c in fausses:
            regroupees[(c[1], c[3])].append(c)
        for (siren, concept), liste in sorted(regroupees.items()):
            pire = plus_grand(liste, lambda c: c[4] - c[5])
            lignes.append(f"| {nom(listes, DEPARTEMENTS, max(c[0] for c in liste), siren)} ({siren}) | "
                          f"{concept.removeprefix('COMPTES_LOCAUX.')} | {plage([c[0] for c in liste])} | "
                          f"{ecart_lisible(pire[4] - pire[5], 'euros')} en {pire[0]} |")
        lignes.append("")
    # Les budgets annexes : une collectivité dont un budget annexe n'est pas présenté par fonction a, dans ce jeu, moins
    # de budgets annexes que dans ses comptes consolidés.
    par_collectivite = collections.defaultdict(list)  # (exercice, siren) → comparaisons de ses budgets annexes
    for c in consolides:
        if c[2] == "BA":
            par_collectivite[(c[0], c[1])].append(c)
    if par_collectivite:
        totaux = "COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS"
        lignes += ["Budgets annexes : le jeu fonctionnel ne donne que des budgets tenus selon la M52 ou la M57, et un "
                   "budget annexe tenu selon une autre instruction n'y figure pas. Une collectivité dont tous les budgets "
                   "annexes y figurent retrouve, pour chaque agrégat, le montant de ses budgets annexes dans ses comptes "
                   "consolidés ; les autres y ont un montant moindre.", "",
                   "| Exercice | Collectivités qui ont des budgets annexes | dont budgets annexes tous présentés par "
                   "fonction | Dépenses totales hors remboursements des budgets annexes : par fonction | dans les comptes "
                   "consolidés |", "|---|---|---|---|---|"]
        for exercice in sorted({e for e, _ in par_collectivite}):
            groupes = [liste for (e, _), liste in par_collectivite.items() if e == exercice]
            completes = sum(1 for liste in groupes if all(c[6] for c in liste))
            depenses = [c for liste in groupes for c in liste if c[3] == totaux]
            lignes.append(f"| {exercice} | {fr(len(groupes), 0)} | {fr(completes, 0)} | "
                          f"{millions(sum(c[4] for c in depenses))} | {millions(sum(c[5] for c in depenses))} |")
        lignes.append("")
        au_dessus = [c for liste in par_collectivite.values() for c in liste if not c[6] and c[4] > c[5]]
        if au_dessus:
            lignes += ["Budgets annexes dont les fonctions réunies dépassent le montant des comptes consolidés, ce que "
                       "l'absence d'un budget n'explique pas, sauf pour un agrégat qu'un montant négatif réduit :", "",
                       "| Collectivité | Agrégat | Exercices | Plus grand écart (fonctions − comptes consolidés) |",
                       "|---|---|---|---|"]
            regroupees = collections.defaultdict(list)
            for c in au_dessus:
                regroupees[(c[1], c[3])].append(c)
            for (siren, concept), liste in sorted(regroupees.items()):
                pire = plus_grand(liste, lambda c: c[4] - c[5])
                lignes.append(f"| {nom(listes, DEPARTEMENTS, max(c[0] for c in liste), siren)} ({siren}) | "
                              f"{concept.removeprefix('COMPTES_LOCAUX.')} | {plage([c[0] for c in liste])} | "
                              f"{ecart_lisible(pire[4] - pire[5], 'euros')} en {pire[0]} |")
            lignes.append("")
    if absents:
        lignes += ["Collectivités qu'un seul des deux jeux donne :", "",
                   "| Collectivité | Exercices | Absente du jeu |", "|---|---|---|"]
        regroupes = collections.defaultdict(list)
        for exercice, siren, jeu in absents:
            regroupes[(siren, jeu)].append(exercice)
        for (siren, jeu), annees in sorted(regroupes.items()):
            source = FONCTIONNELLE if jeu == DEPARTEMENTS else DEPARTEMENTS
            lignes.append(f"| {nom(listes, source, max(annees), siren)} ({siren}) | {plage(annees)} | {jeu} |")
        lignes.append("")
    changeants = {cle: noms for cle, noms in libelles.items() if len(noms) > 1}
    if changeants:
        lignes += ["Fonctions dont le libellé change d'un exercice à l'autre, ou d'un budget à l'autre dans un même "
                   "exercice : une même fonction peut ne pas désigner les mêmes dépenses d'une année à l'autre.", "",
                   "| Nomenclature | Fonction | Libellés (exercices) |", "|---|---|---|"]
        for (nomen, fonction), noms in sorted(changeants.items(), key=lambda e: (e[0][0], e[0][1])):
            textes = [f"{l} ({plage(sorted(a))})" for l, a in sorted(noms.items(), key=lambda e: min(e[1]))]
            lignes.append(f"| {nomen} | {fonction} | {' ; '.join(textes)} |")
        lignes.append("")
    groupes = collections.defaultdict(list)  # regroupement → fonctions
    for (nomen, fonction), noms in sorted(regroupements.items()):
        for r in noms:
            if r != "Autres":
                groupes[r].append(f"{fonction} de la {nomen}")
    melanges = sorted(f"{fonction} de la {nomen}" for (nomen, fonction), noms in regroupements.items() if len(noms) > 1)
    if groupes:
        lignes += ["Regroupements que le portail fait, pour ses visualisations, de fonctions des deux nomenclatures, les "
                   "autres fonctions étant rangées sous « Autres » : "
                   + " ; ".join(f"« {r} » : {', '.join(fs)}" for r, fs in sorted(groupes.items()))
                   + (f". Fonctions rangées dans plusieurs regroupements : {', '.join(melanges)}." if melanges else "."),
                   ""]
    return lignes


def partie_fiscalite(listes, teom_comptes):
    """La fiscalité directe locale : communes et lignes de chaque exercice, produit contre base multipliée par le taux,
    taux net contre taux voté, taxe d'enlèvement des ordures ménagères recensée contre celle des comptes."""
    exercices, produits, taux, teom = fiscalite_locale()
    if not exercices:
        return []
    lignes = ["## 10. Fiscalité directe locale", "",
              "Le fichier de recensement des éléments d'imposition à la fiscalité directe locale (REI) de la DGFiP, que "
              "l'OFGL publie sous une forme simplifiée, donne pour le territoire de chaque commune la base, le taux et "
              "le produit des taxes foncières sur les propriétés bâties (TFPB) et non bâties (TFPNB), de la taxe "
              "d'enlèvement des ordures ménagères (TEOM) et de la cotisation foncière des entreprises (CFE), pour "
              "chacun de leurs bénéficiaires : ce sont les impositions primitives de l'année, sans les rôles "
              "supplémentaires. Le produit d'une ligne se compare à sa base multipliée par son taux net, à l'arrondi "
              "près ; la source prévient qu'il peut en différer, notamment du fait du lissage de la révision des "
              "valeurs locatives des locaux professionnels. Le taux net diffère du taux voté en cas d'intégration "
              "fiscale progressive. La TEOM recensée sur l'ensemble des communes se compare à celle qu'inscrivent les "
              "comptes consolidés des communes, des groupements à fiscalité propre et des syndicats, le REI ne disant "
              "pas lequel la perçoit. Le dernier exercice est provisoire.", "",
              "| Exercice | Version | Statut | Communes | Lignes | dont sous secret statistique |", "|---|---|---|---|---|---|"]
    for exercice, version, statut, communes, nombre, secrets in exercices:
        lignes.append(f"| {exercice} | {version} | {statut} | {fr(communes, 0)} | {fr(nombre, 0)} | {fr(secrets, 0)} |")
    comparees = sum(e[0] for e in produits.values())
    lignes += ["", f"Produit contre base multipliée par le taux net : {fr(comparees, 0)} lignes comparées, "
               f"{fr(sum(e[1] for e in produits.values()), 0)} égales à l'arrondi près, "
               f"{fr(sum(e[2] for e in produits.values()), 0)} en écart de moins de {fr(100 * SEUIL_PRODUIT, 0)} %, "
               f"{fr(sum(e[3] for e in produits.values()), 0)} au-delà.", "",
               f"| Taxe | Bénéficiaire | Lignes comparées | Égales à l'arrondi près | Écart de moins de "
               f"{fr(100 * SEUIL_PRODUIT, 0)} % | Au-delà | Plus grand écart au-delà (produit − base × taux) |",
               "|---|---|---|---|---|---|---|"]
    for (taxe, destinataire), (n, egales, faibles, fortes, pire) in sorted(produits.items()):
        texte = "aucun"
        if pire:
            ecart, calcule, exercice, commune = pire
            texte = (f"{ecart_lisible(ecart, 'euros')} ({pour_cent(ecart / calcule) if calcule else 'base nulle'}) : "
                     f"{nom(listes, FISCALE, exercice, commune)} ({commune}), {exercice}")
        lignes.append(f"| {taxe} | {destinataire} | {fr(n, 0)} | {fr(egales, 0)} | {fr(faibles, 0)} | {fr(fortes, 0)} | "
                      f"{texte} |")
    lignes.append("")
    if taux:
        lignes += ["Lignes dont le taux net diffère du taux voté : "
                   + " ; ".join(f"{taxe}, {destinataire} : {fr(n, 0)}" for (taxe, destinataire), n in sorted(taux.items()))
                   + ".", ""]
    annees = sorted(e for e in teom if any((e, s) in teom_comptes for s in COMPTES_TEOM))
    if annees:
        lignes += ["| Exercice | TEOM recensée | TEOM des comptes : communes | groupements à fiscalité propre | syndicats | "
                   "Écart (recensée − comptes) |", "|---|---|---|---|---|---|"]
        for exercice in annees:
            comptes = [teom_comptes.get((exercice, s), [0.0, 0.0])[0] for s in COMPTES_TEOM]
            ecart = teom[exercice][0] - sum(comptes)
            lignes.append(f"| {exercice} | {millions(teom[exercice][0])} | "
                          + " | ".join(millions(c) for c in comptes)
                          + f" | {ecart_lisible(ecart, 'euros')} ({pour_cent(ecart / sum(comptes)) if sum(comptes) else '—'}) |")
        lignes.append("")
    return lignes


def partie_rei(teom_comptes):
    """Le recensement des éléments d'imposition (REI) : les fichiers lus, le produit contre la base multipliée par le
    taux, la base simplifiée de l'OFGL contre le REI, le produit de chaque taxe et de chaque niveau, chaque année, et la
    TEOM recensée de chaque niveau contre celle de ses comptes."""
    annees, produits, comparaisons, par_taxe, communes_taxe, par_niveau, teom = recensement()
    if not annees:
        return []
    exercices = [i["exercice"] for i, _ in annees]
    lignes = ["## 11. Recensement des éléments d'imposition", "",
              "Le fichier de recensement des éléments d'imposition à la fiscalité directe locale (REI) de la DGFiP donne, "
              "pour le territoire de chaque commune, les bases, les taux et les produits de toutes les impositions "
              "directes locales et de leurs taxes annexes, pour chacun de leurs destinataires : collectivités, "
              "organismes (établissements publics fonciers, chambres consulaires, caisse d'assurance accidents "
              "agricoles, Société du grand projet du Sud-Ouest) et État, qui perçoit des frais sur les impositions et, en "
              "2021 et 2022, la taxe d'habitation sur les résidences principales. Ce sont les impositions du rôle "
              "général de l'année, sans les rôles supplémentaires. La base en retient les variables que décrit "
              "tables/variables_rei.csv : chacune figure au tracé de chacune de ses années, son titre y dit sa "
              "grandeur, et aucune ne donne le montant d'une collectivité répété sur chacune de ses communes, ce que "
              "l'import vérifie. Une imposition sans base ni produit n'est pas retenue.", "",
              "| Exercice | Version | Communes | Variables | Titres de l'en-tête différents du tracé | Valeurs illisibles "
              "| Lignes rétablies | Impositions retenues |", "|---|---|---|---|---|---|---|---|"]
    for inscrit, nombre in annees:
        lignes.append(f"| {inscrit['exercice']} | {inscrit['version']} | {fr(int(inscrit['communes']), 0)} | "
                      f"{fr(int(inscrit['variables']), 0)} | {fr(int(inscrit['titres_differents']), 0)} | "
                      f"{fr(int(inscrit['illisibles']), 0)} | {fr(int(inscrit['lignes_realignees']), 0)} | {fr(nombre, 0)} |")
    lignes += ["", "Les valeurs illisibles sont les marques d'une valeur manquante (« , » en 2012, « . » de 2013 à "
               "2015), et quelques textes dans une colonne numérique ; les lignes rétablies sont celles des communes de "
               "Franche-Comté en 2012, où l'export a fondu deux champs en un.", ""]
    comparees = sum(e[0] for e in produits.values())
    lignes += [f"Produit contre base multipliée par le taux net : {fr(comparees, 0)} impositions comparées, "
               f"{fr(sum(e[1] for e in produits.values()), 0)} égales à l'arrondi près, "
               f"{fr(sum(e[2] for e in produits.values()), 0)} en écart de moins de {fr(100 * SEUIL_PRODUIT, 0)} %, "
               f"{fr(sum(e[3] for e in produits.values()), 0)} au-delà. La source prévient qu'un produit peut différer "
               "de sa base multipliée par son taux, du fait du lissage de la révision des valeurs locatives des locaux "
               "professionnels, des taux moyens d'une commune où plusieurs taux s'appliquent, ou du secret statistique.",
               "", f"| Taxe | Destinataire | Impositions comparées | Égales à l'arrondi près | Écart de moins de "
               f"{fr(100 * SEUIL_PRODUIT, 0)} % | Au-delà | Plus grand écart au-delà (produit − base × taux) |",
               "|---|---|---|---|---|---|---|"]
    for (taxe, destinataire), (n, egales, faibles, fortes, pire) in sorted(produits.items()):
        texte = "aucun"
        if pire:
            ecart, calcule, exercice, commune, nom_commune = pire
            texte = (f"{ecart_lisible(ecart, 'euros')} ({pour_cent(ecart / calcule) if calcule else 'base nulle'}) : "
                     f"{nom_commune} ({commune}), {exercice}")
        lignes.append(f"| {taxe} | {destinataire} | {fr(n, 0)} | {fr(egales, 0)} | {fr(faibles, 0)} | {fr(fortes, 0)} | "
                      f"{texte} |")
    lignes.append("")
    if comparaisons:
        lignes += ["La base simplifiée de la fiscalité directe locale de l'OFGL (section 10) est tirée du REI : son "
                   "produit, pour chaque commune, chaque taxe et chaque bénéficiaire, se compare à celui des "
                   "destinataires du REI dont il vient, à l'euro près. La part intercommunale de la CFE se compare "
                   "toutes zones réunies ; l'effet du coefficient correcteur, que l'OFGL range dans la TFPB des "
                   "communes depuis 2021, n'est pas un impôt et n'a pas d'équivalent ici. Saint-Martin, collectivité "
                   "d'outre-mer, figure au REI (sous le code 97808, que forment son département et son numéro) mais "
                   "pas dans la base simplifiée. Pour les communes de la métropole de Lyon, de 2015 à 2020, le REI "
                   "range dans la part du groupement la TFPB que perçoit la métropole au titre du département, l'OFGL "
                   "dans celle du département : les deux écarts se compensent.", "",
                   "| Taxe | Bénéficiaire (OFGL) | Destinataires (REI) | Exercices | Communes comparées | Égales | "
                   "En écart | Sous secret statistique (OFGL) | Produit OFGL | Produit REI | Plus grand écart (REI − OFGL) |",
                   "|---|---|---|---|---|---|---|---|---|---|---|"]
        for taxe, beneficiaires, destinataires in COMPARAISONS_REI:
            annees_, n, egales, ecarts, secrets, o, r, pire = comparaisons[(taxe, beneficiaires)]
            if not annees_:
                continue
            texte = (f"{ecart_lisible(pire[0], 'euros')} : {pire[3]} ({pire[2]}), {pire[1]}" if pire else "aucun")
            lignes.append(f"| {taxe} | {', '.join(beneficiaires)} | {', '.join(destinataires)} | {plage(annees_)} | "
                          f"{fr(n, 0)} | {fr(egales, 0)} | {fr(ecarts, 0)} | {fr(secrets, 0)} | {millions(o)} | "
                          f"{millions(r)} | {texte} |")
        lignes.append("")
    taxes = {t["taxe"]: t["libelle"] for t in lire("tables/taxes_rei.csv")}
    lignes += ["Produit de chaque taxe, toutes parts réunies, chaque année (en millions d'euros) :", "",
               "| Taxe | " + " | ".join(exercices) + " |", "|---|" + "---|" * len(exercices)]
    for taxe in sorted({t for t, _ in par_taxe}):
        lignes.append(f"| {taxe} ({taxes[taxe]}) | "
                      + " | ".join(fr(par_taxe[(taxe, e)] / 1e6, 1) if (taxe, e) in par_taxe else "—" for e in exercices)
                      + " |")
    lignes += ["", "Communes où le REI donne un produit de chaque taxe, chaque année :", "",
               "| Taxe | " + " | ".join(exercices) + " |", "|---|" + "---|" * len(exercices)]
    for taxe in sorted({t for t, _ in par_taxe}):
        lignes.append(f"| {taxe} | " + " | ".join(fr(communes_taxe[(taxe, e)], 0) if (taxe, e) in communes_taxe else "—"
                                                  for e in exercices) + " |")
    # Une année où une taxe touche moins de la moitié des communes de l'année d'avant et de celle d'après signale un
    # fichier qui ne la donne pas partout ; la taxe sur les résidences secondaires prolonge ici la taxe d'habitation.
    suites = {"THRS": "TH"}
    familles = collections.Counter()
    for (taxe, e), n in communes_taxe.items():
        familles[(suites.get(taxe, taxe), e)] += n
    lacunes = []
    for famille in sorted({f for f, _ in familles}):
        for avant, e, apres in zip(exercices, exercices[1:], exercices[2:]):
            n = familles.get((famille, e), 0)
            if n and n < familles.get((famille, avant), 0) / 2 and n < familles.get((famille, apres), 0) / 2:
                lacunes.append(f"{famille} en {e} : {fr(n, 0)} communes, contre {fr(familles[(famille, avant)], 0)} en "
                               f"{avant} et {fr(familles[(famille, apres)], 0)} en {apres}")
    if lacunes:
        lignes += ["", "Un fichier peut ne pas donner une taxe pour toutes les communes, ses valeurs restant vides : "
                   + " ; ".join(lacunes) + " (pour la taxe d'habitation, celle sur les résidences secondaires depuis "
                   "2023). Le produit de ces années est partiel."]
    lignes += ["", "Produit de chaque niveau qui perçoit, chaque année (en millions d'euros) ; la part fixe de la TEOM est "
               "rapportée au niveau que la fiche de la commune dit la percevoir :", "",
               "| Exercice | " + " | ".join(n for n in ORDRE_NIVEAUX if any((n, e) in par_niveau for e in exercices))
               + " | Ensemble |"]
    niveaux = [n for n in ORDRE_NIVEAUX if any((n, e) in par_niveau for e in exercices)]
    lignes.append("|---|" + "---|" * (len(niveaux) + 1))
    for e in exercices:
        lignes.append(f"| {e} | " + " | ".join(fr(par_niveau.get((n, e), 0.0) / 1e6, 1) for n in niveaux)
                      + f" | {fr(sum(par_niveau.get((n, e), 0.0) for n in niveaux) / 1e6, 1)} |")
    lignes.append("")
    annees_teom = [e for e in exercices if any((e, s) in teom_comptes for _, s in NIVEAUX_COMPTES_TEOM)]
    if annees_teom:
        lignes += ["TEOM recensée de chaque niveau, part fixe et part incitative, contre celle de ses comptes consolidés ; "
                   "le REI range au niveau du groupement la TEOM que celui-ci perçoit pour le compte d'un syndicat :", "",
                   "| Exercice | " + " | ".join(f"{n} : recensée | comptes" for n, _ in NIVEAUX_COMPTES_TEOM)
                   + " | Écart d'ensemble (recensée − comptes) |", "|---|" + "---|---|" * len(NIVEAUX_COMPTES_TEOM) + "---|"]
        for e in annees_teom:
            recensee = [teom.get((n, e), 0.0) for n, _ in NIVEAUX_COMPTES_TEOM]
            comptes = [teom_comptes.get((e, s), [0.0, 0.0])[0] for _, s in NIVEAUX_COMPTES_TEOM]
            ecart = sum(recensee) - sum(comptes)
            lignes.append(f"| {e} | " + " | ".join(f"{millions(r)} | {millions(c)}" for r, c in zip(recensee, comptes))
                          + f" | {ecart_lisible(ecart, 'euros')} ({pour_cent(ecart / sum(comptes)) if sum(comptes) else '—'}) |")
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


# Ce que la base couvre des unités publiques : les décomptes officiels contre les unités dont elle a les comptes un à
# un, que donnent les listes des jeux de l'OFGL (leurs numéros Siren distincts, le jeu des SDIS et celui des centres
# d'action sociale étant publiés budget par budget). Chaque catégorie de la DGCL se compare aux unités de l'exercice
# qui y correspondent : (catégorie, périmètre, [(jeu, fiches retenues)], unités retenues).
UNITES_DGCL, UNITES_ODAL = "dgcl.collectivites-locales-en-chiffres", "insee.liste-odal"
NOMBRE_1ER_JANVIER, NOMBRE_DANS_LE_CHAMP = "UNITES_PUBLIQUES.NOMBRE_1ER_JANVIER", "UNITES_PUBLIQUES.NOMBRE_DANS_LE_CHAMP"
CCAS, EPL = "ofgl.base-ccas-cias", "ofgl.base-epl-consolidee"
MDPH_SYNDICATS, MDPH_EPL = "Maison départementale des personnes handicapées (MDPH)", "GIP - MDPH"
COUVERTURE_DGCL = [
    ("Communes", "COMMUNES", [(COMMUNES, lambda f: True)], "le jeu des communes, Ville de Paris comprise"),
    ("Départements", "CONSEILS_DEPARTEMENTAUX", [(DEPARTEMENTS, lambda f: f.get("categ") == "DEPT")],
     "la catégorie « DEPT » du jeu des départements, qui comprend le Département de Mayotte"),
    ("Régions", "CONSEILS_REGIONAUX", [(REGIONS, lambda f: f.get("categ") == "REG")],
     "la catégorie « REG » du jeu des régions"),
    ("Collectivités à statut particulier", "COLLECTIVITES_STATUT_PARTICULIER",
     [(REGIONS, lambda f: f.get("categ") == "CTU"), (GFP, lambda f: f.get("categ") == "ML")],
     "les collectivités territoriales uniques du jeu des régions (Corse, Martinique, Guyane) et la métropole de Lyon ; "
     "le Département de Mayotte est compté avec les départements"),
    ("Groupements à fiscalité propre", "GFP", [(GFP, lambda f: f.get("categ") == "GFP")],
     "la catégorie « GFP » du jeu des groupements, sans la métropole de Lyon ni les établissements publics territoriaux"),
    ("Syndicats", "SYNDICATS", [(SYNDICATS, lambda f: f.get("categorie_synd") != MDPH_SYNDICATS),
                                (GFP, lambda f: f.get("categ") == "EPT")],
     "le jeu des syndicats sans les maisons départementales des personnes handicapées, et les établissements publics "
     "territoriaux du jeu des groupements, que la DGCL compte parmi les syndicats")]
COUVERTURE_ODAL = {
    "ODAL_SDIS": ([(SDIS, lambda f: True)], "le jeu des SDIS"),
    "ODAL_CCAS": ([(CCAS, lambda f: True)], "le jeu des centres d'action sociale : centres communaux et intercommunaux, et "
                                            "celui de la Ville de Paris"),
    "ODAL_MDPH": ([(SYNDICATS, lambda f: f.get("categorie_synd") == MDPH_SYNDICATS),
                   (EPL, lambda f: f.get("categorie_epl_abr") == MDPH_EPL)],
                  "les maisons départementales des personnes handicapées des jeux des syndicats et des établissements "
                  "publics locaux")}
EPL_HORS_MDPH = [(EPL, lambda f: f.get("categorie_epl_abr") != MDPH_EPL)]
# Les périmètres des autres normes qui décrivent un sous-secteur sans être rangés sous lui : l'État des lois de finances et
# de ses comptes annuels, les ensembles des lois de financement de la sécurité sociale.
AUTRES_PERIMETRES = {"S13111": ("ETAT_LF", "ETAT_CGE"), "S1314": ("ROBSS", "ROBSS_FSV", "SECU_LFSS")}


def sirens(listes, exercice, jeux):
    """Les numéros Siren distincts des fiches retenues de jeux de l'OFGL pour un exercice ; None s'il manque un jeu."""
    retenus = set()
    for jeu, retenue in jeux:
        if (jeu, exercice) not in listes:
            return None
        retenus |= {f["siren"] for f in listes[(jeu, exercice)].values() if retenue(f)}
    return retenus


def nombre_officiel(derniers, source, concept, perimetre, periode):
    ligne = derniers.get((source, "FR", perimetre, concept, "", "", "NOMBRE", periode))
    return round(float(ligne["valeur"])) if ligne else None


def officiel_contre_base(officiel, base):
    """« 34 935 / 34 932 (−3) » : le décompte officiel, les unités de la base, et leur écart s'il y en a un."""
    texte = f"{'—' if officiel is None else fr(officiel, 0)} / {'—' if base is None else fr(len(base), 0)}"
    return texte + (f" ({fr(len(base) - officiel, 0, True)})" if None not in (officiel, base) and len(base) != officiel
                    else "")


def noms_compacts(noms):
    """Des noms de sources d'un producteur : « bdm-dette-trim-apu, t3101 à t3105, t3203 » ; au-delà de quinze, leur nombre,
    le premier et le dernier."""
    noms = sorted(noms)
    if len(noms) > 15:
        return f"{len(noms)} sources ({noms[0]} … {noms[-1]})"
    suites, autres = [], [n for n in noms if not re.fullmatch(r"t[0-9]{4}", n)]
    for n in sorted(int(n[1:]) for n in noms if re.fullmatch(r"t[0-9]{4}", n)):
        if suites and n == suites[-1][-1] + 1:
            suites[-1].append(n)
        else:
            suites.append([n])
    return ", ".join(autres + [f"t{s[0]} à t{s[-1]}" if len(s) >= 3 else ", ".join(f"t{n}" for n in s) for s in suites])


def sources_du_sous_secteur(derniers, perimetre, autres=()):
    """Les sources dont des chiffres portent sur le sous-secteur, sur un périmètre qu'il contient ou sur l'un des
    `autres`, hors décomptes d'unités, groupées par producteur : « insee : t3204, t7304 ; senat : 22 sources (pjl06-051 …
    tas22-018) »."""
    parents = {p["id"]: p["parent_id"] for p in lire("tables/perimetres.csv")}

    def dedans(p):
        while p:
            if p == perimetre or p in autres:
                return True
            p = parents.get(p)
        return False

    par_producteur = collections.defaultdict(set)
    for k in derniers:
        if not k[3].startswith("UNITES_PUBLIQUES.") and dedans(k[2]):
            producteur, nom = k[0].split(".", 1)
            par_producteur[producteur].add(nom)
    return " ; ".join(f"{p} : {noms_compacts(n)}" for p, n in sorted(par_producteur.items()))


def partie_organismes(derniers, listes):
    inscrits = lire("tables/organismes.csv")
    annees_dgcl = sorted({k[7] for k in derniers if k[0] == UNITES_DGCL and k[3] == NOMBRE_1ER_JANVIER})
    annees_odal = sorted({k[7] for k in derniers if k[0] == UNITES_ODAL and k[3] == NOMBRE_DANS_LE_CHAMP})
    if not (inscrits or annees_dgcl or annees_odal):
        return []
    par_liste = collections.defaultdict(list)
    for o in inscrits:
        par_liste[(o["annee"], o["fichier_id"])].append(o)
    (annee_odac, _), odac = max(par_liste.items()) if par_liste else ((None, None), [])
    annee = annee_odac or max(annees_odal or annees_dgcl)
    libelles = {p["id"]: p["libelle"] for p in lire("tables/perimetres.csv")}
    jeux_dgcl = [j for _, _, jeux, _ in COUVERTURE_DGCL for j in jeux]
    jeux_odal = [j for jeux, _ in COUVERTURE_ODAL.values() for j in jeux] + EPL_HORS_MDPH
    lignes = ["## 12. Organismes publics : ce que la base couvre", "",
              "Le secteur des administrations publiques, unité par unité, d'après les listes et décomptes officiels : la "
              "liste des organismes divers d'administration centrale (ODAC) et le nombre d'organismes divers "
              "d'administration locale (ODAL) par catégorie, que l'Insee établit pour les comptes nationaux, le nombre de "
              "collectivités territoriales et de groupements au 1er janvier que publie la DGCL. Ils se comparent aux "
              "unités dont la base a les comptes une à une, d'après les listes des jeux de l'OFGL (numéros Siren "
              "distincts). Un écart n'est pas une erreur : un décompte à une date et la liste des comptes d'un exercice "
              "ne retiennent pas toujours les mêmes unités.", "",
              f"### Les sous-secteurs en {annee}", "",
              "| Sous-secteur | Unités selon les décomptes officiels | Unités dont la base a les comptes, une à une | "
              "Sources de la base sur le sous-secteur ou ses parties |", "|---|---|---|---|"]
    collectivites = nombre_officiel(derniers, UNITES_DGCL, NOMBRE_1ER_JANVIER, "COLLECTIVITES_ET_GROUPEMENTS", annee)
    odal = nombre_officiel(derniers, UNITES_ODAL, NOMBRE_DANS_LE_CHAMP, "S13132", annee)
    base_collectivites, base_odal = sirens(listes, annee, jeux_dgcl), sirens(listes, annee, jeux_odal)
    selon_ofgl = f"jeux de l'OFGL, exercice {annee}"
    sous_secteurs = [
        ("État (S13111)", "S13111", "l'État",
         "l'État, d'après son budget voté (lois de finances initiales), son budget exécuté et ses comptes annuels (lois "
         "de règlement et de résultats)"),
        ("Organismes divers d'administration centrale (S13112)", "S13112",
         f"{fr(len(odac), 0)} (liste des ODAC, {annee_odac})" if odac else "—", "aucun"),
        ("Collectivités locales (S13131)", "S13131",
         "—" if collectivites is None else f"{fr(collectivites, 0)} au 1er janvier (DGCL)",
         "—" if base_collectivites is None else f"{fr(len(base_collectivites), 0)} ({selon_ofgl})"),
        ("Organismes divers d'administration locale (S13132)", "S13132",
         "—" if odal is None else f"{fr(odal, 0)} (liste des ODAL)",
         "—" if base_odal is None else f"{fr(len(base_odal), 0)} : SDIS, centres d'action sociale, établissements "
                                       f"publics locaux ({selon_ofgl})"),
        ("Administrations de sécurité sociale (S1314)", "S1314",
         "pas de liste dans la documentation des comptes nationaux de l'Insee",
         "aucune ; leurs ensembles d'après les lois de financement : régime général, régimes obligatoires de base, FSV, "
         "CADES, FRR")]
    lignes += [f"| {nom} | {officiel} | {base} | "
               f"{sources_du_sous_secteur(derniers, perimetre, AUTRES_PERIMETRES.get(perimetre, ()))} |"
               for nom, perimetre, officiel, base in sous_secteurs] + [""]
    annees = [a for a in annees_dgcl if sirens(listes, a, jeux_dgcl) is not None]
    if annees:
        lignes += ["### Collectivités territoriales et groupements", "",
                   "Pour chaque catégorie, le nombre que la DGCL décompte au 1er janvier (tableaux 2.2 et 2.5a de « Les "
                   "collectivités locales en chiffres »), puis le nombre d'unités dont la base a les comptes de "
                   "l'exercice, et leur écart.", "",
                   "| Catégorie | " + " | ".join(annees) + " |", "|---|" + "---|" * len(annees)]
        for libelle, perimetre, jeux, _ in COUVERTURE_DGCL + [("Ensemble", "COLLECTIVITES_ET_GROUPEMENTS", jeux_dgcl, "")]:
            lignes.append(f"| {libelle} | " + " | ".join(officiel_contre_base(
                nombre_officiel(derniers, UNITES_DGCL, NOMBRE_1ER_JANVIER, perimetre, a), sirens(listes, a, jeux))
                for a in annees) + " |")
        lignes += ["", "Unités retenues dans la base :", ""]
        lignes += [f"- {libelle} : {retenues}." for libelle, _, _, retenues in COUVERTURE_DGCL] + [""]
    if annees_odal:
        a = max(annees_odal)
        lignes += [f"### Organismes divers d'administration locale en {a}", "",
                   "Pour chaque catégorie de la liste de l'Insee, le nombre de ses organismes, puis celui des unités dont "
                   f"la base a les comptes de l'exercice {a}, pour les catégories que publie un jeu de l'OFGL.", "",
                   "| Catégorie | Organismes (Insee) | Dans la base |", "|---|---|---|"]
        for perimetre in list(organismes.CATEGORIES_ODAL.values()) + ["S13132"]:
            jeux = COUVERTURE_ODAL.get(perimetre, ([],))[0] if perimetre != "S13132" else jeux_odal
            base = sirens(listes, a, jeux) if jeux else None
            libelle = "Ensemble" if perimetre == "S13132" else libelles.get(perimetre, perimetre)
            officiel = nombre_officiel(derniers, UNITES_ODAL, NOMBRE_DANS_LE_CHAMP, perimetre, a)
            lignes.append(f"| {libelle} | {'—' if officiel is None else fr(officiel, 0)} | "
                          f"{'—' if base is None else fr(len(base), 0)} |")
            if perimetre == list(organismes.CATEGORIES_ODAL.values())[-1]:
                epl = sirens(listes, a, EPL_HORS_MDPH)
                lignes.append(f"| Établissements publics locaux (jeu de l'OFGL), hors MDPH | — | "
                              f"{'—' if epl is None else fr(len(epl), 0)} |")
        activites = collections.Counter(f.get("libelle_cacti_simplifie") or "non dite" for f in listes.get((EPL, a), {}).values()
                                        if f.get("categorie_epl_abr") != MDPH_EPL)
        lignes += ["", "Unités retenues dans la base :", ""]
        lignes += [f"- {libelles.get(p, p)} : {retenues}." for p, (_, retenues) in COUVERTURE_ODAL.items()]
        if activites:
            premieres, autres = activites.most_common()[:6], activites.most_common()[6:]
            lignes.append("- Établissements publics locaux : établissements publics administratifs, régies personnalisées "
                          "et groupements d'intérêt public, que l'Insee range dans plusieurs de ses catégories ; par "
                          "activité : " + ", ".join(f"{n.lower()} {fr(c, 0)}" for n, c in premieres)
                          + (f", et {fr(sum(c for _, c in autres), 0)} dans {len(autres)} autres activités" if autres else "")
                          + ".")
        lignes.append("")
    if odac:
        fonctions = {f["id"]: f["libelle"] for f in lire("tables/fonctions.csv")}
        par_fonction = collections.Counter(o["fonction_id"] for o in odac)
        lignes += [f"### Organismes divers d'administration centrale en {annee_odac}", "",
                   f"La liste de l'Insee, que la table des organismes reprend organisme par organisme : "
                   f"{fr(len(odac), 0)} organismes, par fonction (premier niveau de la COFOG). La base n'a les comptes "
                   "d'aucun d'eux un à un.", "", "| Fonction | Organismes |", "|---|---|"]
        lignes += [f"| {f} {fonctions.get(f, '')} | {fr(n, 0)} |" for f, n in sorted(par_fonction.items())]
        lignes += [f"| Ensemble | {fr(len(odac), 0)} |", ""]
    return lignes


# --- Comptes individuels de la DGFiP -------------------------------------------------------------------------------

def _ci(composante):
    """« -CHARGES_FONCTIONNEMENT » → « -COMPTES_INDIVIDUELS.CHARGES_FONCTIONNEMENT »."""
    signe = composante[0] if composante[0] in "-?!" else ""
    return signe + "COMPTES_INDIVIDUELS." + composante.lstrip("-?!")


# Identités que les maquettes des comptes individuels énoncent dans leurs libellés (« Résultat comptable = A - B = R »,
# « Résultat d'ensemble = R - E »…) : jusqu'en 2024, le besoin de financement de la section d'investissement (E) est le
# besoin résiduel (D − C) plus le solde des opérations pour compte de tiers ; la maquette de 2025, qui ne donne plus le
# besoin résiduel, le dit égal à D − C (« ! » : cette identité-là ne s'applique pas quand le besoin résiduel est
# publié). La capacité d'autofinancement nette l'est « du remboursement en capital des emprunts ».
IDENTITES_INDIVIDUELLES = [(_ci(t), [_ci(c) for c in cs]) for t, cs in [
    ("RESULTAT_COMPTABLE", ["PRODUITS_FONCTIONNEMENT", "-CHARGES_FONCTIONNEMENT"]),
    ("BESOIN_FINANCEMENT_RESIDUEL", ["EMPLOIS_INVESTISSEMENT", "-RESSOURCES_INVESTISSEMENT"]),
    ("BESOIN_FINANCEMENT_INVESTISSEMENT", ["BESOIN_FINANCEMENT_RESIDUEL", "SOLDE_OPERATIONS_TIERS"]),
    ("BESOIN_FINANCEMENT_INVESTISSEMENT", ["EMPLOIS_INVESTISSEMENT", "-RESSOURCES_INVESTISSEMENT",
                                           "!BESOIN_FINANCEMENT_RESIDUEL"]),
    ("RESULTAT_ENSEMBLE", ["RESULTAT_COMPTABLE", "-BESOIN_FINANCEMENT_INVESTISSEMENT"]),
    ("CAF_NETTE", ["CAF", "-REMBOURSEMENTS_EMPRUNTS_DETTES"])]]
NIVEAUX_INDIVIDUELS = {individuels.COMMUNES: "communes", individuels.GFP: "groupements à fiscalité propre",
                       individuels.DEPARTEMENTS: "départements et collectivités territoriales uniques",
                       individuels.REGIONS: "régions"}
# Les comptes de l'OFGL auxquels se comparent ceux de chaque niveau : son jeu, et son montant, celui du budget principal
# (0), ou, pour les groupements, que la DGFiP donne budgets annexes compris, le montant consolidé (3). Les collectivités
# territoriales uniques, que les comptes individuels rangent parmi les départements, sont dans le jeu des régions de
# l'OFGL.
RAPPROCHEMENTS_OFGL = {individuels.COMMUNES: ("ofgl.base-communes-consolidee", 0),
                       individuels.GFP: ("ofgl.base-gfp-consolidee", 3),
                       individuels.DEPARTEMENTS: ("ofgl.base-departements-consolidee", 0),
                       individuels.REGIONS: ("ofgl.base-regions-consolidee", 0)}
# Les codes de département et de région de la DGFiP outre-mer, et ceux de l'Insee et de l'OFGL ; les codes de région
# des collectivités territoriales uniques de Guyane, de Martinique et de Corse (« 02A » depuis 2018), à défaut d'un
# département de même code.
OUTRE_MER_INSEE = {"101": ("971", "01"), "102": ("973", "03"), "103": ("972", "02"), "104": ("974", "04"),
                   "106": ("976", "06")}
CTU_INDIVIDUELLES = {"102": "03", "103": "02", "02A": "94"}
# Agrégats de même intitulé, ou de même objet, des deux publications : (concept des comptes individuels, concept des
# comptes locaux). Elles sont établies d'après les mêmes comptes de gestion ; l'OFGL définit ses agrégats compte par
# compte, en opérations réelles et hors gestion active de la dette (définitions de la DGCL), quand la maquette de la
# DGFiP ne dit pas les siens.
PAIRES_OFGL = [(_ci(i), "COMPTES_LOCAUX." + o) for i, o in [
    ("CHARGES_PERSONNEL", "FRAIS_PERSONNEL"), ("ACHATS_CHARGES_EXTERNES", "ACHATS_CHARGES_EXTERNES"),
    ("CHARGES_FINANCIERES", "CHARGES_FINANCIERES"), ("DGF", "DGF"), ("PRODUITS_SERVICES_DOMAINE", "VENTES_BIENS_SERVICES"),
    ("FCTVA", "FCTVA"), ("IMPOTS_LOCAUX", "IMPOTS_LOCAUX"), ("AUTRES_IMPOTS_TAXES", "AUTRES_IMPOTS_TAXES"),
    ("FISCALITE_REVERSEE", "FISCALITE_REVERSEE"), ("TICPE", "TICPE"), ("CVAE", "CVAE"),
    ("PRODUITS_FONCTIONNEMENT_CAF", "REC_FONCTIONNEMENT"), ("CHARGES_FONCTIONNEMENT_CAF", "DEP_FONCTIONNEMENT"),
    ("EXCEDENT_BRUT_FONCTIONNEMENT", "EPARGNE_GESTION_COURANTE"), ("CAF", "EPARGNE_BRUTE"), ("CAF_NETTE", "EPARGNE_NETTE"),
    ("DEPENSES_EQUIPEMENT", "DEPENSES_EQUIPEMENT"), ("SUBVENTIONS_EQUIPEMENT_VERSEES", "SUBVENTIONS_EQUIPEMENT_VERSEES"),
    ("EMPRUNTS_DETTES_ASSIMILEES", "EMPRUNTS"), ("REMBOURSEMENTS_EMPRUNTS_DETTES", "REMBOURSEMENTS_DETTE"),
    ("ANNUITE_DETTE", "ANNUITE_DETTE_CHARGES_FINANCIERES"), ("ENCOURS_DETTE", "DETTE"),
    ("ENCOURS_DETTES_BANCAIRES", "DETTE_BANCAIRE"), ("FONDS_ROULEMENT", "FONDS_ROULEMENT")]]


def formule(total, parties):
    """Les parties d'une identité des comptes individuels, avec leurs signes : « PRODUITS_FONCTIONNEMENT −
    CHARGES_FONCTIONNEMENT »."""
    for t, composantes in IDENTITES_INDIVIDUELLES:
        signes = [("−" if c.startswith("-") else "+", c.lstrip("-?")) for c in composantes if not c.startswith("!")]
        if t == total and tuple(c for _, c in signes) == parties:
            texte = " ".join(f"{s} {c.removeprefix('COMPTES_INDIVIDUELS.')}" for s, c in signes)
            return texte[2:] if texte.startswith("+ ") else texte
    return " + ".join(parties)


def comptes_individuels_retenus():
    """{(source, exercice): inscription} : la copie de comptes la plus récente de chaque exercice de chaque niveau."""
    retenus = {}
    for i in lire("tables/fichiers_comptes_individuels.csv"):
        cle = (i["source_id"], i["exercice"])
        if i["contenu"] == "comptes" and (cle not in retenus or i["version"] > retenus[cle]["version"]):
            retenus[cle] = i
    return retenus


def uniques(fiches, champ, filtre=lambda f: True):
    """{code: siren} des collectivités d'une liste de l'OFGL, pour les codes qu'une seule porte."""
    par_code = collections.defaultdict(list)
    for siren, f in fiches.items():
        if filtre(f):
            par_code[f.get(champ, "")].append(siren)
    return {code: s[0] for code, s in par_code.items() if len(s) == 1}


def rapprochement(listes, source, exercice):
    """{collectivité des comptes individuels: (jeu de l'OFGL, siren)} pour un niveau et un exercice : une commune par son
    code Insee, un groupement par son numéro Siren, un département par son code (« 001 » → « 01 », « 101 » → « 971 »),
    ou, à défaut, une collectivité territoriale unique par son code de région, une région par le sien (« 011 » → « 11 »).
    Un code que l'OFGL donne à plusieurs collectivités ne se rapproche pas (« 67A », au Bas-Rhin et au Haut-Rhin jusqu'en
    2020)."""
    jeu = RAPPROCHEMENTS_OFGL[source][0]
    fiches = listes.get((jeu, exercice))
    if fiches is None:
        return None
    if source == individuels.COMMUNES:
        return {code: (jeu, s) for code, s in uniques(fiches, "insee").items()}
    if source == individuels.GFP:
        return {s: (jeu, s) for s in fiches}
    regions = listes.get((RAPPROCHEMENTS_OFGL[individuels.REGIONS][0], exercice), {})
    if source == individuels.REGIONS:
        par_region = uniques(regions, "reg_code")
        return lambda code: ((jeu, par_region[r]) if (r := OUTRE_MER_INSEE[code][1] if code in OUTRE_MER_INSEE
                                                      else code[1:]) in par_region else None)
    par_departement = uniques(fiches, "dep_code")
    ctu = uniques(regions, "reg_code", lambda f: f.get("categ") == "CTU")

    def correspondant(code):
        d = OUTRE_MER_INSEE[code][0] if code in OUTRE_MER_INSEE else code[1:]
        if d in par_departement:
            return jeu, par_departement[d]
        if CTU_INDIVIDUELLES.get(code) in ctu:
            return RAPPROCHEMENTS_OFGL[individuels.REGIONS][0], ctu[CTU_INDIVIDUELLES[code]]
        return None
    return correspondant


def montants_ofgl(fichiers, agregats, retenus, jeu, exercice, k, concepts):
    """{siren: {concept: (montant, marge)}} d'un exercice d'un jeu de l'OFGL, pour les concepts demandés et le montant
    de rang `k`, et les concepts que le jeu publie cet exercice ; rien si le jeu n'a pas l'exercice."""
    inscrit = retenus.get((jeu, exercice))
    if inscrit is None:
        return None, set()
    par_siren, publies = collections.defaultdict(dict), set()
    for siren, agregat, *m in ofgl.montants(fichiers[inscrit["fichier_id"]], agregats, marges=True):
        concept = agregats[agregat]["concept_id"]
        if concept in concepts:
            par_siren[siren][concept] = (m[k], m[4 + k])
            publies.add(concept)
    return par_siren, publies


def comptes_individuels_controles(listes):
    """Pour chaque niveau des comptes individuels et chaque exercice, dans sa version la plus récente : le nombre de
    collectivités, de valeurs lues et absentes ; les identités de la maquette, collectivité par collectivité ; et,
    chaque exercice que publie aussi l'OFGL, chaque collectivité rapprochée de la sienne, agrégat par agrégat."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/variables_comptes_individuels.csv")
    agregats = {a["agregat"]: a for a in lire("tables/agregats_ofgl.csv")}
    retenus_ofgl = montants_retenus()
    exercices = []  # (source, exercice, collectivités, valeurs lues, valeurs absentes)
    identites = collections.defaultdict(lambda: [0, 0, None])  # (source, total, parties, budget) → [vérifiées, en écart, pire]
    annees_en_ecart = collections.defaultdict(set)  # (source, total, parties, budget) → exercices où l'identité est en écart
    # (source, exercice) → (collectivités, rapprochées, collectivités de l'OFGL qu'aucune ne rejoint)
    rapprochees = {}
    # (source, concept de la DGFiP, concept de l'OFGL) → [comparés, égaux, plus grand écart (écart, collectivité, exercice), exercices]
    comparaisons = collections.defaultdict(lambda: [0, 0, None, set()])
    noms = {}  # (source, exercice, collectivité) → nom, pour les collectivités citées
    concepts_ofgl = {o for _, o in PAIRES_OFGL}
    for (source, exercice), inscrit in sorted(comptes_individuels_retenus().items()):
        _, lues, absentes, decimales = individuels.comptes(fichiers[inscrit["fichier_id"]], referentiel)
        variables = individuels.retenues(source, exercice, referentiel)
        montants_par_variable = {v: l["concept_id"] for v, l in variables.items() if l["grandeur"] == "montant"}
        if len(set(montants_par_variable.values())) != len(montants_par_variable):
            raise SystemExit(f"{source}, {exercice} : deux montants de même concept")
        exercices.append((source, exercice, len(lues), sum(len(v) for _, _, v in lues), absentes))
        correspondant = rapprochement(listes, source, exercice)
        ofgl_par_jeu = {}
        if correspondant is not None:
            k = RAPPROCHEMENTS_OFGL[source][1]
            jeux = {RAPPROCHEMENTS_OFGL[source][0]} | ({RAPPROCHEMENTS_OFGL[individuels.REGIONS][0]}
                                                       if source == individuels.DEPARTEMENTS else set())
            ofgl_par_jeu = {j: montants_ofgl(fichiers, agregats, retenus_ofgl, j, exercice, k, concepts_ofgl) for j in jeux}
        trouves = set()
        avant = {cle: v[1] for cle, v in identites.items() if cle[0] == source}
        for code, fiche, valeurs in lues:
            montants = {montants_par_variable[v]: (m, 0.5 * 10 ** -decimales[v]) for v, m in valeurs.items()
                        if v in montants_par_variable}
            identites_comptables(identites, IDENTITES_INDIVIDUELLES, source, exercice, code, montants,
                                 [("budget principal", 0, 1)])
            if correspondant is None:
                continue
            cible = correspondant(code) if callable(correspondant) else correspondant.get(code)
            if cible is None:
                continue
            jeu, siren = cible
            trouves.add(cible)
            par_siren, publies = ofgl_par_jeu.get(jeu, (None, set()))
            if par_siren is None:
                continue
            for concept_dgfip, concept_ofgl in PAIRES_OFGL:
                if concept_dgfip not in montants or concept_ofgl not in publies:
                    continue
                v, m = montants[concept_dgfip]
                o, mo = par_siren.get(siren, {}).get(concept_ofgl, (0.0, 0.0))
                ecart = 1000 * v - o
                entree = comparaisons[(source, concept_dgfip, concept_ofgl)]
                entree[0] += 1
                entree[3].add(exercice)
                if depasse(ecart, 1000 * m + mo):
                    if entree[2] is None or abs(ecart) > abs(entree[2][0]):
                        entree[2] = (ecart, code, exercice)
                else:
                    entree[1] += 1
        for cle, v in identites.items():
            if cle[0] == source and v[1] > avant.get(cle, 0):
                annees_en_ecart[cle].add(exercice)
        # Le nom des collectivités que citent les plus grands écarts de cet exercice.
        cites = {e[2][1] for cle, e in itertools.chain(identites.items(), comparaisons.items())
                 if cle[0] == source and e[2] is not None and e[2][2] == exercice}
        noms.update({(source, exercice, code): fiche.get("inom") or fiche.get("lbudg") or ""
                     for code, fiche, _ in lues if code in cites})
        if correspondant is not None:
            jeu = RAPPROCHEMENTS_OFGL[source][0]
            sans = {(jeu, s) for s in listes.get((jeu, exercice), {})} - trouves
            if source == individuels.REGIONS:
                sans = {(j, s) for j, s in sans if listes[(j, exercice)][s].get("categ") != "CTU"}
            if source == individuels.DEPARTEMENTS:
                sans = {(j, s) for j, s in sans if listes[(j, exercice)][s].get("categ") == "DEPT"}
            rapprochees[(source, exercice)] = (len(lues), len(trouves), len(sans))
    return exercices, identites, annees_en_ecart, rapprochees, comparaisons, noms


def partie_comptes_individuels(listes):
    exercices, identites, annees_en_ecart, rapprochees, comparaisons, noms = comptes_individuels_controles(listes)
    if not exercices:
        return []
    lignes = ["## 13. Comptes individuels de la DGFiP", "",
              "Les comptes individuels que la DGFiP publie pour chaque commune depuis 2000, chaque groupement à fiscalité "
              "propre depuis 2007, chaque département et chaque région depuis 2008 : l'analyse des équilibres financiers "
              "fondamentaux du budget principal (budgets annexes compris pour les groupements) et les éléments de la "
              "fiscalité directe locale, en milliers d'euros, dans la version la plus récente de chaque exercice. Une "
              "valeur est exacte à la demi-unité de la dernière décimale que sa variable publie dans l'exercice.", "",
              "| Niveau | Exercices | Collectivités au dernier exercice | Collectivités-exercices | Valeurs lues | "
              "Valeurs absentes |", "|---|---|---|---|---|---|"]
    par_source = collections.defaultdict(list)
    for e in exercices:
        par_source[e[0]].append(e)
    for source, liste in sorted(par_source.items(), key=lambda e: list(NIVEAUX_INDIVIDUELS).index(e[0])):
        dernier = max(liste, key=lambda e: e[1])
        lignes.append(f"| {NIVEAUX_INDIVIDUELS[source]} | {plage([e[1] for e in liste])} | {fr(dernier[2], 0)} | "
                      f"{fr(sum(e[2] for e in liste), 0)} | {fr(sum(e[3] for e in liste), 0)} | "
                      f"{fr(sum(e[4] for e in liste), 0)} |")
    n, faux = sum(v[0] for v in identites.values()), sum(v[1] for v in identites.values())
    lignes += ["", "Identités que les maquettes énoncent, de chaque collectivité : le résultat comptable (R) est la "
               "différence des produits (A) et des charges (B) de fonctionnement ; le besoin de financement de la section "
               "d'investissement (E), jusqu'en 2024, le besoin résiduel (D − C, emplois moins ressources) plus le solde "
               "des opérations pour compte de tiers, et en 2025 D − C ; le résultat d'ensemble, R − E ; la capacité "
               "d'autofinancement nette, la capacité d'autofinancement moins le remboursement des emprunts et dettes "
               f"assimilées. {fr(n, 0)} vérifiées, {fr(n - faux, 0)} justes, {fr(faux, 0)} en écart.", ""]
    lignes += ["| Niveau | Total | Parties | Vérifiées | En écart | Exercices en écart | Plus grand écart |",
               "|---|---|---|---|---|---|---|"]
    rangs = {(t, tuple(c.lstrip("-?") for c in cs if not c.startswith("!"))): i
             for i, (t, cs) in enumerate(IDENTITES_INDIVIDUELLES)}
    for (source, total, parties, _), (verifiees, nombre, pire) in sorted(
            identites.items(), key=lambda e: (list(NIVEAUX_INDIVIDUELS).index(e[0][0]), rangs[e[0][1:3]])):
        texte = "aucun" if pire is None else (f"{fr(pire[0], 2, True)} k€ : {noms.get((source, pire[2], pire[1]), '')} "
                                              f"({pire[1]}), {pire[2]}")
        annees = annees_en_ecart.get((source, total, parties, _))
        lignes.append(f"| {NIVEAUX_INDIVIDUELS[source]} | {total.removeprefix('COMPTES_INDIVIDUELS.')} | "
                      f"{formule(total, parties)} | {fr(verifiees, 0)} | "
                      f"{fr(nombre, 0)} | {plage(sorted(annees)) if annees else 'aucun'} | {texte} |")
    lignes.append("")
    if rapprochees:
        lignes += ["### Les mêmes collectivités dans les comptes de l'OFGL", "",
                   "Chaque exercice que publient aussi les jeux de l'OFGL (section 7), chaque collectivité rapprochée de "
                   "la sienne : une commune par son code Insee, un groupement par son numéro Siren, un département ou une "
                   "région par son code, une collectivité territoriale unique, que l'OFGL range parmi les régions, par son "
                   "code de région. Le budget principal, ou, pour les groupements, le montant consolidé des budgets "
                   "principal et annexes. Un code que l'OFGL donne à plusieurs collectivités ne se rapproche pas : "
                   "jusqu'en 2015, celui de la région qui a absorbé chacune des régions fusionnées en 2016 ; jusqu'en "
                   "2020, « 67A », celui du Bas-Rhin et du Haut-Rhin.", "",
                   "| Niveau | Exercices | Collectivités | Rapprochées | Sans correspondant | Collectivités de l'OFGL sans "
                   "correspondant |", "|---|---|---|---|---|---|"]
        par_source = collections.defaultdict(list)
        for (source, exercice), r in sorted(rapprochees.items()):
            par_source[source].append((exercice, *r))
        for source, liste in sorted(par_source.items(), key=lambda e: list(NIVEAUX_INDIVIDUELS).index(e[0])):
            lignes.append(f"| {NIVEAUX_INDIVIDUELS[source]} | {plage([e[0] for e in liste])} | "
                          f"{fr(sum(e[1] for e in liste), 0)} | {fr(sum(e[2] for e in liste), 0)} | "
                          f"{fr(sum(e[1] - e[2] for e in liste), 0)} | {fr(sum(e[3] for e in liste), 0)} |")
        lignes += ["", "Agrégats de même intitulé, ou de même objet, des deux publications, établies d'après les mêmes "
                   "comptes de gestion. L'OFGL définit les siens compte par compte, en opérations réelles et hors gestion "
                   "active de la dette (définitions de la DGCL) ; les maquettes de la DGFiP ne disent pas les leurs. Un "
                   "agrégat que le jeu de l'OFGL publie pour d'autres collectivités de l'exercice, mais pas pour celle-ci, "
                   "y vaut zéro. La part d'égaux mesure combien les deux définitions se recouvrent.", "",
                   "| Niveau | Comptes individuels | Comptes de l'OFGL | Exercices | Comparés | Égaux à l'arrondi près | "
                   "Part | Plus grand écart (DGFiP − OFGL) |", "|---|---|---|---|---|---|---|---|"]
        for (source, dgfip, ofgl_), (compares, egaux, pire, annees) in sorted(
                comparaisons.items(), key=lambda e: (list(NIVEAUX_INDIVIDUELS).index(e[0][0]), PAIRES_OFGL.index(e[0][1:]))):
            texte = "aucun" if pire is None else (f"{ecart_lisible(pire[0], 'euros')} : "
                                                  f"{noms.get((source, pire[2], pire[1]), '')} ({pire[1]}), {pire[2]}")
            lignes.append(f"| {NIVEAUX_INDIVIDUELS[source]} | {dgfip.removeprefix('COMPTES_INDIVIDUELS.')} | "
                          f"{ofgl_.removeprefix('COMPTES_LOCAUX.')} | {plage(annees)} | {fr(compares, 0)} | "
                          f"{fr(egaux, 0)} | {fr(100 * egaux / compares, 1)} % | {texte} |")
        lignes.append("")
    return lignes


# 14. Balances des comptes de l'État. Le bilan et le compte de résultat qu'on tire d'une balance, par les indicateurs de
# synthèse que la DGFiP donne à ses lignes : chaque ligne des états financiers est la somme des lignes de ses
# indicateurs, chacune au signe de l'indicateur, plus celle de ses composantes ; la situation nette est l'actif moins le
# passif, et non la somme de ses lignes, la balance laissant le solde de l'exercice dans les comptes de charges et de
# produits.
COMPOSITIONS_ETAT = dict(_RESULTAT)
COMPOSITIONS_ETAT.update({t + s: [c + s for c in cs] for t, cs in _ACTIF for s in ("_BRUT", "_AMORTISSEMENTS")})
COMPOSITIONS_ETAT.update({t: cs for t, cs in _PASSIF if t != "SITUATION_NETTE"})
# La ligne dont chacune est une composante, dans la présentation des états financiers.
PARENTS_ETAT = {c.lstrip("-"): t for t, cs in _RESULTAT + _ACTIF + _PASSIF for c in cs}
PARENTS_ETAT.update({c + s: t + s for t, cs in _ACTIF for c in cs for s in ("_BRUT", "_AMORTISSEMENTS")})
ENGAGEMENTS = "EHB"
COMPOSITIONS_ETAT_SITUATION = dict(_PASSIF)["SITUATION_NETTE"]


def etats_depuis_balance(directs):
    """La fonction qui donne, en millions d'euros (decimal.Decimal), chaque ligne du bilan et du compte de résultat de
    l'État que donne une balance, d'après `directs`, {ligne: somme des lignes de ses indicateurs} ; rien pour une ligne
    dont la balance n'a ni indicateur ni composante."""
    memoire = {}

    def ligne(x):
        if x not in memoire:
            if x == "SITUATION_NETTE":
                memoire[x] = ligne("ACTIF") - ligne("PASSIF")
            elif x in _LIGNES_ACTIF:
                brut, amortissements = ligne(x + "_BRUT"), ligne(x + "_AMORTISSEMENTS")
                memoire[x] = (None if brut is None and amortissements is None
                              else (brut or 0) - (amortissements or 0))
            else:
                parties = [(ligne(c.lstrip("-")), -1 if c.startswith("-") else 1) for c in COMPOSITIONS_ETAT.get(x, [])]
                presentes = [s * v for v, s in parties if v is not None]
                memoire[x] = (directs.get(x) if not presentes
                              else directs.get(x, decimal.Decimal(0)) + sum(presentes))
        return memoire[x]
    return ligne


def balances_retenues():
    """{exercice: inscription de sa balance la plus récente}."""
    retenues = {}
    for i in lire("tables/fichiers_balances_etat.csv"):
        if i["contenu"] == "balance" and (i["exercice"] not in retenues or i["version"] > retenues[i["exercice"]]["version"]):
            retenues[i["exercice"]] = i
    return retenues


def premieres_versions(derniers, perimetre, prefixe, unite):
    """{(concept sans son préfixe, période): ligne} : pour chaque chiffre d'un périmètre dans une unité, sa première
    version publiée, celle de la loi d'approbation des comptes de l'exercice, et non celle qu'une loi suivante peut
    donner en comparaison."""
    retenues = {}
    for l in derniers.values():
        if l["perimetre_id"] == perimetre and l["concept_id"].startswith(prefixe) and l["unite_id"] == unite:
            k = (l["concept_id"].removeprefix(prefixe), l["periode"])
            if k not in retenues or l["version"] < retenues[k]["version"]:
                retenues[k] = l
    return retenues


def balances_etat_controlees(derniers):
    """Pour chaque exercice, la balance inscrite la plus récente, et ce qu'elle donne : (exercice, inscription, comptes
    absents du plan comptable, somme des soldes, {indicateur d'engagements hors bilan: somme}, résultat, {ligne des
    états financiers: (loi, marge, balance)})."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/indicateurs_balances_etat.csv")
    plans = [i for i in lire("tables/fichiers_balances_etat.csv") if i["contenu"] == "plan"]
    plan = balances.plan(fichiers[max(plans, key=lambda i: i["version"])["fichier_id"]]) if plans else {}
    lois = premieres_versions(derniers, "ETAT_CGE", "COMPTES_ETAT.", "MIO_EUR")
    resultat = []
    for exercice, inscrit in sorted(balances_retenues().items()):
        _, decrites, soldes = balances.balance(fichiers[inscrit["fichier_id"]], referentiel)
        rattaches = balances.indicateurs_de(exercice, referentiel)
        directs, engagements = collections.defaultdict(decimal.Decimal), collections.defaultdict(decimal.Decimal)
        resultat_exercice = decimal.Decimal(0)
        for d, solde in zip(decrites, soldes):
            indicateur = rattaches[d["indicateurs_de_synthese"]]
            if indicateur["categorie"] == ENGAGEMENTS:
                engagements[indicateur["indicateur"]] += solde
            if indicateur["categorie"] in ("Charges", "Produits"):
                resultat_exercice += solde
            if indicateur["concept_id"]:
                directs[indicateur["concept_id"].removeprefix("COMPTES_ETAT.")] += int(indicateur["signe"]) * solde / 10 ** 6
        ligne = etats_depuis_balance(directs)
        etats = {concept: (decimal.Decimal(l["valeur"]), decimal.Decimal(valeur(l)[1]) / 10 ** 6, ligne(concept))
                 for (concept, periode), l in lois.items() if periode == exercice}
        absents = len({d["compte"] for d in decrites} - set(plan))
        resultat.append((exercice, inscrit, absents, sum(soldes), dict(engagements), resultat_exercice, etats))
    return resultat


def ecart_etat(etats, concept):
    """L'écart (loi − balance) d'une ligne des états financiers, quand il dépasse l'arrondi de la loi ; sinon zéro, ou
    rien si la balance ne la donne pas."""
    if concept not in etats or etats[concept][2] is None:
        return None
    loi, marge, balance_ = etats[concept]
    return loi - balance_ if abs(loi - balance_) > marge else decimal.Decimal(0)


def sous(concept, total):
    """Vrai si une ligne des états financiers est une composante, directe ou non, d'un total."""
    while concept in PARENTS_ETAT:
        concept = PARENTS_ETAT[concept]
        if concept == total:
            return True
    return False


def explication_ecart(concept, etats):
    """Ce qui explique l'écart d'une ligne des états financiers entre la loi et la balance, quand le calcul le montre :
    le report des exercices antérieurs qui comprend le solde de l'exercice ; un reclassement entre les composantes d'un
    total juste ; une compensation de créances et de dettes, qui réduit d'un même montant l'actif et le passif de la loi,
    et laisse la situation nette juste."""
    loi, marge, balance_ = etats[concept]
    if balance_ is None:
        return "la balance ne distingue pas cette ligne"
    ecart = loi - balance_
    solde = etats.get("SOLDE_OPERATIONS_EXERCICE")
    if concept == "REPORT_EXERCICES_ANTERIEURS" and solde is not None and abs(ecart - solde[0]) <= marge + solde[1]:
        return "la loi y ajoute le solde des opérations de l'exercice"
    parent = PARENTS_ETAT.get(concept)
    if ecart_etat(etats, parent) == 0:
        return f"reclassement entre les composantes de {parent}, total juste"
    actif, passif = ecart_etat(etats, "ACTIF"), ecart_etat(etats, "PASSIF")
    if actif and passif and abs(actif - passif) <= 1 and (concept in ("ACTIF", "PASSIF") or sous(concept, "ACTIF")
                                                          or sous(concept, "PASSIF")):
        if abs(ecart - actif) <= 1:
            return f"compensation de créances et de dettes : la loi a l'actif et le passif moindres de {fr(-actif, 1)} M€"
        if parent and ecart_etat(etats, parent) and abs(ecart_etat(etats, parent) - actif) <= 1:
            return f"reclassement entre les composantes de {parent}, qui porte la compensation"
    return ""


def partie_balances_etat(derniers):
    exercices = balances_etat_controlees(derniers)
    if not exercices:
        return []
    lignes = ["## 14. Balances des comptes de l'État", "",
              "Les balances générales des comptes de l'État que publie la DGFiP, telles qu'à la clôture de chaque exercice "
              "elles ont servi à produire le compte général de l'État : une ligne par compte, mission, programme et nature "
              "budgétaire, avec son solde de sortie, au centime, un solde créditeur étant négatif. Les comptes de charges "
              "et de produits n'y sont pas soldés : leur somme est le résultat de l'exercice, ici un déficit quand elle "
              "est positive. Chaque balance doit s'équilibrer, et les engagements hors bilan (classe 8) avec leur "
              "contrepartie.", "",
              "| Exercice | Lignes | Comptes | Comptes absents du plan comptable joint | Somme des soldes | "
              "Somme des engagements hors bilan | Charges et produits réunis |", "|---|---|---|---|---|---|---|"]
    for exercice, inscrit, absents, total, engagements, resultat, _ in exercices:
        lignes.append(f"| {exercice} | {fr(int(inscrit['lignes']), 0)} | {fr(int(inscrit['comptes']), 0)} | "
                      f"{fr(absents, 0)} | {fr(total + 0, 2)} € | {fr(sum(engagements.values()) + 0, 2)} € | "
                      f"{fr(resultat / 10 ** 6, 1, True)} M€ |")
    indicateurs = sorted({i for *_, engagements, _, _ in exercices for i in engagements})
    referentiel = {i["indicateur"]: i for i in lire("tables/indicateurs_balances_etat.csv")}
    lignes += ["", "Engagements hors bilan de l'État, en milliards d'euros, au signe de leur présentation (un engagement "
               "donné, solde créditeur, est positif) :", "",
               "| Indicateur | " + " | ".join(e[0] for e in exercices) + " |",
               "|---|" + "---|" * len(exercices)]
    for i in indicateurs:
        signe = int(referentiel[i]["signe"])
        lignes.append(f"| {i} | " + " | ".join(fr(signe * e[4][i] / 10 ** 9, 1) if i in e[4] else "—"
                                               for e in exercices) + " |")
    comparees = [(e[0], concept, *v) for e in exercices for concept, v in e[6].items()]
    # Une ligne que la balance n'alimente pas et que la loi donne nulle est égale.
    egales = [c for c in comparees if abs(c[2] - (c[4] or 0)) <= c[3] and (c[4] is not None or c[2] == 0)]
    lignes += ["", "Le bilan et le compte de résultat que donne chaque balance, par les indicateurs de synthèse que la DGFiP "
               "rattache aux lignes des états financiers (tables/indicateurs_balances_etat.csv), contre ceux de la loi "
               "d'approbation des comptes de l'exercice, ligne par ligne et total par total, en millions d'euros. Une "
               "ligne de la loi est exacte au demi-million près ; la situation nette que donne la balance est l'actif "
               f"moins le passif. {fr(len(comparees), 0)} lignes comparées, {fr(len(egales), 0)} égales à l'arrondi "
               f"près.", "",
               "| Exercice | Lignes comparées | Égales | Autres |", "|---|---|---|---|"]
    for exercice in [e[0] for e in exercices]:
        n = sum(1 for c in comparees if c[0] == exercice)
        k = sum(1 for c in egales if c[0] == exercice)
        lignes.append(f"| {exercice} | {fr(n, 0)} | {fr(k, 0)} | {fr(n - k, 0)} |")
    autres = [c for c in comparees if c not in egales]
    # Le montant brut d'un actif qui n'a ni amortissement ni dépréciation n'est pas répété : sa ligne nette, de même écart à
    # l'arrondi près, le donne.
    nets = {(c[0], c[1]): c[2] - (c[4] or 0) for c in autres}
    autres = [c for c in autres if not (c[1].endswith("_BRUT") and (c[0], c[1].removesuffix("_BRUT")) in nets
                                        and abs(nets[(c[0], c[1].removesuffix("_BRUT"))] - (c[2] - (c[4] or 0))) <= 1)]
    if autres:
        lignes += ["", "Lignes qui diffèrent, et ce qui l'explique quand le calcul le montre : le report des exercices "
                   "antérieurs de la loi qui comprend le solde des opérations de l'exercice (le bilan y est présenté après "
                   "son affectation) ; un reclassement entre les lignes d'un même total, que la loi donne alors égal à "
                   "celui de la balance ; une compensation de créances et de dettes, quand l'actif et le passif de la loi "
                   "sont moindres d'un même montant, la situation nette restant juste ; une ligne que la balance ne "
                   "distingue pas. Le montant brut d'un actif n'est pas répété quand sa ligne nette porte le même écart.",
                   "",
                   "| Exercice | Ligne | Loi | Balance | Écart (loi − balance) | Explication |",
                   "|---|---|---|---|---|---|"]
        etats = {e[0]: e[6] for e in exercices}
        for exercice, concept, loi, _, balance_ in sorted(autres):
            lignes.append(f"| {exercice} | {concept} | {fr(loi, 0)} | "
                          f"{'—' if balance_ is None else fr(balance_, 1)} | "
                          f"{'—' if balance_ is None else fr(loi - balance_, 1, True)} | "
                          f"{explication_ecart(concept, etats[exercice])} |")
    # Un exercice où la loi compte le solde de l'exercice dans la situation nette sans le porter sur aucune de ses lignes.
    for exercice, *_, etats in exercices:
        lignes_sn = [etats[c][0] for c in COMPOSITIONS_ETAT_SITUATION if c in etats]
        if "SITUATION_NETTE" in etats and "SOLDE_OPERATIONS_EXERCICE" in etats and lignes_sn:
            reste = etats["SITUATION_NETTE"][0] - sum(lignes_sn)
            solde = etats["SOLDE_OPERATIONS_EXERCICE"][0]
            if abs(reste) > len(lignes_sn) and abs(reste - solde) <= len(lignes_sn) + 1:
                lignes += ["", f"En {exercice}, la situation nette de la loi comprend le solde des opérations de "
                           f"l'exercice ({fr(solde, 0, True)} M€) sans qu'aucune de ses lignes le porte : la balance, "
                           f"dont la situation nette (l'actif moins le passif) est celle de la loi, le laisse dans les "
                           f"comptes de charges et de produits, et la somme des lignes de la loi s'écarte de son total "
                           f"d'autant (section 1)."]
    lignes.append("")
    return lignes


# 15. Dette négociable de l'État. L'encours que l'Insee reprend de l'Agence France Trésor, contre les variations que
# l'Insee publie avec lui, le tableau de financement des lois d'approbation des comptes et les titres négociables de la
# balance de l'État, que la DGFiP détaille par indicateur : le nominal des titres, le différentiel d'indexation des
# titres indexés sur l'inflation, et des intérêts, que l'encours ne compte pas. Un indicateur de détail que
# DETAILS_TITRES ne classe pas est signalé dans le rapport.
DETTE_NEGOCIABLE = "insee.bdm-dette-negociable-etat"
DETAILS_TITRES = {"P001": "nominal", "P002": "nominal", "P009": "nominal", "P012": "nominal",
                  "P005": "indexation", "P014": "indexation",
                  "P004": "interets", "P008": "interets", "P016": "interets", "P017": "interets", "P084": "interets",
                  "P085": "interets"}
BTF = "P012"
# Les OAT que la balance dit « à taux variable », qui sont les OAT indexées, et les différentiels d'indexation.
INDEXES = ("P002", "P005", "P014")
COURT_TERME = ["COURT_TERME_EUROS", "COURT_TERME_DEVISES"]
MOYEN_LONG_TERME = ["MOYEN_LONG_TERME_EUROS", "MOYEN_LONG_TERME_DEVISES"]


def titres_negociables_des_balances():
    """{exercice: {indicateur de détail: montant, en euros}} : les lignes de chaque balance dont l'indicateur de
    synthèse alimente les titres négociables du bilan, au signe du bilan."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/indicateurs_balances_etat.csv")
    resultat = {}
    for exercice, inscrit in sorted(balances_retenues().items()):
        _, decrites, soldes = balances.balance(fichiers[inscrit["fichier_id"]], referentiel)
        rattaches = balances.indicateurs_de(exercice, referentiel)
        detail = collections.defaultdict(decimal.Decimal)
        for d, solde in zip(decrites, soldes):
            indicateur = rattaches[d["indicateurs_de_synthese"]]
            if indicateur["concept_id"] == "COMPTES_ETAT.TITRES_NEGOCIABLES":
                detail[d["indicateurs_de_detail"]] += int(indicateur["signe"]) * solde
        resultat[exercice] = dict(detail)
    return resultat


def code_detail(indicateur):
    """Le code d'un indicateur de détail, tel que la balance l'écrit avant son libellé (« P012_BTF »)."""
    return indicateur.partition("_")[0]


def signe_arrondi(x, decimales):
    """Un écart arrondi, signé, sans « −0 »."""
    return fr(round(x, decimales) + 0.0, decimales, True)


def sur(n, total, mot):
    """« 9 années sur 10 », « 0 exercice sur 10 »."""
    return f"{fr(n, 0)} {mot}{'s' if n >= 2 else ''} sur {fr(total, 0)}"


def partie_dette_negociable(derniers):
    encours, variations = {}, {}
    for l in derniers.values():
        if l["source_id"] == DETTE_NEGOCIABLE:
            cible = variations if l["traitements"] == "variation_depuis_decembre" else encours
            cible[(l["concept_id"].removeprefix("DETTE_NEGOCIABLE."), l["periode"])] = l
    if not encours:
        return []

    def fin(concepts, mois_):
        """(euros, marge) de la somme des encours de la fin d'un mois, ou rien s'il en manque un."""
        lus = [encours.get((c, mois_)) for c in concepts]
        return None if None in lus else (sum(valeur(l)[0] for l in lus), sum(valeur(l)[1] for l in lus))

    mois = sorted({m for _, m in encours})
    # Les mois où un encours n'est pas la somme de ses parts (section 1), et ceux où cette somme est l'encours du mois
    # précédent.
    exceptions = []
    for precedent, m in zip([None] + mois, mois):
        for total, parts in _DETTE_NEGOCIABLE:
            t, s = fin([total], m), fin(parts, m)
            if t is not None and s is not None and depasse(t[0] - s[0], t[1] + s[1]):
                avant = fin([total], precedent) if precedent else None
                exceptions.append((m, total, parts, t[0], s[0],
                                   avant is not None and not depasse(s[0] - avant[0], s[1] + avant[1])))
    devises = [valeur(l)[0] for (c, _), l in encours.items() if c.endswith("_DEVISES")]
    lignes = ["## 15. Dette négociable de l'État", "",
              f"L'encours de la dette négociable de l'État à la fin de chaque mois, de {mois[0]} à {mois[-1]}, que l'Insee "
              "reprend de l'Agence France Trésor : les titres à court terme et à moyen et long terme, en euros et en "
              "devises, à taux fixe et indexés sur l'inflation"
              + (" ; les titres en devises sont nuls sur toute la période" if devises and not any(devises) else "")
              + ". Chaque encours est la somme de ses parts (section 1)"
              + ("" if not exceptions else ", sauf " + " ; ".join(
                  f"en {m}, où {' et '.join(parts)} font {fr(s / 1e6, 0)} M€ et {total} {fr(t / 1e6, 0)} M€"
                  + (f" (leur somme est {total} du mois précédent)" if avant else "")
                  for m, total, parts, t, s, avant in exceptions)) + ".", ""]
    # Les variations depuis le début de l'année, contre la différence des encours.
    ecarts, verifiees = [], 0
    for (concept, m), l in sorted(variations.items()):
        debut, actuel = fin([concept], f"{int(m[:4]) - 1}-12"), fin([concept], m)
        if debut is not None and actuel is not None:
            verifiees += 1
            publiee, marge, _ = valeur(l)
            if depasse(publiee - (actuel[0] - debut[0]), marge + actuel[1] + debut[1]):
                ecarts.append((m, concept, publiee, actuel[0] - debut[0]))
    lignes += [f"Les variations depuis le début de l'année que l'Insee publie avec l'encours, contre la différence de "
               f"l'encours de la fin du mois et de celui de la fin de l'année précédente : {fr(verifiees, 0)} "
               f"vérifiées, {fr(len(ecarts), 0)} en écart" + (" (en millions d'euros) :" if ecarts else "."), ""]
    if ecarts:
        lignes += ["| Mois | Encours | Variation publiée | Différence des encours | Écart |", "|---|---|---|---|---|"]
        lignes += [f"| {m} | {c} | {fr(v / 1e6, 0, True)} | {fr(d / 1e6, 0, True)} | {signe_arrondi((v - d) / 1e6, 0)} |"
                   for m, c, v, d in ecarts]
        lignes.append("")
    # Le tableau de financement : la variation de chaque encours d'une fin d'année à l'autre, contre ses flux.
    tf = {k: valeur(l)[:2] for k, l in premieres_versions(derniers, "ETAT_LF", "LOLF.", "MD_EUR").items()}
    titres = titres_negociables_des_balances()

    def part(exercice, classes):
        """En euros, la part des titres négociables d'une balance que des classes de DETAILS_TITRES réunissent."""
        return float(sum((v for k, v in titres[exercice].items() if DETAILS_TITRES.get(code_detail(k)) in classes),
                         decimal.Decimal(0)))

    lignes += ["Le tableau de financement de l'État, dans la loi d'approbation des comptes de chaque année, en milliards "
               "d'euros : la variation de l'encours à court terme d'une fin d'année à l'autre, contre la variation nette "
               "des titres à court terme ; celle de l'encours à moyen et long terme, contre les émissions nettes des "
               "rachats moins les amortissements. L'écart de celle-ci est la revalorisation des titres indexés sur "
               "l'inflation : l'encours compte leur supplément d'indexation, que les émissions et les amortissements du "
               "tableau ne comptent pas, sauf les suppléments versés à l'échéance des titres, qu'il range dans les "
               "amortissements. La revalorisation est donc la variation du différentiel d'indexation de la balance de "
               "l'État (section 14), plus les suppléments versés"
               + (f" ; elle ne se calcule qu'à partir de {int(min(titres)) + 1}, la première balance de la base étant "
                  f"celle de {min(titres)}." if titres else "."), "",
               "| Année | Court terme : variation de l'encours | Variation nette des titres à court terme | Écart | Moyen et "
               "long terme : variation de l'encours | Émissions moins amortissements | Écart | Revalorisation des titres "
               "indexés | Reste |", "|---|---|---|---|---|---|---|---|---|"]
    courts, restes = [], []
    for annee in range(int(mois[0][:4]) + 1, int(mois[-1][:4]) + 1):
        a, p = str(annee), str(annee - 1)
        c1, c0 = fin(COURT_TERME, f"{a}-12"), fin(COURT_TERME, f"{p}-12")
        l1, l0 = fin(MOYEN_LONG_TERME, f"{a}-12"), fin(MOYEN_LONG_TERME, f"{p}-12")
        if None in (c1, c0, l1, l0) or ("EMISSIONS_DETTE_MLT", a) not in tf:
            continue
        court, long_ = c1[0] - c0[0], l1[0] - l0[0]
        cellules = [signe_arrondi(court / 1e9, 1)]
        variation = tf.get(("VARIATION_TITRES_COURT_TERME", a))
        if variation is None:
            cellules += ["—", "—"]
        else:
            courts.append(not depasse(court - variation[0], c1[1] + c0[1] + variation[1]))
            cellules += [signe_arrondi(variation[0] / 1e9, 1), signe_arrondi((court - variation[0]) / 1e9, 1)]
        amortissements = tf.get(("AMORTISSEMENT_DETTE_MLT", a))
        if amortissements is None and ("AMORTISSEMENT_DETTE_LT", a) in tf and ("AMORTISSEMENT_DETTE_MT", a) in tf:
            amortissements = tuple(x + y for x, y in zip(tf[("AMORTISSEMENT_DETTE_LT", a)],
                                                         tf[("AMORTISSEMENT_DETTE_MT", a)]))
        supplements = tf.get(("SUPPLEMENTS_INDEXATION", a))
        cellules.append(signe_arrondi(long_ / 1e9, 1))
        if amortissements is None:
            cellules += ["—", "—", "—", "—"]
        else:
            flux = tf[("EMISSIONS_DETTE_MLT", a)][0] - amortissements[0]
            cellules += [signe_arrondi(flux / 1e9, 1), signe_arrondi((long_ - flux) / 1e9, 1)]
            if a in titres and p in titres and supplements is not None:
                revalorisation = part(a, ["indexation"]) - part(p, ["indexation"]) + supplements[0]
                reste = long_ - flux - revalorisation
                restes.append(not depasse(reste, l1[1] + l0[1] + tf[("EMISSIONS_DETTE_MLT", a)][1] + amortissements[1]
                                          + supplements[1]))
                cellules += [signe_arrondi(revalorisation / 1e9, 1), signe_arrondi(reste / 1e9, 1)]
            else:
                cellules += ["—", "—"]
        lignes.append(f"| {a} | " + " | ".join(cellules) + " |")
    lignes += ["", f"La variation de l'encours à court terme est la variation nette des titres à court terme du tableau "
               f"de financement {sur(sum(courts), len(courts), 'année')}, à l'arrondi près ; à moyen et long terme, la "
               f"revalorisation des titres indexés explique l'écart à l'arrondi près "
               f"{sur(sum(restes), len(restes), 'année')}.", ""]
    # La balance et le bilan à la fin de l'exercice.
    inconnus = sorted({k for d in titres.values() for k in d if code_detail(k) not in DETAILS_TITRES})
    bilan = premieres_versions(derniers, "ETAT_CGE", "COMPTES_ETAT.", "MIO_EUR")
    lignes += ["L'encours de la fin de chaque exercice contre les titres négociables de la balance de l'État (section 14), "
               "que la DGFiP détaille par indicateur : le nominal des OAT, des BTAN et des BTF ; le différentiel "
               "d'indexation des titres indexés ; les intérêts courus, les coupons courus, les intérêts capitalisés et les "
               "intérêts constatés d'avance. L'encours à court terme est comparé aux BTF ; l'encours indexé sur "
               "l'inflation, aux OAT que la balance dit « à taux variable » et aux différentiels d'indexation. En millions "
               "d'euros." + (f" Indicateurs de détail que la base ne classe pas : {', '.join(inconnus)}." if inconnus
                            else ""), "",
               "| Exercice | Encours | Nominal et indexation (balance) | Écart | Court terme | BTF | Écart | Indexé sur "
               "l'inflation | OAT indexées et indexation | Écart |", "|---|---|---|---|---|---|---|---|---|---|"]
    justes, ecarts_totaux, bilans = collections.defaultdict(list), [], []
    for exercice, detail in sorted(titres.items()):
        total = fin(["ENCOURS"], f"{exercice}-12")
        if total is None:
            continue
        nominal = part(exercice, ["nominal", "indexation"])
        cellules = []
        for nom_, aft, balance_ in (
                ("total", total, nominal),
                ("court", fin(COURT_TERME, f"{exercice}-12"),
                 float(sum((v for k, v in detail.items() if code_detail(k) == BTF), decimal.Decimal(0)))),
                ("indexe", fin(["INDEXEE_INFLATION"], f"{exercice}-12"),
                 float(sum((v for k, v in detail.items() if code_detail(k) in INDEXES), decimal.Decimal(0))))):
            if aft is None:
                cellules += ["—", fr(balance_ / 1e6, 1), "—"]
                continue
            justes[nom_].append(not depasse(aft[0] - balance_, aft[1]))
            cellules += [fr(aft[0] / 1e6, 0), fr(balance_ / 1e6, 1), signe_arrondi((aft[0] - balance_) / 1e6, 1)]
        lignes.append(f"| {exercice} | " + " | ".join(cellules) + " |")
        ecarts_totaux.append((total[0] - nominal, total[0]))
        if ("TITRES_NEGOCIABLES", exercice) in bilan:
            bilans.append((exercice, valeur(bilan[("TITRES_NEGOCIABLES", exercice)]), total[0], nominal,
                           part(exercice, ["interets"])))
    lignes += ["", f"À l'arrondi près, l'encours égale le nominal et l'indexation de la balance "
               f"{sur(sum(justes['total']), len(justes['total']), 'exercice')} ; l'encours à court terme, les BTF, "
               f"{sur(sum(justes['court']), len(justes['court']), 'exercice')} ; l'encours indexé, les OAT indexées et "
               f"leur indexation, {sur(sum(justes['indexe']), len(justes['indexe']), 'exercice')}."]
    if not all(justes["total"]):
        hors = [abs(e) for e, _ in ecarts_totaux]
        lignes[-1] += (f" L'écart de l'encours au nominal et à l'indexation va de {fr(min(hors) / 1e6, 0)} à "
                       f"{fr(max(hors) / 1e6, 0)} millions d'euros"
                       + (", dans un sens ou dans l'autre" if min(e for e, _ in ecarts_totaux) < 0
                          < max(e for e, _ in ecarts_totaux) else "")
                       + f", soit au plus {fr(max(abs(e) / t for e, t in ecarts_totaux) * 100, 3)} % de l'encours ; ni "
                       "l'Insee ni la balance n'en donnent la cause.")
    lignes.append("")
    if bilans:
        lignes += ["Les titres négociables du bilan de la loi d'approbation des comptes (sa première version publiée), "
                   "contre l'encours et les intérêts que la balance range avec les titres, en millions d'euros :", "",
                   "| Exercice | Titres négociables du bilan | Encours | Différence | Intérêts (balance) | Reste |",
                   "|---|---|---|---|---|---|"]
        for exercice, (titres_bilan, _, _), total, _, interets in bilans:
            lignes.append(f"| {exercice} | {fr(titres_bilan / 1e6, 0)} | {fr(total / 1e6, 0)} | "
                          f"{fr((titres_bilan - total) / 1e6, 0, True)} | {fr(interets / 1e6, 1)} | "
                          f"{signe_arrondi((titres_bilan - total - interets) / 1e6, 1)} |")
        # Le reste est l'écart de l'encours à la balance, au signe près, quand le bilan donne les titres de la balance.
        if all(not depasse(t - nominal - interets, marge) for _, (t, marge, _), _, nominal, interets in bilans):
            lignes += ["", "La différence est celle des intérêts ; le reste est, au signe et à l'arrondi du bilan près, "
                       "l'écart de l'encours au nominal et à l'indexation de la balance, ci-dessus : les titres "
                       "négociables du bilan sont ceux de la balance."]
        lignes.append("")
    return lignes


# 16. Comptes de la protection sociale (DREES). Les sections 1 à 3 vérifient les sommes de l'export et du classeur : chaque
# prestation contre ses parties, chaque secteur contre ses régimes, l'ensemble des régimes contre ses secteurs, les
# emplois et les ressources contre leurs lignes et contre leurs groupes de secteurs, les prestations de l'ensemble contre
# celles en espèces et en nature du classeur. Celle-ci rapproche les prestations de chaque groupe de secteurs du classeur
# de celles de ses secteurs dans l'export, et explique l'écart de l'ensemble par le double compte d'un secteur.
GROUPES_CPS = ["CPS_ASSO", "CPS_APUC_APUL", "CPS_SF_SNF"]


def partie_protection_sociale(derniers):
    prestations, especes_nature = {}, collections.defaultdict(lambda: [0.0, 0.0])
    for l in derniers.values():
        if not l["concept_id"].startswith("CPS."):
            continue
        v, m, _ = valeur(l)
        if l["concept_id"] == cps.PRESTATIONS and not l["fonction_id"]:
            prestations[(l["perimetre_id"], l["periode"])] = (v, m)
        elif l["concept_id"] in ("CPS.PRESTATIONS_ESPECES", "CPS.PRESTATIONS_NATURE"):
            especes_nature[(l["perimetre_id"], l["periode"])][0] += v
            especes_nature[(l["perimetre_id"], l["periode"])][1] += m
    if not prestations:
        return []
    parents = {p["id"]: p["parent_id"] for p in lire("tables/perimetres.csv") if p["norme_id"] == "CPS"}
    regimes = set(cps.REGIMES.values())
    annees = sorted({a for _, a in prestations})
    par_annee = collections.Counter(a for p, a in prestations if p in regimes)
    lignes = ["## 16. Comptes de la protection sociale", "",
              f"Les comptes de la protection sociale de la DREES : les prestations de l'ensemble des régimes de "
              f"{annees[0]} à {annees[-1]}, de chaque secteur et de chaque régime depuis {min(par_annee)}, jusqu'à "
              f"{fr(max(par_annee.values()), 0)} régimes une même année ({fr(len({p for p, _ in prestations if p in regimes}), 0)} "
              f"en tout, la nomenclature des régimes changeant en 1990), et les emplois et les ressources de l'ensemble "
              f"des régimes et, depuis {min(a for p, a in especes_nature if p in GROUPES_CPS)}, de chaque groupe de "
              f"secteurs. Les sections 1 à 3 en vérifient les sommes.", ""]
    # Les prestations de chaque groupe de secteurs dans le classeur, contre celles de ses secteurs dans l'export.
    comparees, ecarts = 0, []
    for (groupe, annee), (v, m) in sorted(especes_nature.items()):
        if groupe not in GROUPES_CPS:
            continue
        parties = [prestations[(s, annee)] for s in _CPS_SECTEURS if parents[s] == groupe and (s, annee) in prestations]
        comparees += 1
        somme = sum(x for x, _ in parties)
        if depasse(v - somme, m + sum(x for _, x in parties)):
            ecarts.append((groupe, annee, v, somme))
    lignes += [f"Prestations en espèces et en nature de chaque groupe de secteurs dans le classeur, contre la somme des "
               f"prestations de ses secteurs dans l'export : {fr(comparees, 0)} comparées, {fr(len(ecarts), 0)} en "
               f"écart" + (" (en millions d'euros) :" if ecarts else "."), ""]
    if ecarts:
        lignes += ["| Groupe | Année | Classeur | Export | Écart |", "|---|---|---|---|---|"]
        lignes += [f"| {g} | {a} | {fr(v / 1e6, 1)} | {fr(s / 1e6, 1)} | {signe_arrondi((v - s) / 1e6, 1)} |"
                   for g, a, v, s in ecarts]
        lignes.append("")
    # L'ensemble des régimes : l'écart de l'export au classeur, contre l'excédent des secteurs de l'export sur leurs
    # régimes.
    rangees = []
    for annee in annees:
        if ("CPS_ENSEMBLE", annee) not in prestations or ("CPS_ENSEMBLE", annee) not in especes_nature:
            continue
        (total, marge), (classeur, marge_c) = prestations[("CPS_ENSEMBLE", annee)], especes_nature[("CPS_ENSEMBLE", annee)]
        if not depasse(total - classeur, marge + marge_c):
            continue
        excedents = []
        for s in _CPS_SECTEURS:
            if (s, annee) in prestations:
                parties = [prestations[(r, annee)] for r in regimes if parents[r] == s and (r, annee) in prestations]
                somme = sum(x for x, _ in parties)
                if parties and depasse(prestations[(s, annee)][0] - somme, prestations[(s, annee)][1]
                                       + sum(x for _, x in parties)):
                    excedents.append((s, prestations[(s, annee)][0], somme))
        rangees.append((annee, total, classeur, excedents))
    if rangees:
        lignes += ["Prestations de l'ensemble des régimes, dans l'export et dans le classeur (prestations en espèces et en "
                   "nature), quand elles diffèrent, et secteurs dont l'export donne un total supérieur à la somme de ses "
                   "régimes, en millions d'euros :", "",
                   "| Année | Export | Classeur | Écart | Secteur | Total du secteur | Somme de ses régimes | Excédent |",
                   "|---|---|---|---|---|---|---|---|"]
        for annee, total, classeur, excedents in rangees:
            for k, (s, v, somme) in enumerate(excedents or [("—", None, None)]):
                debut = (f"| {annee} | {fr(total / 1e6, 1)} | {fr(classeur / 1e6, 1)} | "
                         f"{signe_arrondi((total - classeur) / 1e6, 1)}") if k == 0 else "| | | |"
                lignes.append(debut + (f" | {s} | — | — | — |" if v is None else
                                       f" | {s} | {fr(v / 1e6, 1)} | {fr(somme / 1e6, 1)} | "
                                       f"{signe_arrondi((v - somme) / 1e6, 1)} |"))
        doubles = [a for a, total, classeur, e in rangees if len(e) == 1 and abs(e[0][1] - 2 * e[0][2]) <= 1
                   and abs((total - classeur) - (e[0][1] - e[0][2])) <= 1]
        if doubles:
            secteurs_ = sorted({e[0][0] for a, _, _, e in rangees if a in doubles})
            quand = (f"De {doubles[0]} à {doubles[-1]}" if len(doubles) == int(doubles[-1]) - int(doubles[0]) + 1
                     else f"En {plage(doubles)}")
            lignes += ["", f"{quand}, le total de l'export pour {' et '.join(secteurs_)} est le double de la "
                       f"somme de ses régimes, et l'écart de l'ensemble des régimes au classeur est cet excédent, à "
                       f"l'euro près : l'export y compte deux fois ce secteur, le classeur une seule."]
        lignes.append("")
    return lignes


# 17. Budget voté et budget exécuté. Les crédits qu'ouvre la loi de finances initiale de chaque année (états B, C et D)
# contre ce que constate la loi d'approbation des comptes de la même année : dépenses et autorisations d'engagement
# consommées (articles 4 à 6). La section 2 vérifie que chaque mission votée égale la somme de ses programmes, et chaque
# total celle de ses missions. Une mission se rapproche de son exécution par son identifiant, formé de son libellé.
VOTE_EXECUTE = {"BG": ("Budget général", "LOLF.BG_DEPENSES_BRUTES", "LOLF.BG_AE_CONSOMMEES"),
                "BA": ("Budgets annexes", "LOLF.BA_DEPENSES", "LOLF.BA_AE_CONSOMMEES"),
                "CAS": ("Comptes d'affectation spéciale", "LOLF.CAS_DEPENSES", "LOLF.CAS_AE_CONSOMMEES"),
                "CCF": ("Comptes de concours financiers", "LOLF.CCF_DEPENSES", "LOLF.CCF_AE_CONSOMMEES")}
# La mission des dotations pour dépenses accidentelles et imprévisibles et pour mesures générales de rémunérations
# (article 7 de la loi organique relative aux lois de finances), qu'un décret répartit entre les programmes des autres
# missions (article 11) : « Provisions », puis « Crédits non répartis ».
DOTATIONS = ("LOLF.PROVISIONS", "LOLF.CREDITS_NON_REPARTIS")
GRANDS_ECARTS = 15  # missions du budget général citées pour leur écart


def partie_budget_vote(derniers):
    votes, executes, arretees = {}, {}, collections.defaultdict(set)
    concepts_executes = {c for _, d, a in VOTE_EXECUTE.values() for c in (d, a)}
    for l in derniers.values():
        if l["perimetre_id"] != "ETAT_LF" or l["unite_id"] != "EUR":
            continue
        k = (l["concept_id"], l["fonction_id"], l["periode"])
        if l["concept_id"].endswith("_LFI"):
            votes[k] = valeur(l)[0]
            continue
        if l["source_id"].startswith(_LOI[:-1]) and l["fonction_id"]:
            # Les missions et les comptes que la loi d'approbation des comptes arrête, quelle que soit la grandeur.
            arretees[(l["concept_id"].split(".")[1].split("_")[0], l["periode"])].add(l["fonction_id"])
        if l["concept_id"] in concepts_executes and l["source_id"].startswith(_LOI[:-1]):
            # La loi d'approbation des comptes de l'exercice, et non une loi suivante qui le rappellerait.
            if k not in executes or l["version"] < executes[k]["version"]:
                executes[k] = l
    executes = {k: valeur(l)[0] for k, l in executes.items()}
    if not votes:
        return []
    parents = {f["id"]: f["parent_id"] for f in lire("tables/fonctions.csv")}
    libelles = {f["id"]: f["libelle"] for f in lire("tables/fonctions.csv")}
    annees = sorted({p for _, _, p in votes})
    md = lambda x: "—" if x is None else fr(x / 1e9, 1)
    ecart = lambda a, b: "—" if a is None or b is None else signe_arrondi((b - a) / 1e9, 1)
    lignes = ["## 17. Budget voté et budget exécuté", "",
              f"Les crédits qu'ouvre la loi de finances initiale de chaque année, de {annees[0]} à {annees[-1]} (états B, C "
              f"et D), contre ce que constate la loi d'approbation des comptes de la même année : les dépenses, fonds de "
              f"concours compris, et les autorisations d'engagement consommées (articles 4 à 6). L'écart vient des lois de "
              f"finances rectificatives, des décrets d'avance, de virement, de transfert et d'annulation, des reports de "
              f"crédits de l'année précédente, des fonds de concours et des crédits restés sans emploi : la base ne les a "
              f"pas encore un à un. Pour {annees[0]}, le texte lu ne donne que les crédits du budget général. La section 2 "
              f"vérifie que chaque mission votée égale la somme de ses programmes.", ""]
    v = lambda c, a: votes.get((c, "", a))
    e = lambda c, a: executes.get((c, "", a))
    lignes += ["Budget général, en milliards d'euros :", "",
               "| Année | Crédits de paiement votés | Dépenses | Écart | Autorisations d'engagement votées | "
               "Autorisations d'engagement consommées | Écart |", "|---|---|---|---|---|---|---|"]
    for a in annees:
        cp, dep, ae, cons = v("LOLF.BG_CP_LFI", a), e("LOLF.BG_DEPENSES_BRUTES", a), v("LOLF.BG_AE_LFI", a), \
            e("LOLF.BG_AE_CONSOMMEES", a)
        lignes.append(f"| {a} | {md(cp)} | {md(dep)} | {ecart(cp, dep)} | {md(ae)} | {md(cons)} | {ecart(ae, cons)} |")
    lignes += ["", "Budgets annexes et comptes spéciaux dotés de crédits : crédits de paiement votés contre dépenses, en "
               "milliards d'euros :", "",
               "| Année | " + " | ".join(f"{VOTE_EXECUTE[c][0]} : votés | dépenses" for c in ("BA", "CAS", "CCF")) + " |",
               "|---|" + "---|---|" * 3]
    for a in annees:
        lignes.append(f"| {a} | " + " | ".join(f"{md(v(f'LOLF.{c}_CP_LFI', a))} | {md(e(VOTE_EXECUTE[c][1], a))}"
                                              for c in ("BA", "CAS", "CCF")) + " |")
    # Les missions (et les budgets annexes, les comptes) votées contre celles que la loi de la même année arrête : une
    # mission est votée si la loi de finances lui ouvre des autorisations d'engagement ou des crédits de paiement, arrêtée
    # si la loi d'approbation des comptes lui donne un montant, consommé, ouvert, annulé ou, pour un compte, une recette
    # ou un solde.
    sans_vis_a_vis, rapprochees, comptees, ecarts = [], 0, 0, []
    programmes_votes, programmes_rapproches = 0, 0
    for a in annees:
        for c, (nom, depenses, consommees) in VOTE_EXECUTE.items():
            def par_fonction(concepts, source):
                return {f: tuple(source.get((k, f, a)) for k in concepts)
                        for (k, f, p) in source if k in concepts and p == a and f}
            votees = par_fonction((f"LOLF.{c}_AE_LFI", f"LOLF.{c}_CP_LFI"), votes)
            executees = par_fonction((consommees, depenses), executes)
            if not votees or not executees:
                continue
            missions_v = {f for f in votees if parents.get(f) == ""}
            missions_e = {f for f in arretees[(c, a)] if parents.get(f) == ""}
            executees.update({f: (None, None) for f in missions_e if f not in executees})
            comptees += len(missions_v)
            rapprochees += len(missions_v & missions_e)
            programmes = {f for f in votees if parents.get(f, "") != ""}
            programmes_votes += len(programmes)
            programmes_rapproches += len(programmes & arretees[(c, a)])
            for f in sorted(missions_v - missions_e):
                sans_vis_a_vis.append((a, nom, f, "votée seule", *votees[f]))
            for f in sorted(missions_e - missions_v):
                sans_vis_a_vis.append((a, nom, f, "exécutée seule", *executees[f]))
            if c == "BG":
                ecarts += [(a, libelles[f], votees[f][1], executees[f][1]) for f in missions_v & missions_e
                           if votees[f][1] is not None and executees[f][1] is not None]
    nulles = collections.defaultdict(list)  # missions votées sans aucun crédit, qui n'ont rien à exécuter
    for a, nom, f, quoi, ae, cp in sans_vis_a_vis:
        if quoi == "votée seule" and not ae and not cp:
            nulles[libelles[f]].append(a)
    # Les années où la loi d'approbation des comptes ne donne aucun montant à la mission des dotations, et celles où
    # elle lui constate une dépense ou une consommation.
    dotations_seules = sorted({a for a, nom, f, quoi, ae, cp in sans_vis_a_vis
                               if f in DOTATIONS and quoi == "votée seule" and (ae or cp)})
    depensees = sorted({p for (k, f, p), x in executes.items() if f in DOTATIONS and x})
    autres = [s for s in sans_vis_a_vis
              if not (s[3] == "votée seule" and ((not s[4] and not s[5]) or s[2] in DOTATIONS))]
    millions = lambda x: "—" if x is None else fr(x / 1e6, 1)
    lignes += ["", f"Missions, budgets annexes et comptes : {fr(rapprochees, 0)} des {fr(comptees, 0)} missions votées se "
               f"retrouvent, sous le même identifiant, dans la loi d'approbation des comptes de l'année, et "
               f"{fr(programmes_rapproches, 0)} des {fr(programmes_votes, 0)} programmes votés. "
               + ("Les missions votées sans aucun crédit n'ont rien à exécuter : "
                  + " ; ".join(f"{libelle} ({plage(a)})" for libelle, a in sorted(nulles.items())) + ". " if nulles else "")
               + "Les crédits des missions « Provisions », puis « Crédits non répartis », n'ont pas d'exécution propre : "
               "un décret les répartit en cours d'année entre les programmes des autres missions (article 11 de la loi "
               "organique relative aux lois de finances), et la loi d'approbation des comptes "
               + (f"n'y constate de dépense qu'en {plage(depensees)}" if depensees else "n'y constate aucune dépense")
               + (f" ; en {plage(dotations_seules)}, elle ne leur donne aucun montant" if dotations_seules else "")
               + ". Les autres missions sans vis-à-vis, votées sans que la loi d'approbation des comptes leur donne de "
               "montant sous le même identifiant (« votée seule ») ou l'inverse (« exécutée seule »), avec leurs crédits "
               "votés ou ce que cette loi en constate de consommé, en millions d'euros :", "",
               "| Année | Catégorie | Mission ou compte | Rapprochement | Autorisations d'engagement | Crédits de paiement "
               "ou dépenses |", "|---|---|---|---|---|---|"]
    lignes += [f"| {a} | {nom} | {libelles[f]} | {quoi} | {millions(ae)} | {millions(cp)} |"
               for a, nom, f, quoi, ae, cp in autres]
    ecarts.sort(key=lambda x: -abs(x[3] - x[2]))
    lignes += ["", f"Les {GRANDS_ECARTS} plus grands écarts entre les dépenses d'une mission du budget général et ses "
               f"crédits de paiement votés, en milliards d'euros :", "",
               "| Année | Mission | Votés | Dépenses | Écart |", "|---|---|---|---|---|"]
    lignes += [f"| {a} | {libelle} | {md(x)} | {md(y)} | {ecart(x, y)} |" for a, libelle, x, y in ecarts[:GRANDS_ECARTS]]
    lignes.append("")
    return lignes


# 18. Recettes votées et solde voté. Les recettes qu'évalue la loi de finances initiale de chaque année (état A) et
# les soldes que fixe son article d'équilibre, contre ceux que constate la loi d'approbation des comptes de la même
# année (article 1er, et articles 5 et 6 pour chaque budget annexe et compte spécial).
RECETTES_VOTEES = (("Recettes fiscales nettes : votées | exécutées", "LOLF.BG_RECETTES_FISCALES_NETTES"),
                   ("Recettes non fiscales : votées | exécutées", "LOLF.BG_RECETTES_NON_FISCALES"),
                   ("Prélèvements sur recettes : votés | exécutés", "LOLF.BG_PRELEVEMENTS_SUR_RECETTES"))
COMPTES_VOTES = (("Budgets annexes", "LOLF.BA_RECETTES", "LOLF.BA_RECETTES_HORS_FDC"),
                 ("Comptes d'affectation spéciale", "LOLF.CAS_RECETTES", "LOLF.CAS_RECETTES"),
                 ("Comptes de concours financiers", "LOLF.CCF_RECETTES", "LOLF.CCF_RECETTES"))
GRANDS_ECARTS_RECETTES = 10  # comptes cités pour l'écart entre leurs recettes et leur évaluation


def partie_recettes_votees(derniers):
    votes, executes = {}, {}
    for l in derniers.values():
        if l["perimetre_id"] != "ETAT_LF" or valeur(l)[2] != "euros":
            continue
        k = (l["concept_id"], l["fonction_id"], l["periode"])
        if l["concept_id"].endswith("_LFI"):
            if k not in votes or valeur(l)[1] < valeur(votes[k])[1]:
                votes[k] = l  # le montant le plus précis, quand deux tableaux le donnent
        elif l["source_id"].startswith(_LOI[:-1]):
            # La loi d'approbation des comptes de l'exercice, et non une loi suivante qui le rappellerait.
            if k not in executes or l["version"] < executes[k]["version"]:
                executes[k] = l
    v = lambda c, a, f="": valeur(votes[(c + "_LFI", f, a)])[0] if (c + "_LFI", f, a) in votes else None
    e = lambda c, a, f="": valeur(executes[(c, f, a)])[0] if (c, f, a) in executes else None
    annees = sorted({k[2] for k in votes if k[0] == "LOLF.RESULTAT_BUDGETAIRE_LFI"})
    if not annees:
        return []
    md = lambda x: "—" if x is None else fr(x / 1e9, 1)
    ecart = lambda a, b: "—" if a is None or b is None else signe_arrondi((b - a) / 1e9, 1)
    lignes = ["## 18. Recettes votées et solde voté", "",
              f"Les recettes qu'évalue la loi de finances initiale de chaque année, de {annees[0]} à {annees[-1]} (état A), "
              f"et les soldes que fixe son article d'équilibre, contre ce que constate la loi d'approbation des comptes "
              f"de la même année. Une évaluation de recettes n'est pas un plafond : l'écart vient de la conjoncture, des "
              f"mesures votées en cours d'année et de la prévision elle-même. Les recettes fiscales sont nettes des "
              f"remboursements et dégrèvements ; jusqu'à la loi pour 2022, l'état A les évalue brutes, et le tableau de "
              f"l'article d'équilibre donne leur total net, en millions d'euros. L'import vérifie chaque division de "
              f"l'état A contre ses lignes, chaque compte contre ses sections et ses lignes, et les montants du tableau "
              f"d'équilibre entre eux et contre les états A à D, au million près ; la section 2 refait les sommes de "
              f"l'état A.", "", "Budget général, en milliards d'euros :", "",
              "| Année | " + " | ".join(f"{colonnes} | Écart" for colonnes, _ in RECETTES_VOTEES) + " |",
              "|---|" + "---|---|---|" * len(RECETTES_VOTEES)]
    for a in annees:
        lignes.append(f"| {a} | " + " | ".join(f"{md(v(c, a))} | {md(e(c, a))} | {ecart(v(c, a), e(c, a))}"
                                              for _, c in RECETTES_VOTEES) + " |")
    lignes += ["", "Soldes, en milliards d'euros ; jusqu'aux comptes de 2012, le solde général exécuté est le solde "
               "d'exécution des lois de finances, que la loi arrête hors budgets annexes, presque toujours équilibrés :",
               "", "| Année | Solde du budget général : voté | exécuté | Écart | Solde général : voté | exécuté | Écart |",
               "|---|---|---|---|---|---|---|"]
    for a in annees:
        bg_v, bg_e = v("LOLF.SOLDE_BUDGET_GENERAL", a), e("LOLF.SOLDE_BUDGET_GENERAL", a)
        sg_v = v("LOLF.RESULTAT_BUDGETAIRE", a)
        sg_e = e("LOLF.RESULTAT_BUDGETAIRE", a)
        sg_e = e("LOLF.RESULTAT_EXECUTION", a) if sg_e is None else sg_e
        lignes.append(f"| {a} | {md(bg_v)} | {md(bg_e)} | {ecart(bg_v, bg_e)} | {md(sg_v)} | {md(sg_e)} | "
                      f"{ecart(sg_v, sg_e)} |")
    lignes += ["", "Budgets annexes (fonds de concours compris) et comptes spéciaux : recettes votées contre recettes "
               "exécutées, en milliards d'euros :", "",
               "| Année | " + " | ".join(f"{nom} : votées | exécutées" for nom, _, _ in COMPTES_VOTES) + " |",
               "|---|" + "---|---|" * len(COMPTES_VOTES)]
    for a in annees:
        lignes.append(f"| {a} | " + " | ".join(f"{md(v(c, a))} | {md(e(c, a))}" for _, c, _ in COMPTES_VOTES) + " |")
    # Compte par compte, pour les années dont les comptes sont arrêtés : les recettes de chaque budget annexe (hors
    # fonds de concours) et de chaque compte spécial, sous l'identifiant que leur donnent les lois d'approbation des
    # comptes.
    arretees = [a for a in annees if e("LOLF.RESULTAT_BUDGETAIRE", a) is not None
                or e("LOLF.RESULTAT_EXECUTION", a) is not None]
    libelles = {f["id"]: f["libelle"] for f in lire("tables/fonctions.csv")}
    parents = {f["id"]: f["parent_id"] for f in lire("tables/fonctions.csv")}
    ecarts, comptes, absents = [], 0, collections.defaultdict(list)
    for nom, _, c in COMPTES_VOTES:
        for (k, f, a) in votes:
            if k != c + "_LFI" or not f or parents.get(f) != "" or a not in arretees:
                continue
            comptes += 1
            x, y = v(c, a, f), e(c, a, f)
            if y is None:
                absents[libelles.get(f, f)].append((a, x))
            else:
                ecarts.append((a, nom, libelles.get(f, f), x, y))
    ecarts.sort(key=lambda t: -abs(t[4] - t[3]))
    autres = [f"« {compte} » ({plage([a for a, _ in l])}{', évaluées à zéro' if not any(x for _, x in l) else ''})"
              for compte, l in sorted(absents.items(), key=lambda t: (-len(t[1]), t[0]))]
    lignes += ["", f"Compte par compte : {fr(len(ecarts), 0)} des {fr(comptes, 0)} recettes de budgets annexes et de comptes "
               f"spéciaux votées pour les années dont les comptes sont arrêtés, de {arretees[0]} à {arretees[-1]}, se "
               f"retrouvent, sous le même identifiant, dans la loi d'approbation des comptes de l'année."
               + (f" Les {fr(comptes - len(ecarts), 0)} autres n'y ont pas de recettes sous cet identifiant : "
                  f"{', '.join(autres[:-1]) + ' et ' if len(autres) > 1 else ''}{autres[-1]}." if autres else "")
               + f" Les {GRANDS_ECARTS_RECETTES} plus grands écarts entre les recettes d'un compte et leur évaluation, "
               f"en milliards d'euros :", "", "| Année | Catégorie | Compte | Votées | Exécutées | Écart |",
               "|---|---|---|---|---|---|"]
    lignes += [f"| {a} | {nom} | {libelle} | {md(x)} | {md(y)} | {ecart(x, y)} |"
               for a, nom, libelle, x, y in ecarts[:GRANDS_ECARTS_RECETTES]]
    lignes.append("")
    return lignes


# 19. Financement voté. Le tableau de financement de l'article d'équilibre de chaque loi de finances initiale et le
# plafond de la variation de la dette négociable à plus d'un an, contre le tableau de financement que constate la loi
# d'approbation des comptes de la même année (article 2).
def amortissement_nominal(x):
    """L'amortissement du nominal de la dette à moyen et long termes d'un tableau de financement (concept → montant) :
    sa ligne, depuis 2016 ; à défaut, l'amortissement à moyen et long termes moins les suppléments d'indexation ; à
    défaut, l'amortissement à long terme et à moyen terme ; None si le tableau ne donne aucun amortissement."""
    if "LOLF.AMORTISSEMENT_DETTE_NOMINAL" in x:
        return x["LOLF.AMORTISSEMENT_DETTE_NOMINAL"]
    if "LOLF.AMORTISSEMENT_DETTE_MLT" in x:
        return x["LOLF.AMORTISSEMENT_DETTE_MLT"] - x.get("LOLF.SUPPLEMENTS_INDEXATION", 0)
    if "LOLF.AMORTISSEMENT_DETTE_LT" in x or "LOLF.AMORTISSEMENT_DETTE_MT" in x:
        return x.get("LOLF.AMORTISSEMENT_DETTE_LT", 0) + x.get("LOLF.AMORTISSEMENT_DETTE_MT", 0)
    return None


def partie_financement_vote(derniers):
    votes, executes, versions = collections.defaultdict(dict), collections.defaultdict(dict), {}
    for l in derniers.values():
        if l["perimetre_id"] != "ETAT_LF" or l["unite_id"] != "MD_EUR" or l["fonction_id"]:
            continue
        if l["concept_id"].endswith("_LFI"):
            votes[l["periode"]][l["concept_id"].removesuffix("_LFI")] = valeur(l)[0]
        elif l["source_id"].startswith(_LOI[:-1]):
            # La loi d'approbation des comptes de l'exercice, et non une loi suivante qui le rappellerait.
            k = (l["concept_id"], l["periode"])
            if k not in versions or l["version"] < versions[k]:
                versions[k] = l["version"]
                executes[l["periode"]][l["concept_id"]] = valeur(l)[0]
    annees = sorted(a for a in votes if "LOLF.PLAFOND_VARIATION_DETTE" in votes[a])
    if not annees:
        return []
    md = lambda x: "—" if x is None else fr(x / 1e9, 1)
    variation = lambda x: (x["LOLF.EMISSIONS_DETTE_MLT"] - amortissement_nominal(x)
                           if "LOLF.EMISSIONS_DETTE_MLT" in x and amortissement_nominal(x) is not None else None)
    lignes = ["## 19. Financement voté", "",
              f"Le tableau de financement que prévoit l'article d'équilibre de la loi de finances initiale de chaque année, "
              f"de {annees[0]} à {annees[-1]}, et le plafond qu'elle fixe à la variation nette, appréciée en fin d'année, de "
              f"la dette négociable de l'État d'une durée supérieure à un an, contre le tableau de financement que constate "
              f"la loi d'approbation des comptes de la même année. La variation de la dette est, pour l'un et l'autre, les "
              f"émissions de dette à moyen et long termes, nettes des rachats, moins l'amortissement du nominal de cette "
              f"dette. L'import vérifie que le tableau voté s'additionne, que son déficit est l'opposé du solde général de "
              f"l'article d'équilibre, et que le plafond égale la variation qu'il prévoit. Les lois de finances "
              f"rectificatives, que la base ne lit pas encore, modifient le tableau et relèvent souvent le plafond en "
              f"cours d'année.", "", "En milliards d'euros :", "",
              "| Année | Besoin de financement : voté | exécuté | Émissions de dette à moyen et long termes, nettes des "
              "rachats : votées | exécutées | Variation de la dette à plus d'un an : plafond voté | exécutée |",
              "|---|---|---|---|---|---|---|"]
    au_dessus = []
    for a in annees:
        v, e = votes[a], executes.get(a, {})
        plafond, constatee = v["LOLF.PLAFOND_VARIATION_DETTE"], variation(e)
        # Au-delà des arrondis au dixième de milliard des montants en jeu.
        if constatee is not None and constatee - plafond > 0.05e9 * 4:
            au_dessus.append(a)
        lignes.append(f"| {a} | {md(v.get('LOLF.BESOIN_FINANCEMENT'))} | {md(e.get('LOLF.BESOIN_FINANCEMENT'))} | "
                      f"{md(v.get('LOLF.EMISSIONS_DETTE_MLT'))} | {md(e.get('LOLF.EMISSIONS_DETTE_MLT'))} | {md(plafond)} | "
                      f"{md(constatee)} |")
    executees = [a for a in annees if variation(executes.get(a, {})) is not None]
    lignes += ["", f"Sur les {fr(len(executees), 0)} années dont les comptes sont arrêtés, la variation exécutée dépasse le "
               f"plafond de la loi de finances initiale en {fr(len(au_dessus), 0)} : "
               f"{', '.join(au_dessus[:-1]) + ' et ' if len(au_dessus) > 1 else ''}{au_dessus[-1] if au_dessus else ''}. "
               f"La base ne dit pas si le plafond en vigueur en fin d'année, celui de la dernière loi de finances de "
               f"l'année, a été respecté.", ""]
    return lignes


# 20. Plafonds d'emplois votés : celui des emplois de l'État que fixe l'article d'équilibre de chaque loi de finances
# initiale, sa répartition par ministère et par budget annexe, et ceux des opérateurs, des établissements à autonomie
# financière et des autorités publiques indépendantes. La loi d'approbation des comptes ne constate pas d'emplois.
EMPLOIS_VOTES = ("LOLF.PLAFOND_EMPLOIS_LFI", "LOLF.BG_PLAFOND_EMPLOIS_LFI", "LOLF.BA_PLAFOND_EMPLOIS_LFI",
                 "LOLF.OPERATEURS_PLAFOND_EMPLOIS_LFI", "LOLF.EAF_PLAFOND_EMPLOIS_LFI", "LOLF.API_PLAFOND_EMPLOIS_LFI")


def partie_emplois_votes(derniers):
    v = {}
    for l in derniers.values():
        if l["perimetre_id"] == "ETAT_LF" and l["concept_id"] in EMPLOIS_VOTES and not l["fonction_id"]:
            v[(l["concept_id"], l["periode"], l["unite_id"])] = int(float(l["valeur"]))
    annees = sorted({a for _, a, _ in v})
    if not annees:
        return []
    n = lambda c, a, u="ETPT": "—" if (c, a, u) not in v else fr(v[(c, a, u)], 0)
    etat, bg, ba = EMPLOIS_VOTES[:3]
    ecarts = [(a, v[(etat, a, "ETPT")], v[(bg, a, "ETPT")] + v[(ba, a, "ETPT")]) for a in annees
              if (etat, a, "ETPT") in v and v[(etat, a, "ETPT")] != v[(bg, a, "ETPT")] + v[(ba, a, "ETPT")]]
    lignes = ["## 20. Plafonds d'emplois votés", "",
              f"Les plafonds d'emplois que fixe la loi de finances initiale de chaque année, de {annees[0]} à {annees[-1]} : "
              f"celui des emplois rémunérés par l'État, que fixe l'article d'équilibre et que la seconde partie de la loi "
              f"répartit par ministère et par budget annexe, puis ceux des opérateurs de l'État, des agents de droit local "
              f"des établissements à autonomie financière et des autorités publiques indépendantes. Les emplois de l'État "
              f"et des autorités se comptent en équivalents temps plein travaillé (ETPT), ceux des établissements à "
              f"autonomie financière en équivalents temps plein (ETP), et ceux des opérateurs en ETP jusqu'à la loi pour "
              f"2014, en ETPT depuis. L'import vérifie chaque tableau contre ses lignes et contre la phrase qui l'annonce, "
              f"et la section 2 refait ces sommes. La loi d'approbation des comptes ne constate pas d'emplois : la base n'a "
              f"pas encore les emplois consommés.", "",
              "| Année | État (article d'équilibre) | Budget général | Budgets annexes | Opérateurs (ETP) | Opérateurs (ETPT) "
              "| Établissements à autonomie financière (ETP) | Autorités publiques indépendantes |",
              "|---|---|---|---|---|---|---|---|"]
    for a in annees:
        lignes.append(f"| {a} | {n(etat, a)} | {n(bg, a)} | {n(ba, a)} | {n(EMPLOIS_VOTES[3], a, 'ETP')} | "
                      f"{n(EMPLOIS_VOTES[3], a)} | {n(EMPLOIS_VOTES[4], a, 'ETP')} | {n(EMPLOIS_VOTES[5], a)} |")
    lignes.append("")
    if ecarts:
        lignes += [" ".join(f"Pour {a}, le tableau qui répartit le plafond des emplois de l'État par ministère et par "
                            f"budget annexe en compte {fr(t, 0)}, {fr(abs(t - e), 0)} de {'plus' if t > e else 'moins'} "
                            f"que l'article d'équilibre ({fr(e, 0)}) ; ses lignes en font la somme exacte."
                            for a, e, t in ecarts), ""]
    else:
        lignes += ["Chaque année, le tableau qui répartit le plafond des emplois de l'État en fait la somme exacte.", ""]
    return lignes


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
    listes = listes_collectivites()
    lignes += partie_concordances(derniers) + partie_collectivites(derniers, listes) + partie_organismes(derniers, listes)
    lignes += partie_comptes_individuels(listes) + partie_balances_etat(derniers) + partie_dette_negociable(derniers)
    lignes += partie_protection_sociale(derniers) + partie_budget_vote(derniers) + partie_recettes_votees(derniers)
    lignes += partie_financement_vote(derniers) + partie_emplois_votes(derniers)
    RAPPORT.parent.mkdir(exist_ok=True)
    RAPPORT.write_text("\n".join(lignes).rstrip("\n") + "\n", encoding="utf-8")
    print(f"écrit : {RAPPORT.relative_to(RACINE)}")


if __name__ == "__main__":
    ecrire_rapport(charger())
