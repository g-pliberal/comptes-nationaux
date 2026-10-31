#!/usr/bin/env python3
"""Enregistre dans la base les crédits qu'ouvre une loi de finances initiale, les recettes qu'elle évalue et les soldes
qu'elle prévoit, à partir de son texte définitif, tel que le publie l'assemblée qui l'a adopté en dernier (page HTML
archivée du Sénat ou de l'Assemblée nationale).

    python3 outils/importer_lois_finances.py <fichier_id>

Tableaux lus : les états qui répartissent par mission et par programme les autorisations d'engagement et les crédits
de paiement que la loi ouvre : l'état B pour le budget général, l'état C pour les budgets annexes, l'état D pour les
comptes d'affectation spéciale puis pour les comptes de concours financiers. Sous un programme, une ligne « dont
titre 2 » (« dont charges de personnel » pour un budget annexe, jusqu'aux lois pour 2022) donne la part de ses crédits
qui va aux dépenses de personnel. L'état A évalue les recettes, ligne par ligne : celles du budget général par
division (« 11. Impôt sur le revenu »), que récapitule un second tableau, puis celles de chaque budget annexe et de
chaque compte spécial, par section. Le tableau de l'article d'équilibre, en millions d'euros, donne les ressources,
les charges et les soldes de chaque catégorie, et le solde général ; son tableau de financement, en milliards d'euros,
le besoin de financement de l'État et les ressources qui le couvrent, et l'article fixe le plafond de la variation
nette de la dette négociable à plus d'un an et celui des emplois de l'État. La seconde partie de la loi répartit ce
dernier par ministère et par budget annexe, et fixe les plafonds d'emplois des opérateurs de l'État, des agents de droit
local des établissements à autonomie financière et des autorités publiques indépendantes. L'état E (les autorisations
de découvert) et les plafonds d'encours de dette des budgets annexes ne sont pas lus.

Dans l'état A, une division égale la somme de ses lignes, une catégorie de recettes celle de ses divisions, un compte
celle de ses sections, une section celle de ses lignes, un budget annexe celle de ses lignes, dotations aux
amortissements déduites, aux arrondis près : la demi-unité de la page par montant en jeu ; un écart plus grand arrête
l'import, sauf s'il est déclaré dans ECARTS_A. Le tableau d'équilibre s'additionne, à l'arrondi au million près de
chacun de ses montants ; un montant qu'il reprend d'un état, recettes de l'état A ou crédits des états B à D, et chaque
solde que les états permettent de calculer, se vérifient contre eux ; le reste s'enregistre. Les recettes fiscales du
budget général sont brutes dans l'état A jusqu'à la loi pour 2022, nettes des remboursements et dégrèvements depuis
(division 18) ; leur concept le dit. Le tableau de financement s'additionne exactement, hors lignes « Dont … », qui
détaillent celle qui les précède et en font la somme ; son déficit est l'opposé du solde général, à l'arrondi près, et
le plafond de la variation de la dette, exactement ses émissions de dette à moyen et long termes, nettes des rachats,
moins l'amortissement de leur nominal. Une case qui réunit plusieurs lignes se déclare dans FUSIONS_FINANCEMENT. Un
plafond d'emplois égale exactement la somme de ses lignes, et le total de son tableau celui de la phrase qui l'annonce ;
la répartition des emplois de l'État égale le plafond de l'article d'équilibre, à l'écart déclaré dans ECARTS_EMPLOIS
près, et chaque programme des tableaux par mission doit être un programme des états de la loi.

Un état se reconnaît à son intitulé (« ÉTAT B (Article 167 de la loi) »), et les catégories de crédits qu'il répartit
à son titre (« … des crédits du budget général »). Ses tableaux sont ceux qui s'ouvrent entre son intitulé et celui de
l'état suivant, hors ceux qui portent l'intitulé d'un état ; un tableau que la page coupe en plusieurs continue jusqu'à
sa ligne de total, et chaque catégorie a le sien, dans l'ordre du titre.

Une mission égale la somme de ses programmes, en autorisations d'engagement comme en crédits de paiement. Quand un
tableau met des lignes en gras, ses missions sont ces lignes, ou, dans le texte pour 2009, celles qui ne le sont pas ;
certaines pages de l'Assemblée nationale ne marquant pas le gras, les missions se reconnaissent sinon à leurs montants :
une mission se ferme dès que ses programmes font son montant, et une ligne nulle qui la suit est un programme de plus,
sauf si c'est une mission que la base connaît déjà. Un tableau qui ne donne que des missions, comme celui du budget
général dans le texte de la commission mixte paritaire de 2006, se reconnaît à ce que ses lignes font ensemble son
total. Une ligne « (ligne supprimée) » n'est pas un programme. La somme des missions doit faire la ligne de total, et
celle-ci le montant que l'article de la loi ouvre pour la catégorie (« Il est ouvert aux ministres, pour 2024, au titre
du budget général, des autorisations d'engagement et des crédits de paiement s'élevant respectivement aux montants de
… € et de … € ») ; jusqu'aux lois pour 2019, un seul article ouvre ensemble les crédits des comptes d'affectation
spéciale et ceux des comptes de concours financiers. Une case « » » ne porte pas de chiffre : elle vaut zéro dans ces
sommes. Une colonne ou une ligne « dont » inconnue, ou une somme qui ne tombe pas juste, arrête l'import, sauf une
coquille de la page que ses propres sommes démontrent, déclarée dans COQUILLES.

Les missions, les budgets annexes, les comptes spéciaux et leurs programmes sont les fonctions de la norme LOLF, sous
l'identifiant que leur donne l'import des lois d'approbation des comptes (outils/importer_lois_resultats.py) : le
budget voté se compare ainsi, mission par mission, au budget exécuté. Les divisions de recettes du budget général sont
les fonctions LOLF.RECETTES.<numéro et libellé>, leurs lignes, celles de leur division suivies du numéro et du libellé
de la ligne ; une section ou une ligne de compte prend l'identifiant du compte suivi du sien. Un ministère ou une
autorité publique indépendante des plafonds d'emplois est la fonction LOLF.EMPLOIS.<nom>. La version d'un chiffre est la
date que le texte porte ; les crédits ouverts sont des autorisations, et les recettes des évaluations, sans statut de
prévision ou d'exécution.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_page_html,
                    lire_texte_html, montants_de_case, nombre_de_phrase, nombre_texte, table_des_chiffres,
                    texte_html)
import importer_lois_resultats as resultats
from importer_lois_resultats import code_lolf, colonnes, montants, propre, unite

# Catégories de crédits, telles que le titre d'un état et l'article de la loi les nomment.
CATEGORIES = {"BG": r"budget général", "BA": r"budgets annexes", "CAS": r"comptes d[’']affectation spéciale",
              "CCF": r"comptes de concours financiers"}
# Catégorie (ou catégories ouvertes ensemble par un même article) → montants de l'article de la loi.
ARTICLES = {("BG",): r"du budget général", ("BA",): r"des budgets annexes", ("CAS",): r"des comptes d[’']affectation spéciale",
            ("CCF",): r"des comptes de concours financiers",
            ("CAS", "CCF"): r"des comptes d[’']affectation spéciale et des comptes de concours financiers"}
COLONNES = {"Autorisations d’engagement": "AE", "Crédits de paiement": "CP"}
DONT = r"dont (?:titre 2|charges de personnel)"
# Coquilles d'une page, que ses propres sommes démontrent : (source, libellé de la ligne, colonne) → (montant de la
# page, montant juste). Le chiffre garde le montant de la page, avec une note ; les sommes de l'import prennent le
# montant juste.
COQUILLES = {
    ("an.ta13-0808", "Gestion du patrimoine immobilier de l’État", "CP"): (5130000000, 513000000),
}
NEANT = {"»", "-", "–", "—"}
ETAT = r"[ÉE][Tt][Aa][Tt]\s+([A-G])\s*\(\s*[Aa]rticles?\s+[0-9]"

# État A, les voies et moyens : ses parties, chacune annoncée par son intitulé avant son premier tableau.
PARTIES_A = (("BG", r"\bI\.\s*[-–]\s*budget général"),
             ("RECAPITULATION", r"récapitulation (?:des recettes du budget général|générale)"),
             ("BA", r"\bII\.\s*[-–]\s*budgets annexes"),
             ("CAS", r"\bIII\.\s*[-–]\s*comptes d’affectation spéciale"),
             ("CCF", r"\bIV\.\s*[-–]\s*comptes de concours financiers"))
UNITE_A = r"\(\s*en\s+(euros|milliers d’euros)\s*\*?\s*\)"
UNITES_A = {"euros": ("EUR", 1), "milliers d’euros": ("K_EUR", 1000)}
NUMERO_A = r"[0-9]{1,4}(?: (?:bis|ter|quater))?|[A-Z][0-9]{3}"  # numéro de ligne, de division, ou « A701 »
CATEGORIE_A = r"([1-4])\.\s*(.+)"  # « 1. Recettes fiscales »
LETTRE_A = r"([A-D])\.\s*-\s*(.+)"  # « A. - Recettes fiscales », dans le texte pour 2006
DIVISION_A = r"([0-9]{2}(?: ?(?:bis|ter|quater))?)\.\s*(.+)"  # « 13 bis. Contribution sociale sur les bénéfices »
# Concept de chaque catégorie de recettes du budget général ; les recettes fiscales sont brutes jusqu'à la loi pour
# 2022, nettes des remboursements et dégrèvements depuis, quand l'état A les déduit dans sa division 18.
RECETTES_BG = {"1": "LOLF.BG_RECETTES_FISCALES_{}_LFI", "2": "LOLF.BG_RECETTES_NON_FISCALES_LFI",
               "3": "LOLF.BG_PRELEVEMENTS_SUR_RECETTES_LFI", "4": "LOLF.BG_FONDS_DE_CONCOURS_RECETTES_LFI"}
FONDS_DE_CONCOURS_A = r"(?:Évaluation des fonds de concours|Fonds de concours(?: et attributions de produits)?)"
SECTIONS_BA = r"Section des opérations (?:courantes|en capital)"  # budgets annexes, jusqu'à la loi pour 2008
TOTAL_BA = r"Total des recettes(?: nettes| et des ressources de financement)?"
TOTAL_CS = r"Total(?: des recettes| pour les comptes de concours financiers)?"
SECTION_CS = r"Section(?: [0-9]+)?\s*:\s*(.+)"
# Écarts d'une page de l'état A entre un total et la somme de ses lignes : (source, total) → écart (total − somme), en
# euros. Le chiffre du total garde le montant de la page, avec une note, et la section 2 du rapport de cohérence relève
# l'écart ; tout autre écart arrête l'import.
ECARTS_A = {
    ("an.ta14-0267", "Contrôle et exploitation aériens"): 300,
}
ECARTS_VUS = set()  # écarts de ECARTS_A que l'import a rencontrés : un écart déclaré absent arrête l'import

# Article d'équilibre : libellé d'une ligne de son tableau (sans ses appels de note) → concepts des montants de ses
# colonnes de ressources, de charges et de solde. Un montant qu'un état donne déjà, à l'euro, se vérifie contre lui,
# au million près ; un montant que deux lignes donnent se vérifie de même ; les autres s'enregistrent.
EQUILIBRE = {
    "BG": {"Recettes fiscales brutes / dépenses brutes": ("BG_RECETTES_FISCALES_BRUTES", "BG_CP", None),
           "À déduire : Remboursements et dégrèvements": ("BG_REMBOURSEMENTS_DEGREVEMENTS",
                                                        "BG_REMBOURSEMENTS_DEGREVEMENTS", None),
           "Recettes fiscales nettes / dépenses nettes": ("BG_RECETTES_FISCALES_NETTES", "BG_DEPENSES_NETTES_HORS_FDC",
                                                          None),
           "Recettes fiscales / dépenses": ("BG_RECETTES_FISCALES_NETTES", "BG_DEPENSES_NETTES_HORS_FDC", None),
           "Recettes non fiscales": ("BG_RECETTES_NON_FISCALES", None, None),
           "Recettes totales nettes / dépenses nettes": ("BG_RECETTES_NETTES_HORS_FDC", "BG_DEPENSES_NETTES_HORS_FDC",
                                                         None),
           "Recettes totales nettes / dépenses totales nettes": ("BG_RECETTES_NETTES_HORS_FDC",
                                                                 "BG_DEPENSES_NETTES_HORS_FDC", None),
           "Recettes totales / dépenses totales": ("BG_RECETTES_NETTES_HORS_FDC", "BG_DEPENSES_NETTES_HORS_FDC", None),
           "À déduire : Prélèvements sur recettes au profit des collectivités territoriales et de l’Union européenne":
               ("BG_PRELEVEMENTS_SUR_RECETTES", None, None),
           "À déduire : Prélèvements sur recettes au profit des collectivités territoriales et des Communautés "
           "européennes": ("BG_PRELEVEMENTS_SUR_RECETTES", None, None),
           "Montants nets pour le budget général": ("BG_RECETTES_NETTES_HORS_PSR", "BG_DEPENSES_NETTES_HORS_FDC",
                                                    "SOLDE_BUDGET_GENERAL"),
           "Montants nets du budget général": ("BG_RECETTES_NETTES_HORS_PSR", "BG_DEPENSES_NETTES_HORS_FDC",
                                               "SOLDE_BUDGET_GENERAL"),
           "Évaluation des fonds de concours et crédits correspondants": ("BG_FONDS_DE_CONCOURS_RECETTES",
                                                                         "BG_FONDS_DE_CONCOURS_RECETTES", None),
           "Évaluation des fonds de concours et des attributions de produits et crédits correspondants":
               ("BG_FONDS_DE_CONCOURS_RECETTES", "BG_FONDS_DE_CONCOURS_RECETTES", None),
           "Évaluation des fonds de concours et des attributions de produits":
               ("BG_FONDS_DE_CONCOURS_RECETTES", "BG_FONDS_DE_CONCOURS_RECETTES", None),
           "Montants nets pour le budget général, y compris fonds de concours": ("BG_RECETTES_NETTES",
                                                                                 "BG_DEPENSES_NETTES", None),
           "Montants nets pour le budget général y compris fonds de concours": ("BG_RECETTES_NETTES",
                                                                                "BG_DEPENSES_NETTES", None)},
    "BA": {"": ("BA_RECETTES_HORS_FDC", "BA_CP", "BA_SOLDE_HORS_FDC"),  # chaque budget annexe
           "Totaux pour les budgets annexes": ("BA_RECETTES_HORS_FDC", "BA_CP", "BA_SOLDE_HORS_FDC")},
    "BA_FDC": {"": ("BA_FDC_RECETTES", "BA_FDC_RECETTES", None),
               "Totaux pour les budgets annexes, y compris fonds de concours": ("BA_RECETTES", "BA_CHARGES",
                                                                               "SOLDE_BUDGETS_ANNEXES"),
               "Totaux pour les budgets annexes y compris fonds de concours": ("BA_RECETTES", "BA_CHARGES",
                                                                              "SOLDE_BUDGETS_ANNEXES")},
    "CS": {"Comptes d’affectation spéciale": ("CAS_RECETTES", "CAS_CP", "CAS_SOLDE"),
           "Comptes de concours financiers": ("CCF_RECETTES", "CCF_CP", "CCF_SOLDE"),
           "Comptes de commerce (solde)": (None, None, "COMPTES_COMMERCE_SOLDE"),
           "Comptes d’opérations monétaires (solde)": (None, None, "OPERATIONS_MONETAIRES_SOLDE"),
           "Solde pour les comptes spéciaux": (None, None, "SOLDE_COMPTES_SPECIAUX"),
           "Solde général": (None, None, "RESULTAT_BUDGETAIRE")},
}
# Montants que le tableau seul donne, et qui ne servent qu'à le vérifier : les charges des budgets annexes, fonds de
# concours compris.
VERIFIES_SEULEMENT = {"BA_CHARGES"}
RUBRIQUES_EQUILIBRE = {"Budget général": "BG", "Budgets annexes": "BA", "Comptes spéciaux": "CS"}
# Concepts que les états B à D donnent à l'euro, et que le tableau d'équilibre ne donne qu'à leur place.
SUBSTITUTS = {"LOLF.BA_CP_LFI", "LOLF.CAS_CP_LFI", "LOLF.CCF_CP_LFI", "LOLF.CAS_RECETTES_LFI", "LOLF.CCF_RECETTES_LFI"}
SUBSTITUTS_PAR_BUDGET = {"LOLF.BA_RECETTES_HORS_FDC_LFI", "LOLF.BA_FDC_RECETTES_LFI"}
FDC_EQUILIBRE = (r"[ÉE]valuation des fonds de concours(?: et des attributions de produits)?(?: et crédits "
                 r"correspondants)?(?: :)?")

# Tableau de financement de l'article d'équilibre (II, 1°), en milliards d'euros : (rubrique, libellé) → concept de
# l'exécution, que le voté suit de _LFI ; ceux de l'import des lois d'approbation des comptes, et les libellés propres
# aux lois de finances. Une ligne « Dont … » détaille celle qui la précède et n'entre pas dans les totaux.
FINANCEMENT_LFI = resultats.par_forme({**resultats.FINANCEMENT, **{
    ("besoin", "Amortissement de la dette reprise de SNCF Réseau"): "LOLF.AMORTISSEMENT_SNCF_RESEAU",
    ("besoin", "Amortissement des autres dettes reprises"): "LOLF.AMORTISSEMENT_AUTRES_DETTES",
    # loi pour 2018 : la part de l'amortissement qui n'est pas le supplément d'indexation, soit le nominal
    ("besoin", "Dont amortissement de la dette à moyen et long termes"): "LOLF.AMORTISSEMENT_DETTE_NOMINAL",
    ("besoin", "Dont suppléments d’indexation versés à l’échéance (titres indexés) (titres indexés)"):
        "LOLF.SUPPLEMENTS_INDEXATION",
    ("ressources", "Émissions à moyen et long termes (obligations assimilables du Trésor et bons du Trésor à taux fixe "
                   "et intérêt annuel), nettes des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émissions à moyen et long termes (obligations assimilables du Trésor et bons du Trésor à taux fixe "
                   "et intérêt annuel), nettes des rachats effectués par l’État et par la Caisse de la dette publique"):
        "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émissions à moyen et long terme (obligations assimilables du Trésor et bons du Trésor à taux fixe "
                   "et intérêt annuel), nettes des rachats effectués par l’État et par la Caisse de la dette publique"):
        "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émission de dette à moyen et long termes, nette des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Émission de dette à moyen et long termes nette des rachats"): "LOLF.EMISSIONS_DETTE_MLT",
    ("ressources", "Variation du compte de Trésor"): "LOLF.VARIATION_COMPTE_TRESOR",
    ("ressources", "Variation du compte de Trésor et divers"): "LOLF.VARIATION_COMPTE_TRESOR",
}})
TOTAUX_FINANCEMENT = {"besoin": "LOLF.BESOIN_FINANCEMENT", "ressources": "LOLF.RESSOURCES_FINANCEMENT"}
# Case qui réunit les libellés et les montants de plusieurs lignes : (source, libellé de la case) → libellés de ses
# lignes, dans l'ordre de ses montants.
FUSIONS_FINANCEMENT = {
    ("an.ta14-0267", "Déficit à financer Dont déficit budgétaire Dont dotation budgétaire du deuxième programme "
                     "d’investissements d’avenir Autres besoins de trésorerie"):
        ("Déficit à financer", "Dont déficit budgétaire",
         "Dont dotation budgétaire du deuxième programme d’investissements d’avenir", "Autres besoins de trésorerie"),
}
# Plafond de la variation nette de la dette négociable de l'État d'une durée supérieure à un an (II, 4°, puis 3° depuis
# la loi pour 2018), en milliards d'euros.
PLAFOND_DETTE = (r"Le plafond de la variation nette, appréciée en fin d[’']année(?: et en valeur nominale)?, de la dette "
                 r"négociable de l[’'][ÉE]tat d[’']une durée supérieure à un an est fixé à [0-9]+(?:,[0-9]+)?\s+"
                 r"milliards d[’']euros")

# Plafonds des autorisations d'emplois. L'article d'équilibre (III) fixe celui des emplois rémunérés par l'État ; la
# seconde partie de la loi le répartit par ministère et par budget annexe, et fixe, chacun annoncé par la phrase qui
# précède son tableau, celui des opérateurs de l'État, par mission et par programme (depuis la loi pour 2009), celui des
# agents de droit local des établissements à autonomie financière, par programme (depuis 2010), et celui des autorités
# publiques indépendantes, autorité par autorité (depuis 2012).
PLAFOND_EMPLOIS = (r"le plafond d[’']autorisation des emplois rémunérés par l[’'][ÉE]tat, exprimé en équivalents? temps "
                   r"plein travaillé, est fixé au nombre de [0-9]{1,3}(?:[ \u00a0\u202f][0-9]{3})*")
EMPLOIS = {"ETAT": r"plafond des autorisations d’emplois(?: de l’État)?,? pour [0-9]{4}",
           "OPERATEURS": r"plafond des autorisations d’emplois des opérateurs de l’État",
           "EAF": r"établissements à autonomie financière",
           "API": r"autorités publiques (?:et administratives )?indépendantes|diverses autorités publiques"}
DEBUT_EMPLOIS = {"ETAT": 2006, "OPERATEURS": 2009, "EAF": 2010, "API": 2012}  # première loi où paraît chaque tableau
UNITES_EMPLOIS = {"équivalent temps plein travaillé": "ETPT", "équivalents temps plein travaillé": "ETPT",
                  "équivalents temps plein": "ETP"}
CONCEPTS_EMPLOIS = {"OPERATEURS": "LOLF.OPERATEURS_PLAFOND_EMPLOIS_LFI", "EAF": "LOLF.EAF_PLAFOND_EMPLOIS_LFI",
                    "API": "LOLF.API_PLAFOND_EMPLOIS_LFI"}
# Écart du texte entre le plafond des emplois de l'État que fixe l'article d'équilibre et le total du tableau qui le
# répartit par ministère et par budget annexe : source → total du tableau moins plafond. Le chiffre du plafond en porte
# la note ; tout autre écart arrête l'import.
ECARTS_EMPLOIS = {"an.ta17-0227": 500}
# Libellé d'un programme qui, dans un tableau de plafonds d'emplois, diffère de celui des états de la même loi :
# (source, libellé du tableau) → libellé des états. Trois coquilles en 2009 ; en 2019, l'ancien nom du programme 159,
# avant que l'économie sociale et solidaire y entre.
LIBELLES_EMPLOIS = {
    ("senat.tas08-035", "Transmissions des savoirs et démocratisation de la culture"):
        "Transmission des savoirs et démocratisation de la culture",
    ("senat.tas08-035", "Soutien de la politique de défense"): "Soutien de la politique de la défense",
    ("senat.tas08-035", "Conduite et pilotage de la politique de justice"):
        "Conduite et pilotage de la politique de la justice",
    ("an.ta15-0213", "Expertise, information géographique et météorologie"):
        "Expertise, économie sociale et solidaire, information géographique et météorologie",
}


def concept(categorie, colonne, dont):
    return f"LOLF.{categorie}_{colonne}_LFI" + ("_TITRE_2" if dont else "")


def nom(libelle):
    """Le nom d'une mission ou d'un programme, d'après son libellé : un trait d'union insécable est un trait d'union,
    et la mention « (intitulé modifié) », que porte un texte qui l'a changé, n'en fait pas partie."""
    return re.sub(r"\s*\(\s*intitulé modifié\s*\)", "", libelle.replace("\u2011", "-").replace("\u2010", "-"))


def cle_titre(texte):
    return re.sub(r"\s+", " ", texte.replace("'", "’")).lower()


def montant(texte):
    """Le nombre d'une case, 0 pour une case « néant », None pour une case vide."""
    if texte.strip() in NEANT:
        return 0
    n = nombre_texte(texte)
    return float(n[0]) if n else None


