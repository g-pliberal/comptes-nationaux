#!/usr/bin/env python3
"""Enregistre dans la base les comptes des opérateurs de l'État, opérateur par opérateur, tels que la direction du
budget les publie sur data.economie.gouv.fr avec les annexes des projets de loi de finances.

    python3 outils/importer_operateurs.py <fichier_id>

Deux sources, huit sortes de copies, chacune reconnue à son adresse :

- budget.operateurs-plf2012, les données de l'annexe « Opérateurs de l'État » (le « jaune ») au projet de loi de
  finances pour 2012, quatre jeux de data.economie.gouv.fr, exportés en csv (noms des champs en en-tête, triés par
  programme et par opérateur) : le compte de résultat simplifié de 2010 de chaque opérateur, prévu au budget primitif
  (« bp-2010 ») et constaté au compte financier (« cofi-2010 »), dépenses de personnel, de fonctionnement et
  d'intervention, recettes par origine, et, « pour information », ses dépenses d'investissement au tableau de
  financement abrégé ; puis, dans deux jeux à part, les mêmes comptes des établissements publics à caractère
  scientifique et technologique (EPST : CNRS, Inserm, INRA…), présentés par destination, avec leurs charges et
  produits calculés. Aucun de ces jeux ne dit l'unité de ses montants : ce sont des milliers d'euros, comme dans
  l'annexe dont ils viennent (le CNRS y a 2 255 363 de dépenses de personnel au compte financier de 2010, soit 2,3 milliards d'euros).
- budget.operateurs-plf2019, trois pièces jointes du jeu « annexe budget des opérateurs de l'État pour 2018 » du
  projet de loi de finances pour 2019, tirées des projets annuels de performances, en milliers d'euros, comme le disent
  leurs titres et ceux de leurs colonnes : les autorisations budgétaires du budget initial 2018 de chaque opérateur
  (dépenses par nature en autorisations d'engagement et en crédits de paiement, recettes par origine, solde
  budgétaire), celles des EPST, à part, par destination, son équilibre financier (besoins et financements, variation
  de la trésorerie) et son compte de résultat prévisionnel (charges et produits par nature). Ces pièces sont encodées
  en Windows-1252. Le tableau des autorisations budgétaires donne aux EPST un solde nul et rien d'autre : leurs
  dépenses et leurs recettes sont dans le leur.

Chaque ligne est un opérateur ou une catégorie d'opérateurs (« Universités et assimilés »), rattaché au programme
« chef de file » qui le finance. Il devient un périmètre de la norme OPERATEURS (OPERATEUR_<code>), sous l'ensemble
des opérateurs de l'État (OPERATEURS_ETAT). Le code est le sigle que la ligne met avant « - » (« CNRS - Centre
national de la recherche scientifique » → OPERATEUR_CNRS), à défaut le nom entier (« Atout-France » →
OPERATEUR_ATOUT_FRANCE) : un même sigle réunit ainsi les noms qu'un opérateur prend d'une annexe à l'autre (« IGN -
Institut géographique national » en 2012, « IGN - Institut national de l'information géographique et forestière » en
2019). Les exceptions sont déclarées ci-dessous (CODES) : un sigle qui désigne deux opérateurs différents, ou deux
graphies d'un même nom. Les périmètres des opérateurs sont refaits à chaque import à partir de toutes les copies
archivées des deux sources : le libellé est le nom de l'annexe la plus récente, la définition donne chaque nom et
chaque programme chef de file, annexe par annexe. Deux lignes d'une même copie au même code arrêtent l'import.

Chaque colonne de montants est un concept de la norme OPERATEURS (CONCEPTS), suffixé de ce qu'est le document :
_BP pour le budget primitif 2010, _CF pour le compte financier 2010, _BI pour le budget initial 2018. L'en-tête de chaque
copie doit être exactement celui qu'attend l'import, sinon il s'arrête ; seules les colonnes qui décrivent la ligne
(type de mission, mission, programme, opérateur, comptabilité budgétaire, EPST, ministère) ne donnent pas de chiffres,
et, dans les jeux des EPST, la colonne « EPST EQUILIBRE », qui additionne les charges et les produits calculés. Une case
vide ne donne pas de chiffre ; un zéro en donne un. Le statut est « prévision » pour un budget, « définitif » pour un
compte financier ; la version d'un chiffre est la date de modification du jeu de données. L'emplacement d'un chiffre est
sa ligne dans la copie (l'en-tête est la première) et le nom de sa colonne, que le contrôle de la base relit.
"""

import collections
import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_export_ofgl,
                    nombre_texte, table_des_chiffres)
from importer_lois_resultats import code_lolf

SOURCES = {"budget.operateurs-plf2012": "PLF 2012", "budget.operateurs-plf2019": "PLF 2019"}
NORME = "OPERATEURS"
ENSEMBLE = "OPERATEURS_ETAT"
DESCRIPTION = ["type_de_mission", "mission", "code_du_programme", "programme", "operateur"]
DESCRIPTION_2019 = ["Type de Mission", "Mission", "Code du programme", "Programme", "Opérateur",
                    "Comptabilité budgétaire ?", "EPST ?"]
DESCRIPTION_2019_CHEF = ["Type de Mission Chef de file", "Mission Chef de file", "Code du programme chef de file",
                         "Programme Chef de file", "Opérateur ou catégorie d'opérateur", "Comptabilité budgétaire ?",
                         "EPST ?"]
TYPES_DE_MISSION = {"Budget général", "Budgets annexes", "Comptes d'affectation spéciale"}

