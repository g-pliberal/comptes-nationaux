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
| Projets de loi d'approbation des comptes de l'État (de règlement jusqu'aux comptes de 2022, relatifs aux résultats de la gestion depuis), textes publiés par le Sénat | budget de l'État exécuté, à l'euro près : résultat budgétaire ; recettes et dépenses du budget général, des budgets annexes et des comptes spéciaux ; autorisations d'engagement consommées et dépenses par mission et par programme | 2006-2025, depuis le premier budget voté selon la loi organique relative aux lois de finances (LOLF) |
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
| `tables/fonctions.csv` | fonctions de la dépense (COFOG) |
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
| `fonction_id` | la fonction de la dépense : COFOG, ou mission et programme du budget de l'État ; vide pour l'ensemble |
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

- **Version.** Pour Eurostat, la date de mise à jour du jeu de données. Pour l'Insee, la date de dernière modification que le classeur porte en lui-même, à défaut sa date de création ; pour une série de sa Banque de données macro-économiques, la date de dernière mise à jour de la série. Pour un texte publié par le Sénat, la date qu'il porte : enregistrement, transmission ou adoption.
- **Statut.** Eurostat le donne par un indicateur attaché à chaque valeur, conservé dans `drapeau_source`. L'Insee le donne par le calendrier de ses comptes annuels : la dernière année publiée est provisoire, l'avant-dernière semi-définitive, les précédentes définitives.
- **Décimales.** Le nombre de décimales de la valeur enregistrée dans le fichier source, sans les zéros finaux, que le fichier ne conserve pas. Une valeur nulle est exacte : elle prend la précision de sa ligne.
- **Impôts.** Un impôt du tableau 3.217 de l'Insee est un concept de la norme `INSEE_PO` (par exemple `INSEE_PO.CSG`), dont la fiche dit dans quelle catégorie du SEC 2010 l'Insee le range ; les catégories elles-mêmes sont des concepts du SEC 2010 (`SEC2010.D211REC` pour la TVA). Le périmètre de ce tableau est l'ensemble des bénéficiaires des prélèvements obligatoires, `S13_S212` : les administrations publiques et les institutions de l'Union européenne. Une ligne qui ne vise qu'un bénéficiaire porte le sien : `S212` pour les droits de douane versés à l'Union, `S13131` pour les droits de mutation des collectivités locales.
- **Budget de l'État.** Les chiffres du budget relèvent de la norme `LOLF` et du périmètre `ETAT_LF`. Les missions et les programmes sont des fonctions de cette norme, sous un identifiant formé de leur libellé : `LOLF.DEFENSE` pour la mission Défense, `LOLF.DEFENSE.EQUIPEMENT_DES_FORCES` pour l'un de ses programmes. Une mission ou un programme renommé change donc d'identifiant : en 2025, la mission « Travail et emploi » devient « Travail, emploi et administration des ministères sociaux ». Pour chaque année, le texte retenu est le dernier texte complet que le Sénat a reçu ; la fiche de sa source dit s'il est devenu loi ou s'il a été rejeté, ce qui ne change rien aux montants exécutés qu'il arrête. Les lignes propres à une année, comme la régularisation des pensions en 2006 ou la cession de titres EDF en 2007, ont leurs propres concepts. Les règles de lecture des pages du Sénat (cases fusionnées, missions en gras, coupures de mots, en-têtes répétés, deux libellés fautifs) sont écrites en tête de `outils/importer_lois_resultats.py` ; ce qui en sort est vérifié par les identités du budget et les ventilations par mission du rapport de cohérence. La situation mensuelle budgétaire présente le budget général autrement que la loi : les prélèvements sur recettes y sont comptés en dépenses. Ses concepts sont donc distincts, et des passerelles du rapport de cohérence vérifient chaque année le raccord.
- **Passages entre comptabilités.** Le résultat d'exécution des lois de finances relève de la comptabilité budgétaire de l'État (norme `LOLF`, périmètre `ETAT_LF`, le champ des lois de finances) ; le résultat comptable du régime général, de celle des organismes de sécurité sociale (norme `COMPTES_SECU`, périmètre `REGIME_GENERAL`). Les corrections qui mènent de ces soldes au déficit au sens de Maastricht sont des concepts de la norme `INSEE_PASSAGES`, rangés dans la rubrique de l'Insee où elles figurent.
- **Unités.** Avant 1999, les montants en francs sont convertis en euros au taux fixe de 6,55957 francs pour un euro (unités `EUR`, `MIO_EUR`, `MD_EUR`) : c'est la convention de l'Insee, et celle d'Eurostat pour ses montants en monnaie nationale. Eurostat publie aussi des montants convertis en écus au taux de change de chaque année (unité `MIO_ECU_EUR`). Les deux séries se confondent à partir de 1999 ; avant, elles ne se comparent pas.

## Les règles d'enregistrement

1. On ajoute, on n'efface jamais : une nouvelle version d'un chiffre est une nouvelle ligne. Un chiffre qu'une nouvelle version de la source reprend à l'identique n'est pas enregistré une seconde fois : il garde sa version d'origine. Un import qui trouverait, pour un même identifiant, une valeur différente de celle déjà enregistrée s'arrête.
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
- les ventilations par fonction : l'ensemble contre la somme des fonctions, chaque fonction contre celle de ses groupes ;
- l'additivité des sous-secteurs, pour les soldes, les prélèvements obligatoires et les parts de la dépense consolidée de l'ensemble ;
- les passerelles entre tableaux qui présentent autrement les mêmes grandeurs, comme les impôts du tableau 3.217 et les recettes du compte des administrations publiques (tableau 3.201) ;
- les ratios, recalculés à partir de leur dénominateur ;
- les écarts entre sources pour une même grandeur, en distinguant ceux qui touchent un chiffre encore révisable (provisoire, semi-définitif, estimé ou prévu).

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication. Quand une source ne diffuse pas toutes les parties d'une somme, le rapport le dit et vérifie si les parties diffusées suffisent à retrouver le total. Une incohérence signalée est un constat sur la source : elle est publiée telle quelle, jamais corrigée dans la base. Le contrôle sur GitHub refuse une modification de la base dont le rapport n'a pas été mis à jour.

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

Ou ce qu'a rapporté la CSG chaque année, en milliards d'euros :

```sql
SELECT periode, valeur, statut FROM v_dernieres_versions
WHERE concept_id = 'INSEE_PO.CSG' AND unite_id = 'MD_EUR' ORDER BY periode;
```

Le fichier `empreintes.csv` donne une empreinte du contenu de chaque table : une base reconstruite par n'importe qui à partir de la même version du dépôt doit donner les mêmes empreintes.
