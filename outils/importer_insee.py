#!/usr/bin/env python3
"""Enregistre dans la base les chiffres d'un tableau des comptes nationaux de l'Insee archivé (classeur xlsx).

    python3 outils/importer_insee.py <fichier_id>

Tableaux pris en charge :
- 3.201 à 3.214 : dépenses et recettes par nature, pour l'ensemble des administrations publiques et
  chacun de leurs sous-secteurs, jusqu'aux communes, départements, régions et syndicats ;
- 3.215 : dépenses et recettes totales de chaque sous-secteur, en montant et en % du PIB ;
- 3.106 : déficit au sens de Maastricht par sous-secteur, et PIB utilisé pour le ratio ;
- 3.101 : dette au sens de Maastricht par sous-secteur, et PIB utilisé pour le ratio ;
- 3.102 : la même dette, par instrument (dépôts, titres de créance, crédits) ;
- 3.103 : dette nette par sous-secteur, et actifs liquides que la dette nette ne déduit pas ;
- 3.104 : passage du total des passifs à la dette au sens de Maastricht, par sous-secteur ;
- 3.105 : passage du déficit à la variation de la dette au sens de Maastricht ;
- 7.301 à 7.306 : la séquence complète des comptes de l'ensemble des administrations publiques et de
  chacun de leurs sous-secteurs, de la production à la capacité de financement ;
- 3.301 à 3.306 : dépenses par fonction (COFOG, jusqu'aux 69 groupes) et par opération, pour
  l'ensemble des administrations publiques et chacun de leurs sous-secteurs ;
- 3.307 : répartition par sous-secteur des dépenses consolidées de l'ensemble, par fonction ;
- 3.216 : prélèvements obligatoires par sous-secteur et pour l'Union européenne ;
- 3.217 : principaux impôts par catégorie, et passage de l'ensemble des impôts et cotisations aux
  prélèvements obligatoires ;
- 3.107 : passage du résultat d'exécution des lois de finances au déficit de l'État au sens de Maastricht ;
- 3.108 : passage du résultat comptable du régime général au déficit des administrations de sécurité
  sociale au sens de Maastricht.

Chaque libellé ou code de ligne doit avoir une correspondance ci-dessous ou dans les tables de la base :
une ligne inconnue arrête l'import, pour que rien ne soit écarté en silence ; seuls les zéros qu'un tableau
porte sur une ligne sans libellé de chiffre (ligne de séparation, d'unité ou de côté d'un compte) ne sont pas
des chiffres, et l'import dit combien il en a rencontré. La version d'un chiffre est
la date de modification que l'Insee inscrit dans le classeur, à défaut sa date de création. Son statut
suit le calendrier des comptes annuels de l'Insee : la dernière année publiée est provisoire,
l'avant-dernière semi-définitive, les précédentes définitives.
"""

import collections
import re
import sys

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, feuilles_xlsx, fusionner, identifiant, lire,
                    lire_xlsx, nombre, position, table_des_chiffres)

PERIMETRES_32XX = {"3201": "S13", "3202": "S1311", "3203": "S13111", "3204": "S13112", "3205": "S1313",
                   "3206": "S13131", "3207": "S131311", "3208": "S131312", "3209": "S131313",
                   "3210": "S131314", "3211": "S13132", "3212": "S1314", "3213": "S13141", "3214": "S13142"}

# Lignes des tableaux 3.201 à 3.214 : (section, libellé de l'Insee) → concept de la base.
LIGNES_32XX = {
    ("DEPENSES", "Dépenses de fonctionnement"): "INSEE_APU.DEP_FONCTIONNEMENT",
    ("DEPENSES", "Consommation intermédiaire (P2)"): "SEC2010.P2",
    ("DEPENSES", "Rémunération des salariés (D1)"): "SEC2010.D1PAY",
    ("DEPENSES", "Autres impôts sur la production (D29)"): "SEC2010.D29PAY",
    ("DEPENSES", "Revenus de la propriété autres que les intérêts (D4 hors D41)"): "SEC2010.D4_HORS_D41PAY",
    ("DEPENSES", "Impôts courants sur le revenu et le patrimoine (D5)"): "SEC2010.D5PAY",
    ("DEPENSES", "Intérêts (D41)"): "SEC2010.D41PAY",
    ("DEPENSES", "Intérêts hors correction au titre des services d'intermédiation financière indirectement "
                 "mesurés (D41G)"): "SEC2010.D41GPAY",
    ("DEPENSES", "Prestations et autres transferts"): "INSEE_APU.DEP_PRESTATIONS_TRANSFERTS",
    ("DEPENSES", "Prestations sociales autres que transferts sociaux en nature (D62)"): "SEC2010.D62PAY",
    ("DEPENSES", "Transferts sociaux en nature de produits marchands (D632)"): "SEC2010.D632PAY",
    ("DEPENSES", "Subventions (D3)"): "SEC2010.D3PAY",
    ("DEPENSES", "Transferts courants entre administrations publiques (D73)"): "SEC2010.D73PAY",
    ("DEPENSES", "Autres transferts courants (D7 hors D73)"): "SEC2010.D7_HORS_D73PAY",
    ("DEPENSES", "Transferts en capital à payer (D9p hors D995p)"): "SEC2010.D9_HORS_D995PAY",
    ("DEPENSES", "Acquisitions moins cessions d'actifs non financiers"): "INSEE_APU.DEP_ACTIFS_NON_FINANCIERS",
    ("DEPENSES", "Formation brute de capital fixe (P51g)"): "SEC2010.P51G",
    ("DEPENSES", "Autres acquisitions moins cessions d'actifs non financiers (P52, P53, NP)"): "SEC2010.P52_P53_NP",
    ("DEPENSES", "Total des dépenses"): "SEC2010.TE",
    ("DEPENSES", "dont (a) - Cotisations sociales imputées (D122)"): "SEC2010.D122PAY",
    ("DEPENSES", "dont (b) - Capitalisation de la production pour emploi final propre (P51g)"):
        "INSEE_APU.DEP_PRODUCTION_COMPTE_PROPRE",
    ("DEPENSES", "dont (c) - Crédits d'impôts enregistrés en dépenses (**)"): "INSEE_APU.DEP_CREDITS_IMPOT",
    ("DEPENSES", "Dépenses hors éléments imputés (a, b et c) (***)"): "INSEE_APU.DEP_HORS_ELEMENTS_IMPUTES",
    ("RECETTES", "Recettes de production"): "INSEE_APU.REC_PRODUCTION",
    ("RECETTES", "Production des branches marchandes et ventes résiduelles (P11)"): "SEC2010.P11",
    ("RECETTES", "Production pour emploi final propre (P12)"): "SEC2010.P12",
    ("RECETTES", "Paiements partiels des ménages (partie du P13)"): "INSEE_APU.REC_PAIEMENTS_PARTIELS",
    ("RECETTES", "Autres subventions sur la production (D39)"): "SEC2010.D39REC",
    ("RECETTES", "Revenus de la propriété"): "INSEE_APU.REC_REVENUS_PROPRIETE",
    ("RECETTES", "Intérêts (D41)"): "SEC2010.D41REC",
    ("RECETTES", "Intérêts hors correction au titre des services d'intermédiation financière indirectement "
                 "mesurés (D41G)"): "SEC2010.D41GREC",
    ("RECETTES", "Revenus de la propriété autres que les intérêts (D4 hors D41)"): "SEC2010.D4_HORS_D41REC",
    ("RECETTES", "Impôts et cotisations sociales"): "INSEE_APU.REC_IMPOTS_COTISATIONS",
    ("RECETTES", "Impôts sur la production et les importations (D2)"): "SEC2010.D2REC",
    ("RECETTES", "Impôts courants sur le revenu et le patrimoine (D5)"): "SEC2010.D5REC",
    ("RECETTES", "Impôts en capital à recevoir (D91r)"): "SEC2010.D91REC",
    ("RECETTES", "Transferts de recettes fiscales (D733)"): "SEC2010.D733REC",
    ("RECETTES", "Cotisations sociales nettes (D61)"): "SEC2010.D61REC",
    ("RECETTES", "Impôts et cotisations dus non recouvrables nets (D995r)"): "SEC2010.D995REC",
    ("RECETTES", "Autres transferts"): "INSEE_APU.REC_AUTRES_TRANSFERTS",
    ("RECETTES", "Transferts courants entre administrations publiques (D73 hors D733)"): "SEC2010.D73_HORS_D733REC",
    ("RECETTES", "Autres transferts courants (D7 hors D73)"): "SEC2010.D7_HORS_D73REC",
    ("RECETTES", "Transferts en capital (D9r hors D91r, D995r)"): "SEC2010.D9_HORS_D91_D995REC",
    ("RECETTES", "Total des recettes"): "SEC2010.TR",
    ("RECETTES", "dont (a) - Cotisations sociales imputées (D612)"): "SEC2010.D612REC",
    ("RECETTES", "dont (b) - Production pour emploi final propre (P12)"): "SEC2010.P12",
    ("RECETTES", "dont (c') - Crédits d'impôts enregistrés en recettes (**)"): "INSEE_APU.REC_CREDITS_IMPOT",
    ("RECETTES", "Recettes hors éléments imputés (a,b et c') (***)"): "INSEE_APU.REC_HORS_ELEMENTS_IMPUTES",
    ("SOLDES", "Epargne brute (B8g)"): "SEC2010.B8G",
    ("SOLDES", "Capacité (+) ou besoin (-) de financement (B9NF)"): "SEC2010.B9",
}