# Concepts : code → (libellé, sens, définition).
CONCEPTS = {
    # Compte de résultat simplifié de 2010 (hors EPST), au budget primitif et au compte financier.
    "CR_PERSONNEL": ("Dépenses de personnel du compte de résultat", "depense", ""),
    "CR_FONCTIONNEMENT": ("Dépenses de fonctionnement du compte de résultat", "depense", ""),
    "CR_INTERVENTIONS": ("Dépenses d'intervention du compte de résultat", "depense", ""),
    "CR_DEPENSES": ("Dépenses du compte de résultat", "depense",
                    "Total des dépenses de personnel, de fonctionnement et d'intervention."),
    "CR_SUBVENTIONS_ETAT": ("Recettes du compte de résultat : subventions de l'État", "recette", ""),
    "CR_RESSOURCES_FISCALES": ("Recettes du compte de résultat : ressources fiscales", "recette", ""),
    "CR_AUTRES_SUBVENTIONS": ("Recettes du compte de résultat : autres subventions", "recette", ""),
    "CR_RESSOURCES_PROPRES": ("Recettes du compte de résultat : ressources propres et autres", "recette", ""),
    "CR_RECETTES": ("Recettes du compte de résultat", "recette",
                    "Total des subventions de l'État, des ressources fiscales, des autres subventions et des ressources "
                    "propres."),
    "TFA_INVESTISSEMENT": ("Dépenses d'investissement du tableau de financement abrégé", "depense",
                           "Donné « pour information » à côté du compte de résultat."),
    # Comptes de 2010 des établissements publics à caractère scientifique et technologique, par destination.
    "EPST_PERSONNEL_UNITES": ("Dépenses de personnel des EPST : activités conduites par les unités de recherche",
                              "depense", ""),
    "EPST_PERSONNEL_COMMUNES": ("Dépenses de personnel des EPST : actions communes", "depense", ""),
    "EPST_PERSONNEL_SUPPORT": ("Dépenses de personnel des EPST : fonctions support", "depense", ""),
    "EPST_PERSONNEL": ("Dépenses de personnel des EPST", "depense", ""),
    "EPST_FONCTIONNEMENT_UNITES": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : activités "
                                   "conduites par les unités de recherche", "depense", ""),
    "EPST_FONCTIONNEMENT_COMMUNES": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : actions "
                                     "communes", "depense", ""),
    "EPST_FONCTIONNEMENT_SUPPORT": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : fonctions "
                                    "support", "depense", ""),
    "EPST_FONCTIONNEMENT": ("Dépenses de fonctionnement et d'investissement non programmé des EPST", "depense", ""),
    "EPST_INVESTISSEMENT_COMMUNES": ("Investissement programmé et autres opérations en capital des EPST : actions "
                                     "communes", "depense", ""),
    "EPST_INVESTISSEMENT_SUPPORT": ("Investissement programmé et autres opérations en capital des EPST : fonctions "
                                    "support", "depense", ""),
    "EPST_INVESTISSEMENT": ("Investissement programmé et autres opérations en capital des EPST", "depense", ""),
    "EPST_HORS_AGREGATS": ("Dépenses des EPST hors agrégats", "depense", ""),
    "EPST_SCSP": ("Recettes des EPST : subventions pour charges de service public des ministères de tutelle", "recette",
                  ""),
    "EPST_CONTRATS": ("Recettes des EPST : contrats et soutiens finalisés à l'activité de recherche", "recette", ""),
    "EPST_PRODUITS_VALORISES": ("Recettes des EPST : produits valorisés de l'activité de recherche et prestations de "
                                "services", "recette", ""),
    "EPST_AUTRES": ("Recettes des EPST : autres subventions et produits", "recette", ""),
    "EPST_RECETTES": ("Recettes des EPST", "recette", ""),
    "EPST_CHARGES_CALCULEES": ("Charges calculées des EPST", "depense",
                               "Charges sans décaissement (amortissements, provisions), données sous « équilibre »."),
    "EPST_PRODUITS_CALCULES": ("Produits calculés des EPST", "recette",
                               "Produits sans encaissement (reprises, quote-part des subventions d'investissement), "
                               "donnés sous « équilibre »."),
    # Autorisations budgétaires du budget initial 2018 des EPST, par destination, en AE et en CP.
    "EPST_PENSIONS_CIVILES": ("Dépenses de personnel des EPST : dont charges de pensions civiles", "depense", ""),
    "EPST_PERSONNEL_HORS_AGREGATS": ("Dépenses de personnel des EPST : hors agrégats", "depense", ""),
    "EPST_FONCTIONNEMENT_AE": ("Dépenses de fonctionnement et d'investissement non programmé des EPST, en "
                               "autorisations d'engagement", "depense", ""),
    "EPST_FONCTIONNEMENT_CP": ("Dépenses de fonctionnement et d'investissement non programmé des EPST, en crédits de "
                               "paiement", "depense", ""),
    "EPST_FONCTIONNEMENT_UNITES_AE": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : "
                                      "activités conduites par les unités de recherche, en autorisations d'engagement",
                                      "depense", ""),
    "EPST_FONCTIONNEMENT_UNITES_CP": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : "
                                      "activités conduites par les unités de recherche, en crédits de paiement",
                                      "depense", ""),
    "EPST_FONCTIONNEMENT_COMMUNES_AE": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : actions "
                                        "communes, en autorisations d'engagement", "depense", ""),
    "EPST_FONCTIONNEMENT_COMMUNES_CP": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : actions "
                                        "communes, en crédits de paiement", "depense", ""),
    "EPST_FONCTIONNEMENT_SUPPORT_AE": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : "
                                       "fonctions support, en autorisations d'engagement", "depense", ""),
    "EPST_FONCTIONNEMENT_SUPPORT_CP": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : "
                                       "fonctions support, en crédits de paiement", "depense", ""),
    "EPST_FONCTIONNEMENT_HORS_AGREGATS_AE": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : "
                                             "hors agrégats, en autorisations d'engagement", "depense", ""),
    "EPST_FONCTIONNEMENT_HORS_AGREGATS_CP": ("Dépenses de fonctionnement et d'investissement non programmé des EPST : "
                                             "hors agrégats, en crédits de paiement", "depense", ""),
    "EPST_INVESTISSEMENT_AE": ("Investissement programmé et autres opérations en capital des EPST, en autorisations "
                               "d'engagement", "depense", ""),
    "EPST_INVESTISSEMENT_CP": ("Investissement programmé et autres opérations en capital des EPST, en crédits de "
                               "paiement", "depense", ""),
    "EPST_INVESTISSEMENT_COMMUNES_AE": ("Investissement programmé et autres opérations en capital des EPST : actions "
                                        "communes, en autorisations d'engagement", "depense", ""),
    "EPST_INVESTISSEMENT_COMMUNES_CP": ("Investissement programmé et autres opérations en capital des EPST : actions "
                                        "communes, en crédits de paiement", "depense", ""),
    "EPST_INVESTISSEMENT_SUPPORT_AE": ("Investissement programmé et autres opérations en capital des EPST : fonctions "
                                       "support, en autorisations d'engagement", "depense", ""),
    "EPST_INVESTISSEMENT_SUPPORT_CP": ("Investissement programmé et autres opérations en capital des EPST : fonctions "
                                       "support, en crédits de paiement", "depense", ""),
    "EPST_INVESTISSEMENT_HORS_AGREGATS_AE": ("Investissement programmé et autres opérations en capital des EPST : hors "
                                             "agrégats, en autorisations d'engagement", "depense", ""),
    "EPST_INVESTISSEMENT_HORS_AGREGATS_CP": ("Investissement programmé et autres opérations en capital des EPST : hors "
                                             "agrégats, en crédits de paiement", "depense", ""),
    "EPST_DEPENSES_AE": ("Total des dépenses des EPST en autorisations d'engagement", "depense", ""),
    "EPST_DEPENSES_CP": ("Total des dépenses des EPST en crédits de paiement", "depense", ""),
    # Autorisations budgétaires du budget initial 2018 (comptabilité budgétaire du décret GBCP).
    "AB_PERSONNEL": ("Dépenses de personnel, hors enveloppe recherche (AE = CP)", "depense", ""),
    "AB_FONCTIONNEMENT_AE": ("Dépenses de fonctionnement, hors enveloppe recherche, en autorisations d'engagement",
                             "depense", ""),
    "AB_FONCTIONNEMENT_CP": ("Dépenses de fonctionnement, hors enveloppe recherche, en crédits de paiement", "depense",
                             ""),
    "AB_INTERVENTION_AE": ("Dépenses d'intervention en autorisations d'engagement", "depense", ""),
    "AB_INTERVENTION_CP": ("Dépenses d'intervention en crédits de paiement", "depense", ""),
    "AB_INVESTISSEMENT_AE": ("Dépenses d'investissement, hors enveloppe recherche, en autorisations d'engagement",
                             "depense", ""),
    "AB_INVESTISSEMENT_CP": ("Dépenses d'investissement, hors enveloppe recherche, en crédits de paiement", "depense",
                             ""),
    "AB_RECHERCHE_AE": ("Enveloppe recherche des EPST en autorisations d'engagement", "depense", ""),
    "AB_RECHERCHE_CP": ("Enveloppe recherche des EPST en crédits de paiement", "depense", ""),
    "AB_RECHERCHE_PERSONNEL": ("Dépenses de personnel de l'enveloppe recherche (AE = CP)", "depense", ""),
    "AB_RECHERCHE_FONCTIONNEMENT_AE": ("Dépenses de fonctionnement de l'enveloppe recherche en autorisations "
                                       "d'engagement", "depense", ""),
    "AB_RECHERCHE_FONCTIONNEMENT_CP": ("Dépenses de fonctionnement de l'enveloppe recherche en crédits de paiement",
                                       "depense", ""),
    "AB_RECHERCHE_INVESTISSEMENT_AE": ("Dépenses d'investissement de l'enveloppe recherche en autorisations "
                                       "d'engagement", "depense", ""),
    "AB_RECHERCHE_INVESTISSEMENT_CP": ("Dépenses d'investissement de l'enveloppe recherche en crédits de paiement",
                                       "depense", ""),
    "AB_DEPENSES_AE": ("Total des dépenses en autorisations d'engagement", "depense", ""),
    "AB_DEPENSES_CP": ("Total des dépenses en crédits de paiement", "depense", ""),
    "AB_PENSIONS_CIVILES": ("Dont charges de pensions civiles (AE = CP)", "depense", ""),
    "AB_RECETTES_GLOBALISEES": ("Recettes globalisées", "recette", ""),
    "AB_SCSP": ("Subventions pour charges de service public", "recette", ""),
    "AB_AUTRES_FINANCEMENTS_ETAT": ("Autres financements de l'État", "recette", ""),
    "AB_FISCALITE_AFFECTEE": ("Fiscalité affectée", "recette", ""),
    "AB_AUTRES_FINANCEMENTS_PUBLICS": ("Autres financements publics", "recette", ""),
    "AB_RECETTES_PROPRES": ("Recettes propres", "recette", ""),
    "AB_RECETTES_FLECHEES": ("Recettes fléchées", "recette", ""),
    "AB_FINANCEMENTS_ETAT_FLECHES": ("Financements de l'État fléchés", "recette", ""),
    "AB_AUTRES_FINANCEMENTS_PUBLICS_FLECHES": ("Autres financements publics fléchés", "recette", ""),
    "AB_RECETTES_PROPRES_FLECHEES": ("Recettes propres fléchées", "recette", ""),
    "AB_RECETTES": ("Total des recettes", "recette", "Recettes globalisées et recettes fléchées."),
    "AB_SOLDE_BUDGETAIRE": ("Solde budgétaire", "solde", "Recettes moins dépenses en crédits de paiement."),
    # Équilibre financier du budget initial 2018.
    "EF_DEFICIT_BUDGETAIRE": ("Besoins : solde budgétaire (déficit)", "solde", ""),
    "EF_REMBOURSEMENTS": ("Besoins : remboursements d'emprunts, nouveaux prêts, dépôts et cautionnements (capital)",
                          "agregat", ""),
    "EF_TIERS_DECAISSEMENTS": ("Besoins : opérations au nom et pour le compte de tiers", "agregat", ""),
    "EF_AUTRES_DECAISSEMENTS": ("Besoins : autres décaissements sur comptes de tiers", "agregat", ""),
    "EF_SOUS_TOTAL_BESOINS": ("Opérations ayant un impact négatif sur la trésorerie de l'organisme", "agregat", ""),
    "EF_ABONDEMENT_TRESORERIE": ("Abondement de la trésorerie", "solde", ""),
    "EF_ABONDEMENT_FLECHE": ("Abondement de la trésorerie fléchée", "solde", ""),
    "EF_ABONDEMENT_NON_FLECHE": ("Abondement de la trésorerie non fléchée", "solde", ""),
    "EF_TOTAL_BESOINS": ("Total des besoins", "agregat", ""),
    "EF_EXCEDENT_BUDGETAIRE": ("Financements : solde budgétaire (excédent)", "solde", ""),
    "EF_EMPRUNTS": ("Financements : nouveaux emprunts, remboursements de prêts, dépôts et cautionnements (capital)",
                    "agregat", ""),
    "EF_TIERS_ENCAISSEMENTS": ("Financements : opérations au nom et pour le compte de tiers", "agregat", ""),
    "EF_AUTRES_ENCAISSEMENTS": ("Financements : autres encaissements sur comptes de tiers", "agregat", ""),
    "EF_SOUS_TOTAL_FINANCEMENTS": ("Opérations ayant un impact positif sur la trésorerie de l'organisme", "agregat",
                                   ""),
    "EF_PRELEVEMENT_TRESORERIE": ("Prélèvement sur la trésorerie", "solde", ""),
    "EF_PRELEVEMENT_FLECHE": ("Prélèvement sur la trésorerie fléchée", "solde", ""),
    "EF_PRELEVEMENT_NON_FLECHE": ("Prélèvement sur la trésorerie non fléchée", "solde", ""),
    "EF_TOTAL_FINANCEMENTS": ("Total des financements", "agregat", ""),
    # Compte de résultat prévisionnel 2018. Les comptes que nomment les colonnes sont ceux du plan comptable des
    # établissements publics.
    "CRP_PERSONNEL": ("Charges de personnel", "depense", ""),
    "CRP_PENSIONS_CIVILES": ("Charges de pensions civiles incluses dans les charges de personnel", "depense", ""),
    "CRP_FONCTIONNEMENT": ("Charges de fonctionnement", "depense", ""),
    "CRP_INTERVENTIONS": ("Charges d'intervention", "depense", ""),
    "CRP_C68": ("Charges : dont compte 68 (dotations aux amortissements, dépréciations et provisions)", "depense", ""),
    "CRP_C675": ("Charges : compte 675 (valeurs comptables des éléments d'actif cédés)", "depense", ""),
    "CRP_SCSP": ("Produits : subventions pour charges de service public", "recette", ""),
    "CRP_CREDITS_INTERVENTION": ("Produits : crédits d'intervention", "recette", ""),
    "CRP_FISCALITE_AFFECTEE": ("Produits : fiscalité affectée", "recette", ""),
    "CRP_AUTRES_SUBVENTIONS": ("Produits : autres subventions", "recette", ""),
    "CRP_AUTRES_PRODUITS": ("Produits : autres produits", "recette", ""),
    "CRP_C78": ("Produits : dont compte 78 (reprises sur amortissements, dépréciations et provisions)", "recette", ""),
    "CRP_C775": ("Produits : dont compte 775 (produits des cessions d'éléments d'actif)", "recette", ""),
    "CRP_C777": ("Produits : dont compte 777 (quote-part des subventions d'investissement virée au résultat)", "recette",
                 ""),
}
DOCUMENTS = {"BP": "au budget primitif", "CF": "au compte financier", "BI": "au budget initial"}

