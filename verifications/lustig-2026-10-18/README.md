# Vérification : « The French state crowded out by government spending »

Article de Hanno Lustig publié le 18 octobre 2026 sur The Two Cents :
<https://thetwocents.substack.com/p/the-french-state-crowded-out-by-government>

C'est le premier essai de la méthode du projet sur un chiffre extérieur : chaque chiffre vérifiable de l'article est recalculé à partir de sources publiques archivées, puis comparé à la valeur publiée. Le résultat est dans [resultats.md](resultats.md), généré par le script. Aucun chiffre n'y est saisi à la main.

## Contenu

| Fichier | Rôle |
|---|---|
| [verifier.py](verifier.py) | télécharge les sources, contrôle leurs empreintes, refait les calculs et écrit `resultats.md` |
| [sources/](sources/) | copies des données utilisées, telles que renvoyées par Eurostat et l'OCDE |
| [sources/manifeste.csv](sources/manifeste.csv) | pour chaque copie : requête exacte, date de téléchargement, empreinte SHA-256, taille |
| [resultats.md](resultats.md) | chaque chiffre de l'article, son recalcul, l'écart et le verdict |

## Refaire la vérification

Python 3 suffit, sans aucune bibliothèque à installer.

```sh
python3 verifier.py                # à partir des copies archivées, sans réseau
python3 verifier.py --telecharger  # avec les données les plus récentes
```

Sans option, le script refuse de calculer si une copie archivée a été modifiée : son empreinte ne correspondrait plus au manifeste. Avec `--telecharger`, les résultats peuvent changer si Eurostat ou l'OCDE ont révisé leurs données depuis.

## Sources

- Eurostat, dépenses des administrations publiques par fonction (`gov_10a_exp`, classification COFOG) : dépense totale, rémunération des agents et subventions, par sous-secteur.
- Eurostat, comptes des administrations publiques (`gov_10a_main`) : cotisations sociales reçues, rémunérations, intérêts, solde.
- Eurostat, PIB à prix courants (`nama_10_gdp`).
- OCDE, dépenses sociales publiques en % du PIB (base SOCX, jeu `DF_PUB_PRV`).

Ce sont les sources que l'article cite dans les notes de ses graphiques.

## Méthode

L'article retire de la dépense les cotisations retraite que l'État s'impute pour ses fonctionnaires, car les pensions versées sont déjà comptées dans la protection sociale. Le script refait ce retrait comme l'article le décrit :

1. cotisations imputées d'un sous-secteur = cotisations sociales reçues (D.61) − cotisations effectives des employeurs (D.611) − cotisations effectives des ménages (D.613) ;
2. rapport de ce montant à la rémunération des agents du sous-secteur (D.1) ;
3. retrait, dans chaque fonction, de ce rapport appliqué à la rémunération des agents de la fonction.

Le tableau 1 de l'article ne retire que les cotisations de l'État ; son graphique 2 les retire pour tous les sous-secteurs. Le script suit chaque fois le choix de l'article.

Le verdict compare l'écart à l'unité du dernier chiffre publié. Un chiffre arrondi au dixième est « conforme » si le recalcul s'en écarte d'au plus 0,05.

## Limites

- Les estimations 2026 de l'article ne sont pas vérifiables avant la publication des comptes.
- Les moyennes des pays voisins de son graphique 2 ne sont pas recalculées, seules les valeurs françaises le sont.
- Le texte de l'article n'est pas reproduit ici, par respect du droit d'auteur : seuls ses chiffres sont cités, avec leur emplacement.
- Les données d'Eurostat et de l'OCDE sont réutilisables en citant leur source, selon les conditions de chaque organisme.