def entete(tableau):
    """Nombre de lignes d'en-tête d'un tableau de crédits : jusqu'à celle qui nomme les deux colonnes ; None si le
    tableau n'en a pas."""
    for r, ligne in enumerate(tableau[:4]):
        textes = {propre(x) for x in ligne}
        if any(t.startswith("Autorisations d") for t in textes) and "Crédits de paiement" in textes:
            return r + 1
    return None


def article(texte, annee, motif):
    """(autorisations d'engagement, crédits de paiement) que l'article de la loi ouvre pour une catégorie, ou None.
    Les apostrophes s'y lisent d'une seule façon, sans les blancs que certaines pages laissent autour d'elles ou
    devant une virgule."""
    texte = re.sub(r"\s+,", ",", re.sub(r"\s*’\s*", "’", texte.replace("'", "’")))
    trouve = re.findall(rf"Il est ouvert aux ministres, pour {annee},? au titre {motif}, des autorisations d’engagement "
                        rf"et des crédits de paiement s’élevant,? respectivement,? aux montants de ([0-9][0-9 ]*[0-9]) ?€? "
                        rf"et de ([0-9][0-9 ]*[0-9]) ?€?", texte)
    if len(trouve) > 1:
        sys.exit(f"{len(trouve)} articles ouvrent les crédits {motif}")
    return tuple(float(x.replace(" ", "")) for x in trouve[0]) if trouve else None


