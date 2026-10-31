#!/usr/bin/env python3
"""Enregistre dans la base les chiffres d'un projet ou d'une loi d'approbation des comptes de l'État pour une année
(loi de règlement jusqu'aux comptes de 2022, loi relative aux résultats de la gestion et portant approbation des
comptes de l'année depuis), à partir de son texte publié par le Sénat (page HTML archivée).

    python3 outils/importer_lois_resultats.py <fichier_id>

Tableaux pris en charge :
- l'article 1er : résultat budgétaire de l'État, recettes et dépenses du budget général, des budgets annexes
  et des comptes spéciaux ;
- l'article 4 : autorisations d'engagement consommées et dépenses du budget général, par mission et par
  programme, avec les ouvertures et annulations de crédits que la loi y ajoute ;
- les articles 5 et 6 : les mêmes grandeurs pour chaque budget annexe et chaque compte spécial, compte par
  compte et programme par programme, avec les recettes, les majorations de découvert et les soldes des comptes
  spéciaux au 31 décembre, ainsi que les articles qui arrêtent à part les comptes spéciaux clos dans l'année
  (voir lignes_articles_5_6) ;
- l'article 2 : le tableau de financement de l'État, en milliards d'euros ;
- l'article 3 : le compte de résultat et le bilan de l'État, en millions d'euros, en droits constatés ;
- l'article liminaire, depuis les comptes de 2012 : soldes structurel et effectif de l'ensemble des
  administrations publiques et, depuis ceux de 2023, d'autres grandeurs de la programmation des finances
  publiques. Les colonnes de prévision et d'écart n'en sont pas lues.
Un tableau à montants qu'aucun de ces articles ne lit arrête l'import.

Les missions, les budgets annexes, les comptes spéciaux et leurs programmes sont les « fonctions » de la norme
LOLF : l'import les inscrit dans la table des fonctions à leur première apparition, sous un identifiant formé de
leur libellé. Dans l'article 4, une
mission est une ligne en gras, un programme une ligne maigre ou précédée d'un tiret ; un tableau sans gras
distingue ses programmes par le seul tiret. Un en-tête que le tableau répète après un saut de page du texte
imprimé est ignoré. Chaque libellé de ligne et de colonne doit avoir une correspondance
ci-dessous : un libellé inconnu arrête l'import, de même qu'une unité inconnue. Une case vide n'est pas un
chiffre. La version d'un chiffre est la date que le texte porte (enregistrement, transmission ou adoption) ;
les montants exécutés sont définitifs, comme le texte les qualifie, les ajustements de crédits ne reçoivent pas
de statut.
"""

import collections
import difflib
import re
import sys
import unicodedata

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire,
                    lire_tableaux_html, nombre_texte, table_des_chiffres, texte_html)

# Article 1er : libellé de ligne, sous sa forme de reconnaissance (voir cle), → {colonne : concept}. Dans la rubrique
# des budgets annexes, une ligne qui n'est pas ci-dessous est un budget annexe, c'est-à-dire une mission : ses
# colonnes vont dans BUDGET_ANNEXE.
BUDGET_ANNEXE = {"Dépenses": "LOLF.BA_DEPENSES_HORS_FDC", "Recettes": "LOLF.BA_RECETTES_HORS_FDC",
                 "Soldes": "LOLF.BA_SOLDE_HORS_FDC"}
REMBOURSEMENTS = {"Recettes": "LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS", "Dépenses": "LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS"}
# Les comptes de 2006 portent en recettes le solde positif des comptes de commerce et d'opérations monétaires, les
# suivants en dépenses, de signe opposé.
OPERATIONS_MONETAIRES = {"Dépenses": "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_DEPENSES",
                         "Recettes": "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_RECETTES",
                         "Soldes": "LOLF.OPERATIONS_MONETAIRES_SOLDE"}
COMPTES_SPECIAUX = {"Dépenses": "LOLF.CS_DEPENSES", "Recettes": "LOLF.CS_RECETTES", "Soldes": "LOLF.SOLDE_COMPTES_SPECIAUX"}
ARTICLE_1 = {
    "Recettes fiscales brutes": {"Recettes": "LOLF.BG_RECETTES_FISCALES_BRUTES"},
    "À déduire : Remboursements et dégrèvements d’impôts d’État": REMBOURSEMENTS,
    "À déduire : Remboursements et dégrèvements d’impôts": REMBOURSEMENTS,  # libellé des textes jusqu'à 2023
    "Recettes fiscales nettes (a)": {"Recettes": "LOLF.BG_RECETTES_FISCALES_NETTES"},
    "Recettes non fiscales (b)": {"Recettes": "LOLF.BG_RECETTES_NON_FISCALES"},
    "Montant net des recettes hors fonds de concours (c = a + b)": {"Recettes": "LOLF.BG_RECETTES_NETTES_HORS_FDC"},
    "À déduire : Prélèvements sur recettes au profit des collectivités territoriales et de l’Union européenne (d)":
        {"Recettes": "LOLF.BG_PRELEVEMENTS_SUR_RECETTES"},
    "Total net des recettes hors prélèvements sur recettes (e = c - d)": {"Recettes": "LOLF.BG_RECETTES_NETTES_HORS_PSR"},
    "Fonds de concours (f)": {"Recettes": "LOLF.BG_FONDS_DE_CONCOURS_RECETTES"},
    "Montant net des recettes y compris fonds de concours (g = e + f)": {"Recettes": "LOLF.BG_RECETTES_NETTES"},
    "Dépenses brutes hors fonds de concours": {"Dépenses": "LOLF.BG_DEPENSES_BRUTES_HORS_FDC"},
    "Montant net des dépenses (h)": {"Dépenses": "LOLF.BG_DEPENSES_NETTES_HORS_FDC"},
    "Fonds de concours (i)": {"Dépenses": "LOLF.BG_FONDS_DE_CONCOURS_DEPENSES"},
    "Montant net des dépenses y compris fonds de concours (j = h + i)": {"Dépenses": "LOLF.BG_DEPENSES_NETTES"},
    "Total du budget général y compris fonds de concours": {"Dépenses": "LOLF.BG_DEPENSES_NETTES",
                                                            "Recettes": "LOLF.BG_RECETTES_NETTES",
                                                            "Soldes": "LOLF.SOLDE_BUDGET_GENERAL"},
    "Fonds de concours": {"Dépenses": "LOLF.BA_FDC_DEPENSES", "Recettes": "LOLF.BA_FDC_RECETTES",
                          "Soldes": "LOLF.BA_FDC_SOLDE"},
    "Montant des budgets annexes hors fonds de concours": BUDGET_ANNEXE,  # sous-total des textes jusqu'à 2015
    "Total des budgets annexes y compris fonds de concours": {"Dépenses": "LOLF.BA_DEPENSES", "Recettes": "LOLF.BA_RECETTES",
                                                              "Soldes": "LOLF.SOLDE_BUDGETS_ANNEXES"},
    "Comptes d’affectation spéciale": {"Dépenses": "LOLF.CAS_DEPENSES", "Recettes": "LOLF.CAS_RECETTES",
                                       "Soldes": "LOLF.CAS_SOLDE"},
    "Comptes de concours financiers": {"Dépenses": "LOLF.CCF_DEPENSES", "Recettes": "LOLF.CCF_RECETTES",
                                       "Soldes": "LOLF.CCF_SOLDE"},
    "Comptes de commerce (solde)": {"Dépenses": "LOLF.COMPTES_COMMERCE_SOLDE_EN_DEPENSES",
                                    "Recettes": "LOLF.COMPTES_COMMERCE_SOLDE_EN_RECETTES",
                                    "Soldes": "LOLF.COMPTES_COMMERCE_SOLDE"},
    "Comptes d’opérations monétaires hors opérations avec le Fonds monétaire international (solde)": OPERATIONS_MONETAIRES,
    "Comptes d’opérations monétaires hors Fonds monétaire international (solde)": OPERATIONS_MONETAIRES,
    "Total des comptes spéciaux hors opérations avec le Fonds monétaire international": COMPTES_SPECIAUX,
    "Total des comptes spéciaux hors Fonds monétaire international": COMPTES_SPECIAUX,
    "Résultat budgétaire de l’État hors opérations avec le Fonds monétaire international":
        {"Soldes": "LOLF.RESULTAT_BUDGETAIRE"},
    # Jusqu'aux comptes de 2012, le tableau se termine par le solde d'exécution des lois de finances, sans les budgets
    # annexes, présentés en équilibre.
    "Solde d’exécution des lois de finances hors Fonds monétaire international": {"Soldes": "LOLF.RESULTAT_EXECUTION"},
    "À déduire : Prélèvements sur recettes au profit des collectivités territoriales et des Communautés européennes (d)":
        {"Recettes": "LOLF.BG_PRELEVEMENTS_SUR_RECETTES"},
    # Lignes propres aux comptes de 2006 et de 2007.
    "Recettes non fiscales hors fonds de stabilisation des changes (b)": {"Recettes": "LOLF.BG_RECETTES_NON_FISCALES"},
    "Total net des recettes hors fonds de stabilisation des changes hors prélèvements sur recettes (e = c - d)":
        {"Recettes": "LOLF.BG_RECETTES_NETTES_HORS_PSR"},
    "Montant net des recettes hors fonds de stabilisation des changes y compris fonds de concours (g = e + f)":
        {"Recettes": "LOLF.BG_RECETTES_NETTES"},
    "Montant net des dépenses y compris fonds de concours hors mesure de régularisation concernant les pensions "
    "(j’) = (h) + (i)": {"Dépenses": "LOLF.BG_DEPENSES_NETTES_HORS_REGULARISATION_PENSIONS"},
    "Total du budget général y compris fonds de concours hors mesure de régularisation concernant les pensions":
        {"Dépenses": "LOLF.BG_DEPENSES_NETTES_HORS_REGULARISATION_PENSIONS", "Recettes": "LOLF.BG_RECETTES_NETTES",
         "Soldes": "LOLF.SOLDE_BUDGET_GENERAL_HORS_REGULARISATION_PENSIONS"},
    "Solde d’exécution des lois de finances hors Fonds de stabilisation des changes hors Fonds monétaire international":
        {"Soldes": "LOLF.RESULTAT_EXECUTION"},
    "Solde d’exécution des lois de finances hors Fonds de stabilisation des changes hors Fonds monétaire international "
    "et hors mesure de régularisation concernant les pensions":
        {"Soldes": "LOLF.RESULTAT_EXECUTION_HORS_REGULARISATION_PENSIONS"},
    "Solde d’exécution des lois de finances hors Fonds monétaire international et hors produits de cession des titres "
    "EDF": {"Soldes": "LOLF.RESULTAT_EXECUTION_HORS_CESSION_TITRES_EDF"},
}
# Précision qu'un libellé ajoute au concept commun auquel il se rattache, portée par la note du chiffre.
PRECISIONS = {
    "hors fonds de stabilisation des changes": "Le texte de 2006 présente ses recettes non fiscales, et les totaux et "
        "soldes qui en découlent, hors fonds de stabilisation des changes.",
}
RUBRIQUES_ARTICLE_1 = {"Budget général", "Recettes", "Dépenses", "Budgets annexes", "Comptes spéciaux"}

