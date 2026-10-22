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

## 1. Sommes comptables des tableaux de l'Insee

4598 sommes vérifiées (un total contre la somme de ses composantes) : 4590 justes, 8 en écart.

| Source | Périmètre | Année | Total | Total publié (Md€) | Somme des composantes (Md€) | Écart |
|---|---|---|---|---|---|---|
| insee.t3207 | S131311 | 2019 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 36,3688 | 36,2870 | +81,8 M€ |
| insee.t3207 | S131311 | 2020 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 31,1743 | 31,0840 | +90,3 M€ |
| insee.t3207 | S131311 | 2021 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 32,5278 | 32,4602 | +67,6 M€ |
| insee.t3207 | S131311 | 2024 | SEC2010.B9 | −2,8229 | −2,8219 | −1,0 M€ |
| insee.t3208 | S131312 | 2019 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 6,8290 | 6,8270 | +2,0 M€ |
| insee.t3208 | S131312 | 2020 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 6,9480 | 6,9460 | +2,0 M€ |
| insee.t3208 | S131312 | 2024 | SEC2010.B9 | −5,6560 | −5,8130 | +157,0 M€ |
| insee.t3210 | S131314 | 2021 | INSEE_APU.DEP_ACTIFS_NON_FINANCIERS | 5,0710 | 5,0550 | +16,0 M€ |

## 2. Soldes des sous-secteurs

273 additions vérifiées (le solde d'un ensemble contre la somme des soldes de ses parties) : 253 justes, 20 en écart.

| Tableaux | Ensemble | Parties | Années en écart | Plus grand écart |
|---|---|---|---|---|
| insee.t3106 | S1311 | S13111 + S13112 | 19 années entre 1959 et 1977 | +6 502,0 M€ en 1974 |
| insee.t3212, insee.t3213, insee.t3214 | S1314 | S13141 + S13142 | 2019 | +8,0 M€ en 2019 |

## 3. Ratios

Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.

| Dénominateur | Ratios | Retrouvés | Non retrouvés |
|---|---|---|---|
| le PIB indiqué par la source, dans le même tableau | 730 | 597 | 133 |
| la dépense totale du même périmètre, chez la même source | 300 | 300 | 0 |
| non indiqué par la source : chaque série de PIB enregistrée pour l'année est essayée | 826 | 821 | 5 |

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

## 4. Écarts entre sources pour une même grandeur

Même concept, même périmètre, même fonction, même année, montants convertis dans la même unité. Les montants d'Eurostat convertis en écus avant 1999 ne sont pas comparés : ce sont les mêmes données que ses montants en euros, converties autrement.

| Source A | Source B | Comparaisons | Écarts | Plus grand écart (A − B) |
|---|---|---|---|---|
| eurostat.gov_10a_exp | eurostat.gov_10a_main | 60 | 19 | +0,3 point de PIB en 2024 ; −914,4 M€ en 2024 |
| eurostat.gov_10a_exp | insee.t3201 | 30 | 20 | −878,3 M€ en 2023 |
| eurostat.gov_10a_main | insee.t3106 | 248 | 1 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3201 | 124 | 5 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3202 | 124 | 0 | aucun |
| eurostat.gov_10a_main | insee.t3205 | 124 | 0 | aucun |
| eurostat.gov_10a_main | insee.t3212 | 124 | 6 | +39,0 M€ en 2019 |
| eurostat.nama_10_gdp | insee.t3101 | 48 | 42 | −9 571,2 M€ en 1990 |
| eurostat.nama_10_gdp | insee.t3106 | 51 | 0 | aucun |
| insee.t3101 | insee.t3106 | 48 | 42 | +9 571,2 M€ en 1990 |
| insee.t3106 | insee.t3201 | 67 | 0 | aucun |
| insee.t3106 | insee.t3202 | 48 | 0 | aucun |
| insee.t3106 | insee.t3203 | 48 | 0 | aucun |
| insee.t3106 | insee.t3204 | 48 | 0 | aucun |
| insee.t3106 | insee.t3205 | 48 | 0 | aucun |
| insee.t3106 | insee.t3212 | 48 | 0 | aucun |

Détail des grandeurs en écart :

| Source A | Source B | Grandeur | Années en écart | Plus grand écart (A − B) |
|---|---|---|---|---|
| eurostat.gov_10a_exp | eurostat.gov_10a_main | FR S13 SEC2010.TE, en % du PIB | 2024 | +0,3 point de PIB en 2024 |
| eurostat.gov_10a_exp | eurostat.gov_10a_main | FR S13 SEC2010.TE | 18 années entre 1995 et 2024 | −914,4 M€ en 2024 |
| eurostat.gov_10a_exp | insee.t3201 | FR S13 SEC2010.TE | 20 années entre 1995 et 2024 | −878,3 M€ en 2023 |
| eurostat.gov_10a_main | insee.t3106 | FR S1314 SEC2010.B9 | 2011 | +0,9 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3201 | FR S13 SEC2010.TE | 2013, 2021 et 2024 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3201 | FR S13 SEC2010.TR | 2021 et 2024 | +119,0 M€ en 2024 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.B9 | 2011 | +0,4 M€ en 2011 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.TE | 2019 et 2020 | +39,0 M€ en 2019 |
| eurostat.gov_10a_main | insee.t3212 | FR S1314 SEC2010.TR | 2011, 2019 et 2020 | +39,0 M€ en 2019 |
| eurostat.nama_10_gdp | insee.t3101 | FR S1 SEC2010.B1GQ | 42 années entre 1978 et 2019 | −9 571,2 M€ en 1990 |
| insee.t3101 | insee.t3106 | FR S1 SEC2010.B1GQ | 42 années entre 1978 et 2019 | +9 571,2 M€ en 1990 |