SECTEURS = {"S13", "S1311", "S13111", "S13112", "S1313", "S1314"}

# Mentions d'une valeur que l'Insee ne diffuse pas, en minuscules.
NON_DISPONIBLE = {"", "nd", "n.d."}

PERIMETRES_33XX = {"3301": "S13", "3302": "S1311", "3303": "S13111", "3304": "S13112", "3305": "S1313", "3306": "S1314"}

# Opérations des tableaux 3.301 à 3.306 (code de l'Insee en colonne A) → concept de la base.
OPERATIONS_33XX = {"OTE": "SEC2010.TE", "D1": "SEC2010.D1PAY", "P2": "SEC2010.P2", "OED": "SEC2010.D29_D5_D8PAY",
                   "D3": "SEC2010.D3PAY", "D4": "SEC2010.D4PAY", "D62": "SEC2010.D62PAY", "D632": "SEC2010.D632PAY",
                   "D7": "SEC2010.D7PAY", "D9": "SEC2010.D9_HORS_D995PAY", "P5L": "INSEE_APU.DEP_ACTIFS_NON_FINANCIERS"}

# Tableaux 3.216 et 3.217 : libellé de l'Insee → (concept, périmètre, unité) ; un périmètre ou une unité vide
# vaut celui du tableau. Une ligne dont le libellé ne suffit pas (« dont … », « - Impôts », « en % du PIB »,
# détail des crédits d'impôt) se désigne avec la ligne qu'elle détaille : « ligne détaillée / ligne ».
LIGNES_3216 = {
    "S13 et S212 - Prélèvements obligatoires": ("INSEE_PO.PO", "S13_S212", ""),
    "S1311 - Administration publique centrale": ("INSEE_PO.PO", "S1311", ""),
    "S13111 - État": ("INSEE_PO.PO", "S13111", ""),
    "S13111 - État / - Impôts (*)": ("INSEE_PO.PO_IMPOTS", "S13111", ""),
    "S13111 - État / - Cotisations sociales (**)": ("INSEE_PO.PO_COTISATIONS", "S13111", ""),
    "S13112 - Organismes divers d'administration centrale": ("INSEE_PO.PO", "S13112", ""),
    "S1313 - Administrations publiques locales": ("INSEE_PO.PO", "S1313", ""),
    "S1314 - Administrations de sécurité sociale": ("INSEE_PO.PO", "S1314", ""),
    "S1314 - Administrations de sécurité sociale / - Impôts (*)": ("INSEE_PO.PO_IMPOTS", "S1314", ""),
    "S1314 - Administrations de sécurité sociale / - Cotisations sociales (**)": ("INSEE_PO.PO_COTISATIONS", "S1314", ""),
    "S212 - Institutions et organes de l'Union européenne": ("INSEE_PO.PO", "S212", ""),
}
_3217 = {
    "SEC2010": {
        "Taxe sur la valeur ajoutée (TVA) (D211)": "D211REC",
        "Impôts et droits sur les importations (D212)": "D212REC",
        "Impôts sur les produits (D214)": "D214REC",
        "Impôts sur les salaires et la main d'œuvre (D291)": "D291REC",
        "Impôts divers sur la production (D292)": "D292REC",
        "Impôts courants sur le revenu (D51)": "D51REC",
        "Autres impôts courants (D59)": "D59REC",
        "Impôts en capital (D91r)": "D91REC",
        "Cotisations sociales": "D61REC",
        "Cotisations sociales imputées": "D612REC",
        "Impôts et cotisations susceptibles de ne pas être collectés": "D995REC",
        "Impôts et cotisations sociales susceptibles de ne pas être collectés (II)": "D995REC",
    },
    "INSEE_PO": {
        "Accises sur les produits énergétiques (TICPE)": "TICPE",
        "Accises sur l'électricité (TICFE)": "TICFE",
        "Accises sur le gaz naturel (TICGN)": "TICGN",
        "Autres taxes sur l'énergie": "AUTRES_TAXES_ENERGIE",
        "Accises sur les tabacs": "ACCISES_TABACS",
        "Accises sur les alcools et autres boissons": "ACCISES_ALCOOLS",
        "Droits d'enregistrement (sur transactions immobilières et autres)": "DROITS_ENREGISTREMENT",
        "Taxe sur les conventions d'assurances": "TSCA",
        "Taxe de solidarité additionnelle (sur complémentaires santé)": "TSA",
        "Autres taxes sur contrats d'assurance": "AUTRES_TAXES_ASSURANCE",
        "Prélèvements sur les jeux, casinos, paris sportifs et hippiques (**)": "PRELEVEMENTS_JEUX",
        "Taxes sur services de logement et sur constructions": "TAXES_LOGEMENT_CONSTRUCTION",
        "Taxe sur les certificats d'immatriculation des véhicules": "CERTIFICATS_IMMATRICULATION",
        "Taxe additionnelle sur véhicules (malus auto)": "MALUS_AUTO",
        "Taxes sur services de transport": "TAXES_TRANSPORT",
        "Taxe sur les transactions financières": "TTF",
        "Taxes sur ventes de produits pharmaceutiques": "TAXES_PHARMACIE",
        "Taxes sur services numériques et télécommunications": "TAXES_NUMERIQUE_TELECOM",
        "Taxes sur spectacles et divertissements": "TAXES_SPECTACLES",
        "Taxe de séjour": "TAXE_SEJOUR",
        "Taxe générale sur les activités polluantes": "TGAP",
        "Taxe générale sur les activités polluantes / dont part classée en impôts sur la production": "TGAP_PART_PRODUCTION",
        "Redevances des agences de l'eau": "AGENCES_EAU",
        "Redevances des agences de l'eau / dont part classée en impôts sur la production": "AGENCES_EAU_PART_PRODUCTION",
        "Octroi de mer des départements d'outre-mer": "OCTROI_DE_MER",
        "Octroi de mer des départements d'outre-mer / dont part classée en impôts sur importations":
            "OCTROI_DE_MER_PART_IMPORTATIONS",
        "Taxe sur les salaires": "TAXE_SALAIRES",
        "Versement mobilité": "VERSEMENT_MOBILITE",
        "Contributions pour la formation professionnelle et l'apprentissage": "FORMATION_APPRENTISSAGE",
        "Forfait social": "FORFAIT_SOCIAL",
        "Contribution au fonds national d'aide au logement (FNAL)": "FNAL",
        "Contribution de solidarité pour l'autonomie (CNSA)": "CSA",
        "Participation des employeurs à l'effort de construction": "PEEC",
        "Cotisations au régime de garantie des salaires (AGS)": "AGS",
        "Contribution patronale sur stock-options": "STOCK_OPTIONS",
        "Taxe foncière": "TAXE_FONCIERE",
        "Taxe foncière / dont taxe foncière payée par les ménages (*)": "TAXE_FONCIERE_MENAGES",
        "Taxe foncière / dont taxe foncière hors ménages": "TAXE_FONCIERE_HORS_MENAGES",
        "Cotisation foncière des entreprises": "CFE",
        "Impositions forfaitaires sur les entreprises de réseaux": "IFER",
        "Cotisation sur la valeur ajoutée des entreprises": "CVAE",
        "Taxe professionnelle (TP)": "TAXE_PROFESSIONNELLE",
        "Contribution sociale de solidarité des sociétés": "C3S",
        "Contributions des banques aux mécanismes de garantie des dépôts et de résolution bancaire": "CONTRIBUTIONS_BANCAIRES",
        "Taxes pour organismes consulaires (Commerce et Industrie, Métiers et Artisanat, Agriculture)": "TAXES_CONSULAIRES",
        "Taxe sur les surfaces commerciales": "TASCOM",
        "Taxes sur véhicules des entreprises": "TAXES_VEHICULES_ENTREPRISES",
        "Taxes sur les bureaux (création et surfaces)": "TAXES_BUREAUX",
        "Taxe GEMAPI (milieux aquatiques et prévention des inondations)": "GEMAPI",
        "Autres taxes adossées aux impôts fonciers locaux (dont Taxe spéciale d'équipement)": "TAXES_ADOSSEES_FONCIER",
        "Quotas carbone (taxe sur émissions de gaz à effet de serre)": "QUOTAS_CARBONE",
        "Contributions des producteurs d'électricité": "CONTRIBUTIONS_PRODUCTEURS_ELECTRICITE",
        "Contribution sociale généralisée (CSG) (**)": "CSG",
        "Contribution au remboursement de la dette sociale (CRDS) (**)": "CRDS",
        "Prélèvement de solidarité et autres contributions sociales": "PRELEVEMENT_SOLIDARITE",
        "Prélèvements sur les revenus de capitaux mobiliers": "PRELEVEMENTS_CAPITAUX_MOBILIERS",
        "Impôt sur le revenu des personnes physiques (IRPP), avant crédits d'impôt": "IRPP",
        "Crédits d'impôt sur l'IRPP : utilisés en déduction de l'impôt dû": "CI_IRPP_IMPUTES",
        "Crédits d'impôt sur l'IRPP : au-delà de l'impôt dû, payés par l'administration": "CI_IRPP_RESTITUES",
        "Impôt sur les sociétés (IS), avant crédits d'impôt": "IS",
        "Crédits d'impôt sur l'IS : utilisés en déduction de l'impôt dû": "CI_IS_IMPUTES",
        "Crédits d'impôt sur l'IS : au-delà de l'impôt dû, payés par l'administration": "CI_IS_RESTITUES",
        "Contribution sociale sur les bénéfices des sociétés": "CSB",
        "Remises pharmaceutiques": "REMISES_PHARMACEUTIQUES",
        "Contribution exceptionnelle sur les bénéfices des grandes entreprises": "CONTRIBUTION_EXCEPTIONNELLE_GRANDES_ENTREPRISES",
        "Contribution différentielle sur les hauts revenus": "CDHR",
        "Taxe d'habitation": "TAXE_HABITATION",
        "Impôt sur la fortune (IFI, ex ISF)": "IFI_ISF",
        "Contribution à l'audiovisuel public": "AUDIOVISUEL_PUBLIC",
        "Taxe sur les véhicules (vignette auto des ménages)": "VIGNETTE",
        "Droits de mutation à titre gratuit": "DMTG",
        "Droits de mutation à titre gratuit / dont sur donations": "DMTG_DONATIONS",
        "Droits de mutation à titre gratuit / dont sur successions": "DMTG_SUCCESSIONS",
        "Taxations exceptionnelles sur la réserve de capitalisation des assurances": "TAXATION_RESERVE_CAPITALISATION",
        "Cotisations sociales effectives": "COTISATIONS_EFFECTIVES",
        "Ensemble des impôts et cotisations sociales (I)": "IMPOTS_ET_COTISATIONS",
        "Cotisations sociales imputées (III)": "AJUSTEMENT_COTISATIONS_IMPUTEES",
        "Crédits d'impôt (IV)": "AJUSTEMENT_CREDITS_IMPOT",
        "Crédits d'impôt (IV) / Utilisés en déduction de l'impôt dû": "AJUSTEMENT_CREDITS_IMPOT_IMPUTES",
        "Crédits d'impôt (IV) / Au-delà de l'impôt dû, payés par l'administration": "AJUSTEMENT_CREDITS_IMPOT_RESTITUES",
        "Prélèvements obligatoires = (I)+(II)+(III)+(IV)": "PO",
    },
}
LIGNES_3217 = {libelle: (f"{norme}.{code}", "", "") for norme, lignes in _3217.items() for libelle, code in lignes.items()}
LIGNES_3217.update({
    "Droits d'importation au profit de l'Union Européenne": ("SEC2010.D2121REC", "S212", ""),
    "Droits d'enregistrement (sur transactions immobilières et autres) / dont DMTO en ressources des collectivités "
    "locales": ("INSEE_PO.DMTO", "S13131", ""),
    "Contributions des banques aux mécanismes de garantie des dépôts et de résolution bancaire / dont contribution au "
    "fonds de résolution unique (impôt de l’Union européenne)": ("INSEE_PO.FRU", "S212", ""),
    "Prélèvements obligatoires = (I)+(II)+(III)+(IV) / en % du PIB": ("INSEE_PO.PO", "", "PC_PIB"),
    "Prélèvements obligatoires = (I)+(II)+(III)+(IV) / dont impôts nationaux": ("INSEE_PO.PO", "S13", ""),
    "Prélèvements obligatoires = (I)+(II)+(III)+(IV) / dont impôts de l’Union européenne": ("INSEE_PO.PO", "S212", ""),
})

