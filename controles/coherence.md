# Cohérence des chiffres enregistrés

Fichier généré par `outils/controler_coherence.py` à partir de la base : ne pas le modifier à la main.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la demi-unité de la dernière décimale de chaque valeur en jeu, ou l'unité entière pour l'OFGL, qui arrondit ou tronque selon les cas ses montants à l'euro ; un nombre de budgets n'est pas arrondi et doit être exact. Une incohérence signalée ici est un constat sur la source, pas une erreur d'enregistrement : chaque chiffre a été relu dans sa copie archivée.

## Les sources contrôlées

Pour chaque chiffre, la version la plus récente enregistrée chez sa source.

| Source | Titre | Version la plus récente | Chiffres |
|---|---|---|---|
| dgcl.collectivites-locales-en-chiffres | Les collectivités locales en chiffres : annuaire statistique de la DGCL | 2026-07-30 | 150 |
| dgcl.finances-departements | Les finances des départements : comptes de gestion de chaque département, de la métropole de Lyon, de la Ville de Paris et des collectivités territoriales uniques | 2025-12-29 | 19798 |
| dgcl.finances-regions | Les finances des régions : comptes de gestion de chaque région et des collectivités territoriales uniques | 2025-12-29 | 4070 |
| eurostat.gov_10a_exp | Dépenses des administrations publiques par fonction (COFOG) | 2026-10-21 | 1290 |
| eurostat.gov_10a_main | Recettes, dépenses et principaux agrégats des administrations publiques | 2026-10-21 | 1488 |
| eurostat.nama_10_gdp | PIB et principaux agrégats | 2026-10-21 | 102 |
| insee.bdm-comptes-etat | Situation mensuelle du budget de l'État : dépenses, recettes, solde des comptes spéciaux et solde général d'exécution, cumulés depuis le début de l'année (Banque de données macro-économiques, jeu COMPTES-ETAT) | 2026-10-06 | 848 |
| insee.bdm-dette-trim-apu | Dette trimestrielle des administrations publiques : dette au sens de Maastricht par sous-secteur et par instrument, dette nette, actions cotées et titres d'OPC détenus, dette brute au sens du FMI (Banque de données macro-économiques, jeu DETTE-TRIM-APU-2020) | 2026-09-29 | 2583 |
| insee.liste-odal | Liste des organismes divers d'administration locale (ODAL) : nombre d'organismes par catégorie | 2026-05-18 | 24 |
| insee.t3101 | Tableau 3.101 : Dette des administrations publiques (S13) au sens de Maastricht et sa répartition par sous-secteur | 2026-07-28 | 624 |
| insee.t3102 | Tableau 3.102 : Dette des administrations publiques (S13) au sens de Maastricht et sa répartition par sous-secteurs : décomposition par instrument | 2026-07-28 | 1271 |
| insee.t3103 | Tableau 3.103 : Dette nette des administrations publiques (S13) et autres actifs liquides détenus par les administrations publiques | 2026-08-04 | 558 |
| insee.t3104 | Tableau 3.104 : Passage du total des passifs des administrations publiques (S13) en comptabilité nationale à leur dette au sens de Maastricht | 2026-08-04 | 2418 |
| insee.t3105 | Tableau 3.105 : Passage du déficit des administrations publiques (S13) à la variation de leur dette au sens de Maastricht | 2026-07-28 | 306 |
| insee.t3106 | Tableau 3.106 : Déficit des administrations publiques (S13) au sens de Maastricht | 2026-08-10 | 961 |
| insee.t3107 | Tableau 3.107 : Passage du résultat d'exécution des lois de finances au déficit de l'État (S13111) au sens de Maastricht | 2026-05-27 | 587 |
| insee.t3108 | Tableau 3.108 : Passage du résultat comptable du régime général au déficit des administrations de sécurité sociale (S1314) au sens de Maastricht | 2026-08-26 | 313 |
| insee.t3201 | Tableau 3.201 : Dépenses et recettes des administrations publiques (S13) | 2026-08-10 | 3283 |
| insee.t3202 | Tableau 3.202 : Dépenses et recettes de l'administration publique centrale (S1311) | 2026-05-19 | 2352 |
| insee.t3203 | Tableau 3.203 : Dépenses et recettes de l'État (S13111) | 2026-05-19 | 2352 |
| insee.t3204 | Tableau 3.204 : Dépenses et recettes des organismes divers d'administration centrale (S13112) | 2026-05-19 | 2352 |
| insee.t3205 | Tableau 3.205 : Dépenses et recettes des administrations publiques locales (S1313) | 2026-05-19 | 2352 |
| insee.t3206 | Tableau 3.206 : Dépenses et recettes des collectivités locales (S13131) | 2026-05-19 | 625 |
| insee.t3207 | Tableau 3.207 : Dépenses et recettes des communes (S131311) | 2026-05-19 | 329 |
| insee.t3208 | Tableau 3.208 : Dépenses et recettes des départements (S131312) | 2026-05-19 | 329 |
| insee.t3209 | Tableau 3.209 : Dépenses et recettes des régions (S131313) | 2026-05-19 | 329 |
| insee.t3210 | Tableau 3.210 : Dépenses et recettes des syndicats (S131314) | 2026-05-19 | 329 |
| insee.t3211 | Tableau 3.211 : Dépenses et recettes des organismes divers d'administration locale (S13132) | 2026-05-19 | 625 |
| insee.t3212 | Tableau 3.212 : Dépenses et recettes des administrations de sécurité sociale (S1314) | 2026-08-10 | 2352 |
| insee.t3213 | Tableau 3.213 : Dépenses et recettes des régimes d'assurance sociale (S13141) | 2026-08-10 | 627 |
| insee.t3214 | Tableau 3.214 : Dépenses et recettes des organismes dépendant des assurances sociales - hôpitaux (S13142) | 2026-08-10 | 625 |
| insee.t3215 | Tableau 3.215 : Dépenses et recettes des administrations publiques par sous-secteur | 2026-08-10 | 960 |
| insee.t3216 | Tableau 3.216 : Prélèvements obligatoires par sous-secteurs des administrations publiques et pour l'Union européenne | 2026-05-10 | 1290 |
| insee.t3217 | Tableau 3.217 : Principaux impôts par catégorie | 2026-05-10 | 2655 |
| insee.t3301 | Tableau 3.301 : Dépenses des administrations publiques (S13) ventilées par fonction | 2025-11-28 | 21256 |
| insee.t3302 | Tableau 3.302 : Dépenses de l'administration publique centrale (S1311) ventilées par fonction | 2025-11-28 | 19998 |
| insee.t3303 | Tableau 3.303 : Dépenses de l'État (S13111) ventilées par fonction | 2025-11-28 | 9956 |
| insee.t3304 | Tableau 3.304 : Dépenses des organismes divers d'administration centrale (S13112) ventilées par fonction | 2025-11-28 | 8494 |
| insee.t3305 | Tableau 3.305 : Dépenses des administrations publiques locales (S1313) ventilées par fonction | 2025-11-28 | 18857 |
| insee.t3306 | Tableau 3.306 : Dépenses des administrations de sécurité sociale (S1314) ventilées par fonction | 2025-11-28 | 11594 |
| insee.t3307 | Tableau 3.307 : Répartition par sous-secteur des dépenses consolidées des administrations publiques ventilées par fonction | 2025-11-28 | 5968 |
| insee.t7301 | Tableau 7.301 : Compte des administrations publiques (S13) | 2026-08-27 | 7062 |
| insee.t7302 | Tableau 7.302 : Compte de l'administration publique centrale (S1311) | 2026-08-11 | 6778 |
| insee.t7303 | Tableau 7.303 : Compte de l'État (S13111) | 2026-08-11 | 4580 |
| insee.t7304 | Tableau 7.304 : Compte des organismes divers d'administration centrale (S13112) | 2026-08-11 | 4160 |
| insee.t7305 | Tableau 7.305 : Compte des administrations publiques locales (S1313) | 2026-08-11 | 6364 |
| insee.t7306 | Tableau 7.306 : Compte des administrations de sécurité sociale (S1314) | 2026-08-24 | 6372 |
| ofgl.annexe-2a | Rapport de l'Observatoire des finances et de la gestion publique locales, annexe 2A : budgets principaux des collectivités locales, par niveau de collectivité | 2026-08-17 | 3922 |
| ofgl.annexe-2b | Rapport de l'Observatoire des finances et de la gestion publique locales, annexe 2B : budgets annexes des collectivités locales, par niveau de collectivité | 2026-08-17 | 2444 |
| ofgl.annexe-2c | Rapport de l'Observatoire des finances et de la gestion publique locales, annexe 2C : budgets principaux et annexes consolidés de chaque niveau de collectivité | 2026-04-28 | 1415 |
| ofgl.annexe-2d | Rapport de l'Observatoire des finances et de la gestion publique locales, annexe 2D : niveaux consolidés, bloc communal et ensemble des collectivités locales | 2026-04-29 | 566 |
| senat.pjl06-051 | Projet de loi de financement de la sécurité sociale pour 2007, texte n° 51 (2006-2007) transmis au Sénat le 6 novembre 2006 | 2006-11-06 | 42 |
| senat.pjl06-389 | Projet de loi de règlement du budget de l'année 2006, texte n° 389 (2006-2007) transmis au Sénat le 17 juillet 2007 | 2007-07-17 | 1602 |
| senat.pjl07-067 | Projet de loi de financement de la sécurité sociale pour 2008, texte n° 67 (2007-2008) transmis au Sénat le 6 novembre 2007 | 2007-11-06 | 39 |
| senat.pjl07-429 | Projet de loi de règlement des comptes et rapport de gestion pour l'année 2007, texte n° 429 (2007-2008) transmis au Sénat le 1er juillet 2008 | 2008-07-01 | 1341 |
| senat.pjl08-080 | Projet de loi de financement de la sécurité sociale pour 2009, texte n° 80 (2008-2009) transmis au Sénat le 5 novembre 2008 | 2008-11-05 | 39 |
| senat.pjl08-502 | Projet de loi de règlement des comptes et rapport de gestion pour l'année 2008, texte n° 502 (2008-2009) transmis au Sénat le 30 juin 2009 | 2009-06-30 | 1123 |
| senat.pjl09-082 | Projet de loi de financement de la sécurité sociale pour 2010, texte n° 82 (2009-2010) transmis au Sénat le 3 novembre 2009 | 2009-11-03 | 39 |
| senat.pjl09-585 | Projet de loi de règlement des comptes et rapport de gestion pour l'année 2009, texte n° 585 (2009-2010) transmis au Sénat le 29 juin 2010 | 2010-06-29 | 1075 |
| senat.pjl10-084 | Projet de loi de financement de la sécurité sociale pour 2011, texte n° 84 (2010-2011) transmis au Sénat le 3 novembre 2010 | 2010-11-03 | 36 |
| senat.pjl10-672 | Projet de loi de règlement des comptes et rapport de gestion pour l'année 2010, texte n° 672 (2010-2011) transmis au Sénat le 28 juin 2011 | 2011-06-28 | 1096 |
| senat.pjl11-073 | Projet de loi de financement de la sécurité sociale pour 2012, texte n° 73 (2011-2012) transmis au Sénat le 2 novembre 2011 | 2011-11-02 | 172 |
| senat.pjl11-655 | Projet de loi de règlement des comptes et rapport de gestion pour l'année 2011, texte n° 655 (2011-2012) transmis au Sénat le 10 juillet 2012 | 2012-07-10 | 1094 |
| senat.pjl12-103 | Projet de loi de financement de la sécurité sociale pour 2013, texte n° 103 (2012-2013) transmis au Sénat le 6 novembre 2012 | 2012-11-06 | 179 |
| senat.pjl12-799 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2012, texte n° 799 (2012-2013) transmis au Sénat le 23 juillet 2013 en nouvelle lecture | 2013-07-23 | 1128 |
| senat.pjl13-117 | Projet de loi de financement de la sécurité sociale pour 2014, texte n° 117 (2013-2014) transmis au Sénat le 5 novembre 2013 | 2013-11-05 | 179 |
| senat.pjl13-759 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2013, texte n° 759 (2013-2014) transmis au Sénat le 21 juillet 2014 en nouvelle lecture | 2014-07-21 | 1111 |
| senat.pjl14-078 | Projet de loi de financement de la sécurité sociale pour 2015, texte n° 78 (2014-2015) transmis au Sénat le 3 novembre 2014 | 2014-11-03 | 184 |
| senat.pjl14-642 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2014, texte n° 642 (2014-2015) transmis au Sénat le 16 juillet 2015 en nouvelle lecture | 2015-07-16 | 1168 |
| senat.pjl15-128 | Projet de loi de financement de la sécurité sociale pour 2016, texte n° 128 (2015-2016) transmis au Sénat le 2 novembre 2015 | 2015-11-02 | 194 |
| senat.pjl15-785 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2015, texte n° 785 (2015-2016) transmis au Sénat le 12 juillet 2016 en nouvelle lecture | 2016-07-12 | 1073 |
| senat.pjl16-106 | Projet de loi de financement de la sécurité sociale pour 2017, texte n° 106 (2016-2017) transmis au Sénat le 7 novembre 2016 | 2016-11-07 | 206 |
| senat.pjl16-643 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2016, texte n° 643 (2016-2017) transmis au Sénat le 18 juillet 2017 | 2017-07-18 | 1075 |
| senat.pjl17-063 | Projet de loi de financement de la sécurité sociale pour 2018, texte n° 63 (2017-2018) transmis au Sénat le 6 novembre 2017 | 2017-11-06 | 211 |
| senat.pjl17-595 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2017, texte n° 595 (2017-2018) transmis au Sénat le 21 juin 2018 | 2018-06-21 | 1047 |
| senat.pjl18-106 | Projet de loi de financement de la sécurité sociale pour 2019, texte n° 106 (2018-2019) transmis au Sénat le 5 novembre 2018 | 2018-11-05 | 213 |
| senat.pjl18-686 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2018, texte n° 686 (2018-2019) transmis au Sénat le 18 juillet 2019 en nouvelle lecture | 2019-07-18 | 1052 |
| senat.pjl19-098 | Projet de loi de financement de la sécurité sociale pour 2020, texte n° 98 (2019-2020) transmis au Sénat le 4 novembre 2019 | 2019-11-04 | 217 |
| senat.pjl19-505 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2019, texte n° 505 (2019-2020) transmis au Sénat le 11 juin 2020 | 2020-06-11 | 1061 |
| senat.pjl20-101 | Projet de loi de financement de la sécurité sociale pour 2021, texte n° 101 (2020-2021) transmis au Sénat le 2 novembre 2020 | 2020-11-02 | 218 |
| senat.pjl20-784 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2020, texte n° 784 (2020-2021) transmis au Sénat le 21 juillet 2021 en nouvelle lecture | 2021-07-21 | 1061 |
| senat.pjl21-118 | Projet de loi de financement de la sécurité sociale pour 2022, texte n° 118 (2021-2022) transmis au Sénat le 2 novembre 2021 | 2021-11-02 | 221 |
| senat.pjl22-683 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2021, texte n° 683 (2022-2023) transmis au Sénat le 6 juin 2023 | 2023-06-06 | 1090 |
| senat.pjl22-684 | Projet de loi de règlement du budget et d'approbation des comptes de l'année 2022, texte n° 684 (2022-2023) transmis au Sénat le 6 juin 2023 | 2023-06-06 | 1098 |
| senat.pjl22-705 | Projet de loi d'approbation des comptes de la sécurité sociale pour l'année 2022, texte n° 705 (2022-2023) transmis au Sénat le 7 juin 2023 | 2023-06-07 | 215 |
| senat.pjl24-032 | Projet de loi relatif aux résultats de la gestion et portant approbation des comptes de l'année 2023, texte n° 32 (2024-2025) transmis au Sénat le 15 octobre 2024 | 2024-10-15 | 1075 |
| senat.pjl24-035 | Projet de loi d'approbation des comptes de la sécurité sociale de l'année 2023, texte n° 35 (2024-2025) transmis au Sénat le 15 octobre 2024 | 2024-10-15 | 215 |
| senat.pjl24-718 | Projet de loi relatif aux résultats de la gestion et portant approbation des comptes de l'année 2024, texte n° 718 (2024-2025) transmis au Sénat le 10 juin 2025 | 2025-06-10 | 1066 |
| senat.pjl24-729 | Projet de loi d'approbation des comptes de la sécurité sociale de l'année 2024, texte n° 729 (2024-2025) transmis au Sénat le 11 juin 2025 | 2025-06-11 | 214 |
| senat.pjl25-726 | Projet de loi relatif aux résultats de la gestion et portant approbation des comptes de l'année 2025, texte n° 726 (2025-2026) transmis au Sénat le 10 juin 2026 | 2026-06-10 | 1053 |
| senat.pjl25-727 | Projet de loi portant approbation des comptes de la sécurité sociale de l'année 2025, texte n° 727 (2025-2026) transmis au Sénat le 10 juin 2026 | 2026-06-10 | 214 |
| senat.tas05-033 | Projet de loi de financement de la sécurité sociale pour 2006, texte définitif n° 33 (2005-2006) adopté par le Sénat le 23 novembre 2005 | 2005-11-23 | 39 |
| senat.tas22-018 | Projet de loi de financement de la sécurité sociale pour 2023, texte n° 18 (2022-2023) adopté par le Sénat en première lecture le 15 novembre 2022 | 2022-11-15 | 230 |

## 1. Sommes comptables

Un total contre la somme de ses composantes, pour chaque source, périmètre, fonction et année : en montant, ou en % du PIB quand la source y donne aussi ses composantes. Les tableaux des lois d'approbation des comptes changent de lignes d'une année à l'autre, et une case vide y vaut « rien » : une composante qu'ils ne présentent pas une année y compte pour zéro.

33980 sommes vérifiées avec toutes leurs composantes : 33874 justes, 106 en écart.

| Source | Périmètre | Fonction | Année | Total | Total publié | Somme des composantes | Écart |
|---|---|---|---|---|---|---|---|
| dgcl.finances-departements | DEPARTEMENTS_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 59,5032 Md€ | 60,2187 Md€ | −715,5 M€ |
| dgcl.finances-departements | DEPARTEMENTS_BP | ensemble | 2022 | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 71,4088 Md€ | 71,4338 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEPARTEMENTS_CTU_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 70,7601 Md€ | 71,4756 Md€ | −715,5 M€ |
| dgcl.finances-departements | DEPARTEMENTS_CTU_BP | ensemble | 2022 | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 83,9477 Md€ | 83,9727 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEPARTEMENTS_METROPOLE_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 57,5987 Md€ | 58,3032 Md€ | −704,5 M€ |
| dgcl.finances-departements | DEPARTEMENTS_METROPOLE_BP | ensemble | 2022 | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 69,2457 Md€ | 69,2707 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEPARTEMENTS_OUTRE_MER_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,9046 Md€ | 1,9156 Md€ | −11,0 M€ |
| dgcl.finances-departements | DEP_06_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,0877 Md€ | 1,1377 Md€ | −50,0 M€ |
| dgcl.finances-departements | DEP_07_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,3222 Md€ | 0,3322 Md€ | −10,0 M€ |
| dgcl.finances-departements | DEP_10_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,3031 Md€ | 0,3081 Md€ | −5,0 M€ |
| dgcl.finances-departements | DEP_12_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,3168 Md€ | 0,3258 Md€ | −9,0 M€ |
| dgcl.finances-departements | DEP_14_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,6131 Md€ | 0,6581 Md€ | −45,0 M€ |
| dgcl.finances-departements | DEP_15_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,1870 Md€ | 0,1920 Md€ | −5,0 M€ |
| dgcl.finances-departements | DEP_16_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,3785 Md€ | 0,3865 Md€ | −8,0 M€ |
| dgcl.finances-departements | DEP_17_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,6549 Md€ | 0,6689 Md€ | −14,0 M€ |
| dgcl.finances-departements | DEP_19_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,2399 Md€ | 0,2649 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEP_19_BP | ensemble | 2022 | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 0,3328 Md€ | 0,3578 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEP_22_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,5612 Md€ | 0,5712 Md€ | −10,0 M€ |
| dgcl.finances-departements | DEP_25_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,4913 Md€ | 0,4983 Md€ | −7,0 M€ |
| dgcl.finances-departements | DEP_26_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,5211 Md€ | 0,5401 Md€ | −19,0 M€ |
| dgcl.finances-departements | DEP_29_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,8043 Md€ | 0,8483 Md€ | −44,0 M€ |
| dgcl.finances-departements | DEP_31_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,4214 Md€ | 1,4714 Md€ | −50,0 M€ |
| dgcl.finances-departements | DEP_32_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,2410 Md€ | 0,2490 Md€ | −8,0 M€ |
| dgcl.finances-departements | DEP_33_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,5991 Md€ | 1,6091 Md€ | −10,0 M€ |
| dgcl.finances-departements | DEP_34_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,2624 Md€ | 1,2884 Md€ | −26,0 M€ |
| dgcl.finances-departements | DEP_36_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,2017 Md€ | 0,2067 Md€ | −5,0 M€ |
| dgcl.finances-departements | DEP_37_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,5238 Md€ | 0,5488 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEP_42_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,7026 Md€ | 0,7176 Md€ | −15,0 M€ |
| dgcl.finances-departements | DEP_53_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,2810 Md€ | 0,2947 Md€ | −13,7 M€ |
| dgcl.finances-departements | DEP_54_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,6883 Md€ | 0,7101 Md€ | −21,8 M€ |
| dgcl.finances-departements | DEP_57_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,7677 Md€ | 0,7927 Md€ | −25,0 M€ |
| dgcl.finances-departements | DEP_60_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,6784 Md€ | 0,7084 Md€ | −30,0 M€ |
| dgcl.finances-departements | DEP_62_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,5449 Md€ | 1,5867 Md€ | −41,8 M€ |
| dgcl.finances-departements | DEP_63_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,5936 Md€ | 0,6036 Md€ | −10,0 M€ |
| dgcl.finances-departements | DEP_69_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,4004 Md€ | 0,4174 Md€ | −17,0 M€ |
| dgcl.finances-departements | DEP_71_BP | ensemble | 2022 | COMPTES_LOCAUX.EPARGNE_NETTE | 0,0521 Md€ | 0,0579 Md€ | −5,8 M€ |
| dgcl.finances-departements | DEP_71_BP | ensemble | 2022 | COMPTES_LOCAUX.ANNUITE_DETTE | 0,0472 Md€ | 0,0413 Md€ | +5,8 M€ |
| dgcl.finances-departements | DEP_73_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,4248 Md€ | 0,4540 Md€ | −29,2 M€ |
| dgcl.finances-departements | DEP_74_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,6769 Md€ | 0,7269 Md€ | −50,0 M€ |
| dgcl.finances-departements | DEP_83_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 1,0331 Md€ | 1,0631 Md€ | −30,0 M€ |
| dgcl.finances-departements | DEP_84_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,5443 Md€ | 0,5743 Md€ | −30,0 M€ |
| dgcl.finances-departements | DEP_86_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,3899 Md€ | 0,4059 Md€ | −16,0 M€ |
| dgcl.finances-departements | DEP_974_BP | ensemble | 2022 | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 0,9592 Md€ | 0,9702 Md€ | −11,0 M€ |
| insee.bdm-comptes-etat | ETAT_LF | ensemble | 2019-04 | LOLF.RESULTAT_EXECUTION | −67,2150 Md€ | −65,5960 Md€ | −1 619,0 M€ |
| insee.t3104 | S13 | ensemble | 2013 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 155,6000 Md€ | 155,3000 Md€ | +300,0 M€ |
| insee.t3104 | S13 | ensemble | 2015 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 278,7000 Md€ | 277,9000 Md€ | +800,0 M€ |
| insee.t3104 | S13 | ensemble | 2016 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 320,4000 Md€ | 319,3000 Md€ | +1 100,0 M€ |
| insee.t3104 | S13 | ensemble | 2017 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 286,0000 Md€ | 284,8000 Md€ | +1 200,0 M€ |
| insee.t3104 | S13 | ensemble | 2018 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 268,7000 Md€ | 267,2000 Md€ | +1 500,0 M€ |
| insee.t3104 | S13 | ensemble | 2019 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 344,1000 Md€ | 342,3000 Md€ | +1 800,0 M€ |
| insee.t3104 | S13 | ensemble | 2020 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 413,5000 Md€ | 410,8000 Md€ | +2 700,0 M€ |
| insee.t3104 | S13 | ensemble | 2021 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 329,1000 Md€ | 326,3000 Md€ | +2 800,0 M€ |
| insee.t3104 | S1311 | ensemble | 2013 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 145,7000 Md€ | 145,4000 Md€ | +300,0 M€ |
| insee.t3104 | S1311 | ensemble | 2014 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 264,6000 Md€ | 264,1000 Md€ | +500,0 M€ |
| insee.t3104 | S1311 | ensemble | 2015 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 253,9000 Md€ | 253,1000 Md€ | +800,0 M€ |
| insee.t3104 | S1311 | ensemble | 2016 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 293,7000 Md€ | 292,6000 Md€ | +1 100,0 M€ |
| insee.t3104 | S1311 | ensemble | 2017 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 269,4000 Md€ | 268,2000 Md€ | +1 200,0 M€ |
| insee.t3104 | S1311 | ensemble | 2018 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 253,1000 Md€ | 251,7000 Md€ | +1 400,0 M€ |
| insee.t3104 | S1311 | ensemble | 2019 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 326,3000 Md€ | 324,5000 Md€ | +1 800,0 M€ |
| insee.t3104 | S1311 | ensemble | 2020 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 404,5000 Md€ | 401,8000 Md€ | +2 700,0 M€ |
| insee.t3104 | S1311 | ensemble | 2021 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 314,8000 Md€ | 311,9000 Md€ | +2 900,0 M€ |
| insee.t3104 | S13111 | ensemble | 2014 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 262,3000 Md€ | 261,8000 Md€ | +500,0 M€ |
| insee.t3104 | S13111 | ensemble | 2015 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 251,6000 Md€ | 250,8000 Md€ | +800,0 M€ |
| insee.t3104 | S13111 | ensemble | 2016 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 291,6000 Md€ | 290,6000 Md€ | +1 000,0 M€ |
| insee.t3104 | S13111 | ensemble | 2017 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 268,7000 Md€ | 267,4000 Md€ | +1 300,0 M€ |
| insee.t3104 | S13111 | ensemble | 2018 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 252,2000 Md€ | 250,7000 Md€ | +1 500,0 M€ |
| insee.t3104 | S13111 | ensemble | 2019 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 324,9000 Md€ | 323,2000 Md€ | +1 700,0 M€ |
| insee.t3104 | S13111 | ensemble | 2020 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 403,4000 Md€ | 401,1000 Md€ | +2 300,0 M€ |
| insee.t3104 | S13111 | ensemble | 2021 | INSEE_DETTE.PASSAGE_VALEUR_NOMINALE | 313,2000 Md€ | 310,7000 Md€ | +2 500,0 M€ |
| insee.t3207 | S131311 | ensemble | 2019 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 36,3688 Md€ | 36,2870 Md€ | +81,8 M€ |
| insee.t3207 | S131311 | ensemble | 2020 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 31,1743 Md€ | 31,0840 Md€ | +90,3 M€ |
| insee.t3207 | S131311 | ensemble | 2021 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 32,5278 Md€ | 32,4602 Md€ | +67,6 M€ |
| insee.t3207 | S131311 | ensemble | 2024 | SEC2010.B9 | −2,8229 Md€ | −2,8219 Md€ | −1,0 M€ |
| insee.t3208 | S131312 | ensemble | 2019 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 6,8290 Md€ | 6,8270 Md€ | +2,0 M€ |
| insee.t3208 | S131312 | ensemble | 2020 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 6,9480 Md€ | 6,9460 Md€ | +2,0 M€ |
| insee.t3208 | S131312 | ensemble | 2024 | SEC2010.B9 | −5,6560 Md€ | −5,8130 Md€ | +157,0 M€ |
| insee.t3210 | S131314 | ensemble | 2021 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 5,0710 Md€ | 5,0550 Md€ | +16,0 M€ |
| insee.t3217 | S13_S212 | ensemble | 2018 | INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_IMPUTES | −16,8840 Md€ | −16,3100 Md€ | −574,0 M€ |
| insee.t3217 | S13_S212 | ensemble | 2019 | INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_IMPUTES | −17,7060 Md€ | −17,1280 Md€ | −578,0 M€ |
| insee.t7301 | S13 | ensemble | 1959 | SEC2010.P1 | 7,3680 Md€ | 1,4840 Md€ | +5 884,0 M€ |
| insee.t7301 | S13 | ensemble | 1960 | SEC2010.P1 | 7,8240 Md€ | 1,5860 Md€ | +6 238,0 M€ |
| insee.t7301 | S13 | ensemble | 1961 | SEC2010.P1 | 8,6700 Md€ | 1,7810 Md€ | +6 889,0 M€ |
| insee.t7301 | S13 | ensemble | 1962 | SEC2010.P1 | 9,8840 Md€ | 2,0300 Md€ | +7 854,0 M€ |
| insee.t7301 | S13 | ensemble | 1963 | SEC2010.P1 | 11,3010 Md€ | 2,3170 Md€ | +8 984,0 M€ |
| insee.t7301 | S13 | ensemble | 1964 | SEC2010.P1 | 12,4780 Md€ | 2,5870 Md€ | +9 891,0 M€ |
| insee.t7301 | S13 | ensemble | 1965 | SEC2010.P1 | 13,4450 Md€ | 2,8480 Md€ | +10 597,0 M€ |
| insee.t7301 | S13 | ensemble | 1966 | SEC2010.P1 | 14,5190 Md€ | 3,0810 Md€ | +11 438,0 M€ |
| insee.t7301 | S13 | ensemble | 1967 | SEC2010.P1 | 15,8010 Md€ | 3,3630 Md€ | +12 438,0 M€ |
| insee.t7301 | S13 | ensemble | 1968 | SEC2010.P1 | 18,0130 Md€ | 4,0020 Md€ | +14 011,0 M€ |
| insee.t7301 | S13 | ensemble | 1969 | SEC2010.P1 | 20,3340 Md€ | 4,1350 Md€ | +16 199,0 M€ |
| insee.t7301 | S13 | ensemble | 1970 | SEC2010.P1 | 22,7660 Md€ | 4,4340 Md€ | +18 332,0 M€ |
| insee.t7301 | S13 | ensemble | 1971 | SEC2010.P1 | 26,0300 Md€ | 5,1580 Md€ | +20 872,0 M€ |
| insee.t7301 | S13 | ensemble | 1972 | SEC2010.P1 | 29,1870 Md€ | 5,9020 Md€ | +23 285,0 M€ |
| insee.t7301 | S13 | ensemble | 1973 | SEC2010.P1 | 32,8480 Md€ | 6,2150 Md€ | +26 633,0 M€ |
| insee.t7301 | S13 | ensemble | 1974 | SEC2010.P1 | 39,3290 Md€ | 7,4110 Md€ | +31 918,0 M€ |
| insee.t7301 | S13 | ensemble | 1975 | SEC2010.P1 | 48,1020 Md€ | 9,0730 Md€ | +39 029,0 M€ |
| insee.t7301 | S13 | ensemble | 1976 | SEC2010.P1 | 56,6210 Md€ | 10,5060 Md€ | +46 115,0 M€ |
| insee.t7301 | S13 | ensemble | 1977 | SEC2010.P1 | 64,4780 Md€ | 11,4500 Md€ | +53 028,0 M€ |
| senat.pjl13-759 | ETAT_LF | ensemble | 2013 | LOLF.COMPTES_COMMERCE_SOLDE | 0,1368 Md€ | 0,2654 Md€ | −128,6 M€ |
| senat.pjl15-128 | SECU_LFSS | ensemble | 2014 | COMPTES_SECU.ACTIF_CIRCULANT | 69,7000 Md€ | 69,3000 Md€ | +400,0 M€ |
| senat.pjl15-128 | SECU_LFSS | ensemble | 2014 | COMPTES_SECU.PASSIF_FINANCIER | 179,9000 Md€ | 177,0000 Md€ | +2 900,0 M€ |
| senat.pjl19-505 | ETAT_LF | ensemble | 2019 | LOLF.CS_ENSEMBLE_SOLDES_CREDITEURS | 23,3199 Md€ | 24,5853 Md€ | −1 265,4 M€ |
| senat.pjl25-726 | ETAT_CGE | ensemble | 2025 | COMPTES_ETAT.SITUATION_NETTE | −2 115,8890 Md€ | −1 986,4230 Md€ | −129 466,0 M€ |
| senat.pjl25-726 | ETAT_LF | ensemble | 2025 | LOLF.CS_ENSEMBLE_SOLDES_CREDITEURS | 16,0862 Md€ | 16,0902 Md€ | −4,0 M€ |
| senat.tas22-018 | REGIME_GENERAL_HORS_FSV | ensemble | 2021 | COMPTES_SECU.RESULTAT_COMPTABLE | −27,7000 Md€ | −22,8000 Md€ | −4 900,0 M€ |
| senat.tas22-018 | REGIME_GENERAL_HORS_FSV | COMPTES_SECU.MALADIE | 2021 | COMPTES_SECU.RESULTAT_COMPTABLE | −28,7000 Md€ | −29,7000 Md€ | +1 000,0 M€ |

11343 sommes ont des parties que la source ne diffuse pas (cellule vide ou marquée non disponible). Pour 11303 d'entre elles, les parties diffusées suffisent à retrouver le total à l'arrondi près : les parties absentes y sont nulles ou négligeables. Pour les 40 autres, elles ne suffisent pas : des parties absentes ne sont pas nulles.

| Source | Périmètre | Total | Fonction | Années | Plus grand reste (total − parties diffusées) |
|---|---|---|---|---|---|
| insee.t3107 | S13111 | INSEE_PASSAGES.ETAT_DROITS_CONSTATES | ensemble | 2023 | −1 300,0 M€ en 2023 |
| insee.t3107 | S13111 | INSEE_PASSAGES.ETAT_NON_BUDGETAIRES | ensemble | 2019, 2020, 2021 et 2024 | −2 600,0 M€ en 2021 |
| insee.t7301 | S13 | SEC2010.D39PAY_EN_RESSOURCES | ensemble | 35 années entre 1978 et 2012 | −20 309,0 M€ en 2012 |

## 2. Ventilations par fonction

Pour une même grandeur, l'ensemble des fonctions contre la somme des divisions de la COFOG, des missions du budget général de l'État ou de ses comptes (budgets annexes, comptes spéciaux), ou des branches de la sécurité sociale, chaque division contre la somme de ses groupes, chaque mission ou compte contre celle de ses programmes. Pour les branches, seul le solde s'additionne : les recettes et les dépenses de l'ensemble des branches excluent les transferts entre elles, que comptent celles de chaque branche.

