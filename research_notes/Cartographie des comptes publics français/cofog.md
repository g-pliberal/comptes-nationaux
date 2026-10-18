# COFOG (CFAP) : ventilation fonctionnelle des dépenses publiques françaises (état au 18 octobre 2026)

*Notes de recherche, périmètre : dépenses des administrations publiques (APU, secteur S13) ventilées par fonction. Les fichiers Insee (T_3301, T_3303, T_3304, T_3307) et les extractions de l'API Eurostat ont été téléchargés et lus le 18/10/2026. La mention « (calcul) » signale un calcul fait par l'auteur des notes à partir des sources citées. « Comog » désigne très probablement la COFOG : je n'ai trouvé aucune autre acception pertinente en finances publiques. Les classifications « sœurs » de l'ONU, avec lesquelles la confusion est possible, sont la COICOP, la COPNI et la COPP ([UNSD, page révision COFOG](https://unstats.un.org/unsd/classifications/cofog/revision)).*

## 1. Quelle est la dernière ventilation COFOG publiée pour la France (année, valeurs, date de publication) et sa source exacte ?

### Takeaway
Le dernier millésime publié est **2024, provisoire**. Les **dépenses consolidées des APU** s'élèvent à **1 671,8 Md€**. La **protection sociale** en représente 693,0 Md€ (41,5 %), la **santé** 261,2 Md€ (15,6 %), les **services généraux** 181,1 Md€ (10,8 %, dont 58,9 Md€ d'opérations sur la dette publique), les **affaires économiques** 166,1 Md€, l'**enseignement** 148,6 Md€ et la **défense** 54,2 Md€.

Ces données viennent de l'Insee, comptes nationaux annuels base 2020, tableaux 3.301 à 3.307. Elles sont publiées dans l'Insee Résultats « Dépenses des administrations publiques ventilées par fonction en 2024 » (fichiers xlsx créés le 28/11/2025) et analysées dans l'Insee Première n° 2093 du 05/02/2026. Elles sont identiques aux données Eurostat gov_10a_exp (dernière mise à jour le 16/09/2026).

La ventilation 2025 n'est pas encore publiée : l'Insee l'annonce pour décembre 2026. Le total 2025 est en revanche connu : 1 714,2 Md€, soit 57,3 % du PIB.

### Cited Findings

#### 1.1 Ce qu'est la COFOG / CFAP (origine, structure, articulation SEC 2010 / S13)
- La COFOG (*Classification of the Functions of Government*), en français **CFAP (classification des fonctions des administrations publiques)**, répartit les dépenses des APU en dix catégories selon leur finalité. Le champ des administrations publiques et le montant des dépenses sont ceux de la comptabilité nationale. — [Insee, page « … par fonction en 2025 » (paru le 29/05/2026)](https://www.insee.fr/fr/statistiques/8988847)
- La COFOG a été publiée pour la première fois en 1980, puis révisée en 1999. Elle fait partie des quatre classifications des dépenses selon leur objet, avec la COICOP, la COPNI et la COPP. Elle comporte trois niveaux : divisions, groupes et classes. — [UNSD, COFOG revision](https://unstats.un.org/unsd/classifications/cofog/revision) ; texte de la version 1999 : [UNSD, M84](https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/M84_complete_english.pdf)
- **Les 10 divisions, avec leurs intitulés officiels Insee :**
  - 01 Services généraux des administrations publiques
  - 02 Défense
  - 03 Ordre et sécurité publics
  - 04 Affaires économiques
  - 05 Protection de l'environnement
  - 06 Logements et équipements collectifs
  - 07 Santé
  - 08 Loisirs, culture et culte
  - 09 Enseignement
  - 10 Protection sociale

  Les codes Eurostat/Insee vont de GF01 à GF10. — [Insee, T_3301.xlsx, onglet Métadonnées](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
  - La « Méthodologie » de l'Insee Première n° 2093 emploie d'autres libellés pour certaines divisions : « Services publics généraux », « Ordre et sûreté publics », « Logement et développement urbain », « Éducation ». — [Insee Première n° 2093](https://www.insee.fr/fr/statistiques/8735252)
- **69 groupes** (niveau II). Ce chiffre est obtenu (calcul) en comptant les codes des listes Insee et Eurostat :
  - 01 : 8 groupes ; 02 : 5 ; 03 : 6 ; 04 : 9 ; 05 : 6 ; 06 : 6 ; 07 : 6 ; 08 : 6 ; 09 : 8 ; 10 : 9.
  - Chaque division compte un groupe « R-D » (01.5, 02.4, 03.5, 04.8, 05.5, 06.5, 07.5, 08.5, 09.7, 10.8) et un groupe « n.c.a. ». La division 01 comprend en outre le groupe 01.4 « Recherche fondamentale ».
  - Libellés des groupes de la protection sociale : 10.1 Maladie et invalidité ; 10.2 Vieillesse ; 10.3 Survivants ; 10.4 Famille et enfants ; 10.5 Chômage ; 10.6 Logement ; 10.7 Exclusion sociale n.c.a. ; 10.8 R-D dans le domaine de la protection sociale ; 10.9 Protection sociale n.c.a.
  - Le groupe 01.7 s'intitule « Opérations concernant la dette publique ».
  - — [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx) ; [Eurostat API gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)
- **Articulation avec le SEC 2010.** Pour l'Insee, l'approche COFOG est « parfaitement articulée avec le compte de secteur des administrations publiques présenté dans le Tableau Économique d'Ensemble (TEE) et la présentation en dépenses/recettes des statistiques de finances publiques » (MGDD 2022). Elle applique le *Manual on sources and methods for the compilation of COFOG statistics* d'Eurostat (édition 2019). — [Insee, fiche méthodologique COFOG – fonction Protection sociale (base 2020)](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
- **Le total ventilé est la dépense publique totale** (code OTE/TE). Elle est croisée avec les opérations SEC :
  - D1 rémunération des salariés ;
  - P2 consommation intermédiaire ;
  - D62 prestations sociales autres que transferts sociaux en nature ;
  - D632 transferts sociaux en nature – production marchande achetée ;
  - D3 subventions ;
  - D4 revenus de la propriété ;
  - D7 autres transferts courants ;
  - D9 transferts en capital ;
  - P5L acquisition nette d'actifs non financiers (= P5 + NP) ;
  - OED autres impôts sur la production, impôts courants, ajustement pour variation des droits à pension.

  — [Insee T_3301.xlsx (Métadonnées)](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
  - Eurostat diffuse aussi P3, P31 et P32 (dépense de consommation individuelle ou collective), P51G et D92. — [Eurostat API gov_10a_exp, France, toutes opérations](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.MIO_EUR+PC_GDP....FR?startPeriod=2023&format=SDMX-CSV)
- **Secteur et sous-secteurs.** Les données couvrent S13, S1311 (administration centrale), S1313 (APUL) et S1314 (ASSO) de 1995 à 2024. L'État (S13111) et les ODAC (S13112) ne sont distingués qu'à partir de 2009. — [Insee, page « … par fonction en 2024 »](https://www.insee.fr/fr/statistiques/8574707)
- **Consolidation.** Les tableaux Insee sont établis « hors dépenses à l'intérieur du sous-secteur (intérêts, transferts courants et en capital) ». — [Insee T_3301.xlsx (note)](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
- **Exigences européennes.** Le niveau division est obligatoire depuis 1995, le niveau groupe depuis l'année de référence 2001. Selon l'article, les États membres transmettent le tableau 1100 « onze mois après la fin de la période de référence ». — [Eurostat, Statistics Explained « Government expenditure by function – COFOG » (données extraites le 20/08/2026)](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
- **Révision en cours de la COFOG.**
  - La Commission de statistique de l'ONU (53e session, 2022, décision 53/125(i)) a recommandé de réviser la classification. Le travail est confié à l'équipe TT-COFOG, sous l'égide de l'UNCEISC.
  - Une consultation mondiale a eu lieu de novembre 2024 à janvier 2025.
  - L'UNSD indique : « It is anticipated that the update will be completed by 2028 ». Un résumé de recherche secondaire avance plutôt mars 2027 : la page UNSD primaire fait foi.
  - Parmi les thèmes de révision : environnement (alignement CEP/SEEA), R&D (alignement NABS), numérique, genre, distinction dépenses individuelles/collectives.
  - — [UNSD, COFOG revision](https://unstats.un.org/unsd/classifications/cofog/revision)

#### 1.2 Dernier millésime disponible et calendrier
- **Insee, page « Dépenses des administrations publiques ventilées par fonction en 2024 » (Insee Résultats, comptes nationaux annuels base 2020).**
  - Date affichée : « Paru le 27/03/2026 ». Une note datée du 05/02/2026 y figure également.
  - Sept tableaux xlsx :

    | Tableau | Intitulé | Fichier |
    |---|---|---|
    | 3.301 | Dépenses des administrations publiques (S13) ventilées par fonction | T_3301.xlsx |
    | 3.302 | Administration publique centrale (S1311) | T_3302.xlsx |
    | 3.303 | État (S13111) | T_3303.xlsx |
    | 3.304 | ODAC (S13112) | T_3304.xlsx |
    | 3.305 | APUL (S1313) | T_3305.xlsx |
    | 3.306 | ASSO (S1314) | T_3306.xlsx |
    | 3.307 | Répartition par sous-secteur des dépenses consolidées des APU ventilées par fonction | T_3307.xlsx |

  - Le jeu de données associé, DD_CNA_APU, était signalé « momentanément indisponible » le 27/03/2026.
  - — [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707) ; [catalogue DD_CNA_APU](https://catalogue-donnees.insee.fr/fr/catalogue/recherche/DD_CNA_APU)
- **Le fichier T_3301.xlsx** porte la « Date de création du fichier : 2025-11-28 ». Il couvre la période 1995 → 2024, en milliards d'euros, et provient des « Comptes nationaux annuels (base 2020) ». — [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
- **Analyse : Insee Première n° 2093**, « Usage de l'argent public : les dépenses publiques par fonction en 2024 – Une hausse des dépenses publiques portée par les retraites et la santé », Maxime Diaz, paru le 05/02/2026. Les données 2024 y sont provisoires : les données semi-définitives sont attendues à l'automne 2026, les définitives à l'automne 2027. — [Insee Première n° 2093](https://www.insee.fr/fr/statistiques/8735252) ([PDF](https://www.insee.fr/fr/statistiques/fichier/8735252/IP2093.pdf))
- **Millésime 2025.** La page Insee « … par fonction en 2025 » (parue le 29/05/2026) indique : « Les dépenses des administrations publiques ventilées par fonction, tableaux 3.301 à 3.307, seront publiées en décembre 2026 ». — [Insee 8988847](https://www.insee.fr/fr/statistiques/8988847)
- **Totaux 2025 connus, hors ventilation par fonction.** Ils proviennent de l'Insee Première n° 2106 « Le compte des administrations publiques en 2025 » (29/05/2026) :
  - dépenses publiques : 1 714,2 Md€ (+2,5 % après +4,0 % en 2024) ;
  - ratio de dépenses : 57,3 % du PIB (57,0 % en 2024, 56,8 % en 2023) ;
  - déficit : 5,1 % du PIB ; dette : 115,7 % du PIB ;
  - par nature : rémunérations 370,0 Md€, prestations sociales 771,0 Md€, charges d'intérêts 64,7 Md€ (+11,2 %), FBCF 132,2 Md€ ;
  - par sous-secteur : APUC 681,1 Md€, APUL 335,5 Md€, ASSO 803,3 Md€.

  — [Insee Première n° 2106](https://www.insee.fr/fr/statistiques/8997691)
  - Écart de millésime : l'Informations Rapides n° 78 de mars 2026 donnait 57,2 % pour 2025, ratio que l'on retrouve chez Eurostat (gov_10a_main, mise à jour le 21/07/2026 : 1 714,1 Md€, 57,2 %). — [Insee IR n° 78 (lu via résumé de recherche)](https://www.insee.fr/fr/statistiques/8956575) ; [Eurostat API gov_10a_main](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_main/A.PC_GDP+MIO_EUR.S13.TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2022&format=SDMX-CSV)
- **Eurostat gov_10a_exp.**
  - Dernière mise à jour du jeu de données : 16/09/2026.
  - Dernière année disponible : 2024 pour la France, l'UE-27, la zone euro (ZE-20), l'Allemagne, l'Italie et l'Espagne.
  - Données marquées « p » (provisoires) : France 2023-2024, Allemagne 2022-2024, Espagne 2024.

  — [Eurostat API gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)
  - L'article Statistics Explained (données extraites le 20/08/2026) porte sur 2024 ; sa prochaine mise à jour est prévue en mars 2027. — [Eurostat SE COFOG](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)

#### 1.3 France 2024 par division (dépenses consolidées des APU, S13)
Sources :
- montants : [Insee T_3301.xlsx (créé le 28/11/2025)](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx), identiques à [Eurostat gov_10a_exp (MAJ 16/09/2026)](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV) ;
- « % PIB publié » : valeur PC_GDP de gov_10a_exp ;
- « % PIB recalc. » (calcul) : montant divisé par le PIB 2024 de [Eurostat nama_10_gdp (MAJ 15/10/2026), soit 2 935,2 Md€](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp/A.CP_MEUR.B1GQ.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2024&endPeriod=2024&format=SDMX-CSV) ;
- évolutions : calculées à partir de T_3301, ou reprises de l'[IP n° 2093](https://www.insee.fr/fr/statistiques/8735252).

| Code | Division | 2023 (Md€) | 2024 (Md€) | Évol. 24/23 | % du total 2024 | % PIB publié | % PIB recalc. |
|---|---|---|---|---|---|---|---|
| — | **Total** | 1 607,4 | **1 671,8** | +4,0 % (+64 Md€) | 100 | 57,3 | 56,96 |
| GF01 | Services généraux des APU | 174,8 | 181,1 | +3,6 % | 10,8 | 6,2 | 6,17 |
| GF02 | Défense | 51,2 | 54,2 | +5,9 % | 3,2 | 1,9 | 1,85 |
| GF03 | Ordre et sécurité publics | 48,7 | 52,1 | +7,0 % | 3,1 | 1,8 | 1,78 |
| GF04 | Affaires économiques | 177,6 | 166,1 | −6,5 % | 9,9 | 5,7 | 5,66 |
| GF05 | Protection de l'environnement | 28,9 | 30,3 | +4,7 % | 1,8 | 1,0 | 1,03 |
| GF06 | Logements et équipements collectifs | 35,6 | 42,1 | +18,3 % | 2,5 | 1,4 | 1,44 |
| GF07 | Santé | 249,7 | 261,2 | +4,6 % | 15,6 | 8,9 | 8,90 |
| GF08 | Loisirs, culture et culte | 41,4 | 43,1 | +4,0 % | 2,6 | 1,5 | 1,47 |
| GF09 | Enseignement | 141,6 | 148,6 | +5,0 % | 8,9 | 5,1 | 5,06 |
| GF10 | Protection sociale | 657,9 | 693,0 | +5,3 % | 41,5 | 23,7 | 23,61 |

- Série longue (T_3301, Md€) :
  - 1995 : total 680,4 ; protection sociale 267,1 (dont vieillesse 133,1) ; santé 83,7 ; enseignement 69,9 ; services généraux 101,1 ; affaires économiques 77,8 ;
  - 2014 : total 1 257,6 ; protection sociale 528,1 ; santé 179,6.

  — [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
- Évolution des parts dans la dépense entre 2014 et 2024 (Insee) :
  - santé +1,3 pt ; défense +0,4 ; ordre et sécurité +0,3 ; logement +0,3 ; environnement +0,2 ;
  - loisirs-culture −0,1 ; enseignement −0,2 ; protection sociale −0,5 ; affaires économiques −0,6 ; services généraux −1,1.
  - En points de PIB, la santé gagne 0,6 pt et les affaires économiques en perdent 0,6.

  — [IP n° 2093, encadré 1](https://www.insee.fr/fr/statistiques/8735252)
- Moteurs 2024 :
  - **Retraites** : +6,2 % (+23 Md€). Les pensions de base ont été revalorisées de 5,3 % en janvier 2024, les complémentaires de 4,9 % au 1er novembre 2023.
  - **Charge de la dette** : +7 Md€ (+13,8 %), à 60 Md€.
  - **Fin du bouclier tarifaire électricité** : −14 Md€, d'où des affaires économiques en recul de 12 Md€.
  - **Services hospitaliers** : +6 Md€, à 109 Md€.
  - **Défense** : +3 Md€, dont rémunérations 22 Md€, achats 20 Md€ et investissement 11 Md€. La défense militaire en représente 88 %. Croissance de +7,8 %/an sur 2021-2024, contre +2,7 %/an sur 2014-2021.
  - **Logement** : +18,3 %, gonflé en partie par un changement de nomenclature comptable des collectivités locales qui minore symétriquement les affaires économiques. L'effet sera neutralisé dans les données définitives.

  — [IP n° 2093](https://www.insee.fr/fr/statistiques/8735252) ; [Insee 8574707 (note du 05/02/2026)](https://www.insee.fr/fr/statistiques/8574707)

#### 1.4 France 2024 : les 69 groupes (Md€, S13 consolidé)
Source de toute cette section : [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx), avec les mêmes valeurs dans [Eurostat gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV). Les valeurs 2023 sont indiquées entre crochets quand elles sont utiles. « n.d. » : non diffusé.

- **01 Services généraux, 181,1 Md€**
  - 01.1 Fonctionnement des organes exécutifs et législatifs, affaires financières et fiscales, affaires étrangères : 42,8
  - 01.2 Aide économique extérieure : 4,9
  - 01.3 Services généraux : 53,8
  - 01.4 Recherche fondamentale : 19,9
  - 01.5 R & D concernant les services généraux des APU : 0,0
  - 01.6 Services généraux des APU n.c.a. : 0,9
  - **01.7 Opérations concernant la dette publique : 58,9** [51,7] ; soit 3,5 % du total et 2,0 % du PIB
  - 01.8 Transferts de caractère général entre administrations publiques : 0,0 (s'annule en consolidé)
- **02 Défense, 54,2 Md€**
  - 02.1 Défense militaire : 47,7
  - 02.2 Défense civile : 0,2
  - 02.3 Aide militaire à des pays étrangers : 2,0
  - 02.4 R-D concernant la défense : 1,7
  - 02.5 Défense n.c.a. : 2,6
- **03 Ordre et sécurité publics, 52,1 Md€**
  - 03.1 Services de police : 28,9
  - 03.2 Services de protection civile : 7,9
  - 03.3 Tribunaux : 8,3
  - 03.4 Administration pénitentiaire : 5,1
  - 03.5 R-D : 0,0
  - 03.6 n.c.a. : 1,9
- **04 Affaires économiques, 166,1 Md€**
  - 04.1 Tutelle de l'économie générale, des échanges et de l'emploi : 45,3 [2021 : 66,7]
  - 04.2 Agriculture, sylviculture, pêche et chasse : 6,2
  - 04.3 Combustibles et énergie : 15,5 [2021 : 9,8 ; 2022 : 32,6 ; 2023 : 27,1]
  - 04.4 Industries extractives et manufacturières, construction : 1,6
  - 04.5 Transports : 60,7
  - 04.6 Communications : 1,6
  - 04.7 Autres branches d'activité : 11,2
  - 04.8 R-D concernant les affaires économiques : 21,4
  - 04.9 n.c.a. : 2,6
- **05 Protection de l'environnement, 30,3 Md€**
  - 05.1 Gestion des déchets : 15,9
  - 05.2 Gestion des eaux usées : 5,2
  - 05.3 Lutte contre la pollution : 4,3
  - 05.4 Préservation de la diversité biologique et protection de la nature : 1,7
  - 05.5 R-D : 1,8
  - 05.6 n.c.a. : 1,5
- **06 Logements et équipements collectifs, 42,1 Md€**
  - 06.1 Logements : 8,4
  - 06.2 Équipements collectifs : 27,2 [21,2]
  - 06.3 Alimentation en eau : 2,8
  - 06.4 Éclairage public : 1,8
  - 06.5 R-D : 0,0
  - 06.6 n.c.a. : 1,8
- **07 Santé, 261,2 Md€**
  - 07.1 Produits, appareils et matériels médicaux : 43,7
  - 07.2 Services ambulatoires : 91,8
  - 07.3 Services hospitaliers : 109,3
  - 07.4 Services de santé publique : 8,0 [2021 : 16,6]
  - 07.5 R-D dans le domaine de la santé : 6,7
  - 07.6 Santé n.c.a. : 1,6
- **08 Loisirs, culture et culte, 43,1 Md€**
  - 08.1 Services récréatifs et sportifs : 15,6
  - 08.2 Services culturels : 19,0
  - 08.3 Services de radiodiffusion, de télévision et d'édition : 7,6
  - 08.4 Culte et autres services communautaires : 0,7
  - 08.5 R-D : n.d.
  - 08.6 n.c.a. : 0,2
- **09 Enseignement, 148,6 Md€**
  - 09.1 Enseignement préélémentaire et primaire : 42,2
  - 09.2 Enseignement secondaire : 63,8
  - 09.3 Postsecondaire non supérieur : 1,2
  - 09.4 Enseignement supérieur : 12,3
  - 09.5 Enseignement non défini par niveau : 8,6
  - 09.6 Services annexes à l'enseignement : 20,0
  - 09.7 R-D : 0,0
  - 09.8 n.c.a. : 0,6
- **10 Protection sociale, 693,0 Md€**
  - 10.1 Maladie et invalidité : 83,9 [78,4]
  - **10.2 Vieillesse : 392,0** [369,1] ; soit 23,4 % du total et 13,4 % du PIB publié (13,35 % recalc.)
  - 10.3 Survivants : 40,6
  - 10.4 Famille et enfants : 66,7
  - 10.5 Chômage : 48,5 [2021 : 58,4]
  - 10.6 Logement : 21,1
  - 10.7 Exclusion sociale n.c.a. : 36,5
  - 10.8 R-D : n.d.
  - 10.9 Protection sociale n.c.a. : 3,7
- Groupes principaux en % du PIB 2024 recalculé sur 2 935,2 Md€ (calcul) :
  - vieillesse 13,35 ; maladie-invalidité 2,86 ; famille 2,27 ; chômage 1,65 ; survivants 1,38 ; exclusion 1,24 ; logement (10.6) 0,72 ;
  - hospitalier 3,73 ; ambulatoire 3,13 ; produits médicaux 1,49 ;
  - secondaire 2,17 ; primaire 1,44 ; supérieur 0,42 ;
  - dette 2,01 ; défense militaire 1,63 ; transports 2,07.

  — [Eurostat nama_10_gdp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp/A.CP_MEUR.B1GQ.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2024&endPeriod=2024&format=SDMX-CSV)

#### 1.5 France 2024 par sous-secteur
- **Répartition consolidée (tableau 3.307, somme = 1 671,8 Md€) :**

  | | APUC (S1311) | APUL (S1313) | ASSO (S1314) |
  |---|---|---|---|
  | Total | 590,8 | 322,2 | 758,8 |
  | Principales fonctions | GF01 113,9 (dont dette 46,5) ; GF02 54,2 ; GF03 41,9 ; GF04 110,8 (dont énergie 12,6 et transports 24,8) ; GF09 103,8 ; GF10 133,1 | GF01 59,3 (dont dette 6,1) ; GF04 54,8 (dont transports 35,9) ; GF05 25,5 ; GF06 36,1 ; GF08 29,9 ; GF09 44,9 ; GF10 59,2 | GF07 249,6 ; GF10 500,7 ; GF01 7,9 (dont dette 6,2) |
  | Détail de la protection sociale (GF10) | vieillesse 68,5 ; logement 21,1 ; maladie-invalidité 17,5 ; exclusion 17,4 ; chômage 4,2 ; famille 3,5 | exclusion 19,1 ; famille 17,4 ; maladie-invalidité 10,1 ; vieillesse 8,9 | vieillesse 314,5 ; maladie-invalidité 56,3 ; famille 45,8 ; chômage 44,3 |
  | Santé (GF07) | 9,1 | 2,4 | 249,6 |

  Les ASSO portent la totalité des groupes 07.1 (43,7), 07.2 (91,8) et 07.3 (109,3). — [Insee T_3307.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3307.xlsx) ; même ventilation dans l'[IP n° 2093](https://www.insee.fr/fr/statistiques/8735252) (591 / 322 / 759 Md€ ; les ASSO financent 501 Md€ de protection sociale et 250 Md€ de santé)
- **État (S13111, tableau 3.303, non consolidé avec les autres sous-secteurs) : total 600,7 Md€ en 2024 :**
  - GF01 147,8 ; GF02 57,2 ; GF03 41,7 ; GF04 86,1 ; GF05 5,9 ; GF06 3,7 ;
  - GF07 4,5 ; GF08 11,0 ; GF09 102,5 ; GF10 140,5.

  — [Insee T_3303.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3303.xlsx)
- **ODAC (S13112, tableau 3.304) : total 139,6 Md€ :**
  - GF04 66,1 ; GF01 23,8 ; GF09 17,5 ; GF07 11,3 ; GF08 9,8 ;
  - GF06 4,2 ; GF10 4,2 ; GF05 1,3 ; GF03 1,1 ; GF02 0,2.

  — [Insee T_3304.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3304.xlsx)
- **Totaux Eurostat par sous-secteur, non consolidés entre sous-secteurs :** S1311 670,3 Md€ ; S1313 329,7 Md€ ; S1314 778,4 Md€. La somme (1 778,4 Md€) dépasse le total S13 consolidé (1 671,8 Md€). — [Eurostat API gov_10a_exp, France](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.MIO_EUR+PC_GDP....FR?startPeriod=2023&format=SDMX-CSV)

#### 1.6 France 2024 par nature d'opération (S13, Md€)
- **Total 1 671,8 Md€ :**
  - D1 rémunérations : 362,1
  - P2 consommations intermédiaires : 161,1
  - D62 prestations sociales en espèces : 561,9
  - D632 prestations en nature (production marchande achetée) : 185,7
  - D3 subventions : 57,7
  - D4 revenus de la propriété (intérêts) : 60,2
  - D7 autres transferts courants : 93,2
  - D9 transferts en capital : 44,1
  - P5L investissement : 132,1
  - OED : 13,7

  — [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx) ; [Eurostat API France](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.MIO_EUR+PC_GDP....FR?startPeriod=2023&format=SDMX-CSV)
  - L'IP n° 2093 regroupe : rémunérations 362, consommations intermédiaires 161, subventions et autres transferts 209, intérêts 60, prestations en espèces 562, prestations en nature 186, investissement 132. — [IP n° 2093](https://www.insee.fr/fr/statistiques/8735252)
- **Croisement fonction × nature (2024, Md€) :**
  - **Enseignement** : D1 103,8 sur 148,6 (environ 70 %).
  - **Santé** : D632 136,2 (remboursements de soins et de médicaments) et D1 70,1. Le groupe 07.3 hospitalier comprend D1 63,8, P2 30,8 et FBCF 6,0. Les groupes 07.1 et 07.2 sont à 100 % en D632.
  - **Protection sociale** : D62 555,7, D632 44,8, D7 40,4, D1 32,4. La vieillesse comprend D62 362,2 et D632 10,8.
  - **Affaires économiques** : D3 subventions 51,1, P5L 34,2, P2 27,3, D9 26,5, D1 20,3.
  - **Services généraux** : D4 60,2, D1 47,6, D7 30,9.
  - **Défense** : D1 21,5, P2 19,5, P5L 11,3.

  — [Eurostat API France](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.MIO_EUR+PC_GDP....FR?startPeriod=2023&format=SDMX-CSV) ; [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
- **Moyennes 2014-2024 pour la fonction 10** (selon la fiche Insee) :
  - 595,6 Md€ par an, soit 24,4 % du PIB et 42,2 % des dépenses publiques ;
  - vieillesse : 55,3 % de la fonction ; survivants : 6,0 % ; maladie-invalidité : 11,6 % ; chômage : 9,7 % ; famille : 8,1 % ; exclusion : 5,0 % ; logement : 3,5 % ;
  - D62 : 80,0 % ; D632 : 6,7 % ; D7 : 5,3 % ; frais de fonctionnement (D1+P2+P5L) : 7,1 % ;
  - financement par sous-secteur : ASSO 72 %, État 19 %, APUL 8,5 %, ODAC 0,5 %.

  — [Insee, fiche méthodologique COFOG Protection sociale](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)

#### 1.7 Où sont publiées les données (Insee, Eurostat, OCDE) : formats et délais
- **Insee**
  - Publication : Insee Résultats « Dépenses des administrations publiques ventilées par fonction en [année] », une page par campagne. Pages des millésimes 2023 et 2024 : [Insee 8068626](https://www.insee.fr/fr/statistiques/8068626) ; [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707).
  - Fichiers : xlsx `https://www.insee.fr/fr/statistiques/fichier/8574707/T_330x.xlsx`, avec un onglet « Métadonnées » qui reprend les codes de type SDMX (STO, EXPENDITURE, REF_SECTOR, CONSOLIDATION).
  - Analyse annuelle : Insee Première (n° 2093 pour 2024).
  - Données téléchargeables : catalogue de données de l'Insee, jeu DD_CNA_APU.
  - — [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707)
- **Eurostat**
  - Jeu de données **gov_10a_exp** (« General government expenditure by function (COFOG) »), annuel.
  - Dimensions : unit (MIO_EUR, PC_GDP, PC_TOT…) × sector (S13, S1311, S1312, S1313, S1314) × cofog99 (TOTAL, GF01-GF10 et 69 groupes) × na_item (TE, D1, P2, D62, D632, D3, D4, D7, D9, P5, P51G, NP, OP5ANP…) × geo.
  - Accès : API SDMX 2.1, au format SDMX-CSV utilisé ici. — [Eurostat API gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)
  - Les agrégats de dépense totale à jour, y compris pour 2025, sont dans **gov_10a_main**. — [Eurostat API gov_10a_main](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_main/A.PC_GDP+MIO_EUR.S13.TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2022&format=SDMX-CSV)
  - Article de synthèse : Statistics Explained « Government expenditure by function – COFOG », avec tableaux Excel, mis à jour une fois par an (prochaine mise à jour prévue en mars 2027). — [Eurostat SE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
- **OCDE**
  - Tableau « Annual government expenditure by function (COFOG) », identifiant DSD_NASEC10@DF_TABLE11 sur l'OECD Data Explorer, couverture annoncée de 1970 à 2024. Cette information provient de miroirs de données (non vérifiée sur le site de l'OCDE). — [DBnomics (variante IDC)](https://db.nomics.world/OECD/DSD_NASEC10_IDC@DF_TABLE11_IDC) ; [Baselight](https://baselight.app/u/oecd/dataset/oecd_sdd_nad_dsd_nasec10_df_table11_v1_1)
  - Publication associée : *National Accounts of OECD Countries, General Government Accounts*. — [OCDE](https://www.oecd.org/en/publications/national-accounts-of-oecd-countries-general-government-accounts_22215352)

### Inferences
- **Délai de publication.** Pour l'année N, la COFOG française est produite vers la fin novembre N+1 (fichier daté du 28/11/2025 pour 2024). C'est cohérent avec la transmission à Eurostat à t+11 mois. L'Insee la diffuse et l'analyse entre décembre N+1 (annoncé pour 2025) et février-mars N+2 (2024 : IP du 05/02/2026, page datée du 27/03/2026). En octobre 2026, 2024 est donc la dernière année ventilée, tant à l'Insee qu'à Eurostat. La ventilation 2025 de l'Insee est attendue en décembre 2026, celle d'Eurostat avant l'article de mars 2027.
- **Total COFOG et compte APU révisé.** Le total COFOG 2024 (1 671,8 Md€) est antérieur au compte APU révisé de mars-mai 2026 : gov_10a_main donne 1 672,7 Md€ pour 2024, et le total 2025 de l'IP n° 2106 implique environ 1 672,4 Md€ (calcul : 1 714,2 / 1,025). L'écart de l'ordre de 1 Md€ ne sera résorbé qu'avec la publication de décembre 2026.
- **Totaux 2025 par sous-secteur.** La somme APUC + APUL + ASSO de l'IP n° 2106 vaut 1 819,9 Md€, soit plus que 1 714,2 Md€ (calcul). Ces totaux sont donc non consolidés entre sous-secteurs. Il ne faut pas les comparer aux 591 / 322 / 759 Md€ consolidés de 2024 (tableau 3.307).
- **Ordre de grandeur des dépenses sociales.** Santé et protection sociale réunies font 954,2 Md€ en 2024 (calcul), soit 57,1 % de la dépense publique. Le chiffre de « 954 milliards » de « dépenses sociales » diffusé par l'iFRAP correspond exactement à cette somme. — [iFRAP (titre)](https://www.ifrap.org/budget-et-fiscalite/2024-les-depenses-sociales-ont-atteint-954-milliards)

### Gaps
- **Nombre de classes.** Je n'ai pas pu vérifier sur une source primaire le nombre de classes (niveau III, 109 selon l'usage courant) : la page UNSD consultée ne donne pas les effectifs. Le chiffre de 69 groupes résulte de mon comptage des listes de codes.
- **Origine OCDE de la version 1999** (souvent citée) : non confirmée par la page UNSD consultée. Elle serait à vérifier dans la publication M84.
- **Première diffusion Eurostat des données 2024** : je n'ai pas trouvé de date exacte (communiqué de presse). Seules sont connues la dernière mise à jour (16/09/2026) et la date d'extraction de l'article SE (20/08/2026).
- **Écart de dates sur la page Insee 2024.** La page affiche « paru le 27/03/2026 » alors que l'IP date du 05/02/2026 : il s'agit peut-être d'une republication. Le jeu DD_CNA_APU n'a pas pu être consulté (indisponibilité signalée).
- **Fiche Insee n° 20** (« ventilation des dépenses des APU en base 2020 ») : non consultée. Elle contient probablement les règles détaillées pour l'État et les APUL.
- **OCDE** : ni la date de dernière mise à jour du tableau DF_TABLE11 ni l'édition la plus récente de *Government at a Glance* n'ont été vérifiées.

## 2. Comment la France se compare-t-elle à la moyenne de l'UE par fonction, et quelles fonctions expliquent l'écart de dépense totale ?

### Takeaway
En 2024, la France est le deuxième pays de l'UE pour la dépense publique rapportée au PIB, derrière la Finlande, et le deuxième pour la protection sociale. L'écart avec l'UE-27 varie de **7,9 à 8,4 points de PIB** selon le millésime du PIB utilisé.

Recalculé avec un PIB homogène, l'écart est de **8,0 points**, qui se décomposent ainsi :
- **protection sociale : +4,05 pts**, dont **vieillesse +2,70** ;
- **santé : +1,55 pt** ;
- logement et équipements collectifs : +0,70 ;
- affaires économiques : +0,39 (malgré des transports à −0,41) ;
- défense : +0,38 ;
- enseignement : +0,32 ;
- loisirs-culture : +0,29 ;
- environnement : +0,21 ;
- services généraux : +0,12, dont dette +0,08 ;
- ordre public : +0,04.

Retraites et santé expliquent donc à elles seules plus de la moitié de l'écart. En part de la dépense totale, la structure française reste proche de la moyenne européenne : le surplus de dépense est diffus, mais il se concentre dans les transferts sociaux.

### Cited Findings

#### 2.1 Comparaison 2024 en % du PIB (valeurs publiées de gov_10a_exp, S13)
Source : [Eurostat API gov_10a_exp (MAJ 16/09/2026, extraction du 18/10/2026)](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV). Les ratios publiés reposent sur le PIB du millésime retenu par Eurostat pour chaque pays (voir 2.3 et 4.2).

| Code | Fonction | France | UE-27 | ZE-20 | Allemagne | Italie | Espagne |
|---|---|---|---|---|---|---|---|
| TOTAL | Total | 57,3 | 48,9 | 49,3 | 49,4 | 50,4 | 45,5 |
| GF01 | Services généraux | 6,2 | 6,1 | 6,1 | 6,4 | 7,7 | 5,8 |
| GF0107 | dont dette publique | 2,0 | 1,9 | 1,9 | 1,1 | 4,0 | 2,5 |
| GF02 | Défense | 1,9 | 1,5 | 1,4 | 1,4 | 1,3 | 0,9 |
| GF03 | Ordre et sécurité publics | 1,8 | 1,7 | 1,7 | 1,6 | 1,8 | 1,8 |
| GF04 | Affaires économiques | 5,7 | 5,3 | 5,2 | 5,4 | 5,1 | 5,1 |
| GF0405 | dont transports | 2,1 | 2,5 | 2,3 | 2,7 | 2,4 | 1,8 |
| GF05 | Environnement | 1,0 | 0,8 | 0,9 | 0,6 | 0,9 | 1,0 |
| GF06 | Logements et équipements collectifs | 1,4 | 0,7 | 0,7 | 0,5 | 0,8 | 0,5 |
| GF07 | Santé | 8,9 | 7,3 | 7,5 | 7,6 | 6,6 | 6,5 |
| GF0702 | dont services ambulatoires | 3,1 | 2,3 | 2,4 | 2,3 | 2,4 | 2,3 |
| GF0703 | dont services hospitaliers | 3,7 | 3,3 | 3,2 | 2,9 | 2,7 | 2,7 |
| GF08 | Loisirs, culture et culte | 1,5 | 1,2 | 1,1 | 1,1 | 0,9 | 1,2 |
| GF09 | Enseignement | 5,1 | 4,7 | 4,6 | 4,5 | 4,0 | 4,1 |
| GF0904 | dont supérieur | 0,4 | 0,8 | 0,7 | 0,8 | 0,4 | 0,6 |
| GF10 | Protection sociale | 23,7 | 19,6 | 20,1 | 20,4 | 21,3 | 18,7 |
| GF1001 | Maladie et invalidité | 2,9 | 2,8 | 2,8 | 3,3 | 1,7 | 2,8 |
| GF1002 | Vieillesse | 13,4 | 10,7 | 10,9 | 9,9 | 13,9 | 10,4 |
| GF1003 | Survivants | 1,4 | 1,5 | 1,6 | 1,9 | 2,4 | 2,2 |
| GF1004 | Famille et enfants | 2,3 | 2,0 | 1,9 | 1,9 | 1,5 | 1,0 |
| GF1005 | Chômage | 1,7 | 1,2 | 1,3 | 1,7 | 0,9 | 1,5 |
| GF1006 | Logement | 0,7 | 0,4 | 0,4 | 0,4 | 0,0 | 0,0 |
| GF1007 | Exclusion sociale n.c.a. | 1,2 | 0,9 | 0,9 | 0,6 | 0,7 | 0,7 |

- **Montants 2024 (Md€, S13) :**

  | | France | UE-27 | ZE-20 | Allemagne | Italie | Espagne |
  |---|---|---|---|---|---|---|
  | Total | 1 671,8 | 8 854,5 | 7 538,3 | 2 139,7 | 1 109,2 | 725,0 |
  | Protection sociale | 693,0 | 3 541,4 | 3 071,1 | 883,2 | 468,1 | 297,5 |
  | Santé | 261,2 | 1 329,5 | 1 140,8 | 329,3 | 146,1 | 102,9 |

  — [Eurostat API gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)
- **Structure en % de la dépense totale (2024, PC_TOT) :**

  | | France | UE-27 | ZE-20 | Allemagne | Italie | Espagne |
  |---|---|---|---|---|---|---|
  | Protection sociale | 41,5 | 40,0 | 40,7 | 41,3 | 42,2 | 41,0 |
  | Santé | 15,6 | 15,0 | 15,1 | 15,4 | 13,2 | 14,2 |
  | Services généraux | 10,8 | 12,4 | 12,5 | 13,0 | 15,4 | 12,8 |
  | Affaires économiques | 9,9 | 10,8 | 10,6 | 11,0 | 10,1 | 11,2 |
  | Enseignement | 8,9 | 9,7 | 9,4 | 9,1 | 8,0 | 9,1 |
  | Défense | 3,2 | 3,0 | 2,8 | 2,7 | 2,6 | 2,0 |
  | Ordre public | 3,1 | 3,5 | 3,4 | 3,3 | 3,5 | 3,9 |
  | Loisirs-culture | 2,6 | 2,4 | 2,3 | 2,1 | 1,7 | 2,6 |
  | Logement et équipements | 2,5 | 1,5 | 1,5 | 1,0 | 1,5 | 1,1 |
  | Environnement | 1,8 | 1,7 | 1,7 | 1,1 | 1,8 | 2,1 |
  | dont vieillesse | 23,4 | 21,8 | 22,1 | 20,0 | 27,6 | 22,8 |
  | dont dette | 3,5 | 3,9 | 3,9 | 2,3 | 7,9 | 5,5 |

  — [Eurostat API gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)
- **Rappel 2023 (gov_10a_exp, % du PIB, France / UE-27) :**
  - total 56,9 / 48,8 ; protection sociale 23,3 / 19,1 ; santé 8,8 / 7,2 ; affaires économiques 6,3 / 5,8 ; enseignement 5,0 / 4,7.
  - Pour l'Italie, la fonction logement et équipements collectifs atteint 4,4 % du PIB en 2023, contre 0,8 % en 2024.

  — [Eurostat API gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)

#### 2.2 Ce qu'en dit Eurostat (Statistics Explained, données extraites le 20/08/2026)
- **UE-27 en 2024 : dépense totale de 8 855 Md€, soit 49,1 % du PIB** (48,9 % en 2023, pic de 52,9 % en 2020).

  | Fonction | Md€ | % du total | % du PIB |
  |---|---|---|---|
  | Protection sociale | 3 540 | 40,0 | 19,6 |
  | Santé | 1 331 | 15,0 | 7,4 |
  | Services généraux | 1 096 | 12,4 | 6,1 |
  | Affaires économiques | 954 | 10,8 | 5,3 |
  | Enseignement | 860 | 9,7 | 4,8 |
  | Ordre et sécurité | 314 | 3,5 | 1,7 |
  | Défense | 266 | 3,0 | 1,5 |
  | Loisirs-culture | 213 | 2,4 | 1,2 |
  | Environnement | 148 | 1,7 | 0,8 |
  | Logement | 133 | 1,5 | 0,7 |

  Autres éléments : vieillesse 10,7 % du PIB (10,4 % en 2023) ; chômage 214 Md€ (1,2 % du PIB). — [Eurostat SE COFOG](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
- **Classements 2024 en % du PIB :**
  - Dépense totale la plus élevée : Finlande 57,8 ; **France 57,0** ; Autriche 55,3 ; Belgique 54,1 ; Suède 50,5 ; Italie 50,4.
  - Protection sociale la plus élevée : Finlande 26,5 ; **France 23,6** ; Autriche 22,8 ; Italie 21,3 ; Belgique et Allemagne 20,4.
  - Les données françaises 2023-2024 sont provisoires.

  — [Eurostat SE COFOG](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)

#### 2.3 Lecture experte (FIPECO, 08/07/2026)
- François Ecalle, « Les dépenses par politique publique en Europe en 2024 », à partir des données Eurostat. FIPECO regroupe autrement les fonctions :
  - il place toute la santé et l'invalidité en protection sociale ;
  - il isole les intérêts et la recherche fondamentale des services généraux.

  Résultats (% du PIB, France / UE) :

  | Politique (regroupement FIPECO) | France | UE |
  |---|---|---|
  | **Total** | **57,3** | **49,1** (écart affiché : 8,2 pts) |
  | Protection sociale | 32,6 | 27,0 |
  | dont retraites | 14,8 | 12,2 |
  | dont santé | 11,8 | 10,2 |
  | dont famille | 2,3 | 2,0 |
  | dont chômage | 1,7 | 1,2 |
  | dont exclusion | 1,2 | 0,9 |
  | dont aides personnelles au logement | 0,7 | 0,4 |
  | Aides à la pierre, équipements collectifs | 1,4 | 0,7 |
  | Enseignement | 5,1 | 4,8 |
  | Affaires économiques | 5,7 | 5,3 |
  | dont transports | 2,1 | 2,5 |
  | Défense | 1,9 | 1,5 |
  | Intérêts | 2,0 | 1,9 |
  | Services généraux | 3,5 | 3,5 |
  | Recherche fondamentale | 0,7 | 0,7 |

  Les retraites sont « la plus importante source d'écart ». Le total UE retenu (49,1) et le total France (57,3) proviennent de millésimes de PIB différents. — [FIPECO](https://fipeco.fr/commentaire/Les%20d%C3%A9penses%20par%20politique%20publique%20en%20Europe%20en%202024)
- Mises en garde de FIPECO :
  - Les cotisations employeurs de retraite pèsent environ 4,0 % du PIB en France et en Belgique, contre 2,0 % en Allemagne et 0,9 % en Irlande. Le taux employeur des fonctionnaires civils de l'État (78,3 % en 2025) est jugé « excessivement élevé ».
  - Pour la recherche, il vaut mieux comparer le total : 1,8 % du PIB en France contre 1,3 % dans l'UE, car la frontière entre recherche fondamentale et appliquée varie d'un pays à l'autre.

  — [FIPECO](https://fipeco.fr/commentaire/Les%20d%C3%A9penses%20par%20politique%20publique%20en%20Europe%20en%202024)

#### 2.4 PIB utilisés pour les recalculs (2024, Md€)
Les PIB 2024 de nama_10_gdp (mise à jour du 15/10/2026) sont les suivants : France 2 935,2 ; UE-27 18 101,4 ; ZE-20 15 299,6 ; Allemagne 4 386,9 ; Italie 2 210,6 ; Espagne 1 598,6. — [Eurostat API nama_10_gdp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp/A.CP_MEUR.B1GQ.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2024&endPeriod=2024&format=SDMX-CSV)

### Inferences
- **Décomposition homogène de l'écart (calcul).** Méthode : montants gov_10a_exp rapportés au PIB nama_10_gdp du 15/10/2026, pour tous les pays.
  - Totaux 2024 : France 56,96 % ; UE-27 48,92 % ; ZE-20 49,27 % ; Allemagne 48,77 % ; Italie 50,17 % ; Espagne 45,35 %.
  - Écarts France − UE-27 = **+8,04 pts** :

    | Fonction | Écart (pts de PIB) | Détail par groupe |
    |---|---|---|
    | Protection sociale | +4,05 | vieillesse +2,70 ; chômage +0,47 ; logement (10.6) +0,37 ; exclusion +0,35 ; famille +0,29 ; maladie-invalidité +0,09 ; survivants −0,07 ; n.c.a. −0,15 |
    | Santé | +1,55 | ambulatoire +0,80 ; hospitalier +0,46 ; produits médicaux +0,35 |
    | Logement et équipements collectifs | +0,70 | |
    | Affaires économiques | +0,39 | transports −0,41 ; énergie −0,04 |
    | Défense | +0,38 | défense militaire +0,37 |
    | Enseignement | +0,32 | secondaire +0,45 ; services annexes +0,36 ; supérieur −0,34 ; primaire −0,21 |
    | Loisirs-culture | +0,29 | |
    | Environnement | +0,21 | |
    | Services généraux | +0,12 | dette +0,08 |
    | Ordre et sécurité publics | +0,04 | |

  - Vieillesse et santé réunies représentent environ 4,25 pts, soit 53 % de l'écart.
  - L'écart vaut 8,4 pts avec les ratios gov_10a_exp tels que publiés (57,3 contre 48,9), 7,9 pts selon l'article SE (57,0 contre 49,1) et 8,2 pts chez FIPECO.
- **France − ZE-20 (calcul) : +7,68 pts**, dont protection sociale +3,54 (vieillesse +2,48), santé +1,44, logement-équipements +0,71, défense +0,49, enseignement +0,45.
- **France − Allemagne (calcul) : +8,18 pts**, dont protection sociale +3,48. La vieillesse pèse +3,61, alors que l'Allemagne dépense davantage en maladie-invalidité (−0,42), survivants (−0,46) et protection sociale n.c.a. (−0,54). S'y ajoutent santé +1,39, logement-équipements +0,97 et dette +0,88.
- **France − Italie (calcul) : +6,79 pts.** L'Italie dépense nettement plus en intérêts (3,97 % du PIB contre 2,01 %, soit −1,96 pt) et un peu plus en vieillesse (13,86 % contre 13,35 %). L'écart provient donc de la santé (+2,29), de la protection sociale hors vieillesse et de l'enseignement (+1,03).
- **France − Espagne (calcul) : +11,61 pts**, dont protection sociale +5,00 (vieillesse +3,03) et santé +2,46.
- **Lecture générale.** La singularité française tient au niveau, plus qu'à la structure. Les parts de la protection sociale (41,5 % contre 40,0 %) et de la santé (15,6 % contre 15,0 %) dans la dépense totale sont proches de la moyenne de l'UE. Les parts des services généraux, des affaires économiques et de l'enseignement sont même plus faibles en France, parce que le dénominateur y est plus élevé. L'écart de niveau est donc concentré sur des transferts aux ménages, retraites en tête, et sur la santé financée par l'assurance maladie.
- **Effets de convention.** Le bond italien de la fonction logement en 2023 (4,4 % du PIB) correspond probablement à l'enregistrement en dépense des crédits d'impôt à la rénovation (« Superbonus »). Cette explication n'est pas vérifiée dans cette recherche, mais l'exemple montre à quel point des conventions comptables nationales peuvent déplacer les comparaisons fonctionnelles.

### Gaps
- **Article SE complet** : la liste par pays n'a pas été lue (seuls les extrêmes et la France sont cités). L'éventuel tableau Excel de l'article n'a pas été téléchargé.
- **Pas de comparaisons en standards de pouvoir d'achat (SPA) ni par habitant**, ni de comparaison OCDE, par exemple avec les données OCDE hors UE.
- **Comparaisons 2025 par fonction** : indisponibles avant début 2027.
- **Moyennes FIPECO pour la zone euro** : non disponibles dans la note de juillet 2026.

## 3. Comment les 10 divisions COFOG se rattachent-elles (approximativement) aux missions LOLF et aux branches de la Sécurité sociale, et aux outils citoyens « 1 000 € de dépense publique » ?

### Takeaway
Je n'ai trouvé **aucune table de passage officielle publiée** entre missions ou programmes LOLF et fonctions COFOG. L'Insee construit la COFOG de l'État à partir des comptes budgétaires de l'État. Sa fiche méthodologique « Protection sociale » donne de nombreuses affectations précises :
- CAS Pensions → 10.2 ;
- AAH et IJ → 10.1 ;
- APL/ALS/ALF (FNAL) et hébergement → 10.6 ;
- RSA, prime d'activité, AME et chèque énergie → 10.7 ;
- ASS et Unédic → 10.5.

Le périmètre du budget de l'État (APUC : 591 Md€ consolidés, soit 35 % du total) ne couvre qu'une partie de la COFOG. Les ASSO portent 759 Md€, dont l'essentiel de la santé (250 Md€) et 501 Md€ de protection sociale ; les APUL portent 322 Md€.

Les infographies gouvernementales « À quoi servent mes impôts ? / 1 000 € » sont des **regroupements des groupes COFOG de l'Insee** : 561 € de « protection sociale » (santé incluse) avec les données 2023, environ 567 € avec les données 2024.

### Cited Findings

#### 3.1 Comment l'Insee passe du budget et des comptes des APU à la COFOG
- **Sources.** La COFOG repose sur la comptabilité nationale des APU, alimentée par les comptabilités générales et par les comptes budgétaires de l'État. — [IP n° 2093 (méthodologie)](https://www.insee.fr/fr/statistiques/8735252)
- **Transferts.** Ils sont affectés à la fonction qu'ils financent lorsqu'elle est connue, sinon aux services généraux. Exemple donné par l'Insee : la DGF versée par l'État aux collectivités, ce qui « nuit » à la lecture par sous-secteur. Les intérêts de la dette sont conventionnellement classés en services généraux. — [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707) ; [Insee 8988847](https://www.insee.fr/fr/statistiques/8988847)
- **Affectations précises dans la fonction 10** (fiche Insee base 2020) :
  - **10.1 Maladie et invalidité** :
    - IJ maladie et AT-MP versées par la CNAM ;
    - pensions d'invalidité et d'incapacité permanente ;
    - aides de la CNSA aux établissements pour personnes handicapées ;
    - AAH, garantie pour travailleurs handicapés, MDPH ;
    - pensions d'invalidité des anciens combattants (État) ;
    - FIVA, ONIAM.
  - **10.2 Vieillesse** :
    - retraites de la Sécurité sociale (principalement CNAV), de l'État (CAS Pensions) et de l'Agirc-Arrco ;
    - régimes fermés (France Télécom, PTT, SNCF, RATP…) ;
    - APA (départements) ;
    - 50 % du crédit d'impôt pour l'emploi d'un salarié à domicile.
  - **10.3 Survivants** : pensions de réversion et de veuvage, dont Agirc-Arrco ; rentes mutualistes des anciens combattants ; ONaCVG.
  - **10.4 Famille et enfants** :
    - prestations familiales de la CNAF, congés maternité et paternité ;
    - crèches publiques, ASE, familles d'accueil ;
    - garde des moins de 6 ans, imputée à l'État.
  - **10.5 Chômage** :
    - allocations Unédic ;
    - allocations de solidarité de l'État (ASS…) ;
    - formation professionnelle des chômeurs ;
    - AGS ;
    - frais de France Travail et de l'Unédic.
  - **10.6 Logement** :
    - ALF, ALS, APL, enregistrées comme versées par le FNAL, qui appartient au secteur État : « les administrations de sécurité sociale (S1314) ne présentent aucune dépense dans la fonction logement » ;
    - aides à l'investissement HLM ;
    - hébergement d'urgence, CADA, HUDA.
  - **10.7 Exclusion sociale n.c.a.** :
    - RSA, RSA jeunes, RSA recentralisé ;
    - **AME** ;
    - prime d'activité ;
    - chèque énergie, indemnité carburant ;
    - dépenses pour les réfugiés, OFPRA, OFII ;
    - ANCT, LADOM, EPIDE.
  - **10.9 Protection sociale n.c.a.** : CCAS.

  — [Insee, fiche méthodologique COFOG Protection sociale](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
- **Frontière santé / protection sociale.** Les soins (remboursements de médicaments, consultations, hospitalisations) relèvent de la santé (07). Les IJ relèvent de la protection sociale (10). L'Insee conseille de « regrouper les fonctions santé (F7) et protection sociale (F10) pour se rapprocher du périmètre de la Sécurité sociale usuellement admis dans le débat public ». — [Insee, fiche méthodologique](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
- **Mesures énergie.**
  - Remise à la pompe et bouclier tarifaire, non soumis à condition de ressources : subventions (D31), classées en 04.3 « Combustibles et énergie ».
  - Chèque énergie et indemnité carburant, sous condition de ressources : prestations sociales, classées en 10.7.

  — [Insee, fiche méthodologique](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
- **Pensions de l'État (CAS Pensions).**
  - Les pensions versées sont classées « en intégralité en composante vieillesse (F10.2) ».
  - Les cotisations imputées (D122) sont ventilées « au prorata de la répartition des salaires (D11) dans les différentes fonctions COFOG », conformément au manuel COFOG 2019 (§3.5.1).
  - Taux du CAS en 2024 : 74,28 % pour les civils, 126,07 % pour les militaires.
  - Ratio D122/D11 de l'État : 53,4 % en 2024.

  — [Insee, fiche méthodologique](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)

#### 3.2 Poids respectifs des acteurs (2024, consolidé)
- **APUC (État + ODAC) : 590,8 Md€.** Elles portent toute la défense (54,2), l'essentiel de l'ordre public (41,9), deux tiers des affaires économiques (110,8) et de l'enseignement (103,8), 46,5 Md€ d'intérêts et 133,1 Md€ de protection sociale.
- **APUL : 322,2 Md€.** Elles portent 36,1 Md€ sur les 42,1 du logement et des équipements collectifs, 25,5 Md€ sur les 30,3 de l'environnement, 29,9 Md€ sur les 43,1 de la culture, 35,9 Md€ de transports et 44,9 Md€ d'enseignement.
- **ASSO : 758,8 Md€**, presque uniquement en santé (249,6) et en protection sociale (500,7).
- — [Insee T_3307.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3307.xlsx)

#### 3.3 Outils citoyens « À quoi servent mes impôts ? » / « 1 000 € »
- **Page officielle.** Elle s'intitule « A quoi servent mes impôts ? » et présente « comment sont utilisés 1000 € d'impôts, selon une répartition par catégories de dépenses (données 2024 source Insee/DGTrésor) », avec 561 € pour la protection sociale. **Non vérifié** : la page est protégée (HTTP 403) et ce contenu n'est connu que par l'extrait d'un moteur de recherche. — [economie.gouv.fr, « A quoi servent mes impôts ? »](https://www.economie.gouv.fr/node/3225744)
- **Ventilation détaillée relayée par MoneyVox (10/04/2025)**, sous la mention « ministère de l'Économie et des finances, données 2023 » :

  | Catégorie | Montant pour 1 000 € |
  |---|---|
  | **Protection sociale** | **561 €** |
  | dont retraites | 253 € |
  | dont santé | 201 € |
  | dont familles | 40 € |
  | dont chômage | 29 € |
  | dont autres solidarités | 25 € |
  | dont aides au logement | 13 € |
  | Éducation | 88 € |
  | Fonctionnement des administrations publiques | 66 € |
  | Soutien aux activités économiques | 59 € |
  | Transports et équipements collectifs | 50 € |
  | Charge de la dette | 31 € |
  | Défense | 31 € |
  | Recherche | 30 € |
  | Culture et loisirs | 26 € |
  | Sécurité | 25 € |
  | Environnement | 17 € |
  | Infrastructures | 11 € |
  | Justice | 5 € |

  — [MoneyVox](https://www.moneyvox.fr/impot/actualites/102917/retraites-education-defense-ou-va-argent-que-je-donne-aux-impots)
- **Version plus récente (source secondaire, non vérifiée).** BDOR et un résumé d'une page info.gouv.fr indiquent environ 567 € pour la protection sociale et environ 89 € pour l'éducation. Les deux pages sont inaccessibles ou n'ont pas été lues directement. — [BDOR](https://www.bdor.fr/actualites-or/impots-france-1000-euros-repartition-depenses-publiques) ; [info.gouv.fr (403)](https://www.info.gouv.fr/actualite/impots-comment-fonctionne-le-systeme-fiscal-francais)
- **Version 2019 (lue via résumé de recherche, non vérifiée).** Issue du grand débat, elle donnait 575 € de protection sociale, dont 268 € pour les retraites et 191 € pour l'assurance maladie. — [MoneyVox, article 71990](https://www.moneyvox.fr/actu/71990/575-euros-la-part-consacree-a-la-protection-sociale-pour-1-000-euros-de-depenses-publiques)
- **Critique de l'iFRAP (lue via résumé de recherche).** L'iFRAP juge le site « En avoir pour mes impôts » « rudimentaire » : il présente des catégories de dépense, sans relier un impôt donné à une dépense donnée. — [iFRAP](https://www.ifrap.org/budget-et-fiscalite/en-avoir-pour-mes-impots-pas-si-simple-en-france)

### Inferences
- **Correspondance approximative COFOG → missions LOLF → autres APU.** Cette table est construite par l'auteur des notes. Les intitulés de missions sont ceux des PLF récents et n'ont pas été vérifiés ligne à ligne. Les affectations en italique sont confirmées par la fiche Insee.

| Division COFOG | Missions LOLF (budget de l'État) principalement concernées | Autres APU / Sécurité sociale |
|---|---|---|
| 01 Services généraux | Engagements financiers de l'État (charge de la dette → 01.7) ; Gestion des finances publiques ; Action extérieure de l'État (01.1) ; Aide publique au développement (01.2) ; Direction de l'action du Gouvernement ; Pouvoirs publics ; Administration générale et territoriale de l'État ; part « recherche fondamentale » de Recherche et enseignement supérieur (01.4) ; Relations avec les collectivités territoriales et DGF (prélèvement sur recettes) : *classées en 01 tant que la destination n'est pas connue*, puis consolidées dans S13 | APUL : administration générale (01.3) ; CADES et ASSO : intérêts (01.7 ; 6,2 Md€ en 2024) |
| 02 Défense | Défense (02.1 ; R-D 02.4) | — |
| 03 Ordre et sécurité publics | Sécurités (police et gendarmerie → 03.1, sécurité civile → 03.2) ; Justice (tribunaux 03.3, administration pénitentiaire 03.4) | APUL : SDIS (03.2), polices municipales |
| 04 Affaires économiques | Écologie, développement et mobilité durables (transports 04.5, énergie 04.3, dont le bouclier tarifaire) ; Économie ; Travail et emploi (hors indemnisation, → 04.1) ; Agriculture (04.2) ; Investir pour la France de 2030 ; R-D appliquée (04.8) | APUL : transports (35,9 Md€) et action économique ; ODAC (66,1 Md€) |
| 05 Environnement | Écologie (biodiversité, prévention des risques) | APUL : déchets (05.1), eaux usées (05.2) |
| 06 Logement et équipements collectifs | Cohésion des territoires (aides à la pierre, urbanisme → 06.1, 06.2) | APUL : équipements collectifs et aménagement (06.2), eau (06.3), éclairage (06.4) |
| 07 Santé | Santé (santé publique, prévention → 07.4), mais *l'AME relève de 10.7* | ASSO : branche maladie (ONDAM soins de ville → 07.1/07.2 ; établissements → 07.3) |
| 08 Loisirs, culture et culte | Culture (08.2) ; Médias, livre et industries culturelles (08.3) ; Sport, jeunesse et vie associative (08.1) | APUL : 29,9 Md€ |
| 09 Enseignement | Enseignement scolaire (09.1, 09.2) ; Recherche et enseignement supérieur (09.4) | APUL : bâtiments scolaires, *périscolaire et accueils de loisirs → 09* |
| 10 Protection sociale | Régimes sociaux et de retraite et *CAS Pensions → 10.2* ; Solidarité, insertion et égalité des chances (*AAH → 10.1 ; prime d'activité, RSA recentralisé → 10.7*) ; Cohésion des territoires (*APL/FNAL et hébergement → 10.6*) ; Travail et emploi (*ASS → 10.5*) ; Anciens combattants (*10.1, 10.3*) ; Immigration, asile et intégration (*réfugiés, OFPRA, OFII → 10.7 ; CADA, HUDA → 10.6*) ; Écologie (*chèque énergie → 10.7*) ; Santé (*AME → 10.7*) | ASSO, APUL : voir la table suivante |

- **Branches et régimes de sécurité sociale → COFOG.** Les affectations en italique sont confirmées par la fiche Insee ; les autres sont des déductions.

| Branche ou organisme | Fonction COFOG | Montants 2024 |
|---|---|---|
| Maladie (CNAM, ONDAM) : soins | 07.1, 07.2, 07.3 (et 07.4) | ASSO : santé 249,6 Md€, dont 07.1 43,7 ; 07.2 91,8 ; 07.3 109,3. Les hôpitaux publics semblent classés dans les ASSO : le groupe 07.3 des ASSO contient 63,8 Md€ de rémunérations (déduction tirée des données) |
| Maladie et AT-MP : prestations en espèces | *10.1* (IJ, invalidité, incapacité permanente) | ASSO 10.1 : 56,3 |
| Vieillesse (CNAV et régimes de base, régimes spéciaux) et Agirc-Arrco | *10.2* (droits propres), *10.3* (réversion) | ASSO 10.2 : 314,5 |
| Famille (CNAF) | *10.4* (prestations familiales). En revanche, les aides au logement versées par les CAF sont *enregistrées au FNAL (État), en 10.6*, et le RSA et la prime d'activité *en 10.7* (départements, État) | ASSO 10.4 : 45,8 |
| Autonomie (CNSA, branche créée en 2021) | *10.1* (établissements pour personnes handicapées) ; *10.2* (APA, versée via les départements) | non isolable |
| Assurance chômage (Unédic) et France Travail | *10.5* | ASSO 10.5 : 44,3 |
| Dette sociale (CADES) | 01.7 | ASSO 01.7 : 6,2 |

- **Cohérence des outils citoyens avec la COFOG (calcul).** Les montants « pour 1 000 € » se retrouvent à partir des groupes COFOG 2023 de l'Insee :
  - éducation : GF09 141,6 / 1 607,4 → 88 € ;
  - famille : 10.4 → 40 € ; chômage : 10.5 → 29 € ; aides au logement : 10.6 → 13 € ;
  - justice : 03.3 → 5 € ; culture : GF08 → 26 € ;
  - retraites : 10.2 + 10.3 → 254 € (253 € publiés) ;
  - recherche : 01.4 + groupes R-D → environ 31 € ;
  - protection sociale santé incluse, hors R-D santé : (657,9 + 249,7 − 6,5) / 1 607,4 → 561 €.

  Avec les données 2024, le même regroupement donne (693,0 + 261,2 − 6,7) / 1 671,8 → 567 €, et l'éducation 89 €, soit exactement les valeurs relayées par les sources secondaires récentes. On peut en déduire que l'infographie « données 2024 » donne 567 € et que les 561 € correspondent aux données 2023. L'extrait de la page officielle mêle sans doute deux versions.
- **Ce qu'il faut retenir pour la synthèse.** Le « 1 000 € » est une présentation de la **dépense publique totale consolidée, toutes APU**, et non du seul budget de l'État ni de l'usage d'un impôt particulier. Plus de la moitié de cette dépense est portée par les ASSO, financées surtout par cotisations et CSG.

### Gaps
- **Table de passage LOLF → COFOG** : aucune table officielle trouvée, ni dans les documents budgétaires (PLF, RAP, compte général de l'État) ni sur data.economie.gouv.fr. La fiche Insee n° 20 « ventilation des dépenses des APU en base 2020 » n'a pas été consultée et pourrait contenir les règles de passage pour l'État.
- **Avis d'impôt** : je n'ai pas pu vérifier sur source primaire que l'infographie « 1 000 € » accompagne l'avis d'impôt ou figure sur impots.gouv.fr. Les pages economie.gouv.fr et info.gouv.fr renvoient une erreur 403 (protection anti-robot). La date de lancement et l'URL exactes du site « En avoir pour mes impôts » ne sont pas non plus vérifiées.
- **Médico-social** : la ventilation des dépenses médico-sociales de l'ONDAM et de la CNSA entre les fonctions 07 et 10 n'a pas été documentée au-delà de la fiche Insee.

## 4. Quelles précautions garder à l'esprit pour interpréter la COFOG appliquée à la France ?

### Takeaway
Plusieurs précautions s'imposent :
- **Distinguer** les données consolidées (S13) des données non consolidées par sous-secteur.
- **Toujours dater** le millésime, à la fois des dépenses et du PIB : pour 2024, 57,0 % ou 57,3 % du PIB selon la source.
- **Garder en tête trois conventions de classement** :
  - les intérêts sont en 01.7 ;
  - les soins relèvent de 07, mais les IJ et l'invalidité de 10.1, et l'AME de 10.7 ;
  - le bouclier tarifaire est en 04.3, mais le chèque énergie en 10.7.
- **Se méfier des comparaisons internationales**, sensibles aux cotisations retraite imputées, au traitement fiscal des prestations, à l'organisation hospitalière et aux crédits d'impôt.
- **Ne pas surinterpréter** les groupes (niveau II) et les variations d'une année sur l'autre, qui peuvent refléter des changements de nomenclature (par exemple celui des collectivités locales en 2024).

### Cited Findings

#### 4.1 Consolidation et sous-secteurs
- Les tableaux Insee sont consolidés à l'intérieur de chaque sous-secteur : « hors dépenses à l'intérieur du sous-secteur (intérêts, transferts courants et en capital) ». Seul le tableau 3.307 répartit le total S13 consolidé (591 + 322 + 759 = 1 672 Md€). — [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx) ; [Insee T_3307.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3307.xlsx)
- Les totaux Eurostat par sous-secteur (S1311 670,3 ; S1313 329,7 ; S1314 778,4 Md€) font 1 778,4 Md€, contre 1 671,8 Md€ consolidés. L'État seul pèse 600,7 Md€ en non consolidé (tableau 3.303), car il inclut ses transferts aux autres APU. — [Eurostat API France](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.MIO_EUR+PC_GDP....FR?startPeriod=2023&format=SDMX-CSV) ; [Insee T_3303.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3303.xlsx)
- Les transferts dont la destination est inconnue (par exemple la DGF) sont classés en services généraux, ce qui « nuit » à la lecture par sous-secteur. — [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707)

#### 4.2 Millésimes, révisions et dénominateur PIB
- **Calendrier des révisions.** Les données 2024 sont provisoires, avec une version semi-définitive à l'automne 2026 et une version définitive à l'automne 2027. — [IP n° 2093](https://www.insee.fr/fr/statistiques/8735252)
  - Selon un résumé de recherche (page non ouverte), l'Insee signale aussi que les données COFOG peuvent être modifiées à la publication suivante, à la suite des échanges avec Eurostat. — [Insee 8068626](https://www.insee.fr/fr/statistiques/8068626)
- **Rupture de nomenclature en 2024.** Un changement de nomenclature comptable des collectivités locales gonfle « Logements et équipements collectifs » (+18,3 % ; le groupe 06.2 passe de 21,2 à 27,2 Md€) et minore « Affaires économiques ». L'effet sera neutralisé dans les données définitives. — [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707) ; [IP n° 2093](https://www.insee.fr/fr/statistiques/8735252)
- **Ratio au PIB pour 2024 : plusieurs valeurs coexistent.**
  - 57,3 % dans gov_10a_exp (mise à jour du 16/09/2026), qui repose sur un PIB d'un millésime antérieur. — [Eurostat gov_10a_exp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.PC_GDP+MIO_EUR+PC_TOT.S13..TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2019&format=SDMX-CSV)
  - 57,0 % dans gov_10a_main (mise à jour du 21/07/2026), dans l'IP n° 2106 et dans l'article SE. — [Eurostat gov_10a_main](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_main/A.PC_GDP+MIO_EUR.S13.TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2022&format=SDMX-CSV) ; [IP n° 2106](https://www.insee.fr/fr/statistiques/8997691) ; [Eurostat SE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
  - Le PIB français de 2024 vaut 2 935,2 Md€ dans nama_10_gdp (mise à jour du 15/10/2026, provisoire). — [Eurostat nama_10_gdp](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp/A.CP_MEUR.B1GQ.FR+EU27_2020?startPeriod=2022&format=SDMX-CSV)
  - L'article SE prévient : « GDP used for ratios varies by source and date », avec des mises à jour en avril et juillet 2026. — [Eurostat SE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
- **Total des dépenses 2024 selon les sources.** Il vaut 1 671,8 Md€ dans la COFOG (millésime de novembre 2025) et 1 672,7 Md€ dans gov_10a_main (juillet 2026). — [Eurostat gov_10a_main](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_main/A.PC_GDP+MIO_EUR.S13.TE.FR+EU27_2020+EA20+DE+IT+ES?startPeriod=2022&format=SDMX-CSV)

#### 4.3 Conventions de classement propres à la COFOG ou à la France
- **Intérêts dans les services généraux.**
  - Les intérêts de la dette sont conventionnellement classés en services généraux. — [Insee 8988847](https://www.insee.fr/fr/statistiques/8988847)
  - En 2024, 01.7 vaut 58,9 Md€ : D4 60,2 Md€, plus une consommation intermédiaire négative de −1,3 Md€ dont la nature n'a pas été vérifiée. L'IP n° 2093 parle d'une « charge de la dette » de 60 Md€ (+13,8 %). L'IP n° 2106 donne des charges d'intérêts 2025 de 64,7 Md€ (+11,2 %). — [Eurostat API France](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/gov_10a_exp/A.MIO_EUR+PC_GDP....FR?startPeriod=2023&format=SDMX-CSV) ; [IP n° 2093](https://www.insee.fr/fr/statistiques/8735252) ; [IP n° 2106](https://www.insee.fr/fr/statistiques/8997691)
  - **Contradiction à signaler.** Selon le résumé de l'IP n° 2093, les intérêts des ASSO seraient répartis entre santé et protection sociale. Or les tableaux 3.307 et gov_10a_exp ne montrent aucun intérêt (D4) en 07 ou 10, et 6,2 Md€ d'intérêts des ASSO en 01.7. Les tableaux font foi. — [Insee T_3307.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3307.xlsx)
- **Santé et protection sociale.**
  - La frontière entre ces deux fonctions « peut nuire à la comparabilité des résultats internationaux ». — [Insee 8574707](https://www.insee.fr/fr/statistiques/8574707)
  - L'AME est classée en 10.7, pas en santé. — [Insee, fiche méthodologique](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
  - Les comptes satellites (comptes de la santé et de la protection sociale) dépassent en général la division COFOG correspondante. — [Eurostat SE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
  - Selon les estimations précoces ESSPROS d'Eurostat (lues via résumé de recherche), les prestations de protection sociale représentent 31,9 % du PIB en France en 2024. La COFOG donne 23,6 % pour la seule fonction 10, et 32,5 % pour les fonctions 07 et 10 réunies (calcul). — [Eurostat, Social protection statistics – early estimates](https://ec.europa.eu/eurostat/statistics-explained/index.php/Social_protection_statistics_-_early_estimates)
- **Cas frontières tranchés par convention :**
  - hébergement d'urgence et CADA en 10.6, et non en 10.7 ;
  - garde des moins de 6 ans en 10.4 (État), mais accueils de loisirs périscolaires en 09 (communes) ;
  - crédit d'impôt pour les services à la personne partagé à 50 % en 10.2 et à 50 % en 04.7 ;
  - logement social (HLM) classé en sociétés non financières (S11) : seules les aides publiques sont comptées ;
  - mesures énergie : D3 en 04.3 ou prestations en 10.7, selon la condition de ressources.

  — [Insee, fiche méthodologique](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
  - Eurostat note que les mesures de soutien face aux prix de l'énergie n'ont pas été enregistrées de façon pleinement harmonisée entre pays. — [Eurostat SE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG)
- **Pensions des fonctionnaires.**
  - Les cotisations imputées du CAS Pensions (D122) gonflent la masse salariale de chaque fonction au prorata des salaires, en plus de la comptabilisation des pensions en 10.2. — [Insee, fiche méthodologique](https://www.insee.fr/fr/metadonnees/source/fichier/Fiche_methodologique_prot_soc.pdf)
  - FIPECO estime le poids des cotisations employeurs de retraite à environ 4,0 % du PIB en France, contre 2,0 % en Allemagne, ce qui pèse sur les comparaisons de coûts des fonctions régaliennes et éducatives. — [FIPECO](https://fipeco.fr/commentaire/Les%20d%C3%A9penses%20par%20politique%20publique%20en%20Europe%20en%202024)
- **Défense.** La défense au sens COFOG (54,2 Md€, 1,9 % du PIB) n'est pas comparable à la défense au sens de l'OTAN, qui traite différemment les pensions, une partie de l'ordre public et les cotisations employeurs. — [Eurostat SE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_by_function_%E2%80%93_COFOG) ; [IP n° 2093](https://www.insee.fr/fr/statistiques/8735252)
- **Recherche.**
  - La recherche est éclatée entre 01.4 (19,9 Md€) et les groupes R-D de chaque division (04.8 : 21,4 ; 07.5 : 6,7 ; 02.4 : 1,7 ; 05.5 : 1,8). — [Insee T_3301.xlsx](https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx)
  - La frontière entre recherche fondamentale et appliquée diffère d'un pays à l'autre. — [FIPECO](https://fipeco.fr/commentaire/Les%20d%C3%A9penses%20par%20politique%20publique%20en%20Europe%20en%202024)

### Inferences
- **Brut et net.** La COFOG mesure des dépenses brutes. En France, beaucoup de prestations (retraites notamment) sont assujetties à la CSG ou à l'impôt, ce qui gonfle leur poids par rapport aux pays qui versent des prestations nettes ou recourent à des dépenses fiscales. Les crédits d'impôt non remboursables (« niches ») n'apparaissent pas en dépense. Ces deux effets biaisent les comparaisons de niveau : point bien établi dans la littérature, mais non vérifié ici sur source primaire.
- **Enseignement supérieur.** Le faible poids de 09.4 en France (0,42 % du PIB contre 0,76 % dans l'UE) s'explique probablement en partie par le classement d'une partie de la recherche universitaire et publique en 01.4. Il faut donc comparer « supérieur + recherche » plutôt que 09.4 seul (déduction).
- **Hôpitaux publics.** Ils semblent comptés dans les ASSO, puisque le groupe 07.3 des ASSO contient 63,8 Md€ de rémunérations. Les comparaisons par sous-secteur avec des pays où les hôpitaux dépendent des collectivités locales, ou sont des producteurs marchands, ne sont donc pas pertinentes. Seules les comparaisons en S13 consolidé ont du sens (déduction).
- **Fiabilité des niveaux.** Les groupes (niveau II), obligatoires seulement depuis 2001, reposent davantage sur des clés de répartition que les divisions. Il faut privilégier les divisions pour les comparaisons internationales et lire les groupes comme des ordres de grandeur, par exemple 01.3 « Services généraux » (53,8 Md€) ou 06.2 (déduction).
- **Chocs et ruptures de série.** Plusieurs groupes enregistrent des variations ponctuelles :
  - 04.3 : 9,8 Md€ en 2021, puis 32,6 en 2022 et 15,5 en 2024 (bouclier tarifaire) ;
  - 07.4 : 16,6 Md€ en 2021, puis 8,0 en 2024 (Covid) ;
  - 10.5 : 58,4 Md€ en 2021, puis 44,2 en 2022 (activité partielle, classée en chômage) ;
  - 04.1 : 66,7 Md€ en 2021, puis 43,8 en 2022 (aides d'urgence).

  Il faut des moyennes pluriannuelles pour juger d'une structure. La révision en cours de la COFOG à l'ONU, attendue d'ici 2028, créera par ailleurs une rupture de série (déduction tirée des sources UNSD et Insee citées plus haut).
- **Double comptabilisation apparente.** Le « coût » d'une politique en COFOG inclut sa part de frais de fonctionnement et de cotisations imputées, mais pas sa part d'intérêts ni de services généraux. FIPECO souligne qu'une comparaison en « coût complet » demanderait d'en réaffecter une partie.

### Gaps
- **Recensement Eurostat des écarts de classement** : je n'ai pas trouvé d'inventaire officiel des écarts de classement COFOG entre pays (par exemple les réserves de qualité ou les rapports d'inventaire COFOG par pays). Il faudrait consulter le manuel COFOG 2019 et les métadonnées nationales Eurostat.
- **Différence 01.7 / D4 / « charges d'intérêts »** : l'écart entre 58,9 et 60,2 Md€ pour 2024, puis la base 2024 implicite de l'IP n° 2106 (environ 58,2 Md€, soit 64,7 / 1,112 par calcul), n'est pas expliqué. Il s'agit peut-être d'un traitement des SIFIM ou d'une révision, non vérifiée.
- **Date de la fiche méthodologique Insee.** La fiche « Protection sociale » est datée du « 6 février 2025 », mais elle cite des moyennes 2014-2024 et des taux 2024. La date est probablement erronée (2026 ?) et reste à vérifier.