def blocs_des_etats(grilles, formes, flux, source_id):
    """[(catégorie, bloc)] : pour chaque catégorie de chaque état de crédits, ses lignes, tableau par tableau."""
    intitules = list(re.finditer(ETAT, flux))
    resultat = []
    for n, m in enumerate(intitules):
        fin = intitules[n + 1].start() if n + 1 < len(intitules) else len(flux)
        tableaux = [int(k) for k in re.findall(r"⟦([0-9]+)⟧", flux[m.start():fin])]
        tableaux = [k for k in tableaux if not re.search(ETAT, " ".join(x for l in grilles[k] for x in l))]
        premier = next((k for k in tableaux if entete(grilles[k])), None)
        if premier is None:
            continue  # état sans tableau de crédits (recettes, découverts, objectifs)
        titre = cle_titre(flux[m.start():flux.index(f"⟦{premier}⟧", m.start())])
        categories = sorted((c for c, motif in CATEGORIES.items() if re.search(motif, titre)),
                            key=lambda c: re.search(CATEGORIES[c], titre).start())
        blocs, ouvert = [], None
        for k in tableaux:
            t, forme = grilles[k], formes[k]
            e = entete(t)
            if e is None and ouvert is None:
                continue
            if e is not None:
                noms = colonnes(t, e, forme["largeurs"])
                if ouvert is None:
                    ouvert = {"lignes": [], "noms": noms, "unite": unite(t, e, noms, forme, source_id), "total": None,
                              "gras": set(), "avant": flux[(flux.index(f"⟦/{blocs[-1]['dernier']}⟧") if blocs
                                                            else m.start()):flux.index(f"⟦{k}⟧")]}
                elif set(noms.values()) != set(ouvert["noms"].values()):
                    sys.exit(f"tableau {k} : colonnes autres que celles du tableau qu'il continue")
            else:
                e, noms = 0, ouvert["noms"]
                if max(len(l) for l in t) != max(ouvert["noms"]) + 1:
                    sys.exit(f"tableau {k} : {max(len(l) for l in t)} colonnes, quand le tableau qu'il continue en a "
                             f"{max(ouvert['noms']) + 1}")
            textes_entete = {propre(x) for l in t[:e] for x in l if propre(x)} | set(ouvert["noms"].values())
            ouvert["gras"] |= {(k, r) for r, c in forme["gras"] if c == 0}
            ouvert["dernier"] = k
            par_ligne = {}
            for r, c, nombre in montants(t, e, noms, forme["largeurs"]):
                if noms[c] not in COLONNES:
                    sys.exit(f"tableau {k} : colonne « {noms[c]} » inconnue")
                par_ligne.setdefault(r, {})[COLONNES[noms[c]]] = (c, nombre)
            for r in range(e, len(t)):
                libelle = propre(t[r][0])
                # Une case fusionnée sur deux colonnes de même intitulé laisse vide la seconde.
                cases = {}
                for c, x in enumerate(t[r]):
                    if c in noms and noms[c] in COLONNES and not cases.get(COLONNES[noms[c]], "").strip():
                        cases[COLONNES[noms[c]]] = x
                valeurs = {col: montant(x) for col, x in cases.items()}
                notes = {}
                for col in valeurs:
                    publie, juste = COQUILLES.get((source_id, libelle, col), (None, None))
                    if publie is not None:
                        if valeurs[col] != publie:
                            sys.exit(f"tableau {k}, ligne {r} : coquille déclarée ({publie}) absente ({valeurs[col]})")
                        valeurs[col] = juste
                        lisible = lambda x: f"{x:,}".replace(",", "\u202f")
                        notes[col] = (f"Coquille de la page, qui imprime « {' '.join(cases[col].split())} » : le chiffre "
                                      f"en garde la lecture, {lisible(publie)} €, quand les programmes et le total de "
                                      f"l’état comptent {lisible(juste)} €.")
                if ouvert is None:
                    if libelle or any(v is not None for v in valeurs.values()):
                        sys.exit(f"tableau {k}, ligne {r} : ligne après le total (« {libelle} »)")
                    continue
                if not libelle and all(v is None for v in valeurs.values()):
                    continue
                if "(ligne supprimée)" in libelle:
                    if any(valeurs.values()):
                        sys.exit(f"tableau {k}, ligne {r} : ligne supprimée qui porte des crédits")
                    continue
                if not any(v is not None for v in valeurs.values()):
                    if {propre(x) for x in t[r] if propre(x)} <= textes_entete:
                        continue
                    sys.exit(f"tableau {k}, ligne {r} : ligne sans montant (« {libelle} »)")
                if not libelle or set(valeurs) != {"AE", "CP"} or None in valeurs.values():
                    sys.exit(f"tableau {k}, ligne {r} : ligne incomplète (« {libelle} », {valeurs})")
                genre = "total" if re.fullmatch(r"(?i)total|totaux", libelle) else \
                    "dont" if re.fullmatch(rf"(?i){DONT}", libelle) else None
                if genre is None and re.match(r"(?i)(dont|total)\b", libelle):
                    sys.exit(f"tableau {k}, ligne {r} : ligne « {libelle} » inconnue")
                ligne = {"tableau": k, "ligne": r, "libelle": libelle, "nom": nom(libelle), "valeurs": valeurs,
                         "genre": genre, "cases": par_ligne.get(r, {}), "noms": noms, "unite": ouvert["unite"],
                         "notes": notes}
                ouvert["lignes"].append(ligne)
                if genre == "total":
                    ouvert["total"] = ligne
                    blocs.append(ouvert)
                    ouvert = None
        if ouvert is not None:
            sys.exit(f"état {m.group(1)} : tableau sans ligne de total")
        if len(blocs) != len(categories):
            sys.exit(f"état {m.group(1)} : {len(blocs)} tableau(x) de crédits pour {len(categories)} catégorie(s) "
                     f"({', '.join(categories) or 'aucune'})")
        for categorie, bloc in zip(categories, blocs):
            nommees = {c for c, motif in CATEGORIES.items() if re.search(motif, cle_titre(bloc["avant"]))}
            if len(blocs) > 1 and len(nommees) == 1 and nommees != {categorie}:
                sys.exit(f"état {m.group(1)} : le tableau des crédits {categorie} est précédé du titre {nommees.pop()}")
            resultat.append((categorie, bloc))
    return resultat


def egal(a, b):
    return all(abs(a[c] - b[c]) < 0.5 for c in ("AE", "CP"))


def somme(lignes):
    return {c: sum(l["valeurs"][c] for l in lignes) for c in ("AE", "CP")}


def par_marque(ordinaires, marquees):
    """[(mission, programmes)] si les lignes marquées (en gras, ou au contraire non en gras) sont les missions :
    la première ligne en est une, et chacune égale la somme des lignes qui la suivent jusqu'à la suivante ; None
    sinon."""
    if not ordinaires or (ordinaires[0]["tableau"], ordinaires[0]["ligne"]) not in marquees:
        return None
    missions = []
    for l in ordinaires:
        if (l["tableau"], l["ligne"]) in marquees:
            missions.append((l, []))
        else:
            missions[-1][1].append(l)
    return missions if all(programmes and egal(somme(programmes), m["valeurs"]) for m, programmes in missions) else None


def par_sommes(categorie, ordinaires, missions_connues):
    """[(mission, programmes)] d'après les seuls montants : une mission se ferme dès que ses programmes font son
    montant ; une ligne nulle qui suit est un programme de plus, sauf si c'est une mission connue de la base."""
    nulle = lambda l: l["valeurs"]["AE"] == 0 and l["valeurs"]["CP"] == 0
    missions, i = [], 0
    while i < len(ordinaires):
        mission, programmes = ordinaires[i], []
        i += 1
        while not (programmes and egal(somme(programmes), mission["valeurs"])):
            if i == len(ordinaires):
                sys.exit(f"{categorie} : les programmes de la mission « {mission['libelle']} » ne font pas son montant")
            programmes.append(ordinaires[i])
            i += 1
        while i < len(ordinaires) and nulle(ordinaires[i]) and \
                f"LOLF.{code_lolf(ordinaires[i]['nom'])}" not in missions_connues:
            programmes.append(ordinaires[i])
            i += 1
        missions.append((mission, programmes))
    return missions


def structure(categorie, bloc, missions_connues):
    """Rattache chaque ligne à sa mission : {(tableau, ligne) : (libellé, mission ou "")} ; vérifie les sommes. Quand
    le tableau met des lignes en gras, les missions sont ses lignes en gras, ou bien, dans le texte pour 2009, ses
    lignes qui ne le sont pas ; sinon, elles se déduisent des montants (par_sommes)."""
    ordinaires = [l for l in bloc["lignes"] if l["genre"] is None]
    total = bloc["total"]["valeurs"]
    cles = {(l["tableau"], l["ligne"]) for l in ordinaires}
    gras = cles & bloc["gras"]
    if egal(somme(ordinaires), total):  # des missions seules
        if gras and gras != cles:
            sys.exit(f"{categorie} : des missions seules, dont certaines seulement en gras")
        missions = [(l, []) for l in ordinaires]
    elif egal({c: v / 2 for c, v in somme(ordinaires).items()}, total):
        missions = (par_marque(ordinaires, gras) or par_marque(ordinaires, cles - gras)) if gras else \
            par_sommes(categorie, ordinaires, missions_connues)
        if missions is None:
            sys.exit(f"{categorie} : ni ses lignes en gras ni les autres ne sont des missions égales à leurs programmes")
    else:
        sys.exit(f"{categorie} : ses lignes ne font ni son total ni deux fois son total")
    if not egal(somme([m for m, _ in missions]), total):
        sys.exit(f"{categorie} : la somme des missions ne fait pas le total")
    # Une mission sans aucun crédit ne se distingue d'un programme nul que par sa mise en forme : une ligne nulle qui
    # porte le nom d'une mission que la base connaît ne peut pas être un programme d'une autre.
    for mission, programmes in missions:
        for p in programmes:
            if p["valeurs"]["AE"] == 0 and p["valeurs"]["CP"] == 0 and \
                    f"LOLF.{code_lolf(p['nom'])}" in missions_connues and code_lolf(p["nom"]) != code_lolf(mission["nom"]):
                sys.exit(f"{categorie} : la ligne nulle « {p['libelle']} », une mission connue, se range parmi les "
                         f"programmes de la mission « {mission['libelle']} »")
    rattache = {}
    for mission, programmes in missions:
        rattache[(mission["tableau"], mission["ligne"])] = (mission["nom"], "")
        for p in programmes:
            rattache[(p["tableau"], p["ligne"])] = (p["nom"], mission["nom"])
    # Une ligne « dont » appartient au programme qui la précède.
    precedent = None
    for l in bloc["lignes"]:
        if l["genre"] == "dont":
            if precedent is None or not rattache[precedent][1]:
                sys.exit(f"{categorie} : ligne « {l['libelle']} » hors programme (tableau {l['tableau']}, "
                         f"ligne {l['ligne']})")
            rattache[(l["tableau"], l["ligne"])] = rattache[precedent]
        elif l["genre"] is None:
            precedent = (l["tableau"], l["ligne"])
    return rattache


def unite_a(texte):
    """(unité, échelle en euros) qu'annonce un texte (« (En milliers d'euros) »), ou None."""
    trouvees = {m.group(1).lower() for m in re.finditer(UNITE_A, texte.replace("'", "’"), re.I)}
    if len(trouvees) > 1:
        sys.exit(f"état A : unités contradictoires ({', '.join(sorted(trouvees))})")
    return UNITES_A[trouvees.pop()] if trouvees else None


def entete_a(tableau, annee):
    """(lignes d'en-tête, colonne du numéro de ligne ou None, colonne de l'intitulé, colonne de l'évaluation) d'un
    tableau de l'état A, ou None s'il ne nomme pas ses colonnes ; l'évaluation est celle de l'année de la loi."""
    for r, ligne in enumerate(tableau[:4]):
        textes = [propre(x) for x in ligne]
        evaluation = [c for c, x in enumerate(textes) if re.match(r"(?i)[ée]valuation pour [0-9]{4}", x)]
        intitule = [c for c, x in enumerate(textes) if re.match(r"(?i)(?:intitulé|désignation) de", x)]
        numero = [c for c, x in enumerate(textes) if re.match(r"(?i)numéro de ligne", x)]
        if evaluation and intitule:
            if len(evaluation) > 1 or len(intitule) > 1 or len(numero) > 1:
                sys.exit(f"état A : en-tête ambigu ({textes})")
            if not re.match(rf"(?i)[ée]valuation pour {annee}\b", textes[evaluation[0]]):
                sys.exit(f"état A : « {textes[evaluation[0]]} » dans la loi de finances pour {annee}")
            return r + 1, (numero[0] if numero else None), intitule[0], evaluation[0]
    return None