# Copies : motif de l'adresse → (colonnes de description, [(colonne, code du concept)], document, année).
COLONNES_CR = [("cr_depenses_personnel_{}_2010", "CR_PERSONNEL"), ("cr_depenses_fonctionnement_{}_2010",
                                                                   "CR_FONCTIONNEMENT"),
               ("cr_depenses_interventions_{}_2010", "CR_INTERVENTIONS"), ("cr_depenses_{}_2010", "CR_DEPENSES"),
               ("cr_recettes_subventions_de_l_etat_{}_2010", "CR_SUBVENTIONS_ETAT"),
               ("cr_recettes_ressources_fiscales_{}_2010", "CR_RESSOURCES_FISCALES"),
               ("cr_recettes_autres_subventions_{}_2010", "CR_AUTRES_SUBVENTIONS"),
               ("cr_recettes_ressources_propres_et_autres_{}_2010", "CR_RESSOURCES_PROPRES"),
               ("cr_recettes_{}_2010", "CR_RECETTES"),
               ("pour_information_tfa_depenses_investissement_{}_2010", "TFA_INVESTISSEMENT")]
COLONNES_EPST = [
    ("epst_depenses_personnel_activites_conduites_par_les_unites_de_recherche_{}_2010", "EPST_PERSONNEL_UNITES"),
    ("epst_depenses_personnel_actions_communes_{}_2010", "EPST_PERSONNEL_COMMUNES"),
    ("epst_depenses_personnel_fonctions_support_{}_2010", "EPST_PERSONNEL_SUPPORT"),
    ("epst_depenses_personnel_{}_2010", "EPST_PERSONNEL"),
    ("epst_depenses_fonctionnement_et_investissement_non_programme_activites_conduites_par_les_unites_de_r",
     "EPST_FONCTIONNEMENT_UNITES"),
    ("epst_depenses_fonctionnement_et_investissement_non_programme_actions_communes_{}_2010",
     "EPST_FONCTIONNEMENT_COMMUNES"),
    ("epst_depenses_fonctionnement_et_investissement_non_programme_fonctions_support_{}_2010",
     "EPST_FONCTIONNEMENT_SUPPORT"),
    ("epst_depenses_fonctionnement_{}_2010", "EPST_FONCTIONNEMENT"),
    ("epst_depenses_investissement_programme_et_autres_operations_en_capital_actions_communes_{}_2010",
     "EPST_INVESTISSEMENT_COMMUNES"),
    ("epst_depenses_investissement_programme_et_autres_operations_en_capital_fonctions_support_{}_2010",
     "EPST_INVESTISSEMENT_SUPPORT"),
    ("{investissements}", "EPST_INVESTISSEMENT"),
    ("epst_depenses_hors_agregats_{}_2010", "EPST_HORS_AGREGATS"),
    ("epst_recettes_subventions_pour_charges_de_service_public_des_ministeres_de_tutelles_{}_2010", "EPST_SCSP"),
    ("epst_recettes_contrats_et_soutiens_finalises_a_l_activite_de_recherche_{}_2010", "EPST_CONTRATS"),
    ("epst_recettes_produits_valorises_de_l_activite_de_recherche_et_prestations_de_services_{}_2010",
     "EPST_PRODUITS_VALORISES"),
    ("epst_recettes_autres_subventions_et_produits_{}_2010", "EPST_AUTRES"),
    ("epst_recettes_{}_2010", "EPST_RECETTES"),
    ("epst_equilibre_charges_calculees_{}_2010", "EPST_CHARGES_CALCULEES"),
    ("epst_equilibre_produits_calcules_{}_2010", "EPST_PRODUITS_CALCULES"),
    ("epst_equilibre_{}_2010", None),  # charges et produits calculés additionnés : pas un chiffre
]
# Le champ du total des investissements des EPST n'a pas le même nom dans les deux jeux.
INVESTISSEMENTS_EPST = {"cf": "epst_depenses_investissements_cf_2010", "bp": "epst_investissements_bp_2010"}
_D, _F, _I = "DEPENSES Personnel", "DEPENSES Fonctionnement et investissement NON programmé", \
    "DEPENSES Investissement  programmé et autres opérations en capital"