# Article 4 : intitulé de colonne → concept, pour le tableau des autorisations d'engagement et celui des dépenses.
ARTICLE_4 = {
    "Autorisations d’engagement consommées": "LOLF.BG_AE_CONSOMMEES",
    "Autorisations d’engagement engagées": "LOLF.BG_AE_CONSOMMEES",  # libellé des textes jusqu'aux comptes de 2012
    "Ouvertures d’autorisations d’engagement complémentaires": "LOLF.BG_AE_OUVERTURES",
    "Annulations d’autorisations d’engagement non consommées et non reportées": "LOLF.BG_AE_ANNULATIONS",
    "Annulations d’autorisations d’engagement non engagées et non reportées": "LOLF.BG_AE_ANNULATIONS",
    "Dépenses": "LOLF.BG_DEPENSES_BRUTES",
    "Ouvertures de crédits complémentaires": "LOLF.BG_CP_OUVERTURES",
    "Annulations de crédits non consommés et non reportés": "LOLF.BG_CP_ANNULATIONS",
}
NOTE_ASTERISQUE = "Le montant porte un astérisque d’appel de note : la note sous le tableau le précise."
# Libellés fautifs de l'un des deux tableaux de l'article 4, que l'autre donne correctement : (source, libellé) →
# libellé correct. L'emplacement du chiffre garde le libellé de la page.
LIBELLES_CORRIGES = {
    ("senat.pjl15-785", "- Conduite et pilotage des politiques économique et financière"):
        "- Conduite et pilotage des politiques économiques et financières",
    ("senat.pjl24-032", "- Haute Cour. . . . . . . . . . . . . . . . . . . . . . . .u"): "- Haute Cour",
}
# Articles 5 et 6 : budgets annexes et comptes spéciaux, compte par compte. Intitulé de colonne → mesure ; le concept
# d'un chiffre est « LOLF.<catégorie>_<mesure> ».
MESURES = {
    "Autorisations d’engagement consommées": "AE_CONSOMMEES",
    "Autorisations d’engagement engagées": "AE_CONSOMMEES",
    "Autorisations d’engagement": "AE_CONSOMMEES",
    "Ouvertures d’autorisations d’engagement complémentaires": "AE_OUVERTURES",
    "Annulations d’autorisations d’engagement non consommées et non reportées": "AE_ANNULATIONS",
    "Annulations d’autorisations d’engagement non engagées et non reportées": "AE_ANNULATIONS",
    "Dépenses": "DEPENSES",
    "Recettes": "RECETTES",
    "Ouvertures de crédits complémentaires": "CP_OUVERTURES",
    "Annulations de crédits non consommés et non reportés": "CP_ANNULATIONS",
    "Annulations des crédits non consommés et non reportés": "CP_ANNULATIONS",
    "Annulations des crédits non consommés et non reportes": "CP_ANNULATIONS",
    "Majorations du découvert": "MAJORATIONS_DECOUVERT",
    "Débiteurs": "SOLDES_DEBITEURS",
    "Débiteur": "SOLDES_DEBITEURS",
    "Créditeurs": "SOLDES_CREDITEURS",
    "Créditeur": "SOLDES_CREDITEURS",
}
# Rubriques des comptes spéciaux → catégorie. Les comptes de commerce et d'opérations monétaires n'ont pas de programmes.
CATEGORIES = {"Comptes d’affectation spéciale": "CAS", "Comptes de concours financiers": "CCF",
              "Comptes de commerce": "COMPTES_COMMERCE", "Comptes d’opérations monétaires": "OPERATIONS_MONETAIRES",
              "Compte de commerce": "COMPTES_COMMERCE"}  # au singulier dans le tableau d'un compte clos
SANS_PROGRAMMES = {"COMPTES_COMMERCE", "OPERATIONS_MONETAIRES"}
# Lignes d'un budget annexe qui ne sont pas des programmes mais des composantes de son total → libellé retenu.
COMPOSANTES_BUDGET_ANNEXE = {"Augmentation du fonds de roulement": "Augmentation du fonds de roulement",
                             "Augmentation du fonds de roulement (ligne d’équilibre)": "Augmentation du fonds de roulement",
                             "Fonds de concours": "Fonds de concours"}
# Regroupements des textes jusqu'aux comptes de 2010 : comptes dotés de crédits, comptes dotés de découverts. Le total
# général d'un tableau porte sur les catégories qu'il présente.
GROUPES = {"crédits": "CS_A_CREDITS", "découvert": "CS_A_DECOUVERT"}
TOTAUX_GENERAUX = {frozenset({"CAS", "CCF"}): "CS_A_CREDITS", frozenset({"COMPTES_COMMERCE", "OPERATIONS_MONETAIRES"}): "CS_A_DECOUVERT",
                   frozenset(CATEGORIES.values()): "CS_ENSEMBLE"}
# Mesures de chaque catégorie : les comptes à crédits (budgets annexes, comptes d'affectation spéciale, de concours
# financiers) ont des autorisations d'engagement et des crédits, les comptes à découvert (de commerce, d'opérations
# monétaires) des découverts. Une mesure hors de sa catégorie arrête l'import.
MESURES_A_CREDITS = {"AE_CONSOMMEES", "AE_OUVERTURES", "AE_ANNULATIONS", "DEPENSES", "RECETTES", "CP_OUVERTURES",
                     "CP_ANNULATIONS", "SOLDES_DEBITEURS", "SOLDES_CREDITEURS"}
MESURES_A_DECOUVERT = {"DEPENSES", "RECETTES", "MAJORATIONS_DECOUVERT", "SOLDES_DEBITEURS", "SOLDES_CREDITEURS"}
# Intitulés de colonne que le texte contredit : (source, catégorie, intitulé) → (intitulé retenu, explication).
NOTE_2022 = ("Le texte présente les comptes de commerce et d’opérations monétaires sous l’en-tête des comptes dotés de "
             "crédits (« Annulations de crédits non consommés et non reportés »), dans la page du Sénat comme dans le "
             "texte imprimé. Ces comptes sont dotés de découverts et non de crédits, et l’article 6 dit que les "
             "découverts autorisés sont modifiés comme l’indiquent ses tableaux : le montant est une majoration du "
             "découvert, comme les autres années.")
COLONNES_CONTREDITES = {
    ("senat.pjl22-684", "COMPTES_COMMERCE", "Annulations de crédits non consommés et non reportés"):
        ("Majorations du découvert", NOTE_2022),
    ("senat.pjl22-684", "OPERATIONS_MONETAIRES", "Annulations de crédits non consommés et non reportés"):
        ("Majorations du découvert", NOTE_2022),
}
# Le texte de 2006 présente les budgets annexes de l'article 5 hors fonds de concours, les suivants fonds de concours
# compris : les identifiants partagés avec l'article 1er et les ventilations le vérifient.
BUDGETS_ANNEXES_HORS_FDC = {"senat.pjl06-389"}
MESURES_AJUSTEMENTS = {"AE_OUVERTURES", "AE_ANNULATIONS", "CP_OUVERTURES", "CP_ANNULATIONS", "MAJORATIONS_DECOUVERT"}
MESURES_SOLDES = {"SOLDES_DEBITEURS", "SOLDES_CREDITEURS"}

AJUSTEMENTS = {"LOLF.BG_AE_OUVERTURES", "LOLF.BG_AE_ANNULATIONS", "LOLF.BG_CP_OUVERTURES", "LOLF.BG_CP_ANNULATIONS"}
SOLDES = {c for lignes in ARTICLE_1.values() for colonne, c in lignes.items() if colonne == "Soldes"} | {"LOLF.BA_SOLDE_HORS_FDC"}

# Unité annoncée en tête de tableau, « (En euros) » par exemple.
UNITES = {"en euros": "EUR", "en millions d’euros": "MIO_EUR", "en milliards d’euros": "MD_EUR"}
# Unités annoncées que les montants du tableau contredisent : (source, intitulé de sa première colonne de montants,
# unité annoncée) → (unité des montants, explication portée par chacun d'eux).
UNITES_CONTREDITES = {
    ("senat.pjl24-032", "Autorisations d’engagement consommées", "en millions d’euros"): (
        "EUR", "Le tableau annonce des millions d’euros, dans la page du Sénat comme dans le texte imprimé, mais ses "
               "montants sont en euros : ils ont des centimes, et leur total (590 784 984 819,29) est du même ordre "
               "que celui des dépenses du tableau suivant, annoncé en euros (591 887 384 714,81)."),
}


# Articles liminaire, 2 et 3. Un libellé s'y reconnaît à sa forme (voir forme) : sans majuscules ni accents, sans
# appel de note, numéro de ligne en chiffres romains ni « total » en tête, les années remplacées par « n ».

# Article liminaire, depuis les comptes de 2012 : soldes structurel et effectif de l'ensemble des administrations
# publiques et, depuis ceux de 2023, d'autres grandeurs de la programmation des finances publiques. Libellé →
# (concept, périmètre, unité quand le libellé l'annonce, consolidation, traitements).
LIMINAIRE = {
    "Solde structurel": ("PFP.SOLDE_STRUCTUREL", "S13", None, "sans_objet", ""),
    "Solde structurel (en points de produit intérieur brut potentiel)":
        ("PFP.SOLDE_STRUCTUREL", "S13", "PC_PIB_POTENTIEL", "sans_objet", ""),
    "Solde conjoncturel": ("PFP.SOLDE_CONJONCTUREL", "S13", None, "sans_objet", ""),
    "Mesures ponctuelles et temporaires": ("PFP.MESURES_PONCTUELLES_TEMPORAIRES", "S13", None, "sans_objet", ""),
    "Mesures temporaires et ponctuelles": ("PFP.MESURES_PONCTUELLES_TEMPORAIRES", "S13", None, "sans_objet", ""),
    "Solde des mesures ponctuelles et temporaires (en points de produit intérieur brut potentiel)":
        ("PFP.MESURES_PONCTUELLES_TEMPORAIRES", "S13", "PC_PIB_POTENTIEL", "sans_objet", ""),
    "Solde effectif (1 + 2 + 3)": ("SEC2010.B9", "S13", None, "sans_objet", ""),
    "Solde effectif (1+2+3)": ("SEC2010.B9", "S13", None, "sans_objet", ""),
    "Dette au sens de Maastricht": ("PDE.GD", "S13", None, "consolide", ""),
    "Taux de prélèvements obligatoires (y compris Union européenne, nets des crédits d’impôt)":
        ("INSEE_PO.PO", "S13_S212", None, "sans_objet", ""),
    "Dépense publique (hors crédits d’impôt)": ("SEC2010.TE", "S13", None, "consolide", "hors_credits_impot"),
    "Dépense publique (hors crédits d’impôt, en milliards d’euros)":
        ("SEC2010.TE", "S13", "MD_EUR", "consolide", "hors_credits_impot"),
    "Dépense publique ((hors crédits d’impôt, en milliards d’euros)":  # sic, comptes de 2024
        ("SEC2010.TE", "S13", "MD_EUR", "consolide", "hors_credits_impot"),
    "Évolution de la dépense publique (hors crédits d’impôt en volume ( %))":
        ("SEC2010.TE", "S13", "PC_EVOLUTION", "consolide", "hors_credits_impot;volume_champ_constant"),
    "Évolution de la dépense publique hors CI en volume ( %)":
        ("SEC2010.TE", "S13", "PC_EVOLUTION", "consolide", "hors_credits_impot;volume_champ_constant"),
    "Évolution de la dépense publique hors crédits d’impôt en volume (en %)":
        ("SEC2010.TE", "S13", "PC_EVOLUTION", "consolide", "hors_credits_impot;volume_champ_constant"),
    "Principales dépenses d’investissement (en milliards d’euros)":
        ("PFP.PRINCIPALES_DEPENSES_INVESTISSEMENT", "S13", "MD_EUR", "non_precise", ""),
}
UNITES_LIMINAIRE = {"en points de produit intérieur brut": "PC_PIB", "en points de produit intérieur brut - pib": "PC_PIB",
                    "en % du pib sauf mention contraire": "PC_PIB", "en % du pib, sauf mention contraire": "PC_PIB"}
# Colonnes d'exécution autres que la première, qui mesurent les soldes selon une autre méthode : (source, intitulé
# de la colonne) → traitement. Les colonnes de prévision (loi de finances de l'année, loi de programmation) et
# d'écart ne sont pas lues : ces prévisions ont pour source les lois qui les ont votées.
METRIQUES = {
    ("senat.pjl14-642", "Exécution 2014 : Métrique de la loi de programmation des finances publiques 2012-2017"):
        "metrique_lpfp_2012_2017",
    ("senat.pjl16-643", "Exécution 2016 (**)"): "croissance_potentielle_lpfp_2014_2019",
}
COLONNES_PREVISION = ("prevision", "soldes prevus", "ecart", "loi de finances", "loi de programmation", "n-n")
# L'article liminaire reprend les comptes nationaux de l'année, que l'Insee publie au printemps suivant et qui restent
# provisoires jusqu'au printemps d'après, donc à la date du texte ; ses soldes structurel et conjoncturel et ses
# mesures ponctuelles et temporaires sont des estimations, qui dépendent du PIB potentiel retenu.
ESTIMATIONS_LIMINAIRE = {"PFP.SOLDE_STRUCTUREL", "PFP.SOLDE_CONJONCTUREL", "PFP.MESURES_PONCTUELLES_TEMPORAIRES"}