def tableaux_etat_a(grilles, flux, annee, source_id):
    """{partie : [rangée]} : les rangées des tableaux de chaque partie de l'état A (PARTIES_A), dans l'ordre. Une rangée
    est {tableau, ligne, numero, libelle, nombre, valeur, colonne, colonne_libelle, unite, echelle, partiel} ; sa valeur
    est en euros, 0 pour une case « néant », None pour une case vide ; partiel marque une ligne de points, qui tient
    la place des lignes qu'un texte ne reproduit pas."""
    intitules = list(re.finditer(ETAT, flux))
    a = [n for n, m in enumerate(intitules) if m.group(1) == "A"]
    if len(a) != 1:
        sys.exit(f"{len(a)} états A")
    debut = intitules[a[0]].start()
    fin = intitules[a[0] + 1].start() if a[0] + 1 < len(intitules) else len(flux)
    parties, partie, unite_courante, avant = {}, None, None, debut
    for m in re.finditer(r"⟦([0-9]+)⟧", flux[debut:fin]):
        k, p = int(m.group(1)), debut + m.start()
        tableau = grilles[k]
        if re.search(ETAT, " ".join(x for l in tableau for x in l)):
            continue  # intitulé de l'état suivant, mis dans un tableau
        entre, avant = flux[avant:p].replace("'", "’"), flux.index(f"⟦/{k}⟧", p)
        annonces = sorted((t.start(), nom_) for nom_, motif in PARTIES_A if (t := re.search(motif, entre, re.I)))
        if annonces:
            partie, unite_courante = annonces[-1][1], None
        unite_courante = unite_a(entre) or unite_courante
        e = entete_a(tableau, annee)
        textes = [propre(x) for l in tableau for x in l if propre(x)]
        if e is None:
            if textes and all(re.fullmatch(UNITE_A, x.replace("'", "’"), re.I) for x in textes):
                unite_courante = unite_a(" ".join(textes))  # tableau qui ne porte que l'unité des suivants
                continue
            sys.exit(f"état A, tableau {k} : ni en-tête ni unité")
        entete, cn, ci, cv = e
        unite_ = unite_a(" ".join(x for l in tableau[:entete] for x in l)) or unite_courante
        if partie is None or unite_ is None:
            sys.exit(f"état A, tableau {k} : {'partie' if partie is None else 'unité'} inconnue")
        nom_colonne, unite_courante = propre(tableau[entete - 1][cv]), unite_
        for r in range(entete, len(tableau)):
            ligne = tableau[r]
            cases = [propre(nom(x)) for x in ligne]
            if cv < len(cases) and re.match(r"(?i)[ée]valuation pour [0-9]{4}", cases[cv]):
                continue  # en-tête que la page répète au haut d'une nouvelle page
            numero = cases[cn] if cn is not None and re.fullmatch(NUMERO_A, cases[cn]) else ""
            # L'intitulé d'une ligne de total tient parfois dans une autre colonne que celle des intitulés.
            libelle = next((x for c, x in [(ci, cases[ci])] + list(enumerate(cases))
                            if x and c != cv and not (c == cn and numero)), "")
            brut = ligne[cv].strip() if cv < len(ligne) else ""
            nombre = nombre_texte(brut)
            partiel = any(re.fullmatch(r"\.{3,}", x.strip()) for x in ligne)
            if nombre is None and brut and brut not in NEANT and not partiel:
                sys.exit(f"état A, tableau {k}, ligne {r} : montant illisible (« {brut} »)")
            if [c for c, x in enumerate(ligne) if c not in (cn, ci, cv) and nombre_texte(x)]:
                sys.exit(f"état A, tableau {k}, ligne {r} : montant hors de la colonne de l'évaluation")
            valeur = float(nombre[0]) * unite_[1] if nombre else 0 if brut in NEANT and brut else None
            parties.setdefault(partie, []).append(
                {"tableau": k, "ligne": r, "numero": numero, "libelle": libelle, "nombre": nombre, "valeur": valeur,
                 "colonne": cv, "colonne_libelle": nom_colonne, "unite": unite_[0], "echelle": unite_[1],
                 "partiel": partiel, "source": source_id, "note": ""})
    return parties


def numero_division(numero):
    """« 13bis » → « 13 bis »."""
    return re.sub(r"([0-9])(bis|ter|quater)", r"\1 \2", numero)


def ou(g):
    return f"tableau {g['tableau']}, ligne {g['ligne']}"


def verifier_somme(total, parties, quoi, nom_=None):
    """Un total (une rangée) égale la somme de ses parties (des rangées), aux arrondis près : la demi-unité de la page
    pour chaque montant en jeu, comme dans le rapport de cohérence (une page qui arrondit à l'euro des montants calculés
    au centime en laisse un écart d'un euro ou deux). Un écart plus grand arrête l'import, sauf s'il est déclaré dans
    ECARTS_A pour le total `nom_` (son libellé, à défaut), que porte alors la note du total."""
    somme = sum(g["valeur"] or 0 for g in parties)
    nom_ = nom_ or total["libelle"]
    ecart = (total["valeur"] or 0) - somme
    marge = 0.5 * total["echelle"] * (len(parties) + 1)
    declare = ECARTS_A.get((total["source"], nom_))
    if declare is not None and abs(ecart - declare) < 0.5 * total["echelle"]:
        ECARTS_VUS.add((total["source"], nom_))
        lisible = lambda x: f"{x:,.0f}".replace(",", "\u202f")
        total["note"] = (f"La page donne {lisible(total['valeur'])} € pour « {nom_} », et ses lignes en font "
                         f"{lisible(somme)} €, {lisible(abs(ecart))} € de {'moins' if ecart > 0 else 'plus'}.")
    elif abs(ecart) > marge:
        sys.exit(f"état A, {ou(total)} : {quoi} « {nom_} » vaut {total['valeur'] or 0:,.0f} €, ses parties "
                 f"{somme:,.0f} €")


def budget_general_a(rangees):
    """Divisions du tableau détaillé du budget général, chacune {numero, libelle, categorie, rangee, lignes}, et les
    rangées de sa catégorie 4 (fonds de concours) ; None si le texte ne reproduit pas le tableau entier (texte de la
    commission mixte paritaire de 2006, qui n'en garde que les lignes modifiées)."""
    if any(g["partiel"] for g in rangees):
        return None, None
    divisions, categorie, division, fonds = [], None, None, []
    for g in rangees:
        libelle, numero = g["libelle"], g["numero"]
        if not libelle and not numero:
            if g["nombre"]:
                sys.exit(f"état A, {ou(g)} : montant sans intitulé")
            continue
        if not numero and (m := re.fullmatch(CATEGORIE_A, libelle)):
            categorie, division = m.group(1), None
            if categorie == "4" and g["valeur"] is not None:
                fonds.append(g)
            continue
        if categorie == "4" and not numero and re.fullmatch(FONDS_DE_CONCOURS_A, libelle):
            fonds.append(g)
            continue
        if categorie in (None, "4"):
            sys.exit(f"état A, {ou(g)} : « {libelle} » hors des catégories de recettes")
        if not numero and (m := re.fullmatch(DIVISION_A, libelle)):
            if not m.group(1).startswith(categorie):
                sys.exit(f"état A, {ou(g)} : division « {libelle} » dans la catégorie {categorie}")
            division = {"numero": numero_division(m.group(1)), "libelle": m.group(2), "categorie": categorie, "rangee": g, "lignes": []}
            divisions.append(division)
            continue
        if division is None or (numero and not re.fullmatch(r"[0-9]{4}", numero)) or \
                (numero and not numero.startswith(division["numero"][:2])) or (not numero and g["valeur"] is None):
            sys.exit(f"état A, {ou(g)} : ligne « {numero} {libelle} » inconnue")
        division["lignes"].append(g)
    for d in divisions:
        if d["rangee"]["valeur"] is None or not d["lignes"]:
            sys.exit(f"état A, {ou(d['rangee'])} : division sans montant ou sans ligne")
        # Une ligne sans numéro n'est admise que seule dans sa division (la division 18, depuis la loi pour 2023).
        if len(d["lignes"]) > 1 and any(not g["numero"] for g in d["lignes"]):
            sys.exit(f"état A, {ou(d['rangee'])} : ligne sans numéro dans la division « {d['libelle']} »")
        verifier_somme(d["rangee"], d["lignes"], "la division")
    return divisions, fonds


def recapitulation_a(rangees):
    """Catégories de la récapitulation des recettes du budget général, chacune {rangee, divisions : [(numéro, libellé,
    rangée)], fonds : [rangée]}, et ses totaux {"1+2", "1+2-3"} ; dans le texte pour 2006, les parties A à D sont les
    catégories 1 à 4, et la division 1 de la partie A la division 11."""
    categories, totaux, categorie, finie = {}, {}, None, False
    for g in rangees:
        libelle, numero = g["libelle"], g["numero"]
        if finie or re.match(r"II\.\s*-", libelle):
            if g["nombre"]:
                sys.exit(f"état A, {ou(g)} : montant après la récapitulation")
            finie = True  # texte pour 2006, qui énumère ensuite les autres parties de l'état sans les reproduire
            continue
        if not libelle and not numero:
            continue
        m = None if numero else re.fullmatch(CATEGORIE_A, libelle) or re.fullmatch(LETTRE_A, libelle)
        if m:
            categorie = m.group(1) if m.group(1).isdigit() else str("ABCD".index(m.group(1)) + 1)
            categories[categorie] = {"rangee": g if g["valeur"] is not None else None, "divisions": [], "fonds": []}
        elif re.fullmatch(r"Totaux pour la partie [A-D]", libelle) and categorie:
            categories[categorie]["rangee"] = g
        elif re.fullmatch(r"Total des recettes (?:brutes|fiscales et non fiscales)(?: \(1 ?\+ ?2\))?", libelle):
            totaux["1+2"] = g
        elif re.fullmatch(r"Total des recettes,? nettes des prélèvements(?: \(1 ?\+ ?2 ?- ?3\))?|"
                          r"Total des recettes A \+ B - C", libelle):
            totaux["1+2-3"] = g
        elif categorie == "4" and re.fullmatch(FONDS_DE_CONCOURS_A, libelle):
            categories["4"]["fonds"].append(g)
        elif numero and categorie in ("1", "2", "3"):
            categories[categorie]["divisions"].append((numero_division(numero) if len(numero) > 1 else categorie + numero,
                                                       libelle, g))
        elif not numero and categorie in ("1", "2", "3") and (d := re.fullmatch(DIVISION_A, libelle)):
            categories[categorie]["divisions"].append((numero_division(d.group(1)), d.group(2), g))
        else:
            sys.exit(f"état A, {ou(g)} : ligne « {numero} {libelle} » de la récapitulation inconnue")
    if sorted(categories) != ["1", "2", "3", "4"] or any(c["rangee"] is None for n, c in categories.items() if n != "4"):
        sys.exit(f"état A : récapitulation incomplète ({', '.join(sorted(categories))})")
    for n in ("1", "2", "3"):
        verifier_somme(categories[n]["rangee"], [g for _, _, g in categories[n]["divisions"]], "la catégorie")
    fonds = [g for g in [categories["4"]["rangee"]] + categories["4"]["fonds"] if g and g["valeur"] is not None]
    if not fonds or len({g["valeur"] for g in fonds}) > 1:
        sys.exit("état A : fonds de concours de la récapitulation absents ou discordants")
    c = {n: categories[n]["rangee"]["valeur"] for n in ("1", "2", "3")}
    for cle, attendu in (("1+2", c["1"] + c["2"]), ("1+2-3", c["1"] + c["2"] - c["3"])):
        g = totaux.get(cle)
        if g and abs(g["valeur"] - attendu) >= 0.5 * g["echelle"]:
            sys.exit(f"état A, {ou(g)} : « {g['libelle']} » vaut {g['valeur']:,.0f} €, ses catégories {attendu:,.0f} €")
    return categories, totaux


def budgets_annexes_a(rangees, connus):
    """Chaque budget annexe de l'état A : {nom, rangee, sections : [{nom, rangee, lignes, total}], lignes, deductions,
    total, fonds}. Un budget annexe s'annonce par son nom, que `connus` (identifiants) doit contenir ; jusqu'à la loi pour
    2008, ses lignes se rangent en sections, et ses dotations aux amortissements se déduisent de leur somme."""
    budgets, budget, section, deduire = [], None, None, False
    for g in rangees:
        libelle, numero = g["libelle"], g["numero"]
        if not libelle and not numero:
            continue
        if not numero and f"LOLF.{code_lolf(libelle)}" in connus:
            budget = {"nom": libelle, "rangee": g, "sections": [], "lignes": [], "deductions": [], "total": None,
                      "fonds": None}
            budgets.append(budget)
            section, deduire = None, False
            continue
        if budget is None or (budget["total"] and not re.fullmatch(FONDS_DE_CONCOURS_A, libelle)):
            sys.exit(f"état A, {ou(g)} : « {libelle} » hors d'un budget annexe")
        if not numero and re.fullmatch(SECTIONS_BA, libelle):
            section = {"nom": libelle, "rangee": g, "lignes": [], "total": None}
            budget["sections"].append(section)
        elif not numero and libelle.startswith("Total des recettes brutes en"):
            if section is None:
                sys.exit(f"état A, {ou(g)} : « {libelle} » hors d'une section")
            section["total"], section = g, None
        elif not numero and libelle == "À déduire :":
            section, deduire = None, True
        elif not numero and re.fullmatch(TOTAL_BA, libelle):
            budget["total"] = g
        elif not numero and re.fullmatch(FONDS_DE_CONCOURS_A, libelle):
            budget["fonds"] = g
        else:
            (budget["deductions"] if deduire else section["lignes"] if section else budget["lignes"]).append(g)
    for b in budgets:
        if b["total"] is None or any(s["total"] is None for s in b["sections"]):
            sys.exit(f"état A, budget annexe « {b['nom']} » sans total")
        for s in b["sections"]:
            verifier_somme(s["total"], s["lignes"], "la section")
        verifier_somme(b["total"], [s["total"] for s in b["sections"]] + b["lignes"] + b["deductions"],
                       "le budget annexe", b["nom"])
        if b["rangee"]["valeur"] is not None:
            verifier_somme(b["rangee"], [b["total"]] + ([b["fonds"]] if b["fonds"] else []), "le budget annexe")
    return budgets


