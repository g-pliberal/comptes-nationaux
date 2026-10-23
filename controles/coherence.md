# Cohérence des chiffres enregistrés

Fichier généré par `outils/controler_coherence.py` à partir de la base : ne pas le modifier à la main.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la demi-unité de la dernière décimale de chaque valeur en jeu. Une incohérence signalée ici est un constat sur la source, pas une erreur d'enregistrement : chaque chiffre a été relu dans sa copie archivée.

## Les sources contrôlées

Pour chaque chiffre, la version la plus récente enregistrée chez sa source.

| Source | Titre | Version la plus récente | Chiffres |
|---|---|---|---|
| eurostat.gov_10a_exp | Dépenses des administrations publiques par fonction (COFOG) | 2026-10-21 | 1290 |
| eurostat.gov_10a_main | Recettes, dépenses et principaux agrégats des administrations publiques | 2026-10-21 | 1488 |
| eurostat.nama_10_gdp | PIB et principaux agrégats | 2026-10-21 | 102 |
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

## 1. Sommes comptables

Un total contre la somme de ses composantes, pour chaque source, périmètre, fonction et année.

6317 sommes vérifiées avec toutes leurs composantes : 6307 justes, 10 en écart.

| Source | Périmètre | Fonction | Année | Total | Total publié (Md€) | Somme des composantes (Md€) | Écart |
|---|---|---|---|---|---|---|---|
| insee.t3207 | S131311 | ensemble | 2019 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 36,3688 | 36,2870 | +81,8 M€ |
| insee.t3207 | S131311 | ensemble | 2020 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 31,1743 | 31,0840 | +90,3 M€ |
| insee.t3207 | S131311 | ensemble | 2021 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 32,5278 | 32,4602 | +67,6 M€ |
| insee.t3207 | S131311 | ensemble | 2024 | SEC2010.B9 | −2,8229 | −2,8219 | −1,0 M€ |
| insee.t3208 | S131312 | ensemble | 2019 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 6,8290 | 6,8270 | +2,0 M€ |
| insee.t3208 | S131312 | ensemble | 2020 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 6,9480 | 6,9460 | +2,0 M€ |
| insee.t3208 | S131312 | ensemble | 2024 | SEC2010.B9 | −5,6560 | −5,8130 | +157,0 M€ |
| insee.t3210 | S131314 | ensemble | 2021 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 5,0710 | 5,0550 | +16,0 M€ |
| insee.t3217 | S13_S212 | ensemble | 2018 | INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_IMPUTES | −16,8840 | −16,3100 | −574,0 M€ |
| insee.t3217 | S13_S212 | ensemble | 2019 | INSEE_PO.AJUSTEMENT_CREDITS_IMPOT_IMPUTES | −17,7060 | −17,1280 | −578,0 M€ |

11107 sommes ont des parties que la source ne diffuse pas (cellule vide ou marquée non disponible). Pour 11102 d'entre elles, les parties diffusées suffisent à retrouver le total à l'arrondi près : les parties absentes y sont nulles ou négligeables. Pour les 5 autres, elles ne suffisent pas : des parties absentes ne sont pas nulles.

| Source | Périmètre | Total | Fonction | Années | Plus grand reste (total − parties diffusées) |
|---|---|---|---|---|---|
| insee.t3107 | S13111 | INSEE_PASSAGES.ETAT_DROITS_CONSTATES | ensemble | 2023 | −1 300,0 M€ en 2023 |
| insee.t3107 | S13111 | INSEE_PASSAGES.ETAT_NON_BUDGETAIRES | ensemble | 2019, 2020, 2021 et 2024 | −2 600,0 M€ en 2021 |

## 2. Ventilations par fonction

Pour une même grandeur, l'ensemble des fonctions contre la somme des dix divisions de la COFOG, et chaque division contre la somme de ses groupes.

8870 ventilations vérifiées avec toutes leurs parties : 8870 justes, 0 en écart.

6954 ventilations ont des parties que la source ne diffuse pas (cellule vide ou marquée non disponible). Pour toutes, les parties diffusées suffisent à retrouver le total à l'arrondi près : les parties absentes y sont nulles ou négligeables.

## 3. Additivité des sous-secteurs