19649 ventilations vérifiées avec toutes leurs parties : 19647 justes, 2 en écart.

| Source | Périmètre | Grandeur | Fonction | Années en écart | Plus grand écart (total − somme) |
|---|---|---|---|---|---|
| senat.pjl16-643 | ETAT_LF | LOLF.BA_DEPENSES | ensemble | 2016 | +0,6 M€ en 2016 |
| senat.pjl16-643 | ETAT_LF | LOLF.BA_RECETTES | ensemble | 2016 | +0,6 M€ en 2016 |

834 ventilations ont des parties que la source ne diffuse pas (cellule vide ou marquée non disponible). Pour toutes, les parties diffusées suffisent à retrouver le total à l'arrondi près : les parties absentes y sont nulles ou négligeables.

## 3. Additivité des sous-secteurs

Le solde d'un ensemble, ses prélèvements obligatoires, ou sa dépense consolidée au niveau de l'ensemble des administrations publiques (tableau 3.307 de l'Insee), contre la somme de ceux de ses parties ; de même sa dette au sens de Maastricht, ses instruments et sa dette nette, celles d'un sous-secteur étant sa contribution à la dette consolidée de l'ensemble (tableaux 3.101 à 3.104 et dette trimestrielle), et chaque montant de ses comptes complets, qui ne sont pas consolidés (tableaux 7.301 à 7.306) ; pour la sécurité sociale, le résultat du régime général et celui des régimes de base, Fonds de solidarité vieillesse compris, contre la somme des leurs et de celui du FSV, et chaque poste de la situation patrimoniale (annexe A des lois de financement) contre la somme de ses lignes par entité ; pour les collectivités locales, dont la source ne consolide pas les montants entre niveaux, chaque montant d'un niveau contre la somme de ceux des niveaux qui le composent, et celui des groupements à fiscalité propre contre la somme de leurs types (annexes 2A et 2B des rapports de l'OFGL, budgets principaux et budgets annexes), le nombre de budgets de l'ensemble des collectivités contre la somme de ceux de ses niveaux, chaque total des publications de la DGCL contre la somme de ses départements ou de ses régions ; pour les décomptes d'organismes et de collectivités, chaque catégorie contre la somme de ses sous-catégories (organismes divers d'administration locale de l'Insee, collectivités et groupements de la DGCL).

17411 additions vérifiées : 17340 justes, 71 en écart.

| Tableaux | Grandeur | Ensemble | Parties | Fonctions | Années en écart | Plus grand écart |
|---|---|---|---|---|---|---|
| dgcl.finances-departements | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | DEPARTEMENTS_METROPOLE_BP | ses 92 parties (CEA_BP … DEP_95_BP) | ensemble | 2022 | +5,8 M€ en 2022 |
| eurostat.gov_10a_main | SEC2010.B9 | S13 | S1311 + S1313 + S1314 | ensemble | 2011 | −0,4 M€ en 2011 |
| insee.t3101 | PDE.GD | S13 | S1311 + S1313 + S1314 | ensemble | 13 années entre 1996 et 2012 | −1,5 M€ en 2010 |
| insee.t3101 | PDE.GD | S1311 | S13111 + S13112 | ensemble | 14 années entre 1996 et 2012 | +1,8 M€ en 2002 |
| insee.t3104 | PDE.GD | S13 | S1311 + S1313 + S1314 | ensemble | 2025 | −400,0 M€ en 2025 |
| insee.t3106 | SEC2010.B9 | S1311 | S13111 + S13112 | ensemble | 19 années entre 1959 et 1977 | +6 502,0 M€ en 1974 |
| insee.t3212, insee.t3213, insee.t3214 | SEC2010.B9 | S1314 | S13141 + S13142 | ensemble | 2019 | +8,0 M€ en 2019 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEPENSES_INTERVENTION | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEPENSES_INTERVENTION | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEP_TOTALES | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEP_TOTALES | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.IMPOTS_LOCAUX | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.IMPOTS_LOCAUX | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.IMPOTS_TAXES | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.IMPOTS_TAXES | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.REC_FONCTIONNEMENT | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.REC_FONCTIONNEMENT | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.REC_TOTALES | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.REC_TOTALES | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | COLLECTIVITES_TERRITORIALES_GFP_BP | SECTEUR_COMMUNAL_BP + DEPARTEMENTS_BP + REGIONS_CTU_BP | ensemble | 2025 | −47,4 M€ en 2025 |
| ofgl.annexe-2a | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | SECTEUR_COMMUNAL_BP | COMMUNES_BP + GFP_BP | ensemble | 2025 | +47,4 M€ en 2025 |
| senat.pjl13-117 | COMPTES_SECU.REPORT_A_NOUVEAU | SECU_LFSS | REGIME_GENERAL_HORS_FSV + AUTRES_REGIMES_BASE + CADES | ensemble | 2011 | +9 800,0 M€ en 2011 |
| senat.pjl17-063 | COMPTES_SECU.ENCOURS_BANCAIRE | SECU_LFSS | REGIME_GENERAL_HORS_FSV + AUTRES_REGIMES_BASE + FSV + CADES + FRR | ensemble | 2015 | +900,0 M€ en 2015 |
| senat.tas22-018 | COMPTES_SECU.RESULTAT_COMPTABLE | REGIME_GENERAL | REGIME_GENERAL_HORS_FSV + FSV | ensemble | 2021 | −200,0 M€ en 2021 |

## 4. Passerelles entre tableaux

Des tableaux différents présentent autrement les mêmes grandeurs. Chaque passerelle vérifie qu'ils concordent, à l'arrondi près, pour chaque année où figurent tous ses termes. Pour les collectivités locales, la consolidation des budgets principaux et annexes retire chaque flux croisé des recettes comme des dépenses de la même section : la variation du fonds de roulement, l'épargne brute, la dette et la trésorerie d'un ensemble consolidé égalent la somme de celles de ses parties. La dette à la fin du quatrième trimestre est celle de la fin de l'année.

| Passerelle | Années vérifiées | Années en écart | dont hors chiffres révisables | Plus grand écart (gauche − droite) |
|---|---|---|---|---|
| Cotisations sociales : tableau 3.217 contre tableau 3.201 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Cotisations sociales imputées : tableau 3.217 contre tableau 3.201 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Impôts et cotisations dus non recouvrables : tableau 3.217 contre tableau 3.201 | 31 années entre 1995 et 2025 | 2022 | 2022 | +2,0 M€ en 2022 |
| Impôts en capital : tableau 3.217 contre tableau 3.201 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Impôts courants sur le revenu et le patrimoine : D.51 + D.59 du tableau 3.217 contre D.5 du tableau 3.201 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Impôts sur la production et les importations reçus par les administrations publiques : D.211 + D.212 + D.214 + D.291 + D.292 du tableau 3.217, moins les impôts de l'Union européenne du tableau 3.216, contre D.2 du tableau 3.201 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Même passerelle, avec les impôts de l'Union européenne du tableau 3.217 | 31 années entre 1995 et 2025 | 23 années entre 1995 et 2018 | 23 années entre 1995 et 2018 | +734,9 M€ en 1995 |
| Crédits d'impôt retranchés des prélèvements obligatoires (3.217) contre crédits d'impôt enregistrés en recettes (3.201), de signe opposé | 31 années entre 1995 et 2025 | 2017, 2018 et 2021 | 2017, 2018 et 2021 | −85,0 M€ en 2017 |
| Prélèvements obligatoires des administrations publiques : impôts nationaux du tableau 3.217 contre somme des sous-secteurs du tableau 3.216 | 31 années entre 1995 et 2025 | 24 années entre 1995 et 2018 | 24 années entre 1995 et 2018 | +734,9 M€ en 1995 |
| Solde général d'exécution à fin décembre (situation mensuelle) contre soldes du budget général et des comptes spéciaux du projet de loi d'approbation des comptes | 17 années entre 2009 et 2025 | 2016, 2017, 2018 et 2019 | 2016, 2017, 2018 et 2019 | +76,9 M€ en 2016 |
| Solde des comptes spéciaux à fin décembre (situation mensuelle) contre projet de loi d'approbation des comptes | 17 années entre 2009 et 2025 | 2016, 2017, 2018 et 2019 | 2016, 2017, 2018 et 2019 | +33,9 M€ en 2017 |
| Dépenses du budget général à fin décembre (situation mensuelle) contre dépenses nettes plus prélèvements sur recettes du projet de loi d'approbation des comptes | 17 années entre 2009 et 2025 | aucune | aucune | aucun |
| Recettes du budget général à fin décembre (situation mensuelle) contre recettes nettes plus prélèvements sur recettes du projet de loi d'approbation des comptes | 17 années entre 2009 et 2025 | 2010, 2016, 2017 et 2018 | 2010, 2016, 2017 et 2018 | +52,1 M€ en 2016 |
| Solde général d'exécution à fin décembre (situation mensuelle) contre résultat d'exécution des lois de finances du tableau 3.107 | 17 années entre 2009 et 2025 | 2014, 2016 et 2019 | 2014, 2016 et 2019 | +121,0 M€ en 2016 |
| Solde du budget général à fin décembre (situation mensuelle : recettes moins dépenses) contre tableau 3.107 | 17 années entre 2009 et 2025 | 2016 | 2016 | +101,0 M€ en 2016 |
| Solde des comptes spéciaux à fin décembre (situation mensuelle) contre tableau 3.107 | 17 années entre 2009 et 2025 | 2017 | 2017 | +64,0 M€ en 2017 |
| Déficit à financer du tableau de financement contre résultat budgétaire de l'État, de signe opposé, dans le projet de loi d'approbation des comptes | 12 années entre 2014 et 2025 | 2014 | 2014 | −11 955,0 M€ en 2014 |
| Résultat comptable du régime général, Fonds de solidarité vieillesse compris (tableau 3.108), contre soldes du régime général et du FSV approuvés par la loi de financement de la sécurité sociale | 13 années entre 2009 et 2021 | 2021 | 2021 | +4 800,0 M€ en 2021 |
| Dette amortie par la CADES, qu'approuve la loi de financement de la sécurité sociale, contre son résultat de l'exercice dans la situation patrimoniale (annexe A) | 16 années entre 2010 et 2025 | aucune | aucune | aucun |
| Déficit de l'État au sens de Maastricht contre résultat d'exécution des lois de finances plus corrections (1), (2) et (3), dans le tableau 3.107 | 17 années entre 2009 et 2025 | aucune | aucune | aucun |
| Déficit des administrations publiques du tableau 3.105 contre leur capacité de financement au sens de Maastricht (tableau 3.106), de signe opposé | 17 années entre 2009 et 2025 | aucune | aucune | aucun |
| Variation de la dette au sens de Maastricht (tableau 3.105) contre l'écart entre la dette de fin d'année et celle de l'année précédente (tableau 3.101) | 17 années entre 2009 et 2025 | 2011, 2014 et 2015 | 2011, 2014 et 2015 | +633,7 M€ en 2014 |
| Dette au sens de Maastricht des administrations publiques, au quatrième trimestre (série trimestrielle), contre la dette de fin d'année du tableau 3.101 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht de l'État, au quatrième trimestre (série trimestrielle), contre la dette de fin d'année du tableau 3.101 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des organismes divers d'administration centrale, au quatrième trimestre (série trimestrielle), contre la dette de fin d'année du tableau 3.101 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques locales, au quatrième trimestre (série trimestrielle), contre la dette de fin d'année du tableau 3.101 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations de sécurité sociale, au quatrième trimestre (série trimestrielle), contre la dette de fin d'année du tableau 3.101 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques, dépôts, au quatrième trimestre (série trimestrielle), contre le tableau 3.102 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques, titres de créance, au quatrième trimestre (série trimestrielle), contre le tableau 3.102 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques, titres de créance à court terme, au quatrième trimestre (série trimestrielle), contre le tableau 3.102 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques, titres de créance à long terme, au quatrième trimestre (série trimestrielle), contre le tableau 3.102 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques, crédits à court terme, au quatrième trimestre (série trimestrielle), contre le tableau 3.102 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette au sens de Maastricht des administrations publiques, crédits à long terme, au quatrième trimestre (série trimestrielle), contre le tableau 3.102 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Dette nette des administrations publiques, au quatrième trimestre (série trimestrielle), contre le tableau 3.103 | 31 années entre 1995 et 2025 | aucune | aucune | aucun |
| Actions cotées et parts de fonds d'investissement détenues par les administrations publiques, au quatrième trimestre (série trimestrielle), contre le tableau 3.103 | 31 années entre 1995 et 2025 | 15 années entre 2001 et 2015 | 15 années entre 2001 et 2015 | −5 300,0 M€ en 2015 |
| Collectivités locales, variation du fonds de roulement : communes, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2018 et 2023 | 2018 et 2023 | −0,2 M€ en 2023 |
| Collectivités locales, variation du fonds de roulement : groupements à fiscalité propre, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2018 et 2023 | 2018 et 2023 | −0,6 M€ en 2018 |
| Collectivités locales, variation du fonds de roulement : départements, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, variation du fonds de roulement : régions et CTU, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, variation du fonds de roulement : syndicats, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2018 | 2018 | +0,5 M€ en 2018 |
| Collectivités locales, variation du fonds de roulement : bloc communal consolidé (annexe 2D) contre communes plus groupements à fiscalité propre consolidés (2C) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, variation du fonds de roulement : ensemble des collectivités consolidé (annexe 2D) contre ses cinq niveaux consolidés (2C) | 9 années entre 2017 et 2025 | 7 années entre 2017 et 2023 | 7 années entre 2017 et 2023 | +30,2 M€ en 2022 |
| Collectivités locales, épargne brute : communes, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2018 et 2023 | 2018 et 2023 | −0,1 M€ en 2023 |
| Collectivités locales, épargne brute : groupements à fiscalité propre, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2018 et 2023 | 2018 et 2023 | +0,1 M€ en 2023 |
| Collectivités locales, épargne brute : départements, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, épargne brute : régions et CTU, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, épargne brute : syndicats, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2018 | 2018 | +16 440 € en 2018 |
| Collectivités locales, épargne brute : bloc communal consolidé (annexe 2D) contre communes plus groupements à fiscalité propre consolidés (2C) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, épargne brute : ensemble des collectivités consolidé (annexe 2D) contre ses cinq niveaux consolidés (2C) | 9 années entre 2017 et 2025 | 7 années entre 2017 et 2023 | 7 années entre 2017 et 2023 | +30,2 M€ en 2022 |
| Collectivités locales, dette au 31 décembre : communes, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2023 | 2023 | −0,1 M€ en 2023 |
| Collectivités locales, dette au 31 décembre : groupements à fiscalité propre, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | 2023 | 2023 | +0,1 M€ en 2023 |
| Collectivités locales, dette au 31 décembre : départements, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, dette au 31 décembre : régions et CTU, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, dette au 31 décembre : syndicats, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, dette au 31 décembre : bloc communal consolidé (annexe 2D) contre communes plus groupements à fiscalité propre consolidés (2C) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, dette au 31 décembre : ensemble des collectivités consolidé (annexe 2D) contre ses cinq niveaux consolidés (2C) | 9 années entre 2017 et 2025 | aucune | aucune | aucun |
| Collectivités locales, trésorerie nette au 31 décembre : communes, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 2022, 2023, 2024 et 2025 | 2023 | 2023 | −0,1 M€ en 2023 |
| Collectivités locales, trésorerie nette au 31 décembre : groupements à fiscalité propre, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 2022, 2023, 2024 et 2025 | 2023 | 2023 | +0,1 M€ en 2023 |
| Collectivités locales, trésorerie nette au 31 décembre : départements, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 2022, 2023, 2024 et 2025 | aucune | aucune | aucun |
| Collectivités locales, trésorerie nette au 31 décembre : régions et CTU, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 2022, 2023, 2024 et 2025 | aucune | aucune | aucun |
| Collectivités locales, trésorerie nette au 31 décembre : syndicats, budgets principaux et annexes consolidés (annexe 2C de l'OFGL) contre budgets principaux (2A) plus budgets annexes (2B) | 2022, 2023, 2024 et 2025 | aucune | aucune | aucun |
| Collectivités locales, trésorerie nette au 31 décembre : bloc communal consolidé (annexe 2D) contre communes plus groupements à fiscalité propre consolidés (2C) | 2022, 2023, 2024 et 2025 | aucune | aucune | aucun |
| Collectivités locales, trésorerie nette au 31 décembre : ensemble des collectivités consolidé (annexe 2D) contre ses cinq niveaux consolidés (2C) | 2022, 2023, 2024 et 2025 | aucune | aucune | aucun |

Les comptes complets des tableaux 7.301 à 7.306 et les dépenses et recettes des tableaux 3.201 à 3.214 présentent les mêmes opérations, sous-secteur par sous-secteur. Les premiers ne sont pas consolidés ; les seconds consolident les revenus de la propriété et les transferts entre administrations, qui ne se comparent donc pas. Les autres opérations doivent être égales ; les subventions, que les comptes complets inscrivent avec un signe négatif, de signe opposé. L'épargne brute et la capacité de financement, que la consolidation ne change pas, se comparent à la section 6.

| Comptes complets | Dépenses et recettes | Comparaisons | En écart | dont hors chiffres révisables | Plus grand écart (comptes complets − dépenses et recettes) |
|---|---|---|---|---|---|
| SEC2010.P11 | SEC2010.P11 | 307 | 19 | 19 | −14,0 M€ (S13, 1971) |
| SEC2010.P12 | SEC2010.P12 | 307 | 0 | 0 | aucun |
| SEC2010.P2 | SEC2010.P2 | 307 | 0 | 0 | aucun |
| SEC2010.D1PAY | SEC2010.D1PAY | 307 | 0 | 0 | aucun |
| SEC2010.D122PAY | SEC2010.D122PAY | 307 | 0 | 0 | aucun |
| SEC2010.D29PAY | SEC2010.D29PAY | 307 | 0 | 0 | aucun |
| SEC2010.D39REC_EN_EMPLOIS | −SEC2010.D39REC | 257 | 0 | 0 | aucun |
| SEC2010.D2REC | SEC2010.D2REC | 307 | 0 | 0 | aucun |
| SEC2010.D3PAY_EN_RESSOURCES | −SEC2010.D3PAY | 307 | 0 | 0 | aucun |
| SEC2010.D5REC | SEC2010.D5REC | 307 | 0 | 0 | aucun |
| SEC2010.D5PAY | SEC2010.D5PAY | 259 | 0 | 0 | aucun |
| SEC2010.D61REC | SEC2010.D61REC | 307 | 0 | 0 | aucun |
| SEC2010.D612REC | SEC2010.D612REC | 307 | 0 | 0 | aucun |
| SEC2010.D62PAY | SEC2010.D62PAY | 307 | 0 | 0 | aucun |
| SEC2010.D632PAY | SEC2010.D632PAY | 307 | 17 | 17 | −14,1 M€ (S13, 1971) |
| SEC2010.D91REC | SEC2010.D91REC | 186 | 0 | 0 | aucun |
| SEC2010.P51G | SEC2010.P51G | 307 | 0 | 0 | aucun |

## 5. Ratios

Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.

La dette trimestrielle en % du PIB rapporte l'encours, à la fin du quatrième trimestre, au PIB de l'année, et les autres trimestres au cumul du PIB trimestriel, corrigé des variations saisonnières et des jours ouvrables, des quatre derniers trimestres, que la base n'enregistre pas : ces 92 ratios-là ne sont pas recalculés.

| Dénominateur | Ratios | Retrouvés | Non retrouvés |
|---|---|---|---|
| le PIB indiqué par la source, dans le même tableau | 730 | 597 | 133 |
| la dépense totale du même périmètre, chez la même source | 300 | 300 | 0 |
| non indiqué par la source : chaque série de PIB enregistrée pour l'année est essayée | 2197 | 2185 | 12 |

Ratios non retrouvés :

- **eurostat.gov_10a_exp, SEC2010.TE, S13, en % du PIB** : 5 ratios (ensemble des fonctions et 2 fonctions COFOG) ne sont retrouvés avec aucune des séries de PIB enregistrées, pour 2023 et 2024.
  En 2023, aucune série enregistrée ne les retrouve ; il faudrait un PIB compris entre 2 822,462 et 2 827,428 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 833,826 Md€ ; insee.t3101 2 833,826 Md€ ; insee.t3106 2 833,826 Md€).
  En 2024, aucune série enregistrée ne les retrouve ; il faudrait un PIB compris entre 2 918,015 et 2 920,164 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 935,236 Md€ ; insee.t3101 2 935,236 Md€ ; insee.t3106 2 935,236 Md€).
- **insee.t3101, PDE.GD, S13, en % du PIB** : 38 ratios ne sont pas retrouvés avec le PIB indiqué, celui de insee.t3101, pour 38 années entre 1978 et 2019.
  Avec le PIB de eurostat.nama_10_gdp, 37 sont retrouvés.
  Avec le PIB de insee.t3106, 37 sont retrouvés.
  En 2016, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 229,541 et 2 231,814 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 231,819 Md€ ; insee.t3101 2 234,129 Md€ ; insee.t3106 2 231,819 Md€).
- **insee.t3101, PDE.GD, S1311, en % du PIB** : 36 ratios ne sont pas retrouvés avec le PIB indiqué, celui de insee.t3101, pour 36 années entre 1978 et 2019.
  Avec le PIB de eurostat.nama_10_gdp, 36 sont retrouvés.
  Avec le PIB de insee.t3106, 36 sont retrouvés.
- **insee.t3101, PDE.GD, S13111, en % du PIB** : 37 ratios ne sont pas retrouvés avec le PIB indiqué, celui de insee.t3101, pour 37 années entre 1978 et 2019.
  Avec le PIB de eurostat.nama_10_gdp, 37 sont retrouvés.
  Avec le PIB de insee.t3106, 37 sont retrouvés.
- **insee.t3101, PDE.GD, S13112, en % du PIB** : 3 ratios ne sont pas retrouvés avec le PIB indiqué, celui de insee.t3101, pour 1989, 1992 et 1996.
  Avec le PIB de eurostat.nama_10_gdp, 3 sont retrouvés.
  Avec le PIB de insee.t3106, 3 sont retrouvés.
- **insee.t3101, PDE.GD, S1313, en % du PIB** : 17 ratios ne sont pas retrouvés avec le PIB indiqué, celui de insee.t3101, pour 17 années entre 1978 et 2019.
  Avec le PIB de eurostat.nama_10_gdp, 17 sont retrouvés.
  Avec le PIB de insee.t3106, 17 sont retrouvés.
- **insee.t3101, PDE.GD, S1314, en % du PIB** : 2 ratios ne sont pas retrouvés avec le PIB indiqué, celui de insee.t3101, pour 2007 et 2009.
  Avec le PIB de eurostat.nama_10_gdp, 2 sont retrouvés.
  Avec le PIB de insee.t3106, 2 sont retrouvés.
- **insee.t3215, SEC2010.TE, S13, en % du PIB** : 2 ratios ne sont retrouvés avec aucune des séries de PIB enregistrées, pour 2023 et 2024.
  En 2023, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 833,825 et 2 833,827 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 833,826 Md€ ; insee.t3101 2 833,826 Md€ ; insee.t3106 2 833,826 Md€).
  En 2024, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 935,235 et 2 935,237 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 935,236 Md€ ; insee.t3101 2 935,236 Md€ ; insee.t3106 2 935,236 Md€).
- **insee.t3215, SEC2010.TE, S1314, en % du PIB** : 1 ratio n’est retrouvé avec aucune des séries de PIB enregistrées, pour 2023.
  En 2023, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 833,825 et 2 833,827 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 833,826 Md€ ; insee.t3101 2 833,826 Md€ ; insee.t3106 2 833,826 Md€).
- **insee.t3215, SEC2010.TR, S13, en % du PIB** : 2 ratios ne sont retrouvés avec aucune des séries de PIB enregistrées, pour 2023 et 2024.
  En 2023, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 833,825 et 2 833,827 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 833,826 Md€ ; insee.t3101 2 833,826 Md€ ; insee.t3106 2 833,826 Md€).
  En 2024, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 935,235 et 2 935,237 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 935,236 Md€ ; insee.t3101 2 935,236 Md€ ; insee.t3106 2 935,236 Md€).
- **senat.pjl24-032, SEC2010.TE, S13, en % du PIB** : 1 ratio n’est retrouvé avec aucune des séries de PIB enregistrées, pour 2023.
  En 2023, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 799,118 et 2 805,826 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 833,826 Md€ ; insee.t3101 2 833,826 Md€ ; insee.t3106 2 833,826 Md€).
- **senat.pjl24-718, SEC2010.TE, S13, en % du PIB** : 1 ratio n’est retrouvé avec aucune des séries de PIB enregistrées, pour 2024.
  En 2024, aucune série enregistrée ne le retrouve ; il faudrait un PIB compris entre 2 922,054 et 2 929,016 Md€ (PIB enregistrés : eurostat.nama_10_gdp 2 935,236 Md€ ; insee.t3101 2 935,236 Md€ ; insee.t3106 2 935,236 Md€).

## 6. Écarts entre sources pour une même grandeur

Même concept, même périmètre, même fonction, même consolidation, même année, montants convertis dans la même unité. Les montants d'Eurostat convertis en écus avant 1999 ne sont pas comparés : ce sont les mêmes données que ses montants en euros, converties autrement.

Un chiffre que sa source présente comme provisoire, semi-définitif, estimé ou prévu peut encore être révisé : un écart qui en touche un peut venir d'une révision entre deux versions. Les écarts « hors chiffres révisables » sont ceux où aucune des deux sources ne présente son chiffre ainsi.