def comptes_speciaux_a(rangees, connus, categorie):
    """Chaque compte d'affectation spéciale ou de concours financiers de l'état A : {nom, rangee, sections : [{nom,
    rangee, lignes}], lignes}, et la rangée du total de la partie. Un compte s'annonce par son nom, que `connus`
    (identifiants) doit contenir, une section par « Section : », une ligne par son numéro."""
    comptes, compte, section, total = [], None, None, None
    for g in rangees:
        libelle, numero = g["libelle"], g["numero"]
        if not libelle and not numero:
            continue
        if total:
            sys.exit(f"état A, {ou(g)} : « {libelle} » après le total des comptes")
        if not numero and re.fullmatch(TOTAL_CS, libelle):
            total = g
        elif not numero and (m := re.fullmatch(SECTION_CS, libelle)):
            if compte is None:
                sys.exit(f"état A, {ou(g)} : section hors d'un compte")
            section = {"nom": m.group(1), "rangee": g, "lignes": []}
            compte["sections"].append(section)
        elif numero:
            if compte is None or (compte["sections"] and section is None):
                sys.exit(f"état A, {ou(g)} : ligne « {numero} {libelle} » hors d'un compte ou d'une section")
            (section or compte)["lignes"].append(g)
        elif f"LOLF.{code_lolf(libelle)}" in connus:
            compte = {"nom": libelle, "rangee": g, "sections": [], "lignes": []}
            comptes.append(compte)
            section = None
        else:
            sys.exit(f"état A, {ou(g)} : « {libelle} », compte {categorie} inconnu")
    if total is None or not comptes:
        sys.exit(f"état A : comptes {categorie} sans total")
    for c in comptes:
        for s in c["sections"]:
            verifier_somme(s["rangee"], s["lignes"], "la section")
        verifier_somme(c["rangee"], [s["rangee"] for s in c["sections"]] + c["lignes"], "le compte")
    verifier_somme(total, [c["rangee"] for c in comptes], "le total")
    return comptes, total


def recettes_a(parties, budgets_connus, comptes_connus):
    """[(concept, fonction, libellé de la fonction, parent, rangée)] : les montants de l'état A à enregistrer, et
    "nettes" ou "brutes", selon que les recettes fiscales du budget général s'entendent nettes ou brutes des
    remboursements et dégrèvements. `budgets_connus`, `comptes_connus` : identifiants des budgets annexes et, par
    catégorie, des comptes spéciaux."""
    if "BG" not in parties or "RECAPITULATION" not in parties:
        sys.exit("état A sans tableau du budget général ou sans récapitulation")
    divisions, fonds = budget_general_a(parties["BG"])
    categories, totaux = recapitulation_a(parties["RECAPITULATION"])
    nettes = any(n == "18" for n, _, _ in categories["1"]["divisions"])
    if nettes != any(re.search(r"(?i)remboursements et dégrèvements", l) for n, l, _ in categories["1"]["divisions"]):
        sys.exit("état A : division des remboursements et dégrèvements sans le numéro 18, ou l'inverse")
    sorte = "NETTES" if nettes else "BRUTES"
    concept_ = lambda c: RECETTES_BG[c].format(sorte)
    montants = []
    if divisions is None:  # la récapitulation seule donne les divisions
        for c in ("1", "2", "3"):
            for numero, libelle, g in categories[c]["divisions"]:
                f = f"LOLF.RECETTES.{code_lolf(numero + ' ' + libelle)}"
                montants.append((concept_(c), f, f"{numero}. {libelle}", "", g))
    else:
        recap = {n: g["valeur"] for c in ("1", "2", "3") for n, _, g in categories[c]["divisions"]}
        if recap != {d["numero"]: d["rangee"]["valeur"] for d in divisions}:
            sys.exit("état A : les divisions du tableau détaillé et de la récapitulation diffèrent")
        if any(g["valeur"] != (categories["4"]["rangee"] or categories["4"]["fonds"][0])["valeur"] for g in fonds):
            sys.exit("état A : fonds de concours du tableau détaillé et de la récapitulation discordants")
        for d in divisions:
            f = f"LOLF.RECETTES.{code_lolf(d['numero'] + ' ' + d['libelle'])}"
            montants.append((concept_(d["categorie"]), f, f"{d['numero']}. {d['libelle']}", "", d["rangee"]))
            for g in d["lignes"]:
                nom_ = f"{g['numero']} {g['libelle']}".strip()
                montants.append((concept_(d["categorie"]), f"{f}.{code_lolf(nom_)}", nom_, f, g))
    for c in ("1", "2", "3"):
        montants.append((concept_(c), "", "", "", categories[c]["rangee"]))
    fdc = categories["4"]["rangee"] or categories["4"]["fonds"][0]
    montants.append((concept_("4"), "", "", "", fdc))
    if nettes:  # les totaux de la récapitulation s'entendent alors comme ceux de l'exécution
        montants += [("LOLF.BG_RECETTES_NETTES_HORS_FDC_LFI", "", "", "", totaux["1+2"]),
                     ("LOLF.BG_RECETTES_NETTES_HORS_PSR_LFI", "", "", "", totaux["1+2-3"])]
    for b in budgets_annexes_a(parties.get("BA", []), budgets_connus):
        f = f"LOLF.{code_lolf(b['nom'])}"
        montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFI", f, b["nom"], "", b["total"]))
        if b["rangee"]["nombre"]:
            montants.append(("LOLF.BA_RECETTES_LFI", f, b["nom"], "", b["rangee"]))
        if b["fonds"] and b["fonds"]["nombre"]:
            montants.append(("LOLF.BA_FDC_RECETTES_LFI", f, b["nom"], "", b["fonds"]))
        groupes = [(f"{f}.{code_lolf(s['nom'])}", s["nom"], s["lignes"], s["total"]) for s in b["sections"]]
        for fs, nom_s, lignes, total in groupes:
            montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFI", fs, nom_s, f, total))
        for parent, lignes in [(fs, lignes) for fs, _, lignes, _ in groupes] + [(f, b["lignes"])]:
            for g in lignes:
                nom_ = f"{g['numero']} {g['libelle']}".strip()
                montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFI", f"{parent}.{code_lolf(nom_)}", nom_, parent, g))
        for g in b["deductions"]:
            nom_ = f"À déduire : {g['numero']} {g['libelle']}".replace("  ", " ")
            montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFI", f"{f}.{code_lolf(nom_)}", nom_, f, g))
    for categorie in ("CAS", "CCF"):
        if categorie not in parties:
            continue
        comptes, total = comptes_speciaux_a(parties[categorie], comptes_connus[categorie], categorie)
        c_ = f"LOLF.{categorie}_RECETTES_LFI"
        montants.append((c_, "", "", "", total))
        for compte in comptes:
            f = f"LOLF.{code_lolf(compte['nom'])}"
            montants.append((c_, f, compte["nom"], "", compte["rangee"]))
            for parent, nom_p, lignes, g_p in [(f, None, compte["lignes"], None)] + \
                    [(f"{f}.{code_lolf(s['nom'])}", s["nom"], s["lignes"], s["rangee"]) for s in compte["sections"]]:
                if nom_p:
                    montants.append((c_, parent, nom_p, f, g_p))
                for g in lignes:
                    nom_ = f"{g['numero']} {g['libelle']}".strip()
                    montants.append((c_, f"{parent}.{code_lolf(nom_)}", nom_, parent, g))
    return [m for m in montants if m[4]["nombre"]], sorte


def equilibre(grilles, flux, annee):
    """Les montants du tableau de l'article d'équilibre, en millions d'euros : [(rubrique, clé de EQUILIBRE, fonction,
    côté R, C ou S, rangée)]. Une rangée est {tableau, ligne, colonne, libelle, colonne_libelle, nombre, valeur} ; sa
    valeur est 0 pour une case « néant »."""
    trouves = [k for k, t in enumerate(grilles)
               if any(l and re.sub(r"\*+", "", propre(l[0])) == "Solde général" for l in t)]
    if len(trouves) != 1:
        sys.exit(f"{len(trouves)} tableaux d'équilibre")
    k = trouves[0]
    p = flux.index(f"⟦{k}⟧")
    if not re.search(rf"Pour {annee},? les ressources affectées au budget", flux[max(0, p - 800):p].replace("'", "’")):
        sys.exit(f"tableau d'équilibre : l'article qui le précède n'est pas celui de la loi pour {annee}")
    t = grilles[k]
    entete, cols = None, {}
    for r, ligne in enumerate(t[:5]):
        for c, x in enumerate(ligne):
            x = propre(x)
            for cote, motif in (("R", r"Ressources"), ("C", r"Dépenses|Charges"), ("S", r"Soldes?\b")):
                if re.match(motif, x) and cote not in cols:
                    cols[cote], entete = (c, x), r
    annonce = flux[max(0, p - 300):p] + " ".join(x for l in t[:entete + 1] for x in l)
    if sorted(cols) != ["C", "R", "S"] or not re.search(r"(?i)\(\s*en millions d’euros\s*\*?\s*\)",
                                                        annonce.replace("'", "’")):
        sys.exit(f"tableau d'équilibre : colonnes ou unité inconnues ({cols})")
    # Depuis la loi pour 2023, chaque colonne de ressources et de charges se détaille en fonctionnement et
    # investissement, sous les numéros 1 (total), 2 et 3 ; seul le total est lu.
    sous_colonnes = set()
    if entete + 1 < len(t) and [propre(x) for x in t[entete + 1][cols["R"][0]:cols["R"][0] + 3]] == ["1", "2", "3"]:
        entete += 1
        sous_colonnes = {cols[c][0] + d for c in ("R", "C") for d in (1, 2)}
    montants, rubrique, bloc = [], None, None
    for r in range(entete + 1, len(t)):
        ligne = t[r]
        libelle = re.sub(r"^-\s*", "", re.sub(r"\*+", "", propre(nom(ligne[0])))).strip()
        libelle = re.sub(r"^A déduire", "À déduire", re.sub(r"^Evaluation", "Évaluation", libelle))
        nombres = {c: (n, float(n[0])) for c, x in enumerate(ligne) if c and (n := nombre_texte(x))}
        neants = {c for c, x in enumerate(ligne) if c and x.strip() in NEANT}
        if not libelle and not nombres:
            continue
        if libelle.startswith("Les montants figurant dans le présent tableau"):
            continue  # note sur les arrondis
        if libelle in RUBRIQUES_EQUILIBRE:
            rubrique = bloc = RUBRIQUES_EQUILIBRE[libelle]
            continue
        if rubrique == "BA" and re.fullmatch(FDC_EQUILIBRE, libelle) and not nombres:
            bloc = "BA_FDC"
            continue
        if bloc is None:
            sys.exit(f"tableau d'équilibre, ligne {r} : « {libelle} » hors d'une rubrique")
        table = EQUILIBRE[bloc]
        cle_ = {k.lower(): k for k in table}.get(libelle.lower(), "" if bloc in ("BA", "BA_FDC") else None)
        if cle_ is None:
            sys.exit(f"tableau d'équilibre, ligne {r} : « {libelle} » inconnu")
        fonction = f"LOLF.{code_lolf(libelle)}" if cle_ == "" else ""
        if table[cle_][:2] == (None, None):  # ligne d'un seul solde, où qu'il soit dans la ligne
            if len(nombres) != 1:
                sys.exit(f"tableau d'équilibre, ligne {r} : « {libelle} » sans montant unique")
            c, (n, v) = next(iter(nombres.items()))
            montants.append((bloc, cle_, fonction, "S", {"tableau": k, "ligne": r, "colonne": c, "libelle": libelle,
                                                         "colonne_libelle": cols["S"][1], "nombre": n, "valeur": v}))
            continue
        hors = set(nombres) - {cols[c][0] for c in cols} - sous_colonnes
        if hors:
            sys.exit(f"tableau d'équilibre, ligne {r} : montant hors des colonnes ({sorted(hors)})")
        for cote in ("R", "C", "S"):
            c = cols[cote][0]
            if c in nombres or c in neants:
                n, v = nombres.get(c, (None, 0))
                if table[cle_]["RCS".index(cote)] is None:
                    if v:
                        sys.exit(f"tableau d'équilibre, ligne {r} : « {libelle} », montant inattendu ({cote})")
                    continue
                montants.append((bloc, cle_, fonction, cote, {"tableau": k, "ligne": r, "colonne": c,
                                                              "libelle": libelle, "colonne_libelle": cols[cote][1],
                                                              "nombre": n, "valeur": v}))
    return montants