# Tableaux 3.107 et 3.108 : libellé de l'Insee → (concept, périmètre). Une ligne « Autres » se désigne avec la
# rubrique où elle figure : « rubrique / Autres ». Le résultat d'exécution des lois de finances couvre le champ
# des lois de finances, plus étroit que l'État de la comptabilité nationale ; les corrections, l'État (S13111).
_E, _S = "INSEE_PASSAGES.ETAT_", "INSEE_PASSAGES.SECU_"
LIGNES_3107 = {
    "Résultat d’exécution des lois de finances (hors opérations avec le FMI)": ("LOLF.RESULTAT_EXECUTION", "ETAT_LF"),
    "Solde d'exécution du budget général": ("LOLF.SOLDE_BUDGET_GENERAL", "ETAT_LF"),
    "Solde des comptes spéciaux (hors opérations avec le FMI)": ("LOLF.SOLDE_COMPTES_SPECIAUX", "ETAT_LF"),
    "Déficit de l'État au sens de Maastricht = RE + (1) + (2) + (3)": ("SEC2010.B9", "S13111"),
    **{libelle: (_E + code, "S13111") for libelle, code in {
        "Opérations budgétaires traitées en opérations financières (1)": "OPERATIONS_FINANCIERES",
        "Prêts accordés par l'État, nets des remboursements": "PRETS_NETS",
        "Prises de participations, nettes des cessions": "PARTICIPATIONS_NETTES",
        "Autres opérations financières": "AUTRES_OPERATIONS_FINANCIERES",
        "Corrections de droits constatés (2)": "DROITS_CONSTATES",
        "Impôts : IRPP, ISF, TVA, TIPP, TTF et dégrèvements d'impôts locaux": "DC_IMPOTS",
        "Amendes en attente de confirmation et contentieux fiscaux": "DC_AMENDES_CONTENTIEUX",
        "Décalage comptable charges à payer sur achats de l'État": "DC_CHARGES_A_PAYER",
        "Décalage comptable lié aux remboursements de la contribution additionnelle de 3% sur les dividendes":
            "DC_CONTRIBUTION_DIVIDENDES",
        "Règlement de la dette État-Sécu": "DC_DETTE_ETAT_SECU",
        "Décalage entre livraisons et paiements de matériel militaire": "DC_MATERIEL_MILITAIRE",
        "Décalage entre la reconnaissance et la liquidation des crédits d'impôts": "DC_CREDITS_IMPOT",
        "Décalage comptable sur les exonérations de cotisations sociales": "DC_EXONERATIONS_COTISATIONS",
        "Décalage comptable sur la compensation des primes d'épargne": "DC_PRIMES_EPARGNE",
        "Décalage sur le transfert de la CVAE vers les collectivités locales": "DC_TRANSFERT_CVAE",
        "Décalage sur le transfert du produit des amendes vers les collectivités locales": "DC_TRANSFERT_AMENDES",
        "Décalage sur des transferts vers les organismes divers d'administration centrale": "DC_TRANSFERTS_ODAC",
        "Décalage comptable sur les dépenses du fonds de solidarité et les allocations d'activité partielle":
            "DC_FONDS_SOLIDARITE_ACTIVITE_PARTIELLE",
        "Décalage sur le paiement des budgets rectificatifs de l'Union Européenne": "DC_BUDGETS_RECTIFICATIFS_UE",
        "Étalements des versements de soultes liées aux retraites": "DC_SOULTES_RETRAITES",
        "Étalement des versements de la SFEF": "DC_SFEF",
        "Étalement du versement de la BDF pour le désendettement de la Grèce": "DC_BDF_GRECE",
        "Décalage comptable des charge spour service public de l'énergie (solde)": "DC_SERVICE_PUBLIC_ENERGIE",
        "Décalage comptable liée aux ventes de fréquences hertziennes": "DC_FREQUENCES_HERTZIENNES",
        "Décalage comptable sur le non recouvrement des impôts": "DC_NON_RECOUVREMENT",
        "Décalage comptable versements aux banques multilatérales de développement": "DC_BANQUES_MULTILATERALES",
        "Etalement des primes des prêts garantis par l'Etat": "DC_PRIMES_PGE",
        "Recettes de financement européen de France Relance (hors financement des dépenses des administrations de "
        "sécurité sociale)": "DC_FRANCE_RELANCE",
        "Bouclier tarifaire gaz - compensation fournisseurs": "DC_BOUCLIER_GAZ",
        "Bouclier tarifaire éléctricité - compensation fournisseurs": "DC_BOUCLIER_ELECTRICITE",
        "Corrections de droits constatés (2) / Autres": "DC_AUTRES",
        "Opérations non-budgétaires affectant le besoin de financement (3)": "NON_BUDGETAIRES",
        "Besoin ou capacité de financement des budgets annexes": "NB_BUDGETS_ANNEXES",
        "Remises de dettes aux États étrangers": "NB_REMISES_DETTES",
        "Différence entre intérêts courus et intérêts échus dans l'année et étalement des primes et décotes":
            "NB_INTERETS_COURUS",
        "Dividendes reçus sous forme de titres": "NB_DIVIDENDES_TITRES",
        "Besoin de financement des fonds inclus dans l'État en comptabilité nationale": "NB_FONDS",
        "Consolidation des Partenariats Publics Privés (PPP)": "NB_PPP",
        "Affectation de droits tabacs pour le règlement de la dette État-Sécu": "NB_DROITS_TABACS",
        "Transferts de titres de l'ERAP vers l'État": "NB_ERAP",
        "Reprise de la dette de l'EPFR (défaisance du crédit Lyonnais)": "NB_EPFR",
        "Dotations non-consommables du PIA": "NB_PIA_NON_CONSOMMABLES",
        "Dotations consommables du PIA (vers fonds CDC)": "NB_PIA_CONSOMMABLES",
        "Prise en compte des coûts de construction LGV Tour-Bordeaux": "NB_LGV_TOURS_BORDEAUX",
        "Droits d'enregistrement": "NB_DROITS_ENREGISTREMENT",
        "Bénéfices réinvestis d'investissement direct étranger": "NB_BENEFICES_REINVESTIS",
        "Reprise de dette de SNCF Réseau": "NB_DETTE_SNCF_RESEAU",
        "Conversion du prêt accordé à Air France en instrument de capital": "NB_AIR_FRANCE",
        "Bouclier tarifaire - électricité - relèvement plafond ARENH": "NB_ARENH",
        "Dotations non consommable vers BPIFrance participations (FII)": "NB_BPIFRANCE_FII",
        "Reprise de trésorerie pour soutien au commerce extérieur": "NB_COMMERCE_EXTERIEUR",
        "CSPE - ZNI": "NB_CSPE_ZNI",
        "Crédit-bail": "NB_CREDIT_BAIL",
        "Opérations non-budgétaires affectant le besoin de financement (3) / Autres": "NB_AUTRES",
    }.items()},
}
LIGNES_3108 = {
    "Résultat comptable du régime général de la sécurité sociale (CNAF, CNAM, CNAV, CNSA* et FSV) - RC":
        ("COMPTES_SECU.RESULTAT_COMPTABLE", "REGIME_GENERAL"),
    "Capacité (+) / Besoin (-) de financement du régime général au sens de Maastricht = RC + (1)":
        ("SEC2010.B9", "REGIME_GENERAL"),
    "Capacité (+) / Besoin (-) de financement des administrations de sécurité sociale hors régime général (2)":
        ("SEC2010.B9", "S1314_HORS_RG"),
    "Caisse d'amortissement de la dette sociale (CADES)": ("SEC2010.B9", "CADES"),
    "Fonds de réserve des retraites (FRR)": ("SEC2010.B9", "FRR"),
    "Autres régimes de sécurité sociale, dont assurance chômage": ("SEC2010.B9", "AUTRES_REGIMES_SECU"),
    "Organismes dépendant des administrations de sécurité sociale (dont hôpitaux publics)": ("SEC2010.B9", "S13142"),
    "Capacité (+) / Besoin (-) de financement de l'ensemble des administrations de sécurité sociale au sens de "
    "Maastricht - D = RC + (1) + (2)": ("SEC2010.B9", "S1314"),
    **{libelle: (_S + code, "REGIME_GENERAL") for libelle, code in {
        "Corrections réalisées en comptabilité nationale (1)": "CORRECTIONS",
        "Opérations du compte de résultat non reprises en comptabilité nationale": "COMPTE_RESULTAT_NON_REPRIS",
        "Opérations du bilan traitées en dépense ou recette en comptabilité nationale": "OPERATIONS_BILAN",
        "Étalement du versement de la soulte IEG de 2005": "SOULTE_IEG",
        "Produit de la soulte IEG gérée par le FRR au profit de la CNAV": "PRODUIT_SOULTE_IEG_FRR",
        "Gestion du FCAATA isolée de la CNAM jusqu'en 2011": "FCAATA",
        "Opérations de réconciliation des transferts entre administrations publiques": "RECONCILIATION_TRANSFERTS",
        "Mises en réserve de l'ex section II du FSV": "RESERVES_FSV",
        "Ajustement lié à l’estimation des impôts et cotisations susceptibles de ne pas être recouvrés": "NON_RECOUVREMENT",
        "Correction liée aux impôts et cotisations des indépendants dus au titre de 2020 et suspendus lors de la première "
        "vague de l'épidémie de covid-19": "INDEPENDANTS_COVID",
        "Autres corrections de droit constaté": "DROITS_CONSTATES",
        "Corrections réalisées en comptabilité nationale (1) / Autres": "AUTRES",
    }.items()},
}