COLONNES_EPST_BI = [
    (f"{_D} (A2) : Total (a2+b2+c2+d2) BI 2018 AE=CP", "EPST_PERSONNEL"),
    (f"{_D} : dont charges de pensions civiles BI 2018 AE=CP", "EPST_PENSIONS_CIVILES"),
    (f"{_D} : activités conduites par les unités de recherche (a2) BI 2018 AE=CP", "EPST_PERSONNEL_UNITES"),
    (f"{_D} : actions communes (b2) BI 2018 AE=CP", "EPST_PERSONNEL_COMMUNES"),
    (f"{_D} : fonctions support (c2) BI 2018 AE=CP", "EPST_PERSONNEL_SUPPORT"),
    (f"{_D} : hors agrégats (d2) BI 2018 AE=CP", "EPST_PERSONNEL_HORS_AGREGATS"),
    (f"{_F} (B3) : Total (e3+f3+g3+h3) BI 2018 AE", "EPST_FONCTIONNEMENT_AE"),
    (f"{_F} (B4) : Total (e4+f4+g4+h4) BI 2018 CP", "EPST_FONCTIONNEMENT_CP"),
    (f"{_F} (B3) : activités conduites par les unités de recherche (e3) BI 2018 AE", "EPST_FONCTIONNEMENT_UNITES_AE"),
    (f"{_F} (B4) : activités conduites par les unités de recherche (e4) BI 2018 CP", "EPST_FONCTIONNEMENT_UNITES_CP"),
    (f"{_F} (B3) : actions communes (f3) BI 2018 AE", "EPST_FONCTIONNEMENT_COMMUNES_AE"),
    (f"{_F} (B4) : actions communes (f4) BI 2018 CP", "EPST_FONCTIONNEMENT_COMMUNES_CP"),
    (f"{_F} (B3) : fonctions support (g3) BI 2018 AE", "EPST_FONCTIONNEMENT_SUPPORT_AE"),
    (f"{_F} (B4) : fonctions support (g4) BI 2018 CP", "EPST_FONCTIONNEMENT_SUPPORT_CP"),
    (f"{_F} (B3) : hors agrégats (h3) BI 2018 AE", "EPST_FONCTIONNEMENT_HORS_AGREGATS_AE"),
    (f"{_F} (B4) : hors agrégats (h4) BI 2018 CP", "EPST_FONCTIONNEMENT_HORS_AGREGATS_CP"),
    (f"{_I} (C3) : Total (i3+j3+k3) BI 2018 AE", "EPST_INVESTISSEMENT_AE"),
    (f"{_I} (C4) : Total (i4+j4+k4) BI 2018 CP", "EPST_INVESTISSEMENT_CP"),
    (f"{_I} (C3) : actions commune (i3) BI 2018 AE", "EPST_INVESTISSEMENT_COMMUNES_AE"),
    (f"{_I} (C4) : actions commune (i4) BI 2018 CP", "EPST_INVESTISSEMENT_COMMUNES_CP"),
    (f"{_I} (C3) : fonctions support (j3) BI 2018 AE", "EPST_INVESTISSEMENT_SUPPORT_AE"),
    (f"{_I} (C4) : fonctions support (j4) BI 2018 CP", "EPST_INVESTISSEMENT_SUPPORT_CP"),
    (f"{_I} (C3) : hors agrégats (k3) BI 2018 AE", "EPST_INVESTISSEMENT_HORS_AGREGATS_AE"),
    (f"{_I} (C4) : hors agrégats (k4) BI 2018 CP", "EPST_INVESTISSEMENT_HORS_AGREGATS_CP"),
    ("DEPENSES Total des dépenses (A3+B3+C3) : BI 2018 AE", "EPST_DEPENSES_AE"),
    ("DEPENSES Total des dépenses (A4+B4+C4) : BI 2018 CP", "EPST_DEPENSES_CP"),
    ("RECETTES Subventions pour charges de service public des ministères de tutelles BI 2018", "EPST_SCSP"),
    ("RECETTES Contrats et soutiens finalisés à l'activité de recherche BI 2018", "EPST_CONTRATS"),
    ("RECETTES Produits valorisés de l'activité de recherche et prestations de services BI 2018",
     "EPST_PRODUITS_VALORISES"),
    ("RECETTES Autres subventions et produits BI 2018", "EPST_AUTRES"),
    ("RECETTES Total des recettes BI 2018", "EPST_RECETTES"),
    ("Code Ministère", None), ("Ministère", None),
]
COLONNES_AB = [
    ("DEPENSES BI 2018 Personnel  (a)  (AE=CP) (hors env. Rech)", "AB_PERSONNEL"),
    ("DEPENSES BI 2018 Fonctionnement (b)  (AE)  (hors env. Rech)", "AB_FONCTIONNEMENT_AE"),
    ("DEPENSES BI 2018 Fonctionnement (b)  (CP)  (hors env. Rech)", "AB_FONCTIONNEMENT_CP"),
    ("DEPENSES BI 2018 Intervention (c)  (AE)", "AB_INTERVENTION_AE"),
    ("DEPENSES BI 2018 Intervention (c)  (CP)", "AB_INTERVENTION_CP"),
    ("DEPENSES BI 2018 Investissement (d)  (AE)  (hors env. Rech)", "AB_INVESTISSEMENT_AE"),
    ("DEPENSES BI 2018 Investissement (d)  (CP)  (hors env. Rech)", "AB_INVESTISSEMENT_CP"),
    ("DEPENSES BI 2018 Total Enveloppe recherche (e=f+g+h)  (AE)", "AB_RECHERCHE_AE"),
    ("DEPENSES BI 2018 Total Enveloppe recherche (e=f+g+h)  (CP)", "AB_RECHERCHE_CP"),
    ("DEPENSES BI 2018 Personnel Enveloppe recherche (f)  (AE = CP)", "AB_RECHERCHE_PERSONNEL"),
    ("DEPENSES BI 2018 Fonctionnement Enveloppe recherche (g)  (AE)", "AB_RECHERCHE_FONCTIONNEMENT_AE"),
    ("DEPENSES BI 2018 Fonctionnement Enveloppe recherche (g) (CP)", "AB_RECHERCHE_FONCTIONNEMENT_CP"),
    ("DEPENSES BI 2018 Investissement Enveloppe recherche (h)  (AE)", "AB_RECHERCHE_INVESTISSEMENT_AE"),
    ("DEPENSES BI 2018 Investissement Enveloppe recherche (h) (CP)", "AB_RECHERCHE_INVESTISSEMENT_CP"),
    ("DEPENSES BI 2018 TOTAL DES DEPENSES (a+b+c+d+e)  (AE)", "AB_DEPENSES_AE"),
    ("DEPENSES BI 2018 TOTAL DES DEPENSES (a+b+c+d+e) (CP)", "AB_DEPENSES_CP"),
    ("DEPENSES BI 2018 dont charges de pensions civiles  (AE=CP)", "AB_PENSIONS_CIVILES"),
    ("RECETTES BI 2018 Recettes globalisées (i=j+k+l+m+n)", "AB_RECETTES_GLOBALISEES"),
    ("RECETTES BI 2018 Subventions pour charges de service public (j)", "AB_SCSP"),
    ("RECETTES BI 2018 Autres financements de l'Etat (k)", "AB_AUTRES_FINANCEMENTS_ETAT"),
    ("RECETTES BI 2018 Fiscalité affectée (l)", "AB_FISCALITE_AFFECTEE"),
    ("RECETTES BI 2018 Autres financements publics (m)", "AB_AUTRES_FINANCEMENTS_PUBLICS"),
    ("RECETTES BI 2018 Recettes propres (n)", "AB_RECETTES_PROPRES"),
    ("RECETTES BI 2018 Recettes fléchées (o=p+q+r)", "AB_RECETTES_FLECHEES"),
    ("RECETTES BI 2018 Financements de l'Etat fléchés (p)", "AB_FINANCEMENTS_ETAT_FLECHES"),
    ("RECETTES BI 2018 Autres financements publics fléchés (q)", "AB_AUTRES_FINANCEMENTS_PUBLICS_FLECHES"),
    ("RECETTES BI 2018 Recettes propres fléchées (r)", "AB_RECETTES_PROPRES_FLECHEES"),
    ("RECETTES BI 2018 TOTAL DES RECETTES (i+o)", "AB_RECETTES"),
    ("RECETTES BI 2018 SOLDE BUDGETAIRE (Recettes - Dépenses (CP)", "AB_SOLDE_BUDGETAIRE"),
    ("Code Ministère chef de file", None), ("Ministère Chef de file", None), ("", None),
]
COLONNES_EF = [
    ("BESOINS 2018 Solde budgétaire (déficit)  (D2)", "EF_DEFICIT_BUDGETAIRE"),
    ("BESOINS 2018 Remboursements d'emprunts (capital) ; Nouveaux prêts (capital) ; Dépôts et cautionnements (b1)",
     "EF_REMBOURSEMENTS"),
    ("BESOINS 2018 Opérations au nom et pour le compte de tiers (c1)", "EF_TIERS_DECAISSEMENTS"),
    ("BESOINS 2018 Autres décaissements sur comptes de tiers (e1)", "EF_AUTRES_DECAISSEMENTS"),
    ("BESOINS 2018 Sous-total des opérations ayant un impact Négatif sur la trésorerie de l'organisme "
     "(1)=(D2)+(b1)+(c1)+(e1)", "EF_SOUS_TOTAL_BESOINS"),
    ("BESOINS 2018 ABONDEMENT de la trésorerie (l)=(2)-(1)", "EF_ABONDEMENT_TRESORERIE"),
    ("BESOINS 2018 dont Abondement de la trésorerie fléchée (a1)", "EF_ABONDEMENT_FLECHE"),
    ("BESOINS 2018 dont Abondement de la trésorerie non fléchée (f1)", "EF_ABONDEMENT_NON_FLECHE"),
    ("BESOINS 2018 TOTAL DES BESOINS (1+l)", "EF_TOTAL_BESOINS"),
    ("FINANCEMENT 2018 Solde budgétaire (excédent) (D1)", "EF_EXCEDENT_BUDGETAIRE"),
    ("FINANCEMENT 2018 Nouveaux emprunts (capital) ; Remboursements de prêts (capital) ; Dépôts et cautionnements (b2)",
     "EF_EMPRUNTS"),
    ("FINANCEMENT 2018 Opérations au nom et pour le compte de tiers (c2)", "EF_TIERS_ENCAISSEMENTS"),
    ("FINANCEMENT 2018 Autres encaissements sur comptes de tiers (e2)", "EF_AUTRES_ENCAISSEMENTS"),
    ("FINANCEMENT 2018 Sous-total des opérations ayant un impact Positif sur la trésorerie de l'organisme "
     "(2)=(D1)+(b2)+(c2)+(e2)", "EF_SOUS_TOTAL_FINANCEMENTS"),
    ("FINANCEMENT 2018 PRELEVEMENT de la trésorerie (ll)=(1)-(2)", "EF_PRELEVEMENT_TRESORERIE"),
    ("FINANCEMENT 2018 dont Prélèvement sur la trésorerie fléchée (a2)", "EF_PRELEVEMENT_FLECHE"),
    ("FINANCEMENT 2018 dont Prélévement sur la trésorerie non fléchée (f2)", "EF_PRELEVEMENT_NON_FLECHE"),
    ("FINANCEMENT 2018 TOTAL DES FINANCEMENTS  (2+ll)", "EF_TOTAL_FINANCEMENTS"),
    ("Code Ministère", None), ("Ministère", None),
]
COLONNES_CRP = [
    ("Charges : Personnel 2018", "CRP_PERSONNEL"),
    ("Charges : Charges de pensions civiles incluses dans Personnel 2018", "CRP_PENSIONS_CIVILES"),
    ("Charges : Fonctionnement 2018", "CRP_FONCTIONNEMENT"), ("Charges : Interventions 2018", "CRP_INTERVENTIONS"),
    ("Charges : dont C68 2018", "CRP_C68"), ("Charges : C675 2018", "CRP_C675"),
    ("Produits : Subventions pour charge de service public 2018", "CRP_SCSP"),
    ("Produits : Crédits d'intervention 2018", "CRP_CREDITS_INTERVENTION"),
    ("Produits : Fiscalité affectée 2018", "CRP_FISCALITE_AFFECTEE"),
    ("Produits : Autres subventions 2018", "CRP_AUTRES_SUBVENTIONS"),
    ("Produits : Autres produits 2018", "CRP_AUTRES_PRODUITS"), ("Produits : dont C78 2018", "CRP_C78"),
    ("Produits : dont C775 2018", "CRP_C775"), ("Produits : dont C777 2018", "CRP_C777"),
    ("Code Ministère", None), ("Ministère", None),
]
_EXPORT = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/{}/exports/csv?order_by=code_du_programme," \
          "operateur"