def verifier_equilibre(montants, sorte):
    """Le tableau d'équilibre s'additionne, à l'arrondi au million près de chacun de ses montants ; un montant que deux
    lignes donnent y est le même."""
    v = {}
    for bloc, cle_, fonction, cote, g in montants:
        v.setdefault((EQUILIBRE[bloc][cle_]["RCS".index(cote)], fonction, cote), set()).add(g["valeur"])
    for cle_, valeurs in v.items():
        if len(valeurs) > 1:
            sys.exit(f"tableau d'équilibre : {cle_} vaut tour à tour {sorted(valeurs)}")
    x = {cle_: valeurs.pop() for cle_, valeurs in v.items()}
    budgets = sorted({f for (_, f, _) in x if f})
    # (signe, concept, côté, fonction) ; une fonction nulle désigne chaque budget annexe, un « ? » un terme facultatif,
    # qui vaut zéro quand le tableau ne le donne pas (une ligne sans solde, un budget annexe sans fonds de concours).
    identites = [
        ("BG_RECETTES_NETTES_HORS_FDC R", ["BG_RECETTES_FISCALES_NETTES R", "BG_RECETTES_NON_FISCALES R"]),
        ("BG_RECETTES_NETTES_HORS_PSR R", ["BG_RECETTES_NETTES_HORS_FDC R", "-BG_PRELEVEMENTS_SUR_RECETTES R"]),
        ("BG_RECETTES_NETTES R", ["BG_RECETTES_NETTES_HORS_PSR R", "BG_FONDS_DE_CONCOURS_RECETTES R"]),
        ("BG_DEPENSES_NETTES C", ["BG_DEPENSES_NETTES_HORS_FDC C", "BG_FONDS_DE_CONCOURS_RECETTES C"]),
        ("SOLDE_BUDGET_GENERAL S", ["BG_RECETTES_NETTES_HORS_PSR R", "-BG_DEPENSES_NETTES_HORS_FDC C"]),
        ("BA_RECETTES_HORS_FDC R", ["BA_RECETTES_HORS_FDC R *"]),
        ("BA_CP C", ["BA_CP C *"]),
        ("?BA_SOLDE_HORS_FDC S", ["?BA_SOLDE_HORS_FDC S *"]),
        ("BA_RECETTES R", ["BA_RECETTES_HORS_FDC R", "?BA_FDC_RECETTES R *"]),
        ("BA_CHARGES C", ["BA_CP C", "?BA_FDC_RECETTES C *"]),
        ("?SOLDE_BUDGETS_ANNEXES S", ["BA_RECETTES R", "-BA_CHARGES C"]),
        ("CAS_SOLDE S", ["CAS_RECETTES R", "-CAS_CP C"]),
        ("CCF_SOLDE S", ["CCF_RECETTES R", "-CCF_CP C"]),
        ("SOLDE_COMPTES_SPECIAUX S", ["CAS_SOLDE S", "CCF_SOLDE S", "COMPTES_COMMERCE_SOLDE S",
                                      "OPERATIONS_MONETAIRES_SOLDE S"]),
        ("RESULTAT_BUDGETAIRE S", ["SOLDE_BUDGET_GENERAL S", "?BA_SOLDE_HORS_FDC S", "SOLDE_COMPTES_SPECIAUX S"]),
    ]
    identites += [(f"?BA_SOLDE_HORS_FDC S {f}", [f"BA_RECETTES_HORS_FDC R {f}", f"-BA_CP C {f}"]) for f in budgets]
    if sorte == "BRUTES":
        identites += [("BG_RECETTES_FISCALES_NETTES R", ["BG_RECETTES_FISCALES_BRUTES R",
                                                         "-BG_REMBOURSEMENTS_DEGREVEMENTS R"]),
                      ("BG_DEPENSES_NETTES_HORS_FDC C", ["BG_CP C", "-BG_REMBOURSEMENTS_DEGREVEMENTS C"])]

    def termes(spec):
        signe, facultatif = (-1 if "-" in spec[:2] else 1), "?" in spec[:2]
        concept_, cote, *fonction = spec.lstrip("-?").split()
        fonctions = budgets if fonction == ["*"] else fonction or [""]
        valeurs = [x.get((concept_, f, cote)) for f in fonctions]
        if None in valeurs and not facultatif:
            return None
        return [signe * (v or 0) for v in valeurs]

    for total, parties in identites:
        t = termes(total)
        if t is None or (total.startswith("?") and (total.split()[0].lstrip("?"), (total.split()[2:] or [""])[0],
                                                     total.split()[1]) not in x):
            continue  # le tableau ne donne pas ce total
        p = [termes(s) for s in parties]
        if None in p:
            sys.exit(f"tableau d'équilibre : un terme de {total} manque ({parties})")
        somme = sum(sum(q) for q in p)
        if abs(t[0] - somme) > 0.5 * (sum(len(q) for q in p) + 1) + 1e-9:
            sys.exit(f"tableau d'équilibre : {total} vaut {t[0]}, ses parties {somme} ({parties})")


def credits_200(connus, fonctions):
    """Crédits de paiement du programme 200, « Remboursements et dégrèvements d'impôts d'État », dans l'état B."""
    trouves = [v for (c, f), v in connus.items() if c == "LOLF.BG_CP_LFI" and
               f.startswith("LOLF.REMBOURSEMENTS_ET_DEGREVEMENTS.") and
               re.match(r"Remboursements et dégrèvements d[’']impôts d[’']État", fonctions[f]["libelle"])]
    if len(trouves) != 1:
        sys.exit(f"état B : {len(trouves)} programmes des remboursements et dégrèvements d'impôts d'État")
    return trouves[0]


def financement(grilles, flux, annee, source_id):
    """Les lignes du tableau de financement de l'article d'équilibre, en milliards d'euros, dans l'ordre du tableau :
    [(rubrique, concept, dont, rangée)], dont vrai pour une ligne « Dont … ». Une rangée est {tableau, ligne, colonne,
    morceau, libelle, nombre, valeur} ; sa valeur est 0 pour une case « néant ». Une case déclarée dans
    FUSIONS_FINANCEMENT, qui réunit plusieurs lignes, se lit montant par montant, que `morceau` numérote."""
    trouves = [k for k, t in enumerate(grilles) if any(l and resultats.forme(l[0]) == "besoin de financement" for l in t)]
    if len(trouves) != 1:
        sys.exit(f"{len(trouves)} tableaux de financement")
    k = trouves[0]
    p = flux.index(f"⟦{k}⟧")
    # Les marques d'alinéa que la page du Sénat de 2025 tire d'une police de symboles (zone d'usage privé d'Unicode)
    # ne sont pas du texte.
    avant = re.sub(r"\s+", " ", re.sub(r"[\ue000-\uf8ff]", " ", flux[max(0, p - 400):p]).replace("'", "’"))
    if not re.search(rf"Pour {annee}\s*:\s*1° Les ressources et les charges de trésorerie qui concourent à la réalisation "
                     rf"de l’équilibre financier sont évaluées comme suit", avant):
        sys.exit(f"tableau de financement : l'article qui le précède n'est pas celui de la loi pour {annee}")
    t, unite_ = grilles[k], r"\(\s*en milliards d’euros\s*\)"
    if not re.search(unite_, (avant[-100:] + " ".join(x for l in t[:3] for x in l)).replace("'", "’"), re.I):
        sys.exit("tableau de financement : unité inconnue")
    lignes, rubrique = [], None
    for r, ligne in enumerate(t):
        textes = [propre(x) for x in ligne if propre(x) and propre(x) != ";"]
        if not textes or all(re.fullmatch(unite_, x.replace("'", "’"), re.I) for x in textes):
            continue
        libelle = propre(nom(ligne[0]))
        cases = [(c, x.strip()) for c, x in enumerate(ligne) if c and x.strip() and x.strip() != ";"]
        if resultats.forme(libelle) in resultats.RUBRIQUES_FINANCEMENT_ and not cases:
            rubrique = resultats.RUBRIQUES_FINANCEMENT_[resultats.forme(libelle)]
            continue
        if rubrique is None or len(cases) != 1:
            sys.exit(f"tableau de financement, ligne {r} : « {libelle} », {len(cases)} montant(s)"
                     + ("" if rubrique else " hors d'une rubrique"))
        c, case = cases[0]
        libelles = FUSIONS_FINANCEMENT.get((source_id, libelle))
        if libelles is not None:
            nombres = montants_de_case(case)
            if " ".join(libelles) != libelle or nombres is None or len(nombres) != len(libelles):
                sys.exit(f"tableau de financement, ligne {r} : case fusionnée « {case} » autre que déclarée")
            parties = [(n + 1, l, x) for n, (l, x) in enumerate(zip(libelles, nombres))]
        else:
            neant = case.replace("\u2011", "-") in NEANT
            nombre_ = None if neant else nombre_texte(case)
            if nombre_ is None and not neant:
                sys.exit(f"tableau de financement, ligne {r} : montant illisible (« {case} »)")
            parties = [(None, libelle, nombre_)]
        for morceau, libelle_, nombre_ in parties:
            concept_ = FINANCEMENT_LFI.get((rubrique, resultats.forme(libelle_)))
            if concept_ is None:
                sys.exit(f"tableau de financement, ligne {r} : « {libelle_} » inconnu ({rubrique})")
            lignes.append((rubrique, concept_, libelle_.startswith("Dont "),
                           {"tableau": k, "ligne": r, "colonne": c, "morceau": morceau, "libelle": libelle_,
                            "nombre": nombre_, "valeur": float(nombre_[0]) if nombre_ else 0.0}))
    return lignes


def verifier_financement(lignes, solde_general, plafond):
    """Le tableau de financement s'additionne exactement : ses montants sont publiés au dixième de milliard, et les
    lois pour 2006 à 2026 en donnent des totaux qui en sont la somme exacte. Le besoin et les ressources sont chacun la
    somme de leurs lignes, hors lignes « Dont … », et sont égaux ; une ligne que des lignes « Dont … » détaillent est
    leur somme ; le plafond de la variation de la dette (`plafond`, en milliards d'euros) est les émissions de dette à
    moyen et long termes moins l'amortissement de leur nominal. Le déficit budgétaire est l'opposé du solde général de
    l'article d'équilibre (`solde_general`, en millions d'euros), à son arrondi au dixième de milliard près."""
    v = {}
    for _, concept_, _, g in lignes:
        if concept_ in v:
            sys.exit(f"tableau de financement : {concept_} deux fois")
        v[concept_] = g["valeur"]
    egal_ = lambda a, b: abs(a - b) < 1e-6  # aux imprécisions du calcul en virgule flottante près
    for rubrique, total in TOTAUX_FINANCEMENT.items():
        parties = [g["valeur"] for r, c, dont, g in lignes if r == rubrique and not dont and c != total]
        if total not in v or not egal_(v[total], sum(parties)):
            sys.exit(f"tableau de financement : {total} vaut {v.get(total)}, ses lignes {sum(parties):.1f}")
    if not egal_(v["LOLF.BESOIN_FINANCEMENT"], v["LOLF.RESSOURCES_FINANCEMENT"]):
        sys.exit("tableau de financement : besoin et ressources diffèrent")
    detaillee, details = None, []
    for _, concept_, dont, g in lignes + [(None, None, False, None)]:
        if dont:
            details.append(g["valeur"])
            continue
        if details and not egal_(v[detaillee], sum(details)):
            sys.exit(f"tableau de financement : {detaillee} vaut {v[detaillee]}, ses lignes « Dont » {sum(details):.1f}")
        detaillee, details = concept_, []
    deficit = v.get("LOLF.DEFICIT_A_FINANCER_DEFICIT_BUDGETAIRE", v.get("LOLF.DEFICIT_A_FINANCER"))
    if deficit is None or abs(deficit * 1e3 + solde_general) > 50.5:  # 50 M€ d'arrondi, et 0,5 M€ pour le solde
        sys.exit(f"tableau de financement : déficit budgétaire {deficit} Md€, solde général {solde_general} M€")
    if "LOLF.AMORTISSEMENT_DETTE_NOMINAL" in v:
        nominal = v["LOLF.AMORTISSEMENT_DETTE_NOMINAL"]
    elif "LOLF.AMORTISSEMENT_DETTE_MLT" in v:
        nominal = v["LOLF.AMORTISSEMENT_DETTE_MLT"] - v.get("LOLF.SUPPLEMENTS_INDEXATION", 0)
    else:
        nominal = v.get("LOLF.AMORTISSEMENT_DETTE_LT", 0) + v.get("LOLF.AMORTISSEMENT_DETTE_MT", 0)
    variation = v.get("LOLF.EMISSIONS_DETTE_MLT", 0) - nominal
    if not egal_(plafond, variation):
        sys.exit(f"plafond de la variation de la dette : {plafond} Md€, émissions moins amortissement {variation:.1f}")