# Tableau 3.215 : en-tête du bloc d'un sous-secteur → périmètre ; ligne → concept. Les dépenses et les recettes d'un
# sous-secteur sont consolidées en son sein, pas entre sous-secteurs : elles ne s'additionnent pas.
PERIMETRES_3215 = {"Etat (S13111)": "S13111", "ODAC (S13112)": "S13112", "Administrations publiques locales (S1313)": "S1313",
                   "Administrations de sécurité sociale (S1314)": "S1314", "Ensemble": "S13"}
LIGNES_3215 = {"-Dépenses": "SEC2010.TE", "-Recettes": "SEC2010.TR"}

# Tableaux de la dette. 3.102 : code de l'instrument (colonne A) → concept, sous l'en-tête du bloc de chaque sous-secteur ;
# la dette d'un sous-secteur y est, comme au tableau 3.101, sa contribution à la dette consolidée de l'ensemble.
INSTRUMENTS_3102 = {"F2N": "PDE.GD_F2", "F31_32": "PDE.GD_F3", "F31": "PDE.GD_F31", "F32": "PDE.GD_F32",
                    "F41": "PDE.GD_F41", "F42": "PDE.GD_F42", "GD": "PDE.GD"}
# 3.103 : en-tête de bloc → (concept, unité, consolidation), une ligne par sous-secteur.
BLOCS_3103 = {"Dette nette en milliards d'euros": ("INSEE_DETTE.DETTE_NETTE", "MD_EUR", "consolide"),
              "Dette nette en % du PIB": ("INSEE_DETTE.DETTE_NETTE", "PC_PIB", "consolide"),
              "Autres actifs liquides en milliards d'euros (**)": ("INSEE_DETTE.AUTRES_ACTIFS_LIQUIDES", "MD_EUR",
                                                                   "non_precise")}