# Article 2 : tableau de financement, en milliards d'euros. (Rubrique, libellé) → concept ; une ligne « dont » est
# une partie de la ligne qui la précède.
FINANCEMENT = {
    ("besoin", "Amortissement de la dette à long terme"): "LOLF.AMORTISSEMENT_DETTE_LT",
    ("besoin", "Amortissement de la dette à long terme (y compris rachats de titres d’échéance 2009 avant leur maturité)"):
        "LOLF.AMORTISSEMENT_DETTE_LT",
    ("besoin", "Dont amortissement de la dette à long terme"): "LOLF.AMORTISSEMENT_DETTE_LT",
    ("besoin", "Amortissement de la dette à moyen terme"): "LOLF.AMORTISSEMENT_DETTE_MT",
    ("besoin", "Amortissement de la dette à moyen terme (y compris rachats de titres d’échéance 2009 avant leur maturité)"):
        "LOLF.AMORTISSEMENT_DETTE_MT",
    ("besoin", "Dont amortissement de la dette à moyen terme"): "LOLF.AMORTISSEMENT_DETTE_MT",
    ("besoin", "Amortissement de la dette à moyen et long termes"): "LOLF.AMORTISSEMENT_DETTE_MLT",
    ("besoin", "Dont amortissement nominal de la dette à moyen et long termes"): "LOLF.AMORTISSEMENT_DETTE_NOMINAL",
    ("besoin", "Dont remboursement du nominal à valeur faciale"): "LOLF.AMORTISSEMENT_DETTE_NOMINAL",
    ("besoin", "Dont suppléments d’indexation versés à l’échéance (titres indexés)"): "LOLF.SUPPLEMENTS_INDEXATION",
    ("besoin", "Amortissement de dettes reprises par l’État"): "LOLF.AMORTISSEMENT_DETTES_REPRISES",
    ("besoin", "Amortissement SNCF Réseau"): "LOLF.AMORTISSEMENT_SNCF_RESEAU",
    ("besoin", "Amortissement des autres dettes"): "LOLF.AMORTISSEMENT_AUTRES_DETTES",
    ("besoin", "Engagements de l’État"): "LOLF.ENGAGEMENTS_ETAT",
    ("besoin", "Impact en trésorerie du solde de la gestion 2006"): "LOLF.IMPACT_TRESORERIE_SOLDE_GESTION",
    ("besoin", "Déficit à financer"): "LOLF.DEFICIT_A_FINANCER",
    ("besoin", "Déficit budgétaire"): "LOLF.DEFICIT_A_FINANCER",  # comptes de 2015
    ("besoin", "Dont déficit budgétaire"): "LOLF.DEFICIT_A_FINANCER_DEFICIT_BUDGETAIRE",
    ("besoin", "Dont dotation budgétaire du deuxième programme d’investissements d’avenir"):
        "LOLF.DEFICIT_A_FINANCER_DOTATION_PIA",
    ("besoin", "Variation des dépôts de garantie"): "LOLF.VARIATION_DEPOTS_GARANTIE",
    ("besoin", "Variation d’autres besoins de trésorerie"): "LOLF.VARIATION_AUTRES_BESOINS_TRESORERIE",
    ("besoin", "Autres besoins de trésorerie"): "LOLF.AUTRES_BESOINS_TRESORERIE",
    ("besoin", "Total du besoin de financement"): "LOLF.BESOIN_FINANCEMENT",
    ("besoin", "Total"): "LOLF.BESOIN_FINANCEMENT",
    ("ressources", "Émissions à moyen et long termes (obligations assimilables du Trésor et bons du Trésor à taux fixe et "
                   "intérêts annuels), nettes des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émissions à moyen et long terme (obligations assimilables du Trésor et bons du Trésor à taux fixe et "
                   "intérêts annuels), nettes des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émissions à moyen et long terme (obligations assimilables du Trésor et bons du Trésor à taux fixe et "
                   "intérêts annuels), nettes des rachats en nominal"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émissions de dette à moyen et long termes, nettes des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émission de dette à moyen et long termes, nettes des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émission de dette à moyen et long terme, nettes des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Annulation de titres de l’État par la Caisse de la dette publique"): "LOLF.ANNULATION_TITRES_CDP",
    ("ressources", "Ressources affectées à la Caisse de la dette publique et consacrées au désendettement"):
        "LOLF.RESSOURCES_CDP",
    ("ressources", "Variation nette des bons du Trésor à taux fixe et intérêts précomptés"):
        "LOLF.VARIATION_TITRES_COURT_TERME",
    ("ressources", "Variation des bons du Trésor à taux fixe et intérêts précomptés"): "LOLF.VARIATION_TITRES_COURT_TERME",
    ("ressources", "Variation nette de l’encours des titres d’État à court terme"): "LOLF.VARIATION_TITRES_COURT_TERME",
    ("ressources", "Variation des dépôts des correspondants"): "LOLF.VARIATION_DEPOTS_CORRESPONDANTS",
    ("ressources", "Variation des dépôts des correspondants (EPIC, EPA, collectivités territoriales)"):
        "LOLF.VARIATION_DEPOTS_CORRESPONDANTS",
    ("ressources", "Variation des dépôts des correspondants (EPIC, EPA, collectivités territoriales) et assimilés"):
        "LOLF.VARIATION_DEPOTS_CORRESPONDANTS",
    ("ressources", "Variation des correspondants"): "LOLF.VARIATION_DEPOTS_CORRESPONDANTS",
    ("ressources", "Variation d’avances de trésorerie"): "LOLF.VARIATION_AVANCES_TRESORERIE",
    ("ressources", "Variation du compte du Trésor et divers"): "LOLF.VARIATION_COMPTE_TRESOR",
    ("ressources", "Variation du compte du Trésor"): "LOLF.VARIATION_COMPTE_TRESOR",
    ("ressources", "Variation du solde du compte du Trésor"): "LOLF.VARIATION_COMPTE_TRESOR",
    ("ressources", "Variation du solde du compte du Trésor et assimilé"): "LOLF.VARIATION_COMPTE_TRESOR",
    ("ressources", "Variation des disponibilités du Trésor à la Banque de France et des placements de trésorerie de "
                   "l’État"): "LOLF.VARIATION_DISPONIBILITES_TRESOR",
    ("ressources", "Autres ressources de trésorerie"): "LOLF.AUTRES_RESSOURCES_TRESORERIE",
    ("ressources", "Autres ressources nettes de trésorerie"): "LOLF.AUTRES_RESSOURCES_TRESORERIE",
    ("ressources", "Total des ressources de financement"): "LOLF.RESSOURCES_FINANCEMENT",
    ("ressources", "Total"): "LOLF.RESSOURCES_FINANCEMENT",
}
RUBRIQUES_FINANCEMENT = {"Besoin de financement": "besoin", "Ressources de financement": "ressources"}
SOLDES_FINANCEMENT = {"LOLF.IMPACT_TRESORERIE_SOLDE_GESTION", "LOLF.DEFICIT_A_FINANCER",
                      "LOLF.DEFICIT_A_FINANCER_DEFICIT_BUDGETAIRE", "LOLF.DEFICIT_A_FINANCER_DOTATION_PIA"}

# Article 3 : compte de résultat (tableaux des charges nettes, des produits régaliens nets et de détermination du
# solde des opérations de l'exercice) et bilan, en millions d'euros. Libellé → concept, ou rubrique → concept pour
# les libellés que plusieurs rubriques emploient.
RUBRIQUES_RESULTAT = {"Charges de fonctionnement nettes": "fonctionnement", "Charges d’intervention nettes": "intervention",
                      "Charges financières nettes": "financier", "Produits régaliens nets": "regalien",
                      "Tableau des produits régaliens nets": "regalien", "Solde des opérations de l’exercice": "solde",
                      "Tableau de détermination du solde des opérations de l’exercice": "solde",
                      "Charges nettes": "charges", "Tableau des charges nettes": "charges"}
_E = "COMPTES_ETAT."
RESULTAT = {
    "Charges de personnel": _E + "CHARGES_PERSONNEL",
    "Achats, variations de stocks et prestations externes": _E + "ACHATS_PRESTATIONS_EXTERNES",
    "Dotations aux amortissements, aux provisions et aux dépréciations": {"fonctionnement": _E + "DOTATIONS_FONCTIONNEMENT",
                                                                          "financier": _E + "DOTATIONS_FINANCIERES"},
    "Autres charges de fonctionnement": _E + "AUTRES_CHARGES_FONCTIONNEMENT",
    "Total des charges de fonctionnement direct": _E + "CHARGES_FONCTIONNEMENT_DIRECT",
    "Subventions pour charges de service public": _E + "SUBVENTIONS_CHARGES_SERVICE_PUBLIC",
    "Dotations aux provisions": _E + "DOTATIONS_FONCTIONNEMENT_INDIRECT",
    "Autres charges de fonctionnement indirect": _E + "AUTRES_CHARGES_FONCTIONNEMENT_INDIRECT",
    "Total des charges de fonctionnement indirect": _E + "CHARGES_FONCTIONNEMENT_INDIRECT",
    "Total des charges de fonctionnement": _E + "CHARGES_FONCTIONNEMENT",
    "Ventes de produits et prestations de service": _E + "VENTES_PRESTATIONS",
    "Ventes de produits et prestations de services": _E + "VENTES_PRESTATIONS",
    "Production stockée et immobilisée": _E + "PRODUCTION_STOCKEE_IMMOBILISEE",
    "Production stockée immobilisée": _E + "PRODUCTION_STOCKEE_IMMOBILISEE",
    "Reprises sur provisions et sur dépréciations": {"fonctionnement": _E + "REPRISES_FONCTIONNEMENT",
                                                     "intervention": _E + "REPRISES_INTERVENTION",
                                                     "financier": _E + "REPRISES_FINANCIERES"},
    "Autres produits de fonctionnement": _E + "AUTRES_PRODUITS_FONCTIONNEMENT",
    "Total des produits de fonctionnement": _E + "PRODUITS_FONCTIONNEMENT",
    "Charges de fonctionnement nettes": _E + "CHARGES_FONCTIONNEMENT_NETTES",
    "Transferts aux ménages": _E + "TRANSFERTS_MENAGES",
    "Transferts aux entreprises": _E + "TRANSFERTS_ENTREPRISES",
    "Transferts aux collectivités territoriales": _E + "TRANSFERTS_COLLECTIVITES_TERRITORIALES",
    "Transferts aux autres collectivités": _E + "TRANSFERTS_AUTRES_COLLECTIVITES",
    "Charges résultant de la mise en jeu de garanties": _E + "CHARGES_GARANTIES",
    "Dotations aux provisions et aux dépréciations": _E + "DOTATIONS_INTERVENTION",
    "Total des charges d’intervention": _E + "CHARGES_INTERVENTION",
    "Contributions reçues de tiers": _E + "CONTRIBUTIONS_TIERS",
    "Total des produits d’intervention": _E + "PRODUITS_INTERVENTION",
    "Charges d’intervention nettes": _E + "CHARGES_INTERVENTION_NETTES",
    "Intérêts": _E + "INTERETS",
    "Pertes de change liées aux opérations financières": _E + "PERTES_CHANGE",
    "Autres charges financières": _E + "AUTRES_CHARGES_FINANCIERES",
    "Total des charges financières": _E + "CHARGES_FINANCIERES",
    "Produits des créances de l’actif immobilisé": _E + "PRODUITS_CREANCES_ACTIF_IMMOBILISE",
    "Produits des immobilisations financières": _E + "PRODUITS_IMMOBILISATIONS_FINANCIERES",
    "Gains de change liés aux opérations financières": _E + "GAINS_CHANGE",
    "Gains de change liés aux opérations financière": _E + "GAINS_CHANGE",  # sic, comptes de 2007
    "Autres intérêts et produits assimilés": _E + "AUTRES_INTERETS_PRODUITS",
    "Total des produits financiers": _E + "PRODUITS_FINANCIERS",
    "Charges financières nettes": _E + "CHARGES_FINANCIERES_NETTES",
    "Charges nettes": _E + "CHARGES_NETTES",
    "Impôt sur le revenu": _E + "IMPOT_REVENU",
    "Impôt sur les sociétés": _E + "IMPOT_SOCIETES",
    "Taxe sur les salaires": _E + "TAXE_SALAIRES",
    "Taxe intérieure sur les produits pétroliers": _E + "TICPE",
    "Taxe intérieure de consommation sur les produits énergétiques": _E + "TICPE",
    "Taxe sur la valeur ajoutée": _E + "TVA",
    "Enregistrement, timbre, autres contributions et taxes indirectes": _E + "ENREGISTREMENT_TIMBRE",
    "Autres produits de nature fiscale et assimilés": _E + "AUTRES_PRODUITS_FISCAUX",
    "Produits fiscaux nets": _E + "PRODUITS_FISCAUX_NETS",
    "Amendes, prélèvements divers et autres pénalités": _E + "AMENDES",
    "Autres produits régaliens nets": _E + "AUTRES_PRODUITS_REGALIENS_NETS",
    "Ressource propre de l’Union européenne basée sur le produit national brut": _E + "RESSOURCE_PROPRE_UE_RNB",
    "Ressource propre de l’Union européenne basée sur le revenu national brut": _E + "RESSOURCE_PROPRE_UE_RNB",
    "Ressources propres de l’Union européenne basée sur le revenu national brut": _E + "RESSOURCE_PROPRE_UE_RNB",
    "Ressource propre de l’Union européenne basée sur la taxe sur la valeur ajoutée": _E + "RESSOURCE_PROPRE_UE_TVA",
    "Ressources propres de l’Union européenne basée sur la taxe sur la valeur ajoutée": _E + "RESSOURCE_PROPRE_UE_TVA",
    "Ressources propres de l’Union européenne basées sur le produit national brut et la taxe sur la valeur ajoutée":
        _E + "RESSOURCES_PROPRES_UE",
    "Ressources propres de l’Union européenne basées sur le revenu national brut et la taxe sur la valeur ajoutée":
        _E + "RESSOURCES_PROPRES_UE",
    "Ressources propres du budget de l’Union européenne basées sur le produit national brut et la taxe sur la valeur "
    "ajoutée": _E + "RESSOURCES_PROPRES_UE",
    "Ressources propres du budget de l’Union européenne basées sur le revenu national brut et la taxe sur la valeur "
    "ajoutée": _E + "RESSOURCES_PROPRES_UE",
    "Ressources propres de l’Union européenne": _E + "RESSOURCES_PROPRES_UE",
    "Ressources propres du budget de l’Union européenne": _E + "RESSOURCES_PROPRES_UE",
    "Prélèvement sur les recettes de l’État au profit de l’Union européenne": _E + "RESSOURCES_PROPRES_UE",
    "Produits régaliens nets": _E + "PRODUITS_REGALIENS_NETS",
    "Solde des opérations de l’exercice": _E + "SOLDE_OPERATIONS_EXERCICE",
}
# Bilan : (côté, libellé) → concept du montant net ; le brut et les amortissements et dépréciations d'une ligne de
# l'actif ont le même concept, suivi de _BRUT ou _AMORTISSEMENTS. Le côté change après le total de l'actif, puis après
# celui du passif.
BILAN = {
    ("actif", "Immobilisations incorporelles"): _E + "IMMOBILISATIONS_INCORPORELLES",
    ("actif", "Immobilisations corporelles"): _E + "IMMOBILISATIONS_CORPORELLES",
    ("actif", "Immobilisations financières"): _E + "IMMOBILISATIONS_FINANCIERES",
    ("actif", "Total actif immobilisé"): _E + "ACTIF_IMMOBILISE",
    ("actif", "Stocks"): _E + "STOCKS",
    ("actif", "Créances"): _E + "CREANCES",
    ("actif", "Redevables"): _E + "CREANCES_REDEVABLES",
    ("actif", "Redevable s"): _E + "CREANCES_REDEVABLES",  # sic, comptes de 2006
    ("actif", "Clients"): _E + "CREANCES_CLIENTS",
    ("actif", "Autres créances"): _E + "AUTRES_CREANCES",
    ("actif", "Charges constatées d’avance"): _E + "CHARGES_CONSTATEES_AVANCE",
    ("actif", "Total actif circulant (hors trésorerie)"): _E + "ACTIF_CIRCULANT",
    ("actif", "Disponibilités"): _E + "DISPONIBILITES",
    ("actif", "Fonds bancaires et fonds en caisse"): _E + "FONDS_BANCAIRES_CAISSE",
    ("actif", "Valeurs escomptées, en cours d’encaissement et de décaissement"): _E + "VALEURS_ESCOMPTEES",
    ("actif", "Autres composantes de trésorerie"): _E + "AUTRES_COMPOSANTES_TRESORERIE",
    ("actif", "Équivalents de trésorerie"): _E + "EQUIVALENTS_TRESORERIE",
    ("actif", "Valeurs mobilières de placement"): _E + "VALEURS_MOBILIERES_PLACEMENT",
    ("actif", "Total trésorerie"): _E + "TRESORERIE_ACTIF",
    ("actif", "Comptes de régularisation"): _E + "COMPTES_REGULARISATION_ACTIF",
    ("actif", "Total actif"): _E + "ACTIF",
    ("passif", "Titres négociables"): _E + "TITRES_NEGOCIABLES",
    ("passif", "Titres non négociables"): _E + "TITRES_NON_NEGOCIABLES",
    ("passif", "Autres emprunts"): _E + "AUTRES_EMPRUNTS",
    ("passif", "Dettes financières et autres emprunts"): _E + "DETTES_FINANCIERES_AUTRES_EMPRUNTS",
    ("passif", "Total dettes financières"): _E + "DETTES_FINANCIERES",
    ("passif", "Dettes de fonctionnement"): _E + "DETTES_FONCTIONNEMENT",
    ("passif", "Dettes d’intervention"): _E + "DETTES_INTERVENTION",
    ("passif", "Produits constatés d’avance"): _E + "PRODUITS_CONSTATES_AVANCE",
    ("passif", "Autres dettes non financières"): _E + "AUTRES_DETTES_NON_FINANCIERES",
    ("passif", "Total dettes non financières"): _E + "DETTES_NON_FINANCIERES",
    ("passif", "Provisions pour risques"): _E + "PROVISIONS_RISQUES",
    ("passif", "Provisions pour charges"): _E + "PROVISIONS_CHARGES",
    ("passif", "Total provisions pour risques et charges"): _E + "PROVISIONS_RISQUES_CHARGES",
    ("passif", "Autres passifs (hors trésorerie)"): _E + "AUTRES_PASSIFS",
    ("passif", "Correspondants du Trésor et personnes habilitées"): _E + "CORRESPONDANTS_TRESOR",
    ("passif", "Autres"): _E + "AUTRES_TRESORERIE_PASSIF",
    ("passif", "Total trésorerie"): _E + "TRESORERIE_PASSIF",
    ("passif", "Comptes de régularisation"): _E + "COMPTES_REGULARISATION_PASSIF",
    ("passif", "Total passif (hors situation nette)"): _E + "PASSIF",
    ("situation", "Report des exercices antérieurs"): _E + "REPORT_EXERCICES_ANTERIEURS",
    ("situation", "Solde des opérations d’exercices antérieurs en attente d’affectation"):
        _E + "SOLDE_EXERCICES_ANTERIEURS_ATTENTE",
    ("situation", "Écarts de réévaluation et d’intégration"): _E + "ECARTS_REEVALUATION_INTEGRATION",
    ("situation", "Solde des opérations de l’exercice"): _E + "SOLDE_EXERCICE_BILAN",
    ("situation", "Situation nette"): _E + "SITUATION_NETTE",
}
RUBRIQUES_BILAN = {"Actif immobilisé", "Actif circulant (hors trésorerie)", "Trésorerie", "Dettes financières",
                   "Dettes non financières (hors trésorerie)", "Provisions pour risques et charges"}
MESURES_BILAN = {"brut": "_BRUT", "net": ""}  # et toute colonne qui commence par « amortissement » : _AMORTISSEMENTS

# Année des comptes : la seule que le texte désigne par « budget de l'année » ou « comptes de l'année ».
ANNEE = r"(?:budget|comptes) de l[’'] ?année ([0-9]{4})"


def propre(texte):
    """Libellé sans points de conduite, avec un seul type de tiret et d'apostrophe."""
    texte = texte.replace("–", "-").replace("−", "-").replace("'", "’")
    return re.sub(r"^(\s*\.)+|(\s*\.)+\s*$", "", texte).strip()


def cle(libelle):
    """Forme d'un libellé qui sert à le reconnaître : ponctuation et formules écrites d'une seule façon.
    « Montant net des recettes, hors fonds de concours (c) = (a) + (b) » se reconnaît comme
    « Montant net des recettes hors fonds de concours (c = a + b) »."""
    texte = re.sub(r"\s*,\s+(hors|y compris)\b", r" \1", re.sub(r"\s*:\s*", " : ", libelle))
    texte = re.sub(r"\s+", " ", texte).strip()
    formule = re.search(r"\(([a-z]) ?\) ?= ?((?:\([a-z] ?\) ?[-+] ?)+\([a-z] ?\))$", texte)
    if formule:
        termes = re.sub(r" ?([-+]) ?", r" \1 ", re.sub(r"\(([a-z]) ?\)", r"\1", formule.group(2)))
        texte = f"{texte[:formule.start()]}({formule.group(1)} = {termes})"
    return texte


def code_lolf(libelle):
    """Identifiant formé d'un libellé : « Action extérieure de l’État » → ACTION_EXTERIEURE_DE_LETAT ; les ligatures
    s'écrivent en deux lettres (« œuvres » → OEUVRES)."""
    ligatures = {"œ": "oe", "Œ": "OE", "æ": "ae", "Æ": "AE"}
    ascii_ = unicodedata.normalize("NFKD", re.sub("[œŒæÆ]", lambda m: ligatures[m.group(0)], libelle))
    ascii_ = ascii_.encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "_", ascii_.upper()).strip("_")