def tableaux_emplois(grilles, formes, flux, annee):
    """{sorte : (tableau, phrase, unité)} : le tableau de chaque plafond d'emplois de la seconde partie de la loi,
    reconnu à la phrase qui l'annonce, entre le tableau qui porte des nombres avant lui et son début ; un tableau sans
    nombre (un intitulé d'article mis en tableau) ne compte pas."""
    trouves, fin = {}, 0
    for m in re.finditer(r"⟦([0-9]+)⟧", flux):
        k = int(m.group(1))
        if not any(nombre_texte(x) for l in grilles[k] for x in l[1:]):
            continue
        entre = re.sub(r"\s+", " ", re.sub(r"[\ue000-\uf8ff]|⟦/?[0-9]+⟧", " ", flux[fin:m.start()])).replace("'", "’")
        fin = flux.index(f"⟦/{k}⟧", m.start())
        i = entre.rfind("Article ")
        phrase = entre[i:].strip() if i >= 0 else ""
        if "plafond des autorisations d’emplois" not in phrase or not re.search(r"comme suit\s*:$", phrase):
            continue
        sortes = [s for s, motif in EMPLOIS.items() if re.search(motif, phrase)]
        unites = {UNITES_EMPLOIS[u] for u in re.findall(r"en (équivalents? temps plein(?: travaillé)?)", phrase)}
        if len(sortes) != 1 or len(unites) != 1 or not re.search(rf"\b[Pp]our {annee}\b", phrase):
            sys.exit(f"tableau {k} : plafond d'emplois de sorte, d'unité ou d'année inconnue (« {phrase[:160]} »)")
        if sortes[0] in trouves:
            sys.exit(f"plafond d'emplois {sortes[0]} : deux tableaux")
        trouves[sortes[0]] = (k, phrase, unites.pop())
    attendus = {s for s, a in DEBUT_EMPLOIS.items() if int(annee) >= a}
    if set(trouves) != attendus:
        sys.exit(f"plafonds d'emplois : {sorted(trouves)} au lieu de {sorted(attendus)}")
    return trouves


def rangees_emplois(tableau, forme, k):
    """Les lignes d'un tableau de plafonds d'emplois : [(ligne, libellé, nombre ou None, en gras)], hors en-têtes ; un
    tableau a une colonne de plafond, et une ligne au plus un nombre."""
    rangees = []
    for r, ligne in enumerate(tableau):
        libelle = re.sub(r"\s+", " ", propre(nom(ligne[0]))).strip(" .…") if ligne else ""  # points de conduite
        nombres = [(c, n) for c, x in enumerate(ligne) if c and (n := nombre_texte(x))]
        if len(nombres) > 1 or any(n[1] for _, n in nombres):
            sys.exit(f"tableau {k}, ligne {r} : plusieurs plafonds, ou un plafond qui n'est pas un nombre entier")
        if not nombres and (not libelle or re.match(r"(?i)\(en équivalents|désignation|missions?\s*(?:/|et)\s*programmes?|"
                                                    r"autorité$|plafond", libelle)):
            continue  # en-tête, ligne vide
        if any(x.strip() and not nombre_texte(x) and x.strip().replace("\u2011", "-") not in NEANT
               and not re.match(r"(?i)plafond|\(en", x.strip()) for x in ligne[1:]):
            sys.exit(f"tableau {k}, ligne {r} : plafond illisible ({ligne[1:]})")
        c, nombre_ = nombres[0] if nombres else (None, None)
        rangees.append({"ligne": r, "colonne": c, "libelle": libelle, "nombre": nombre_, "gras": (r, 0) in forme["gras"]})
    return rangees


def total_emplois(rangees, k, total_phrase=None):
    """La dernière rangée d'un tableau de plafonds d'emplois, son total, et les autres ; le total doit avoir un nombre,
    et égaler celui de la phrase qui annonce le tableau quand elle en donne un."""
    if not rangees or not re.fullmatch(r"Total(?: général)?", rangees[-1]["libelle"]) or not rangees[-1]["nombre"]:
        sys.exit(f"tableau {k} : plafonds d'emplois sans total en dernière ligne")
    total = rangees[-1]
    if total_phrase is not None and int(total["nombre"][0]) != total_phrase:
        sys.exit(f"tableau {k} : total {total['nombre'][0]}, la phrase qui l'annonce {total_phrase}")
    return total, rangees[:-1]


def somme_emplois(total, parties, quoi, k):
    """Un plafond d'emplois égale exactement la somme de ses parties (des rangées, une case vide valant zéro)."""
    somme = sum(int(g["nombre"][0]) for g in parties if g["nombre"])
    if int(total["nombre"][0]) != somme:
        sys.exit(f"tableau {k}, ligne {total['ligne']} : {quoi} « {total['libelle']} » vaut {total['nombre'][0]}, "
                 f"ses lignes {somme}")


def emplois_etat(rangees, k, plafond, source_id, fonctions):
    """Le plafond des emplois de l'État, réparti par ministère (fonction LOLF.EMPLOIS.<ministère>) et par budget annexe
    (la fonction du budget annexe) : [(concept, fonction, rangée)] et l'écart du total au plafond de l'article
    d'équilibre. Les ministères font la ligne « I. Budget général », les budgets annexes la ligne « II. Budgets
    annexes », et les deux, le total général ; un ministère sans plafond (ses emplois sont comptés ailleurs) n'a pas de
    chiffre. Le total général égale le plafond de l'article d'équilibre, à l'écart déclaré dans ECARTS_EMPLOIS près."""
    total, corps = total_emplois(rangees, k)
    parties, partie = {"BG": None, "BA": None}, None
    lignes = {"BG": [], "BA": []}
    for g in corps:
        if re.fullmatch(r"I\.\s*[-–‑]?\s*Budget général", g["libelle"]):
            partie = "BG"
        elif re.fullmatch(r"II\.\s*[-–‑]?\s*Budgets annexes", g["libelle"]):
            partie = "BA"
        elif partie is None:
            sys.exit(f"tableau {k}, ligne {g['ligne']} : « {g['libelle']} » avant le budget général")
        else:
            lignes[partie].append(g)
            continue
        if parties[partie] is not None or not g["nombre"]:
            sys.exit(f"tableau {k}, ligne {g['ligne']} : « {g['libelle']} » deux fois, ou sans plafond")
        parties[partie] = g
    if None in parties.values():
        sys.exit(f"tableau {k} : budget général ou budgets annexes absents")
    for p in ("BG", "BA"):
        somme_emplois(parties[p], lignes[p], "le plafond", k)
    somme_emplois(total, [parties["BG"], parties["BA"]], "le plafond", k)
    ecart = int(total["nombre"][0]) - plafond
    if ecart != ECARTS_EMPLOIS.get(source_id, 0):
        sys.exit(f"tableau {k} : total général {total['nombre'][0]}, plafond de l'article d'équilibre {plafond} (écart "
                 f"déclaré : {ECARTS_EMPLOIS.get(source_id, 0)})")
    resultat = []
    for p in ("BG", "BA"):
        resultat.append((f"LOLF.{p}_PLAFOND_EMPLOIS_LFI", "", parties[p]))
        for g in lignes[p]:
            if not g["nombre"]:
                continue
            f = f"LOLF.{'EMPLOIS.' if p == 'BG' else ''}{code_lolf(g['libelle'])}"
            if p == "BA" and f not in fonctions:
                sys.exit(f"tableau {k}, ligne {g['ligne']} : budget annexe « {g['libelle']} » inconnu")
            resultat.append((f"LOLF.{p}_PLAFOND_EMPLOIS_LFI", f, g))
    return resultat, ecart


def emplois_par_programme(rangees, k, total_phrase, concept_, missions_texte, programmes_texte, source_id):
    """Un plafond d'emplois réparti par mission et par programme (opérateurs, établissements à autonomie financière) :
    [(concept, fonction, rangée)]. Une mission est une mission que la loi dote dans ses états B à D (« budget annexe »
    entre parenthèses ne fait pas partie de son nom), en gras ou qui n'est pas un programme de la mission en cours ; ses
    programmes, ceux que ces états lui donnent, la suivent et en font le plafond. Une mission
    sans plafond n'est qu'un intitulé. Sans mission qui le précède, un programme est celui de la seule mission qui en a
    un de ce nom. Le total est la somme des missions dotées et des programmes des autres."""
    total, corps = total_emplois(rangees, k, total_phrase)
    resultat, mission, missions_, programmes_ = [], None, [], {None: []}
    for g in corps:
        nom_ = re.sub(r"\s*\(budget annexe\)$", "", LIBELLES_EMPLOIS.get((source_id, g["libelle"]), g["libelle"]))
        programme = f"{mission}.{code_lolf(nom_)}" if mission else None
        de_la_mission = programme in programmes_texte.get(mission, ())
        if f"LOLF.{code_lolf(nom_)}" in missions_texte and (g["gras"] or not de_la_mission):
            mission = f"LOLF.{code_lolf(nom_)}"
            missions_.append((mission, g))
            programmes_[mission] = []
            continue
        if mission is None:
            candidates = [m for m, ps in programmes_texte.items() if f"{m}.{code_lolf(nom_)}" in ps]
            programme = f"{candidates[0]}.{code_lolf(nom_)}" if len(candidates) == 1 else None
        if programme is None or programme.rsplit(".", 1)[0] not in programmes_texte or \
                programme not in programmes_texte[programme.rsplit(".", 1)[0]]:
            sys.exit(f"tableau {k}, ligne {g['ligne']} : programme « {nom_} » inconnu des états")
        programmes_[mission].append(g)
        if g["nombre"]:
            resultat.append((concept_, programme, g))
    parties = programmes_[None]
    for mission_, g in missions_:
        if g["nombre"]:
            somme_emplois(g, programmes_[mission_], "la mission", k)
            resultat.append((concept_, mission_, g))
            parties.append(g)
        else:
            parties += programmes_[mission_]
    somme_emplois(total, parties, "le total", k)
    resultat.append((concept_, "", total))
    return resultat


def emplois_api(rangees, k, total_phrase):
    """Le plafond d'emplois des autorités publiques indépendantes, autorité par autorité (fonction
    LOLF.EMPLOIS.<autorité>, de son nom sans le sigle entre parenthèses qui le suit) : [(concept, fonction, rangée)]."""
    total, corps = total_emplois(rangees, k, total_phrase)
    somme_emplois(total, corps, "le total", k)
    concept_, sans_sigle = CONCEPTS_EMPLOIS["API"], lambda libelle: re.sub(r"\s*\([^()]*\)$", "", libelle)
    return [(concept_, f"LOLF.EMPLOIS.{code_lolf(sans_sigle(g['libelle']))}", g) for g in corps if g["nombre"]] + \
        [(concept_, "", total)]