# 3.104 : libellé → concept, sous l'en-tête du bloc de chaque sous-secteur. Le total des passifs et les lignes qui le
# rapprochent de la dette portent sur des passifs non consolidés ; la dette au sens de Maastricht est consolidée.
LIGNES_3104 = {"Total des passifs en comptabilité nationale (TP)": "INSEE_DETTE.TOTAL_PASSIFS",
               "Différence de champ (1)": "INSEE_DETTE.DIFFERENCE_CHAMP",
               "Comptes à payer et produits dérivés": "INSEE_DETTE.COMPTES_A_PAYER_DERIVES",
               "Dépôts de garantie": "INSEE_DETTE.DEPOTS_GARANTIE",
               "Passage à la dette consolidée (2)": "INSEE_DETTE.PASSAGE_DETTE_CONSOLIDEE",
               "Consolidation des dépôts": "INSEE_DETTE.CONSOLIDATION_DEPOTS",
               "Consolidation des titres de créance": "INSEE_DETTE.CONSOLIDATION_TITRES",
               "Consolidation des crédits": "INSEE_DETTE.CONSOLIDATION_CREDITS",
               "Passage à la valeur nominale (3)": "INSEE_DETTE.PASSAGE_VALEUR_NOMINALE",
               "Intérêts courus non échus (ICNE) sur dépôts": "INSEE_DETTE.ICNE_DEPOTS",
               "Écart de valorisation sur obligations (y.c. ICNE)": "INSEE_DETTE.ECART_VALORISATION_OBLIGATIONS",
               "Intérêts courus non échus sur crédits": "INSEE_DETTE.ICNE_CREDITS",
               "Dette au sens de Maastricht = TP - (1) - (2) - (3)": "PDE.GD",
               "Contribution à la dette au sens de Maastricht = TP - (1) - (2) - (3)": "PDE.GD"}
# 3.105 : libellé → (concept, consolidation), pour l'ensemble des administrations publiques. Le déficit y est compté
# positivement.
LIGNES_3105 = {
    "Déficit des administrations publiques (*) - D": ("INSEE_DETTE.DEFICIT", "sans_objet"),
    "Acquisitions d'actifs nettes des cessions et hors autres comptes à recevoir (1)":
        ("INSEE_DETTE.ACQUISITIONS_NETTES_ACTIFS", "non_precise"),
    "F2 Numéraires et dépôts": ("INSEE_DETTE.ACQUISITIONS_F2", "non_precise"),
    "F3 Titres hors actions": ("INSEE_DETTE.ACQUISITIONS_F3", "non_precise"),
    "F4 Crédits": ("INSEE_DETTE.ACQUISITIONS_F4", "non_precise"),
    "F5 Actions et autres participations": ("INSEE_DETTE.ACQUISITIONS_F5", "non_precise"),
    "F71 Produits dérivés financiers": ("INSEE_DETTE.ACQUISITIONS_F71", "non_precise"),
    "F6 Réserve d'assurances": ("INSEE_DETTE.ACQUISITIONS_F6", "non_precise"),
    "Variation du passif financier hors dette de Maastricht et hors autres comptes à payer (2)":
        ("INSEE_DETTE.VARIATION_PASSIF_HORS_DETTE", "non_precise"),
    "F28, F38, F48 Intérêts courus non échus (y.c étalements des primes et décôtes)":
        ("INSEE_DETTE.VARIATION_ICNE", "non_precise"),
    "F1, F5, F6, F7 Autres passifs hors dettes de Maastricht et hors autres comptes à payer":
        ("INSEE_DETTE.VARIATION_AUTRES_PASSIFS", "non_precise"),
    "Changements de volume inclus dans la dette de Maastricht (3)": ("INSEE_DETTE.CHANGEMENTS_VOLUME", "non_precise"),
    "K10, K12 Changement de classement et autres changements de volume": ("INSEE_DETTE.RECLASSEMENTS", "non_precise"),
    "K11 Valorisation de la dette en devises": ("INSEE_DETTE.VALORISATION_DEVISES", "non_precise"),
    "K14 Gains/Pertes sur rachats de titres": ("INSEE_DETTE.RACHATS_TITRES", "non_precise"),
    "F8 Solde des autres comptes à recevoir/à payer (4)": ("INSEE_DETTE.SOLDE_AUTRES_COMPTES", "non_precise"),
    "Ecart statistique B9nf - B9f (5)": ("INSEE_DETTE.ECART_STATISTIQUE", "non_precise"),
    "Variation de la dette au sens de Maastricht = D + (1) + (2) + (3) + (4) + (5)": ("INSEE_DETTE.VARIATION_DETTE",
                                                                                      "consolide"),
}
# Libellés de lignes sans chiffre, dont les cellules ne portent que des zéros de mise en page.
SANS_CHIFFRES = {"", "En milliards d'euros"}

# Tableaux 7.301 à 7.306 : (code de l'opération en colonne A, côté du compte) → concept. Un solde (B…) est l'emploi
# d'un compte et la ressource du suivant : il a le même concept des deux côtés. Une opération reçue (ressource) prend
# le suffixe REC, une opération versée (emploi) le suffixe PAY, comme dans les tableaux 3.201 à 3.214 ; les produits
# (P…) et les acquisitions d'actifs non produits (NP) n'en ont pas. Le SEC 2010 inscrit avec un signe négatif les
# subventions et les transferts en capital versés, en ressources, et les subventions reçues par les administrations
# productrices, en emplois : ces lignes ont leurs propres concepts (…_EN_RESSOURCES, …_EN_EMPLOIS).
PERIMETRES_73XX = {"7301": "S13", "7302": "S1311", "7303": "S13111", "7304": "S13112", "7305": "S1313", "7306": "S1314"}
_SOLDES_73XX = ["B1G", "B1N", "B2G", "B2N", "B5G", "B5N", "B6G", "B6N", "B7G", "B7N", "B8G", "B8N", "B9"]
_PRODUITS_73XX = {"Ressources": ["P1", "P11", "P12", "P13"],
                  "Emplois": ["P2", "P51C", "P3", "P31", "P32", "P4", "P5", "P51G", "P52", "NP"]}