def unite_annoncee(texte):
    trouve = re.fullmatch(r"\((en [^)*]+)\*?\)", propre(texte), re.I)
    return trouve.group(1).lower() if trouve else None


def colonnes(tableau, entete, largeurs):
    """Intitulé de chaque colonne : le dernier texte non vide des lignes d'en-tête qui la couvre, unité exceptée."""
    noms = {}
    for r, ligne in enumerate(tableau[:entete]):
        for c, texte in enumerate(ligne):
            if propre(texte) and c > 0 and unite_annoncee(texte) is None:
                for dc in range(largeurs.get((r, c), 1)):
                    noms[c + dc] = propre(texte)
    return noms


def unite(tableau, entete, noms, forme, source_id):
    """(unité, note) des montants d'un tableau, d'après l'unité annoncée dans ses lignes d'en-tête ou, à défaut, dans
    sa légende."""
    annoncees = {unite_annoncee(x) for l in tableau[:entete] for x in l} - {None} or \
        {unite_annoncee(forme["legende"])} - {None}
    if len(annoncees) != 1 or next(iter(annoncees)) not in UNITES:
        sys.exit(f"tableau « {noms.get(1)} » : unité annoncée inconnue ou absente ({annoncees or 'aucune'})")
    annoncee = next(iter(annoncees))
    return UNITES_CONTREDITES.get((source_id, noms.get(1), annoncee), (UNITES[annoncee], ""))


def montants(tableau, entete, noms, largeurs):
    """(ligne, colonne, nombre) de chaque montant sous l'en-tête ; une case à cheval sur deux colonnes d'intitulés
    différents arrête l'import."""
    for r in range(entete, len(tableau)):
        for c, x in enumerate(tableau[r]):
            nombre = nombre_texte(x) if c > 0 else None
            if c > 0 and not nombre and re.search(r"[0-9]", x):
                sys.exit(f"tableau « {noms.get(1)} », ligne {r} : montant illisible (« {x} »)")
            if not nombre:
                continue
            if len({noms.get(c + dc) for dc in range(largeurs.get((r, c), 1))}) > 1:
                sys.exit(f"tableau « {noms.get(1)} », ligne {r} : case à cheval sur deux colonnes")
            yield r, c, nombre


