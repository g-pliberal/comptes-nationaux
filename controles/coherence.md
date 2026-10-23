# Cohérence des chiffres enregistrés

Fichier généré par `outils/controler_coherence.py` à partir de la base : ne pas le modifier à la main.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la demi-unité de la dernière décimale de chaque valeur en jeu, ou l'unité entière pour l'OFGL, qui arrondit ou tronque selon les cas ses montants à l'euro ; un nombre de budgets n'est pas arrondi et doit être exact. Une incohérence signalée ici est un constat sur la source, pas une erreur d'enregistrement : chaque chiffre a été relu dans sa copie archivée.

## Les sources contrôlées

Pour chaque chiffre, la version la plus récente enregistrée chez sa source.

| Source | Titre | Version la plus récente | Chiffres |
|---|---|---|---|
| dgcl.finances-departements | Les finances des départements : comptes de gestion de chaque département, de la métropole de Lyon, de la Ville de Paris et des collectivités territoriales uniques | 2025-12-29 | 19798 |
| dgcl.finances-regions | Les finances des régions : comptes de gestion de chaque région et des collectivités territoriales uniques | 2025-12-29 | 4070 |
| eurostat.gov_10a_exp | Dépenses des administrations publiques par fonction (COFOG) | 2026-10-21 | 1290 |
| eurostat.gov_10a_main | Recettes, dépenses et principaux agrégats des administrations publiques | 2026-10-21 | 1488 |
| eurostat.nama_10_gdp | PIB et principaux agrégats | 2026-10-21 | 102 |
| insee.bdm-comptes-etat | Situation mensuelle du budget de l'État : dépenses, recettes, solde des comptes spéciaux et solde général d'exécution, cumulés depuis le début de l'année (Banque de données macro-économiques, jeu COMPTES-ETAT) | 2026-10-06 | 848 |
| insee.t3101 | Tableau 3.101 : Dette des administrations publiques (S13) au sens de Maastricht et sa répartition par sous-secteur | 2026-07-28 | 624 |
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
| insee.t3216 | Tableau 3.216 : Prélèvements obligatoires par sous-secteurs des administrations publiques et pour l'Union européenne | 2026-05-10 | 1290 |
| insee.t3217 | Tableau 3.217 : Principaux impôts par catégorie | 2026-05-10 | 2655 |
| insee.t3301 | Tableau 3.301 : Dépenses des administrations publiques (S13) ventilées par fonction | 2025-11-28 | 21256 |
| insee.t3302 | Tableau 3.302 : Dépenses de l'administration publique centrale (S1311) ventilées par fonction | 2025-11-28 | 19998 |
| insee.t3303 | Tableau 3.303 : Dépenses de l'État (S13111) ventilées par fonction | 2025-11-28 | 9956 |
| insee.t3304 | Tableau 3.304 : Dépenses des organismes divers d'administration centrale (S13112) ventilées par fonction | 2025-11-28 | 8494 |
| insee.t3305 | Tableau 3.305 : Dépenses des administrations publiques locales (S1313) ventilées par fonction | 2025-11-28 | 18857 |
| insee.t3306 | Tableau 3.306 : Dépenses des administrations de sécurité sociale (S1314) ventilées par fonction | 2025-11-28 | 11594 |
| insee.t3307 | Tableau 3.307 : Répartition par sous-secteur des dépenses consolidées des administrations publiques ventilées par fonction | 2025-11-28 | 5968 |
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

20550 sommes vérifiées avec toutes leurs composantes : 20488 justes, 62 en écart.

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
| senat.pjl13-759 | ETAT_LF | ensemble | 2013 | LOLF.COMPTES_COMMERCE_SOLDE | 0,1368 Md€ | 0,2654 Md€ | −128,6 M€ |
| senat.pjl15-128 | SECU_LFSS | ensemble | 2014 | COMPTES_SECU.ACTIF_CIRCULANT | 69,7000 Md€ | 69,3000 Md€ | +400,0 M€ |
| senat.pjl15-128 | SECU_LFSS | ensemble | 2014 | COMPTES_SECU.PASSIF_FINANCIER | 179,9000 Md€ | 177,0000 Md€ | +2 900,0 M€ |
| senat.pjl19-505 | ETAT_LF | ensemble | 2019 | LOLF.CS_ENSEMBLE_SOLDES_CREDITEURS | 23,3199 Md€ | 24,5853 Md€ | −1 265,4 M€ |
| senat.pjl25-726 | ETAT_CGE | ensemble | 2025 | COMPTES_ETAT.SITUATION_NETTE | −2 115,8890 Md€ | −1 986,4230 Md€ | −129 466,0 M€ |
| senat.pjl25-726 | ETAT_LF | ensemble | 2025 | LOLF.CS_ENSEMBLE_SOLDES_CREDITEURS | 16,0862 Md€ | 16,0902 Md€ | −4,0 M€ |
| senat.tas22-018 | REGIME_GENERAL_HORS_FSV | ensemble | 2021 | COMPTES_SECU.RESULTAT_COMPTABLE | −27,7000 Md€ | −22,8000 Md€ | −4 900,0 M€ |
| senat.tas22-018 | REGIME_GENERAL_HORS_FSV | COMPTES_SECU.MALADIE | 2021 | COMPTES_SECU.RESULTAT_COMPTABLE | −28,7000 Md€ | −29,7000 Md€ | +1 000,0 M€ |