Le solde d'un ensemble, ses prélèvements obligatoires, ou sa dépense consolidée au niveau de l'ensemble des administrations publiques (tableau 3.307 de l'Insee), contre la somme de ceux de ses parties.

1689 additions vérifiées : 1668 justes, 21 en écart.

| Tableaux | Grandeur | Ensemble | Parties | Fonctions | Années en écart | Plus grand écart |
|---|---|---|---|---|---|---|
| eurostat.gov_10a_main | SEC2010.B9 | S13 | S1311 + S1313 + S1314 | ensemble | 2011 | −0,4 M€ en 2011 |
| insee.t3106 | SEC2010.B9 | S1311 | S13111 + S13112 | ensemble | 19 années entre 1959 et 1977 | +6 502,0 M€ en 1974 |
| insee.t3212, insee.t3213, insee.t3214 | SEC2010.B9 | S1314 | S13141 + S13142 | ensemble | 2019 | +8,0 M€ en 2019 |

## 4. Passerelles entre tableaux

Des tableaux différents présentent autrement les mêmes grandeurs. Chaque passerelle vérifie qu'ils concordent, à l'arrondi près, pour chaque année où figurent tous ses termes.

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
| Déficit de l'État au sens de Maastricht contre résultat d'exécution des lois de finances plus corrections (1), (2) et (3), dans le tableau 3.107 | 17 années entre 2009 et 2025 | aucune | aucune | aucun |

## 5. Ratios

Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.

| Dénominateur | Ratios | Retrouvés | Non retrouvés |
|---|---|---|---|
| le PIB indiqué par la source, dans le même tableau | 730 | 597 | 133 |
| la dépense totale du même périmètre, chez la même source | 300 | 300 | 0 |
| non indiqué par la source : chaque série de PIB enregistrée pour l'année est essayée | 1497 | 1492 | 5 |

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

## 6. Écarts entre sources pour une même grandeur

Même concept, même périmètre, même fonction, même consolidation, même année, montants convertis dans la même unité. Les montants d'Eurostat convertis en écus avant 1999 ne sont pas comparés : ce sont les mêmes données que ses montants en euros, converties autrement.

Un chiffre que sa source présente comme provisoire, semi-définitif, estimé ou prévu peut encore être révisé : un écart qui en touche un peut venir d'une révision entre deux versions. Les écarts « hors chiffres révisables » sont ceux où aucune des deux sources ne présente son chiffre ainsi.

| Source A | Source B | Comparaisons | Écarts | dont hors chiffres révisables | Plus grand écart hors chiffres révisables (A − B) | Plus grand écart (A − B) |
|---|---|---|---|---|---|---|
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
| eurostat.nama_10_gdp | insee.t3101 | 48 | 42 | 42 | −9 571,2 M€ en 1990 | −9 571,2 M€ en 1990 |
| eurostat.nama_10_gdp | insee.t3106 | 51 | 0 | 0 | aucun | aucun |
| insee.t3101 | insee.t3106 | 48 | 42 | 42 | +9 571,2 M€ en 1990 | +9 571,2 M€ en 1990 |
| insee.t3106 | insee.t3107 | 17 | 1 | 1 | −59,0 M€ en 2016 | −59,0 M€ en 2016 |
| insee.t3106 | insee.t3108 | 17 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3201 | 67 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3202 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3203 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3204 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3205 | 48 | 0 | 0 | aucun | aucun |
| insee.t3106 | insee.t3212 | 48 | 0 | 0 | aucun | aucun |
| insee.t3107 | insee.t3203 | 17 | 1 | 1 | +59,2 M€ en 2016 | +59,2 M€ en 2016 |
| insee.t3108 | insee.t3212 | 17 | 0 | 0 | aucun | aucun |
| insee.t3108 | insee.t3214 | 13 | 6 | 6 | +271,0 M€ en 2018 | +271,0 M€ en 2018 |
| insee.t3201 | insee.t3301 | 240 | 35 | 19 | +43,1 M€ en 2021 | −2 012,0 M€ en 2024 |
| insee.t3201 | insee.t3307 | 16 | 16 | 14 | −20 301,8 M€ en 2009 | −20 301,8 M€ en 2009 |
| insee.t3202 | insee.t3302 | 240 | 20 | 5 | −0,6 M€ en 2016 | +1 029,5 M€ en 2024 |
| insee.t3203 | insee.t3303 | 128 | 21 | 6 | −2,0 M€ en 2021 | +698,0 M€ en 2023 |
| insee.t3204 | insee.t3304 | 128 | 17 | 2 | −2,4 M€ en 2020 | +3 073,7 M€ en 2024 |
| insee.t3205 | insee.t3305 | 240 | 18 | 2 | −0,6 M€ en 2002 | +738,0 M€ en 2024 |
| insee.t3212 | insee.t3306 | 240 | 19 | 5 | −39,4 M€ en 2019 | +1 304,3 M€ en 2024 |
| insee.t3216 | insee.t3217 | 93 | 24 | 24 | +734,9 M€ en 1995 | +734,9 M€ en 1995 |
| insee.t3301 | insee.t3307 | 1248 | 408 | 408 | −20 301,0 M€ en 2009 | −20 301,0 M€ en 2009 |

Détail des grandeurs en écart :

| Source A | Source B | Grandeur | Fonctions en écart | Années en écart | dont hors chiffres révisables | Plus grand écart (A − B) |
|---|---|---|---|---|---|---|
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
| eurostat.nama_10_gdp | insee.t3101 | FR S1 SEC2010.B1GQ | ensemble | 42 années entre 1978 et 2019 | 42 années entre 1978 et 2019 | −9 571,2 M€ en 1990 |
| insee.t3101 | insee.t3106 | FR S1 SEC2010.B1GQ | ensemble | 42 années entre 1978 et 2019 | 42 années entre 1978 et 2019 | +9 571,2 M€ en 1990 |
| insee.t3106 | insee.t3107 | FR S13111 SEC2010.B9 | ensemble | 2016 | 2016 | −59,0 M€ en 2016 |
| insee.t3107 | insee.t3203 | FR S13111 SEC2010.B9 | ensemble | 2016 | 2016 | +59,2 M€ en 2016 |
| insee.t3108 | insee.t3214 | FR S13142 SEC2010.B9 | ensemble | 6 années entre 2013 et 2018 | 6 années entre 2013 et 2018 | +271,0 M€ en 2018 |
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
| insee.t3301 | insee.t3307 | FR S13 SEC2010.TE | ensemble, 9 divisions et 41 groupes | 10 années entre 2009 et 2018 | 10 années entre 2009 et 2018 | −20 301,0 M€ en 2009 (ensemble) |