def article_1(tableaux):
    """(indice, tableau) de l'article 1er : celui qui se termine par le résultat budgétaire, ou jusqu'aux comptes de
    2012 par le solde d'exécution des lois de finances."""
    for i, t in enumerate(tableaux):
        if any(propre(l[0]).startswith(("Résultat budgétaire de l’État", "Solde d’exécution des lois de finances"))
               for l in t if l):
            return i, t
    sys.exit("tableau de l'article 1er introuvable")


def lignes_article_1(i, tableau, forme, source_id):
    """Un libellé coupé sur deux lignes, dont la seconde commence par une minuscule et la première ne porte aucun
    montant, se lit d'un seul tenant quand il a ainsi une correspondance ; une ligne sans libellé qui porte des
    montants, sous un libellé connu qui n'en porte aucun, prend ce libellé. Un montant pris dans une case fusionnée sur plusieurs lignes, dont le texte
    reste dans la première, va à la seule ligne du bloc dont le libellé a une correspondance pour sa colonne ;
    l'emplacement reste celui de la case."""
    entete = next(r for r, l in enumerate(tableau) if "Soldes" in [propre(x) for x in l]) + 1
    noms = colonnes(tableau, entete, forme["largeurs"])
    unite_, note_unite = unite(tableau, entete, noms, forme, source_id)
    libelles, rubriques, rubrique, decales = {}, {}, "", set()
    for r in range(entete, len(tableau)):
        libelle, precedent = propre(tableau[r][0]), libelles.get(r - 1, "")
        precedent_vide = r > entete and not any(nombre_texte(x) for x in tableau[r - 1][1:])
        if not libelle and cle(precedent) in ARTICLE_1 and precedent_vide and any(nombre_texte(x) for x in tableau[r][1:]):
            libelle = precedent
            decales.add(r)
        elif libelle[:1].islower() and cle(f"{precedent} {libelle}") in ARTICLE_1 and precedent_vide:
            libelle = f"{precedent} {libelle}"
        libelles[r] = libelle
        rubrique = cle(libelle) if cle(libelle) in RUBRIQUES_ARTICLE_1 else rubrique
        rubriques[r] = rubrique

    def correspondance(r):
        if cle(libelles[r]) in ARTICLE_1:
            return ARTICLE_1[cle(libelles[r])], ""
        if rubriques[r] == "Budgets annexes" and libelles[r] and cle(libelles[r]) not in RUBRIQUES_ARTICLE_1 and \
                not libelles[r].lower().startswith(("total", "fonds", "dont")):
            return BUDGET_ANNEXE, (libelles[r], "")
        return {}, ""

    for r, c, nombre in montants(tableau, entete, noms, forme["largeurs"]):
        bloc = range(r, r + forme["fusions"].get((r, c), 1))
        cibles = [s for s in bloc if noms.get(c) in correspondance(s)[0]]
        if len(cibles) != 1:
            sys.exit(f"article 1er, ligne {r}, colonne « {noms.get(c)} » : {len(cibles)} correspondance(s) pour "
                     f"« {' / '.join(libelles[s] for s in bloc)} »")
        concepts, fonction = correspondance(cibles[0])
        notes = [f"Case fusionnée sur les lignes {r} à {bloc[-1]} du tableau ; le montant est celui de la seule ligne "
                 f"chiffrée du bloc." if len(bloc) > 1 else "",
                 "Montant porté une ligne sous son libellé." if cibles[0] in decales else "", note_unite]
        notes += [n for motif, n in PRECISIONS.items() if motif in cle(libelles[cibles[0]]).lower()]
        yield {"tableau": i, "ligne": r, "colonne": c, "libelle": libelles[cibles[0]], "intitule": noms[c],
               "concept": concepts[noms[c]], "fonction": fonction, "nombre": nombre, "unite": unite_,
               "note": " ".join(n for n in notes if n)}


def lignes_article_4(tableaux, formes, source_id, recolle):
    """Les deux tableaux de l'article 4, autorisations d'engagement puis dépenses, listent les mêmes missions et
    programmes dans le même ordre : chaque ligne doit désigner la même fonction dans l'un et l'autre, et une ligne en
    gras dans l'un est une mission dans les deux."""
    numeros = [i for i, t in enumerate(tableaux) if t and any(propre(x).startswith("Désignation des missions")
                                                               for l in t[:3] for x in l)]
    if len(numeros) != 2:
        sys.exit(f"article 4 : {len(numeros)} tableau(x) de missions au lieu de deux")
    lus = []
    for i in numeros:
        t, forme = tableaux[i], formes[i]
        entete = next(r for r, l in enumerate(t) if any("Ouvertures" in x for x in l)) + 1
        noms = colonnes(t, entete, forme["largeurs"])
        textes_entete = {propre(x) for l in t[:entete] for x in l if propre(x)}
        # Une ligne vide, ou un en-tête répété après un saut de page du texte imprimé, ne compte pas.
        lignes = [r for r in range(entete, len(t)) if propre(t[r][0]) and
                  not {propre(x) for x in t[r] if propre(x)} <= textes_entete]
        lus.append({"i": i, "t": t, "forme": forme, "entete": entete, "noms": noms, "lignes": lignes,
                    "unite": unite(t, entete, noms, forme, source_id)})
    if len(lus[0]["lignes"]) != len(lus[1]["lignes"]):
        sys.exit(f"article 4 : {len(lus[0]['lignes'])} lignes dans un tableau, {len(lus[1]['lignes'])} dans l'autre")
    gras_present = any((r, 0) in lu["forme"]["gras"] for lu in lus for r in lu["lignes"])
    structure, mission = [], None
    for position, rangs in enumerate(zip(*(lu["lignes"] for lu in lus))):
        bruts = [propre(lu["t"][r][0]) for lu, r in zip(lus, rangs)]
        nets = [recolle(re.sub(r"^[-+]+\s*", "", LIBELLES_CORRIGES.get((source_id, b), b))) for b in bruts]
        if code_lolf(nets[0]) != code_lolf(nets[1]):
            sys.exit(f"article 4, ligne {position + 1} : « {bruts[0]} » d'un côté, « {bruts[1]} » de l'autre")
        tiret = any(b.startswith(("-", "+")) for b in bruts)
        gras = any((r, 0) in lu["forme"]["gras"] for lu, r in zip(lus, rangs))
        if nets[0].lower().startswith("total"):
            if nets[0].lower() != "total":
                sys.exit(f"article 4, ligne {position + 1} : total inattendu (« {bruts[0]} »)")
            structure.append("")
        elif tiret and gras:
            sys.exit(f"article 4, ligne {position + 1} : ligne en gras précédée d'un tiret (« {bruts[0]} »)")
        elif gras or not (gras_present or tiret):
            mission = nets[0]
            structure.append((nets[0], ""))
        elif mission is None:
            sys.exit(f"article 4, ligne {position + 1} : programme hors mission (« {bruts[0]} »)")
        else:
            structure.append((nets[0], mission))
    for lu in lus:
        types = dict(zip(lu["lignes"], structure))
        unite_, note = lu["unite"]
        for r, c, nombre in montants(lu["t"], lu["entete"], lu["noms"], lu["forme"]["largeurs"]):
            if r not in types:
                sys.exit(f"article 4, tableau {lu['i']}, ligne {r} : montant sans libellé")
            if lu["noms"].get(c) not in ARTICLE_4:
                sys.exit(f"article 4, tableau {lu['i']}, ligne {r} : colonne « {lu['noms'].get(c)} » sans correspondance")
            yield {"tableau": lu["i"], "ligne": r, "colonne": c, "libelle": propre(lu["t"][r][0]),
                   "intitule": lu["noms"][c], "concept": ARTICLE_4[lu["noms"][c]], "fonction": types[r],
                   "nombre": nombre, "unite": unite_, "note": note}


def est_entete(cellules):
    """Une ligne d'en-tête : tous ses textes sont la désignation, l'unité ou des intitulés de colonne."""
    textes = [propre(c) for c in cellules if propre(c)]
    return bool(textes) and all(t in MESURES or unite_annoncee(t) or t.startswith(
        ("Désignation", "des comptes spéciaux", "des budgets annexes", "Ajustements de la loi", "Opérations de l’année",
         "Soldes au 31 décembre", "Solde au 31 décembre")) for t in textes)


def famille(tableau, forme):
    """BA (budgets annexes), CS (comptes spéciaux) ou CLOS (compte spécial clos, arrêté par un article à part)."""
    designation = next(propre(c) for l in tableau[:4] for c in l if propre(c).startswith("Désignation"))
    legende = forme["legende"]
    if "compte spécial" in designation or re.search(r"\b(?:du|sur le) compte spécial\b", legende):
        return "CLOS"
    for texte in (designation, legende):
        if "budgets annexes" in texte:
            return "BA"
        if re.search(r"comptes spécia", texte):
            return "CS"
    sys.exit(f"tableau « {designation} » : budgets annexes ou comptes spéciaux ?")


def segments_de_comptes(tableaux, formes, source_id):
    """Les tableaux des articles 5 et 6, découpés en segments : chacun sous son bloc d'en-tête, car une même grille
    en réunit parfois deux. Un tableau sans désignation, dont l'en-tête ne porte que des intitulés de colonne de ces
    articles, prolonge le tableau de comptes qui le précède. Un tableau à montants sans en-tête qui suit un tableau de
    comptes, sans texte entre eux, le prolonge aussi, sur les mêmes colonnes : la page de 2008 coupe ainsi en trois,
    sans en répéter l'en-tête, le tableau des autorisations d'engagement des comptes spéciaux. Un autre tableau à
    montants entre deux tableaux de comptes arrête l'import. Les tableaux d'un compte spécial clos dans l'année, que
    le texte arrête à part, forment la famille CLOS."""
    segments, precedente, lus, ignores = [], None, [], []
    for i, t in enumerate(tableaux):
        if not t:
            continue
        suite, a_montants = None, any(nombre_texte(x) for l in t for x in l[1:])
        if any(propre(c).startswith("Désignation") and "missions" not in propre(c) for l in t[:4] for c in l):
            fam = famille(t, formes[i])
        elif precedente and est_entete(t[0]) and any(propre(c) in MESURES for l in t[:4] if est_entete(l) for c in l):
            fam = precedente
        elif a_montants and segments and segments[-1]["i"] == i - 1 and not formes[i]["legende"] and not est_entete(t[0]):
            suite, fam = segments[-1], precedente
            if len(t[0]) != len(suite["t"][0]):
                sys.exit(f"tableau {i} : suite sans en-tête du tableau {i - 1}, sur {len(t[0])} colonnes au lieu de "
                         f"{len(suite['t'][0])}")
        else:
            if a_montants:
                ignores.append(i)
            continue
        precedente = fam
        lus.append(i)
        bloc, unite_tableau = [], suite and suite["unite"]
        courant = {**suite, "i": i, "t": t, "forme": formes[i], "lignes": []} if suite else None
        for r, ligne in enumerate(t):
            if est_entete(ligne):
                if courant is not None:
                    segments.append(courant)
                    courant, bloc = None, []
                bloc.append(r)
            elif any(propre(c) for c in ligne):
                if courant is None:
                    if not bloc:
                        sys.exit(f"tableau {i}, ligne {r} : montants sans en-tête")
                    noms = colonnes(t[bloc[0]:bloc[-1] + 1], bloc[-1] - bloc[0] + 1,
                                    {(rr - bloc[0], c): l for (rr, c), l in formes[i]["largeurs"].items()})
                    mesures = {MESURES[n] for n in noms.values() if n in MESURES}
                    genre = "AE" if any(m.startswith("AE_") for m in mesures) else \
                        "SOLDES" if mesures & MESURES_SOLDES else "OPERATIONS"
                    # L'unité annoncée en tête du tableau vaut pour tous ses segments.
                    entete_ = t[bloc[0]:bloc[-1] + 1]
                    if bloc[0] > 0 and not any(unite_annoncee(c) for l in entete_ for c in l) and unite_tableau:
                        unite_ = unite_tableau
                    else:
                        unite_ = unite(entete_, len(entete_), noms, formes[i] if bloc[0] == 0 else
                                       {**formes[i], "legende": ""}, source_id)
                    unite_tableau = unite_tableau or unite_
                    courant = {"famille": fam, "genre": genre, "i": i, "t": t, "forme": formes[i], "noms": noms,
                               "unite": unite_, "lignes": []}
                courant["lignes"].append(r)
        if courant is not None:
            segments.append(courant)
    entre = [i for i in ignores if lus and lus[0] < i < lus[-1]]
    if entre:
        sys.exit(f"tableaux {entre} : montants entre deux tableaux de comptes, ni en-tête ni suite d'un tableau")
    return segments


