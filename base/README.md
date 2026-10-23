# La base des chiffres

Chaque chiffre est enregistré avec sa fiche d'identité complète : ce qui est mesuré, selon quelle norme, sur quel périmètre, dans quelle unité, pour quelle période, dans quelle version, et où il se trouve exactement dans sa source. Deux chiffres ne se comparent que si leurs fiches coïncident ; sinon, la fiche dit en quoi ils diffèrent.

La base est faite de tables en texte (CSV) décrites par des schémas, au format ouvert [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/). Chaque modification est visible dans l'historique du dépôt. Une base SQLite interrogeable se reconstruit à partir de ces tables à tout moment.

## Ce qu'elle contient

| Source | Contenu | Années |
|---|---|---|
| Insee, tableaux 3.201 à 3.214 des comptes nationaux annuels | dépenses et recettes par nature, au sens du SEC 2010, des administrations publiques et de chacun de leurs sous-secteurs : État, organismes divers d'administration centrale, collectivités locales (communes, départements, régions, syndicats), organismes divers d'administration locale, sécurité sociale (régimes d'assurance sociale, hôpitaux) | 1959-2025 pour l'ensemble des administrations publiques ; depuis 1978 pour l'administration centrale, l'État, ses organismes, les administrations locales et la sécurité sociale ; depuis 2013 pour les collectivités locales, les organismes locaux, les régimes d'assurance sociale et les hôpitaux ; depuis 2019 pour les communes, départements, régions et syndicats |
| Insee, tableau 3.106 | déficit public au sens de Maastricht par sous-secteur, en milliards d'euros et en % du PIB | 1949-2025 (depuis 1959 pour l'État et ses organismes) |
| Insee, tableau 3.101 | dette publique au sens de Maastricht par sous-secteur, en milliards d'euros et en % du PIB | 1978-2025 |
| Insee, tableaux 3.301 à 3.306 | dépenses par fonction (classification COFOG : 10 divisions et 69 groupes), croisées avec leur nature (rémunérations, consommations intermédiaires, prestations, investissement…), pour l'ensemble des administrations publiques et chacun de leurs sous-secteurs | 1995-2024 (depuis 2009 pour l'État et ses organismes) |
| Insee, tableau 3.307 | part de chaque sous-secteur dans la dépense consolidée de l'ensemble des administrations publiques, par fonction | 2009-2024 |
| Insee, tableau 3.217 | principaux impôts, un par un (TVA, accises sur l'énergie, taxe foncière, CSG, impôt sur le revenu, impôt sur les sociétés, droits de succession…), rangés dans leur catégorie du SEC 2010, et le passage de l'ensemble des impôts et cotisations aux prélèvements obligatoires | 1995-2025 |
| Insee, tableau 3.216 | prélèvements obligatoires par bénéficiaire : État, organismes divers d'administration centrale, administrations locales, sécurité sociale, Union européenne | 1959-2025 (depuis 1978 pour l'État et ses organismes) |
| Insee, tableau 3.107 | passage du résultat d'exécution des lois de finances (le solde du budget de l'État) au déficit de l'État au sens de Maastricht, correction par correction | 2009-2025 |
| Insee, tableau 3.108 | passage du résultat comptable du régime général de la sécurité sociale au déficit de l'ensemble des administrations de sécurité sociale : corrections, puis soldes de la CADES, du Fonds de réserve pour les retraites, des autres régimes et des organismes dépendants | 2009-2025 |
| Projets de loi d'approbation des comptes de l'État (de règlement jusqu'aux comptes de 2022, relatifs aux résultats de la gestion depuis), textes publiés par le Sénat | budget de l'État exécuté, à l'euro près : résultat budgétaire ; recettes et dépenses du budget général, des budgets annexes et des comptes spéciaux ; autorisations d'engagement consommées et dépenses par mission et par programme ; chaque budget annexe et chaque compte spécial, compte par compte et programme par programme, avec ses recettes et, pour les comptes spéciaux, leurs soldes au 31 décembre | 2006-2025, depuis le premier budget voté selon la loi organique relative aux lois de finances (LOLF) |
| Les mêmes textes, articles 2 et 3 et article liminaire | tableau de financement de l'État : besoin de financement (amortissement de la dette, déficit à financer) et ressources qui le couvrent ; compte de résultat et bilan de l'État en droits constatés ; soldes structurel, conjoncturel et effectif de l'ensemble des administrations publiques et, depuis les comptes de 2023, leur dette, leur taux de prélèvements obligatoires et leur dépense | 2006-2025, bilan d'ouverture au 1er janvier 2006 compris ; article liminaire depuis les comptes de 2012 |
| Lois de financement de la sécurité sociale (comptes de 2004 à 2021) et projets de loi d'approbation des comptes de la sécurité sociale (depuis ceux de 2022), textes publiés par le Sénat | recettes, dépenses et solde de l'exercice clos, par branche (maladie, accidents du travail et maladies professionnelles, vieillesse, famille et, depuis 2021, autonomie), de l'ensemble des régimes obligatoires de base et du régime général (jusqu'en 2021), et ceux des organismes qui concourent à leur financement (Fonds de solidarité vieillesse ; FFIPSA et CNSA les premières années) ; dépenses constatées dans le champ de l'objectif national de dépenses d'assurance maladie (ONDAM), recettes affectées au Fonds de réserve pour les retraites et mises en réserve par le FSV, dette amortie par la CADES ; depuis les comptes de 2022, recettes, dépenses et solde des administrations de sécurité sociale en % du PIB | 2004-2025 |
| Les mêmes textes, annexe A | situation patrimoniale au 31 décembre des régimes de base, du FSV, de la CADES et du FRR : actif et passif, fonds propres, dettes financières, avec les lignes de chaque entité (régime général, autres régimes, FSV, CADES, FRR, Acoss) ; évolution depuis 2009 de leur passif net, de leur endettement financier net et de leur résultat | 2009-2025 (situation patrimoniale depuis les comptes de 2010, évolution depuis ceux de 2013) |
| Rapports de l'Observatoire des finances et de la gestion publique locales (OFGL), annexe 2A, tableaux de la DGCL | comptes des budgets principaux des collectivités locales, niveau par niveau : communes, groupements de communes à fiscalité propre, secteur communal, départements, régions et collectivités territoriales uniques, syndicats, et leurs ensembles ; pour la dernière année de chaque rapport, chaque type de groupement (métropoles, communautés urbaines, d'agglomération, de communes). Dépenses et recettes de fonctionnement (achats, personnel, interventions ; impôts locaux, fraction de TVA, droits de mutation, dotations de l'État…), dépenses et recettes d'investissement, épargne, capacité ou besoin de financement, emprunts, remboursements et dette au 31 décembre | 2017-2025 |
| Les mêmes rapports, annexes 2B, 2C et 2D | les mêmes comptes pour les budgets annexes de chaque niveau ; pour les budgets principaux et annexes de chaque niveau, consolidés des flux croisés entre eux ; pour le bloc communal et l'ensemble des collectivités locales, consolidés aussi entre niveaux : tous les budgets de toutes les collectivités locales, sans double compte. Pour la dernière année de chaque rapport, le nombre de budgets principaux et annexes de chaque niveau | 2017-2025 (nombre de budgets depuis 2020) |
| Direction générale des collectivités locales (DGCL), « Les finances des départements » et « Les finances des régions » | comptes de chaque département, de la métropole de Lyon, de la Ville de Paris, de chaque région et des collectivités territoriales uniques (Corse, Guyane, Martinique), et leurs totaux : dépenses et recettes de fonctionnement et d'investissement et leur détail (personnel, interventions, impôts locaux, droits de mutation, dotations de l'État…), intérêts, emprunts, remboursements et dette, soldes de gestion | 2020-2024 |
| Insee, situation mensuelle du budget de l'État | dépenses, recettes, solde des comptes spéciaux et solde général d'exécution, cumulés depuis janvier, chaque mois | janvier 2009 à août 2026 |
| Eurostat, `gov_10a_main`, `gov_10a_exp`, `nama_10_gdp` | dépenses, recettes, solde et intérêts des administrations publiques ; dépenses par fonction (COFOG) ; PIB | 1995-2025 (dépenses par fonction jusqu'en 2024) ; PIB depuis 1975 |

Les tableaux de l'Insee font foi pour la France : Eurostat reprend les comptes que l'Insee lui transmet, et le [rapport de cohérence](../controles/coherence.md) montre où les deux concordent et où ils s'écartent.

## Les tables

| Table | Contenu |
|---|---|
| `tables/chiffres/<producteur>/<tableau>.csv` | les chiffres, un par ligne, avec leur fiche d'identité ; un fichier par source (un tableau de l'Insee, un jeu de données d'Eurostat), et `tiers.csv` pour les chiffres cités par un tiers |
| `tables/sources.csv` | producteurs et publications : statistiques officielles, documents publics, articles, communications |
| `tables/fichiers.csv` | copies archivées des fichiers sources : requête exacte, date, empreinte SHA-256 |
| `tables/concepts.csv` | ce qui est mesuré, défini dans une norme (par exemple la dépense totale au sens du SEC 2010) |
| `tables/normes.csv` | normes et méthodes de référence |
| `tables/perimetres.csv` | secteurs et sous-secteurs : administrations publiques, administration centrale, locale, sécurité sociale… |
| `tables/fonctions.csv` | fonctions de la dépense : divisions et groupes de la COFOG, missions et programmes du budget de l'État, branches de la sécurité sociale |
| `tables/unites.csv` | unités : millions d'euros, % du PIB, % de la dépense… |
| `tables/traitements.csv` | retraitements nommés, appliqués à certains chiffres |
| `tables/calculs.csv` | recettes de nos propres calculs : formule, chiffres d'entrée, script |
| `tables/corrections.csv` | journal des corrections de nos erreurs d'enregistrement |
| `archives/` | les copies archivées elles-mêmes |
| `schemas/` | la description de chaque table : colonnes, types, valeurs permises, références |

## La fiche d'identité d'un chiffre

| Colonne | Signification |
|---|---|
| `concept_id` | ce qui est mesuré, avec sa norme |
| `perimetre_id`, `zone` | qui est couvert, dans quel pays |
| `fonction_id` | la fonction de la dépense : COFOG, mission et programme du budget de l'État, ou branche de la sécurité sociale ; vide pour l'ensemble |
| `traitements` | les retraitements appliqués, vides s'il n'y en a pas (par exemple `cumul_depuis_janvier` pour un montant cumulé depuis le début de l'année) |
| `unite_id`, `decimales` | l'unité, et le nombre de décimales de la valeur telle qu'elle figure dans la source |
| `periode` | l'année, le trimestre ou le mois |
| `statut` | prévision, estimation, provisoire, semi-définitif, définitif, ou non précisé par la source |
| `version` | la date de la version de la source d'où vient le chiffre |
| `consolidation` | avec ou sans les flux entre administrations : `consolide` (sans les flux internes au périmètre), `consolide_apu` (part du périmètre dans la dépense consolidée de l'ensemble des administrations publiques : sans ses flux internes, ni ceux avec les autres sous-secteurs), `non_consolide`, ou `sans_objet` (un solde, le PIB) |
| `denominateur_id` | pour un ratio, l'identifiant du chiffre qui lui sert de dénominateur, quand la source l'indique |
| `source_id`, `fichier_id`, `emplacement` | la source, la copie archivée et l'endroit exact |
| `nature` | `publie` par la source elle-même, `cite` par un tiers, ou `calcule` ici |

L'identifiant d'un chiffre est formé de ses composantes, séparées par « : » (« - » pour une composante vide). Il ne change jamais. Par exemple :

```
insee.t3201:FR:S13:SEC2010.TE:-:-:MD_EUR:2025:2026-08-10
```

se lit : selon le tableau 3.201 de l'Insee, dépense totale au sens du SEC 2010 des administrations publiques françaises, ensemble des fonctions, sans retraitement, en milliards d'euros, pour 2025, dans la version du 10 août 2026.

Selon la source :

- **Version.** Pour Eurostat, la date de mise à jour du jeu de données. Pour l'Insee, la date de dernière modification que le classeur porte en lui-même, à défaut sa date de création ; pour une série de sa Banque de données macro-économiques, la date de dernière mise à jour de la série. Pour un texte publié par le Sénat, la date qu'il porte : enregistrement, transmission ou adoption. Pour un rapport de l'OFGL ou une publication de la DGCL, la date de modification inscrite dans le classeur.
- **Statut.** Eurostat le donne par un indicateur attaché à chaque valeur, conservé dans `drapeau_source`. L'Insee le donne par le calendrier de ses comptes annuels : la dernière année publiée est provisoire, l'avant-dernière semi-définitive, les précédentes définitives. L'OFGL marque provisoires les montants de la dernière année de chaque rapport ; les autres sont définitifs, comme les comptes de gestion que publie la DGCL.
- **Décimales.** Le nombre de décimales de la valeur enregistrée dans le fichier source, sans les zéros finaux, que le fichier ne conserve pas. Une valeur nulle est exacte : elle prend la précision de sa ligne. Les montants de l'OFGL sont arrondis à l'euro, ceux de la DGCL au centime : chacun prend la précision de sa ligne, ou de sa colonne, celle de sa valeur la plus précise.
- **Impôts.** Un impôt du tableau 3.217 de l'Insee est un concept de la norme `INSEE_PO` (par exemple `INSEE_PO.CSG`), dont la fiche dit dans quelle catégorie du SEC 2010 l'Insee le range ; les catégories elles-mêmes sont des concepts du SEC 2010 (`SEC2010.D211REC` pour la TVA). Le périmètre de ce tableau est l'ensemble des bénéficiaires des prélèvements obligatoires, `S13_S212` : les administrations publiques et les institutions de l'Union européenne. Une ligne qui ne vise qu'un bénéficiaire porte le sien : `S212` pour les droits de douane versés à l'Union, `S13131` pour les droits de mutation des collectivités locales.
- **Budget de l'État.** Les chiffres du budget relèvent de la norme `LOLF` et du périmètre `ETAT_LF`. Les missions et les programmes sont des fonctions de cette norme, sous un identifiant formé de leur libellé : `LOLF.DEFENSE` pour la mission Défense, `LOLF.DEFENSE.EQUIPEMENT_DES_FORCES` pour l'un de ses programmes. Une mission ou un programme renommé change donc d'identifiant : en 2025, la mission « Travail et emploi » devient « Travail, emploi et administration des ministères sociaux ». Pour chaque année, le texte retenu est le dernier texte complet que le Sénat a reçu ; la fiche de sa source dit s'il est devenu loi ou s'il a été rejeté, ce qui ne change rien aux montants exécutés qu'il arrête. Les lignes propres à une année, comme la régularisation des pensions en 2006 ou la cession de titres EDF en 2007, ont leurs propres concepts. Les règles de lecture des pages du Sénat (cases fusionnées, missions en gras, coupures de mots, en-têtes répétés, deux libellés fautifs) sont écrites en tête de `outils/importer_lois_resultats.py` ; ce qui en sort est vérifié par les identités du budget et les ventilations par mission du rapport de cohérence. En 2023, le tableau des autorisations d'engagement de l'article 4 annonce des millions d'euros, dans la page comme dans le texte imprimé, pour des montants en euros (ils ont des centimes) : ils sont enregistrés en euros, avec une note qui l'explique. La situation mensuelle budgétaire présente le budget général autrement que la loi : les prélèvements sur recettes y sont comptés en dépenses. Ses concepts sont donc distincts, et des passerelles du rapport de cohérence vérifient chaque année le raccord.
- **Budgets annexes et comptes spéciaux.** Chaque budget annexe et chaque compte spécial est une fonction de la norme `LOLF`, comme une mission, et ses programmes, quand il en a, des fonctions sous la sienne : `LOLF.CONTROLE_ET_EXPLOITATION_AERIENS` pour un budget annexe, `LOLF.CONTROLE_ET_EXPLOITATION_AERIENS.NAVIGATION_AERIENNE` pour l'un de ses programmes. Le concept dit la catégorie du compte et la grandeur : `LOLF.CAS_DEPENSES` pour les dépenses d'un compte d'affectation spéciale, de l'un de ses programmes ou de toute la catégorie ; `LOLF.CCF_SOLDES_DEBITEURS` pour les soldes débiteurs au 31 décembre des comptes de concours financiers ; `LOLF.CS_A_CREDITS_…` (comptes d'affectation spéciale et de concours financiers) et `LOLF.CS_A_DECOUVERT_…` (comptes de commerce et d'opérations monétaires) pour les regroupements que présentent certains textes. L'article 1er présente chaque budget annexe hors fonds de concours, puis leurs fonds de concours et leur total ; l'article 5 compte chaque budget annexe fonds de concours compris, sauf dans le texte de 2006. Un compte spécial clos dans l'année est arrêté par un article à part : ses chiffres prennent les concepts de sa catégorie ; les totaux de cet article ont leurs propres concepts (`…_COMPTES_CLOS`), comme ceux de l'article 6 de la même année, qui ne portent que sur les comptes qui se poursuivent (`…_HORS_COMPTES_CLOS`). Le rapport de cohérence ne peut pas rapprocher ces totaux de leurs comptes, qui gardent le concept de leur catégorie : l'import vérifie que chacun égale la somme des comptes qu'il couvre. En 2022, l'article 6 présente sous l'intitulé des annulations de crédits les majorations de découvert des comptes de commerce et d'opérations monétaires, qui n'ont pas de crédits : ces chiffres sont enregistrés comme des majorations de découvert, avec une note qui l'explique.
- **Tableau de financement.** L'article 2 arrête les ressources et les charges de trésorerie de l'État : son besoin de financement (amortissement de la dette, déficit à financer) et les ressources qui le couvrent (émissions de dette, variation des titres à court terme et des dépôts des correspondants). Ses lignes relèvent de la norme `LOLF` et du périmètre `ETAT_LF`, en milliards d'euros ; une ligne « dont » est une partie de la ligne qui la précède. Seule la colonne de l'exécution est lue : celle de la loi de finances de l'année, que présentent aussi les textes de 2006 et 2007, est une prévision.
- **Comptes de l'État.** Le compte de résultat et le bilan de l'article 3 relèvent de la comptabilité générale de l'État, en droits constatés (norme `COMPTES_ETAT`, périmètre `ETAT_CGE`), en millions d'euros. Une ligne de l'actif a trois concepts : le montant net (`COMPTES_ETAT.IMMOBILISATIONS_CORPORELLES`), le brut (`…_BRUT`) et les amortissements et dépréciations (`…_AMORTISSEMENTS`). Le bilan au 1er janvier d'une année est enregistré comme celui de la fin de la précédente : le bilan d'ouverture au 1er janvier 2006 a la période 2005. Le texte des comptes de 2006 présente aussi ce bilan d'ouverture, celui de 2007 ce bilan et les comptes de 2006 : ces chiffres gardent la version de leur texte, et le rapport de cohérence compare ceux qui figurent dans les deux.
- **Article liminaire.** Depuis les comptes de 2012, l'article liminaire présente les soldes de l'ensemble des administrations publiques (périmètre `S13`) : le solde effectif, qui est le déficit au sens de Maastricht (`SEC2010.B9`, en % du PIB), et ses composantes, le solde structurel, le solde conjoncturel et les mesures ponctuelles et temporaires (norme `PFP`). Depuis les comptes de 2023, il donne aussi la dette au sens de Maastricht, le taux de prélèvements obligatoires et la dépense publique hors crédits d'impôt (traitement `hors_credits_impot`). Ces chiffres sont ceux des comptes nationaux de l'année, encore provisoires à la date du texte : ils ont pu être révisés depuis, et le rapport de cohérence montre l'écart avec ceux que l'Insee publie aujourd'hui. Les soldes structurel et conjoncturel sont des estimations, qui dépendent du PIB potentiel retenu ; quand un texte les mesure de deux façons, la seconde porte un traitement qui la nomme (`metrique_lpfp_2012_2017` en 2014, `croissance_potentielle_lpfp_2014_2019` en 2016). Les colonnes de prévision et d'écart ne sont pas enregistrées : ces prévisions ont pour source les lois de finances et de programmation qui les ont votées.
- **Sécurité sociale.** Les tableaux d'équilibre des lois de financement relèvent de la comptabilité des organismes de sécurité sociale (norme `COMPTES_SECU`) : recettes (`COMPTES_SECU.RECETTES`), dépenses (`COMPTES_SECU.DEPENSES`) et solde, qui est leur résultat comptable (`COMPTES_SECU.RESULTAT_COMPTABLE`), en milliards d'euros. Les branches sont des fonctions de cette norme (`COMPTES_SECU.MALADIE`, `COMPTES_SECU.AT_MP`, `COMPTES_SECU.VIEILLESSE`, `COMPTES_SECU.FAMILLE`, `COMPTES_SECU.AUTONOMIE`) ; la ligne « toutes branches » est l'ensemble, sans fonction. Les recettes et les dépenses d'une branche comprennent les transferts qu'elle reçoit des autres branches ou leur verse (`non_consolide`) ; celles de l'ensemble les excluent (`consolide`) : seul le solde de l'ensemble égale la somme de ceux des branches. Les périmètres sont l'ensemble des régimes obligatoires de base (`ROBSS`), le régime général sans le Fonds de solidarité vieillesse (`REGIME_GENERAL_HORS_FSV`), et les organismes qui concourent au financement des régimes (`FSV`, `FFIPSA`, `CNSA`) ; depuis les comptes de 2015, les tableaux ajoutent l'ensemble FSV compris : `ROBSS_FSV`, et pour le régime général `REGIME_GENERAL`, le périmètre du tableau 3.108 de l'Insee. Les montants que l'article énonce dans son texte relèvent de la norme `LFSS` : dépenses constatées dans le champ de l'ONDAM (`LFSS.ONDAM_CONSTATE`, périmètre `ROBSS`), recettes affectées au Fonds de réserve pour les retraites (`LFSS.FRR_RECETTES_AFFECTEES`, `FRR`), recettes mises en réserve par le FSV (`LFSS.FSV_RECETTES_MISES_EN_RESERVE`, `FSV`), dette amortie par la CADES (`LFSS.CADES_DETTE_AMORTIE`, `CADES`). Leur emplacement est la phrase même qui les énonce (`phrase=…`), que le contrôle de la base retrouve dans la copie archivée ; des recettes « nulles » valent zéro. Pour chaque exercice, le texte retenu est celui dont les articles qui approuvent les comptes sont devenus ceux de la loi : le texte que le Sénat a reçu en première lecture, quand ces articles n'ont pas changé ensuite, ce que la fiche de chaque source établit ; pour 2004, le texte définitif, le Sénat ayant modifié l'ONDAM constaté ; pour 2021, le texte du Sénat, qui a rétabli ces articles, supprimés par l'Assemblée nationale, avec d'autres montants que le projet du Gouvernement. Les comptes de 2022 à 2024 n'ont pas été approuvés : les deux assemblées ont rejeté chaque projet de loi d'approbation ; celui des comptes de 2025, rejeté par l'Assemblée nationale, a été adopté par le Sénat. Leurs montants sont ceux du projet du Gouvernement. L'article liminaire de ces projets donne les recettes, les dépenses et le solde des administrations de sécurité sociale (`S1314`) au sens de la comptabilité nationale, en % du PIB, provisoires à la date du texte. Les tableaux de prévision des lois de financement (année en cours, année à venir) ne sont pas enregistrés.
- **Situation patrimoniale de la sécurité sociale.** Depuis les comptes de 2010, l'annexe A des lois de financement, puis l'annexe des projets de loi d'approbation, présente le bilan des régimes obligatoires de base, du FSV, de la CADES et du FRR (périmètre `SECU_LFSS`) au 31 décembre de l'exercice et de l'exercice précédent, en milliards d'euros ; chaque ligne prend la période de sa colonne, et les colonnes de variation ne sont pas lues. Les agrégats et les postes ont leurs concepts (`COMPTES_SECU.TOTAL_ACTIF`, `COMPTES_SECU.ACTIF_FINANCIER`, `COMPTES_SECU.DETTES_REPRESENTEES_PAR_UN_TITRE`, `COMPTES_SECU.FONDS_PROPRES`…) ; sous un poste, la ligne d'une entité prend le concept du poste et le périmètre de l'entité : `REGIME_GENERAL_HORS_FSV`, `AUTRES_REGIMES_BASE`, `FSV`, `CADES`, `FRR`, `ACOSS` (et `ROBSS` pour la ligne « Régime général / autres régimes » de 2012). Pour certains postes financiers, l'Acoss a sa propre ligne : celle du régime général n'en comprend alors pas le montant, et une note le dit. Le résultat de l'exercice inscrit au bilan a son concept (`COMPTES_SECU.RESULTAT_EXERCICE_BILAN`), distinct du solde des tableaux d'équilibre, auquel le rapport de cohérence le compare. Depuis les comptes de 2013, un tableau retrace depuis 2009 le passif net (`COMPTES_SECU.PASSIF_NET`, les fonds propres négatifs), l'endettement financier net (`COMPTES_SECU.ENDETTEMENT_FINANCIER_NET`) et le résultat comptable de l'ensemble ; ses lignes de variation ne sont pas lues. Deux tableaux n'indiquent pas leur unité, la situation patrimoniale de 2022 et le tableau d'évolution de 2013 : l'import ne les lit en milliards d'euros que parce que le texte de l'annexe donne ainsi leur passif net ou leur endettement de l'année, et une note le dit. La note du texte de 2011 sur les données de 2010, retraitées, accompagne ces chiffres. Le rapport de cohérence vérifie que l'actif égale le passif, que chaque agrégat égale la somme de ses postes et chaque poste celle de ses lignes par entité, et compare chaque année les chiffres qu'un texte reprend du précédent.
- **Collectivités locales.** L'annexe 2A des rapports de l'OFGL présente les comptes de gestion des budgets principaux, en opérations réelles et hors gestion active de la dette, selon les agrégats que la DGCL définit compte par compte (norme `COMPTES_LOCAUX` : `COMPTES_LOCAUX.DEP_FONCTIONNEMENT`, `COMPTES_LOCAUX.IMPOTS_LOCAUX`, `COMPTES_LOCAUX.EPARGNE_BRUTE`, `COMPTES_LOCAUX.DETTE`…), en milliards d'euros. Chaque niveau est un périmètre : `COMMUNES_BP`, `GFP_BP` (groupements de communes à fiscalité propre), `SECTEUR_COMMUNAL_BP`, `DEPARTEMENTS_BP`, `REGIONS_CTU_BP`, `SYNDICATS_BP`, et leurs ensembles, `COLLECTIVITES_TERRITORIALES_GFP_BP` sans les syndicats et `COLLECTIVITES_LOCALES_BP` avec eux ; le tableau des types de groupements, en millions d'euros, a les siens (`GFP_METROPOLES_BP`, `GFP_CU_BP`, `GFP_CA_BP`, `GFP_CC_BP`). La fiche de chaque périmètre dit qui il couvre : la Ville de Paris est comptée avec les communes depuis 2019, les collectivités territoriales uniques de Guyane, de Martinique et de Corse avec les régions, la métropole de Lyon avec les groupements. Les montants ne sont pas consolidés entre niveaux (`non_consolide`), sauf les reversements de fiscalité : ce qu'un groupement reverse à ses communes est une recette des communes et une moindre recette du groupement. Les lignes « dont » (fraction de TVA, droits de mutation, fiscalité reversée…) sont des parties de la ligne qu'elles suivent. Les taux d'évolution et les ratios, que la source calcule à partir des montants, ne sont pas enregistrés. Chaque rapport reprend les années précédentes, parfois révisées : un montant garde la version du rapport où il paraît pour la première fois avec sa valeur, et les éditions s'importent donc dans l'ordre de leur parution. Les annexes 2B, 2C et 2D des mêmes rapports donnent les mêmes agrégats pour les budgets annexes de chaque niveau (`COMMUNES_BA`, `GFP_BA`… `COLLECTIVITES_LOCALES_BA`), non consolidés entre niveaux ; pour les budgets principaux et annexes de chaque niveau, consolidés des flux croisés entre eux (`COMMUNES_BP_BA`, `GFP_BP_BA`, `DEPARTEMENTS_BP_BA`, `REGIONS_CTU_BP_BA`, `SYNDICATS_BP_BA`) ; pour le bloc communal et l'ensemble des collectivités locales, consolidés aussi entre niveaux (`SECTEUR_COMMUNAL_BP_BA`, `COLLECTIVITES_LOCALES_BP_BA`). Ce dernier est le périmètre le plus large des comptes locaux : toutes les collectivités et tous leurs budgets, y compris les établissements publics sociaux et médico-sociaux (EPSM, nomenclature M22), sans double compte. Les dépenses et les recettes des comptes consolidés le sont (`consolide`) ; leur dette et leur trésorerie restent la somme de celles des budgets (`non_consolide`). La feuille « Poids des budgets annexes » de l'annexe 2B donne, pour la dernière année de chaque rapport, le nombre de budgets principaux et annexes de chaque niveau (`COMPTES_LOCAUX.NOMBRE_BUDGETS`, unité `NOMBRE`) et leurs principales dépenses, provisoires comme les autres montants de cette année ; elle n'indique pas l'unité de ses montants, des milliards d'euros comme le montrent ceux des budgets annexes, identiques à ceux des tableaux, que l'import vérifie sans les enregistrer une seconde fois : une note le dit. Dans l'édition de 2021 de l'annexe 2C, l'en-tête de la colonne des valeurs provisoires du tableau des syndicats porte « 2019 », comme la colonne qui la précède : ses montants, ceux de 2020 selon les autres tableaux de l'édition et l'édition suivante, sont enregistrés pour 2020, avec une note. Le tableau régionalisé de l'annexe 2D, en montants par habitant et en ratios, n'est pas lu. Les publications annuelles de la DGCL donnent les mêmes agrégats pour chaque collectivité, en millions d'euros au centime : chacune est un périmètre (`DEP_01_BP` pour l'Ain, `REG_84_BP` pour Auvergne-Rhône-Alpes, `VILLE_DE_PARIS_BP`, `METROPOLE_LYON_BP`, `CEA_BP` pour la Collectivité européenne d'Alsace, `COLLECTIVITE_DE_CORSE_BP`, `CTU_MARTINIQUE_BP`, `CTU_GUYANE_BP`), rangé sous les totaux de la publication (`DEPARTEMENTS_METROPOLE_BP`, `DEPARTEMENTS_OUTRE_MER_BP`, `DEPARTEMENTS_BP`, `DEPARTEMENTS_CTU_BP`, `REGIONS_BP`…). Les collectivités de Corse, de Guyane et de Martinique figurent dans les deux publications, sous le même périmètre. La DGCL ajoute les intérêts et l'annuité de la dette, et les soldes de gestion (`COMPTES_LOCAUX.DEPENSES_GESTION`, `COMPTES_LOCAUX.EPARGNE_GESTION`) ; les montants que ses soldes de gestion reprennent d'autres tableaux ne sont lus qu'une fois. Ses tableaux des prélèvements et reversements de fiscalité, des dépenses par fonction et des données de contexte ne sont pas encore lus. Dans les classeurs des régions de 2022 à 2024, la colonne de la dette porte l'intitulé de l'année précédente : ses montants, qui sont ceux de l'année du classeur selon la ligne des années et l'annexe 2A de l'OFGL, sont enregistrés pour celle-ci, avec une note.
- **Passages entre comptabilités.** Le résultat d'exécution des lois de finances relève de la comptabilité budgétaire de l'État (norme `LOLF`, périmètre `ETAT_LF`, le champ des lois de finances) ; le résultat comptable du régime général, de celle des organismes de sécurité sociale (norme `COMPTES_SECU`, périmètre `REGIME_GENERAL`). Les corrections qui mènent de ces soldes au déficit au sens de Maastricht sont des concepts de la norme `INSEE_PASSAGES`, rangés dans la rubrique de l'Insee où elles figurent.
- **Unités.** Avant 1999, les montants en francs sont convertis en euros au taux fixe de 6,55957 francs pour un euro (unités `EUR`, `MIO_EUR`, `MD_EUR`) : c'est la convention de l'Insee, et celle d'Eurostat pour ses montants en monnaie nationale. Eurostat publie aussi des montants convertis en écus au taux de change de chaque année (unité `MIO_ECU_EUR`). Les deux séries se confondent à partir de 1999 ; avant, elles ne se comparent pas.

## Les règles d'enregistrement

1. On ajoute, on n'efface jamais : une nouvelle version d'un chiffre est une nouvelle ligne. Un chiffre qu'une nouvelle version de la source reprend à l'identique n'est pas enregistré une seconde fois : il garde sa version d'origine. Importer de nouveau un fichier n'ajoute rien. Un import qui trouverait, pour un même identifiant, une valeur différente de celle déjà enregistrée s'arrête.
2. Un chiffre publié par une source renvoie à une copie archivée ; un chiffre cité renvoie à l'endroit exact chez celui qui le cite ; un chiffre calculé renvoie à sa recette dans `calculs.csv`.
3. Une erreur d'enregistrement se corrige dans la ligne et s'inscrit dans `corrections.csv`, avec sa date et sa raison.
4. Rien n'entre dans la base sans passer le contrôle `python3 outils/valider.py`. Il vérifie les schémas, les références, la concordance de chaque identifiant avec sa fiche et l'intégrité des copies archivées. Il relit aussi chaque chiffre publié dans sa copie archivée et refuse toute valeur différente.
5. Un importateur ne laisse rien de côté en silence : une ligne, un code ou un texte de la source sans correspondance dans la base arrête l'import. Seules les cellules vides ou marquées non disponibles (« nd », « N.D. ») ne deviennent pas des chiffres, et l'import dit combien il en a rencontré.

Ces règles appliquent la [charte d'indépendance](../CHARTE.md).

## Ajouter des chiffres

D'une statistique officielle :

```sh
# 1. déclarer la source dans base/tables/sources.csv
python3 outils/archiver.py <source_id> "<url>"     # archive le fichier et l'inscrit dans fichiers.csv
python3 outils/importer_insee.py <fichier_id>      # tableaux des comptes nationaux de l'Insee (classeurs xlsx)
python3 outils/importer_eurostat.py <fichier_id>   # jeux de données d'Eurostat (JSON-stat)
python3 outils/importer_insee_bdm.py <fichier_id>  # séries de la Banque de données macro-économiques de l'Insee (SDMX)
python3 outils/importer_lois_resultats.py <fichier_id>  # lois d'approbation des comptes de l'État (texte du Sénat)
python3 outils/importer_lois_secu.py <fichier_id>  # lois de financement et d'approbation des comptes de la sécurité sociale
python3 outils/importer_ofgl.py <fichier_id>       # annexes 2A à 2D des rapports de l'OFGL (collectivités locales), dans l'ordre des éditions
python3 outils/importer_dgcl.py <fichier_id>       # comptes de chaque département et de chaque région publiés par la DGCL
python3 outils/valider.py
python3 outils/controler_coherence.py              # met à jour le rapport de cohérence
```

Quand l'Insee ou Eurostat publie une nouvelle version, on archive le nouveau fichier et on l'importe : seuls les chiffres qui changent s'ajoutent, sous la nouvelle version.

Cité par un tiers : déclarer la source, puis ajouter la ligne dans `tables/chiffres/tiers.csv` avec l'endroit exact où figure le chiffre, et lancer le contrôle. Le contrôle refuse un identifiant qui ne correspond pas à la fiche.

## Contrôler la cohérence des sources

```sh
python3 outils/controler_coherence.py   # écrit controles/coherence.md
```

Le [rapport de cohérence](../controles/coherence.md) vérifie ce que disent les sources elles-mêmes :

- les sommes comptables : un total contre la somme de ses composantes ;
- les ventilations par fonction : l'ensemble contre la somme des fonctions, chaque fonction contre celle de ses groupes ; pour les branches de la sécurité sociale, le solde seulement ;
- l'additivité des sous-secteurs, pour les soldes, les prélèvements obligatoires et les parts de la dépense consolidée de l'ensemble, celle des lignes par entité de la situation patrimoniale de la sécurité sociale, celle des niveaux de collectivités locales, pour tous les montants de leurs budgets principaux et de leurs budgets annexes et pour leurs nombres de budgets, et celle des départements et des régions dans les totaux de la DGCL ;
- les passerelles entre tableaux qui présentent autrement les mêmes grandeurs, comme les impôts du tableau 3.217 et les recettes du compte des administrations publiques (tableau 3.201), ou ce que la consolidation des comptes locaux laisse inchangé : la variation du fonds de roulement, l'épargne brute, la dette et la trésorerie d'un niveau consolidé contre la somme de celles de ses budgets principaux et annexes, et celles du bloc communal et de l'ensemble des collectivités contre la somme de leurs niveaux ;
- les ratios, recalculés à partir de leur dénominateur ;
- les écarts entre sources pour une même grandeur, en distinguant ceux qui touchent un chiffre encore révisable (provisoire, semi-définitif, estimé ou prévu).

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : une demi-unité de la dernière décimale de chaque valeur, une unité entière pour l'OFGL, qui arrondit ou tronque selon les cas ses montants à l'euro ; un nombre de budgets, qui n'est pas arrondi, doit être exact. Quand une source ne diffuse pas toutes les parties d'une somme, le rapport le dit et vérifie si les parties diffusées suffisent à retrouver le total. Une incohérence signalée est un constat sur la source : elle est publiée telle quelle, jamais corrigée dans la base. Le contrôle sur GitHub refuse une modification de la base dont le rapport n'a pas été mis à jour.

## Interroger la base

```sh
python3 outils/construire.py   # écrit base/construite/comptes.sqlite et base/construite/empreintes.csv
```

La base SQLite s'ouvre avec n'importe quel outil SQLite (par exemple DB Browser for SQLite). Elle contient une table par fichier de `tables/`, toutes les familles de chiffres étant réunies dans `chiffres`, et deux vues :

- `v_chiffres` : les chiffres avec les libellés de leurs concepts, périmètres, fonctions, unités et sources ;
- `v_dernieres_versions` : pour chaque chiffre, sa version la plus récente chez la même source.

Par exemple, la dépense totale de 2025 selon chaque source enregistrée :

```sql
SELECT source_id, unite_id, valeur, statut, version
FROM v_dernieres_versions
WHERE zone = 'FR' AND perimetre_id = 'S13' AND concept_id = 'SEC2010.TE'
  AND fonction_id IS NULL AND traitements IS NULL AND periode = '2025';
```

Ou la dépense publique de 2024 par grande fonction, selon le tableau 3.301 de l'Insee :

```sql
SELECT f.libelle, v.valeur
FROM v_dernieres_versions v JOIN fonctions f ON f.id = v.fonction_id
WHERE v.source_id = 'insee.t3301' AND v.concept_id = 'SEC2010.TE' AND v.periode = '2024'
  AND f.parent_id IS NULL
ORDER BY v.valeur DESC;
```

Ou les dépenses de l'État en 2025 par mission, en milliards d'euros :

```sql
SELECT f.libelle, round(v.valeur / 1e9, 1) AS milliards
FROM v_dernieres_versions v JOIN fonctions f ON f.id = v.fonction_id
WHERE v.concept_id = 'LOLF.BG_DEPENSES_BRUTES' AND v.periode = '2025' AND f.parent_id IS NULL
ORDER BY v.valeur DESC;
```

Ou le solde de chaque branche du régime général, chaque année, en milliards d'euros :

```sql
SELECT v.periode, f.libelle, v.valeur
FROM v_dernieres_versions v JOIN fonctions f ON f.id = v.fonction_id
WHERE v.perimetre_id = 'REGIME_GENERAL_HORS_FSV' AND v.concept_id = 'COMPTES_SECU.RESULTAT_COMPTABLE'
ORDER BY v.periode, f.libelle;
```

Ou l'épargne brute de chaque niveau de collectivités locales, chaque année, en milliards d'euros :

```sql
SELECT v.periode, p.libelle, round(v.valeur, 2) AS milliards, v.statut
FROM v_dernieres_versions v JOIN perimetres p ON p.id = v.perimetre_id
WHERE v.source_id = 'ofgl.annexe-2a' AND v.concept_id = 'COMPTES_LOCAUX.EPARGNE_BRUTE' AND v.unite_id = 'MD_EUR'
ORDER BY v.periode, p.libelle;
```

Ou les comptes de l'ensemble des collectivités locales, tous budgets compris et consolidés, chaque année, en milliards d'euros :

```sql
SELECT v.periode, c.libelle, round(v.valeur, 2) AS milliards, v.statut
FROM v_dernieres_versions v JOIN concepts c ON c.id = v.concept_id
WHERE v.perimetre_id = 'COLLECTIVITES_LOCALES_BP_BA'
  AND v.concept_id IN ('COMPTES_LOCAUX.REC_TOTALES', 'COMPTES_LOCAUX.DEP_TOTALES', 'COMPTES_LOCAUX.DETTE')
ORDER BY v.periode, c.libelle;
```

Ou la dette de chaque département au 31 décembre 2024, en millions d'euros :

```sql
SELECT p.libelle, round(v.valeur, 1) AS millions
FROM v_dernieres_versions v JOIN perimetres p ON p.id = v.perimetre_id
WHERE v.source_id = 'dgcl.finances-departements' AND v.concept_id = 'COMPTES_LOCAUX.DETTE' AND v.periode = '2024'
  AND p.parent_id IN ('DEPARTEMENTS_METROPOLE_BP', 'DEPARTEMENTS_OUTRE_MER_BP')
ORDER BY v.valeur DESC;
```

Ou ce qu'a rapporté la CSG chaque année, en milliards d'euros :

```sql
SELECT periode, valeur, statut FROM v_dernieres_versions
WHERE concept_id = 'INSEE_PO.CSG' AND unite_id = 'MD_EUR' ORDER BY periode;
```

Le fichier `empreintes.csv` donne une empreinte du contenu de chaque table : une base reconstruite par n'importe qui à partir de la même version du dépôt doit donner les mêmes empreintes.