| Source A | Source B | Comparaisons | Écarts | dont hors chiffres révisables | Plus grand écart hors chiffres révisables (A − B) | Plus grand écart (A − B) |
|---|---|---|---|---|---|---|
| dgcl.finances-departements | dgcl.finances-regions | 540 | 0 | 0 | aucun | aucun |
| dgcl.finances-departements | ofgl.annexe-2a | 170 | 8 | 8 | +715,5 M€ en 2022 | +715,5 M€ en 2022 |
| dgcl.finances-departements | ofgl.annexe-2b | 10 | 9 | 0 | aucun | −703,9 M€ en 2022 |
| dgcl.finances-regions | ofgl.annexe-2a | 165 | 7 | 7 | +9 933 € en 2023 | +9 933 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2b | 10 | 5 | 0 | aucun | +144,4 M€ en 2024 |
| eurostat.gov_10a_exp | eurostat.gov_10a_main | 60 | 19 | 16 | +3,2 M€ en 2019 | +0,3 point de PIB en 2024 ; −914,4 M€ en 2024 |
| eurostat.gov_10a_exp | insee.t3201 | 30 | 20 | 18 | −42,4 M€ en 2021 | −878,3 M€ en 2023 |
| eurostat.gov_10a_exp | insee.t3215 | 60 | 22 | 18 | +3,2 M€ en 2019 | +0,3 point de PIB en 2024 ; −914,4 M€ en 2024 |
| eurostat.gov_10a_exp | insee.t3301 | 330 | 5 | 5 | +0,9 M€ en 2020 | +0,9 M€ en 2020 |
| eurostat.gov_10a_exp | insee.t3307 | 176 | 100 | 100 | −20 300,8 M€ en 2009 | −20 300,8 M€ en 2009 |
| eurostat.gov_10a_main | insee.t3106 | 248 | 1 | 1 | +0,9 M€ en 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3108 | 17 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t3201 | 124 | 5 | 3 | −43,0 M€ en 2021 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3202 | 124 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t3205 | 124 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t3212 | 124 | 6 | 6 | +39,0 M€ en 2019 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3215 | 372 | 3 | 2 | +0,4 M€ en 2011 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3301 | 30 | 15 | 13 | −3,3 M€ en 2019 | +914,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3302 | 30 | 6 | 4 | −0,6 M€ en 2015 | +954,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3305 | 30 | 4 | 2 | −0,6 M€ en 2002 | +738,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3306 | 30 | 3 | 1 | +0,7 M€ en 2022 | −1 139,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3307 | 16 | 16 | 14 | −20 301,7 M€ en 2009 | −20 301,7 M€ en 2009 |
| eurostat.gov_10a_main | insee.t7301 | 31 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t7302 | 31 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t7305 | 31 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t7306 | 31 | 1 | 1 | +0,9 M€ en 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | senat.pjl12-799 | 1 | 1 | 0 | aucun | −0,4 point de PIB en 2012 |
| eurostat.gov_10a_main | senat.pjl13-759 | 1 | 1 | 0 | aucun | −0,6 point de PIB en 2013 |
| eurostat.gov_10a_main | senat.pjl14-642 | 1 | 1 | 0 | aucun | −0,6 point de PIB en 2014 |
| eurostat.gov_10a_main | senat.pjl15-785 | 1 | 1 | 0 | aucun | −0,3 point de PIB en 2015 |
| eurostat.gov_10a_main | senat.pjl16-643 | 1 | 1 | 0 | aucun | −0,4 point de PIB en 2016 |
| eurostat.gov_10a_main | senat.pjl17-595 | 1 | 1 | 0 | aucun | −0,8 point de PIB en 2017 |
| eurostat.gov_10a_main | senat.pjl18-686 | 1 | 1 | 0 | aucun | +0,2 point de PIB en 2018 |
| eurostat.gov_10a_main | senat.pjl19-505 | 1 | 1 | 0 | aucun | +0,6 point de PIB en 2019 |
| eurostat.gov_10a_main | senat.pjl20-784 | 1 | 1 | 0 | aucun | +0,3 point de PIB en 2020 |
| eurostat.gov_10a_main | senat.pjl22-683 | 1 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl22-684 | 1 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl22-705 | 3 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl24-032 | 1 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl24-035 | 3 | 2 | 0 | aucun | −0,3 point de PIB en 2023 |
| eurostat.gov_10a_main | senat.pjl24-718 | 1 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl24-729 | 3 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl25-726 | 1 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | senat.pjl25-727 | 3 | 0 | 0 | aucun | aucun |
| eurostat.nama_10_gdp | insee.t3101 | 48 | 42 | 42 | −9 571,2 M€ en 1990 | −9 571,2 M€ en 1990 |
| eurostat.nama_10_gdp | insee.t3106 | 51 | 0 | 0 | aucun | aucun |
| insee.t3101 | insee.t3102 | 186 | 0 | 0 | aucun | aucun |
| insee.t3101 | insee.t3104 | 186 | 16 | 15 | +171,0 M€ en 2015 | −500,0 M€ en 2025 |
| insee.t3101 | insee.t3106 | 48 | 42 | 42 | +9 571,2 M€ en 1990 | +9 571,2 M€ en 1990 |
| insee.t3101 | senat.pjl24-032 | 1 | 1 | 0 | aucun | −1,1 point de PIB en 2023 |
| insee.t3101 | senat.pjl24-718 | 1 | 1 | 0 | aucun | −0,4 point de PIB en 2024 |
| insee.t3101 | senat.pjl25-726 | 1 | 0 | 0 | aucun | aucun |
| insee.t3102 | insee.t3104 | 186 | 3 | 2 | +200,0 M€ en 2015 | −500,0 M€ en 2025 |
| insee.t3106 | insee.t3107 | 17 | 1 | 1 | −59,0 M€ en 2016 | −59,0 M€ en 2016 |
| insee.t3106 | insee.t3108 | 17 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3201 | 67 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3202 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3203 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3204 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3205 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3212 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t7301 | 77 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t7302 | 77 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t7303 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t7304 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t7305 | 77 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t7306 | 77 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl12-799 | 1 | 1 | 0 | aucun | −0,4 point de PIB en 2012 |
| insee.t3106 | senat.pjl13-759 | 1 | 1 | 0 | aucun | −0,6 point de PIB en 2013 |
| insee.t3106 | senat.pjl14-642 | 1 | 1 | 0 | aucun | −0,6 point de PIB en 2014 |
| insee.t3106 | senat.pjl15-785 | 1 | 1 | 0 | aucun | −0,3 point de PIB en 2015 |
| insee.t3106 | senat.pjl16-643 | 1 | 1 | 0 | aucun | −0,4 point de PIB en 2016 |
| insee.t3106 | senat.pjl17-595 | 1 | 1 | 0 | aucun | −0,8 point de PIB en 2017 |
| insee.t3106 | senat.pjl18-686 | 1 | 1 | 0 | aucun | +0,2 point de PIB en 2018 |
| insee.t3106 | senat.pjl19-505 | 1 | 1 | 0 | aucun | +0,6 point de PIB en 2019 |
| insee.t3106 | senat.pjl20-784 | 1 | 1 | 0 | aucun | +0,3 point de PIB en 2020 |
| insee.t3106 | senat.pjl22-683 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl22-684 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl22-705 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl24-032 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl24-035 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl24-718 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl24-729 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl25-726 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | senat.pjl25-727 | 1 | 0 | 0 | aucun | aucun |
| insee.t3107 | insee.t3203 | 17 | 1 | 1 | +59,2 M€ en 2016 | +59,2 M€ en 2016 |
| insee.t3107 | insee.t7303 | 17 | 1 | 1 | +59,0 M€ en 2016 | +59,0 M€ en 2016 |
| insee.t3107 | senat.pjl09-585 | 3 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl10-672 | 3 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl11-655 | 3 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl12-799 | 3 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl13-759 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl14-642 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl15-785 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl16-643 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl17-595 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl18-686 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl19-505 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl20-784 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl22-683 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl22-684 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl24-032 | 2 | 0 | 0 | aucun | aucun |
| insee.t3107 | senat.pjl24-718 | 2 | 1 | 0 | aucun | −50,0 M€ en 2024 |
| insee.t3107 | senat.pjl25-726 | 2 | 0 | 0 | aucun | aucun |
| insee.t3108 | insee.t3212 | 17 | 0 | 0 | aucun | aucun |
| insee.t3108 | insee.t3214 | 13 | 6 | 6 | +271,0 M€ en 2018 | +271,0 M€ en 2018 |
| insee.t3108 | insee.t7306 | 17 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl16-106 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl17-063 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl18-106 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl19-098 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl20-101 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl21-118 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.tas22-018 | 1 | 1 | 1 | +5 000,0 M€ en 2021 | +5 000,0 M€ en 2021 |
| insee.t3201 | insee.t3215 | 96 | 3 | 2 | +43,0 M€ en 2021 | −119,0 M€ en 2024 |
| insee.t3201 | insee.t3301 | 240 | 35 | 19 | +43,1 M€ en 2021 | −2 012,0 M€ en 2024 |
| insee.t3201 | insee.t3307 | 16 | 16 | 14 | −20 301,8 M€ en 2009 | −20 301,8 M€ en 2009 |
| insee.t3201 | insee.t7301 | 134 | 1 | 1 | +1,3 M€ en 2022 | +1,3 M€ en 2022 |
| insee.t3202 | insee.t3302 | 240 | 20 | 5 | −0,6 M€ en 2016 | +1 029,5 M€ en 2024 |
| insee.t3202 | insee.t7302 | 96 | 0 | 0 | aucun | aucun |
| insee.t3203 | insee.t3215 | 96 | 0 | 0 | aucun | aucun |
| insee.t3203 | insee.t3303 | 128 | 21 | 6 | −2,0 M€ en 2021 | +698,0 M€ en 2023 |
| insee.t3203 | insee.t7303 | 96 | 0 | 0 | aucun | aucun |
| insee.t3204 | insee.t3215 | 96 | 0 | 0 | aucun | aucun |
| insee.t3204 | insee.t3304 | 128 | 17 | 2 | −2,4 M€ en 2020 | +3 073,7 M€ en 2024 |
| insee.t3204 | insee.t7304 | 96 | 1 | 1 | +1,4 M€ en 2022 | +1,4 M€ en 2022 |
| insee.t3205 | insee.t3215 | 96 | 0 | 0 | aucun | aucun |
| insee.t3205 | insee.t3305 | 240 | 18 | 2 | −0,6 M€ en 2002 | +738,0 M€ en 2024 |
| insee.t3205 | insee.t7305 | 96 | 0 | 0 | aucun | aucun |
| insee.t3212 | insee.t3215 | 96 | 4 | 4 | −39,0 M€ en 2019 | −39,0 M€ en 2019 |
| insee.t3212 | insee.t3306 | 240 | 19 | 5 | −39,4 M€ en 2019 | +1 304,3 M€ en 2024 |
| insee.t3212 | insee.t7306 | 96 | 0 | 0 | aucun | aucun |
| insee.t3215 | insee.t3301 | 30 | 15 | 13 | −3,3 M€ en 2019 | +914,2 M€ en 2024 |
| insee.t3215 | insee.t3303 | 16 | 7 | 5 | −2,0 M€ en 2021 | +698,0 M€ en 2023 |
| insee.t3215 | insee.t3304 | 16 | 4 | 2 | −2,4 M€ en 2020 | +3 073,7 M€ en 2024 |
| insee.t3215 | insee.t3305 | 30 | 4 | 2 | −0,6 M€ en 2002 | +738,0 M€ en 2024 |
| insee.t3215 | insee.t3306 | 30 | 3 | 1 | +0,7 M€ en 2022 | −1 139,0 M€ en 2024 |
| insee.t3215 | insee.t3307 | 16 | 16 | 14 | −20 301,8 M€ en 2009 | −20 301,8 M€ en 2009 |
| insee.t3215 | senat.pjl22-705 | 2 | 1 | 0 | aucun | −0,1 point de PIB en 2022 |
| insee.t3215 | senat.pjl24-035 | 2 | 2 | 0 | aucun | −0,3 point de PIB en 2023 |
| insee.t3215 | senat.pjl24-729 | 2 | 2 | 0 | aucun | −0,1 point de PIB en 2024 |
| insee.t3215 | senat.pjl25-727 | 2 | 2 | 0 | aucun | +0,1 point de PIB en 2025 |
| insee.t3216 | insee.t3217 | 93 | 24 | 24 | +734,9 M€ en 1995 | +734,9 M€ en 1995 |
| insee.t3216 | senat.pjl24-032 | 1 | 1 | 0 | aucun | −0,3 point de PIB en 2023 |
| insee.t3216 | senat.pjl24-718 | 1 | 1 | 0 | aucun | −0,1 point de PIB en 2024 |
| insee.t3216 | senat.pjl25-726 | 1 | 0 | 0 | aucun | aucun |
| insee.t3217 | senat.pjl24-032 | 1 | 1 | 0 | aucun | −0,3 point de PIB en 2023 |
| insee.t3217 | senat.pjl24-718 | 1 | 1 | 0 | aucun | −0,1 point de PIB en 2024 |
| insee.t3217 | senat.pjl25-726 | 1 | 0 | 0 | aucun | aucun |
| insee.t3301 | insee.t3307 | 1248 | 408 | 408 | −20 301,0 M€ en 2009 | −20 301,0 M€ en 2009 |
| ofgl.annexe-2a | ofgl.annexe-2b | 108 | 86 | 0 | aucun | −703,9 M€ en 2022 |
| senat.pjl06-389 | senat.pjl07-429 | 127 | 10 | 10 | +3 761,0 M€ en 2006 | +3 761,0 M€ en 2006 |
| senat.pjl11-073 | senat.pjl12-103 | 66 | 6 | 6 | −1 000,0 M€ en 2010 | −1 000,0 M€ en 2010 |
| senat.pjl12-103 | senat.pjl13-117 | 69 | 1 | 1 | +9 800,0 M€ en 2011 | +9 800,0 M€ en 2011 |
| senat.pjl13-117 | senat.pjl14-078 | 65 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl15-128 | 79 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl16-106 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl17-063 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl18-106 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl19-098 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl20-101 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl21-118 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl22-705 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl24-035 | 8 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl24-729 | 6 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.pjl25-727 | 4 | 0 | 0 | aucun | aucun |
| senat.pjl14-078 | senat.tas22-018 | 10 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl16-106 | 85 | 1 | 1 | −400,0 M€ en 2014 | −400,0 M€ en 2014 |
| senat.pjl15-128 | senat.pjl17-063 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl18-106 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl19-098 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl20-101 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl21-118 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl22-705 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl24-035 | 15 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl24-729 | 12 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.pjl25-727 | 9 | 0 | 0 | aucun | aucun |
| senat.pjl15-128 | senat.tas22-018 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl17-063 | 92 | 1 | 1 | +900,0 M€ en 2015 | +900,0 M€ en 2015 |
| senat.pjl16-106 | senat.pjl18-106 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl19-098 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl20-101 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl21-118 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl22-705 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl24-035 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl24-729 | 15 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.pjl25-727 | 12 | 0 | 0 | aucun | aucun |
| senat.pjl16-106 | senat.tas22-018 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl18-106 | 95 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl19-098 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl20-101 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl21-118 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl22-705 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl24-035 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl24-729 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.pjl25-727 | 15 | 0 | 0 | aucun | aucun |
| senat.pjl17-063 | senat.tas22-018 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl19-098 | 100 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl20-101 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl21-118 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl22-705 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl24-035 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl24-729 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.pjl25-727 | 18 | 0 | 0 | aucun | aucun |
| senat.pjl18-106 | senat.tas22-018 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.pjl20-101 | 101 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.pjl21-118 | 30 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.pjl22-705 | 30 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.pjl24-035 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.pjl24-729 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.pjl25-727 | 21 | 0 | 0 | aucun | aucun |
| senat.pjl19-098 | senat.tas22-018 | 30 | 0 | 0 | aucun | aucun |
| senat.pjl20-101 | senat.pjl21-118 | 104 | 0 | 0 | aucun | aucun |
| senat.pjl20-101 | senat.pjl22-705 | 33 | 0 | 0 | aucun | aucun |
| senat.pjl20-101 | senat.pjl24-035 | 30 | 0 | 0 | aucun | aucun |
| senat.pjl20-101 | senat.pjl24-729 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl20-101 | senat.pjl25-727 | 24 | 0 | 0 | aucun | aucun |
| senat.pjl20-101 | senat.tas22-018 | 33 | 0 | 0 | aucun | aucun |
| senat.pjl21-118 | senat.pjl22-705 | 36 | 0 | 0 | aucun | aucun |
| senat.pjl21-118 | senat.pjl24-035 | 33 | 0 | 0 | aucun | aucun |
| senat.pjl21-118 | senat.pjl24-729 | 30 | 0 | 0 | aucun | aucun |
| senat.pjl21-118 | senat.pjl25-727 | 27 | 0 | 0 | aucun | aucun |
| senat.pjl21-118 | senat.tas22-018 | 107 | 0 | 0 | aucun | aucun |
| senat.pjl22-705 | senat.pjl24-035 | 110 | 0 | 0 | aucun | aucun |
| senat.pjl22-705 | senat.pjl24-729 | 36 | 0 | 0 | aucun | aucun |
| senat.pjl22-705 | senat.pjl25-727 | 33 | 0 | 0 | aucun | aucun |
| senat.pjl22-705 | senat.tas22-018 | 110 | 0 | 0 | aucun | aucun |
| senat.pjl24-035 | senat.pjl24-729 | 110 | 0 | 0 | aucun | aucun |
| senat.pjl24-035 | senat.pjl25-727 | 36 | 0 | 0 | aucun | aucun |
| senat.pjl24-035 | senat.tas22-018 | 36 | 0 | 0 | aucun | aucun |
| senat.pjl24-729 | senat.pjl25-727 | 110 | 0 | 0 | aucun | aucun |
| senat.pjl24-729 | senat.tas22-018 | 33 | 0 | 0 | aucun | aucun |
| senat.pjl25-727 | senat.tas22-018 | 30 | 0 | 0 | aucun | aucun |

Détail des grandeurs en écart :

| Source A | Source B | Grandeur | Fonctions en écart | Années en écart | dont hors chiffres révisables | Plus grand écart (A − B) |
|---|---|---|---|---|---|---|
| dgcl.finances-departements | ofgl.annexe-2a | FR DEPARTEMENTS_BP COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | ensemble | 2022 | 2022 | +715,5 M€ en 2022 |
| dgcl.finances-departements | ofgl.annexe-2a | FR DEPARTEMENTS_BP COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | ensemble | 2022 | 2022 | +25,0 M€ en 2022 |
| dgcl.finances-departements | ofgl.annexe-2a | FR DEPARTEMENTS_BP COMPTES_LOCAUX.EMPRUNTS | ensemble | 2020 et 2022 | 2020 et 2022 | +15,8 M€ en 2020 |
| dgcl.finances-departements | ofgl.annexe-2a | FR DEPARTEMENTS_BP COMPTES_LOCAUX.EPARGNE_NETTE | ensemble | 2020 et 2022 | 2020 et 2022 | −15,8 M€ en 2020 |
| dgcl.finances-departements | ofgl.annexe-2a | FR DEPARTEMENTS_BP COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | ensemble | 2020 et 2022 | 2020 et 2022 | +15,8 M€ en 2020 |
| dgcl.finances-departements | ofgl.annexe-2b | FR DEPARTEMENTS_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | −703,9 M€ en 2022 |
| dgcl.finances-departements | ofgl.annexe-2b | FR DEPARTEMENTS_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 2021, 2022, 2023 et 2024 | aucune | +0,9 M€ en 2022 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | ensemble | 2023 | 2023 | −14 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | ensemble | 2023 | 2023 | +9 933 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.EPARGNE_BRUTE | ensemble | 2023 | 2023 | −15 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.EPARGNE_NETTE | ensemble | 2023 | 2023 | −15 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.REC_FONCTIONNEMENT | ensemble | 2023 | 2023 | −14 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.REC_INVESTISSEMENT | ensemble | 2023 | 2023 | +9 932 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2a | FR REGIONS_CTU_BP COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | ensemble | 2023 | 2023 | +9 919 € en 2023 |
| dgcl.finances-regions | ofgl.annexe-2b | FR REGIONS_CTU_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 2023 et 2024 | aucune | +144,4 M€ en 2024 |
| dgcl.finances-regions | ofgl.annexe-2b | FR REGIONS_CTU_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 2020, 2023 et 2024 | aucune | +4,5 M€ en 2024 |
| eurostat.gov_10a_exp | eurostat.gov_10a_main | FR S13 SEC2010.TE, en % du PIB | ensemble | 2024 | aucune | +0,3 point de PIB en 2024 |
| eurostat.gov_10a_exp | eurostat.gov_10a_main | FR S13 SEC2010.TE | ensemble | 18 années entre 1995 et 2024 | 16 années entre 1995 et 2022 | −914,4 M€ en 2024 |
| eurostat.gov_10a_exp | insee.t3201 | FR S13 SEC2010.TE | ensemble | 20 années entre 1995 et 2024 | 18 années entre 1995 et 2022 | −878,3 M€ en 2023 |
| eurostat.gov_10a_exp | insee.t3215 | FR S13 SEC2010.TE, en % du PIB | ensemble | 2023 et 2024 | aucune | +0,3 point de PIB en 2024 |
| eurostat.gov_10a_exp | insee.t3215 | FR S13 SEC2010.TE | ensemble | 20 années entre 1995 et 2024 | 18 années entre 1995 et 2022 | −914,4 M€ en 2024 |
| eurostat.gov_10a_exp | insee.t3301 | FR S13 SEC2010.TE | ensemble, GF01, GF04 et GF05 | 2012, 2018, 2020 et 2021 | 2012, 2018, 2020 et 2021 | +0,9 M€ en 2020 (GF01) |
| eurostat.gov_10a_exp | insee.t3307 | FR S13 SEC2010.TE | ensemble et 9 divisions | 10 années entre 2009 et 2018 | 10 années entre 2009 et 2018 | −20 300,8 M€ en 2009 (ensemble) |
| eurostat.gov_10a_main | insee.t3106 | FR S1314 SEC2010.B9 | ensemble | 2011 | 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3201 | FR S13 SEC2010.TE | ensemble | 2013, 2021 et 2024 | 2013 et 2021 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3201 | FR S13 SEC2010.TR | ensemble | 2021 et 2024 | 2021 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.B9 | ensemble | 2011 | 2011 | +0,4 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.TE | ensemble | 2019 et 2020 | 2019 et 2020 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.TR | ensemble | 2011, 2019 et 2020 | 2011, 2019 et 2020 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3215 | FR S13 SEC2010.TE | ensemble | 2013 | 2013 | +0,2 M€ en 2013 |
| eurostat.gov_10a_main | insee.t3215 | FR S13 SEC2010.TR | ensemble | 2024 | aucune | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3215 | FR S1314 SEC2010.TR | ensemble | 2011 | 2011 | +0,4 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3301 | FR S13 SEC2010.TE | ensemble | 15 années entre 1995 et 2024 | 13 années entre 1995 et 2022 | +914,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3302 | FR S1311 SEC2010.TE | ensemble | 6 années entre 1996 et 2024 | 1996, 2008, 2015 et 2016 | +954,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3305 | FR S1313 SEC2010.TE | ensemble | 2002, 2013, 2023 et 2024 | 2002 et 2013 | +738,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3306 | FR S1314 SEC2010.TE | ensemble | 2022, 2023 et 2024 | 2022 | −1 139,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3307 | FR S13 SEC2010.TE | ensemble | 16 années entre 2009 et 2024 | 14 années entre 2009 et 2022 | −20 301,7 M€ en 2009 |
| eurostat.gov_10a_main | insee.t7306 | FR S1314 SEC2010.B9 | ensemble | 2011 | 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | senat.pjl12-799 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2012 | aucune | −0,4 point de PIB en 2012 |
| eurostat.gov_10a_main | senat.pjl13-759 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2013 | aucune | −0,6 point de PIB en 2013 |
| eurostat.gov_10a_main | senat.pjl14-642 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2014 | aucune | −0,6 point de PIB en 2014 |
| eurostat.gov_10a_main | senat.pjl15-785 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2015 | aucune | −0,3 point de PIB en 2015 |
| eurostat.gov_10a_main | senat.pjl16-643 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2016 | aucune | −0,4 point de PIB en 2016 |
| eurostat.gov_10a_main | senat.pjl17-595 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2017 | aucune | −0,8 point de PIB en 2017 |
| eurostat.gov_10a_main | senat.pjl18-686 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2018 | aucune | +0,2 point de PIB en 2018 |
| eurostat.gov_10a_main | senat.pjl19-505 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2019 | aucune | +0,6 point de PIB en 2019 |
| eurostat.gov_10a_main | senat.pjl20-784 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2020 | aucune | +0,3 point de PIB en 2020 |
| eurostat.gov_10a_main | senat.pjl24-035 | FR S1314 SEC2010.TE, en % du PIB | ensemble | 2023 | aucune | −0,2 point de PIB en 2023 |
| eurostat.gov_10a_main | senat.pjl24-035 | FR S1314 SEC2010.TR, en % du PIB | ensemble | 2023 | aucune | −0,3 point de PIB en 2023 |
| eurostat.nama_10_gdp | insee.t3101 | FR S1 SEC2010.B1GQ | ensemble | 42 années entre 1978 et 2019 | 42 années entre 1978 et 2019 | −9 571,2 M€ en 1990 |
| insee.t3101 | insee.t3104 | FR S13 PDE.GD | ensemble | 6 années entre 2013 et 2022 | 6 années entre 2013 et 2022 | +171,0 M€ en 2015 |
| insee.t3101 | insee.t3104 | FR S1311 PDE.GD | ensemble | 9 années entre 1996 et 2020 | 9 années entre 1996 et 2020 | −79,2 M€ en 2007 |
| insee.t3101 | insee.t3104 | FR S1314 PDE.GD | ensemble | 2025 | aucune | −500,0 M€ en 2025 |
| insee.t3101 | insee.t3106 | FR S1 SEC2010.B1GQ | ensemble | 42 années entre 1978 et 2019 | 42 années entre 1978 et 2019 | +9 571,2 M€ en 1990 |
| insee.t3101 | senat.pjl24-032 | FR S13 PDE.GD, en % du PIB | ensemble | 2023 | aucune | −1,1 point de PIB en 2023 |
| insee.t3101 | senat.pjl24-718 | FR S13 PDE.GD, en % du PIB | ensemble | 2024 | aucune | −0,4 point de PIB en 2024 |
| insee.t3102 | insee.t3104 | FR S13 PDE.GD | ensemble | 2015 et 2020 | 2015 et 2020 | +200,0 M€ en 2015 |
| insee.t3102 | insee.t3104 | FR S1314 PDE.GD | ensemble | 2025 | aucune | −500,0 M€ en 2025 |
| insee.t3106 | insee.t3107 | FR S13111 SEC2010.B9 | ensemble | 2016 | 2016 | −59,0 M€ en 2016 |
| insee.t3106 | senat.pjl12-799 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2012 | aucune | −0,4 point de PIB en 2012 |
| insee.t3106 | senat.pjl13-759 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2013 | aucune | −0,6 point de PIB en 2013 |
| insee.t3106 | senat.pjl14-642 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2014 | aucune | −0,6 point de PIB en 2014 |
| insee.t3106 | senat.pjl15-785 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2015 | aucune | −0,3 point de PIB en 2015 |
| insee.t3106 | senat.pjl16-643 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2016 | aucune | −0,4 point de PIB en 2016 |
| insee.t3106 | senat.pjl17-595 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2017 | aucune | −0,8 point de PIB en 2017 |
| insee.t3106 | senat.pjl18-686 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2018 | aucune | +0,2 point de PIB en 2018 |
| insee.t3106 | senat.pjl19-505 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2019 | aucune | +0,6 point de PIB en 2019 |
| insee.t3106 | senat.pjl20-784 | FR S13 SEC2010.B9, en % du PIB | ensemble | 2020 | aucune | +0,3 point de PIB en 2020 |
| insee.t3107 | insee.t3203 | FR S13111 SEC2010.B9 | ensemble | 2016 | 2016 | +59,2 M€ en 2016 |
| insee.t3107 | insee.t7303 | FR S13111 SEC2010.B9 | ensemble | 2016 | 2016 | +59,0 M€ en 2016 |
| insee.t3107 | senat.pjl24-718 | FR ETAT_LF LOLF.SOLDE_COMPTES_SPECIAUX | ensemble | 2024 | aucune | −50,0 M€ en 2024 |
| insee.t3108 | insee.t3214 | FR S13142 SEC2010.B9 | ensemble | 6 années entre 2013 et 2018 | 6 années entre 2013 et 2018 | +271,0 M€ en 2018 |
| insee.t3108 | senat.tas22-018 | FR REGIME_GENERAL COMPTES_SECU.RESULTAT_COMPTABLE | ensemble | 2021 | 2021 | +5 000,0 M€ en 2021 |
| insee.t3201 | insee.t3215 | FR S13 SEC2010.TE | ensemble | 2021 et 2024 | 2021 | −119,0 M€ en 2024 |
| insee.t3201 | insee.t3215 | FR S13 SEC2010.TR | ensemble | 2021 | 2021 | +43,0 M€ en 2021 |
| insee.t3201 | insee.t3301 | FR S13 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | +487,9 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D1PAY | ensemble | 2011, 2023 et 2024 | 2011 | +889,0 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D3PAY | ensemble | 2001, 2023 et 2024 | 2001 | +552,0 M€ en 2023 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +1 807,3 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −1 949,3 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D9_HORS_D995PAY | ensemble | 6 années entre 2010 et 2024 | 2010, 2013, 2019 et 2021 | −2 012,0 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | +1 340,5 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.TE | ensemble | 15 années entre 1995 et 2024 | 13 années entre 1995 et 2022 | +877,8 M€ en 2023 |
| insee.t3201 | insee.t3307 | FR S13 SEC2010.TE | ensemble | 16 années entre 2009 et 2024 | 14 années entre 2009 et 2022 | −20 301,8 M€ en 2009 |
| insee.t3201 | insee.t7301 | FR S13 SEC2010.B8G | ensemble | 2022 | 2022 | +1,3 M€ en 2022 |
| insee.t3202 | insee.t3302 | FR S1311 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | −207,2 M€ en 2023 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.D1PAY | ensemble | 2023 et 2024 | aucune | +1 029,5 M€ en 2024 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.D3PAY | ensemble | 2023 et 2024 | aucune | +549,0 M€ en 2023 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.D62PAY | ensemble | 2023 | aucune | +79,0 M€ en 2023 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −375,0 M€ en 2024 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.D9_HORS_D995PAY | ensemble | 2023 et 2024 | aucune | −585,0 M€ en 2024 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.P2 | ensemble | 2022, 2023 et 2024 | 2022 | +773,0 M€ en 2024 |
| insee.t3202 | insee.t3302 | FR S1311 SEC2010.TE | ensemble | 6 années entre 1996 et 2024 | 1996, 2008, 2015 et 2016 | +954,2 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | −83,0 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.D1PAY | ensemble | 2024 | aucune | +4,4 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.D3PAY | ensemble | 2023 et 2024 | aucune | +386,0 M€ en 2023 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +176,0 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −374,0 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.D9_HORS_D995PAY | ensemble | 2018, 2023 et 2024 | 2018 | −441,0 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | +26,1 M€ en 2024 |
| insee.t3203 | insee.t3303 | FR S13111 SEC2010.TE | ensemble | 7 années entre 2014 et 2024 | 5 années entre 2014 et 2021 | +698,0 M€ en 2023 |
| insee.t3204 | insee.t3304 | FR S13112 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | −286,0 M€ en 2023 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.D1PAY | ensemble | 2023 et 2024 | aucune | +1 025,1 M€ en 2024 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.D3PAY | ensemble | 2023 et 2024 | aucune | +163,0 M€ en 2023 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | −175,0 M€ en 2024 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.D632PAY | ensemble | 2023 | aucune | +184,0 M€ en 2023 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.D9_HORS_D995PAY | ensemble | 2023 et 2024 | aucune | +170,0 M€ en 2024 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | +746,9 M€ en 2024 |
| insee.t3204 | insee.t3304 | FR S13112 SEC2010.TE | ensemble | 2018, 2020, 2023 et 2024 | 2018 et 2020 | +3 073,7 M€ en 2024 |
| insee.t3204 | insee.t7304 | FR S13112 SEC2010.B8G | ensemble | 2022 | 2022 | +1,4 M€ en 2022 |
| insee.t3205 | insee.t3305 | FR S1313 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | +592,5 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D1PAY | ensemble | 2023 et 2024 | aucune | +24,0 M€ en 2023 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D3PAY | ensemble | 2023 et 2024 | aucune | −10,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +502,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −525,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D9_HORS_D995PAY | ensemble | 2023 et 2024 | aucune | −331,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | −316,2 M€ en 2023 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.TE | ensemble | 2002, 2013, 2023 et 2024 | 2002 et 2013 | +738,0 M€ en 2024 |
| insee.t3212 | insee.t3215 | FR S1314 SEC2010.TE | ensemble | 2019 et 2020 | 2019 et 2020 | −39,0 M€ en 2019 |
| insee.t3212 | insee.t3215 | FR S1314 SEC2010.TR | ensemble | 2019 et 2020 | 2019 et 2020 | −39,0 M€ en 2019 |
| insee.t3212 | insee.t3306 | FR S1314 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | −162,8 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D1PAY | ensemble | 2023 et 2024 | aucune | −156,3 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D3PAY | ensemble | 2024 | aucune | +166,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +1 304,3 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −1 049,3 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D9_HORS_D995PAY | ensemble | 2019, 2020 et 2024 | 2019 et 2020 | −1 181,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | +464,6 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.TE | ensemble | 5 années entre 2019 et 2024 | 2019, 2020 et 2022 | −1 139,0 M€ en 2024 |
| insee.t3215 | insee.t3301 | FR S13 SEC2010.TE | ensemble | 15 années entre 1995 et 2024 | 13 années entre 1995 et 2022 | +914,2 M€ en 2024 |
| insee.t3215 | insee.t3303 | FR S13111 SEC2010.TE | ensemble | 7 années entre 2014 et 2024 | 5 années entre 2014 et 2021 | +698,0 M€ en 2023 |
| insee.t3215 | insee.t3304 | FR S13112 SEC2010.TE | ensemble | 2018, 2020, 2023 et 2024 | 2018 et 2020 | +3 073,7 M€ en 2024 |
| insee.t3215 | insee.t3305 | FR S1313 SEC2010.TE | ensemble | 2002, 2013, 2023 et 2024 | 2002 et 2013 | +738,0 M€ en 2024 |
| insee.t3215 | insee.t3306 | FR S1314 SEC2010.TE | ensemble | 2022, 2023 et 2024 | 2022 | −1 139,0 M€ en 2024 |
| insee.t3215 | insee.t3307 | FR S13 SEC2010.TE | ensemble | 16 années entre 2009 et 2024 | 14 années entre 2009 et 2022 | −20 301,8 M€ en 2009 |
| insee.t3215 | senat.pjl22-705 | FR S1314 SEC2010.TR, en % du PIB | ensemble | 2022 | aucune | −0,1 point de PIB en 2022 |
| insee.t3215 | senat.pjl24-035 | FR S1314 SEC2010.TE, en % du PIB | ensemble | 2023 | aucune | −0,2 point de PIB en 2023 |
| insee.t3215 | senat.pjl24-035 | FR S1314 SEC2010.TR, en % du PIB | ensemble | 2023 | aucune | −0,3 point de PIB en 2023 |
| insee.t3215 | senat.pjl24-729 | FR S1314 SEC2010.TE, en % du PIB | ensemble | 2024 | aucune | −0,1 point de PIB en 2024 |
| insee.t3215 | senat.pjl24-729 | FR S1314 SEC2010.TR, en % du PIB | ensemble | 2024 | aucune | −0,1 point de PIB en 2024 |
| insee.t3215 | senat.pjl25-727 | FR S1314 SEC2010.TE, en % du PIB | ensemble | 2025 | aucune | +0,1 point de PIB en 2025 |
| insee.t3215 | senat.pjl25-727 | FR S1314 SEC2010.TR, en % du PIB | ensemble | 2025 | aucune | +0,1 point de PIB en 2025 |
| insee.t3216 | insee.t3217 | FR S212 INSEE_PO.PO | ensemble | 24 années entre 1995 et 2018 | 24 années entre 1995 et 2018 | +734,9 M€ en 1995 |
| insee.t3216 | senat.pjl24-032 | FR S13_S212 INSEE_PO.PO, en % du PIB | ensemble | 2023 | aucune | −0,3 point de PIB en 2023 |
| insee.t3216 | senat.pjl24-718 | FR S13_S212 INSEE_PO.PO, en % du PIB | ensemble | 2024 | aucune | −0,1 point de PIB en 2024 |
| insee.t3217 | senat.pjl24-032 | FR S13_S212 INSEE_PO.PO, en % du PIB | ensemble | 2023 | aucune | −0,3 point de PIB en 2023 |
| insee.t3217 | senat.pjl24-718 | FR S13_S212 INSEE_PO.PO, en % du PIB | ensemble | 2024 | aucune | −0,1 point de PIB en 2024 |
| insee.t3301 | insee.t3307 | FR S13 SEC2010.TE | ensemble, 9 divisions et 41 groupes | 10 années entre 2009 et 2018 | 10 années entre 2009 et 2018 | −20 301,0 M€ en 2009 (ensemble) |
| ofgl.annexe-2a | ofgl.annexe-2b | FR COLLECTIVITES_LOCALES_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 6 années entre 2020 et 2025 | aucune | −651,3 M€ en 2022 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR COLLECTIVITES_LOCALES_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | +359,5 M€ en 2020 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR COLLECTIVITES_LOCALES_BP COMPTES_LOCAUX.DEP_TOTALES | ensemble | 6 années entre 2020 et 2025 | aucune | −637,7 M€ en 2022 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR COMMUNES_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 6 années entre 2020 et 2025 | aucune | −47,4 M€ en 2025 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR COMMUNES_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | +9,7 M€ en 2024 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR COMMUNES_BP COMPTES_LOCAUX.DEP_TOTALES | ensemble | 6 années entre 2020 et 2025 | aucune | −47,4 M€ en 2025 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR DEPARTEMENTS_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | −703,9 M€ en 2022 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR DEPARTEMENTS_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 2021, 2022, 2023 et 2024 | aucune | +0,9 M€ en 2022 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR DEPARTEMENTS_BP COMPTES_LOCAUX.DEP_TOTALES | ensemble | 5 années entre 2020 et 2024 | aucune | −703,0 M€ en 2022 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR GFP_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | +140,1 M€ en 2021 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR GFP_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | +361,7 M€ en 2020 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR GFP_BP COMPTES_LOCAUX.DEP_TOTALES | ensemble | 5 années entre 2020 et 2024 | aucune | +473,2 M€ en 2020 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR REGIONS_CTU_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 2023 et 2024 | aucune | +144,4 M€ en 2024 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR REGIONS_CTU_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 2020, 2023 et 2024 | aucune | +4,5 M€ en 2024 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR REGIONS_CTU_BP COMPTES_LOCAUX.DEP_TOTALES | ensemble | 2020, 2023 et 2024 | aucune | +148,9 M€ en 2024 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR SYNDICATS_BP COMPTES_LOCAUX.DEP_FONCTIONNEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | +145,4 M€ en 2024 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR SYNDICATS_BP COMPTES_LOCAUX.DEP_INVESTISSEMENT | ensemble | 5 années entre 2020 et 2024 | aucune | −1,9 M€ en 2024 |
| ofgl.annexe-2a | ofgl.annexe-2b | FR SYNDICATS_BP COMPTES_LOCAUX.DEP_TOTALES | ensemble | 5 années entre 2020 et 2024 | aucune | +143,8 M€ en 2024 |
| senat.pjl06-389 | senat.pjl07-429 | FR ETAT_CGE COMPTES_ETAT.ACTIF | ensemble | 2005 et 2006 | 2005 et 2006 | +3 760,0 M€ en 2006 |
| senat.pjl06-389 | senat.pjl07-429 | FR ETAT_CGE COMPTES_ETAT.AUTRES_TRESORERIE_PASSIF | ensemble | 2005 et 2006 | 2005 et 2006 | +3 761,0 M€ en 2006 |
| senat.pjl06-389 | senat.pjl07-429 | FR ETAT_CGE COMPTES_ETAT.PASSIF | ensemble | 2005 et 2006 | 2005 et 2006 | +3 761,0 M€ en 2006 |
| senat.pjl06-389 | senat.pjl07-429 | FR ETAT_CGE COMPTES_ETAT.TRESORERIE_ACTIF | ensemble | 2005 et 2006 | 2005 et 2006 | +3 761,0 M€ en 2006 |
| senat.pjl06-389 | senat.pjl07-429 | FR ETAT_CGE COMPTES_ETAT.TRESORERIE_PASSIF | ensemble | 2005 et 2006 | 2005 et 2006 | +3 761,0 M€ en 2006 |
| senat.pjl11-073 | senat.pjl12-103 | FR SECU_LFSS COMPTES_SECU.ACTIF_CIRCULANT | ensemble | 2010 | 2010 | −200,0 M€ en 2010 |
| senat.pjl11-073 | senat.pjl12-103 | FR SECU_LFSS COMPTES_SECU.AUTRES_PASSIFS | ensemble | 2010 | 2010 | +700,0 M€ en 2010 |
| senat.pjl11-073 | senat.pjl12-103 | FR SECU_LFSS COMPTES_SECU.DETTES_ENTITES_PUBLIQUES | ensemble | 2010 | 2010 | −1 000,0 M€ en 2010 |
| senat.pjl11-073 | senat.pjl12-103 | FR SECU_LFSS COMPTES_SECU.PASSIF_CIRCULANT | ensemble | 2010 | 2010 | −300,0 M€ en 2010 |
| senat.pjl11-073 | senat.pjl12-103 | FR SECU_LFSS COMPTES_SECU.TOTAL_ACTIF | ensemble | 2010 | 2010 | −300,0 M€ en 2010 |
| senat.pjl11-073 | senat.pjl12-103 | FR SECU_LFSS COMPTES_SECU.TOTAL_PASSIF | ensemble | 2010 | 2010 | −300,0 M€ en 2010 |
| senat.pjl12-103 | senat.pjl13-117 | FR REGIME_GENERAL_HORS_FSV COMPTES_SECU.REPORT_A_NOUVEAU | ensemble | 2011 | 2011 | +9 800,0 M€ en 2011 |
| senat.pjl15-128 | senat.pjl16-106 | FR SECU_LFSS COMPTES_SECU.CREANCES_ENTITES_PUBLIQUES | ensemble | 2014 | 2014 | −400,0 M€ en 2014 |
| senat.pjl16-106 | senat.pjl17-063 | FR FSV COMPTES_SECU.ENCOURS_BANCAIRE | ensemble | 2015 | 2015 | +900,0 M€ en 2015 |

## 7. Comptes de chaque collectivité

