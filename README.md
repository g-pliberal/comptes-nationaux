# Comptes publics de la France

Reconstituer de façon vérifiable les comptes de l'ensemble des administrations publiques françaises : recettes et dépenses, du total jusqu'au détail, sur le plus d'années possible.

Chaque chiffre est enregistré avec sa fiche d'identité et sa source, et chaque calcul se refait avec le code du dépôt. Les règles sont fixées par la [charte d'indépendance et d'exactitude](CHARTE.md).

## Contenu

| Dossier | Contenu |
|---|---|
| [base/](base/) | la base des chiffres : tables, schémas, copies archivées des sources ; pour l'instant, les comptes des administrations publiques de l'Insee et d'Eurostat |
| [controles/](controles/) | le [rapport de cohérence](controles/coherence.md) des sources : sommes, soldes, ratios, écarts entre sources |
| [outils/](outils/) | archivage des sources, import, contrôle et construction de la base |
| [reports/](reports/), [research_notes/](research_notes/) | recherche documentaire de départ sur les sources des comptes publics |

## Vérifier

Python 3 suffit, sans aucune bibliothèque à installer.

```sh
python3 outils/valider.py              # contrôle les tables, les références et l'intégrité des copies archivées,
                                       # et relit chaque chiffre publié dans sa copie archivée
python3 outils/controler_coherence.py  # refait le rapport de cohérence des sources
python3 outils/construire.py           # construit la base SQLite interrogeable
```

Les mêmes contrôles tournent sur GitHub à chaque modification.

## Principes

- La norme de référence est le système européen des comptes (SEC 2010) ; les autres comptabilités (budget de l'État, comptes de la sécurité sociale, comptes des collectivités) s'y rattachent par des passerelles documentées.
- On ajoute, on n'efface jamais : les révisions des sources deviennent de nouvelles versions.
- Tout reste sur GitHub : les données, le code, l'historique et les contrôles.