_PIECE = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/projet-de-loi-de-finances-pour-2019-plf-2019" \
         "-annexe-budget-des-operateurs-de-let/attachments/{}"


def _epst(document):
    return [(c.format(document) if c != "{investissements}" else INVESTISSEMENTS_EPST[document], k)
            for c, k in COLONNES_EPST]


COPIES = {
    _EXPORT.format("plf2012-jaune-donnees-operateurs-bp-2010"):
        (DESCRIPTION, [(c.format("bp"), k) for c, k in COLONNES_CR], "BP", "2010"),
    _EXPORT.format("plf2012-jaune-donnees-operateurs-cofi-2010"):
        (DESCRIPTION, [(c.format("cf"), k) for c, k in COLONNES_CR], "CF", "2010"),
    _EXPORT.format("plf2012-jaune-donnees-operateurs-epst-bp-2010"): (DESCRIPTION, _epst("bp"), "BP", "2010"),
    _EXPORT.format("plf2012-jaune-donnees-operateurs-epst-cofi-2010"): (DESCRIPTION, _epst("cf"), "CF", "2010"),
    _PIECE.format("plf2019_autorisations_budgetaires_bi_2018_en_keu_csv"):
        (DESCRIPTION_2019_CHEF, COLONNES_AB, "BI", "2018"),
    _PIECE.format("plf2019_operateurs_autorisations_budgetaires_du_bi_2018_des_epst_csv"):
        (DESCRIPTION_2019, COLONNES_EPST_BI, "BI", "2018"),
    _PIECE.format("plf2019_equilibre_financier_en_keu_perimetre_operateurs_en_comptabilite_budgetaire_yc_epst_csv"):
        (DESCRIPTION_2019_CHEF, COLONNES_EF, "BI", "2018"),
    _PIECE.format("plf2019_operateurs_compte_de_resultat_previsionnel_des_operateurs_pour_2018_csv"):
        (DESCRIPTION_2019, COLONNES_CRP, "BI", "2018"),
}