Les comptes que l'OFGL publie collectivité par collectivité sur data.ofgl.fr, dans la version la plus récente de chaque exercice. Chaque ligne donne, pour une collectivité et un agrégat, le montant de son budget principal, celui de ses budgets annexes, les flux croisés entre eux et le montant consolidé : celui-ci doit être la somme des deux premiers moins le troisième, à l'arrondi près : la demi-unité de la dernière décimale publiée de chaque montant, au centime au plus fin (les montants de 2022 n'ont que dix chiffres significatifs). Pour chaque collectivité, les identités comptables de la section 1 s'appliquent à chacun des quatre montants. La somme des collectivités se compare aux totaux des annexes des rapports de l'OFGL : 2A pour les budgets principaux, 2B pour les budgets annexes, 2C pour les comptes consolidés ; celle des départements sans la métropole de Lyon ni la Ville de Paris, que les annexes comptent avec les groupements à fiscalité propre et avec les communes. Le budget principal de chaque département et de chaque région se compare aussi à sa fiche dans les publications de la DGCL. Les SDIS et les centres d'action sociale ne sont publiés que budget par budget, sans consolidation : chaque ligne donne le montant d'un budget, auquel s'appliquent les identités comptables. Les annexes ne donnent de total ni pour eux, ni pour les établissements publics locaux.

| Jeu de données | Exercices | Collectivités au dernier exercice | Lignes | Lignes dont le consolidé n'est pas BP + BA − flux |
|---|---|---|---|---|
| ofgl.base-ccas-cias | 8 années entre 2018 et 2025 | 11 023 | 5 154 438 | sans objet |
| ofgl.base-communes-consolidee | 8 années entre 2018 et 2025 | 34 778 | 13 535 660 | 0 |
| ofgl.base-departements-consolidee | 14 années entre 2012 et 2025 | 97 | 88 417 | 0 |
| ofgl.base-epl-consolidee | 8 années entre 2018 et 2025 | 1 197 | 382 050 | 0 |
| ofgl.base-gfp-consolidee | 8 années entre 2018 et 2025 | 1 262 | 508 116 | 0 |
| ofgl.base-regions-consolidee | 14 années entre 2012 et 2025 | 17 | 14 547 | 0 |
| ofgl.base-sdis | 14 années entre 2012 et 2025 | 97 | 84 420 | sans objet |
| ofgl.base-syndicats-consolidee | 8 années entre 2018 et 2025 | 8 522 | 3 027 867 | 0 |

Identités comptables de chaque collectivité, ou de chaque budget pour les jeux publiés budget par budget : 32 462 722 vérifiées, 32 462 722 justes, 0 en écart.

Collectivités que deux jeux de données donnent : 131 768 montants comparés de l'un à l'autre, 131 762 égaux, 6 en écart. Les agrégats qu'un seul des deux jeux publie, désignés par leur concept de la norme COMPTES_LOCAUX, ne se comparent pas.

| Premier jeu | Second jeu | Collectivités | Exercices | Montants comparés | En écart | Agrégats du seul premier jeu | Agrégats du seul second |
|---|---|---|---|---|---|---|---|
| ofgl.base-communes-consolidee | ofgl.base-departements-consolidee | VILLE DE PARIS (217500016) | 7 années entre 2019 et 2025 | 1 400 | 0 | TEOM | ALLOCATIONS_APA, ALLOCATIONS_PCH, ALLOCATIONS_RSA, CONCOURS_CNSA, CONTRIBUTIONS_SDIS, CVAE, DDEC, DMTO, DMTO_APRES_PEREQUATION, EPARGNE_BRUTE_AVANT_TRAVAUX_REGIE, FMDI, FRAIS_HEBERGEMENT, PRELEVEMENTS_PEREQUATION_DMTO, TICPE, TRAVAUX_REGIE, TSCA |
| ofgl.base-departements-consolidee | ofgl.base-gfp-consolidee | MET DE LYON (200046977) | 8 années entre 2018 et 2025 | 1 572 | 6 | ALLOCATIONS_APA, ALLOCATIONS_PCH, ALLOCATIONS_RSA, ATTRIBUTIONS_PEREQUATION_DMTO, CONCOURS_CNSA, CONTRIBUTIONS_SDIS, CVAE, DDEC, DMTO, DMTO_APRES_PEREQUATION, EPARGNE_BRUTE_AVANT_TRAVAUX_REGIE, FMDI, FRAIS_HEBERGEMENT, PRELEVEMENTS_PEREQUATION_DMTO, TICPE, TSCA | CREDITS_TRESORERIE, TEOM, VERSEMENT_TRANSPORT |
| ofgl.base-epl-consolidee | ofgl.base-syndicats-consolidee | 102 collectivités | 8 années entre 2018 et 2025 | 128 796 | 0 | aucun | aucun |

| Collectivité | Exercice | Grandeur | Montant | Écart (premier jeu − second) |
|---|---|---|---|---|
| MET DE LYON (200046977) | 2024 | COMPTES_LOCAUX.AUTRES_IMPOTS_TAXES | budget principal | +8,4 M€ |
| MET DE LYON (200046977) | 2024 | COMPTES_LOCAUX.AUTRES_IMPOTS_TAXES | consolidé | +8,4 M€ |
| MET DE LYON (200046977) | 2024 | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | budget principal | −8,4 M€ |
| MET DE LYON (200046977) | 2024 | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | consolidé | −8,4 M€ |
| MET DE LYON (200046977) | 2024 | COMPTES_LOCAUX.IMPOTS_TAXES | budget principal | +8,4 M€ |
| MET DE LYON (200046977) | 2024 | COMPTES_LOCAUX.IMPOTS_TAXES | consolidé | +8,4 M€ |

Somme des collectivités contre les totaux des annexes : 4 271 comparaisons, 2 970 justes, 1 301 en écart. Le dernier exercice d'un jeu est provisoire, et les annexes d'un rapport ne sont pas toujours établies sur la même version des comptes que le portail : un écart qui touche un chiffre révisable peut venir de là.

| Jeu de données | Montant | Comparaisons | En écart | dont hors chiffres révisables | Plus grand écart hors chiffres révisables (somme − annexe) | Plus grand écart (somme − annexe) |
|---|---|---|---|---|---|---|
| ofgl.base-communes-consolidee | budget principal | 308 | 115 | 76 | −13,6 M€ en 2024 (COMPTES_LOCAUX.REC_TOTALES) | −82,3 M€ en 2025 (COMPTES_LOCAUX.DEP_TOTALES) |
| ofgl.base-communes-consolidee | budgets annexes | 252 | 93 | 62 | −1,2 M€ en 2024 (COMPTES_LOCAUX.DETTE) | −17,3 M€ en 2025 (COMPTES_LOCAUX.DETTE) |
| ofgl.base-communes-consolidee | consolidé | 252 | 152 | 120 | +121,0 M€ en 2024 (COMPTES_LOCAUX.DEPENSES_INTERVENTION) | +173,8 M€ en 2025 (COMPTES_LOCAUX.DEPENSES_INTERVENTION) |
| ofgl.base-departements-consolidee | budget principal | 364 | 32 | 4 | −0,7 M€ en 2024 (COMPTES_LOCAUX.TICPE) | +18,9 M€ en 2025 (COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS) |
| ofgl.base-departements-consolidee | budgets annexes | 283 | 36 | 20 | −36,7 M€ en 2023 (COMPTES_LOCAUX.DEP_TOTALES) | −36,7 M€ en 2023 (COMPTES_LOCAUX.DEP_TOTALES) |
| ofgl.base-departements-consolidee | consolidé | 283 | 142 | 115 | −49,0 M€ en 2023 (COMPTES_LOCAUX.DEP_TOTALES) | −63,9 M€ en 2025 (COMPTES_LOCAUX.REC_FONCTIONNEMENT) |
| ofgl.base-gfp-consolidee | budget principal | 300 | 38 | 0 | aucun | −53,7 M€ en 2025 (COMPTES_LOCAUX.DETTE) |
| ofgl.base-gfp-consolidee | budgets annexes | 252 | 69 | 37 | +0,6 M€ en 2018 (COMPTES_LOCAUX.DEP_TOTALES) | +94,8 M€ en 2025 (COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT) |
| ofgl.base-gfp-consolidee | consolidé | 252 | 56 | 24 | +84,4 M€ en 2024 (COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES) | +131,2 M€ en 2025 (COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES) |
| ofgl.base-regions-consolidee | budget principal | 355 | 32 | 0 | aucun | +100,4 M€ en 2025 (COMPTES_LOCAUX.DEP_FONCTIONNEMENT) |
| ofgl.base-regions-consolidee | budgets annexes | 283 | 12 | 0 | aucun | +1,8 M€ en 2025 (COMPTES_LOCAUX.REC_TOTALES) |
| ofgl.base-regions-consolidee | consolidé | 283 | 27 | 0 | aucun | +99,0 M€ en 2025 (COMPTES_LOCAUX.DEP_FONCTIONNEMENT) |
| ofgl.base-syndicats-consolidee | budget principal | 300 | 170 | 134 | −27,5 M€ en 2019 (COMPTES_LOCAUX.DEP_TOTALES) | −120,7 M€ en 2025 (COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS) |
| ofgl.base-syndicats-consolidee | budgets annexes | 252 | 111 | 81 | −3,3 M€ en 2020 (COMPTES_LOCAUX.REC_TOTALES) | −19,8 M€ en 2025 (COMPTES_LOCAUX.DEP_TOTALES) |
| ofgl.base-syndicats-consolidee | consolidé | 252 | 216 | 184 | −27,1 M€ en 2019 (COMPTES_LOCAUX.DEP_TOTALES) | −122,4 M€ en 2025 (COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS) |

Écarts hors chiffres révisables :

| Jeu de données | Montant | Grandeur | Années en écart | Plus grand écart (somme − annexe) |
|---|---|---|---|---|
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2019 et 2024 | −2,6 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 2019 et 2024 | −0,3 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_DOTATIONS | 2024 | −25 556 € en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_IMPOTS_TAXES | 2019 et 2024 | −0,6 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2019 et 2024 | −0,4 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 2019 et 2024 | −0,1 M€ en 2019 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2019 et 2024 | −0,8 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.CHARGES_FINANCIERES | 2019 et 2024 | −0,2 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.CONCOURS_ETAT | 2019 et 2024 | −0,9 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 2019 et 2024 | −5,0 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DEPENSES_INTERVENTION | 2019 et 2024 | −0,3 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2019 et 2024 | −7,6 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2019 et 2024 | −5,2 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DEP_TOTALES | 2019 et 2024 | −13,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 2019 et 2024 | −12,8 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DETTE | 2019 et 2024 | −4,0 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DGF | 2019 et 2024 | −0,5 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.DOTATIONS_SUBVENTIONS_INVESTISSEMENT | 2019 et 2024 | −3,4 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.EPARGNE_BRUTE | 2019 et 2024 | −1,2 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.EPARGNE_NETTE | 2019 et 2024 | −0,8 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.FCTVA | 2019 et 2024 | −1,4 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.FISCALITE_REVERSEE | 5 années entre 2018 et 2024 | +3,0 M€ en 2018 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.FLUX_NET_DETTE | 2019 et 2024 | +0,3 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.FRAIS_PERSONNEL | 2019 et 2024 | −4,2 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.IMPOTS_LOCAUX | 2019 et 2024 | −5,3 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.IMPOTS_TAXES | 2019 et 2024 | −6,0 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.PEREQUATIONS_COMPENSATIONS | 2019 et 2024 | −0,3 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2019 et 2024 | −8,8 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2019 et 2024 | −4,9 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.REC_TOTALES | 2019 et 2024 | −13,6 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 2019 et 2024 | −13,6 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 2019 et 2024 | −0,3 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.SUBVENTIONS_EQUIPEMENT_VERSEES | 2019 et 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2019 et 2024 | −0,5 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.TRESORERIE_NETTE | 2024 | −4,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2019 et 2024 | −0,5 M€ en 2024 |
| ofgl.base-communes-consolidee | budget principal | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 2019 et 2024 | −1,0 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2018 et 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 2018 et 2024 | −0,2 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2018 et 2024 | −0,2 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2018, 2019, 2023 et 2024 | −0,1 M€ en 2023 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.CHARGES_FINANCIERES | 2019 et 2024 | −48 236 € en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 2024 | −908 € en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2018, 2019 et 2024 | −0,2 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2024 | −907 € en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES | 2018, 2019 et 2024 | −0,4 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 2018, 2019 et 2024 | −0,2 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DETTE | 5 années entre 2018 et 2024 | −1,2 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.DOTATIONS_SUBVENTIONS_INVESTISSEMENT | 2024 | −47 710 € en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.EMPRUNTS | 2023 | −0,1 M€ en 2023 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.EPARGNE_BRUTE | 2018, 2019, 2023 et 2024 | +0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.FCTVA | 2024 | −6 844 € en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.FLUX_NET_DETTE | 2018, 2019, 2023 et 2024 | +0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.FRAIS_PERSONNEL | 2018 et 2024 | −18 184 € en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2018, 2023 et 2024 | −0,3 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES | 2018, 2023 et 2024 | −0,3 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 2018, 2023 et 2024 | −0,3 M€ en 2018 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 2018, 2019 et 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2023 | −0,1 M€ en 2023 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.TRESORERIE_NETTE | 2023 | −0,1 M€ en 2023 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2018, 2019, 2023 et 2024 | +0,2 M€ en 2024 |
| ofgl.base-communes-consolidee | budgets annexes | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 2018 et 2024 | −0,2 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 5 années entre 2018 et 2024 | −1,7 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 7 années entre 2018 et 2024 | −110,3 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 7 années entre 2018 et 2024 | −110,2 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 2018, 2019 et 2024 | +0,1 M€ en 2018 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2018, 2019 et 2024 | −0,8 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.CHARGES_FINANCIERES | 2019 et 2024 | −0,2 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.CONCOURS_ETAT | 2019 et 2024 | −0,9 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 2019 et 2024 | −5,0 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DEPENSES_INTERVENTION | 2019, 2022, 2023 et 2024 | +121,0 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 7 années entre 2018 et 2024 | −73,7 M€ en 2023 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2019 et 2024 | −5,2 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES | 7 années entre 2018 et 2024 | −73,7 M€ en 2023 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 7 années entre 2018 et 2024 | −73,7 M€ en 2023 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DETTE | 2018, 2019, 2020 et 2024 | −5,2 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.DOTATIONS_SUBVENTIONS_INVESTISSEMENT | 2019 et 2024 | −3,4 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.EPARGNE_BRUTE | 2018, 2019 et 2024 | −1,1 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.FCTVA | 2019 et 2024 | −1,4 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.FLUX_NET_DETTE | 2018, 2019 et 2024 | +0,5 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.FRAIS_PERSONNEL | 2018, 2019 et 2024 | −4,2 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.IMPOTS_TAXES | 2019 et 2024 | −6,0 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 7 années entre 2018 et 2024 | −73,7 M€ en 2023 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2018, 2019 et 2024 | −4,9 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES | 7 années entre 2018 et 2024 | −73,7 M€ en 2023 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 7 années entre 2018 et 2024 | −73,7 M€ en 2023 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 2018, 2019 et 2024 | −0,5 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.SUBVENTIONS_EQUIPEMENT_VERSEES | 2019 et 2024 | −0,1 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2019, 2022, 2023 et 2024 | +120,8 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.TRESORERIE_NETTE | 2024 | −4,1 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2018, 2019 et 2024 | −0,3 M€ en 2024 |
| ofgl.base-communes-consolidee | consolidé | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 5 années entre 2018 et 2024 | +0,3 M€ en 2023 |
| ofgl.base-departements-consolidee | budget principal | COMPTES_LOCAUX.DMTO | 2022, 2023 et 2024 | −0,1 M€ en 2023 |
| ofgl.base-departements-consolidee | budget principal | COMPTES_LOCAUX.TICPE | 2024 | −0,7 M€ en 2024 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2023 | −5,7 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 2023 | −0,2 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2023 | −0,4 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 2023 | −12 100 € en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2023 | +1,5 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 2023 | −0,3 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2023 | −36,3 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2023 | −0,3 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES | 2023 | −36,7 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 2023 | −36,7 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.EPARGNE_BRUTE | 2023 | +1,2 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.FCTVA | 2023 | −39 431 € en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.FRAIS_PERSONNEL | 2023 | −30,4 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2023 | −35,1 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2023 | −0,1 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES | 2023 | −35,2 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 2023 | −35,2 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2023 | −34,7 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2023 | +1,5 M€ en 2023 |
| ofgl.base-departements-consolidee | budgets annexes | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 2023 | −5 938 € en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2023 | −5,7 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 2023 | −0,2 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 8 années entre 2017 et 2024 | −2,7 M€ en 2019 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2023 | −0,4 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 8 années entre 2017 et 2024 | −18,5 M€ en 2022 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 8 années entre 2017 et 2024 | −33,7 M€ en 2024 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 2023 | −0,3 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2023 et 2024 | −36,3 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 8 années entre 2017 et 2024 | −2,7 M€ en 2019 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES | 8 années entre 2017 et 2024 | −49,0 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 8 années entre 2017 et 2024 | −36,9 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.EMPRUNTS | 8 années entre 2017 et 2024 | −2,7 M€ en 2019 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.EPARGNE_BRUTE | 2023 et 2024 | −29,9 M€ en 2024 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.FCTVA | 2023 | −39 430 € en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.FLUX_NET_DETTE | 8 années entre 2017 et 2024 | +17,9 M€ en 2022 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.FRAIS_PERSONNEL | 2023 et 2024 | −30,4 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2023 et 2024 | −42,2 M€ en 2024 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.REC_INVESTISSEMENT | 8 années entre 2017 et 2024 | −18,5 M€ en 2022 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES | 8 années entre 2017 et 2024 | −47,6 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 8 années entre 2017 et 2024 | −47,4 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 8 années entre 2017 et 2024 | −18,5 M€ en 2022 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2023 et 2024 | −34,7 M€ en 2023 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2023 et 2024 | −29,9 M€ en 2024 |
| ofgl.base-departements-consolidee | consolidé | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 2023 et 2024 | −12,3 M€ en 2024 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2018 et 2024 | +47 670 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 2018 | +1 976 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2018 | −1 082 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 2018 | +23 357 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2018, 2023 et 2024 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.CHARGES_FINANCIERES | 2018 | +16 440 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2018 et 2024 | +0,1 M€ en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2018 | +1 975 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES | 2018 et 2024 | +0,6 M€ en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 2018 et 2024 | +0,1 M€ en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.DETTE | 2018 et 2023 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.EMPRUNTS | 2023 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.EPARGNE_BRUTE | 2018, 2023 et 2024 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.FLUX_NET_DETTE | 2018 et 2023 | −0,5 M€ en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.IMPOTS_TAXES | 2018 | +1 083 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2023 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2018 | +23 357 € en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES | 2018 et 2023 | +0,2 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 2018 et 2023 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 2018 | +0,6 M€ en 2018 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2023 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.TRESORERIE_NETTE | 2023 | +0,1 M€ en 2023 |
| ofgl.base-gfp-consolidee | budgets annexes | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2018, 2023 et 2024 | −0,6 M€ en 2018 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2023 et 2024 | −16,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2018 | −1 082 € en 2018 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2024 | +4 185 € en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.DEPENSES_INTERVENTION | 2024 | +84,4 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2023 et 2024 | +67,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES | 2023 et 2024 | +67,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 2023 et 2024 | +67,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.DETTE | 2018 | +1 989 € en 2018 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.EPARGNE_BRUTE | 2024 | +4 185 € en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.IMPOTS_TAXES | 2018 | +1 082 € en 2018 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2023 et 2024 | +67,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES | 2023 et 2024 | +67,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 2023 et 2024 | +67,7 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2024 | +84,4 M€ en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2024 | +4 185 € en 2024 |
| ofgl.base-gfp-consolidee | consolidé | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 2023 et 2024 | −16,7 M€ en 2024 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 6 années entre 2018 et 2024 | −8,4 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 5 années entre 2018 et 2024 | −2,5 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 2024 | −32 771 € en 2024 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_DOTATIONS | 2018 | +44 365 € en 2018 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_IMPOTS_TAXES | 2019 | −5,1 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2018, 2019, 2022 et 2023 | −1,9 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 2022, 2023 et 2024 | −0,1 M€ en 2022 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 6 années entre 2018 et 2024 | +3,6 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.CHARGES_FINANCIERES | 2019 et 2023 | −0,8 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 6 années entre 2018 et 2024 | +14,7 M€ en 2024 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DEPENSES_INTERVENTION | 2019 | −2 630 € en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 6 années entre 2018 et 2024 | −20,5 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2018, 2019, 2023 et 2024 | −6,2 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DEP_TOTALES | 6 années entre 2018 et 2024 | −27,5 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 6 années entre 2018 et 2024 | −22,0 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DETTE | 2019 et 2023 | −23,1 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DGF | 2018 | −44 363 € en 2018 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.DOTATIONS_SUBVENTIONS_INVESTISSEMENT | 2023 | −0,3 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.EMPRUNTS | 2023 | −2,0 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.EPARGNE_BRUTE | 6 années entre 2018 et 2024 | −5,9 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.EPARGNE_NETTE | 6 années entre 2018 et 2024 | +7,6 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.FCTVA | 2022, 2023 et 2024 | −5 734 € en 2024 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.FLUX_NET_DETTE | 2019, 2022 et 2023 | +5,5 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.FRAIS_PERSONNEL | 5 années entre 2018 et 2024 | −11,0 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.IMPOTS_LOCAUX | 2019 | −1,3 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.IMPOTS_TAXES | 2019 | −6,3 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 6 années entre 2018 et 2024 | −18,4 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2022, 2023 et 2024 | −0,3 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.REC_TOTALES | 6 années entre 2018 et 2024 | −20,4 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 6 années entre 2018 et 2024 | −18,4 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 2019, 2022 et 2023 | −5,5 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.SUBVENTIONS_EQUIPEMENT_VERSEES | 2021, 2022, 2023 et 2024 | −14,8 M€ en 2024 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2019, 2023 et 2024 | −12,0 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.TRESORERIE_NETTE | 2022, 2023 et 2024 | −3,2 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 6 années entre 2018 et 2024 | +9,1 M€ en 2019 |
| ofgl.base-syndicats-consolidee | budget principal | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 6 années entre 2018 et 2024 | −15,9 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 2020, 2021 et 2023 | −0,6 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 2020 et 2023 | −41 940 € en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 2018 et 2023 | −0,7 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 2020 | −0,1 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 2018 et 2023 | −0,7 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 2018, 2020, 2021 et 2023 | −0,5 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.CHARGES_FINANCIERES | 2018 | −16 439 € en 2018 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.CONCOURS_ETAT | 5 années entre 2018 et 2024 | −0,6 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 2020, 2021 et 2023 | −32 704 € en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DEPENSES_INTERVENTION | 2023 | −4 623 € en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 2018, 2020, 2021 et 2023 | −2,9 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 2018, 2020, 2021 et 2023 | −0,7 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES | 2018, 2020, 2021 et 2023 | −2,9 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 2018, 2020, 2021 et 2023 | −2,9 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DETTE | 2020 et 2021 | −3,1 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.DOTATIONS_SUBVENTIONS_INVESTISSEMENT | 2023 | −6 158 € en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.EMPRUNTS | 2020 et 2021 | −50 000 € en 2021 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.EPARGNE_BRUTE | 2018, 2020, 2021 et 2023 | −0,5 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.FCTVA | 2020 et 2023 | −3 382 € en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.FLUX_NET_DETTE | 2018, 2020 et 2021 | +0,6 M€ en 2018 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.FRAIS_PERSONNEL | 2020, 2021 et 2023 | −2,3 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 2020, 2021 et 2023 | −3,3 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.REC_INVESTISSEMENT | 2018, 2020 et 2023 | −0,7 M€ en 2023 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES | 2018, 2020, 2021 et 2023 | −3,3 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 2018, 2020, 2021 et 2023 | −3,3 M€ en 2020 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 2018 et 2020 | −0,5 M€ en 2018 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 2020, 2021 et 2023 | −1,6 M€ en 2021 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 2018, 2020, 2021 et 2023 | +0,5 M€ en 2018 |
| ofgl.base-syndicats-consolidee | budgets annexes | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 2020 | −2,0 M€ en 2020 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.ACHATS_CHARGES_EXTERNES | 7 années entre 2018 et 2024 | −7,8 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 6 années entre 2018 et 2024 | −2,7 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_DEP_INVESTISSEMENT | 7 années entre 2018 et 2024 | −1,1 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 7 années entre 2018 et 2024 | −2,1 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 5 années entre 2020 et 2024 | −0,7 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.CAPACITE_BESOIN_FINANCEMENT | 7 années entre 2018 et 2024 | +5,5 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.CHARGES_FINANCIERES | 6 années entre 2019 et 2024 | −0,9 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.CONCOURS_ETAT | 5 années entre 2018 et 2024 | −0,6 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DEPENSES_EQUIPEMENT | 7 années entre 2018 et 2024 | +14,7 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DEPENSES_INTERVENTION | 2019, 2023 et 2024 | +22,9 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DEP_FONCTIONNEMENT | 7 années entre 2018 et 2024 | +21,8 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DEP_INVESTISSEMENT | 7 années entre 2018 et 2024 | −7,2 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES | 7 années entre 2018 et 2024 | −27,1 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS | 7 années entre 2018 et 2024 | +21,6 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DETTE | 2019, 2020, 2021 et 2023 | −23,1 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.DOTATIONS_SUBVENTIONS_INVESTISSEMENT | 2023 | −0,3 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.EMPRUNTS | 7 années entre 2018 et 2024 | −2,4 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.EPARGNE_BRUTE | 7 années entre 2018 et 2024 | −6,1 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.FCTVA | 2020, 2022, 2023 et 2024 | −5 734 € en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.FLUX_NET_DETTE | 7 années entre 2018 et 2024 | +5,4 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.FRAIS_PERSONNEL | 7 années entre 2018 et 2024 | −11,0 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.IMPOTS_TAXES | 2019 | −6,3 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 7 années entre 2018 et 2024 | +21,7 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.REC_INVESTISSEMENT | 5 années entre 2020 et 2024 | −1,0 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES | 7 années entre 2018 et 2024 | −22,6 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 7 années entre 2018 et 2024 | +21,7 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 6 années entre 2019 et 2024 | −5,5 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.SUBVENTIONS_EQUIPEMENT_VERSEES | 2021, 2022, 2023 et 2024 | −14,8 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.SUBVENTIONS_PARTICIPATIONS_RECUES | 5 années entre 2019 et 2024 | +22,3 M€ en 2024 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.TRESORERIE_NETTE | 2022, 2023 et 2024 | −3,2 M€ en 2023 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.VARIATION_FONDS_ROULEMENT | 7 années entre 2018 et 2024 | +11,0 M€ en 2019 |
| ofgl.base-syndicats-consolidee | consolidé | COMPTES_LOCAUX.VENTES_BIENS_SERVICES | 7 années entre 2018 et 2024 | −15,2 M€ en 2023 |

Budget principal de chaque département et de chaque région contre sa fiche dans les publications de la DGCL (« Les finances des départements », « Les finances des régions ») : 19 329 comparaisons, 19 272 justes, 57 en écart.

| Jeu de données | Grandeur | Comparaisons | En écart | Années en écart | Plus grand écart (OFGL − DGCL) |
|---|---|---|---|---|---|
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.AUTRES_DEP_FONCTIONNEMENT | 486 | 33 | 2022 | −50,0 M€ : DEP HAUTE-GARONNE (223100017), 2022 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.AUTRES_IMPOTS_TAXES | 486 | 1 | 2024 | +8,4 M€ : MET DE LYON (200046977), 2024 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 486 | 2 | 2022 et 2024 | −25,0 M€ : DEP CORREZE (221927205), 2022 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.DMTO | 486 | 7 | 2022, 2023 et 2024 | −0,1 M€ : DEP EURE-ET-LOIR (222800013), 2023 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.EMPRUNTS | 486 | 2 | 2020 et 2022 | −15,8 M€ : DEP SAONE-ET-LOIRE (227100013), 2020 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.EPARGNE_NETTE | 486 | 2 | 2020 et 2022 | +15,8 M€ : DEP SAONE-ET-LOIRE (227100013), 2020 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | 486 | 1 | 2020 | −15,8 M€ : DEP SAONE-ET-LOIRE (227100013), 2020 |
| ofgl.base-departements-consolidee | COMPTES_LOCAUX.TICPE | 486 | 1 | 2024 | −0,7 M€ : DEP MAYOTTE (229850003), 2024 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.AUTRES_REC_FONCTIONNEMENT | 85 | 1 | 2023 | +14 € : REG PAYS-DE-LA-LOIRE (234400034), 2023 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.AUTRES_REC_INVESTISSEMENT | 85 | 1 | 2023 | −9 933 € : REG OCCITANIE (200053791), 2023 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.EPARGNE_BRUTE | 85 | 1 | 2023 | +14 € : REG PAYS-DE-LA-LOIRE (234400034), 2023 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.EPARGNE_NETTE | 85 | 1 | 2023 | +14 € : REG PAYS-DE-LA-LOIRE (234400034), 2023 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.REC_FONCTIONNEMENT | 85 | 1 | 2023 | +14 € : REG PAYS-DE-LA-LOIRE (234400034), 2023 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.REC_INVESTISSEMENT | 85 | 1 | 2023 | −9 933 € : REG OCCITANIE (200053791), 2023 |
| ofgl.base-regions-consolidee | COMPTES_LOCAUX.REC_TOTALES_HORS_EMPRUNTS | 85 | 2 | 2023 | −9 932 € : REG OCCITANIE (200053791), 2023 |

## 8. Flux entre administrations

Ce qu'une administration déclare verser à une autre doit se retrouver dans les comptes de celle qui le reçoit. Deux flux se lisent ainsi des deux côtés : la dotation globale de fonctionnement, que l'État notifie à chaque collectivité et que celle-ci inscrit à ses comptes, et la contribution des départements aux services départementaux d'incendie et de secours (SDIS). Les comptes des communes et des groupements à fiscalité propre ne détaillent ni leurs contributions aux SDIS, ni leurs subventions aux centres d'action sociale : ces flux ne se lisent que chez qui les reçoit.

### La dotation globale de fonctionnement

L'État notifie à chaque commune, à chaque groupement à fiscalité propre et à chaque département le montant de sa dotation globale de fonctionnement, d'après les fichiers de répartition de la DGCL ; la collectivité l'inscrit à ses comptes (agrégat « Dotation globale de fonctionnement », compte 741, tous budgets). La commune se retrouve par son code Insee de l'exercice, le groupement par son numéro Siren, le département par son code ; le Bas-Rhin et le Haut-Rhin se comparent avec la Collectivité européenne d'Alsace, que les comptes codent tous 67A. La métropole de Lyon et la Ville de Paris, que deux jeux des comptes donnent, se comparent une fois, avec les deux parts de leur dotation : de groupement et de département pour la première, de commune et de département pour la seconde. La collectivité de Corse et les collectivités territoriales uniques de Martinique et de Guyane se comparent à leurs comptes du jeu des régions, les syndicats touristiques, auxquels le jeu des groupements notifie la dotation des groupements touristiques, aux leurs du jeu des syndicats. Le dernier exercice des comptes est provisoire.

Dotation notifiée : pour chaque collectivité et chaque exercice, son total égale la somme de ses parts : 328 130 identités vérifiées, 328 095 justes, 35 en écart. Dotations notifiées en parties seulement, sans total, qui ne se vérifient ni ne se comparent : COMMUNAUTE D’AGGLOMERATION DE VESOUL (70) (247000011), 2019.

| Jeu de données | Total | Parties | En écart | Plus grand écart |
|---|---|---|---|---|
| ofgl.dotations-communes | Montant Dotation DGF | Montant Dotation forfaitaire, Montant Dotation DSR | 2 sur 109 346 | −13 485 € : POMMIERS-EN-FOREZ (42) (42173), 2025 |
| ofgl.dotations-communes | Montant Dotation DGF | Montant Dotation forfaitaire, Montant Dotation DSR, Montant Dotation DNP | 2 sur 187 424 | −9 778 € : SAINT-GERMAIN-LAVAL (42) (42230), 2025 |
| ofgl.dotations-gfp | Montant DGF | Montant Dotation des groupements touristiques | 31 sur 56 | −2,6 M€ : SI DE LA GRANDE PLAGNE (73) (257300087), 2025 |

Dotation notifiée contre dotation inscrite : 290 857 comparaisons de 2018 à 2025, 259 771 égales à l'arrondi près, 31 086 en écart, dont 27 609 de 1 % ou plus.

| Niveau | Exercice | Comparaisons | Égales | En écart | dont de 1 % ou plus | Notifié | Inscrit | Écart (notifié − inscrit) |
|---|---|---|---|---|---|---|---|---|
| communes | 2018 | 35 356 | 31 304 | 4 052 | 3 660 | 11 627,8 M€ | 11 684,7 M€ | −56,9 M€ |
| communes | 2019 | 34 966 | 30 952 | 4 014 | 3 579 | 11 662,3 M€ | 11 716,5 M€ | −54,2 M€ |
| communes | 2020 | 34 968 | 31 131 | 3 837 | 3 400 | 11 712,0 M€ | 11 758,7 M€ | −46,6 M€ |
| communes | 2021 | 34 964 | 31 267 | 3 697 | 3 262 | 11 777,4 M€ | 11 821,9 M€ | −44,6 M€ |
| communes | 2022 | 34 955 | 30 404 | 4 551 | 4 136 | 11 839,2 M€ | 11 897,1 M€ | −58,0 M€ |
| communes | 2023 | 34 945 | 31 131 | 3 814 | 3 469 | 12 147,6 M€ | 12 206,4 M€ | −58,8 M€ |
| communes | 2024 | 34 932 | 31 514 | 3 418 | 3 016 | 12 390,1 M€ | 12 450,0 M€ | −59,9 M€ |
| communes | 2025 | 34 778 | 31 941 | 2 837 | 2 537 | 12 604,0 M€ | 12 645,7 M€ | −41,7 M€ |
| groupements à fiscalité propre | 2018 | 1 264 | 1 142 | 122 | 82 | 6 687,1 M€ | 6 688,7 M€ | −1,6 M€ |
| groupements à fiscalité propre | 2019 | 1 258 | 1 155 | 103 | 74 | 6 640,9 M€ | 6 619,7 M€ | +21,2 M€ |
| groupements à fiscalité propre | 2020 | 1 255 | 1 161 | 94 | 66 | 6 586,3 M€ | 6 363,6 M€ | +222,7 M€ |
| groupements à fiscalité propre | 2021 | 1 254 | 1 166 | 88 | 59 | 6 521,7 M€ | 6 512,7 M€ | +9,1 M€ |
| groupements à fiscalité propre | 2022 | 1 255 | 1 157 | 98 | 64 | 6 453,6 M€ | 6 448,7 M€ | +4,8 M€ |
| groupements à fiscalité propre | 2023 | 1 255 | 1 172 | 83 | 57 | 6 458,1 M€ | 6 457,4 M€ | +0,7 M€ |
| groupements à fiscalité propre | 2024 | 1 255 | 1 177 | 78 | 54 | 6 529,1 M€ | 6 531,3 M€ | −2,1 M€ |
| groupements à fiscalité propre | 2025 | 1 251 | 1 188 | 63 | 42 | 6 441,1 M€ | 6 440,4 M€ | +0,7 M€ |
| syndicats | 2018 | 24 | 18 | 6 | 6 | 6,4 M€ | 4,2 M€ | +2,2 M€ |
| syndicats | 2019 | 21 | 15 | 6 | 6 | 6,3 M€ | 4,0 M€ | +2,2 M€ |
| syndicats | 2020 | 20 | 15 | 5 | 5 | 6,3 M€ | 4,1 M€ | +2,2 M€ |
| syndicats | 2021 | 20 | 16 | 4 | 4 | 5,5 M€ | 4,1 M€ | +1,4 M€ |
| syndicats | 2022 | 20 | 15 | 5 | 5 | 5,5 M€ | 4,0 M€ | +1,5 M€ |
| syndicats | 2023 | 19 | 13 | 6 | 6 | 5,5 M€ | 3,8 M€ | +1,7 M€ |
| syndicats | 2024 | 19 | 13 | 6 | 6 | 5,5 M€ | 4,2 M€ | +1,3 M€ |
| syndicats | 2025 | 18 | 7 | 11 | 11 | 0,0 M€ | 4,0 M€ | −4,0 M€ |
| départements | 2018 | 96 | 85 | 11 | 0 | 8 139,3 M€ | 8 139,8 M€ | −0,5 M€ |
| départements | 2019 | 95 | 85 | 10 | 0 | 8 132,4 M€ | 8 132,8 M€ | −0,4 M€ |
| départements | 2020 | 95 | 83 | 12 | 1 | 8 035,0 M€ | 8 005,8 M€ | +29,3 M€ |
| départements | 2021 | 95 | 81 | 14 | 2 | 7 945,6 M€ | 7 975,9 M€ | −30,3 M€ |
| départements | 2022 | 95 | 85 | 10 | 0 | 7 805,7 M€ | 7 806,3 M€ | −0,7 M€ |
| départements | 2023 | 95 | 86 | 9 | 0 | 7 798,5 M€ | 7 798,9 M€ | −0,4 M€ |
| départements | 2024 | 95 | 86 | 9 | 0 | 7 797,2 M€ | 7 798,1 M€ | −0,9 M€ |
| départements | 2025 | 95 | 90 | 5 | 0 | 7 797,2 M€ | 7 797,5 M€ | −0,3 M€ |
| collectivités uniques | 2018 | 3 | 1 | 2 | 0 | 303,7 M€ | 304,3 M€ | −0,6 M€ |
| collectivités uniques | 2019 | 3 | 3 | 0 | 0 | 304,1 M€ | 304,1 M€ | +0,00 € |
| collectivités uniques | 2020 | 3 | 3 | 0 | 0 | 303,8 M€ | 303,8 M€ | +0,00 € |
| collectivités uniques | 2021 | 3 | 1 | 2 | 0 | 304,3 M€ | 304,9 M€ | −0,5 M€ |
| collectivités uniques | 2022 | 3 | 2 | 1 | 0 | 304,2 M€ | 304,3 M€ | −14 108 € |
| collectivités uniques | 2023 | 3 | 1 | 2 | 0 | 304,1 M€ | 304,1 M€ | −40 068 € |
| collectivités uniques | 2024 | 3 | 2 | 1 | 0 | 304,0 M€ | 304,0 M€ | −0,1 M€ |
| collectivités uniques | 2025 | 3 | 3 | 0 | 0 | 303,7 M€ | 303,7 M€ | +0,00 € |

Les 20 plus grands écarts :

| Collectivité | Niveau | Exercice | Notifié | Inscrit | Écart (notifié − inscrit) |
|---|---|---|---|---|---|
| MET MEL (245900410) | groupements à fiscalité propre | 2020 | 216,4 M€ | 0,0 M€ | +216,4 M€ (+100,0 %) |
| DEP REUNION (974) | départements | 2020 | 241,2 M€ | 211,5 M€ | +29,7 M€ (+12,3 %) |
| DEP REUNION (974) | départements | 2021 | 184,6 M€ | 214,3 M€ | −29,7 M€ (−13,8 %) |
| CA DU CALAISIS (246201149) | groupements à fiscalité propre | 2019 | 10,2 M€ | 0,0 M€ | +10,2 M€ (+100,0 %) |
| CU LE HAVRE SEINE METROPOLE (200084952) | groupements à fiscalité propre | 2019 | 26,9 M€ | 36,3 M€ | −9,4 M€ (−25,8 %) |
| CA ST GERMAIN BOUCLES DE SEINE (200058519) | groupements à fiscalité propre | 2019 | 31,3 M€ | 23,2 M€ | +8,1 M€ (+25,8 %) |
| CA SEINE EURE - EX (200035665) | groupements à fiscalité propre | 2019 | 6,6 M€ | 0,0 M€ | +6,6 M€ (+100,0 %) |
| CA DU SICOVAL (243100633) | groupements à fiscalité propre | 2018 | 7,1 M€ | 0,8 M€ | +6,3 M€ (+88,9 %) |
| CA DU SICOVAL (243100633) | groupements à fiscalité propre | 2019 | 7,0 M€ | 0,9 M€ | +6,2 M€ (+87,5 %) |
| CA DU SICOVAL (243100633) | groupements à fiscalité propre | 2020 | 7,0 M€ | 1,0 M€ | +6,1 M€ (+86,0 %) |
| CA DU SICOVAL (243100633) | groupements à fiscalité propre | 2021 | 7,0 M€ | 1,1 M€ | +5,9 M€ (+84,3 %) |
| CA DU SICOVAL (243100633) | groupements à fiscalité propre | 2022 | 7,0 M€ | 1,2 M€ | +5,8 M€ (+82,5 %) |
| TSINGONI (200008886) | communes | 2023 | 4,4 M€ | 9,3 M€ | −4,9 M€ (−53,0 %) |
| NOISY-LE-SEC (219300530) | communes | 2018 | 12,8 M€ | 17,1 M€ | −4,3 M€ (−25,0 %) |
| NOISY-LE-SEC (219300530) | communes | 2019 | 12,9 M€ | 17,2 M€ | −4,2 M€ (−24,6 %) |
| EPINAY-SUR-SEINE (219300316) | communes | 2019 | 23,8 M€ | 27,2 M€ | −3,4 M€ (−12,5 %) |
| EPINAY-SUR-SEINE (219300316) | communes | 2018 | 23,0 M€ | 26,3 M€ | −3,3 M€ (−12,4 %) |
| SEGRE EN ANJOU BLEU (200065423) | communes | 2024 | 4,4 M€ | 7,4 M€ | −3,0 M€ (−40,7 %) |
| SIVU GRANDE PLAGNE (257300087) | syndicats | 2025 | 0,0 M€ | 2,6 M€ | −2,6 M€ (−100,0 %) |
| AUBERVILLIERS (219300019) | communes | 2022 | 30,5 M€ | 33,0 M€ | −2,6 M€ (−7,7 %) |

Dotations notifiées à des collectivités qui n'ont pas de comptes dans ces jeux, comme les communes et les collectivités d'outre-mer hors du champ des balances comptables de la DGFiP (Saint-Pierre-et-Miquelon, Saint-Martin, Wallis-et-Futuna, Polynésie française…) :

| Jeu des dotations | Exercices | Collectivités au dernier exercice | Notifié au dernier exercice | Les plus grandes au dernier exercice |
|---|---|---|---|---|
| ofgl.dotations-communes | 8 années entre 2018 et 2025 | 183 | 201,5 M€ | NOUMEA (988) (98818), PAPEETE (987) (98735), FAAA (987) (98715) |
| ofgl.dotations-departements | 8 années entre 2018 et 2025 | 2 | 15,7 M€ | SAINT-MARTIN (978), ST PIERRE ET MIQUELON (975) |
| ofgl.dotations-gfp | 8 années entre 2018 et 2025 | 20 | 16,8 M€ | CA D’EPINAL (88) (200068757), CC TEREHEAMANU (987) (200094803), CC DE HAVA’I (987) (200031243) |

Dotations inscrites aux comptes de collectivités auxquelles les fichiers de répartition ne notifient rien :

| Niveau | Exercices | Collectivités au dernier exercice | Inscrit au dernier exercice | Les plus grandes au dernier exercice |
|---|---|---|---|---|
| communes | 2021 | 1 | 0,2 M€ | LES TROIS-LACS (200063782) |
| groupements à fiscalité propre | 8 années entre 2018 et 2025 | 1 | 0,0 M€ | GRAND-ORLY SEINE BIEVRE (200058014) |
| syndicats | 8 années entre 2018 et 2025 | 32 | 10,4 M€ | SMICTOM OUEST AUDOIS (251100236), SYNDMC BASSIN VERSANT GAPEAU (200046795), EAUX PLUVIALES URB - SICTEUB (200091924) |
| collectivités uniques | 8 années entre 2018 et 2025 | 2 | 0,1 M€ | REG HAUTS DE FRANCE (200053742), REG NOUVELLE AQUITAINE (200053759) |

### Les contributions des départements aux SDIS

Les départements publient leur contribution aux SDIS sous l'agrégat « Contributions aux SDIS », que les SDIS comptent parmi les participations qu'ils reçoivent. Chaque département se compare au SDIS de son territoire : sa contribution, tous budgets, contre les participations des départements que le SDIS inscrit à son budget principal. Le Bas-Rhin, le Haut-Rhin puis la Collectivité européenne d'Alsace, que le jeu des départements désigne tous par le code 67A, se comparent aux SDIS du Bas-Rhin et du Haut-Rhin ensemble, comme la collectivité de Corse, depuis 2018, à ceux de Corse-du-Sud et de Haute-Corse. Le SDIS du Rhône inscrit la contribution de la métropole de Lyon, depuis 2015, et ceux de Martinique et de Guyane celle de leur collectivité territoriale unique, depuis 2016, parmi les autres participations, puis parmi celles des groupements à fiscalité propre : la métropole se compare à ces deux rubriques, chaque collectivité territoriale unique à ces deux rubriques et aux participations des départements, que le SDIS de Martinique emploie en 2016 ; ces rubriques peuvent compter d'autres participations que la sienne. Le dernier exercice est provisoire.

1 335 comparaisons de 2012 à 2025 : 1 024 égales à l'arrondi près, 311 en écart, dont 170 de 1 % ou plus.

| Exercice | Comparaisons | Égales | En écart | dont de 1 % ou plus | Versé | Reçu | Écart (versé − reçu) |
|---|---|---|---|---|---|---|---|
| 2012 | 93 | 72 | 21 | 9 | 2 386,6 M€ | 2 391,6 M€ | −5,0 M€ |
| 2013 | 94 | 71 | 23 | 11 | 2 427,4 M€ | 2 436,3 M€ | −8,9 M€ |
| 2014 | 94 | 73 | 21 | 8 | 2 464,7 M€ | 2 472,1 M€ | −7,4 M€ |
| 2015 | 95 | 75 | 20 | 9 | 2 530,1 M€ | 2 536,1 M€ | −6,0 M€ |
| 2016 | 96 | 79 | 17 | 10 | 2 559,9 M€ | 2 557,2 M€ | +2,6 M€ |
| 2017 | 96 | 77 | 19 | 12 | 2 573,2 M€ | 2 571,4 M€ | +1,7 M€ |
| 2018 | 95 | 74 | 21 | 10 | 2 590,3 M€ | 2 592,1 M€ | −1,8 M€ |
| 2019 | 96 | 77 | 19 | 10 | 2 629,4 M€ | 2 624,6 M€ | +4,8 M€ |
| 2020 | 96 | 76 | 20 | 12 | 2 685,7 M€ | 2 682,6 M€ | +3,0 M€ |
| 2021 | 96 | 69 | 27 | 16 | 2 750,4 M€ | 2 753,2 M€ | −2,7 M€ |
| 2022 | 96 | 70 | 26 | 20 | 2 867,0 M€ | 2 873,9 M€ | −6,8 M€ |
| 2023 | 96 | 71 | 25 | 16 | 3 008,4 M€ | 3 009,6 M€ | −1,2 M€ |
| 2024 | 96 | 69 | 27 | 14 | 3 128,5 M€ | 3 136,7 M€ | −8,2 M€ |
| 2025 | 96 | 71 | 25 | 13 | 3 216,7 M€ | 3 224,3 M€ | −7,6 M€ |

Comparaisons en écart, territoire par territoire, sous le nom le plus récent de chacun :

| Collectivité | SDIS | Exercices en écart | dont de 1 % ou plus | Plus grand écart (versé − reçu) |
|---|---|---|---|---|
| DEP AIN | SDIS AIN | 2024 et 2025 | aucun | −0,1 M€ en 2025 (−0,2 %) |
| DEP ALLIER | SDIS ALLIER | 2024 et 2025 | 2024 et 2025 | −0,3 M€ en 2024 (−1,3 %) |
| DEP ALPES-DE-HAUTE-PROVENCE | SDIS ALPES-DE-HAUTE-PROVENCE | 6 années entre 2012 et 2017 | 6 années entre 2012 et 2017 | −1,8 M€ en 2012 (−22,2 %) |
| DEP DES HAUTES-ALPES | SDIS HAUTES-ALPES | 7 années entre 2012 et 2025 | aucun | −24 000 € en 2012 (−0,4 %) |
| DEP ARDECHE | SDIS ARDECHE | 7 années entre 2019 et 2025 | 2019, 2022 et 2025 | −2,1 M€ en 2022 (−10,4 %) |
| DEP ARIEGE | SDIS ARIEGE | 2024 | aucun | −780 € en 2024 (moins de 0,1 %) |
| DEP AUBE | SDIS AUBE | 2012, 2014 et 2015 | 2012 | +0,4 M€ en 2012 (+8,4 %) |
| DEP AUDE | SDIS AUDE | 14 années entre 2012 et 2025 | 14 années entre 2012 et 2025 | −1,2 M€ en 2020 (−7,5 %) |
| DEP BOUCHES-DU-RHONE | SDIS BOUCHES-DU-RHONE | 14 années entre 2012 et 2025 | 14 années entre 2012 et 2025 | +10,0 M€ en 2021 (+12,7 %) |
| DEP CHARENTE | SDIS CHARENTE | 2025 | aucun | −155 € en 2025 (moins de 0,1 %) |
| DEP CHARENTE-MARITIME | SDIS CHARENTE-MARITIME | 2023 | aucun | −0,1 M€ en 2023 (−0,3 %) |
| DEP CORREZE | SDIS DEP-CORREZE | 2018, 2019, 2020 et 2021 | 2018, 2019, 2020 et 2021 | −0,2 M€ en 2018 (−2,6 %) |
| DEP CREUSE | SDIS CREUSE | 5 années entre 2019 et 2023 | 2021, 2022 et 2023 | −0,1 M€ en 2023 (−1,5 %) |
| DEP DORDOGNE | SDIS DORDOGNE | 13 années entre 2013 et 2025 | 7 années entre 2019 et 2025 | −0,4 M€ en 2025 (−1,8 %) |
| DEP EURE | SDIS DE L' EURE | 2012 et 2013 | 2013 | −1,8 M€ en 2013 (−7,7 %) |
| DEP FINISTERE | SDIS FINISTERE | 2022, 2023 et 2024 | 2022, 2023 et 2024 | +1,6 M€ en 2022 (+6,0 %) |
| DEP CORSE-DU-SUD | SDIS CORSE-DU-SUD | 2016 et 2017 | 2016 et 2017 | −1,1 M€ en 2016 (−5,3 %) |
| COLLECTIVITE DE CORSE | SDIS CORSE-DU-SUD et SDIS HAUTE-CORSE | 2021 et 2022 | 2021 et 2022 | +1,2 M€ en 2021 (+2,6 %) |
| DEP HAUTE-CORSE | SDIS HAUTE-CORSE | 2014 | aucun | −19 000 € en 2014 (−0,1 %) |
| DEP GARD | SDIS GARD | 2020 et 2022 | 2020 et 2022 | −3,0 M€ en 2020 (−6,5 %) |
| DEP GERS | SDIS GERS | 2018 et 2025 | 2025 | −0,1 M€ en 2025 (−1,2 %) |
| DEP GIRONDE | SDIS GIRONDE | 2015 | aucun | +50 € en 2015 (moins de 0,1 %) |
| DEP HERAULT | SDIS HERAULT | 2018 et 2019 | aucun | −0,1 M€ en 2019 (−0,2 %) |
| DEP ILLE-ET-VILAINE | SDIS ILLE-ET-VILAINE | 2012 et 2013 | 2012 et 2013 | −1,0 M€ en 2012 (−3,3 %) |
| DEP JURA | SDIS JURA | 14 années entre 2012 et 2025 | 12 années entre 2012 et 2023 | +0,5 M€ en 2014 (+7,1 %) |
| DEP DES LANDES | SDIS LANDES | 14 années entre 2012 et 2025 | 2022 et 2023 | −1,7 M€ en 2022 (−7,1 %) |
| DEP LOIR-ET-CHER | SDIS LOIR-ET-CHER | 2024 et 2025 | aucun | −3 150 € en 2025 (moins de 0,1 %) |
| DEP LOIRE | SDIS LOIRE | 2013 | aucun | +435 € en 2013 (moins de 0,1 %) |
| DEP LOIRE-ATLANTIQUE | SDIS LOIRE-ATLANTIQUE | 8 années entre 2015 et 2024 | aucun | −0,1 M€ en 2018 (−0,2 %) |
| DEP LOIRET | SDIS LOIRET | 2021 | 2021 | −1,5 M€ en 2021 (−6,9 %) |
| DEP LOT | SDIS LOT | 13 années entre 2012 et 2025 | 5 années entre 2012 et 2016 | +0,2 M€ en 2013 (+3,7 %) |
| DEP LOZERE | SDIS LOZERE | 7 années entre 2012 et 2025 | aucun | −14 466 € en 2012 (−0,4 %) |
| DEP MANCHE | SDIS MANCHE | 2023 et 2024 | 2023 et 2024 | −0,3 M€ en 2023 (−1,7 %) |
| DEP HAUTE-MARNE | SDIS HAUTE-MARNE | 2012, 2013, 2014 et 2023 | 2023 | −1,0 M€ en 2023 (−10,9 %) |
| DEP MAYENNE | SDIS MAYENNE | 14 années entre 2012 et 2025 | aucun | −48 030 € en 2019 (−0,5 %) |
| DEP MOSELLE | SDIS MOSELLE | 2012, 2013 et 2024 | aucun | −0,1 M€ en 2012 (−0,2 %) |
| DEP PAS-DE-CALAIS | SDIS PAS-DE-CALAIS | 7 années entre 2012 et 2018 | 6 années entre 2013 et 2018 | −1,9 M€ en 2015 (−2,6 %) |
| DEP HAUTES-PYRENEES | SDIS HAUTES-PYRENEES | 6 années entre 2013 et 2018 | 2015, 2016 et 2017 | +0,4 M€ en 2015 (+3,8 %) |
| COLLECTIVITE EUROPEENNE D'ALSACE | SIS BAS-RHIN et SIS HAUT-RHIN | 2019, 2021 et 2023 | aucun | −41 010 € en 2021 (−0,1 %) |
| MET DE LYON | SDMIS RHONE METROPOLE LYON | 11 années entre 2015 et 2025 | 5 années entre 2020 et 2025 | −6,2 M€ en 2021 (−5,0 %) |
| DEP HAUTE-SAONE | SDIS HAUTE-SAONE | 2012 | aucun | −2 058 € en 2012 (moins de 0,1 %) |
| DEP SAONE-ET-LOIRE | SDIS SAONE-ET-LOIRE | 14 années entre 2012 et 2025 | 14 années entre 2012 et 2025 | −0,5 M€ en 2013 (−3,3 %) |
| DEP SARTHE | SDIS SARTHE | 2012 et 2013 | 2012 et 2013 | +0,7 M€ en 2012 (+4,1 %) |
| DEP SAVOIE | SDIS SAVOIE | 8 années entre 2012 et 2025 | aucun | −40 251 € en 2022 (−0,1 %) |
| DEP HAUTE-SAVOIE | SDIS HAUTE-SAVOIE | 2023, 2024 et 2025 | 2023, 2024 et 2025 | −12,0 M€ en 2025 (−19,0 %) |
| DEP DEUX-SEVRES | SDIS DEUX-SEVRES | 6 années entre 2013 et 2025 | 2022 et 2023 | +0,3 M€ en 2022 (+1,9 %) |
| DEP SOMME | SDIS SOMME | 2012, 2020 et 2021 | aucun | +0,1 M€ en 2012 (+0,2 %) |
| DEP VAR | SDIS VAR | 2017 | 2017 | +1,0 M€ en 2017 (+2,0 %) |
| DEP VAUCLUSE | SDIS VAUCLUSE | 7 années entre 2017 et 2025 | 6 années entre 2018 et 2025 | −2,5 M€ en 2024 (−6,6 %) |
| DEP VIENNE | SDIS VIENNE | 9 années entre 2015 et 2025 | 9 années entre 2015 et 2025 | −0,5 M€ en 2017 (−4,0 %) |
| DEP YONNE | SDIS YONNE | 2014 et 2015 | aucun | −180 € en 2014 (moins de 0,1 %) |
| DEP TERRITOIRE-BELFORT | SDIS TERR-BELFORT | 9 années entre 2017 et 2025 | 9 années entre 2017 et 2025 | −0,1 M€ en 2021 (−1,6 %) |
| DEP ESSONNE | SDIS ESSONNE | 14 années entre 2012 et 2025 | aucun | +0,6 M€ en 2020 (+0,7 %) |
| DEP GUADELOUPE | SDIS GUADELOUPE | 5 années entre 2020 et 2024 | 5 années entre 2020 et 2024 | −1,5 M€ en 2024 (−5,5 %) |
| DEP MARTINIQUE | SDIS MARTINIQUE | 2014 et 2015 | aucun | −0,1 M€ en 2015 (−0,5 %) |
| CTU MARTINIQUE | SDIS MARTINIQUE | 10 années entre 2016 et 2025 | 10 années entre 2016 et 2025 | −4,5 M€ en 2018 (−25,0 %) |
| DEP GUYANE | SDIS GUYANE | 2013 et 2014 | 2013 et 2014 | −0,9 M€ en 2014 (−9,6 %) |
| CTU Guyane | SDIS GUYANE | 2021 et 2022 | 2021 et 2022 | −0,9 M€ en 2021 (−5,2 %) |
| DEP MAYOTTE | SDIS MAYOTTE | 2020 et 2022 | 2022 | −0,1 M€ en 2022 (−1,2 %) |

Contributions sans SDIS à qui les comparer. Paris et les départements de la petite couronne n'ont pas de SDIS : la brigade de sapeurs-pompiers de Paris, unité militaire, y tient ce rôle, et ses comptes ne figurent pas dans ces jeux ; aucune contribution n'est publiée sous cet agrégat pour DEP HAUTS-DE-SEINE (229200506).

| Collectivité | Exercices | Contribution au dernier exercice |
|---|---|---|
| DEP DU VAL-DE-MARNE (229400288) | 14 années entre 2012 et 2025 | 41,7 M€ en 2025 |
| DEP SEINE-SAINT-DENIS (229300082) | 10 années entre 2016 et 2025 | 49,3 M€ en 2025 |
| VILLE DE PARIS (217500016) | 7 années entre 2019 et 2025 | 112,0 M€ en 2025 |

Participations des départements qu'un SDIS déclare recevoir sans que son département publie de contribution sous cet agrégat :

| SDIS | Exercices | Plus grande participation |
|---|---|---|
| SDIS ARDECHE | 7 années entre 2012 et 2018 | 17,5 M€ en 2015 |
| SDIS HAUTES-PYRENEES | 2012 | 10,0 M€ en 2012 |
| SDIS MAYOTTE | 2012, 2013, 2014 et 2015 | 13,7 M€ en 2014 |

## 9. Dépenses de chaque département par fonction

La présentation fonctionnelle des comptes des départements, que l'OFGL publie sur data.ofgl.fr, ventile les dépenses de chaque budget des départements, de la métropole de Lyon et de la Ville de Paris entre les fonctions de la nomenclature de son instruction budgétaire et comptable : la M52, puis la M57, que les départements adoptent l'un après l'autre et dont les fonctions ne se correspondent pas toutes ; le jeu ne porte que sur les dépenses. Chaque montant y figure à chacun des niveaux de sa fonction, d'un à quatre chiffres, et un montant nul n'a pas de ligne : une fonction doit valoir la somme de ses sous-fonctions, et les fonctions de premier niveau réunies, le total du budget. Dans chaque fonction s'appliquent les identités comptables des agrégats de dépenses, une partie sans ligne valant zéro. La somme des fonctions de premier niveau du budget principal de chaque collectivité se compare au montant de son budget principal dans le jeu de ses comptes consolidés, celle de ses budgets annexes réunis au montant de ses budgets annexes. Le dernier exercice est provisoire.

| Exercice | Version | Statut | Budgets principaux en M52 | Budgets principaux en M57 | Budgets annexes | Lignes |
|---|---|---|---|---|---|---|
| 2012 | 2026-08-05 | definitif | 101 | 0 | 80 | 59 245 |
| 2013 | 2026-08-05 | definitif | 101 | 0 | 90 | 59 367 |
| 2014 | 2026-08-05 | definitif | 100 | 1 | 120 | 59 571 |
| 2015 | 2026-08-05 | definitif | 100 | 2 | 123 | 60 137 |
| 2016 | 2026-08-05 | definitif | 99 | 1 | 133 | 58 342 |
| 2017 | 2026-08-05 | definitif | 99 | 1 | 129 | 59 013 |
| 2018 | 2026-08-05 | definitif | 96 | 2 | 123 | 57 214 |
| 2019 | 2026-08-05 | definitif | 90 | 8 | 148 | 60 819 |
| 2020 | 2026-08-05 | definitif | 89 | 9 | 151 | 60 762 |
| 2021 | 2026-08-05 | definitif | 78 | 19 | 140 | 61 496 |
| 2022 | 2026-08-05 | definitif | 68 | 29 | 142 | 63 147 |
| 2023 | 2026-08-05 | definitif | 49 | 48 | 139 | 65 005 |
| 2024 | 2026-08-05 | definitif | 2 | 95 | 135 | 71 269 |
| 2025 | 2026-08-05 | provisoire | 2 | 95 | 139 | 70 348 |

Fonctions comparées à la somme de leurs sous-fonctions, pour chaque budget et chaque agrégat : 326 246, dont 325 168 égales à l'arrondi près et 1 078 en écart. Un écart peut venir d'un montant que le budget classe dans la fonction sans le ventiler entre ses sous-fonctions : il se retrouve alors dans chacun des agrégats qui comptent ce montant.

| Fonction | Exercices en écart | Budgets en écart, chaque exercice compté | Plus grand écart (fonction − sous-fonctions) |
|---|---|---|---|
| 0 de la M52 (SERVICES GÉNÉRAUX) | 8 années entre 2012 et 2019 | 22 | +2,1 M€ (DEP_FONCTIONNEMENT) : VOSGES DEVELOPPEMENT-DEP VOSGES (22880001700250), 2013 |
| 02 de la M52 (Administration générale) | 10 années entre 2013 et 2022 | 21 | +29,2 M€ (DEP_FONCTIONNEMENT) : DEP MAYOTTE (22985000300018), 2016 |
| 020 de la M52 (Administration générale de la collectivité) | 11 années entre 2012 et 2022 | 21 | −2,5 M€ (DEP_FONCTIONNEMENT) : DEP MAYOTTE (22985000300018), 2013 |
| 04 de la M52 (Coopération décentralisée, action européenne et internationale) | 11 années entre 2012 et 2023 | 24 | +0,6 M€ (DEP_FONCTIONNEMENT) : DEP MAYOTTE (22985000300018), 2017 |
| 1 de la M52 (Sécurité) | 5 années entre 2012 et 2018 | 13 | +6,2 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP YVELINES (22780646000019), 2012 |
| 2 de la M52 (Enseignement) | 5 années entre 2012 et 2023 | 8 | +0,2 M€ (DEP_INVESTISSEMENT) : DEP PYRENEES-ATLANTIQUES (22640001800876), 2023 |
| 22 de la M52 (Enseignement du second degré) | 9 années entre 2014 et 2023 | 9 | +0,2 M€ (DEPENSES_EQUIPEMENT) : DEP DEUX-SEVRES (22790001600352), 2020 |
| 3 de la M52 (Culture, vie sociale, jeunesse, sports et loisirs) | 2012, 2016 et 2023 | 3 | +0,4 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP LOIRE (22420001400013), 2016 |
| 31 de la M52 (Culture) | 8 années entre 2013 et 2023 | 14 | +4,7 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP MAYOTTE (22985000300018), 2017 |
| 4 de la M52 (Prévention médico-sociale) | 2013, 2015, 2016 et 2019 | 6 | +7 261 € (DEP_FONCTIONNEMENT) : DEP DU LOIRET (22450001700013), 2013 |
| 5 de la M52 (Action sociale) | 12 années entre 2012 et 2023 | 13 | +0,1 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP DU VAL-DE-MARNE (22940028800010), 2012 |
| 53 de la M52 (Personnes âgées) | 2017 | 47 | +58,0 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP VAR (22830001800113), 2017 |
| 54 de la M52 (Revenu minimum d'insertion) | 2012, 2016 et 2017 | 4 | +3,3 M€ (DEP_FONCTIONNEMENT) : DEP MAYOTTE (22985000300018), 2016 |
| 547 de la M52 (Revenu minimum d'insertion - Revenu minimum d'activité) | 8 années entre 2012 et 2019 | 12 | +0,1 M€ (DEPENSES_INTERVENTION) : DEP OISE (22600001600403), 2016 |
| 55 de la M52 (Personnes dépendantes (APA)) | 2015 | 1 | +19 336 € (DEPENSES_INTERVENTION) : DEP NIEVRE (22580001000012), 2015 |
| 56 de la M52 (Revenu de solidarité active) | 2014 et 2019 | 2 | +0,1 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP ARDENNES (22080004900011), 2014 |
| 6 de la M52 (Réseaux et infrastructures) | 9 années entre 2012 et 2020 | 26 | +6,3 M€ (DEPENSES_INTERVENTION) : DEP MAYOTTE (22985000300018), 2016 |
| 62 de la M52 (Routes et voirie) | 11 années entre 2012 et 2023 | 27 | +1,9 M€ (DEP_INVESTISSEMENT) : DEP BOUCHES-DU-RHONE (22130001500247), 2012 |
| 7 de la M52 (Aménagement et environnement) | 2015 | 1 | +356 € (DEPENSES_INTERVENTION) : DEP CHER (22180001400013), 2015 |
| 73 de la M52 (Environnement) | 5 années entre 2016 et 2023 | 11 | +7,2 M€ (DEP_FONCTIONNEMENT) : DEP MAYOTTE (22985000300018), 2016 |
| 8 de la M52 (Transports) | 2013 et 2015 | 2 | +3 158 € (DEPENSES_INTERVENTION) : TRANSPORTS SCOLAIRES (22570001200209), 2015 |
| 82 de la M52 (Transports publics de voyageurs) | 6 années entre 2013 et 2019 | 12 | +0,8 M€ (DEP_TOTALES_HORS_REMBOURSEMENTS) : DEP COTES-D'ARMOR (22220001600327), 2017 |
| 9 de la M52 (Développement économique) | 2012 | 1 | +3 100 € (DEPENSES_INTERVENTION) : DEP ISERE (22380001200013), 2012 |
| 92 de la M52 (Agriculture et pêche) | 6 années entre 2012 et 2019 | 8 | +6,1 M€ (FRAIS_PERSONNEL) : DEP MAYOTTE (22985000300018), 2018 |
| 20 de la M57 (Services communs) | 2021, 2023 et 2024 | 7 | +3,8 M€ (DEP_FONCTIONNEMENT) : DEP SEINE-MARITIME (22760540900019), 2021 |
| 25 de la M57 (Formation professionnelle) | 2024 et 2025 | 2 | +18 498 € (ACHATS_CHARGES_EXTERNES) : DEP HAUTES-PYRENEES (22650001500012), 2025 |
| 50 de la M57 (Services communs) | 2021, 2022, 2023 et 2024 | 15 | +16,0 M€ (DEP_FONCTIONNEMENT) : DEP VAUCLUSE (22840001600017), 2021 |

Identités comptables dans chaque fonction de chaque budget : 342 175 vérifiées, 342 175 justes, 0 en écart.

| Total | Parties | Vérifiées | En écart | Plus grand écart |
|---|---|---|---|---|
| DEP_FONCTIONNEMENT | ACHATS_CHARGES_EXTERNES, FRAIS_PERSONNEL, CHARGES_FINANCIERES, DEPENSES_INTERVENTION, AUTRES_DEP_FONCTIONNEMENT | 127 075 | 0 | aucun |
| DEP_INVESTISSEMENT | DEPENSES_EQUIPEMENT, SUBVENTIONS_EQUIPEMENT_VERSEES, AUTRES_DEP_INVESTISSEMENT | 81 324 | 0 | aucun |
| DEP_TOTALES_HORS_REMBOURSEMENTS | DEP_FONCTIONNEMENT, DEP_INVESTISSEMENT | 133 776 | 0 | aucun |

Fonctions de premier niveau du budget principal de chaque collectivité, réunies, contre le montant de son budget principal dans ses comptes consolidés : 23 460 comparaisons, 23 445 égales à l'arrondi près, 15 en écart.

| Collectivité | Agrégat | Exercices en écart | Plus grand écart (fonctions − comptes consolidés) |
|---|---|---|---|
| DEP EURE (222702292) | AUTRES_DEP_FONCTIONNEMENT | 2023 et 2025 | +2 362 € en 2023 |
| DEP EURE (222702292) | DEP_FONCTIONNEMENT | 2023 et 2025 | +2 362 € en 2023 |
| DEP EURE (222702292) | DEP_TOTALES_HORS_REMBOURSEMENTS | 2023 et 2025 | +2 362 € en 2023 |
| DEP LOT-ET-GARONNE (224700013) | DEPENSES_EQUIPEMENT | 2025 | +0,1 M€ en 2025 |
| DEP LOT-ET-GARONNE (224700013) | DEP_INVESTISSEMENT | 2025 | +0,1 M€ en 2025 |
| DEP LOT-ET-GARONNE (224700013) | DEP_TOTALES_HORS_REMBOURSEMENTS | 2025 | +0,1 M€ en 2025 |
| DEP MEURTHE-ET-MOSELLE (225400019) | DEPENSES_EQUIPEMENT | 2013 | +0,4 M€ en 2013 |
| DEP MEURTHE-ET-MOSELLE (225400019) | DEP_INVESTISSEMENT | 2013 | +0,4 M€ en 2013 |
| DEP MEURTHE-ET-MOSELLE (225400019) | DEP_TOTALES_HORS_REMBOURSEMENTS | 2013 | +0,4 M€ en 2013 |
| DEP RHONE (226900017) | AUTRES_DEP_FONCTIONNEMENT | 2023 | +820 € en 2023 |
| DEP RHONE (226900017) | DEP_FONCTIONNEMENT | 2023 | +820 € en 2023 |
| DEP RHONE (226900017) | DEP_TOTALES_HORS_REMBOURSEMENTS | 2023 | +820 € en 2023 |

Budgets annexes : le jeu fonctionnel ne donne que des budgets tenus selon la M52 ou la M57, et un budget annexe tenu selon une autre instruction n'y figure pas. Une collectivité dont tous les budgets annexes y figurent retrouve, pour chaque agrégat, le montant de ses budgets annexes dans ses comptes consolidés ; les autres y ont un montant moindre.

| Exercice | Collectivités qui ont des budgets annexes | dont budgets annexes tous présentés par fonction | Dépenses totales hors remboursements des budgets annexes : par fonction | dans les comptes consolidés |
|---|---|---|---|---|
| 2012 | 99 | 8 | 312,4 M€ | 1 923,2 M€ |
| 2013 | 99 | 9 | 319,7 M€ | 1 870,0 M€ |
| 2014 | 99 | 11 | 398,8 M€ | 1 862,3 M€ |
| 2015 | 100 | 10 | 394,4 M€ | 2 071,6 M€ |
| 2016 | 97 | 12 | 408,2 M€ | 2 068,1 M€ |
| 2017 | 97 | 13 | 333,0 M€ | 1 868,9 M€ |
| 2018 | 94 | 11 | 342,7 M€ | 1 629,0 M€ |
| 2019 | 96 | 13 | 519,8 M€ | 2 119,8 M€ |
| 2020 | 96 | 12 | 681,5 M€ | 2 200,7 M€ |
| 2021 | 95 | 13 | 718,3 M€ | 2 307,3 M€ |
| 2022 | 94 | 14 | 814,2 M€ | 2 425,7 M€ |
| 2023 | 93 | 14 | 913,0 M€ | 2 558,7 M€ |
| 2024 | 92 | 13 | 906,5 M€ | 2 652,4 M€ |
| 2025 | 91 | 12 | 943,8 M€ | 2 595,4 M€ |

Budgets annexes dont les fonctions réunies dépassent le montant des comptes consolidés, ce que l'absence d'un budget n'explique pas, sauf pour un agrégat qu'un montant négatif réduit :

| Collectivité | Agrégat | Exercices | Plus grand écart (fonctions − comptes consolidés) |
|---|---|---|---|
| DEP CANTAL (221500010) | ACHATS_CHARGES_EXTERNES | 2015 | +1,2 M€ en 2015 |
| DEP CANTAL (221500010) | AUTRES_DEP_FONCTIONNEMENT | 2015 | +3 585 € en 2015 |
| DEP CANTAL (221500010) | DEP_FONCTIONNEMENT | 2015 | +2,7 M€ en 2015 |
| DEP CANTAL (221500010) | DEP_TOTALES_HORS_REMBOURSEMENTS | 2015 | +2,7 M€ en 2015 |
| DEP CANTAL (221500010) | FRAIS_PERSONNEL | 2015 | +1,5 M€ en 2015 |
| DEP FINISTERE (222900011) | DEPENSES_EQUIPEMENT | 2014 | +0,1 M€ en 2014 |
| DEP FINISTERE (222900011) | DEP_INVESTISSEMENT | 2014 | +0,1 M€ en 2014 |
| DEP ILLE-ET-VILAINE (223500018) | AUTRES_DEP_FONCTIONNEMENT | 2012 | +0,1 M€ en 2012 |
| DEP MARNE (225100015) | CHARGES_FINANCIERES | 2015 | +0,1 M€ en 2015 |
| DEP MOSELLE (225700012) | ACHATS_CHARGES_EXTERNES | 2014 | +0,1 M€ en 2014 |
| DEP MOSELLE (225700012) | DEPENSES_INTERVENTION | 2014 | +2,4 M€ en 2014 |
| DEP MOSELLE (225700012) | DEP_FONCTIONNEMENT | 2014 | +2,5 M€ en 2014 |
| DEP MOSELLE (225700012) | DEP_TOTALES_HORS_REMBOURSEMENTS | 2014 | +2,5 M€ en 2014 |
| DEP SAONE-ET-LOIRE (227100013) | CHARGES_FINANCIERES | 2016 | +0,1 M€ en 2016 |

Fonctions dont le libellé change d'un exercice à l'autre, ou d'un budget à l'autre dans un même exercice : une même fonction peut ne pas désigner les mêmes dépenses d'une année à l'autre.

| Nomenclature | Fonction | Libellés (exercices) |
|---|---|---|
| M57 | 11 | Gendarmerie, police, sécurité, justice (2016 et 2017) ; Police, sécurité, justice (8 années entre 2018 et 2025) |
| M57 | 33 | Jeunesse (action socio-éducative…) et loisirs (11 années entre 2014 et 2025) ; Jeunesse (action socio-éducative.) et loisirs (2022) |
| M57 | 4213 | Crèches et garderies (2015 et 2017) ; Aides sociales à l'enfance (8 années entre 2018 et 2025) |
| M57 | 422 | Personnes handicapées (2014, 2015, 2016 et 2017) ; Petite enfance (7 années entre 2019 et 2025) |
| M57 | 4238 | Autres (2017) ; Autres actions en faveur des personnes âgées (8 années entre 2018 et 2025) |
| M57 | 588 | Autres (2014 et 2015) ; Autres actions d'aménagement (7 années entre 2019 et 2025) |
| M57 | 6312 | Autres (11 années entre 2014 et 2024) ; Marchés alimentaires (2025) |

Regroupements que le portail fait, pour ses visualisations, de fonctions des deux nomenclatures, les autres fonctions étant rangées sous « Autres » : « 221-Collèges » : 221 de la M52, 221 de la M57 ; « 62-Voirie » : 62 de la M52, 84 de la M57.

## 10. Fiscalité directe locale

Le fichier de recensement des éléments d'imposition à la fiscalité directe locale (REI) de la DGFiP, que l'OFGL publie sous une forme simplifiée, donne pour le territoire de chaque commune la base, le taux et le produit des taxes foncières sur les propriétés bâties (TFPB) et non bâties (TFPNB), de la taxe d'enlèvement des ordures ménagères (TEOM) et de la cotisation foncière des entreprises (CFE), pour chacun de leurs bénéficiaires : ce sont les impositions primitives de l'année, sans les rôles supplémentaires. Le produit d'une ligne se compare à sa base multipliée par son taux net, à l'arrondi près ; la source prévient qu'il peut en différer, notamment du fait du lissage de la révision des valeurs locatives des locaux professionnels. Le taux net diffère du taux voté en cas d'intégration fiscale progressive. La TEOM recensée sur l'ensemble des communes se compare à celle qu'inscrivent les comptes consolidés des communes, des groupements à fiscalité propre et des syndicats, le REI ne disant pas lequel la perçoit. Le dernier exercice est provisoire.

| Exercice | Version | Statut | Communes | Lignes | dont sous secret statistique |
|---|---|---|---|---|---|
| 2012 | 2026-10-06 | definitif | 36 677 | 256 073 | 8 601 |
| 2013 | 2026-10-06 | definitif | 36 668 | 256 398 | 7 820 |
| 2014 | 2026-10-06 | definitif | 36 678 | 255 783 | 7 102 |
| 2015 | 2026-10-06 | definitif | 36 670 | 258 960 | 6 654 |
| 2016 | 2026-10-06 | definitif | 36 534 | 258 533 | 6 409 |
| 2017 | 2026-10-06 | definitif | 35 514 | 249 632 | 5 310 |
| 2018 | 2026-10-06 | definitif | 35 385 | 282 215 | 6 183 |
| 2019 | 2026-10-06 | definitif | 35 226 | 292 160 | 8 271 |
| 2020 | 2026-10-06 | definitif | 34 965 | 293 292 | 8 175 |
| 2021 | 2026-10-06 | definitif | 34 968 | 299 036 | 6 811 |
| 2022 | 2026-10-06 | definitif | 34 959 | 314 080 | 7 167 |
| 2023 | 2026-10-06 | definitif | 34 950 | 320 900 | 6 760 |
| 2024 | 2026-10-06 | definitif | 34 939 | 325 947 | 6 564 |
| 2025 | 2026-10-06 | provisoire | 34 906 | 327 553 | 6 447 |

Produit contre base multipliée par le taux net : 3 717 566 lignes comparées, 2 067 182 égales à l'arrondi près, 1 125 260 en écart de moins de 1 %, 525 124 au-delà.

| Taxe | Bénéficiaire | Lignes comparées | Égales à l'arrondi près | Écart de moins de 1 % | Au-delà | Plus grand écart au-delà (produit − base × taux) |
|---|---|---|---|---|---|---|
| CFE | Commune | 98 109 | 51 331 | 40 109 | 6 669 | −0,2 M€ (−26,3 %) : Modane (73157), 2019 |
| CFE | GFP (GEMAPI) | 153 608 | 112 441 | 3 255 | 37 912 | −5 388 € (−2,4 %) : Montpellier (34172), 2018 |
| CFE | GFP / en ZAE | 2 806 | 1 753 | 481 | 572 | −12 214 € (−12,3 %) : Honfleur (14333), 2017 |
| CFE | GFP / en zone éolienne | 1 039 | 984 | 55 | 0 | aucun |
| CFE | GFP / hors zone | 443 333 | 197 076 | 201 775 | 44 482 | +0,7 M€ (+7,5 %) : Saint-Pierre (97416), 2019 |
| CFE | Région (TASA) | 13 521 | 10 180 | 0 | 3 341 | −9 097 € (−3,5 %) : Le Mesnil-Amelot (77291), 2021 |
| CFE | Syndicat | 5 470 | 3 328 | 1 133 | 1 009 | +10 546 € (+20,3 %) : Génos (65195), 2020 |
| TEOM | Divers / zone taux plein | 343 360 | 307 858 | 33 558 | 1 944 | −0,3 M€ (−29,7 %) : Livarot-Pays-d'Auge (14371), 2025 |
| TEOM | Divers / zone taux réduit A | 12 458 | 12 444 | 9 | 5 | −17 898 € (−3,6 %) : Melle (79174), 2019 |
| TEOM | Divers / zone taux réduit B | 1 789 | 1 788 | 1 | 0 | aucun |
| TEOM | Divers / zone taux réduit C | 174 | 174 | 0 | 0 | aucun |
| TEOM | Divers / zone taux réduit D | 9 | 9 | 0 | 0 | aucun |
| TFPB | Commune | 497 492 | 322 824 | 166 955 | 7 713 | −1,6 M€ (−8,6 %) : Chessy (77111), 2021 |
| TFPB | Département | 323 449 | 196 322 | 88 896 | 38 231 | −2,9 M€ (−34,3 %) : Chessy (77111), 2017 |
| TFPB | GFP | 419 540 | 378 299 | 35 414 | 5 827 | +0,1 M€ (+2,6 %) : Angers (49007), 2019 |
| TFPB | GFP (GEMAPI) | 169 683 | 162 717 | 373 | 6 593 | +0,3 M€ (+6 308,1 %) : Plouvorn (29210), 2018 |
| TFPB | Région (TASA) | 13 935 | 13 851 | 0 | 84 | +0,1 M€ (+16,0 %) : Saint-Denis (93066), 2018 |
| TFPB | Syndicat | 30 985 | 28 921 | 1 000 | 1 064 | +22 503 € (+70,7 %) : Villeneuve-Loubet (06161), 2022 |
| TFPNB | Commune | 495 660 | 158 313 | 329 876 | 7 471 | −11 199 € (−22,0 %) : Clefs-Val d'Anjou (49101), 2014 |
| TFPNB | GFP | 491 044 | 93 324 | 209 720 | 188 000 | +12 179 € (+90,9 %) : Val-d'Oire-et-Gartempe (87028), 2019 |
| TFPNB | GFP (GEMAPI) | 169 369 | 7 886 | 5 657 | 155 826 | −771 € (−29,3 %) : Roquebrune-sur-Argens (83107), 2020 |
| TFPNB | Syndicat | 30 733 | 5 359 | 6 993 | 18 381 | −705 € (−43,2 %) : Roquebrune-sur-Argens (83107), 2025 |

Lignes dont le taux net diffère du taux voté : CFE, Commune : 381 ; CFE, GFP / en ZAE : 72 ; CFE, GFP / hors zone : 155 490 ; TFPB, Commune : 5 104 ; TFPB, GFP : 67 874 ; TFPNB, Commune : 5 099 ; TFPNB, GFP : 70 257.

| Exercice | TEOM recensée | TEOM des comptes : communes | groupements à fiscalité propre | syndicats | Écart (recensée − comptes) |
|---|---|---|---|---|---|
| 2018 | 6 896,0 M€ | 622,0 M€ | 6 299,4 M€ | 271,9 M€ | −297,3 M€ (−4,1 %) |
| 2019 | 6 981,6 M€ | 628,4 M€ | 6 344,8 M€ | 259,8 M€ | −251,5 M€ (−3,5 %) |
| 2020 | 7 101,8 M€ | 631,4 M€ | 6 475,8 M€ | 212,6 M€ | −218,0 M€ (−3,0 %) |
| 2021 | 7 394,1 M€ | 506,8 M€ | 6 879,1 M€ | 222,9 M€ | −214,6 M€ (−2,8 %) |
| 2022 | 7 876,9 M€ | 518,4 M€ | 7 354,2 M€ | 238,7 M€ | −234,4 M€ (−2,9 %) |
| 2023 | 8 489,7 M€ | 546,5 M€ | 7 924,2 M€ | 255,7 M€ | −236,7 M€ (−2,7 %) |
| 2024 | 8 934,3 M€ | 559,6 M€ | 8 362,2 M€ | 259,1 M€ | −246,5 M€ (−2,7 %) |
| 2025 | 9 156,6 M€ | 571,6 M€ | 8 586,3 M€ | 266,8 M€ | −268,1 M€ (−2,8 %) |

## 11. Recensement des éléments d'imposition

Le fichier de recensement des éléments d'imposition à la fiscalité directe locale (REI) de la DGFiP donne, pour le territoire de chaque commune, les bases, les taux et les produits de toutes les impositions directes locales et de leurs taxes annexes, pour chacun de leurs destinataires : collectivités, organismes (établissements publics fonciers, chambres consulaires, caisse d'assurance accidents agricoles, Société du grand projet du Sud-Ouest) et État, qui perçoit des frais sur les impositions et, en 2021 et 2022, la taxe d'habitation sur les résidences principales. Ce sont les impositions du rôle général de l'année, sans les rôles supplémentaires. La base en retient les variables que décrit tables/variables_rei.csv : chacune figure au tracé de chacune de ses années, son titre y dit sa grandeur, et aucune ne donne le montant d'une collectivité répété sur chacune de ses communes, ce que l'import vérifie. Une imposition sans base ni produit n'est pas retenue.

| Exercice | Version | Communes | Variables | Titres de l'en-tête différents du tracé | Valeurs illisibles | Lignes rétablies | Impositions retenues |
|---|---|---|---|---|---|---|---|
| 2012 | 2021-12-28 | 36 681 | 452 | 0 | 1 026 145 | 1 785 | 895 889 |
| 2013 | 2021-12-28 | 36 672 | 785 | 0 | 1 236 295 | 0 | 904 814 |
| 2014 | 2021-12-28 | 36 682 | 778 | 0 | 1 276 710 | 0 | 908 112 |
| 2015 | 2021-12-28 | 36 674 | 807 | 0 | 1 266 448 | 0 | 912 488 |
| 2016 | 2021-12-28 | 36 538 | 864 | 0 | 0 | 0 | 909 258 |
| 2017 | 2021-12-28 | 35 518 | 871 | 0 | 0 | 0 | 885 567 |
| 2018 | 2021-12-28 | 35 389 | 951 | 0 | 0 | 0 | 892 832 |
| 2019 | 2021-12-28 | 35 230 | 1 060 | 0 | 0 | 0 | 896 959 |
| 2020 | 2021-12-29 | 34 969 | 1 114 | 101 | 0 | 0 | 896 901 |
| 2021 | 2025-10-16 | 34 969 | 1 149 | 0 | 0 | 0 | 876 017 |
| 2022 | 2023-06-21 | 34 960 | 1 180 | 0 | 0 | 0 | 886 321 |
| 2023 | 2025-03-13 | 34 951 | 1 104 | 0 | 0 | 0 | 647 277 |
| 2024 | 2025-06-16 | 34 940 | 1 101 | 0 | 0 | 0 | 791 362 |
| 2025 | 2026-08-20 | 34 907 | 1 043 | 0 | 0 | 0 | 789 653 |

Les valeurs illisibles sont les marques d'une valeur manquante (« , » en 2012, « . » de 2013 à 2015), et quelques textes dans une colonne numérique ; les lignes rétablies sont celles des communes de Franche-Comté en 2012, où l'export a fondu deux champs en un.

Produit contre base multipliée par le taux net : 7 660 345 impositions comparées, 3 227 853 égales à l'arrondi près, 3 110 866 en écart de moins de 1 %, 1 321 626 au-delà. La source prévient qu'un produit peut différer de sa base multipliée par son taux, du fait du lissage de la révision des valeurs locatives des locaux professionnels, des taux moyens d'une commune où plusieurs taux s'appliquent, ou du secret statistique.

| Taxe | Destinataire | Impositions comparées | Égales à l'arrondi près | Écart de moins de 1 % | Au-delà | Plus grand écart au-delà (produit − base × taux) |
|---|---|---|---|---|---|---|
| CFE | Société du grand projet du Sud-Ouest (TSC) | 4 398 | 3 175 | 482 | 741 | −204 € (−1,6 %) : LE TEICH (33527), 2025 |
| CFE | TSE | 294 450 | 89 333 | 107 125 | 97 992 | −37 644 € (−3,8 %) : LE MESNIL AMELOT (77291), 2021 |
| CFE | chambre de commerce et d'industrie | 405 858 | 198 460 | 101 380 | 106 018 | +0,1 M€ (base nulle) : MONT DE LANS (38253), 2016 |
| CFE | chambre de métiers, droit additionnel | 316 615 | 126 041 | 103 471 | 87 103 | −0,2 M€ (−7,9 %) : PARIS (75056), 2017 |
| CFE | commune | 96 728 | 47 061 | 42 991 | 6 676 | −0,2 M€ (−26,3 %) : MODANE (73157), 2019 |
| CFE | groupement (GEMAPI) | 75 075 | 30 183 | 19 545 | 25 347 | +46 746 € (+1,2 %) : VILLE DE PARIS (75056), 2025 |
| CFE | groupement, fiscalité additionnelle ou de zone, hors zone | 94 800 | 44 494 | 38 689 | 11 617 | −0,5 M€ (−32,0 %) : MODANE (73157), 2019 |
| CFE | groupement, fiscalité unique ou zone d'activités | 347 160 | 129 447 | 184 024 | 33 689 | +0,7 M€ (+7,5 %) : SAINT PIERRE (97416), 2019 |
| CFE | groupement, zone éolienne | 1 027 | 686 | 341 | 0 | aucun |
| CFE | région Île-de-France (TASA) | 13 517 | 3 616 | 4 435 | 5 466 | −9 097 € (−3,5 %) : LE MESNIL AMELOT (77291), 2021 |
| CFE | syndicats | 5 456 | 2 643 | 1 665 | 1 148 | +10 546 € (+20,3 %) : GENOS (65195), 2020 |
| TAFNB | commune | 100 187 | 56 863 | 35 943 | 7 381 | +210 € (+1,9 %) : BESSE SUR ISSOLE (83018), 2013 |
| TAFNB | groupement | 348 926 | 147 928 | 179 920 | 21 078 | −538 € (−1,2 %) : LORGUES (83072), 2023 |
| TAFNB | métropole du Grand Paris | 1 308 | 546 | 762 | 0 | aucun |
| TEOM | zone à taux plein | 343 403 | 280 766 | 60 663 | 1 974 | +0,3 M€ (base nulle) : GENNES-VAL DE LOIRE (49261), 2019 |
| TEOM | zone à taux réduit A | 12 487 | 12 404 | 28 | 55 | +0,1 M€ (base nulle) : TORIGNY-LES-VILLES (50601), 2016 |
| TEOM | zone à taux réduit B | 1 797 | 1 782 | 6 | 9 | +0,1 M€ (base nulle) : MONCOUTANT-SUR-SEVRE (79179), 2021 |
| TEOM | zone à taux réduit C | 175 | 174 | 0 | 1 | +29 146 € (base nulle) : SABLONS SUR HUISNE (61116), 2016 |
| TEOM | zone à taux réduit D | 9 | 9 | 0 | 0 | aucun |
| TFPB | TSE | 324 048 | 85 436 | 141 297 | 97 315 | +0,3 M€ (+7 329,3 %) : PLOUVORN (29210), 2018 |
| TFPB | TSE autres | 25 542 | 9 554 | 13 863 | 2 125 | +0,1 M€ (+19,6 %) : SAINT DENIS (93066), 2018 |
| TFPB | commune | 497 722 | 237 837 | 252 108 | 7 777 | −1,6 M€ (−8,6 %) : CHESSY (77111), 2021 |
| TFPB | département | 323 052 | 183 324 | 101 625 | 38 103 | −2,9 M€ (−34,3 %) : CHESSY (77111), 2017 |
| TFPB | groupement | 419 833 | 240 367 | 167 443 | 12 023 | +0,3 M€ (+1,2 %) : VILLEURBANNE (69266), 2017 |
| TFPB | groupement (GEMAPI) | 169 683 | 50 950 | 89 325 | 29 408 | +0,3 M€ (+6 308,1 %) : PLOUVORN (29210), 2018 |
| TFPB | région Île-de-France (TASA) | 13 935 | 4 164 | 8 863 | 908 | +0,1 M€ (+16,0 %) : SAINT DENIS (93066), 2018 |
| TFPB | syndicats | 30 985 | 13 455 | 14 055 | 3 475 | +22 503 € (+70,7 %) : VILLENEUVE LOUBET (06161), 2022 |
| TFPNB | TSE | 235 524 | 13 592 | 2 345 | 219 587 | +4 847 € (+11,4 %) : VILLE DE PARIS (75056), 2018 |
| TFPNB | TSE autres | 24 008 | 1 296 | 1 356 | 21 356 | −306 € (−19,1 %) : MONTAUBAN (82121), 2023 |
| TFPNB | caisse d'assurance accidents agricoles, droit proportionnel | 20 050 | 20 050 | 0 | 0 | aucun |
| TFPNB | chambre d'agriculture | 497 600 | 220 622 | 253 725 | 23 253 | +642 € (+1,2 %) : LEGE-CAP-FERRET (33236), 2024 |
| TFPNB | commune | 495 100 | 119 972 | 367 624 | 7 504 | −11 199 € (−22,0 %) : CLEFS-VAL D'ANJOU (49101), 2014 |
| TFPNB | groupement | 489 043 | 66 917 | 233 671 | 188 455 | +12 179 € (+90,9 %) : VAL-D'OIRE-ET-GARTEMPE (87028), 2019 |
| TFPNB | groupement (GEMAPI) | 168 548 | 4 299 | 7 114 | 157 135 | −771 € (−29,3 %) : ROQUEBRUNE-SUR-ARGENS (83107), 2020 |
| TFPNB | syndicats | 30 733 | 4 201 | 7 997 | 18 535 | −705 € (−43,2 %) : ROQUEBRUNE-SUR-ARGENS (83107), 2025 |
| TH | TSE | 221 770 | 64 745 | 105 567 | 51 458 | −2 052 € (−1,3 %) : CLERMONT-FERRAND (63113), 2012 |
| TH | TSE autres | 14 172 | 6 093 | 7 670 | 409 | +937 € (+1,1 %) : LE PECQ (78481), 2020 |
| TH | commune | 372 634 | 223 857 | 148 055 | 722 | +1,2 M€ (+5,1 %) : DUNKERQUE (59183), 2013 |
| TH | commune (GEMAPI) | 8 | 1 | 6 | 1 | −84 € (−1,2 %) : OUISTREHAM (14488), 2016 |
| TH | groupement | 369 497 | 213 690 | 155 343 | 464 | +0,2 M€ (+6,8 %) : BORDEAUX (33063), 2021 |
| TH | groupement (GEMAPI) | 82 784 | 44 859 | 28 101 | 9 824 | −0,1 M€ (−17,9 %) : VILLE DE PARIS (75056), 2022 |
| TH | syndicats | 24 634 | 10 383 | 12 063 | 2 188 | −0,1 M€ (−5,4 %) : SAINT-GERMAIN-EN-LAYE (78551), 2020 |
| TH | État (part communale) | 49 130 | 13 844 | 34 824 | 462 | −0,1 M€ (−1,2 %) : ANNECY (74010), 2022 |
| TH | État (part intercommunale) | 48 862 | 12 521 | 36 228 | 113 | +12 216 € (+4,2 %) : MELLE (79174), 2021 |
| THLV | TSE | 9 482 | 5 085 | 1 135 | 3 262 | −27 € (−1,2 %) : AGEN (47001), 2025 |
| THLV | TSE autres | 875 | 474 | 169 | 232 | −8 € (−1,7 %) : COUTRAS (33138), 2023 |
| THLV | commune | 27 425 | 18 256 | 8 804 | 365 | +6 757 € (+8,2 %) : VALSERHONE (01033), 2020 |
| THLV | groupement | 3 120 | 2 394 | 726 | 0 | aucun |
| THLV | groupement (GEMAPI) | 10 525 | 6 305 | 2 491 | 1 729 | +15 € (+1,4 %) : SAINT-LOUIS (68297), 2023 |
| THLV | syndicats | 3 217 | 1 847 | 655 | 715 | −11 € (−2,8 %) : GRUISSAN (11170), 2023 |
| THRS | TSE | 42 602 | 23 949 | 7 007 | 11 646 | −921 € (−2,8 %) : LEUCATE (11202), 2023 |
| THRS | TSE autres | 5 597 | 3 349 | 1 454 | 794 | −138 € (−6,7 %) : SAVIGNY LE TEMPLE (77445), 2023 |
| THRS | commune | 50 704 | 49 115 | 1 534 | 55 | −22 089 € (−6,8 %) : VALSERHONE (01033), 2023 |
| THRS | groupement | 50 311 | 48 729 | 1 492 | 90 | +7 244 € (+3,7 %) : TOUROUVRE AU PERCHE (61491), 2024 |
| THRS | groupement (GEMAPI) | 41 135 | 24 480 | 13 184 | 3 471 | −372 € (−2,3 %) : VILLERS SUR MER (14754), 2025 |
| THRS | syndicats | 3 079 | 2 230 | 477 | 372 | −572 € (−5,8 %) : GRUISSAN (11170), 2025 |

La base simplifiée de la fiscalité directe locale de l'OFGL (section 10) est tirée du REI : son produit, pour chaque commune, chaque taxe et chaque bénéficiaire, se compare à celui des destinataires du REI dont il vient, à l'euro près. La part intercommunale de la CFE se compare toutes zones réunies ; l'effet du coefficient correcteur, que l'OFGL range dans la TFPB des communes depuis 2021, n'est pas un impôt et n'a pas d'équivalent ici. Saint-Martin, collectivité d'outre-mer, figure au REI (sous le code 97808, que forment son département et son numéro) mais pas dans la base simplifiée. Pour les communes de la métropole de Lyon, de 2015 à 2020, le REI range dans la part du groupement la TFPB que perçoit la métropole au titre du département, l'OFGL dans celle du département : les deux écarts se compensent.

| Taxe | Bénéficiaire (OFGL) | Destinataires (REI) | Exercices | Communes comparées | Égales | En écart | Sous secret statistique (OFGL) | Produit OFGL | Produit REI | Plus grand écart (REI − OFGL) |
|---|---|---|---|---|---|---|---|---|---|---|
| TFPB | Commune | commune | 14 années entre 2012 et 2025 | 497 472 | 497 458 | 14 | 0 | 332 216,3 M€ | 332 404,7 M€ | +18,3 M€ : SAINT-MARTIN (97808), 2025 |
| TFPB | Syndicat | syndicats | 14 années entre 2012 et 2025 | 30 937 | 30 937 | 0 | 0 | 1 734,8 M€ | 1 734,8 M€ | aucun |
| TFPB | GFP | groupement | 14 années entre 2012 et 2025 | 419 673 | 419 319 | 354 | 0 | 22 293,1 M€ | 23 839,7 M€ | +110,5 M€ : LYON (69123), 2020 |
| TFPB | Département | département | 9 années entre 2012 et 2020 | 323 406 | 323 052 | 354 | 0 | 119 709,2 M€ | 118 162,6 M€ | −110,5 M€ : LYON (69123), 2020 |
| TFPB | Région (TASA) | région Île-de-France (TASA) | 11 années entre 2015 et 2025 | 13 935 | 13 935 | 0 | 0 | 613,4 M€ | 613,4 M€ | aucun |
| TFPB | GFP (GEMAPI) | groupement (GEMAPI) | 11 années entre 2015 et 2025 | 169 675 | 169 675 | 0 | 0 | 1 560,5 M€ | 1 560,5 M€ | aucun |
| TFPNB | Commune | commune | 14 années entre 2012 et 2025 | 494 477 | 494 463 | 14 | 0 | 12 013,4 M€ | 12 017,4 M€ | +0,4 M€ : SAINT-MARTIN (97808), 2025 |
| TFPNB | Syndicat | syndicats | 14 années entre 2012 et 2025 | 30 706 | 30 706 | 0 | 0 | 77,6 M€ | 77,6 M€ | aucun |
| TFPNB | GFP | groupement | 14 années entre 2012 et 2025 | 488 812 | 488 812 | 0 | 0 | 2 120,8 M€ | 2 120,8 M€ | aucun |
| TFPNB | GFP (GEMAPI) | groupement (GEMAPI) | 11 années entre 2015 et 2025 | 168 429 | 168 429 | 0 | 0 | 94,3 M€ | 94,3 M€ | aucun |
| CFE | Commune | commune | 14 années entre 2012 et 2025 | 96 268 | 96 265 | 3 | 0 | 10 530,3 M€ | 10 530,3 M€ | +8 € : MOLESME (21419), 2018 |
| CFE | Syndicat | syndicats | 14 années entre 2012 et 2025 | 5 456 | 5 454 | 2 | 0 | 109,4 M€ | 109,4 M€ | +544 € : BUTTEN (67072), 2018 |
| CFE | GFP / hors zone, GFP / en ZAE, GFP / en zone éolienne | groupement, fiscalité additionnelle ou de zone, hors zone, groupement, fiscalité unique ou zone d'activités, groupement, zone éolienne | 14 années entre 2012 et 2025 | 438 565 | 438 564 | 1 | 570 | 91 012,0 M€ | 91 012,0 M€ | +0,1 M€ : AIGRE (16005), 2019 |
| CFE | Région (TASA) | région Île-de-France (TASA) | 11 années entre 2015 et 2025 | 13 517 | 13 517 | 0 | 0 | 248,4 M€ | 248,4 M€ | aucun |
| CFE | GFP (GEMAPI) | groupement (GEMAPI) | 11 années entre 2015 et 2025 | 152 061 | 152 060 | 1 | 142 | 512,8 M€ | 512,8 M€ | +4 € : BEAULIEU (58026), 2020 |
| TEOM | Divers / zone taux plein | zone à taux plein | 14 années entre 2012 et 2025 | 343 403 | 343 360 | 43 | 0 | 99 264,7 M€ | 99 325,8 M€ | +7,5 M€ : SAINT-MARTIN (97808), 2025 |
| TEOM | Divers / zone taux réduit A | zone à taux réduit A | 14 années entre 2012 et 2025 | 12 487 | 12 437 | 50 | 0 | 2 044,7 M€ | 2 045,6 M€ | +0,1 M€ : TORIGNY-LES-VILLES (50601), 2016 |
| TEOM | Divers / zone taux réduit B | zone à taux réduit B | 14 années entre 2012 et 2025 | 1 797 | 1 788 | 9 | 0 | 173,3 M€ | 173,6 M€ | +0,1 M€ : MONCOUTANT-SUR-SEVRE (79179), 2021 |
| TEOM | Divers / zone taux réduit C | zone à taux réduit C | 14 années entre 2012 et 2025 | 175 | 174 | 1 | 0 | 36,4 M€ | 36,5 M€ | +29 146 € : SABLONS SUR HUISNE (61116), 2016 |
| TEOM | Divers / zone taux réduit D | zone à taux réduit D | 9 années entre 2014 et 2022 | 9 | 9 | 0 | 0 | 0,0 M€ | 0,0 M€ | aucun |

Produit de chaque taxe, toutes parts réunies, chaque année (en millions d'euros) :

| Taxe | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CFE (Cotisation foncière des entreprises) | 7 736,8 | 8 042,1 | 8 109,7 | 8 396,7 | 8 606,2 | 8 944,1 | 9 151,0 | 9 214,2 | 9 386,5 | 7 906,1 | 8 082,2 | 8 675,2 | 9 089,6 | 9 477,3 |
| CVAE (Cotisation sur la valeur ajoutée des entreprises) | 14 875,8 | 16 035,9 | 15 622,3 | 16 326,9 | 16 556,0 | 17 317,4 | 17 405,6 | 18 661,1 | 19 228,9 | 9 568,0 | 9 264,3 | — | — | — |
| IFER_BAR (Imposition forfaitaire sur les entreprises de réseaux : centrales hydrauliques) | 20,1 | 22,1 | 22,1 | 22,7 | 23,4 | 24,7 | 25,1 | 25,5 | 27,5 | 28,1 | 27,5 | 28,4 | 29,7 | 30,3 |
| IFER_EOL (Imposition forfaitaire sur les entreprises de réseaux : éoliennes terrestres) | 35,8 | 41,9 | 46,2 | 52,0 | 57,0 | 65,3 | 76,8 | 88,9 | 96,3 | 105,6 | 116,8 | 132,3 | 145,7 | 156,4 |
| IFER_GAZ (Imposition forfaitaire sur les entreprises de réseaux : installations gazières) | 10,0 | 9,9 | 11,1 | 11,6 | 11,7 | 12,1 | 14,9 | 15,1 | 13,4 | 13,6 | 13,8 | 14,5 | 17,7 | 18,0 |
| IFER_GEO (Imposition forfaitaire sur les entreprises de réseaux : centrales géothermiques) | — | — | — | — | — | — | — | — | 0,3 | — | — | — | — | — |
| IFER_HYD (Imposition forfaitaire sur les entreprises de réseaux : hydroliennes) | 0,1 | — | — | — | — | — | — | — | — | — | — | — | — | — |
| IFER_NUC (Imposition forfaitaire sur les entreprises de réseaux : centrales nucléaires et thermiques à flamme) | 4,1 | — | 3,2 | 3,2 | 4,7 | 3,2 | 3,2 | 3,2 | 3,2 | 5,7 | 5,7 | 5,9 | 6,1 | 6,3 |
| IFER_PV (Imposition forfaitaire sur les entreprises de réseaux : centrales photovoltaïques) | 1,5 | 4,0 | 5,2 | 7,0 | 10,8 | 12,8 | 14,9 | 18,1 | 18,6 | 20,6 | 24,8 | 31,0 | 36,6 | 45,3 |
| IFER_RAD (Imposition forfaitaire sur les entreprises de réseaux : stations radioélectriques) | 119,4 | 126,8 | 137,1 | 150,2 | 159,4 | 181,5 | 187,1 | 197,7 | 213,6 | 242,0 | 270,1 | 305,0 | 337,4 | 378,0 |
| IFER_TRA (Imposition forfaitaire sur les entreprises de réseaux : transformateurs électriques) | 6,1 | 1,3 | 1,4 | 1,3 | 4,7 | 4,9 | 5,1 | 5,6 | 5,2 | 5,6 | 5,6 | 6,0 | 6,8 | 7,0 |
| TAFNB (Taxe additionnelle à la taxe foncière sur les propriétés non bâties) | 76,0 | 77,4 | 78,2 | 79,7 | 79,9 | 80,6 | 81,6 | 84,6 | 85,4 | 86,0 | 89,4 | 95,2 | 99,2 | 99,5 |
| TASCOM (Taxe sur les surfaces commerciales) | 561,4 | 611,7 | 618,0 | 641,2 | 661,1 | 828,6 | 676,4 | 695,5 | 697,3 | 686,0 | 734,6 | 808,4 | 902,7 | 842,7 |
| TEOM (Taxe d'enlèvement des ordures ménagères) | 6 089,9 | 6 256,2 | 6 357,6 | 6 555,6 | 6 690,3 | 6 793,9 | 6 920,9 | 7 014,0 | 7 139,7 | 7 434,9 | 7 921,0 | 8 539,5 | 8 992,3 | 9 230,4 |
| TFPB (Taxe foncière sur les propriétés bâties) | 28 586,1 | 29 818,7 | 30 622,8 | 31 863,2 | 33 443,0 | 34 290,1 | 35 289,3 | 36 227,3 | 37 008,4 | 36 230,2 | 38 308,3 | 42 188,6 | 44 484,5 | 45 738,9 |
| TFPNB (Taxe foncière sur les propriétés non bâties) | 1 266,3 | 1 285,1 | 1 297,8 | 1 317,3 | 1 323,8 | 1 331,6 | 1 347,5 | 1 370,8 | 1 385,2 | 1 398,2 | 1 442,7 | 1 543,7 | 1 622,3 | 1 523,9 |
| TH (Taxe d'habitation) | 20 032,3 | 20 774,8 | 21 105,8 | 22 296,2 | 22 382,8 | 22 826,6 | 23 378,2 | 24 161,8 | 24 513,0 | 8 492,8 | 5 902,2 | — | — | — |
| THLV (Taxe d'habitation sur les logements vacants) | 21,4 | 66,4 | 62,8 | 63,6 | 72,9 | 67,0 | 74,7 | 79,0 | 89,3 | 86,7 | 88,6 | 115,2 | 194,8 | 138,7 |
| THRS (Taxe d'habitation sur les résidences secondaires et autres locaux meublés non affectés à l'habitation principale) | — | — | — | — | — | — | — | — | — | — | — | 2 510,1 | 3 905,8 | 3 151,2 |

Communes où le REI donne un produit de chaque taxe, chaque année :

| Taxe | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CFE | 32 064 | 32 445 | 32 642 | 32 882 | 32 917 | 32 036 | 32 066 | 30 759 | 30 651 | 31 611 | 31 658 | 31 925 | 32 067 | 32 152 |
| CVAE | 30 527 | 31 045 | 31 180 | 31 337 | 31 379 | 30 705 | 30 762 | 29 798 | 29 689 | 30 328 | 30 372 | — | — | — |
| IFER_BAR | 204 | 227 | 233 | 240 | 246 | 257 | 261 | 257 | 257 | 263 | 261 | 256 | 260 | 268 |
| IFER_EOL | 448 | 513 | 559 | 615 | 670 | 741 | 825 | 914 | 975 | 1 076 | 1 094 | 1 155 | 1 205 | 1 258 |
| IFER_GAZ | 95 | 82 | 143 | 135 | 127 | 134 | 131 | 132 | 131 | 135 | 137 | 138 | 137 | 143 |
| IFER_GEO | — | — | — | — | — | — | — | — | 1 | — | — | — | — | — |
| IFER_HYD | 1 | — | — | — | — | — | — | — | — | — | — | — | — | — |
| IFER_NUC | 1 | — | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 55 | 53 | 55 | 55 | 54 |
| IFER_PV | 68 | 191 | 229 | 276 | 315 | 354 | 398 | 436 | 488 | 546 | 637 | 791 | 1 611 | 3 517 |
| IFER_RAD | 6 950 | 7 386 | 6 937 | 7 301 | 7 712 | 8 859 | 9 763 | 10 234 | 10 713 | 11 238 | 11 521 | 12 028 | 12 665 | 13 482 |
| IFER_TRA | 10 | 6 | 6 | 6 | 8 | 8 | 9 | 10 | 9 | 10 | 10 | 10 | 12 | 13 |
| TAFNB | 32 946 | 32 979 | 33 034 | 33 056 | 32 917 | 32 005 | 31 894 | 31 773 | 31 561 | 31 593 | 31 619 | 31 660 | 31 696 | 31 688 |
| TASCOM | 2 464 | 2 632 | 2 587 | 2 524 | 2 654 | 2 618 | 2 616 | 2 573 | 2 592 | 2 565 | 2 608 | 2 529 | 2 610 | 2 586 |
| TEOM | 24 601 | 24 594 | 24 439 | 24 492 | 24 484 | 24 360 | 24 660 | 24 726 | 24 437 | 24 638 | 24 857 | 24 373 | 24 369 | 24 381 |
| TFPB | 36 601 | 36 589 | 36 596 | 36 587 | 36 416 | 35 397 | 35 268 | 35 114 | 34 856 | 34 886 | 34 879 | 34 868 | 34 856 | 34 821 |
| TFPNB | 36 589 | 36 578 | 36 593 | 36 588 | 36 398 | 35 380 | 35 250 | 35 089 | 34 828 | 34 884 | 34 873 | 34 869 | 34 860 | 34 821 |
| TH | 36 601 | 36 598 | 36 607 | 36 601 | 36 462 | 35 442 | 35 306 | 35 155 | 34 891 | 32 314 | 30 497 | — | — | — |
| THLV | 3 157 | 3 627 | 3 838 | 3 991 | 4 231 | 4 215 | 4 547 | 4 732 | 4 711 | 3 607 | 3 754 | 770 | 6 374 | 6 676 |
| THRS | — | — | — | — | — | — | — | — | — | — | — | 1 955 | 25 449 | 23 300 |

Un fichier peut ne pas donner une taxe pour toutes les communes, ses valeurs restant vides : TH en 2023 : 1 955 communes, contre 30 497 en 2022 et 25 449 en 2024 ; THLV en 2023 : 770 communes, contre 3 754 en 2022 et 6 374 en 2024 (pour la taxe d'habitation, celle sur les résidences secondaires depuis 2023). Le produit de ces années est partiel.

Produit de chaque niveau qui perçoit, chaque année (en millions d'euros) ; la part fixe de la TEOM est rapportée au niveau que la fiche de la commune dit la percevoir :

| Exercice | communes | syndicats | groupements | départements | régions | organismes | État | non dit | Ensemble |
|---|---|---|---|---|---|---|---|---|---|
| 2012 | 32 496,0 | 436,1 | 20 339,6 | 18 726,5 | 3 718,4 | 1 673,4 | 2 053,0 | 0,0 | 79 443,0 |
| 2013 | 33 294,8 | 387,9 | 21 744,7 | 19 899,4 | 4 008,7 | 1 704,4 | 2 134,0 | 0,0 | 83 174,0 |
| 2014 | 33 322,9 | 339,4 | 22 586,9 | 20 002,7 | 3 905,2 | 1 763,2 | 2 180,8 | 0,0 | 84 101,2 |
| 2015 | 34 817,2 | 324,9 | 24 156,0 | 20 289,4 | 4 160,3 | 1 776,2 | 2 264,5 | 0,0 | 87 788,4 |
| 2016 | 34 537,5 | 296,4 | 25 592,5 | 21 307,8 | 4 217,1 | 1 799,4 | 2 336,8 | 0,0 | 90 087,7 |
| 2017 | 34 630,2 | 271,0 | 27 089,0 | 17 822,9 | 8 737,2 | 1 843,5 | 2 390,4 | 0,1 | 92 784,3 |
| 2018 | 35 168,4 | 242,1 | 28 069,7 | 18 206,1 | 8 744,2 | 1 786,6 | 2 435,0 | 0,4 | 94 652,4 |
| 2019 | 37 036,5 | 242,4 | 28 948,2 | 18 024,9 | 9 336,1 | 1 784,8 | 2 489,3 | 0,4 | 97 862,5 |
| 2020 | 37 762,6 | 227,6 | 29 669,2 | 18 394,3 | 9 615,1 | 1 701,6 | 2 528,2 | 13,1 | 99 911,6 |
| 2021 | 36 825,8 | 228,4 | 22 186,4 | 3 954,6 | 76,6 | 1 326,5 | 7 698,2 | 13,5 | 72 310,1 |
| 2022 | 38 459,8 | 242,9 | 23 271,1 | 3 843,6 | 76,8 | 1 239,7 | 5 163,5 | 0,0 | 72 297,6 |
| 2023 | 41 193,7 | 254,7 | 19 564,4 | 167,2 | 76,8 | 1 336,3 | 2 406,0 | 0,1 | 64 999,1 |
| 2024 | 44 098,1 | 268,9 | 21 305,7 | 184,6 | 76,7 | 1 365,9 | 2 571,1 | 0,1 | 69 871,1 |
| 2025 | 44 515,2 | 276,8 | 21 766,1 | 204,5 | 76,8 | 1 392,3 | 2 612,0 | 0,1 | 70 843,8 |

TEOM recensée de chaque niveau, part fixe et part incitative, contre celle de ses comptes consolidés ; le REI range au niveau du groupement la TEOM que celui-ci perçoit pour le compte d'un syndicat :

| Exercice | communes : recensée | comptes | groupements : recensée | comptes | syndicats : recensée | comptes | Écart d'ensemble (recensée − comptes) |
|---|---|---|---|---|---|---|---|
| 2018 | 622,7 M€ | 622,0 M€ | 6 247,7 M€ | 6 299,4 M€ | 50,2 M€ | 271,9 M€ | −272,7 M€ (−3,8 %) |
| 2019 | 629,7 M€ | 628,4 M€ | 6 335,0 M€ | 6 344,8 M€ | 49,0 M€ | 259,8 M€ | −219,4 M€ (−3,0 %) |
| 2020 | 628,0 M€ | 631,4 M€ | 6 447,4 M€ | 6 475,8 M€ | 51,1 M€ | 212,6 M€ | −193,2 M€ (−2,6 %) |
| 2021 | 506,8 M€ | 506,8 M€ | 6 862,0 M€ | 6 879,1 M€ | 52,6 M€ | 222,9 M€ | −187,4 M€ (−2,5 %) |
| 2022 | 521,7 M€ | 518,4 M€ | 7 339,5 M€ | 7 354,2 M€ | 59,7 M€ | 238,7 M€ | −190,3 M€ (−2,3 %) |
| 2023 | 550,3 M€ | 546,5 M€ | 7 922,9 M€ | 7 924,2 M€ | 66,2 M€ | 255,7 M€ | −187,0 M€ (−2,1 %) |
| 2024 | 563,3 M€ | 559,6 M€ | 8 359,9 M€ | 8 362,2 M€ | 68,9 M€ | 259,1 M€ | −188,6 M€ (−2,1 %) |
| 2025 | 577,1 M€ | 571,6 M€ | 8 582,5 M€ | 8 586,3 M€ | 70,7 M€ | 266,8 M€ | −194,4 M€ (−2,1 %) |

## 12. Organismes publics : ce que la base couvre

Le secteur des administrations publiques, unité par unité, d'après les listes et décomptes officiels : la liste des organismes divers d'administration centrale (ODAC) et le nombre d'organismes divers d'administration locale (ODAL) par catégorie, que l'Insee établit pour les comptes nationaux, le nombre de collectivités territoriales et de groupements au 1er janvier que publie la DGCL. Ils se comparent aux unités dont la base a les comptes une à une, d'après les listes des jeux de l'OFGL (numéros Siren distincts). Un écart n'est pas une erreur : un décompte à une date et la liste des comptes d'un exercice ne retiennent pas toujours les mêmes unités.

### Les sous-secteurs en 2024

| Sous-secteur | Unités selon les décomptes officiels | Unités dont la base a les comptes, une à une | Sources de la base sur le sous-secteur ou ses parties |
|---|---|---|---|
| État (S13111) | l'État | l'État, d'après son budget exécuté et ses comptes annuels (lois de règlement et de résultats) | insee : bdm-comptes-etat, bdm-dette-trim-apu, t3101 à t3104, t3106, t3107, t3203, t3215, t3216, t3303, t3307, t7303 ; senat : 20 sources (pjl06-389 … pjl25-726) |
| Organismes divers d'administration centrale (S13112) | 701 (liste des ODAC, 2024) | aucun | insee : bdm-dette-trim-apu, t3101 à t3104, t3106, t3204, t3215, t3216, t3304, t3307, t7304 |
| Collectivités locales (S13131) | 44 932 au 1er janvier (DGCL) | 44 951 (jeux de l'OFGL, exercice 2024) | dgcl : finances-departements, finances-regions ; insee : t3206 à t3210, t3217 ; ofgl : annexe-2a, annexe-2b, annexe-2c, annexe-2d |
| Organismes divers d'administration locale (S13132) | 22 697 (liste des ODAL) | 12 704 : SDIS, centres d'action sociale, établissements publics locaux (jeux de l'OFGL, exercice 2024) | insee : t3211 |
| Administrations de sécurité sociale (S1314) | pas de liste dans la documentation des comptes nationaux de l'Insee | aucune ; leurs ensembles d'après les lois de financement : régime général, régimes obligatoires de base, FSV, CADES, FRR | eurostat : gov_10a_main ; insee : bdm-dette-trim-apu, t3101 à t3104, t3106, t3108, t3212 à t3216, t3306, t3307, t7306 ; senat : 22 sources (pjl06-051 … tas22-018) |

### Collectivités territoriales et groupements

Pour chaque catégorie, le nombre que la DGCL décompte au 1er janvier (tableaux 2.2 et 2.5a de « Les collectivités locales en chiffres »), puis le nombre d'unités dont la base a les comptes de l'exercice, et leur écart.

| Catégorie | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Communes | 34 955 / 34 955 | 34 945 / 34 945 | 34 935 / 34 932 (−3) | 34 875 / 34 778 (−97) |
| Départements | 95 / 95 | 95 / 95 | 95 / 95 | 95 / 95 |
| Régions | 14 / 14 | 14 / 14 | 14 / 14 | 14 / 14 |
| Collectivités à statut particulier | 5 / 4 (−1) | 5 / 4 (−1) | 5 / 4 (−1) | 5 / 4 (−1) |
| Groupements à fiscalité propre | 1 254 / 1 254 | 1 254 / 1 254 | 1 254 / 1 254 | 1 254 / 1 250 (−4) |
| Syndicats | 8 882 / 8 940 (+58) | 8 777 / 8 820 (+43) | 8 629 / 8 652 (+23) | 8 322 / 8 435 (+113) |
| Ensemble | 45 205 / 45 262 (+57) | 45 090 / 45 132 (+42) | 44 932 / 44 951 (+19) | 44 565 / 44 576 (+11) |

Unités retenues dans la base :

- Communes : le jeu des communes, Ville de Paris comprise.
- Départements : la catégorie « DEPT » du jeu des départements, qui comprend le Département de Mayotte.
- Régions : la catégorie « REG » du jeu des régions.
- Collectivités à statut particulier : les collectivités territoriales uniques du jeu des régions (Corse, Martinique, Guyane) et la métropole de Lyon ; le Département de Mayotte est compté avec les départements.
- Groupements à fiscalité propre : la catégorie « GFP » du jeu des groupements, sans la métropole de Lyon ni les établissements publics territoriaux.
- Syndicats : le jeu des syndicats sans les maisons départementales des personnes handicapées, et les établissements publics territoriaux du jeu des groupements, que la DGCL compte parmi les syndicats.

### Organismes divers d'administration locale en 2024

Pour chaque catégorie de la liste de l'Insee, le nombre de ses organismes, puis celui des unités dont la base a les comptes de l'exercice 2024, pour les catégories que publie un jeu de l'OFGL.

| Catégorie | Organismes (Insee) | Dans la base |
|---|---|---|
| Agences d'urbanisme | 50 | — |
| Centre de gestion de la propriété forestière | 1 | — |
| Chambres consulaires | 274 | — |
| Établissements publics fonciers | 40 | — |
| ODAL divers | 145 | — |
| Services départementaux d'incendie et de secours | 97 | 97 |
| Électricité de Mayotte | 1 | — |
| Établissements publics d'aménagement | 11 | — |
| Île-de-France Mobilités | 1 | — |
| Offices de tourisme | 433 | — |
| Société de la ligne nouvelle Montpellier Perpignan | 1 | — |
| Société de la ligne nouvelle Provence Côte d'Azur | 1 | — |
| Société de livraison des ouvrages olympiques | 1 | — |
| Société du canal Seine-Nord Europe | 1 | — |
| Sociétés d'aménagement foncier et d'établissement rural | 18 | — |
| Sociétés de grands projets | 2 | — |
| Agences et offices de l'eau | 10 | — |
| Établissements publics culturels locaux | 248 | — |
| Caisses des écoles | 1 113 | — |
| Centres de gestion de la fonction publique territoriale | 98 | — |
| Établissements publics locaux d'enseignement | 7 967 | — |
| Centres communaux d'action sociale | 12 085 | 11 394 |
| Maisons départementales des personnes handicapées | 99 | 102 |
| Établissements publics locaux (jeu de l'OFGL), hors MDPH | — | 1 111 |
| Ensemble | 22 697 | 12 704 |

Unités retenues dans la base :

- Services départementaux d'incendie et de secours : le jeu des SDIS.
- Centres communaux d'action sociale : le jeu des centres d'action sociale : centres communaux et intercommunaux, et celui de la Ville de Paris.
- Maisons départementales des personnes handicapées : les maisons départementales des personnes handicapées des jeux des syndicats et des établissements publics locaux.
- Établissements publics locaux : établissements publics administratifs, régies personnalisées et groupements d'intérêt public, que l'Insee range dans plusieurs de ses catégories ; par activité : tourisme 420, activités culturelles 230, activités diverses 169, production et distribution d'énergie 64, activités sportives 33, nouvelles technologies de l'information et de la communication 19, et 176 dans 26 autres activités.

### Organismes divers d'administration centrale en 2024

La liste de l'Insee, que la table des organismes reprend organisme par organisme : 701 organismes, par fonction (premier niveau de la COFOG). La base n'a les comptes d'aucun d'eux un à un.

| Fonction | Organismes |
|---|---|
| GF01 Services généraux des administrations publiques | 119 |
| GF02 Défense | 5 |
| GF03 Ordre et sécurité publics | 5 |
| GF04 Affaires économiques | 60 |
| GF05 Protection de l'environnement | 16 |
| GF06 Logements et équipements collectifs | 6 |
| GF07 Santé | 82 |
| GF08 Loisirs, culture et culte | 115 |
| GF09 Enseignement | 286 |
| GF10 Protection sociale | 7 |
| Ensemble | 701 |

## 13. Comptes individuels de la DGFiP

Les comptes individuels que la DGFiP publie pour chaque commune depuis 2000, chaque groupement à fiscalité propre depuis 2007, chaque département et chaque région depuis 2008 : l'analyse des équilibres financiers fondamentaux du budget principal (budgets annexes compris pour les groupements) et les éléments de la fiscalité directe locale, en milliers d'euros, dans la version la plus récente de chaque exercice. Une valeur est exacte à la demi-unité de la dernière décimale que sa variable publie dans l'exercice.

| Niveau | Exercices | Collectivités au dernier exercice | Collectivités-exercices | Valeurs lues | Valeurs absentes |
|---|---|---|---|---|---|
| communes | 26 années entre 2000 et 2025 | 34 860 | 937 985 | 48 609 722 | 13 |
| groupements à fiscalité propre | 19 années entre 2007 et 2025 | 1 273 | 35 745 | 1 787 515 | 0 |
| départements et collectivités territoriales uniques | 18 années entre 2008 et 2025 | 98 | 1 792 | 76 385 | 0 |
| régions | 18 années entre 2008 et 2025 | 14 | 350 | 13 437 | 0 |

Identités que les maquettes énoncent, de chaque collectivité : le résultat comptable (R) est la différence des produits (A) et des charges (B) de fonctionnement ; le besoin de financement de la section d'investissement (E), jusqu'en 2024, le besoin résiduel (D − C, emplois moins ressources) plus le solde des opérations pour compte de tiers, et en 2025 D − C ; le résultat d'ensemble, R − E ; la capacité d'autofinancement nette, la capacité d'autofinancement moins le remboursement des emprunts et dettes assimilées. 4 736 523 vérifiées, 4 734 762 justes, 1 761 en écart.

| Niveau | Total | Parties | Vérifiées | En écart | Exercices en écart | Plus grand écart |
|---|---|---|---|---|---|---|
| communes | RESULTAT_COMPTABLE | PRODUITS_FONCTIONNEMENT − CHARGES_FONCTIONNEMENT | 937 985 | 0 | aucun | aucun |
| communes | BESOIN_FINANCEMENT_RESIDUEL | EMPLOIS_INVESTISSEMENT − RESSOURCES_INVESTISSEMENT | 903 125 | 1 139 | 2005, 2007 et 2024 | +5 035,20 k€ : GONESSE (95277), 2024 |
| communes | BESOIN_FINANCEMENT_INVESTISSEMENT | BESOIN_FINANCEMENT_RESIDUEL + SOLDE_OPERATIONS_TIERS | 903 125 | 0 | aucun | aucun |
| communes | BESOIN_FINANCEMENT_INVESTISSEMENT | EMPLOIS_INVESTISSEMENT − RESSOURCES_INVESTISSEMENT | 34 860 | 0 | aucun | aucun |
| communes | RESULTAT_ENSEMBLE | RESULTAT_COMPTABLE − BESOIN_FINANCEMENT_INVESTISSEMENT | 937 985 | 2 | 2005 | −0,36 k€ : ROANNE (42187), 2005 |
| communes | CAF_NETTE | CAF − REMBOURSEMENTS_EMPRUNTS_DETTES | 937 985 | 194 | 14 années entre 2000 et 2025 | −2 900,00 k€ : WATTRELOS (59650), 2012 |
| groupements à fiscalité propre | RESULTAT_COMPTABLE | PRODUITS_FONCTIONNEMENT − CHARGES_FONCTIONNEMENT | 35 745 | 0 | aucun | aucun |
| groupements à fiscalité propre | CAF_NETTE | CAF − REMBOURSEMENTS_EMPRUNTS_DETTES | 35 745 | 344 | 2023, 2024 et 2025 | −9 826,00 k€ : AIX MARSEILLE PROVENCE BP MET (200054807), 2025 |
| départements et collectivités territoriales uniques | RESULTAT_COMPTABLE | PRODUITS_FONCTIONNEMENT − CHARGES_FONCTIONNEMENT | 1 792 | 0 | aucun | aucun |
| départements et collectivités territoriales uniques | BESOIN_FINANCEMENT_RESIDUEL | EMPLOIS_INVESTISSEMENT − RESSOURCES_INVESTISSEMENT | 1 694 | 72 | 2024 | +4 463,69 k€ : DEP CHARENTE-MARITIME (017), 2024 |
| départements et collectivités territoriales uniques | BESOIN_FINANCEMENT_INVESTISSEMENT | BESOIN_FINANCEMENT_RESIDUEL + SOLDE_OPERATIONS_TIERS | 1 694 | 0 | aucun | aucun |
| départements et collectivités territoriales uniques | BESOIN_FINANCEMENT_INVESTISSEMENT | EMPLOIS_INVESTISSEMENT − RESSOURCES_INVESTISSEMENT | 98 | 0 | aucun | aucun |
| départements et collectivités territoriales uniques | RESULTAT_ENSEMBLE | RESULTAT_COMPTABLE − BESOIN_FINANCEMENT_INVESTISSEMENT | 1 792 | 0 | aucun | aucun |
| départements et collectivités territoriales uniques | CAF_NETTE | CAF − REMBOURSEMENTS_EMPRUNTS_DETTES | 1 292 | 0 | aucun | aucun |
| régions | RESULTAT_COMPTABLE | PRODUITS_FONCTIONNEMENT − CHARGES_FONCTIONNEMENT | 350 | 0 | aucun | aucun |
| régions | BESOIN_FINANCEMENT_RESIDUEL | EMPLOIS_INVESTISSEMENT − RESSOURCES_INVESTISSEMENT | 336 | 10 | 2024 | +15 062,50 k€ : REG HAUTS DE FRANCE (032), 2024 |
| régions | BESOIN_FINANCEMENT_INVESTISSEMENT | BESOIN_FINANCEMENT_RESIDUEL + SOLDE_OPERATIONS_TIERS | 336 | 0 | aucun | aucun |
| régions | BESOIN_FINANCEMENT_INVESTISSEMENT | EMPLOIS_INVESTISSEMENT − RESSOURCES_INVESTISSEMENT | 14 | 0 | aucun | aucun |
| régions | RESULTAT_ENSEMBLE | RESULTAT_COMPTABLE − BESOIN_FINANCEMENT_INVESTISSEMENT | 350 | 0 | aucun | aucun |
| régions | CAF_NETTE | CAF − REMBOURSEMENTS_EMPRUNTS_DETTES | 220 | 0 | aucun | aucun |

### Les mêmes collectivités dans les comptes de l'OFGL

Chaque exercice que publient aussi les jeux de l'OFGL (section 7), chaque collectivité rapprochée de la sienne : une commune par son code Insee, un groupement par son numéro Siren, un département ou une région par son code, une collectivité territoriale unique, que l'OFGL range parmi les régions, par son code de région. Le budget principal, ou, pour les groupements, le montant consolidé des budgets principal et annexes. Un code que l'OFGL donne à plusieurs collectivités ne se rapproche pas : jusqu'en 2015, celui de la région qui a absorbé chacune des régions fusionnées en 2016 ; jusqu'en 2020, « 67A », celui du Bas-Rhin et du Haut-Rhin.

| Niveau | Exercices | Collectivités | Rapprochées | Sans correspondant | Collectivités de l'OFGL sans correspondant |
|---|---|---|---|---|---|
| communes | 8 années entre 2018 et 2025 | 279 943 | 279 857 | 86 | 8 |
| groupements à fiscalité propre | 8 années entre 2018 et 2025 | 10 163 | 10 138 | 25 | 7 |
| départements et collectivités territoriales uniques | 14 années entre 2012 et 2025 | 1 392 | 1 369 | 23 | 25 |
| régions | 14 années entre 2012 et 2025 | 246 | 182 | 64 | 64 |

Agrégats de même intitulé, ou de même objet, des deux publications, établies d'après les mêmes comptes de gestion. L'OFGL définit les siens compte par compte, en opérations réelles et hors gestion active de la dette (définitions de la DGCL) ; les maquettes de la DGFiP ne disent pas les leurs. Un agrégat que le jeu de l'OFGL publie pour d'autres collectivités de l'exercice, mais pas pour celle-ci, y vaut zéro. La part d'égaux mesure combien les deux définitions se recouvrent.

| Niveau | Comptes individuels | Comptes de l'OFGL | Exercices | Comparés | Égaux à l'arrondi près | Part | Plus grand écart (DGFiP − OFGL) |
|---|---|---|---|---|---|---|---|
| communes | CHARGES_PERSONNEL | FRAIS_PERSONNEL | 8 années entre 2018 et 2025 | 279 857 | 279 855 | 100,0 % | −2 023 € : SUZAN (09304), 2020 |
| communes | ACHATS_CHARGES_EXTERNES | ACHATS_CHARGES_EXTERNES | 8 années entre 2018 et 2025 | 279 857 | 279 832 | 100,0 % | +0,9 M€ : RAMATUELLE (83101), 2023 |
| communes | CHARGES_FINANCIERES | CHARGES_FINANCIERES | 8 années entre 2018 et 2025 | 279 857 | 279 021 | 99,7 % | +34,1 M€ : MARSEILLE (13055), 2021 |
| communes | DGF | DGF | 8 années entre 2018 et 2025 | 279 857 | 279 855 | 100,0 % | −18 530 € : SUZAN (09304), 2021 |
| communes | PRODUITS_SERVICES_DOMAINE | VENTES_BIENS_SERVICES | 8 années entre 2018 et 2025 | 279 857 | 279 850 | 100,0 % | −311 € : SAINT-JULIEN-DE-TOURSAC (15194), 2020 |
| communes | FCTVA | FCTVA | 8 années entre 2018 et 2025 | 279 857 | 279 854 | 100,0 % | +24 248 € : MEYRIEU-LES-ETANGS (38231), 2019 |
| communes | IMPOTS_LOCAUX | IMPOTS_LOCAUX | 8 années entre 2018 et 2025 | 279 857 | 7 834 | 2,8 % | −1 042,8 M€ : VILLE DE PARIS (75056), 2023 |
| communes | AUTRES_IMPOTS_TAXES | AUTRES_IMPOTS_TAXES | 8 années entre 2018 et 2025 | 279 857 | 44 975 | 16,1 % | −365,3 M€ : PARIS 01 (75056), 2018 |
| communes | FISCALITE_REVERSEE | FISCALITE_REVERSEE | 5 années entre 2021 et 2025 | 174 572 | 153 737 | 88,1 % | +110,9 M€ : VILLE DE PARIS (75056), 2025 |
| communes | PRODUITS_FONCTIONNEMENT_CAF | REC_FONCTIONNEMENT | 8 années entre 2018 et 2025 | 279 857 | 250 504 | 89,5 % | +101,5 M€ : VILLE DE PARIS (75056), 2020 |
| communes | CHARGES_FONCTIONNEMENT_CAF | DEP_FONCTIONNEMENT | 8 années entre 2018 et 2025 | 279 857 | 277 717 | 99,2 % | +52,7 M€ : BOULOGNE-BILLANCOURT (92012), 2018 |
| communes | EXCEDENT_BRUT_FONCTIONNEMENT | EPARGNE_GESTION_COURANTE | 8 années entre 2018 et 2025 | 279 857 | 251 779 | 90,0 % | +11,9 M€ : VILLE DE PARIS (75056), 2025 |
| communes | CAF | EPARGNE_BRUTE | 8 années entre 2018 et 2025 | 279 857 | 250 579 | 89,5 % | +101,5 M€ : VILLE DE PARIS (75056), 2020 |
| communes | CAF_NETTE | EPARGNE_NETTE | 8 années entre 2018 et 2025 | 279 857 | 164 813 | 58,9 % | +125,9 M€ : VILLE DE PARIS (75056), 2020 |
| communes | DEPENSES_EQUIPEMENT | DEPENSES_EQUIPEMENT | 8 années entre 2018 et 2025 | 279 857 | 155 359 | 55,5 % | +481,5 M€ : PARIS 01 (75056), 2019 |
| communes | EMPRUNTS_DETTES_ASSIMILEES | EMPRUNTS | 8 années entre 2018 et 2025 | 279 857 | 185 386 | 66,2 % | −335,3 M€ : VILLE DE PARIS (75056), 2022 |
| communes | REMBOURSEMENTS_EMPRUNTS_DETTES | REMBOURSEMENTS_DETTE | 8 années entre 2018 et 2025 | 279 857 | 179 570 | 64,2 % | +70,6 M€ : LEVALLOIS-PERRET (92044), 2018 |
| communes | ANNUITE_DETTE | ANNUITE_DETTE_CHARGES_FINANCIERES | 8 années entre 2018 et 2025 | 279 857 | 159 043 | 56,8 % | −76,2 M€ : PARIS 01 (75056), 2019 |
| communes | ENCOURS_DETTE | DETTE | 8 années entre 2018 et 2025 | 279 857 | 279 836 | 100,0 % | −1,0 M€ : KUNHEIM (68172), 2018 |
| communes | ENCOURS_DETTES_BANCAIRES | DETTE_BANCAIRE | 8 années entre 2018 et 2025 | 279 857 | 279 831 | 100,0 % | −2,1 M€ : VENCE (06157), 2020 |
| communes | FONDS_ROULEMENT | FONDS_ROULEMENT | 8 années entre 2018 et 2025 | 279 857 | 272 364 | 97,3 % | −34,9 M€ : MARSEILLE (13055), 2023 |
| groupements à fiscalité propre | CHARGES_PERSONNEL | FRAIS_PERSONNEL | 8 années entre 2018 et 2025 | 10 138 | 9 847 | 97,1 % | −7,6 M€ : CA BASSIN BRIVE (200043172), 2024 |
| groupements à fiscalité propre | ACHATS_CHARGES_EXTERNES | ACHATS_CHARGES_EXTERNES | 8 années entre 2018 et 2025 | 10 138 | 6 400 | 63,1 % | +19,2 M€ : CA GRD PARIS SUD SEINE ESS SEN (200059228), 2025 |
| groupements à fiscalité propre | CHARGES_FINANCIERES | CHARGES_FINANCIERES | 8 années entre 2018 et 2025 | 10 138 | 9 963 | 98,3 % | +16,8 M€ : CA GRD PARIS SUD SEINE ESS SEN (200059228), 2018 |
| groupements à fiscalité propre | DGF | DGF | 8 années entre 2018 et 2025 | 10 138 | 10 138 | 100,0 % | aucun |
| groupements à fiscalité propre | PRODUITS_SERVICES_DOMAINE | VENTES_BIENS_SERVICES | 8 années entre 2018 et 2025 | 10 138 | 2 819 | 27,8 % | +77,4 M€ : BORDEAUX METROPOLE (243300316), 2025 |
| groupements à fiscalité propre | FCTVA | FCTVA | 8 années entre 2018 et 2025 | 10 138 | 9 972 | 98,4 % | −0,3 M€ : CC VALLEE DES BAUX - ALPILLES (241300375), 2019 |
| groupements à fiscalité propre | IMPOTS_LOCAUX | IMPOTS_LOCAUX | 8 années entre 2018 et 2025 | 10 138 | 95 | 0,9 % | +3 413,5 M€ : METROPOLE DU GRAND PARIS (200054781), 2023 |
| groupements à fiscalité propre | AUTRES_IMPOTS_TAXES | AUTRES_IMPOTS_TAXES | 8 années entre 2018 et 2025 | 10 138 | 4 686 | 46,2 % | +361,0 M€ : MET AIX MARSEILLE PROVENCE (200054807), 2021 |
| groupements à fiscalité propre | FISCALITE_REVERSEE | FISCALITE_REVERSEE | 8 années entre 2018 et 2025 | 10 138 | 769 | 7,6 % | −345,7 M€ : MET AIX MARSEILLE PROVENCE (200054807), 2021 |
| groupements à fiscalité propre | PRODUITS_FONCTIONNEMENT_CAF | REC_FONCTIONNEMENT | 8 années entre 2018 et 2025 | 10 138 | 2 805 | 27,7 % | −115,5 M€ : METROPOLE NCA (200030195), 2023 |
| groupements à fiscalité propre | CHARGES_FONCTIONNEMENT_CAF | DEP_FONCTIONNEMENT | 8 années entre 2018 et 2025 | 10 138 | 6 061 | 59,8 % | −115,6 M€ : METROPOLE NCA (200030195), 2023 |
| groupements à fiscalité propre | CAF | EPARGNE_BRUTE | 8 années entre 2018 et 2025 | 10 138 | 2 953 | 29,1 % | +71,2 M€ : METROPOLE DU GRAND PARIS (200054781), 2025 |
| groupements à fiscalité propre | CAF_NETTE | EPARGNE_NETTE | 8 années entre 2018 et 2025 | 10 138 | 1 486 | 14,7 % | −98,7 M€ : Metropole europ de Lille (200093201), 2025 |
| groupements à fiscalité propre | DEPENSES_EQUIPEMENT | DEPENSES_EQUIPEMENT | 8 années entre 2018 et 2025 | 10 138 | 755 | 7,4 % | +319,5 M€ : AIX MARSEILLE PROVENCE BP MET (200054807), 2025 |
| groupements à fiscalité propre | EMPRUNTS_DETTES_ASSIMILEES | EMPRUNTS | 8 années entre 2018 et 2025 | 10 138 | 4 469 | 44,1 % | +99,9 M€ : Metropole europ de Lille (200093201), 2025 |
| groupements à fiscalité propre | REMBOURSEMENTS_EMPRUNTS_DETTES | REMBOURSEMENTS_DETTE | 8 années entre 2018 et 2025 | 10 138 | 3 635 | 35,9 % | +98,8 M€ : Metropole europ de Lille (200093201), 2025 |
| groupements à fiscalité propre | ANNUITE_DETTE | ANNUITE_DETTE_CHARGES_FINANCIERES | 8 années entre 2018 et 2025 | 10 138 | 2 545 | 25,1 % | +90,2 M€ : Metropole europ de Lille (200093201), 2025 |
| groupements à fiscalité propre | ENCOURS_DETTE | DETTE | 8 années entre 2018 et 2025 | 10 138 | 9 854 | 97,2 % | −46,9 M€ : AIX MARSEILLE PROVENCE BP MET (200054807), 2025 |
| groupements à fiscalité propre | ENCOURS_DETTES_BANCAIRES | DETTE_BANCAIRE | 8 années entre 2018 et 2025 | 10 138 | 10 103 | 99,7 % | −1,5 M€ : CC LAUTRECOIS-PAYS D'AGOUT (200034056), 2018 |
| départements et collectivités territoriales uniques | CHARGES_PERSONNEL | FRAIS_PERSONNEL | 14 années entre 2012 et 2025 | 1 369 | 1 368 | 99,9 % | −522 € : CTU COLLECTIVITE DE CORSE (02A), 2018 |
| départements et collectivités territoriales uniques | ACHATS_CHARGES_EXTERNES | ACHATS_CHARGES_EXTERNES | 14 années entre 2012 et 2025 | 1 369 | 1 301 | 95,0 % | +1,0 M€ : DEP HAUTE-SAVOIE (074), 2017 |
| départements et collectivités territoriales uniques | CHARGES_FINANCIERES | CHARGES_FINANCIERES | 14 années entre 2012 et 2025 | 1 369 | 1 311 | 95,8 % | +149,7 M€ : DEP RHONE (069), 2016 |
| départements et collectivités territoriales uniques | DGF | DGF | 14 années entre 2012 et 2025 | 1 369 | 1 369 | 100,0 % | aucun |
| départements et collectivités territoriales uniques | FCTVA | FCTVA | 14 années entre 2012 et 2025 | 1 369 | 1 369 | 100,0 % | aucun |
| départements et collectivités territoriales uniques | IMPOTS_LOCAUX | IMPOTS_LOCAUX | 13 années entre 2013 et 2025 | 1 271 | 779 | 61,3 % | +898,2 M€ : DEP PARIS (075), 2013 |
| départements et collectivités territoriales uniques | AUTRES_IMPOTS_TAXES | AUTRES_IMPOTS_TAXES | 14 années entre 2012 et 2025 | 1 369 | 967 | 70,6 % | +55,4 M€ : DEP PARIS (075), 2016 |
| départements et collectivités territoriales uniques | TICPE | TICPE | 2012 | 98 | 98 | 100,0 % | aucun |
| départements et collectivités territoriales uniques | CVAE | CVAE | 11 années entre 2012 et 2022 | 1 078 | 103 | 9,6 % | +15,6 M€ : CTG COLLECTIVITE TERRITORIALE GUYANE (102), 2016 |
| départements et collectivités territoriales uniques | PRODUITS_FONCTIONNEMENT_CAF | REC_FONCTIONNEMENT | 9 années entre 2017 et 2025 | 876 | 433 | 49,4 % | +73,7 M€ : DEP BOUCHES-DU-RHONE (013), 2020 |
| départements et collectivités territoriales uniques | CHARGES_FONCTIONNEMENT_CAF | DEP_FONCTIONNEMENT | 9 années entre 2017 et 2025 | 876 | 754 | 86,1 % | +48,8 M€ : COLLECTIVITE DE CORSE (02A), 2020 |
| départements et collectivités territoriales uniques | EXCEDENT_BRUT_FONCTIONNEMENT | EPARGNE_GESTION_COURANTE | 13 années entre 2013 et 2025 | 1 271 | 640 | 50,4 % | −52,1 M€ : DEP VAR (083), 2025 |
| départements et collectivités territoriales uniques | CAF | EPARGNE_BRUTE | 14 années entre 2012 et 2025 | 1 369 | 645 | 47,1 % | +112,9 M€ : DEP REUNION (104), 2013 |
| départements et collectivités territoriales uniques | CAF_NETTE | EPARGNE_NETTE | 13 années entre 2013 et 2025 | 1 271 | 358 | 28,2 % | −187,5 M€ : DEP RHONE (069), 2016 |
| départements et collectivités territoriales uniques | DEPENSES_EQUIPEMENT | DEPENSES_EQUIPEMENT | 13 années entre 2013 et 2025 | 1 271 | 118 | 9,3 % | +185,5 M€ : DEP HAUTS-DE-SEINE (092), 2015 |
| départements et collectivités territoriales uniques | SUBVENTIONS_EQUIPEMENT_VERSEES | SUBVENTIONS_EQUIPEMENT_VERSEES | 14 années entre 2012 et 2025 | 1 369 | 779 | 56,9 % | +74,3 M€ : DEP GARD (030), 2013 |
| départements et collectivités territoriales uniques | EMPRUNTS_DETTES_ASSIMILEES | EMPRUNTS | 13 années entre 2013 et 2025 | 1 271 | 811 | 63,8 % | +298,6 M€ : DEP RHONE (069), 2016 |
| départements et collectivités territoriales uniques | REMBOURSEMENTS_EMPRUNTS_DETTES | REMBOURSEMENTS_DETTE | 13 années entre 2013 et 2025 | 1 271 | 755 | 59,4 % | +187,5 M€ : DEP RHONE (069), 2016 |
| départements et collectivités territoriales uniques | ANNUITE_DETTE | ANNUITE_DETTE_CHARGES_FINANCIERES | 13 années entre 2013 et 2025 | 1 271 | 139 | 10,9 % | +181,2 M€ : DEP RHONE (069), 2016 |
| départements et collectivités territoriales uniques | ENCOURS_DETTE | DETTE | 9 années entre 2017 et 2025 | 876 | 876 | 100,0 % | aucun |
| départements et collectivités territoriales uniques | ENCOURS_DETTES_BANCAIRES | DETTE_BANCAIRE | 14 années entre 2012 et 2025 | 1 369 | 1 324 | 96,7 % | −236,9 M€ : DEP SEINE-SAINT-DENIS (093), 2014 |
| départements et collectivités territoriales uniques | FONDS_ROULEMENT | FONDS_ROULEMENT | 13 années entre 2013 et 2025 | 1 271 | 668 | 52,6 % | +237,7 M€ : CTU COLLECTIVITE TERRITORIALE GUYANE (102), 2018 |
| régions | CHARGES_PERSONNEL | FRAIS_PERSONNEL | 14 années entre 2012 et 2025 | 182 | 182 | 100,0 % | aucun |
| régions | ACHATS_CHARGES_EXTERNES | ACHATS_CHARGES_EXTERNES | 14 années entre 2012 et 2025 | 182 | 182 | 100,0 % | aucun |
| régions | CHARGES_FINANCIERES | CHARGES_FINANCIERES | 14 années entre 2012 et 2025 | 182 | 163 | 89,6 % | +82,4 M€ : COLLECTIVITE TERRITORIALE DE CORSE (094), 2015 |
| régions | DGF | DGF | 14 années entre 2012 et 2025 | 182 | 182 | 100,0 % | aucun |
| régions | FCTVA | FCTVA | 14 années entre 2012 et 2025 | 182 | 182 | 100,0 % | aucun |
| régions | IMPOTS_LOCAUX | IMPOTS_LOCAUX | 13 années entre 2013 et 2025 | 172 | 111 | 64,5 % | +674,8 M€ : REG ILE-DE-FRANCE (011), 2013 |
| régions | AUTRES_IMPOTS_TAXES | AUTRES_IMPOTS_TAXES | 14 années entre 2012 et 2025 | 182 | 160 | 87,9 % | −9,4 M€ : REGION REUNION (104), 2021 |
| régions | TICPE | TICPE | 14 années entre 2012 et 2025 | 182 | 142 | 78,0 % | −102,2 M€ : REG ILE-DE-FRANCE (011), 2015 |
| régions | CVAE | CVAE | 9 années entre 2012 et 2020 | 112 | 12 | 10,7 % | +8,5 M€ : REG GUADELOUPE (101), 2012 |
| régions | PRODUITS_FONCTIONNEMENT_CAF | REC_FONCTIONNEMENT | 9 années entre 2017 et 2025 | 127 | 82 | 64,6 % | +37,0 M€ : REG PROVENCE-ALPES-COTE-D'AZUR (093), 2020 |
| régions | CHARGES_FONCTIONNEMENT_CAF | DEP_FONCTIONNEMENT | 9 années entre 2017 et 2025 | 127 | 107 | 84,3 % | +6,1 M€ : REG OCCITANIE (076), 2024 |
| régions | EXCEDENT_BRUT_FONCTIONNEMENT | EPARGNE_GESTION_COURANTE | 13 années entre 2013 et 2025 | 172 | 117 | 68,0 % | +7,3 M€ : REG HAUTS DE FRANCE (032), 2025 |
| régions | CAF | EPARGNE_BRUTE | 13 années entre 2013 et 2025 | 172 | 96 | 55,8 % | +35,8 M€ : REG PROVENCE-ALPES-COTE-D'AZUR (093), 2020 |
| régions | CAF_NETTE | EPARGNE_NETTE | 13 années entre 2013 et 2025 | 172 | 66 | 38,4 % | −81,7 M€ : REG OCCITANIE (076), 2022 |
| régions | DEPENSES_EQUIPEMENT | DEPENSES_EQUIPEMENT | 13 années entre 2013 et 2025 | 172 | 23 | 13,4 % | +427,9 M€ : REG PROVENCE-ALPES-COTE-D'AZUR (093), 2025 |
| régions | SUBVENTIONS_EQUIPEMENT_VERSEES | SUBVENTIONS_EQUIPEMENT_VERSEES | 14 années entre 2012 et 2025 | 182 | 111 | 61,0 % | −102,2 M€ : REG NORMANDIE (028), 2022 |
| régions | EMPRUNTS_DETTES_ASSIMILEES | EMPRUNTS | 13 années entre 2013 et 2025 | 172 | 82 | 47,7 % | +127,3 M€ : COLLECTIVITE TERRITORIALE DE CORSE (094), 2015 |
| régions | REMBOURSEMENTS_EMPRUNTS_DETTES | REMBOURSEMENTS_DETTE | 13 années entre 2013 et 2025 | 172 | 100 | 58,1 % | +81,7 M€ : REG OCCITANIE (076), 2022 |
| régions | ANNUITE_DETTE | ANNUITE_DETTE_CHARGES_FINANCIERES | 13 années entre 2013 et 2025 | 172 | 11 | 6,4 % | −146,3 M€ : REG PROVENCE-ALPES-COTE-D'AZUR (093), 2024 |
| régions | ENCOURS_DETTE | DETTE | 13 années entre 2013 et 2025 | 172 | 172 | 100,0 % | aucun |
| régions | ENCOURS_DETTES_BANCAIRES | DETTE_BANCAIRE | 10 années entre 2012 et 2025 | 137 | 131 | 95,6 % | +41,3 M€ : REG CENTRE (024), 2012 |
| régions | FONDS_ROULEMENT | FONDS_ROULEMENT | 13 années entre 2013 et 2025 | 172 | 98 | 57,0 % | +146,9 M€ : REG PROVENCE-ALPES-COTE-D'AZUR (093), 2022 |

## 14. Balances des comptes de l'État

Les balances générales des comptes de l'État que publie la DGFiP, telles qu'à la clôture de chaque exercice elles ont servi à produire le compte général de l'État : une ligne par compte, mission, programme et nature budgétaire, avec son solde de sortie, au centime, un solde créditeur étant négatif. Les comptes de charges et de produits n'y sont pas soldés : leur somme est le résultat de l'exercice, ici un déficit quand elle est positive. Chaque balance doit s'équilibrer, et les engagements hors bilan (classe 8) avec leur contrepartie.

| Exercice | Lignes | Comptes | Comptes absents du plan comptable joint | Somme des soldes | Somme des engagements hors bilan | Charges et produits réunis |
|---|---|---|---|---|---|---|
| 2016 | 48 517 | 1 913 | 0 | 0,00 € | 0,00 € | +75 602,5 M€ |
| 2017 | 49 327 | 1 919 | 0 | 0,00 € | 0,00 € | +60 958,0 M€ |
| 2018 | 50 156 | 1 952 | 0 | 0,00 € | 0,00 € | +51 873,3 M€ |
| 2019 | 51 433 | 1 971 | 0 | 0,00 € | 0,00 € | +84 637,8 M€ |
| 2020 | 50 903 | 1 991 | 0 | 0,00 € | 0,00 € | +165 601,4 M€ |
| 2021 | 52 111 | 1 986 | 0 | 0,00 € | 0,00 € | +142 088,2 M€ |
| 2022 | 53 181 | 1 992 | 0 | 0,00 € | 0,00 € | +160 027,5 M€ |
| 2023 | 53 352 | 1 993 | 0 | 0,00 € | 0,00 € | +124 929,9 M€ |
| 2024 | 54 414 | 2 006 | 0 | 0,00 € | 0,00 € | +123 703,9 M€ |
| 2025 | 54 095 | 2 050 | 9 | 0,00 € | 0,00 € | +129 467,1 M€ |

Engagements hors bilan de l'État, en milliards d'euros, au signe de leur présentation (un engagement donné, solde créditeur, est positif) :

| Indicateur | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| S801_Dette garantie par l'Etat | 195,2 | 204,4 | 210,6 | 205,4 | 319,7 | 319,1 | 302,1 | 281,2 | 257,5 | 237,1 |
| S802_Garanties liées à des missions d'int gén | 11,9 | 10,9 | 519,0 | 530,8 | 566,0 | 591,1 | 642,5 | 728,2 | 770,4 | 794,4 |
| S803_Garanties de passif | 43,7 | 42,0 | 37,2 | 38,2 | 37,7 | 35,8 | 29,6 | 28,2 | 27,6 | 26,1 |
| S804_Engagements financiers de l'Etat | 68,2 | 65,8 | 87,5 | 135,2 | 112,5 | 122,8 | 147,4 | 240,0 | 189,8 | 198,5 |
| S805_Dispositifs d'intervention | 570,9 | 616,3 | 639,0 | 720,6 | 871,9 | 933,0 | 609,2 | 678,8 | 571,0 | 461,0 |
| S806_Engagements reçus | 15,6 | 16,7 | 21,3 | 24,5 | 27,2 | 58,2 | 70,1 | 53,2 | 45,4 | 45,8 |
| S899_Contrepartie des engagements | 874,2 | 922,7 | 1 472,0 | 1 605,7 | 1 880,5 | 1 943,6 | 1 660,6 | 1 903,3 | 1 770,9 | 1 671,5 |

Le bilan et le compte de résultat que donne chaque balance, par les indicateurs de synthèse que la DGFiP rattache aux lignes des états financiers (tables/indicateurs_balances_etat.csv), contre ceux de la loi d'approbation des comptes de l'exercice, ligne par ligne et total par total, en millions d'euros. Une ligne de la loi est exacte au demi-million près ; la situation nette que donne la balance est l'actif moins le passif. 1 251 lignes comparées, 1 108 égales à l'arrondi près.

| Exercice | Lignes comparées | Égales | Autres |
|---|---|---|---|
| 2016 | 124 | 106 | 18 |
| 2017 | 124 | 107 | 17 |
| 2018 | 124 | 107 | 17 |
| 2019 | 124 | 112 | 12 |
| 2020 | 124 | 114 | 10 |
| 2021 | 126 | 107 | 19 |
| 2022 | 127 | 107 | 20 |
| 2023 | 127 | 111 | 16 |
| 2024 | 127 | 120 | 7 |
| 2025 | 124 | 117 | 7 |

Lignes qui diffèrent, et ce qui l'explique quand le calcul le montre : le report des exercices antérieurs de la loi qui comprend le solde des opérations de l'exercice (le bilan y est présenté après son affectation) ; un reclassement entre les lignes d'un même total, que la loi donne alors égal à celui de la balance ; une compensation de créances et de dettes, quand l'actif et le passif de la loi sont moindres d'un même montant, la situation nette restant juste ; une ligne que la balance ne distingue pas. Le montant brut d'un actif n'est pas répété quand sa ligne nette porte le même écart.

| Exercice | Ligne | Loi | Balance | Écart (loi − balance) | Explication |
|---|---|---|---|---|---|
| 2016 | AUTRES_CREANCES | 17 087 | 17 084,9 | +2,1 | reclassement entre les composantes de CREANCES, total juste |
| 2016 | AUTRES_DETTES_NON_FINANCIERES | 121 646 | 121 972,7 | −326,7 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2016 | CREANCES_CLIENTS | 2 938 | 2 457,2 | +480,8 | reclassement entre les composantes de CREANCES, total juste |
| 2016 | CREANCES_REDEVABLES | 64 791 | 64 783,9 | +7,1 | reclassement entre les composantes de CREANCES, total juste |
| 2016 | DETTES_FONCTIONNEMENT | 7 753 | 7 945,0 | −192,0 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2016 | DETTES_INTERVENTION | 16 790 | 16 247,9 | +542,1 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2016 | FONDS_BANCAIRES_CAISSE | 12 162 | 12 213,9 | −51,9 | reclassement entre les composantes de TRESORERIE_ACTIF, total juste |
| 2016 | REPORT_EXERCICES_ANTERIEURS | −1 549 863 | −1 474 260,7 | −75 602,3 | la loi y ajoute le solde des opérations de l'exercice |
| 2016 | RESSOURCE_PROPRE_UE_RNB | −15 722 | — | — | la balance ne distingue pas cette ligne |
| 2016 | RESSOURCE_PROPRE_UE_TVA | −4 720 | — | — | la balance ne distingue pas cette ligne |
| 2016 | TRANSFERTS_AUTRES_COLLECTIVITES | 25 370 | 25 372,7 | −2,7 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2016 | TRANSFERTS_ENTREPRISES | 16 270 | 16 267,5 | +2,5 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2016 | VALEURS_ESCOMPTEES | −2 751 | −2 803,4 | +52,4 | reclassement entre les composantes de TRESORERIE_ACTIF, total juste |
| 2017 | AUTRES_CREANCES | 15 908 | 15 907,4 | +0,6 | reclassement entre les composantes de CREANCES, total juste |
| 2017 | AUTRES_DETTES_NON_FINANCIERES | 137 685 | 138 212,0 | −527,0 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2017 | CREANCES_CLIENTS | 2 135 | 2 031,3 | +103,7 | reclassement entre les composantes de CREANCES, total juste |
| 2017 | CREANCES_REDEVABLES | 67 112 | 67 104,1 | +7,9 | reclassement entre les composantes de CREANCES, total juste |
| 2017 | DETTES_FONCTIONNEMENT | 7 619 | 7 606,4 | +12,6 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2017 | DETTES_INTERVENTION | 16 122 | 15 591,0 | +531,0 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2017 | FONDS_BANCAIRES_CAISSE | 20 763 | 21 242,8 | −479,8 | reclassement entre les composantes de TRESORERIE_ACTIF, total juste |
| 2017 | REPORT_EXERCICES_ANTERIEURS | −1 611 274 | −1 550 315,9 | −60 958,1 | la loi y ajoute le solde des opérations de l'exercice |
| 2017 | RESSOURCE_PROPRE_UE_RNB | −11 953 | — | — | la balance ne distingue pas cette ligne |
| 2017 | RESSOURCE_PROPRE_UE_TVA | −4 422 | — | — | la balance ne distingue pas cette ligne |
| 2017 | TRANSFERTS_AUTRES_COLLECTIVITES | 24 305 | 24 307,5 | −2,5 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2017 | TRANSFERTS_ENTREPRISES | 18 750 | 18 747,7 | +2,3 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2017 | VALEURS_ESCOMPTEES | −1 934 | −2 413,5 | +479,5 | reclassement entre les composantes de TRESORERIE_ACTIF, total juste |
| 2018 | AUTRES_CREANCES_BRUT | 17 169 | 17 168,4 | +0,6 | reclassement entre les composantes de CREANCES_BRUT, total juste |
| 2018 | AUTRES_DETTES_NON_FINANCIERES | 138 759 | 139 305,6 | −546,6 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2018 | CREANCES_CLIENTS | 1 764 | 1 682,1 | +81,9 | reclassement entre les composantes de CREANCES, total juste |
| 2018 | CREANCES_REDEVABLES | 69 354 | 69 341,5 | +12,5 | reclassement entre les composantes de CREANCES, total juste |
| 2018 | DETTES_FONCTIONNEMENT | 7 552 | 7 543,8 | +8,2 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2018 | DETTES_INTERVENTION | 13 195 | 12 644,3 | +550,7 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2018 | FONDS_BANCAIRES_CAISSE | 31 464 | 32 514,3 | −1 050,3 | reclassement entre les composantes de TRESORERIE_ACTIF, total juste |
| 2018 | REPORT_EXERCICES_ANTERIEURS | −1 663 382 | −1 611 508,6 | −51 873,4 | la loi y ajoute le solde des opérations de l'exercice |
| 2018 | RESSOURCE_PROPRE_UE_RNB | −16 124 | — | — | la balance ne distingue pas cette ligne |
| 2018 | RESSOURCE_PROPRE_UE_TVA | −4 518 | — | — | la balance ne distingue pas cette ligne |
| 2018 | TRANSFERTS_AUTRES_COLLECTIVITES | 23 033 | 23 037,2 | −4,2 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2018 | TRANSFERTS_ENTREPRISES | 18 051 | 18 046,3 | +4,7 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2018 | VALEURS_ESCOMPTEES | 8 | −1 043,2 | +1 051,2 | reclassement entre les composantes de TRESORERIE_ACTIF, total juste |
| 2019 | AUTRES_DETTES_NON_FINANCIERES | 154 497 | 155 232,6 | −735,6 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2019 | CREANCES_CLIENTS | 1 521 | 1 427,9 | +93,1 | reclassement entre les composantes de CREANCES, total juste |
| 2019 | CREANCES_REDEVABLES | 76 179 | 76 170,7 | +8,3 | reclassement entre les composantes de CREANCES, total juste |
| 2019 | DETTES_FONCTIONNEMENT | 7 943 | 7 938,2 | +4,8 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2019 | DETTES_INTERVENTION | 9 528 | 8 787,4 | +740,6 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2019 | REPORT_EXERCICES_ANTERIEURS | −1 748 246 | −1 663 608,1 | −84 637,9 | la loi y ajoute le solde des opérations de l'exercice |
| 2019 | RESSOURCE_PROPRE_UE_RNB | −16 373 | — | — | la balance ne distingue pas cette ligne |
| 2019 | RESSOURCE_PROPRE_UE_TVA | −4 649 | — | — | la balance ne distingue pas cette ligne |
| 2019 | TRANSFERTS_AUTRES_COLLECTIVITES | 23 905 | 23 909,6 | −4,6 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2019 | TRANSFERTS_ENTREPRISES | 17 042 | 17 037,7 | +4,3 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2020 | AUTRES_DETTES_NON_FINANCIERES | 140 682 | 141 691,9 | −1 009,9 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2020 | CREANCES_CLIENTS | 1 217 | 1 219,3 | −2,3 | reclassement entre les composantes de CREANCES, total juste |
| 2020 | DETTES_FONCTIONNEMENT | 7 351 | 7 343,1 | +7,9 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2020 | DETTES_INTERVENTION | 15 086 | 14 071,6 | +1 014,4 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2020 | REPORT_EXERCICES_ANTERIEURS | −1 913 987 | −1 748 385,9 | −165 601,1 | la loi y ajoute le solde des opérations de l'exercice |
| 2020 | RESSOURCE_PROPRE_UE_RNB | −18 893 | — | — | la balance ne distingue pas cette ligne |
| 2020 | RESSOURCE_PROPRE_UE_TVA | −4 796 | — | — | la balance ne distingue pas cette ligne |
| 2020 | TRANSFERTS_AUTRES_COLLECTIVITES | 25 165 | 25 263,4 | −98,4 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2020 | TRANSFERTS_ENTREPRISES | 57 765 | 57 666,0 | +99,0 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2021 | ACTIF | 1 223 749 | 1 223 791,2 | −42,2 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 42,2 M€ |
| 2021 | ACTIF_CIRCULANT | 146 781 | 146 822,3 | −41,3 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 42,2 M€ |
| 2021 | AUTRES_CREANCES | 28 281 | 28 323,1 | −42,1 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 42,2 M€ |
| 2021 | AUTRES_DETTES_NON_FINANCIERES | 151 291 | 152 314,5 | −1 023,5 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2021 | CREANCES | 107 872 | 107 914,0 | −42,0 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 42,2 M€ |
| 2021 | CREANCES_CLIENTS | 2 560 | 2 563,7 | −3,7 | reclassement entre les composantes de CREANCES, qui porte la compensation |
| 2021 | CREANCES_REDEVABLES | 77 031 | 77 030,3 | +0,7 | reclassement entre les composantes de CREANCES, qui porte la compensation |
| 2021 | DETTES_FONCTIONNEMENT | 7 352 | 7 345,6 | +6,4 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2021 | DETTES_INTERVENTION | 12 854 | 11 869,0 | +985,0 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2021 | DETTES_NON_FINANCIERES | 297 656 | 297 697,7 | −41,7 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 42,2 M€ |
| 2021 | PASSIF | 2 881 375 | 2 881 417,1 | −42,1 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 42,2 M€ |
| 2021 | REPORT_EXERCICES_ANTERIEURS | −2 058 376 | −1 916 287,9 | −142 088,1 | la loi y ajoute le solde des opérations de l'exercice |
| 2021 | TRANSFERTS_AUTRES_COLLECTIVITES | 28 109 | 28 533,6 | −424,6 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2021 | TRANSFERTS_ENTREPRISES | 68 787 | 68 362,5 | +424,5 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2022 | ACTIF | 1 284 166 | 1 284 187,0 | −21,0 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 21,0 M€ |
| 2022 | ACTIF_CIRCULANT | 171 233 | 171 253,4 | −20,4 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 21,0 M€ |
| 2022 | AUTRES_CREANCES | 35 203 | 35 223,9 | −20,9 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 21,0 M€ |
| 2022 | AUTRES_DETTES_NON_FINANCIERES | 159 066 | 160 048,4 | −982,4 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2022 | CREANCES | 114 757 | 114 777,2 | −20,2 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 21,0 M€ |
| 2022 | CREANCES_CLIENTS | 2 894 | 2 893,1 | +0,9 | reclassement entre les composantes de CREANCES, qui porte la compensation |
| 2022 | CREANCES_REDEVABLES | 76 659 | 76 664,6 | −5,6 | reclassement entre les composantes de CREANCES, qui porte la compensation |
| 2022 | DETTES_FONCTIONNEMENT | 8 246 | 8 240,1 | +5,9 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2022 | DETTES_INTERVENTION | 10 974 | 10 005,7 | +968,3 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2022 | DETTES_NON_FINANCIERES | 298 304 | 298 324,6 | −20,6 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 21,0 M€ |
| 2022 | PASSIF | 3 042 097 | 3 042 118,2 | −21,2 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 21,0 M€ |
| 2022 | REPORT_EXERCICES_ANTERIEURS | −2 076 536 | −1 916 508,9 | −160 027,1 | la loi y ajoute le solde des opérations de l'exercice |
| 2022 | TRANSFERTS_AUTRES_COLLECTIVITES | 30 969 | 31 183,8 | −214,8 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2022 | TRANSFERTS_ENTREPRISES | 39 547 | 39 332,2 | +214,8 | reclassement entre les composantes de CHARGES_INTERVENTION, total juste |
| 2023 | ACTIF | 1 294 468 | 1 294 478,2 | −10,2 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 10,2 M€ |
| 2023 | ACTIF_CIRCULANT | 204 259 | 204 269,3 | −10,3 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 10,2 M€ |
| 2023 | AUTRES_CREANCES | 25 912 | 25 922,1 | −10,1 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 10,2 M€ |
| 2023 | AUTRES_DETTES_NON_FINANCIERES | 153 185 | 154 196,1 | −1 011,1 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2023 | CREANCES | 113 344 | 113 354,5 | −10,5 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 10,2 M€ |
| 2023 | CREANCES_CLIENTS | 8 533 | 8 533,8 | −0,8 | reclassement entre les composantes de CREANCES, qui porte la compensation |
| 2023 | DETTES_FONCTIONNEMENT | 10 218 | 10 213,3 | +4,7 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2023 | DETTES_INTERVENTION | 10 961 | 9 955,9 | +1 005,1 | reclassement entre les composantes de DETTES_NON_FINANCIERES, qui porte la compensation |
| 2023 | DETTES_NON_FINANCIERES | 283 189 | 283 199,8 | −10,8 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 10,2 M€ |
| 2023 | PASSIF | 3 169 568 | 3 169 578,1 | −10,1 | compensation de créances et de dettes : la loi a l'actif et le passif moindres de 10,2 M€ |
| 2023 | REPORT_EXERCICES_ANTERIEURS | −2 041 365 | −1 916 435,1 | −124 929,9 | la loi y ajoute le solde des opérations de l'exercice |
| 2024 | AUTRES_DETTES_NON_FINANCIERES | 150 648 | 151 536,6 | −888,6 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2024 | CREANCES_CLIENTS | 2 642 | 2 640,0 | +2,0 | reclassement entre les composantes de CREANCES, total juste |
| 2024 | CREANCES_REDEVABLES | 81 308 | 81 309,0 | −1,0 | reclassement entre les composantes de CREANCES, total juste |
| 2024 | DETTES_FONCTIONNEMENT | 11 391 | 11 386,3 | +4,7 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2024 | DETTES_INTERVENTION | 11 122 | 10 229,0 | +893,0 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2024 | REPORT_EXERCICES_ANTERIEURS | −2 047 770 | −1 924 066,3 | −123 703,7 | la loi y ajoute le solde des opérations de l'exercice |
| 2025 | AUTRES_CREANCES_BRUT | 33 145 | 33 144,1 | +0,9 | reclassement entre les composantes de CREANCES_BRUT, total juste |
| 2025 | AUTRES_DETTES_NON_FINANCIERES | 163 563 | 163 559,1 | +3,9 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |
| 2025 | CREANCES_CLIENTS | 3 033 | 3 032,0 | +1,0 | reclassement entre les composantes de CREANCES, total juste |
| 2025 | CREANCES_REDEVABLES | 80 229 | 80 223,0 | +6,0 | reclassement entre les composantes de CREANCES, total juste |
| 2025 | DETTES_FONCTIONNEMENT | 11 513 | 11 501,0 | +12,0 | reclassement entre les composantes de DETTES_NON_FINANCIERES, total juste |

En 2025, la situation nette de la loi comprend le solde des opérations de l'exercice (−129 467 M€) sans qu'aucune de ses lignes le porte : la balance, dont la situation nette (l'actif moins le passif) est celle de la loi, le laisse dans les comptes de charges et de produits, et la somme des lignes de la loi s'écarte de son total d'autant (section 1).