def chiffre(fichier, annee, concept_, fonction, unite_, nombre, emplacement, note=""):
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement,
        "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept_, "fonction_id": fonction, "traitements": "",
        "unite_id": unite_, "periode": annee, "valeur": nombre[0], "decimales": nombre[1], "statut": "non_precise",
        "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": "non_consolide",
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions, programmes, comptes et
    lignes de recettes."""
    chemin = BASE / fichier["chemin"]
    texte = texte_html(lire_texte_html(chemin))
    annees = set(re.findall(r"Il est ouvert aux ministres, pour ([0-9]{4}),? au titre du budget général", texte))
    if len(annees) != 1 or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année de la loi ({', '.join(sorted(annees)) or 'aucune'}) ou date du texte "
                 f"introuvable")
    annee = annees.pop()
    if not int(annee) - 1 <= int(fichier["mis_a_jour_source"][:4]) <= int(annee):
        sys.exit(f"{fichier['id']} : loi de finances pour {annee} dans un texte daté {fichier['mis_a_jour_source']}")
    # Une coupure de mot de fin de ligne du texte imprimé, restée dans la page (« dévelop-pement »), se recolle quand
    # le mot entier figure ailleurs dans le texte.
    mots = set(re.findall(r"\w+", texte.lower()))
    recolle = lambda libelle: re.sub(r"(\w+)-(\w+)", lambda m: m.group(1) + m.group(2) if m.group(1)[-1].islower() and
                                     m.group(2)[0].islower() and (m.group(1) + m.group(2)).lower() in mots
                                     else m.group(0), libelle)
    grilles, formes, flux = lire_page_html(chemin)
    blocs = blocs_des_etats(grilles, formes, flux, fichier["source_id"])
    totaux = {c: b["total"]["valeurs"] for c, b in blocs}
    # Chaque article qui ouvre des crédits doit avoir son état ; un texte de commission mixte paritaire, qui ne reproduit
    # que ce qui restait en discussion, n'a l'article que s'il a l'état.
    for categories, motif in ARTICLES.items():
        ouverts = article(texte, annee, motif)
        if ouverts is None:
            continue
        if not all(c in totaux for c in categories):
            sys.exit(f"{fichier['id']} : l'article ouvre des crédits {motif}, dont l'état n'est pas lu")
        for i, colonne in enumerate(("AE", "CP")):
            if abs(sum(totaux[c][colonne] for c in categories) - ouverts[i]) >= 0.5:
                sys.exit(f"{'+'.join(categories)} : l'article ouvre {ouverts[i]:,.0f} € en {colonne}, l'état en "
                         f"totalise {sum(totaux[c][colonne] for c in categories):,.0f}")
    lus = set(totaux)
    if not all(article(texte, annee, ARTICLES[(c,)]) or ("CAS" in lus and "CCF" in lus and
                                                          article(texte, annee, ARTICLES[("CAS", "CCF")]))
               for c in lus):
        sys.exit(f"{fichier['id']} : un état sans l'article qui en ouvre les crédits")
    missions_connues = {f for f, l in fonctions.items() if f.startswith("LOLF.") and not l["parent_id"]
                        and not f.startswith(("LOLF.RECETTES.", "LOLF.EMPLOIS."))}
    # (concept, fonction) → montant en euros, de chaque chiffre lu dans un état : ce que le tableau d'équilibre reprend.
    connus, missions = {}, {"BG": set(), "BA": set(), "CAS": set(), "CCF": set()}
    programmes = {}  # mission ou budget annexe → ses programmes dans les états de la loi
    for categorie, bloc in blocs:
        rattache = structure(categorie, bloc, missions_connues)
        for l in bloc["lignes"]:
            fonction = ""
            if l["genre"] != "total":
                libelle, mission = (recolle(x) for x in rattache[(l["tableau"], l["ligne"])])
                parent = f"LOLF.{code_lolf(mission)}" if mission else ""
                fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
                if parent:
                    fonctions.setdefault(parent, {"id": parent, "libelle": mission, "norme_id": "LOLF", "parent_id": ""})
                    programmes.setdefault(parent, set()).add(fonction)
                else:
                    missions[categorie].add(fonction)
                fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF",
                                                "parent_id": parent})
            unite_, note = l["unite"]
            for colonne, (c, nombre) in sorted(l["cases"].items()):
                ligne = chiffre(fichier, annee, concept(categorie, colonne, l["genre"] == "dont"), fonction, unite_,
                                nombre, f"tableau={l['tableau']};ligne={l['ligne']};colonne={c};libelle={l['libelle']};"
                                        f"colonne_libelle={l['noms'][c]}",
                                " ".join(n for n in (note, l["notes"].get(colonne, "")) if n))
                connus[(ligne["concept_id"], fonction)] = l["valeurs"][colonne]
                yield ligne
    # État A : les recettes de chaque ligne, division, section et compte.
    parties = tableaux_etat_a(grilles, flux, annee, fichier["source_id"])
    for rangees in parties.values():
        for g in rangees:
            g["libelle"] = recolle(g["libelle"])
    recettes, sorte = recettes_a(parties, missions["BA"], missions)
    absents = [n for s, n in ECARTS_A if s == fichier["source_id"] and (s, n) not in ECARTS_VUS]
    if absents:
        sys.exit(f"état A : écart déclaré absent ({', '.join(absents)})")
    for concept_, fonction, libelle, parent, g in recettes:
        if fonction:
            fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": parent})
        if (concept_, fonction) in connus:
            sys.exit(f"état A, {ou(g)} : {concept_} de « {fonction or 'ensemble'} » déjà lu")
        connus[(concept_, fonction)] = g["valeur"]
        yield chiffre(fichier, annee, concept_, fonction, g["unite"], g["nombre"],
                      f"tableau={g['tableau']};ligne={g['ligne']};colonne={g['colonne']};"
                      f"libelle={(g['numero'] + ' ' + g['libelle']).strip()};colonne_libelle={g['colonne_libelle']}",
                      g["note"])
    # Tableau de l'article d'équilibre, en millions d'euros : ce qu'il reprend d'un état se vérifie, le reste
    # s'enregistre.
    tableau_equilibre = equilibre(grilles, flux, annee)
    verifier_equilibre(tableau_equilibre, sorte)
    enregistres = {}
    for bloc, cle_, fonction, cote, g in tableau_equilibre:
        c_ = EQUILIBRE[bloc][cle_]["RCS".index(cote)]
        if c_ in VERIFIES_SEULEMENT:
            continue
        concept_, cle = f"LOLF.{c_}_LFI", (f"LOLF.{c_}_LFI", fonction)
        if cle in connus:  # au million près : le tableau arrondit parfois un total depuis ses montants arrondis
            if abs(g["valeur"] * 1e6 - connus[cle]) >= 1e6:
                sys.exit(f"tableau d'équilibre, ligne {g['ligne']} : « {g['libelle']} », {g['valeur']:,.0f} M€ quand "
                         f"l'état donne {connus[cle]:,.0f} € ({concept_})")
        elif cle in enregistres:
            if g["valeur"] != enregistres[cle]:
                sys.exit(f"tableau d'équilibre, ligne {g['ligne']} : « {g['libelle']} », {g['valeur']} M€ quand une "
                         f"autre ligne en donne {enregistres[cle]} ({concept_})")
        else:
            enregistres[cle] = g["valeur"]
            if fonction and fonction not in fonctions:
                if bloc not in ("BA", "BA_FDC"):
                    sys.exit(f"tableau d'équilibre : fonction {fonction} inconnue")
                fonctions[fonction] = {"id": fonction, "libelle": g["libelle"], "norme_id": "LOLF", "parent_id": ""}
            if g["nombre"]:
                # Un montant qu'un état donnerait à l'euro, quand le texte ne reproduit pas cet état (2006).
                substitut = concept_ in SUBSTITUTS or (fonction and concept_ in SUBSTITUTS_PAR_BUDGET)
                yield chiffre(fichier, annee, concept_, fonction, "MIO_EUR", g["nombre"],
                              f"tableau={g['tableau']};ligne={g['ligne']};colonne={g['colonne']};libelle={g['libelle']};"
                              f"colonne_libelle={g['colonne_libelle']}",
                              "Lu dans le tableau de l'article d'équilibre, en millions d'euros : le texte ne reproduit "
                              "pas l'état qui le donne à l'euro." if substitut else "")
    # Les remboursements et dégrèvements que le tableau déduit des recettes brutes et des dépenses brutes sont les
    # crédits de leur mission ; depuis la loi pour 2023, ses dépenses sont nettes de ceux d'impôts d'État (programme 200).
    mission_rd = "LOLF.REMBOURSEMENTS_ET_DEGREVEMENTS"
    if sorte == "BRUTES":
        deduits, credits = enregistres.get(("LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS_LFI", "")), \
            connus.get(("LOLF.BG_CP_LFI", mission_rd))
    else:
        deduits = enregistres.get(("LOLF.BG_DEPENSES_NETTES_HORS_FDC_LFI", ""))
        credits = connus[("LOLF.BG_CP_LFI", "")] - credits_200(connus, fonctions)
    if deduits is None or credits is None or abs(deduits * 1e6 - credits) >= 1e6:
        sys.exit(f"tableau d'équilibre : {deduits} M€ quand l'état B donne {credits} € ({sorte.lower()})")
    # Chaque solde contre celui que donnent les états : recettes de l'état A moins crédits des états B à D. Le tableau
    # calcule un solde de ses montants arrondis : il peut s'écarter de l'exact d'un demi-million par montant arrondi
    # en jeu (recettes brutes, non fiscales, prélèvements et crédits pour le budget général ; recettes et crédits
    # pour un budget annexe ou une catégorie de comptes), et d'un demi-million de plus pour son propre arrondi.
    depenses_bg = connus[("LOLF.BG_CP_LFI", "")] - (0 if sorte == "BRUTES" else credits_200(connus, fonctions))
    soldes = {("LOLF.SOLDE_BUDGET_GENERAL_LFI", ""): ([("LOLF.BG_RECETTES_NETTES_HORS_PSR_LFI", "")]
                                                     if sorte == "NETTES" else None, depenses_bg)}
    for f in missions["BA"]:
        soldes[("LOLF.BA_SOLDE_HORS_FDC_LFI", f)] = ([("LOLF.BA_RECETTES_HORS_FDC_LFI", f)], connus.get(("LOLF.BA_CP_LFI", f)))
    for c in ("CAS", "CCF"):
        soldes[(f"LOLF.{c}_SOLDE_LFI", "")] = ([(f"LOLF.{c}_RECETTES_LFI", "")], connus.get((f"LOLF.{c}_CP_LFI", "")))
    for cle, (recettes_, depenses) in soldes.items():
        if cle == ("LOLF.SOLDE_BUDGET_GENERAL_LFI", "") and recettes_ is None:
            exact = sum(connus[(RECETTES_BG[c].format("BRUTES"), "")] * (-1 if c == "3" else 1) for c in "123")
        elif all(r in connus for r in recettes_) and depenses is not None:
            exact = sum(connus[r] for r in recettes_)
        else:
            continue  # le texte ne reproduit pas l'état
        prevu = enregistres.get(cle, 0)  # un solde que le tableau laisse vide est nul
        marge = 0.5e6 * ((4 if cle[0] == "LOLF.SOLDE_BUDGET_GENERAL_LFI" else 2) + 1)
        if abs(prevu * 1e6 - (exact - depenses)) > marge:
            sys.exit(f"tableau d'équilibre : {cle[0]} de « {cle[1] or 'ensemble'} », {prevu} M€ quand les états en "
                     f"donnent {exact - depenses:,.0f} €")
    # Tableau de financement (II, 1°) et plafond de la variation de la dette négociable à plus d'un an, en milliards
    # d'euros : ils se vérifient l'un par l'autre, et contre le solde général.
    plafonds = list(re.finditer(PLAFOND_DETTE, texte))
    plafond = nombre_de_phrase(plafonds[0].group(0)) if len(plafonds) == 1 else None
    if plafond is None:
        sys.exit(f"{len(plafonds)} plafond(s) de la variation de la dette négociable, ou montant illisible")
    lignes_financement = financement(grilles, flux, annee, fichier["source_id"])
    verifier_financement(lignes_financement, enregistres[("LOLF.RESULTAT_BUDGETAIRE_LFI", "")], float(plafond[0]))
    for _, concept_, _, g in lignes_financement:
        if g["nombre"]:
            morceau = f"morceau={g['morceau']};" if g["morceau"] else ""
            yield chiffre(fichier, annee, f"{concept_}_LFI", "", "MD_EUR", g["nombre"],
                          f"tableau={g['tableau']};ligne={g['ligne']};colonne={g['colonne']};{morceau}"
                          f"libelle={g['libelle']}")
    yield chiffre(fichier, annee, "LOLF.PLAFOND_VARIATION_DETTE_LFI", "", "MD_EUR", plafond,
                  f"phrase={plafonds[0].group(0)}")
    # Plafonds des autorisations d'emplois : celui de l'article d'équilibre, puis les tableaux de la seconde partie.
    phrases = list(re.finditer(PLAFOND_EMPLOIS, texte))
    nombre_ = nombre_de_phrase(phrases[0].group(0)) if len(phrases) == 1 else None
    if nombre_ is None:
        sys.exit(f"{len(phrases)} plafond(s) des emplois de l'État dans l'article d'équilibre, ou nombre illisible")
    sortes = tableaux_emplois(grilles, formes, flux, annee)
    k, phrase, unite_ = sortes["ETAT"]
    lus, ecart = emplois_etat(rangees_emplois(grilles[k], formes[k], k), k, int(nombre_[0]), fichier["source_id"],
                              fonctions)
    lus = [(k, unite_, *l) for l in lus]
    for sorte in ("OPERATEURS", "EAF", "API"):
        if sorte not in sortes:
            continue
        k, phrase, unite_ = sortes[sorte]
        fixe = re.search(r"est fixé à ([0-9]{1,3}(?:[ \u00a0\u202f][0-9]{3})*)", phrase)
        fixe = int(re.sub(r"\D", "", fixe.group(1))) if fixe else None
        rangees = rangees_emplois(grilles[k], formes[k], k)
        if sorte == "API":
            lus += [(k, unite_, *l) for l in emplois_api(rangees, k, fixe)]
        else:
            lus += [(k, unite_, *l) for l in emplois_par_programme(rangees, k, fixe, CONCEPTS_EMPLOIS[sorte],
                                                                    set().union(*missions.values()), programmes,
                                                                    fichier["source_id"])]
    note = (f"Le tableau de l'article qui répartit ce plafond par ministère et par budget annexe en compte "
            f"{int(nombre_[0]) + ecart:,}".replace(",", "\u202f") + f", {abs(ecart)} de {'plus' if ecart > 0 else 'moins'}, "
            f"et ses lignes en font la somme exacte." if ecart else "")
    yield chiffre(fichier, annee, "LOLF.PLAFOND_EMPLOIS_LFI", "", "ETPT", nombre_, f"phrase={phrases[0].group(0)}", note)
    for k, unite_, concept_, fonction, g in lus:
        if fonction.startswith("LOLF.EMPLOIS."):
            fonctions.setdefault(fonction, {"id": fonction, "libelle": g["libelle"], "norme_id": "LOLF", "parent_id": ""})
        yield chiffre(fichier, annee, concept_, fonction, unite_, g["nombre"],
                      f"tableau={k};ligne={g['ligne']};colonne={g['colonne']};libelle={g['libelle']}")


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