# Codes déclarés : nom tel que l'écrit l'annexe → code. Un sigle qui désigne deux opérateurs, et les graphies d'un même
# nom qui donneraient deux codes.
CODES = {
    "ANSP - Agence Nationale de Santé Publique": "SANTE_PUBLIQUE_FRANCE",  # l'ANSP de 2010 : services à la personne
    "CAMPUSFRANCE": "CAMPUS_FRANCE",
    "FRANCE AGRI MER": "FRANCEAGRIMER",
    "UNIVERSCIENCE (fusion de la CSI et du Palais de la découverte)": "UNIVERSCIENCE",
}


def propre(texte):
    return " ".join(texte.split())


def code_operateur(nom):
    """Le code d'un opérateur : celui que déclare CODES, à défaut le sigle avant « - », à défaut le nom entier."""
    nom = propre(nom)
    if nom in CODES:
        return CODES[nom]
    trouve = re.match(r"(.{1,25}?) - ", nom)
    return code_lolf(trouve.group(1) if trouve else nom)


def sorte(fichier):
    if fichier["source_id"] not in SOURCES:
        sys.exit(f"{fichier['id']} : source inattendue ({', '.join(SOURCES)})")
    if fichier["url"] not in COPIES:
        sys.exit(f"{fichier['id']} : adresse inattendue ({fichier['url']})")
    return COPIES[fichier["url"]]