def structure_des_comptes(segs, fam, recolle, source_id):
    """Les lignes d'un tableau de comptes (segments d'une même famille et d'un même genre), avec leur rôle : rubrique
    de catégorie, total, composante d'un budget annexe, ou ligne de compte ou de programme, à départager ensuite."""
    lignes, categorie = [], "BA" if fam == "BA" else None
    for seg in segs:
        t = seg["t"]
        for r in seg["lignes"]:
            brut = propre(t[r][0])
            chiffres = any(nombre_texte(x) for x in t[r][1:])
            if not brut:
                if chiffres:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : montants sans libellé")
                continue
            cle_ = cle(brut)
            groupe = re.fullmatch(r"(?i)(?:[ab]\.?\s*-?\s*)?comptes à (crédits|découvert)", cle_)
            total = re.fullmatch(r"(?i)tota(?:l|ux)(?: (?:des?|du) | )?(.*)", cle_)
            if fam in ("CS", "CLOS") and cle_ in CATEGORIES:
                categorie = CATEGORIES[cle_]
                lignes.append({"seg": seg, "r": r, "role": "rubrique", "cible": categorie})
            elif groupe:
                if chiffres:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : montants sur la rubrique « {brut} »")
            elif total:
                reste = total.group(1).lower()
                cibles = {k.lower(): v for k, v in CATEGORIES.items()}
                if reste in cibles:
                    cible = cibles[reste]
                elif reste == "budgets annexes" and fam == "BA":
                    cible = "BA"
                elif re.fullmatch(r"comptes à (crédits|découvert)", reste):
                    cible = GROUPES[reste.split()[-1]]
                elif reste in ("", "général", "comptes spéciaux"):
                    cible = "BA" if fam == "BA" else None  # total général, fixé d'après les rubriques présentes
                else:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : total inattendu (« {brut} »)")
                lignes.append({"seg": seg, "r": r, "role": "total", "cible": cible})
            elif categorie is None or re.match(r"(?i)tota", cle_):
                sys.exit(f"tableau {seg['i']}, ligne {r} : compte hors rubrique ou total inconnu (« {brut} »)")
            elif fam == "BA" and cle_ in COMPOSANTES_BUDGET_ANNEXE:
                lignes.append({"seg": seg, "r": r, "role": "composante", "categorie": categorie, "brut": brut,
                               "net": COMPOSANTES_BUDGET_ANNEXE[cle_]})
            else:
                lignes.append({"seg": seg, "r": r, "role": "ligne", "categorie": categorie, "brut": brut,
                               "tiret": brut.startswith(("-", "+")), "gras": (r, 0) in seg["forme"]["gras"],
                               "net": recolle(re.sub(r"^(?:[-+]+|\d+\.\s*-)\s*", "",
                                                     LIBELLES_CORRIGES.get((source_id, brut), brut)))})
    presentes = frozenset(l["cible"] for l in lignes if l["role"] == "rubrique")
    for l in lignes:
        if l["role"] == "total" and l["cible"] is None:
            if fam == "CLOS" and len(presentes) == 1:
                l["cible"] = next(iter(presentes))
            elif presentes in TOTAUX_GENERAUX:
                l["cible"] = TOTAUX_GENERAUX[presentes]
            else:
                sys.exit(f"tableau {l['seg']['i']}, ligne {l['r']} : total général de {sorted(presentes)}")
    return lignes


def proches(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= 0.85


def apparier(a, b, quoi):
    """Les lignes de deux tableaux qui se correspondent, alignées dans l'ordre : (ligne de a, ligne de b) ; une ligne
    que l'autre tableau ne présente pas reste seule. Deux lignes appariées doivent avoir des libellés presque
    identiques ; un remplacement de plusieurs lignes par un autre nombre de lignes arrête l'import."""
    cles = lambda lignes: [(l["categorie"], code_lolf(l["net"])) for l in lignes]
    paires = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, cles(a), cles(b), autojunk=False).get_opcodes():
        if op == "equal" or op == "replace" and i2 - i1 == j2 - j1:
            for x, y in zip(a[i1:i2], b[j1:j2]):
                if x["categorie"] != y["categorie"] or not proches(x["net"], y["net"]):
                    sys.exit(f"{quoi} : « {x['brut']} » d'un côté, « {y['brut']} » de l'autre")
                paires.append((x, y))
        elif op == "replace":
            sys.exit(f"{quoi} : {[l['brut'] for l in a[i1:i2]]} d'un côté, {[l['brut'] for l in b[j1:j2]]} de l'autre")
        else:
            paires += [(x,) for x in a[i1:i2]] + [(y,) for y in b[j1:j2]]
    return paires


def lignes_articles_5_6(tableaux, formes, source_id, recolle):
    """Budgets annexes (article 5) et comptes spéciaux (article 6), compte par compte et programme par programme.
    Les segments d'une même famille (budgets annexes ou comptes spéciaux) et d'un même genre (autorisations
    d'engagement, opérations de l'année, soldes au 31 décembre) forment un seul tableau, dont les rubriques donnent la
    catégorie des comptes.

    Les budgets annexes, comptes d'affectation spéciale et comptes de concours financiers ont des programmes ; leurs
    tableaux des autorisations d'engagement et des opérations présentent les mêmes lignes, que l'on départage
    ensemble : une ligne précédée d'un tiret dans l'un ou l'autre est un programme ; sinon, une ligne en gras dans l'un
    ou l'autre est un compte, de même qu'une ligne maigre quand les programmes de sa catégorie portent un tiret ; le
    reste, ce sont des programmes. Une même ligne y prend le libellé du tableau des opérations, à condition que les deux
    libellés soient presque identiques ; une ligne que l'un des deux tableaux ne présente pas y reste seule.
    L'augmentation du fonds de roulement et les fonds de concours d'un budget annexe en sont des composantes, à côté de
    ses programmes. Les comptes de commerce et d'opérations monétaires n'ont pas de programmes, ni le tableau des
    soldes, dont chaque compte prend de même le libellé du tableau des opérations."""
    tables = {}
    for seg in segments_de_comptes(tableaux, formes, source_id):
        tables.setdefault((seg["famille"], seg["genre"]), []).append(seg)
    structures = {cle_: structure_des_comptes(segs, cle_[0], recolle, source_id) for cle_, segs in tables.items()}
    for fam in ("BA", "CS", "CLOS"):
        ae, operations = structures.get((fam, "AE"), []), structures.get((fam, "OPERATIONS"), [])
        a = [l for l in ae if l["role"] == "ligne"]
        b = [l for l in operations if l["role"] == "ligne" and l["categorie"] not in SANS_PROGRAMMES]
        tirets = {l["categorie"] for l in a + b if l["tiret"]}
        for paire in apparier(a, b, f"{fam}, autorisations d'engagement et opérations"):
            if any(l["tiret"] for l in paire):
                if any(l["tiret"] and l["gras"] for l in paire):
                    sys.exit(f"{fam} : ligne en gras précédée d'un tiret (« {paire[0]['brut']} »)")
                role = "programme"
            else:
                role = "compte" if any(l["gras"] for l in paire) or paire[0]["categorie"] in tirets else "programme"
            for l in paire:
                l["role"], l["net"] = role, paire[-1]["net"]
    for (fam, genre), lignes in structures.items():
        for l in lignes:
            if l["role"] == "ligne":
                l["role"] = "compte"  # comptes de commerce et d'opérations monétaires, soldes
        compte = None
        for l in lignes:
            if l["role"] in ("rubrique", "total"):
                compte = None
            elif l["role"] == "compte":
                compte, l["fonction"] = l["net"], (l["net"], "")
            elif compte is None:
                sys.exit(f"tableau {l['seg']['i']}, ligne {l['r']} : {l['role']} hors compte (« {l['brut']} »)")
            else:
                l["fonction"] = (l["net"], compte)
    for fam in ("BA", "CS", "CLOS"):
        comptes_op = [l for l in structures.get((fam, "OPERATIONS"), []) if l["role"] == "compte"]
        comptes_so = [l for l in structures.get((fam, "SOLDES"), []) if l["role"] == "compte"]
        for paire in apparier(comptes_so, comptes_op, f"{fam}, soldes et opérations"):
            if len(paire) == 2:
                paire[0]["net"], paire[0]["fonction"] = paire[1]["net"], (paire[1]["net"], "")
    # Les comptes clos dans l'année sont des comptes de leur catégorie ; les totaux de l'article 6 ne portent alors
    # que sur les comptes qui se poursuivent (« hors comptes clos »), ceux des tableaux des comptes clos sur ces seuls
    # comptes. Le rapport de cohérence ne peut pas rapprocher ces totaux de leurs comptes, qui portent le concept de
    # leur catégorie : chacun doit égaler la somme des comptes de son tableau qu'il couvre.
    clos = {l["categorie"] for (fam, genre), lignes in structures.items() if fam == "CLOS" for l in lignes
            if l["role"] in ("compte", "programme")}
    touches = clos | ({"CS_A_CREDITS"} if clos & {"CAS", "CCF"} else set()) | \
        ({"CS_A_DECOUVERT"} if clos & SANS_PROGRAMMES else set()) | ({"CS_ENSEMBLE"} if clos else set())
    composition = {v: k for k, v in TOTAUX_GENERAUX.items()}
    sommes, a_verifier = collections.defaultdict(float), []
    for (fam, genre), lignes in structures.items():
        for l in lignes:
            seg, r = l["seg"], l["r"]
            t, noms, largeurs = seg["t"], seg["noms"], seg["forme"]["largeurs"]
            for c, x in enumerate(t[r]):
                nombre = nombre_texte(x) if c > 0 else None
                if c > 0 and not nombre and re.search(r"[0-9]", x):
                    sys.exit(f"tableau {seg['i']}, ligne {r} : montant illisible (« {x} »)")
                if not nombre:
                    continue
                if len({noms.get(c + dc) for dc in range(largeurs.get((r, c), 1))}) > 1:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : case à cheval sur deux colonnes")
                if noms.get(c) not in MESURES:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : colonne « {noms.get(c)} » sans correspondance")
                if l["role"] in ("rubrique", "total"):
                    categorie, fonction = l["cible"], ""
                else:
                    categorie, fonction = l["categorie"], l["fonction"]
                intitule, note_colonne = COLONNES_CONTREDITES.get((source_id, categorie, noms[c]), (noms[c], ""))
                mesure = MESURES[intitule]
                if mesure not in (MESURES_A_DECOUVERT if categorie in SANS_PROGRAMMES | {"CS_A_DECOUVERT"} else
                                  MESURES_A_CREDITS):
                    if float(nombre[0]) == 0:
                        continue  # un zéro dans une colonne étrangère à la catégorie n'en est pas un chiffre
                    sys.exit(f"tableau {seg['i']}, ligne {r} : « {noms[c]} » pour la catégorie {categorie}")
                concept = f"LOLF.{categorie}_{mesure}"
                if categorie == "BA" and source_id in BUDGETS_ANNEXES_HORS_FDC and mesure in ("DEPENSES", "RECETTES"):
                    concept += "_HORS_FDC"
                if l["role"] in ("rubrique", "total") and (fam == "CLOS" or categorie in touches):
                    concept += "_COMPTES_CLOS" if fam == "CLOS" else "_HORS_COMPTES_CLOS"
                    a_verifier.append((seg["i"], r, fam, genre, categorie, mesure, float(nombre[0])))
                elif l["role"] == "compte":
                    sommes[(fam, genre, categorie, mesure)] += float(nombre[0])
                unite_, note = seg["unite"]
                note = " ".join(n for n in (note, note_colonne, NOTE_ASTERISQUE if "*" in x else "") if n)
                yield {"tableau": seg["i"], "ligne": r, "colonne": c, "libelle": propre(t[r][0]), "intitule": noms[c],
                       "concept": concept, "fonction": fonction, "nombre": nombre, "unite": unite_, "note": note,
                       "ajustement": mesure in MESURES_AJUSTEMENTS, "solde": mesure in MESURES_SOLDES}
    for i, r, fam, genre, categorie, mesure, valeur in a_verifier:
        somme = sum(sommes[(fam, genre, c, mesure)] for c in composition.get(categorie, {categorie}))
        if abs(valeur - somme) > 0.005:
            sys.exit(f"tableau {i}, ligne {r} : total {valeur:.2f}, somme des comptes qu'il couvre {somme:.2f}")