11116 sommes ont des parties que la source ne diffuse pas (cellule vide ou marquée non disponible). Pour 11111 d'entre elles, les parties diffusées suffisent à retrouver le total à l'arrondi près : les parties absentes y sont nulles ou négligeables. Pour les 5 autres, elles ne suffisent pas : des parties absentes ne sont pas nulles.

| Source | Périmètre | Total | Fonction | Années | Plus grand reste (total − parties diffusées) |
|---|---|---|---|---|---|
| insee.t3107 | S13111 | INSEE_PASSAGES.ETAT_DROITS_CONSTATES | ensemble | 2023 | −1 300,0 M€ en 2023 |
| insee.t3107 | S13111 | INSEE_PASSAGES.ETAT_NON_BUDGETAIRES | ensemble | 2019, 2020, 2021 et 2024 | −2 600,0 M€ en 2021 |

## 2. Ventilations par fonction

Pour une même grandeur, l'ensemble des fonctions contre la somme des divisions de la COFOG, des missions du budget général de l'État ou de ses comptes (budgets annexes, comptes spéciaux), ou des branches de la sécurité sociale, chaque division contre la somme de ses groupes, chaque mission ou compte contre celle de ses programmes. Pour les branches, seul le solde s'additionne : les recettes et les dépenses de l'ensemble des branches excluent les transferts entre elles, que comptent celles de chaque branche.

19649 ventilations vérifiées avec toutes leurs parties : 19647 justes, 2 en écart.

| Source | Périmètre | Grandeur | Fonction | Années en écart | Plus grand écart (total − somme) |
|---|---|---|---|---|---|
| senat.pjl16-643 | ETAT_LF | LOLF.BA_DEPENSES | ensemble | 2016 | +0,6 M€ en 2016 |
| senat.pjl16-643 | ETAT_LF | LOLF.BA_RECETTES | ensemble | 2016 | +0,6 M€ en 2016 |

834 ventilations ont des parties que la source ne diffuse pas (cellule vide ou marquée non disponible). Pour toutes, les parties diffusées suffisent à retrouver le total à l'arrondi près : les parties absentes y sont nulles ou négligeables.

## 3. Additivité des sous-secteurs