def lignes_operateurs(fichier):
    """[(n° de ligne, valeurs, programme chef de file, nom de l'opérateur)] d'une copie, son en-tête vérifié."""
    description, colonnes, _, _ = sorte(fichier)
    entete, lignes = lire_export_ofgl(BASE / fichier["chemin"])
    attendu = description + [c for c, _ in colonnes]
    if entete != attendu:
        ecart = next((a, b) for a, b in zip(entete + [None] * len(attendu), attendu + [None] * len(entete)) if a != b)
        sys.exit(f"{fichier['id']} : en-tête inattendu (colonne « {ecart[0]} », attendu « {ecart[1]} »)")
    resultat = []
    for n, valeurs in enumerate(lignes, start=2):
        if len(valeurs) != len(entete):
            sys.exit(f"{fichier['id']}, ligne {n} : {len(valeurs)} valeurs, {len(entete)} colonnes")
        if valeurs[0] not in TYPES_DE_MISSION:
            sys.exit(f"{fichier['id']}, ligne {n} : type de mission inattendu « {valeurs[0]} »")
        if not re.fullmatch(r"P[0-9]{3}", valeurs[2]) or not propre(valeurs[4]):
            sys.exit(f"{fichier['id']}, ligne {n} : programme « {valeurs[2]} » ou opérateur « {valeurs[4]} » inattendus")
        resultat.append((n, valeurs, f"{valeurs[2][1:]} « {propre(valeurs[3])} »", propre(valeurs[4])))
    codes = collections.Counter(code_operateur(nom) for _, _, _, nom in resultat)
    doubles = [c for c, k in codes.items() if k > 1]
    if doubles:
        sys.exit(f"{fichier['id']} : plusieurs lignes au même code d'opérateur : {', '.join(sorted(doubles))}")
    return resultat


