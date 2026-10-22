# La base des chiffres

Chaque chiffre est enregistré avec sa fiche d'identité complète : ce qui est mesuré, selon quelle norme, sur quel périmètre, dans quelle unité, pour quelle période, dans quelle version, et où il se trouve exactement dans sa source. Deux chiffres ne se comparent que si leurs fiches coïncident ; sinon, la fiche dit en quoi ils diffèrent.

La base est faite de tables en texte (CSV) décrites par des schémas, au format ouvert [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/). Chaque modification est visible dans l'historique du dépôt. Une base SQLite interrogeable se reconstruit à partir de ces tables à tout moment.

## Les tables

| Table | Contenu |
|---|---|
| `tables/chiffres/*.csv` | les chiffres, un par ligne, avec leur fiche d'identité ; un fichier par famille de sources |
| `tables/sources.csv` | producteurs et publications : statistiques officielles, documents publics, articles, communications |
| `tables/fichiers.csv` | copies archivées des fichiers sources : requête exacte, date, empreinte SHA-256 |
| `tables/concepts.csv` | ce qui est mesuré, défini dans une norme (par exemple la dépense totale au sens du SEC 2010) |
| `tables/normes.csv` | normes et méthodes de référence |
| `tables/perimetres.csv` | secteurs et sous-secteurs : administrations publiques, administration centrale, locale, sécurité sociale… |
| `tables/fonctions.csv` | fonctions de la dépense (COFOG) et leurs regroupements |
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
| `fonction_id` | la fonction COFOG, vide pour l'ensemble |
| `traitements` | les retraitements appliqués, vides s'il n'y en a pas |
| `unite_id`, `decimales` | l'unité et la précision publiées |
| `periode` | l'année, le trimestre ou le mois |
| `statut` | prévision, estimation, provisoire, semi-définitif, définitif, ou non précisé par la source |
| `version` | la date de publication de la version d'où vient le chiffre |
| `consolidation` | avec ou sans les flux entre administrations |
| `source_id`, `fichier_id`, `emplacement` | la source, la copie archivée et l'endroit exact |
| `nature` | `publie` par la source elle-même, `cite` par un tiers, ou `calcule` ici |

L'identifiant d'un chiffre est formé de ses composantes, séparées par « : » (« - » pour une composante vide). Il ne change jamais. Par exemple :

```
eurostat.gov_10a_main:FR:S13:SEC2010.TE:-:-:MIO_EUR:2025:2026-10-21
```

se lit : selon Eurostat, dépense totale au sens du SEC 2010 des administrations publiques françaises, ensemble des fonctions, sans retraitement, en millions d'euros, pour 2025, dans la version publiée le 21 octobre 2026.

## Les règles d'enregistrement

1. On ajoute, on n'efface jamais : une nouvelle version d'un chiffre est une nouvelle ligne.
2. Un chiffre publié par une source renvoie à une copie archivée ; un chiffre cité renvoie à l'endroit exact chez celui qui le cite ; un chiffre calculé renvoie à sa recette dans `calculs.csv`.
3. Une erreur d'enregistrement se corrige dans la ligne et s'inscrit dans `corrections.csv`, avec sa date et sa raison.
4. Rien n'entre dans la base sans passer le contrôle `python3 outils/valider.py`. Il vérifie les schémas, les références, la concordance de chaque identifiant avec sa fiche et l'intégrité des copies archivées. Il relit aussi chaque chiffre publié dans sa copie archivée et refuse toute valeur différente.

Ces règles appliquent la [charte d'indépendance](../CHARTE.md).

## Ajouter des chiffres

D'une statistique officielle :

```sh
# 1. déclarer la source dans base/tables/sources.csv
python3 outils/archiver.py <source_id> "<requête exacte>"   # archive le fichier et l'inscrit dans fichiers.csv
python3 outils/importer_eurostat.py <fichier_id>           # un importateur par producteur ; Eurostat pour l'instant
python3 outils/valider.py
```

Cité par un tiers : déclarer la source, puis ajouter la ligne dans `tables/chiffres/tiers.csv` avec l'endroit exact où figure le chiffre, et lancer le contrôle. Le contrôle refuse un identifiant qui ne correspond pas à la fiche.

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

Le fichier `empreintes.csv` donne une empreinte du contenu de chaque table : une base reconstruite par n'importe qui à partir de la même version du dépôt doit donner les mêmes empreintes.