Le solde d'un ensemble, ses prélèvements obligatoires, ou sa dépense consolidée au niveau de l'ensemble des administrations publiques (tableau 3.307 de l'Insee), contre la somme de ceux de ses parties ; pour la sécurité sociale, le résultat du régime général et celui des régimes de base, Fonds de solidarité vieillesse compris, contre la somme des leurs et de celui du FSV, et chaque poste de la situation patrimoniale (annexe A des lois de financement) contre la somme de ses lignes par entité ; pour les collectivités locales, dont la source ne consolide pas les montants entre niveaux, chaque montant d'un niveau contre la somme de ceux des niveaux qui le composent, et celui des groupements à fiscalité propre contre la somme de leurs types (annexes 2A et 2B des rapports de l'OFGL, budgets principaux et budgets annexes), le nombre de budgets de l'ensemble des collectivités contre la somme de ceux de ses niveaux, chaque total des publications de la DGCL contre la somme de ses départements ou de ses régions.

6525 additions vérifiées : 6482 justes, 43 en écart.

| Tableaux | Grandeur | Ensemble | Parties | Fonctions | Années en écart | Plus grand écart |
|---|---|---|---|---|---|---|
| dgcl.finances-departements | COMPTES_LOCAUX.REMBOURSEMENTS_DETTE | DEPARTEMENTS_METROPOLE_BP | ses 92 parties (CEA_BP … DEP_95_BP) | ensemble | 2022 | +5,8 M€ en 2022 |
| eurostat.gov_10a_main | SEC2010.B9 | S13 | S1311 + S1313 + S1314 | ensemble | 2011 | −0,4 M€ en 2011 |
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

Des tableaux différents présentent autrement les mêmes grandeurs. Chaque passerelle vérifie qu'ils concordent, à l'arrondi près, pour chaque année où figurent tous ses termes. Pour les collectivités locales, la consolidation des budgets principaux et annexes retire chaque flux croisé des recettes comme des dépenses de la même section : la variation du fonds de roulement, l'épargne brute, la dette et la trésorerie d'un ensemble consolidé égalent la somme de celles de ses parties.

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

## 5. Ratios

Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.

| Dénominateur | Ratios | Retrouvés | Non retrouvés |
|---|---|---|---|
| le PIB indiqué par la source, dans le même tableau | 730 | 597 | 133 |
| la dépense totale du même périmètre, chez la même source | 300 | 300 | 0 |
| non indiqué par la source : chaque série de PIB enregistrée pour l'année est essayée | 1500 | 1493 | 7 |

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
| eurostat.gov_10a_exp | insee.t3301 | 330 | 5 | 5 | +0,9 M€ en 2020 | +0,9 M€ en 2020 |
| eurostat.gov_10a_exp | insee.t3307 | 176 | 100 | 100 | −20 300,8 M€ en 2009 | −20 300,8 M€ en 2009 |
| eurostat.gov_10a_main | insee.t3106 | 248 | 1 | 1 | +0,9 M€ en 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3108 | 17 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t3201 | 124 | 5 | 3 | −43,0 M€ en 2021 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3202 | 124 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t3205 | 124 | 0 | 0 | aucun | aucun |
| eurostat.gov_10a_main | insee.t3212 | 124 | 6 | 6 | +39,0 M€ en 2019 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3301 | 30 | 15 | 13 | −3,3 M€ en 2019 | +914,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3302 | 30 | 6 | 4 | −0,6 M€ en 2015 | +954,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3305 | 30 | 4 | 2 | −0,6 M€ en 2002 | +738,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3306 | 30 | 3 | 1 | +0,7 M€ en 2022 | −1 139,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3307 | 16 | 16 | 14 | −20 301,7 M€ en 2009 | −20 301,7 M€ en 2009 |
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
| insee.t3101 | insee.t3106 | 48 | 42 | 42 | +9 571,2 M€ en 1990 | +9 571,2 M€ en 1990 |
| insee.t3101 | senat.pjl24-032 | 1 | 1 | 0 | aucun | −1,1 point de PIB en 2023 |
| insee.t3101 | senat.pjl24-718 | 1 | 1 | 0 | aucun | −0,4 point de PIB en 2024 |
| insee.t3101 | senat.pjl25-726 | 1 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3107 | 17 | 1 | 1 | −59,0 M€ en 2016 | −59,0 M€ en 2016 |
| insee.t3106 | insee.t3108 | 17 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3201 | 67 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3202 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3203 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3204 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3205 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3212 | 48 | 0 | 0 | aucun | aucun |
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
| insee.t3108 | senat.pjl16-106 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl17-063 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl18-106 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl19-098 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl20-101 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.pjl21-118 | 1 | 0 | 0 | aucun | aucun |
| insee.t3108 | senat.tas22-018 | 1 | 1 | 1 | +5 000,0 M€ en 2021 | +5 000,0 M€ en 2021 |
| insee.t3201 | insee.t3301 | 240 | 35 | 19 | +43,1 M€ en 2021 | −2 012,0 M€ en 2024 |
| insee.t3201 | insee.t3307 | 16 | 16 | 14 | −20 301,8 M€ en 2009 | −20 301,8 M€ en 2009 |
| insee.t3202 | insee.t3302 | 240 | 20 | 5 | −0,6 M€ en 2016 | +1 029,5 M€ en 2024 |
| insee.t3203 | insee.t3303 | 128 | 21 | 6 | −2,0 M€ en 2021 | +698,0 M€ en 2023 |
| insee.t3204 | insee.t3304 | 128 | 17 | 2 | −2,4 M€ en 2020 | +3 073,7 M€ en 2024 |
| insee.t3205 | insee.t3305 | 240 | 18 | 2 | −0,6 M€ en 2002 | +738,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | 240 | 19 | 5 | −39,4 M€ en 2019 | +1 304,3 M€ en 2024 |
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
| eurostat.gov_10a_exp | insee.t3301 | FR S13 SEC2010.TE | ensemble, GF01, GF04 et GF05 | 2012, 2018, 2020 et 2021 | 2012, 2018, 2020 et 2021 | +0,9 M€ en 2020 (GF01) |
| eurostat.gov_10a_exp | insee.t3307 | FR S13 SEC2010.TE | ensemble et 9 divisions | 10 années entre 2009 et 2018 | 10 années entre 2009 et 2018 | −20 300,8 M€ en 2009 (ensemble) |
| eurostat.gov_10a_main | insee.t3106 | FR S1314 SEC2010.B9 | ensemble | 2011 | 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3201 | FR S13 SEC2010.TE | ensemble | 2013, 2021 et 2024 | 2013 et 2021 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3201 | FR S13 SEC2010.TR | ensemble | 2021 et 2024 | 2021 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.B9 | ensemble | 2011 | 2011 | +0,4 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.TE | ensemble | 2019 et 2020 | 2019 et 2020 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.TR | ensemble | 2011, 2019 et 2020 | 2011, 2019 et 2020 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3301 | FR S13 SEC2010.TE | ensemble | 15 années entre 1995 et 2024 | 13 années entre 1995 et 2022 | +914,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3302 | FR S1311 SEC2010.TE | ensemble | 6 années entre 1996 et 2024 | 1996, 2008, 2015 et 2016 | +954,2 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3305 | FR S1313 SEC2010.TE | ensemble | 2002, 2013, 2023 et 2024 | 2002 et 2013 | +738,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3306 | FR S1314 SEC2010.TE | ensemble | 2022, 2023 et 2024 | 2022 | −1 139,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3307 | FR S13 SEC2010.TE | ensemble | 16 années entre 2009 et 2024 | 14 années entre 2009 et 2022 | −20 301,7 M€ en 2009 |
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
| insee.t3101 | insee.t3106 | FR S1 SEC2010.B1GQ | ensemble | 42 années entre 1978 et 2019 | 42 années entre 1978 et 2019 | +9 571,2 M€ en 1990 |
| insee.t3101 | senat.pjl24-032 | FR S13 PDE.GD, en % du PIB | ensemble | 2023 | aucune | −1,1 point de PIB en 2023 |
| insee.t3101 | senat.pjl24-718 | FR S13 PDE.GD, en % du PIB | ensemble | 2024 | aucune | −0,4 point de PIB en 2024 |
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
| insee.t3107 | senat.pjl24-718 | FR ETAT_LF LOLF.SOLDE_COMPTES_SPECIAUX | ensemble | 2024 | aucune | −50,0 M€ en 2024 |
| insee.t3108 | insee.t3214 | FR S13142 SEC2010.B9 | ensemble | 6 années entre 2013 et 2018 | 6 années entre 2013 et 2018 | +271,0 M€ en 2018 |
| insee.t3108 | senat.tas22-018 | FR REGIME_GENERAL COMPTES_SECU.RESULTAT_COMPTABLE | ensemble | 2021 | 2021 | +5 000,0 M€ en 2021 |
| insee.t3201 | insee.t3301 | FR S13 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | +487,9 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D1PAY | ensemble | 2011, 2023 et 2024 | 2011 | +889,0 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D3PAY | ensemble | 2001, 2023 et 2024 | 2001 | +552,0 M€ en 2023 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +1 807,3 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −1 949,3 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.D9_HORS_D995PAY | ensemble | 6 années entre 2010 et 2024 | 2010, 2013, 2019 et 2021 | −2 012,0 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | +1 340,5 M€ en 2024 |
| insee.t3201 | insee.t3301 | FR S13 SEC2010.TE | ensemble | 15 années entre 1995 et 2024 | 13 années entre 1995 et 2022 | +877,8 M€ en 2023 |
| insee.t3201 | insee.t3307 | FR S13 SEC2010.TE | ensemble | 16 années entre 2009 et 2024 | 14 années entre 2009 et 2022 | −20 301,8 M€ en 2009 |
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
| insee.t3205 | insee.t3305 | FR S1313 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | +592,5 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D1PAY | ensemble | 2023 et 2024 | aucune | +24,0 M€ en 2023 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D3PAY | ensemble | 2023 et 2024 | aucune | −10,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +502,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −525,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.D9_HORS_D995PAY | ensemble | 2023 et 2024 | aucune | −331,0 M€ en 2024 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | −316,2 M€ en 2023 |
| insee.t3205 | insee.t3305 | FR S1313 SEC2010.TE | ensemble | 2002, 2013, 2023 et 2024 | 2002 et 2013 | +738,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | ensemble | 2023 et 2024 | aucune | −162,8 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D1PAY | ensemble | 2023 et 2024 | aucune | −156,3 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D3PAY | ensemble | 2024 | aucune | +166,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D62PAY | ensemble | 2023 et 2024 | aucune | +1 304,3 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D632PAY | ensemble | 2023 et 2024 | aucune | −1 049,3 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.D9_HORS_D995PAY | ensemble | 2019, 2020 et 2024 | 2019 et 2020 | −1 181,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.P2 | ensemble | 2023 et 2024 | aucune | +464,6 M€ en 2024 |
| insee.t3212 | insee.t3306 | FR S1314 SEC2010.TE | ensemble | 5 années entre 2019 et 2024 | 2019, 2020 et 2022 | −1 139,0 M€ en 2024 |
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

Les comptes que l'OFGL publie collectivité par collectivité sur data.ofgl.fr, dans la version la plus récente de chaque exercice. Chaque ligne donne, pour une collectivité et un agrégat, le montant de son budget principal, celui de ses budgets annexes, les flux croisés entre eux et le montant consolidé : celui-ci doit être la somme des deux premiers moins le troisième, à l'arrondi près : la demi-unité de la dernière décimale publiée de chaque montant, au centime au plus fin (les montants de 2022 n'ont que dix chiffres significatifs). Pour chaque collectivité, les identités comptables de la section 1 s'appliquent à chacun des quatre montants. La somme des collectivités se compare aux totaux des annexes des rapports de l'OFGL : 2A pour les budgets principaux, 2B pour les budgets annexes, 2C pour les comptes consolidés ; celle des départements sans la métropole de Lyon ni la Ville de Paris, que les annexes comptent avec les groupements à fiscalité propre et avec les communes. Le budget principal de chaque département et de chaque région se compare aussi à sa fiche dans les publications de la DGCL.

| Jeu de données | Exercices | Collectivités au dernier exercice | Lignes | Lignes dont le consolidé n'est pas BP + BA − flux |
|---|---|---|---|---|
| ofgl.base-communes-consolidee | 8 années entre 2018 et 2025 | 34 778 | 13 535 660 | 0 |
| ofgl.base-departements-consolidee | 14 années entre 2012 et 2025 | 97 | 88 417 | 0 |
| ofgl.base-gfp-consolidee | 8 années entre 2018 et 2025 | 1 262 | 508 116 | 0 |
| ofgl.base-regions-consolidee | 14 années entre 2012 et 2025 | 17 | 14 547 | 0 |
| ofgl.base-syndicats-consolidee | 8 années entre 2018 et 2025 | 8 522 | 3 027 867 | 0 |

Identités comptables de chaque collectivité : 29 515 772 vérifiées, 29 515 772 justes, 0 en écart.

Collectivités que deux jeux de données donnent : 2 972 montants comparés de l'un à l'autre, 2 966 égaux, 6 en écart. Les agrégats qu'un seul des deux jeux publie, désignés par leur concept de la norme COMPTES_LOCAUX, ne se comparent pas.

| Collectivité | Premier jeu | Second jeu | Exercices | Montants comparés | En écart | Agrégats du seul premier jeu | Agrégats du seul second |
|---|---|---|---|---|---|---|---|
| MET DE LYON (200046977) | ofgl.base-departements-consolidee | ofgl.base-gfp-consolidee | 8 années entre 2018 et 2025 | 1 572 | 6 | ALLOCATIONS_APA, ALLOCATIONS_PCH, ALLOCATIONS_RSA, ATTRIBUTIONS_PEREQUATION_DMTO, CONCOURS_CNSA, CONTRIBUTIONS_SDIS, CVAE, DDEC, DMTO, DMTO_APRES_PEREQUATION, EPARGNE_BRUTE_AVANT_TRAVAUX_REGIE, FMDI, FRAIS_HEBERGEMENT, PRELEVEMENTS_PEREQUATION_DMTO, TICPE, TSCA | CREDITS_TRESORERIE, TEOM, VERSEMENT_TRANSPORT |
| VILLE DE PARIS (217500016) | ofgl.base-communes-consolidee | ofgl.base-departements-consolidee | 7 années entre 2019 et 2025 | 1 400 | 0 | TEOM | ALLOCATIONS_APA, ALLOCATIONS_PCH, ALLOCATIONS_RSA, CONCOURS_CNSA, CONTRIBUTIONS_SDIS, CVAE, DDEC, DMTO, DMTO_APRES_PEREQUATION, EPARGNE_BRUTE_AVANT_TRAVAUX_REGIE, FMDI, FRAIS_HEBERGEMENT, PRELEVEMENTS_PEREQUATION_DMTO, TICPE, TRAVAUX_REGIE, TSCA |

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