def chiffres(fichier):
    _, colonnes, document, annee = sorte(fichier)
    entete = lire_export_ofgl(BASE / fichier["chemin"])[0]
    for n, valeurs, _, nom in lignes_operateurs(fichier):
        for colonne, code in colonnes:
            texte = valeurs[entete.index(colonne)].strip()
            if code is None or not texte:
                continue
            lu = nombre_texte(texte)
            if lu is None:
                sys.exit(f"{fichier['id']}, ligne {n}, colonne « {colonne} » : « {texte} » n'est pas un nombre")
            ligne = {
                "source_id": fichier["source_id"], "fichier_id": fichier["id"],
                "emplacement": f"ligne={n};colonne={colonne}", "zone": "FR",
                "perimetre_id": f"OPERATEUR_{code_operateur(nom)}", "concept_id": f"{NORME}.{code}_{document}",
                "fonction_id": "", "traitements": "", "unite_id": "K_EUR", "periode": annee, "valeur": lu[0],
                "decimales": lu[1], "statut": "definitif" if document == "CF" else "prevision", "drapeau_source": "",
                "version": fichier["mis_a_jour_source"][:10], "consolidation": "non_consolide", "denominateur_id": "",
                "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": "",
            }
            ligne["id"] = identifiant(ligne)
            yield ligne


def referentiels():
    """(normes, concepts, périmètres) de la base, avec ceux de la norme OPERATEURS refaits : ses concepts d'après
    CONCEPTS, ses périmètres d'après toutes les copies archivées des deux sources."""
    normes = {n["id"]: n for n in lire("tables/normes.csv")}
    normes[NORME] = {"id": NORME, "libelle": "Comptes des opérateurs de l'État (annexes budgétaires)",
                     "reference": "Annexe « Opérateurs de l'État » et projets annuels de performances des projets de "
                                  "loi de finances, que prévoit l'article 51 de la loi organique relative aux lois de "
                                  "finances ; comptabilité des établissements publics nationaux, budgétaire et "
                                  "générale, du décret n° 2012-1246 relatif à la gestion budgétaire et comptable "
                                  "publique (titre III)",
                     "url": "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000026597003"}
    concepts = {c["id"]: c for c in lire("tables/concepts.csv") if c["norme_id"] != NORME}
    documents = collections.defaultdict(set)
    for _, colonnes, document, _ in COPIES.values():
        for _, code in colonnes:
            if code:
                documents[code].add(document)
    for code, (libelle, sens, definition) in CONCEPTS.items():
        if not documents[code]:
            sys.exit(f"concept {code} sans colonne")
        for document in sorted(documents[code]):
            identifiant_ = f"{NORME}.{code}_{document}"
            concepts[identifiant_] = {"id": identifiant_, "libelle": f"{libelle}, {DOCUMENTS[document]}",
                                      "norme_id": NORME, "code_norme": f"{code}_{document}", "sens": sens,
                                      "definition": definition}
    perimetres = {p["id"]: p for p in lire("tables/perimetres.csv") if p["norme_id"] != NORME}
    perimetres[ENSEMBLE] = {"id": ENSEMBLE, "libelle": "Opérateurs de l'État", "norme_id": NORME, "parent_id": "",
                            "definition": "Organismes distincts de l'État, dotés de la personnalité morale, qui exercent "
                                          "une activité de service public financée pour l'essentiel par lui et qu'il "
                                          "contrôle, et que les annexes budgétaires présentent un à un ou par "
                                          "catégorie. La plupart sont des organismes divers d'administration centrale "
                                          "(S13112) de la comptabilité nationale, mais les deux listes ne se "
                                          "recouvrent pas."}
    vus = collections.defaultdict(lambda: collections.defaultdict(set))  # code → édition → {(nom, programme)}
    for fichier in lire("tables/fichiers.csv"):
        if fichier["source_id"] in SOURCES:
            for _, _, programme, nom in lignes_operateurs(fichier):
                vus[code_operateur(nom)][SOURCES[fichier["source_id"]]].add((nom, programme))
    for code, editions in vus.items():
        derniere = editions[max(editions)]
        noms = sorted({nom for nom, _ in derniere})
        textes = []
        for edition in sorted(editions):
            noms_ = " ; ".join(f"« {n} »" for n in sorted({n for n, _ in editions[edition]}))
            programmes = " ; ".join(sorted({p for _, p in editions[edition]}))
            textes.append(f"{edition} : {noms_}, programme chef de file {programmes}")
        perimetres[f"OPERATEUR_{code}"] = {
            "id": f"OPERATEUR_{code}", "libelle": noms[0], "norme_id": NORME, "parent_id": ENSEMBLE,
            "definition": "Opérateur de l'État, ou catégorie d'opérateurs, que nomment les annexes budgétaires ("
                          + " ; ".join(textes) + ")."}
    return normes, concepts, perimetres


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    nouveaux = list(chiffres(fichier))
    normes, concepts, perimetres = referentiels()
    ecrire("tables/normes.csv", champs("normes"), normes.values())
    ecrire("tables/concepts.csv", champs("concepts"), concepts.values())
    ecrire("tables/perimetres.csv", champs("perimetres"), perimetres.values())
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, nouveaux, fichier["id"])
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte "
          f"{len(existants)} ; {sum(p['norme_id'] == NORME for p in perimetres.values()) - 1} opérateurs ou "
          f"catégories")


if __name__ == "__main__":
    main()