_OPERATIONS_73XX = {
    "Ressources": ["D2", "D21", "D211", "D212", "D214", "D29", "D291", "D292", "D4", "D41", "D42", "D421", "D422", "D43",
                   "D44", "D45", "D5", "D51", "D59", "D61", "D611", "D612", "D613", "D613CE", "D613NSI", "D7", "D7S",
                   "D71", "D72", "D73", "D731", "D732", "D733", "D74", "D75", "D751", "D759", "D76"],
    "Emplois": ["D1", "D11", "D12", "D121", "D122", "D29", "D291", "D292", "D4", "D41", "D42", "D421", "D422", "D43",
                "D44", "D45", "D5", "D51", "D59", "D62", "D621", "D622", "D623", "D7", "D7S", "D71", "D72", "D73", "D731",
                "D732", "D733", "D74", "D75", "D751", "D759", "D76", "D63", "D631", "D632"]}
LIGNES_73XX = {(code, cote): f"SEC2010.{code}" for code in _SOLDES_73XX for cote in ("Ressources", "Emplois")}
LIGNES_73XX.update({(code, cote): f"SEC2010.{code}" for cote, codes in _PRODUITS_73XX.items() for code in codes})
LIGNES_73XX.update({(code, cote): f"SEC2010.{code}{'REC' if cote == 'Ressources' else 'PAY'}"
                    for cote, codes in _OPERATIONS_73XX.items() for code in codes})
LIGNES_73XX.update({(f"D9{c}R", "Ressources"): f"SEC2010.D9{c}REC" for c in ("", "1", "2", "9")})
LIGNES_73XX.update({(f"D9{c}P", "Ressources"): f"SEC2010.D9{c}PAY_EN_RESSOURCES" for c in ("", "1", "2", "9")})
LIGNES_73XX.update({(f"D3{c}", "Ressources"): f"SEC2010.D3{c}PAY_EN_RESSOURCES" for c in ("", "1", "9", "91", "92", "99")})
LIGNES_73XX.update({("D39", "Emplois"): "SEC2010.D39REC_EN_EMPLOIS", ("D73S", "Ressources"): "SEC2010.D73S"})
# De 1949 à 1977, l'Insee ne ventile pas les transferts courants entre administrations publiques : les autres
# transferts courants de ces années ne les comprennent pas.
NOTE_D7_1949_1977 = ("De 1949 à 1977, hors transferts courants entre administrations publiques (D.73), que l'Insee ne "
                     "ventile pas pour ces années.")


def libelle(cellules, colonne, n):
    return " ".join(str(cellules.get(f"{colonne}{n}", "")).split())


def en_texte(valeur):
    return str(int(valeur)) if isinstance(valeur, float) and valeur.is_integer() else str(valeur).strip()


def entete_des_annees(cellules):
    """Colonne → année, d'après la première ligne qui contient une suite d'années."""
    lignes = {}
    for ref, valeur in cellules.items():
        texte = en_texte(valeur)
        if re.fullmatch(r"(19|20)[0-9]{2}", texte):
            n, colonne = position(ref)
            lignes.setdefault(n, {})[colonne] = texte
    n = min(n for n, annees in lignes.items() if len(annees) >= 3)
    return lignes[n]


def valeurs_de_la_ligne(cellules, n, annees):
    """Valeurs numériques d'une ligne, par colonne ; aucune pour une ligne d'en-tête qui répète les années.

    Une cellule vide ou marquée non disponible (« nd », « N.D. ») n'est pas un chiffre ; tout autre texte
    arrête l'import."""
    contenu = {colonne: cellules[f"{colonne}{n}"] for colonne in annees if f"{colonne}{n}" in cellules}
    if contenu and all(en_texte(v) == annees[colonne] for colonne, v in contenu.items()):
        return {}
    for colonne, v in contenu.items():
        if not isinstance(v, float) and en_texte(v).lower() not in NON_DISPONIBLE:
            sys.exit(f"cellule {colonne}{n} : « {v} » n'est ni un nombre ni une mention de valeur non disponible")
    return {colonne: v for colonne, v in contenu.items() if isinstance(v, float)}


def non_disponibles(cellules, annees):
    """Nombre de cellules marquées non disponibles dans les colonnes des années, pour le compte rendu de l'import."""
    return sum(1 for ref, v in cellules.items()
               if position(ref)[1] in annees and not isinstance(v, float) and en_texte(v).lower() in NON_DISPONIBLE - {""})


def tableau_32xx(numero, cellules, annees):
    perimetre, section = PERIMETRES_32XX[numero], None
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        if texte.upper() in ("DEPENSES", "RECETTES", "SOLDES"):
            section = texte.upper()
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs or section is None:
            continue
        concept = LIGNES_32XX.get((section, texte))
        if concept is None:
            sys.exit(f"tableau {numero}, ligne {n} : libellé sans correspondance ({section}, « {texte} »)")
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre, "concept_id": concept, "unite_id": "MD_EUR", "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": texte, "annee": annees[colonne],
                   "consolidation": "consolide", "ratio": False}


def tableau_dette_ou_deficit(numero, cellules, annees):
    """Tableaux 3.101 (dette) et 3.106 (déficit) : une ligne par sous-secteur, en Md€ puis en % du PIB."""
    concept = {"3101": "PDE.GD", "3106": "SEC2010.B9"}[numero]
    consolidation = {"3101": "consolide", "3106": "sans_objet"}[numero]
    unite = None
    for n in sorted({position(ref)[0] for ref in cellules}):
        code, texte = libelle(cellules, "A", n), libelle(cellules, "B", n)
        if texte.startswith("En milliards"):
            unite = "MD_EUR"
            continue
        if texte.startswith("En % du produit intérieur brut"):
            unite = "PC_PIB"
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if texte.startswith(("Série de PIB", "Série du PIB")):
            ligne = {"perimetre_id": "S1", "concept_id": "SEC2010.B1GQ", "unite_id": "MD_EUR",
                     "consolidation": "sans_objet", "ratio": False}
        else:
            secteur = code or texte.split(" - ")[0]
            if secteur not in SECTEURS or unite is None:
                sys.exit(f"tableau {numero}, ligne {n} : ligne non reconnue (« {code} », « {texte} »)")
            ligne = {"perimetre_id": secteur, "concept_id": concept, "unite_id": unite,
                     "consolidation": consolidation, "ratio": unite == "PC_PIB"}
        for colonne, valeur in valeurs.items():
            yield {**ligne, "valeur": valeur, "cellule": f"{colonne}{n}", "libelle": texte, "annee": annees[colonne]}


def tableau_cofog(numero, cellules, annees):
    """Tableaux 3.301 à 3.307 : une ligne par opération (3.307 : par sous-secteur) et par fonction COFOG,
    codes en colonnes A et C."""
    if libelle(cellules, "A", 2) != "Unité : Milliard d'euros":
        sys.exit(f"tableau {numero} : unité inattendue (« {libelle(cellules, 'A', 2)} »)")
    fonctions = {f["id"] for f in lire("tables/fonctions.csv")}
    for n in sorted({position(ref)[0] for ref in cellules}):
        code, fonction = libelle(cellules, "A", n), libelle(cellules, "C", n)
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if fonction != "_Z" and fonction not in fonctions:
            sys.exit(f"tableau {numero}, ligne {n} : fonction sans correspondance (« {fonction} »)")
        if numero == "3307":
            # Part de chaque sous-secteur dans la dépense consolidée de l'ensemble des administrations publiques :
            # sans les flux internes au sous-secteur, ni ceux avec les autres sous-secteurs.
            if code not in SECTEURS:
                sys.exit(f"tableau {numero}, ligne {n} : sous-secteur sans correspondance (« {code} »)")
            ligne = {"perimetre_id": code, "concept_id": "SEC2010.TE",
                     "consolidation": "consolide" if code == "S13" else "consolide_apu"}
        else:
            if code not in OPERATIONS_33XX:
                sys.exit(f"tableau {numero}, ligne {n} : opération sans correspondance (« {code} »)")
            ligne = {"perimetre_id": PERIMETRES_33XX[numero], "concept_id": OPERATIONS_33XX[code],
                     "consolidation": "consolide"}
        for colonne, valeur in valeurs.items():
            yield {**ligne, "fonction_id": "" if fonction == "_Z" else fonction, "unite_id": "MD_EUR",
                   "valeur": valeur, "cellule": f"{colonne}{n}", "libelle": f"{code}/{fonction}",
                   "annee": annees[colonne], "ratio": False}