def forme(libelle):
    """Forme d'un libellé des articles liminaire, 2 et 3 qui sert à le reconnaître : « TOTAL DES CHARGES FINANCIÈRES
    NETTES (XI = IX - X) » se reconnaît comme « Charges financières nettes »."""
    t = unicodedata.normalize("NFKD", propre(libelle).replace("’", "'").lower()).encode("ascii", "ignore").decode()
    t = re.sub(r"\([ivx]+(?:\s*[=+-]\s*[ivx]+)*\)|\(\d\)|\(\*+\)|\*", " ", t)
    t = re.sub(r"\b(?:19|20)[0-9]{2}\b", "n", t)
    t = re.sub(r"\(\s+", "(", re.sub(r"\s+\)", ")", re.sub(r"[\s.:]+", " ", t))).strip(" ,")
    return re.sub(r"^total(?: des| du| de la| de l'| d')? ", "", t)


def par_forme(dictionnaire):
    """Le même dictionnaire, ses libellés remplacés par leur forme ; deux libellés de même forme doivent y
    désigner la même chose."""
    formes = {}
    for cle_, valeur in dictionnaire.items():
        f = (cle_[0], forme(cle_[1])) if isinstance(cle_, tuple) else forme(cle_)
        if formes.setdefault(f, valeur) != valeur:
            sys.exit(f"libellés de même forme qui diffèrent : {cle_}")
    return formes


LIMINAIRE_ = par_forme(LIMINAIRE)
FINANCEMENT_ = par_forme(FINANCEMENT)
RUBRIQUES_FINANCEMENT_ = par_forme(RUBRIQUES_FINANCEMENT)
RESULTAT_ = par_forme(RESULTAT)
RUBRIQUES_RESULTAT_ = par_forme(RUBRIQUES_RESULTAT)
BILAN_ = par_forme(BILAN)
RUBRIQUES_BILAN_ = {forme(r) for r in RUBRIQUES_BILAN}
APPEL = r"\([0-9]\)|\(\*+\)|\*+"


def textes(ligne):
    """Les textes d'une ligne qui ne sont pas des montants."""
    return [propre(x) for x in ligne if propre(x) and not nombre_texte(x)]


def montants_de(ligne):
    """{colonne : nombre} des montants d'une ligne, hors première colonne."""
    return {c: n for c, x in enumerate(ligne) if c > 0 and (n := nombre_texte(x))}


def notes_du_tableau(tableau):
    """{appel : texte} des notes d'un tableau : les lignes qui commencent par un appel (« (1) », « * », « (**) »),
    une ligne pouvant en réunir plusieurs."""
    notes = {}
    for ligne in tableau:
        texte = " ".join(textes(ligne))
        if re.match(APPEL, texte) and not montants_de(ligne):
            for appel, contenu in re.findall(rf"({APPEL})\s*(.+?)(?=\s+(?:\([0-9]\)|\(\*+\))\s|$)", texte):
                notes[appel] = contenu
    return notes


def note_des_appels(appels, notes):
    """La note de chaque appel, celle du tableau ou, s'il n'y en a pas, un renvoi au texte."""
    return " ".join(dict.fromkeys(notes.get(a) or f"Appel de note {a} : la note se trouve dans le texte, hors du tableau."
                                  for a in appels))


def entetes(tableau, lignes, largeurs):
    """Intitulés de chaque colonne : les textes des lignes d'en-tête qui la couvrent, de haut en bas, unités exceptées."""
    noms = collections.defaultdict(list)
    for r in lignes:
        for c, texte in enumerate(tableau[r]):
            if c > 0 and propre(texte) and unite_annoncee(propre(texte).rstrip(" *")) is None:
                for dc in range(largeurs.get((r, c), 1)):
                    noms[c + dc].append(propre(texte))
    return noms


def unites_annoncees(tableau, forme_):
    """Les unités qu'un tableau annonce dans ses lignes ou, à défaut, dans sa légende."""
    return {unite_annoncee(propre(x).rstrip(" *")) for l in tableau for x in l} - {None} or \
        {unite_annoncee(forme_["legende"])} - {None}


def genre_de_tableau(tableau):
    """liminaire, financement, bilan ou resultat ; None si le tableau n'est d'aucun de ces genres."""
    formes = {forme(t) for l in tableau for t in textes(l)}
    if any(f.startswith("solde structurel") for f in formes):
        return "liminaire"
    if "besoin de financement" in formes:
        return "financement"
    if any(f in ("actif immobilise", "actif") for f in formes):
        return "bilan"
    if formes & set(RESULTAT_):
        return "resultat"
    return None


def lignes_article_liminaire(i, tableau, forme_, annee, source_id):
    """Les lignes d'en-tête précèdent la première ligne de grandeur. La première colonne d'exécution porte la mesure
    principale ; les autres doivent figurer dans METRIQUES. Les appels de note des libellés, qui se confondent avec le
    numéro des composantes du solde effectif, ne sont pas suivis ; ceux des intitulés de colonne et des montants le
    sont. Statut : voir ESTIMATIONS_LIMINAIRE."""
    debut = next((r for r, l in enumerate(tableau) if l and forme(l[0]) in LIMINAIRE_), None)
    if debut is None:
        sys.exit(f"article liminaire, tableau {i} : aucune grandeur reconnue")
    annoncees = unites_annoncees(tableau[:debut], forme_)
    if len(annoncees) != 1 or next(iter(annoncees)) not in UNITES_LIMINAIRE:
        sys.exit(f"article liminaire : unité annoncée inconnue ou absente ({annoncees or 'aucune'})")
    unite_tableau = UNITES_LIMINAIRE[next(iter(annoncees))]
    appels_unite = [a for l in tableau[:debut] for x in l if unite_annoncee(propre(x).rstrip(" *"))
                    for a in re.findall(APPEL, propre(x).split(")")[-1])]
    noms = entetes(tableau, range(debut), forme_["largeurs"])
    notes = notes_du_tableau(tableau[debut:])
    executions = [c for c in sorted(noms) if any(forme(n).startswith("execution") for n in noms[c])]
    for c in sorted(noms):
        if c not in executions and not any(forme(n).startswith(COLONNES_PREVISION) for n in noms[c]):
            sys.exit(f"article liminaire : colonne « {' '.join(noms[c])} » inconnue")
    if not executions or not any(re.search(rf"\b{annee}\b", " ".join(noms[c])) for c in executions[:1]):
        sys.exit(f"article liminaire : pas de colonne d'exécution de {annee}")
    for r in range(debut, len(tableau)):
        ligne, libelle = tableau[r], propre(tableau[r][0])
        if forme(libelle) not in LIMINAIRE_:
            if montants_de(ligne):
                sys.exit(f"article liminaire, ligne {r} : grandeur inconnue (« {libelle} »)")
            continue
        concept, perimetre, unite_ligne, consolidation, traitements = LIMINAIRE_[forme(libelle)]
        if set(montants_de(ligne)) - set(noms):
            sys.exit(f"article liminaire, ligne {r} : montant dans une colonne sans intitulé")
        for c in executions:
            nombre = nombre_texte(ligne[c]) if c < len(ligne) else None
            if not nombre:
                if c < len(ligne) and re.search(r"[0-9]", ligne[c]):
                    sys.exit(f"article liminaire, ligne {r} : montant illisible (« {ligne[c]} »)")
                continue
            intitule = " ".join(noms[c])
            metrique = ""
            if c != executions[0]:
                metrique = METRIQUES.get((source_id, intitule))
                if metrique is None:
                    sys.exit(f"article liminaire : colonne d'exécution « {intitule} » sans métrique connue")
            appels = [a for n in noms[c] for a in re.findall(APPEL, n)] + re.findall(APPEL, ligne[c]) + appels_unite
            yield {"tableau": i, "ligne": r, "colonne": c, "libelle": libelle, "intitule": intitule, "concept": concept,
                   "fonction": "", "nombre": nombre, "unite": unite_ligne or unite_tableau,
                   "note": note_des_appels(appels, notes), "perimetre": perimetre, "consolidation": consolidation,
                   "traitements": ";".join(t for t in (traitements, metrique) if t),
                   "statut": "estimation" if concept in ESTIMATIONS_LIMINAIRE or "*" in ligne[c] and
                   notes.get("*", "").startswith("Estimation") else "provisoire"}


def lignes_article_2(i, tableau, forme_, annee, source_id):
    """La colonne lue est celle de l'exécution de l'année ; celle de la loi de finances de l'année, que présentent les
    textes jusqu'aux comptes de 2007, ne l'est pas. Une ligne sans montant est une rubrique ou une ligne vide."""
    annoncees = unites_annoncees(tableau, forme_)
    if annoncees != {"en milliards d’euros"}:
        sys.exit(f"tableau de financement : unité annoncée inconnue ou absente ({annoncees or 'aucune'})")
    colonnes_ = {c for l in tableau for c, x in enumerate(l) if c > 0 and forme(x).startswith("execution")}
    if len(colonnes_) != 1:
        sys.exit(f"tableau de financement : {len(colonnes_)} colonne(s) d'exécution")
    execution = colonnes_.pop()
    intitule = next(propre(l[execution]) for l in tableau if forme(l[execution]).startswith("execution"))
    if intitule != f"Exécution {annee}":
        sys.exit(f"tableau de financement : colonne « {intitule} »")
    for c in {c for l in tableau for c, x in enumerate(l) if c > 0 and c != execution and propre(x)}:
        intitules = [x for l in tableau if c < len(l) for x in [l[c]] if propre(x) and not nombre_texte(x)]
        if not intitules or not all(forme(x).startswith("loi de finances de l'annee") for x in intitules):
            sys.exit("tableau de financement : colonne autre que l'exécution et la loi de finances de l'année")
    notes, rubrique = notes_du_tableau(tableau), None
    for r, ligne in enumerate(tableau):
        libelle = propre(ligne[0])
        if forme(libelle) in RUBRIQUES_FINANCEMENT_ and not nombre_texte(ligne[execution]):
            rubrique = RUBRIQUES_FINANCEMENT_[forme(libelle)]
            continue
        nombre = nombre_texte(ligne[execution])
        if not nombre:
            if re.search(r"[0-9]", ligne[execution]) and not forme(ligne[execution]).startswith("execution"):
                sys.exit(f"tableau de financement, ligne {r} : montant illisible (« {ligne[execution]} »)")
            if libelle and (rubrique, forme(libelle)) not in FINANCEMENT_ and not re.match(APPEL, libelle) and \
                    unite_annoncee(libelle) is None:
                sys.exit(f"tableau de financement, ligne {r} : libellé inconnu (« {libelle} »)")
            continue
        concept = FINANCEMENT_.get((rubrique, forme(libelle)))
        if concept is None:
            sys.exit(f"tableau de financement, ligne {r} : libellé inconnu (« {libelle} », rubrique {rubrique})")
        appels = re.findall(APPEL, libelle) + re.findall(APPEL, ligne[execution])
        yield {"tableau": i, "ligne": r, "colonne": execution, "libelle": libelle, "intitule": intitule,
               "concept": concept, "fonction": "", "nombre": nombre, "unite": "MD_EUR",
               "note": note_des_appels(appels, notes), "consolidation": "sans_objet" if concept in SOLDES_FINANCEMENT
               else "non_consolide", "statut": "definitif"}


