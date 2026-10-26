# Comptes publics de la France

Reconstituer de façon vérifiable les comptes de l'ensemble des administrations publiques françaises : recettes et dépenses, du total jusqu'au détail, sur le plus d'années possible.

Chaque chiffre est enregistré avec sa fiche d'identité et sa source, et chaque calcul se refait avec le code du dépôt. Les règles sont fixées par la [charte d'indépendance et d'exactitude](CHARTE.md). Les étapes à venir sont dans la [feuille de route](FEUILLE_DE_ROUTE.md).

## Contenu

| Dossier | Contenu |
|---|---|
| [base/](base/) | la base des chiffres : tables, schémas, copies archivées des sources ; pour l'instant, les comptes des administrations publiques de l'Insee et d'Eurostat, dont les dépenses par fonction, les recettes impôt par impôt, les comptes complets de l'ensemble et de chaque sous-secteur depuis 1949, de la production à la capacité de financement, la dette au sens de Maastricht par instrument, la dette nette, la dette à la fin de chaque trimestre, et le passage du budget de l'État et des comptes de la sécurité sociale au déficit au sens de Maastricht, puis du déficit à la variation de la dette ; le budget de l'État exécuté depuis 2006, par mission et par programme, et chacun de ses budgets annexes et comptes spéciaux, son tableau de financement, son compte de résultat et son bilan, tels que les arrêtent les lois d'approbation des comptes, et, depuis 2016, la balance de ses comptes, compte par compte, mission par mission et programme par programme, avec ses engagements hors bilan, d'après la DGFiP ; les comptes de la sécurité sociale depuis 2004, par branche, pour l'ensemble des régimes de base et le régime général, avec le Fonds de solidarité vieillesse, l'ONDAM, le Fonds de réserve pour les retraites et la CADES, tels que les approuvent les lois de financement, et depuis 2010 leur situation patrimoniale : bilan, fonds propres, dettes financières, entité par entité ; les comptes des collectivités locales depuis 2017, niveau par niveau (communes, intercommunalités, départements, régions, syndicats), budgets principaux, budgets annexes, et tous budgets consolidés jusqu'à l'ensemble des collectivités sans double compte, d'après les rapports de l'Observatoire des finances et de la gestion publique locales, et, d'après son portail de données, ceux de chaque commune, de chaque intercommunalité, de chaque syndicat et de chaque établissement public local depuis 2018, de chaque département et de chaque région depuis 2012, avec les dépenses de chaque département par fonction (action sociale, collèges, voirie, transports…), et, budget par budget, ceux de chaque service d'incendie et de secours depuis 2012 et de chaque centre d'action sociale depuis 2018 ; d'après les comptes individuels que publie la DGFiP, l'analyse des équilibres financiers et la fiscalité directe locale de chaque commune depuis 2000, de chaque intercommunalité depuis 2007, de chaque département et de chaque région depuis 2008 ; depuis 2020, ceux de chaque département et de chaque région aussi d'après la Direction générale des collectivités locales ; depuis 2018, la dotation globale de fonctionnement que l'État notifie à chaque commune, à chaque intercommunalité et à chaque département ; depuis 2012, les bases, taux et produits de toutes les impositions directes locales sur le territoire de chaque commune (taxes foncières, taxe d'habitation, cotisation foncière des entreprises, part de la CVAE, taxe d'enlèvement des ordures ménagères, taxe sur les surfaces commerciales, impositions forfaitaires sur les entreprises de réseaux), pour chacun de leurs destinataires, des communes à l'État en passant par les chambres consulaires, d'après le recensement de la DGFiP et sa version simplifiée par l'Observatoire ; enfin, ce que compte le secteur public, unité par unité : la liste des organismes divers d'administration centrale et le nombre de ceux d'administration locale, par catégorie, que l'Insee établit pour les comptes nationaux, et le nombre de collectivités territoriales et de groupements au 1er janvier, d'après la Direction générale des collectivités locales |
| [controles/](controles/) | le [rapport de cohérence](controles/coherence.md) des sources : sommes, ventilations, soldes, passerelles entre tableaux, ratios, écarts entre sources, comptes de chaque collectivité, flux entre administrations, dépenses des départements par fonction, fiscalité directe locale, recensement des éléments d'imposition, ce que la base couvre des organismes publics, comptes individuels de la DGFiP, et balances des comptes de l'État contre leurs états financiers |
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