def tableau_prelevements(numero, cellules, annees):
    """Tableaux 3.216 et 3.217 : une ligne par bénéficiaire ou par impôt. Le retrait du libellé dit quelle ligne
    en détaille une autre ; le périmètre du tableau 3.217 est l'ensemble des bénéficiaires des prélèvements
    obligatoires, administrations publiques et institutions de l'Union européenne."""
    if not any(libelle(cellules, "B", position(ref)[0]) in ("Milliards d'euros", "En milliards d'euros") for ref in cellules):
        sys.exit(f"tableau {numero} : unité des montants introuvable")
    connues = LIGNES_3216 if numero == "3216" else LIGNES_3217
    unite, pile = "MD_EUR", []  # pile : (retrait, libellé) des lignes qui en contiennent d'autres
    for n in sorted({position(ref)[0] for ref in cellules}):
        brut = str(cellules.get(f"B{n}", ""))
        texte, retrait = " ".join(brut.split()), len(brut) - len(brut.lstrip())
        if not texte:
            continue
        if texte.startswith(("En milliards d'euros", "En % du produit intérieur brut")):
            unite = "MD_EUR" if texte.startswith("En milliards") else "PC_PIB"
        while pile and pile[-1][0] >= retrait:
            pile.pop()
        detaillee = pile[-1][1] if pile else ""
        pile.append((retrait, texte))
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        # Une ligne partielle se lit toujours avec la ligne qu'elle détaille ; une autre, par son libellé s'il suffit.
        partielle = texte.startswith(("dont ", "- ", "en % du PIB"))
        cle = texte if not partielle and texte in connues else f"{detaillee} / {texte}"
        if cle not in connues:
            sys.exit(f"tableau {numero}, ligne {n} : libellé sans correspondance (« {cle} »)")
        concept, perimetre, unite_ligne = connues[cle]
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre or "S13_S212", "concept_id": concept, "unite_id": unite_ligne or unite,
                   "consolidation": "sans_objet", "valeur": valeur, "cellule": f"{colonne}{n}", "libelle": texte,
                   "annee": annees[colonne], "ratio": False}


def tableau_passage(numero, cellules, annees):
    """Tableaux 3.107 et 3.108 : passage d'un solde de comptabilité publique au déficit au sens de Maastricht,
    une ligne par correction, regroupées en rubriques numérotées (1), (2), (3)."""
    if not any(libelle(cellules, "B", position(ref)[0]) == "Milliards d'euros" for ref in cellules):
        sys.exit(f"tableau {numero} : unité des montants introuvable")
    connues = LIGNES_3107 if numero == "3107" else LIGNES_3108
    rubrique = ""
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        if re.search(r"\([123]\)$", texte):
            rubrique = texte
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not texte or not valeurs:
            continue
        cle = f"{rubrique} / {texte}" if texte == "Autres" else texte
        if cle not in connues:
            sys.exit(f"tableau {numero}, ligne {n} : libellé sans correspondance (« {cle} »)")
        concept, perimetre = connues[cle]
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre, "concept_id": concept, "unite_id": "MD_EUR", "consolidation": "sans_objet",
                   "valeur": valeur, "cellule": f"{colonne}{n}", "libelle": texte, "annee": annees[colonne],
                   "ratio": False}


def tableau_3215(cellules, annees):
    """Tableau 3.215 : dépenses et recettes de chaque sous-secteur, en milliards d'euros puis en % du PIB, que le tableau
    ne donne pas."""
    unite = perimetre = None
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        if texte.startswith(("En milliards d'euros", "En % du produit intérieur brut")):
            unite = "MD_EUR" if texte.startswith("En milliards") else "PC_PIB"
            continue
        if texte in PERIMETRES_3215:
            perimetre, bloc = PERIMETRES_3215[texte], texte
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if texte not in LIGNES_3215 or perimetre is None or unite is None:
            sys.exit(f"tableau 3215, ligne {n} : ligne non reconnue (« {texte} »)")
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre, "concept_id": LIGNES_3215[texte], "unite_id": unite, "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": f"{bloc} / {texte}", "annee": annees[colonne],
                   "consolidation": "consolide", "ratio": False}


def bloc_de_secteur(texte):
    """Le sous-secteur qu'annonce l'en-tête d'un bloc (« S1311 - Administration publique centrale »), ou rien."""
    code = texte.split(" - ")[0]
    return code if " - " in texte and code in SECTEURS else None


def tableau_3102(cellules, annees):
    """Tableau 3.102 : la dette au sens de Maastricht de chaque sous-secteur, par instrument, en milliards d'euros."""
    if libelle(cellules, "A", 2) != "Unité : Milliard d'euros":
        sys.exit(f"tableau 3102 : unité inattendue (« {libelle(cellules, 'A', 2)} »)")
    perimetre = None
    for n in sorted({position(ref)[0] for ref in cellules}):
        code, texte = libelle(cellules, "A", n), libelle(cellules, "B", n)
        if not code and bloc_de_secteur(texte):
            perimetre, bloc = bloc_de_secteur(texte), texte
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if code not in INSTRUMENTS_3102 or perimetre is None:
            sys.exit(f"tableau 3102, ligne {n} : ligne non reconnue (« {code} », « {texte} »)")
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre, "concept_id": INSTRUMENTS_3102[code], "unite_id": "MD_EUR",
                   "valeur": valeur, "cellule": f"{colonne}{n}", "libelle": f"{bloc} / {code}", "annee": annees[colonne],
                   "consolidation": "consolide", "ratio": False}


def tableau_3103(cellules, annees):
    """Tableau 3.103 : dette nette de chaque sous-secteur, en milliards d'euros et en % du PIB, que le tableau ne
    donne pas, puis les actifs liquides que la dette nette ne déduit pas."""
    bloc = None
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        if texte in BLOCS_3103:
            bloc = texte
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        secteur = bloc_de_secteur(texte)
        if bloc is None or secteur is None:
            sys.exit(f"tableau 3103, ligne {n} : ligne non reconnue (« {texte} »)")
        concept, unite, consolidation = BLOCS_3103[bloc]
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": secteur, "concept_id": concept, "unite_id": unite, "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": f"{bloc} / {texte}", "annee": annees[colonne],
                   "consolidation": consolidation, "ratio": False}


def tableau_3104(cellules, annees):
    """Tableau 3.104 : pour chaque sous-secteur, du total de ses passifs à sa dette au sens de Maastricht, en milliards
    d'euros."""
    perimetre = None
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        if bloc_de_secteur(texte):
            perimetre, bloc = bloc_de_secteur(texte), texte
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if texte not in LIGNES_3104 or perimetre is None:
            sys.exit(f"tableau 3104, ligne {n} : ligne non reconnue (« {texte} »)")
        concept = LIGNES_3104[texte]
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre, "concept_id": concept, "unite_id": "MD_EUR", "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": f"{bloc} / {texte}", "annee": annees[colonne],
                   "consolidation": "consolide" if concept == "PDE.GD" else "non_consolide", "ratio": False}