def lignes_compte_de_resultat(tableaux, formes, annee):
    """Les tableaux du compte de résultat se lisent à la suite, une rubrique valant jusqu'à la suivante : une ligne
    sans montant qui porte son nom, la légende du tableau, ou le premier de deux libellés d'une même ligne. Une ligne
    d'années indique celle de chaque colonne ; à défaut, les montants sont ceux de l'année des comptes."""
    rubrique = None
    for i, tableau in tableaux:
        if unites_annoncees(tableau, formes[i]) != {"en millions d’euros"}:
            sys.exit(f"compte de résultat, tableau {i} : unité annoncée inconnue ou absente")
        rubrique = RUBRIQUES_RESULTAT_.get(forme(formes[i]["legende"]), rubrique)
        notes, annees = notes_du_tableau(tableau), {}
        for r, ligne in enumerate(tableau):
            libelles, montants_ = textes(ligne), montants_de(ligne)
            # Ligne des années, qui peut aussi porter le nom d'une rubrique (comptes de 2023 et 2024).
            if montants_ and all(re.fullmatch(r"(?:19|20)[0-9]{2}(?:\s*\([0-9]\))?", propre(ligne[c])) for c in montants_) \
                    and all(forme(t) in RUBRIQUES_RESULTAT_ for t in libelles):
                annees = {c: n[0] for c, n in montants_.items()}
                rubrique = RUBRIQUES_RESULTAT_[forme(libelles[0])] if libelles else rubrique
                continue
            if not montants_:
                for t in libelles:
                    if forme(t) in RUBRIQUES_RESULTAT_:
                        rubrique = RUBRIQUES_RESULTAT_[forme(t)]
                    elif forme(t) not in RESULTAT_ and unite_annoncee(t) is None and not re.match(APPEL, t):
                        sys.exit(f"compte de résultat, tableau {i}, ligne {r} : libellé inconnu (« {t} »)")
                continue
            if len(libelles) == 2 and forme(libelles[0]) in RUBRIQUES_RESULTAT_:
                rubrique, libelles = RUBRIQUES_RESULTAT_[forme(libelles[0])], libelles[1:]
            if len(libelles) != 1:
                sys.exit(f"compte de résultat, tableau {i}, ligne {r} : libellés {libelles}")
            libelle = libelles[0]
            f = forme(libelle)
            # Une rubrique et le premier libellé de ses lignes, réunis dans une même case (comptes de 2021).
            tete = next((x for x in RUBRIQUES_RESULTAT_ if f.startswith(x + " ") and f[len(x) + 1:] in RESULTAT_), None)
            if tete:
                rubrique, f = RUBRIQUES_RESULTAT_[tete], f[len(tete) + 1:]
            concept = RESULTAT_.get(f)
            if isinstance(concept, dict):
                concept = concept.get(rubrique)
            if concept is None:
                sys.exit(f"compte de résultat, tableau {i}, ligne {r} : libellé inconnu (« {libelle} », rubrique {rubrique})")
            for c, nombre in montants_.items():
                if annees and c not in annees or not annees and len(montants_) > 1:
                    sys.exit(f"compte de résultat, tableau {i}, ligne {r} : colonne {c} sans année")
                periode = annees.get(c, annee)
                if not annee - 1 <= int(periode) <= annee:
                    sys.exit(f"compte de résultat, tableau {i} : année {periode} dans les comptes de {annee}")
                appels = re.findall(APPEL, libelle) + re.findall(APPEL, ligne[c])
                yield {"tableau": i, "ligne": r, "colonne": c, "libelle": libelle, "intitule": str(periode),
                       "concept": concept, "fonction": "", "nombre": nombre, "unite": "MIO_EUR",
                       "note": note_des_appels(appels, notes), "perimetre": "ETAT_CGE", "periode": str(periode),
                       "consolidation": "sans_objet" if concept == _E + "SOLDE_OPERATIONS_EXERCICE" else "non_consolide",
                       "statut": "definitif"}


def colonne_de_bilan(textes_):
    """(période, suffixe du concept, note) d'une colonne du bilan, d'après ses intitulés : sa date, puis le brut, les
    amortissements et dépréciations, ou le net. Le bilan au 1er janvier d'une année est celui de la fin de la
    précédente."""
    dates, mesures = [], []
    for t in textes_:
        fin = re.fullmatch(r"31 décembre ((?:19|20)[0-9]{2})|31/12/((?:19|20)[0-9]{2})", t)
        debut = re.fullmatch(r"1 ?er janvier ((?:19|20)[0-9]{2})", t)
        if fin:
            dates.append((fin.group(1) or fin.group(2), ""))
        elif debut:
            dates.append((str(int(debut.group(1)) - 1), f"Bilan au 1er janvier {debut.group(1)}."))
        else:
            mesures.append(forme(t))
    mesure = " ".join(mesures)
    suffixe = "_AMORTISSEMENTS" if mesure.startswith("amortissement") else MESURES_BILAN.get(mesure)
    if len(dates) != 1 or suffixe is None:
        sys.exit(f"bilan : colonne « {' '.join(textes_)} »")
    return dates[0][0], suffixe, dates[0][1]


def lignes_bilan(i, tableau, forme_, annee):
    """Les lignes d'en-tête précèdent la première rubrique. Le brut et les amortissements ne se lisent qu'à l'actif."""
    if unites_annoncees(tableau, forme_) != {"en millions d’euros"}:
        sys.exit("bilan : unité annoncée inconnue ou absente")
    debut = next(r for r, l in enumerate(tableau) if l and forme(l[0]) in RUBRIQUES_BILAN_)
    noms = entetes(tableau, range(debut), forme_["largeurs"])
    chiffrees = {c for l in tableau[debut:] for c in montants_de(l)}
    # Une date d'en-tête unique, que la page place au-dessus d'une seule colonne, vaut pour toutes.
    dates = {t for c in chiffrees for t in noms[c] if re.search(r"(?:19|20)[0-9]{2}", t)}
    if len(dates) == 1:
        noms = {c: [*dates] + [t for t in noms[c] if t not in dates] for c in chiffrees}
    colonnes_ = {c: colonne_de_bilan(noms[c]) for c in chiffrees}
    if any(not annee - 2 <= int(p) <= annee for p, _, _ in colonnes_.values()):
        sys.exit(f"bilan : date hors des comptes de {annee} et des deux années précédentes")
    if not any(p == str(annee) and s == "" for p, s, _ in colonnes_.values()):
        sys.exit(f"bilan : pas de colonne du net au 31 décembre {annee}")
    notes, cote = notes_du_tableau(tableau), "actif"
    for r in range(debut, len(tableau)):
        ligne, libelle = tableau[r], propre(tableau[r][0])
        concept = BILAN_.get((cote, forme(libelle)))
        montants_ = montants_de(ligne)
        if not montants_:
            if libelle and concept is None and forme(libelle) not in RUBRIQUES_BILAN_ and not re.match(APPEL, libelle):
                sys.exit(f"bilan, ligne {r} : libellé inconnu (« {libelle} »)")
            continue
        if concept is None:
            sys.exit(f"bilan, ligne {r} : libellé inconnu (« {libelle} », côté {cote})")
        for c, nombre in montants_.items():
            if c not in colonnes_:
                sys.exit(f"bilan, ligne {r} : montant hors colonne")
            periode, suffixe, note_date = colonnes_[c]
            if suffixe and cote != "actif":
                sys.exit(f"bilan, ligne {r} : brut ou amortissements hors de l'actif")
            appels = re.findall(APPEL, libelle) + re.findall(APPEL, ligne[c])
            yield {"tableau": i, "ligne": r, "colonne": c, "libelle": libelle, "intitule": " ".join(noms[c]),
                   "concept": concept + suffixe, "fonction": "", "nombre": nombre, "unite": "MIO_EUR",
                   "note": " ".join(n for n in (note_date, note_des_appels(appels, notes)) if n), "perimetre": "ETAT_CGE",
                   "periode": periode, "consolidation": "sans_objet", "statut": "definitif"}
        cote = {_E + "ACTIF": "passif", _E + "PASSIF": "situation"}.get(concept, cote)


def lignes_articles_liminaire_2_3(tableaux, formes, lus, annee, source_id):
    """Les tableaux à montants que les articles 1er, 4, 5 et 6 ne lisent pas : article liminaire, tableau de
    financement, compte de résultat et bilan. Un tableau à montants d'aucun de ces genres arrête l'import ; chaque
    genre a son tableau, sauf le compte de résultat, qui en a souvent plusieurs, et l'article liminaire, qui n'existe que
    depuis les comptes de 2012."""
    par_genre = collections.defaultdict(list)
    for i, t in enumerate(tableaux):
        if i in lus or not any(montants_de(l) for l in t):
            continue
        genre = genre_de_tableau(t)
        if genre is None:
            sys.exit(f"tableau {i} : montants d'un tableau qu'aucun article ne lit")
        par_genre[genre].append((i, t))
    attendus = {"financement", "resultat", "bilan"} | ({"liminaire"} if int(annee) >= 2012 else set())
    if set(par_genre) != attendus or any(len(v) > 1 for g, v in par_genre.items() if g != "resultat"):
        sys.exit(f"articles liminaire, 2 et 3 : tableaux {dict((g, [i for i, _ in v]) for g, v in par_genre.items())}")
    for i, t in par_genre.get("liminaire", []):
        yield from lignes_article_liminaire(i, t, formes[i], int(annee), source_id)
    for i, t in par_genre["financement"]:
        yield from lignes_article_2(i, t, formes[i], int(annee), source_id)
    yield from lignes_compte_de_resultat(par_genre["resultat"], formes, int(annee))
    for i, t in par_genre["bilan"]:
        yield from lignes_bilan(i, t, formes[i], int(annee))


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions et programmes."""
    chemin = BASE / fichier["chemin"]
    annees = set(re.findall(ANNEE, texte_html(chemin.read_text(encoding="utf-8"))))
    if len(annees) != 1 or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année des comptes ({', '.join(sorted(annees)) or 'aucune'}) ou date du texte "
                 f"introuvable")
    annee = annees.pop()
    if not int(annee) < int(fichier["mis_a_jour_source"][:4]) <= int(annee) + 2:
        sys.exit(f"{fichier['id']} : comptes de {annee} dans un texte daté {fichier['mis_a_jour_source']}")
    # Une coupure de mot de fin de ligne du texte imprimé, restée dans la page (« dévelop-pement »), se recolle quand
    # le mot entier figure ailleurs dans le texte.
    mots = set(re.findall(r"\w+", texte_html(chemin.read_text(encoding="utf-8")).lower()))
    recolle = lambda libelle: re.sub(r"(\w+)-(\w+)", lambda m: m.group(1) + m.group(2) if m.group(1)[-1].islower() and
                                     m.group(2)[0].islower() and (m.group(1) + m.group(2)).lower() in mots
                                     else m.group(0), libelle)
    tableaux, formes = lire_tableaux_html(chemin, mise_en_forme=True)
    i, tableau = article_1(tableaux)
    brutes = list(lignes_article_1(i, tableau, formes[i], fichier["source_id"])) + \
        list(lignes_article_4(tableaux, formes, fichier["source_id"], recolle)) + \
        list(lignes_articles_5_6(tableaux, formes, fichier["source_id"], recolle))
    lus = {b["tableau"] for b in brutes}
    brutes += list(lignes_articles_liminaire_2_3(tableaux, formes, lus, annee, fichier["source_id"]))
    for brute in brutes:
        fonction = ""
        if brute["fonction"]:
            libelle, mission = brute["fonction"]
            parent = f"LOLF.{code_lolf(mission)}" if mission else ""
            fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
            if parent:
                fonctions.setdefault(parent, {"id": parent, "libelle": mission, "norme_id": "LOLF", "parent_id": ""})
            fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": parent})
        concept = brute["concept"]
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"tableau={brute['tableau']};ligne={brute['ligne']};colonne={brute['colonne']};"
                           f"libelle={brute['libelle']};colonne_libelle={brute['intitule']}",
            "zone": "FR", "perimetre_id": brute.get("perimetre", "ETAT_LF"), "concept_id": concept,
            "fonction_id": fonction, "traitements": brute.get("traitements", ""), "unite_id": brute["unite"],
            "periode": brute.get("periode", annee), "valeur": brute["nombre"][0], "decimales": brute["nombre"][1],
            "statut": brute.get("statut") or ("non_precise" if concept in AJUSTEMENTS or brute.get("ajustement")
                                              else "definitif"),
            "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10],
            "consolidation": brute.get("consolidation") or ("sans_objet" if concept in SOLDES or brute.get("solde")
                                                            else "non_consolide"),
            "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": brute["note"],
        }
        ligne["id"] = identifiant(ligne)
        yield ligne


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    ajoutes, inchanges = fusionner(existants, list(lignes_du_fichier(fichier, fonctions)), fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
