# Feuille de route

Les étapes prévues pour compléter la base, du plus large au plus petit, chacune publiée par une pull request.

| # | Étape | Ce qu'elle apporte | État |
|---|---|---|---|
| 1 | Tableaux de l'Insee pas encore lus : 3.102 à 3.105, 3.215, comptes complets 7.301 à 7.306, dette trimestrielle | le haut de la pyramide au complet | fait |
| 2 | Listes officielles des organismes publics | « tout le public » défini d'après les listes officielles, et ce que la base en couvre | fait, sauf les opérateurs de l'État : pas de liste exploitable après 2019 |
| 3 | Balances des comptes de l'État, 2016-2025 | les comptes de l'État compte par compte, mission par mission et programme par programme, recoupés avec son bilan et son compte de résultat | fait |
| 4 | Comptes individuels des collectivités que publie la DGFiP | les comptes de chaque commune depuis 2000, de chaque intercommunalité depuis 2007, de chaque département et de chaque région depuis 2008, recoupés avec ceux de l'OFGL | fait |
| 5 | Recensement des éléments d'imposition (REI) de 1982 à 2011 | trente ans de fiscalité locale, à l'époque de la taxe professionnelle | à faire ; volume à mesurer |
| 6 | Balances comptables des collectivités, 2010-2025 | chaque agrégat de l'OFGL recalculé à partir des comptes eux-mêmes | à faire ; plusieurs gigaoctets, stockage à décider |
| 7 | Montants du REI par collectivité et tableaux de la DGCL non lus | ce que l'État verse à chaque collectivité | à faire |
| 8 | Opérateurs de l'État, hôpitaux, sécurité sociale régime par régime | les comptes de chaque organisme sous les totaux de l'Insee : aucun des 701 organismes divers d'administration centrale n'a encore les siens dans la base | en cours : les prestations de chaque régime de protection sociale sont faites (DREES) ; les opérateurs de l'État restent à faire ; aucune source ouverte ne donne les comptes de chaque hôpital public : la DGFiP ne publie pas leurs balances, et Hospi Diag, sur data.gouv.fr, n'en donne que des ratios et n'est plus mis à jour depuis 2017 |
| 9 | Niches fiscales et sociales, engagements hors bilan, budgets votés | la dépense publique au sens large, et le budget voté face au budget exécuté | en cours : le budget voté est fait, crédits et recettes (ce qu'ouvre et évalue chaque loi de finances initiale de 2006 à 2026, par mission et par programme, ligne de recettes par ligne, avec les soldes de son article d'équilibre, face à l'exécution que constatent les lois d'approbation des comptes) ; restent le tableau de financement voté, le plafond des emplois, les niches fiscales et sociales et les engagements hors bilan, que les balances de l'État donnent déjà par grande catégorie |
| 10 | Base prête à télécharger, synthèse lisible, contrôles plus rapides, détection des nouvelles versions des sources | une base utilisable sans la reconstruire, et tenue à jour | à faire ; la base construite pèse plus de 6 gigaoctets, plus que les 2 gigaoctets d'un fichier des « Releases » de GitHub |
| 11 | Dette négociable de l'État | l'encours de la dette négociable de l'État, mois par mois, d'après l'Insee et l'Agence France Trésor, recoupé avec le tableau de financement, la balance et le bilan de l'État | fait |

Avant les étapes 5 et 6, il faut décider où ranger les plus gros fichiers. La proposition est de garder dans le dépôt la fiche et l'empreinte de chaque fichier, et de mettre les plus gros dans les « Releases » de GitHub : tout resterait sur GitHub.
