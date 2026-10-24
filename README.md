# Comptes publics de la France

Reconstituer de façon vérifiable les comptes de l'ensemble des administrations publiques françaises : recettes et dépenses, du total jusqu'au détail, sur le plus d'années possible.

Chaque chiffre est enregistré avec sa fiche d'identité et sa source, et chaque calcul se refait avec le code du dépôt. Les règles sont fixées par la [charte d'indépendance et d'exactitude](CHARTE.md).

## Contenu

| Dossier | Contenu |
|---|---|
| [base/](base/) | la base des chiffres : tables, schémas, copies archivées des sources ; pour l'instant, les comptes des administrations publiques de l'Insee et d'Eurostat, dont les dépenses par fonction, les recettes impôt par impôt et le passage du budget de l'État et des comptes de la sécurité sociale au déficit au sens de Maastricht ; le budget de l'État exécuté depuis 2006, par mission et par programme, et chacun de ses budgets annexes et comptes spéciaux, son tableau de financement, son compte de résultat et son bilan, tels que les arrêtent les lois d'approbation des comptes ; les comptes de la sécurité sociale depuis 2004, par branche, pour l'ensemble des régimes de base et le régime général, avec le Fonds de solidarité vieillesse, l'ONDAM, le Fonds de réserve pour les retraites et la CADES, tels que les approuvent les lois de financement, et depuis 2010 leur situation patrimoniale : bilan, fonds propres, dettes financières, entité par entité ; les comptes des collectivités locales depuis 2017, niveau par niveau (communes, intercommunalités, départements, régions, syndicats), budgets principaux, budgets annexes, et tous budgets consolidés jusqu'à l'ensemble des collectivités sans double compte, d'après les rapports de l'Observatoire des finances et de la gestion publique locales, et, d'après son portail de données, ceux de chaque commune, de chaque intercommunalité, de chaque syndicat et de chaque établissement public local depuis 2018, de chaque département et de chaque région depuis 2012, et, budget par budget, ceux de chaque service d'incendie et de secours depuis 2012 et de chaque centre d'action sociale depuis 2018 ; depuis 2020, ceux de chaque département et de chaque région aussi d'après la Direction générale des collectivités locales |
| [controles/](controles/) | le [rapport de cohérence](controles/coherence.md) des sources : sommes, ventilations, soldes, passerelles entre tableaux, ratios, écarts entre sources |
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