def zeros_de_mise_en_page(numero, n, valeurs, ignores):
    """Les cellules d'une ligne sans libellé de chiffre : des zéros de mise en page, comptés, ou l'import s'arrête."""
    if any(v != 0 for v in valeurs.values()):
        sys.exit(f"tableau {numero}, ligne {n} : valeurs sur une ligne sans libellé de chiffre")
    ignores["zéros de mise en page"] += len(valeurs)


def tableau_3105(cellules, annees, ignores):
    """Tableau 3.105 : du déficit de l'ensemble des administrations publiques à la variation de sa dette au sens de
    Maastricht, en milliards d'euros. Ses lignes de séparation portent des zéros."""
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if texte in SANS_CHIFFRES:
            zeros_de_mise_en_page("3105", n, valeurs, ignores)
            continue
        if texte not in LIGNES_3105:
            sys.exit(f"tableau 3105, ligne {n} : libellé sans correspondance (« {texte} »)")
        concept, consolidation = LIGNES_3105[texte]
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": "S13", "concept_id": concept, "unite_id": "MD_EUR", "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": texte, "annee": annees[colonne],
                   "consolidation": consolidation, "ratio": False}


def tableau_comptes(numero, cellules, annees, ignores):
    """Tableaux 7.301 à 7.306 : la séquence des comptes d'un sous-secteur, compte par compte, ressources puis emplois,
    une ligne par opération (code en colonne A), en milliards d'euros. Les comptes ne sont pas consolidés. Un solde,
    emploi d'un compte puis ressource du suivant, n'est lu qu'une fois : ses autres lignes doivent redonner les mêmes
    valeurs."""
    if libelle(cellules, "A", 2) != "Unité : Milliard d'euros":
        sys.exit(f"tableau {numero} : unité inattendue (« {libelle(cellules, 'A', 2)} »)")
    perimetre, compte, cote, soldes = PERIMETRES_73XX[numero], None, None, {}
    for n in sorted({position(ref)[0] for ref in cellules}):
        code, texte = libelle(cellules, "A", n), libelle(cellules, "B", n)
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not code:
            if texte.startswith("Compte "):
                compte, cote = texte, None
            elif texte in ("Ressources", "Emplois"):
                cote = texte
            if valeurs:
                zeros_de_mise_en_page(numero, n, valeurs, ignores)
            continue
        if not valeurs:
            continue
        concept = LIGNES_73XX.get((code, cote))
        if concept is None or compte is None:
            sys.exit(f"tableau {numero}, ligne {n} : opération sans correspondance ({compte}, {cote}, « {code} »)")
        if code in _SOLDES_73XX:
            if concept in soldes:
                if valeurs != soldes[concept]:
                    sys.exit(f"tableau {numero}, ligne {n} : le solde {code} n'a pas les valeurs de sa première ligne")
                ignores["valeurs de soldes repris d'un compte au suivant, vérifiées"] += len(valeurs)
                continue
            soldes[concept] = valeurs
        for colonne, valeur in valeurs.items():
            annee = annees[colonne]
            yield {"perimetre_id": perimetre, "concept_id": concept, "unite_id": "MD_EUR", "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": f"{compte} / {cote} / {code}", "annee": annee,
                   "consolidation": "sans_objet" if code in _SOLDES_73XX else "non_consolide", "ratio": False,
                   "notes": NOTE_D7_1949_1977 if code == "D7" and int(annee) <= 1977 else ""}


def statut(annee, derniere):
    return {derniere: "provisoire", derniere - 1: "semi_definitif"}.get(annee, "definitif")


def lignes_du_fichier(fichier):
    """Les chiffres d'une copie archivée, le nombre de cellules qui y sont marquées non disponibles, et le compte des
    cellules lues qui ne sont pas des chiffres (zéros de mise en page, soldes repris d'un compte au suivant)."""
    numero = fichier["source_id"].removeprefix("insee.t")
    version = fichier["mis_a_jour_source"][:10]
    if not version:
        sys.exit(f"{fichier['id']} : date du classeur absente, version inconnue")
    chemin = BASE / fichier["chemin"]
    # La feuille de données est la première qui n'est pas une feuille de métadonnées (tableau 3.101).
    nom = next(f for f in feuilles_xlsx(chemin) if f.strip().lower() != "métadonnées")
    nom, cellules = lire_xlsx(chemin, nom)
    annees = entete_des_annees(cellules)
    derniere = max(int(a) for a in annees.values())
    ignores = collections.Counter()
    if numero in PERIMETRES_32XX:
        brutes = tableau_32xx(numero, cellules, annees)
    elif numero == "3215":
        brutes = tableau_3215(cellules, annees)
    elif numero in ("3101", "3106"):
        brutes = tableau_dette_ou_deficit(numero, cellules, annees)
    elif numero == "3102":
        brutes = tableau_3102(cellules, annees)
    elif numero == "3103":
        brutes = tableau_3103(cellules, annees)
    elif numero == "3104":
        brutes = tableau_3104(cellules, annees)
    elif numero == "3105":
        brutes = tableau_3105(cellules, annees, ignores)
    elif numero in PERIMETRES_73XX:
        brutes = tableau_comptes(numero, cellules, annees, ignores)
    elif numero in PERIMETRES_33XX or numero == "3307":
        brutes = tableau_cofog(numero, cellules, annees)
    elif numero in ("3216", "3217"):
        brutes = tableau_prelevements(numero, cellules, annees)
    elif numero in ("3107", "3108"):
        brutes = tableau_passage(numero, cellules, annees)
    else:
        sys.exit(f"tableau {numero} non pris en charge")
    brutes, lignes = list(brutes), []
    # Un zéro est exact : il prend la précision de sa ligne, celle de la valeur la plus précise de la ligne.
    precision = {}
    for brute in brutes:
        n = position(brute["cellule"])[0]
        precision[n] = max(precision.get(n, 0), nombre(brute["valeur"])[1])
    for brute in brutes:
        valeur, decimales = nombre(brute["valeur"])
        if float(valeur) == 0:
            decimales = precision[position(brute["cellule"])[0]]
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"feuille={nom};cellule={brute['cellule']};ligne={brute['libelle']};annee={brute['annee']}",
            "zone": "FR", "perimetre_id": brute["perimetre_id"], "concept_id": brute["concept_id"],
            "fonction_id": brute.get("fonction_id", ""), "traitements": "", "unite_id": brute["unite_id"],
            "periode": brute["annee"], "valeur": valeur, "decimales": decimales, "statut": statut(int(brute["annee"]), derniere),
            "drapeau_source": "", "version": version, "consolidation": brute["consolidation"],
            "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(),
            "notes": brute.get("notes", ""),
        }
        if brute["ratio"]:  # le PIB utilisé pour le ratio figure dans le même tableau
            ligne["denominateur_id"] = identifiant({**ligne, "perimetre_id": "S1", "concept_id": "SEC2010.B1GQ",
                                                    "unite_id": "MD_EUR"})
        ligne["id"] = identifiant(ligne)
        lignes.append(ligne)
    return lignes, non_disponibles(cellules, annees), ignores


def resoudre_denominateurs(existants):
    """Un PIB inchangé d'une version à l'autre n'est enregistré qu'une fois : le dénominateur d'un ratio
    renvoie alors à la version la plus récente du PIB qui précède celle du ratio."""
    for ligne in existants.values():
        d = ligne["denominateur_id"]
        if d and d not in existants:
            prefixe = d.rsplit(":", 1)[0] + ":"
            candidats = [i for i in existants if i.startswith(prefixe) and i.rsplit(":", 1)[1] <= ligne["version"]]
            ligne["denominateur_id"] = max(candidats, key=lambda i: i.rsplit(":", 1)[1]) if candidats else d


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    lignes, nd, ignores = lignes_du_fichier(fichier)
    ajoutes, inchanges = fusionner(existants, lignes, fichier["id"])
    resoudre_denominateurs(existants)
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés"
          + (f", {nd} cellules marquées non disponibles" if nd else "")
          + "".join(f", {n} {quoi}" for quoi, n in sorted(ignores.items())) + f" ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
