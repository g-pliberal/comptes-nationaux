#!/usr/bin/env python3
"""Enregistre dans la base le coût de chaque dépense fiscale (« niche fiscale »), tel que le chiffre le tome II de
l'annexe « Évaluations des voies et moyens » d'un projet de loi de finances (article 51 de la loi organique relative
aux lois de finances), dans le classeur de la liste des dépenses fiscales que la direction du budget publie sur
data.economie.gouv.fr.

    python3 outils/importer_depenses_fiscales.py <fichier_id>

La feuille « Chiffrages » du classeur porte une ligne par dépense fiscale : l'impôt dont elle relève (« Catégorie »),
son numéro à six chiffres, son libellé législatif, et son coût en millions d'euros pour trois années, l'avant-dernière
(« Réalisation »), la dernière et celle du projet de loi (« Prévision »). Les en-têtes doivent être ceux que l'import
attend et nommer ces trois années ; le classeur du projet de loi de finances pour 2020 ne les nomme pas
(« Réalisation », « Prévision de réalisation », « Prévision ») : ce sont 2018, 2019 et 2020 (ANNEES_DECLAREES). Une case
sans montant ne donne pas de chiffre, et doit être l'une de celles que la légende de la feuille explique : « - »
(aucun effet budgétaire), « ε » (montant inférieur à 0,5 million d'euros, non calculé), « nc » (non chiffré), ou vide.
Tout autre contenu, un numéro qui n'a pas six chiffres ou qui revient deux fois, arrête l'import.

Une dépense fiscale est la fonction LOLF.DEPENSE_FISCALE.<numéro>, créée s'il le faut avec le libellé du premier
classeur importé qui la porte (les libellés changent d'une année à l'autre, pas les numéros). L'impôt dont elle relève
change lui aussi de nom d'un classeur à l'autre (la taxe intérieure de consommation sur les produits énergétiques
devient « Taxes intérieures de consommation », puis « Accise sur les énergies ») : chaque chiffre garde, dans ses
notes, la catégorie que lui donne son classeur (« Catégorie : Impôt sur le revenu »). Le chiffre est le coût
(LOLF.DEPENSE_FISCALE), en millions d'euros : une
estimation pour l'année de la « Réalisation » (le tome chiffre un manque à gagner, il ne le constate pas), une prévision
pour les deux autres. Les sommes ne sont pas refaites ici : le rapport de cohérence les fait, par impôt et par année,
et compare les chiffrages successifs d'une même année. La période d'un chiffre est son année, sa version la date de
modification inscrite dans le classeur.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_xlsx, nombre,
                    position, table_des_chiffres)

SOURCE = re.compile(r"budget\.depenses-fiscales-plf([0-9]{4})")
FEUILLE = "Chiffrages"
RACINE = "LOLF.DEPENSE_FISCALE"
CONCEPT = "LOLF.DEPENSE_FISCALE"
# Cases sans montant que la légende de la feuille explique.
SANS_MONTANT = {"-", "ε", "nc", ""}
# Projet de loi dont le classeur ne nomme pas les années de ses trois colonnes.
ANNEES_DECLAREES = {2020: (2018, 2019, 2020)}
COLONNES = ("F", "G", "H")
STATUTS = ("estimation", "prevision", "prevision")
LEGENDE = "Les chiffrages des colonnes F,G et H sont en millions d'euros"


def propre(valeur):
    return " ".join(str(valeur).split())


def lignes_de_la_feuille(cellules):
    """{numéro de ligne: {colonne: valeur}}."""
    lignes = {}
    for reference, valeur in cellules.items():
        n, colonne = position(reference)
        lignes.setdefault(n, {})[colonne] = valeur
    return lignes


def annees_du_classeur(lignes, plf, lieu):
    """Les trois années des colonnes F, G et H, lues dans les en-têtes ou déclarées."""
    if not propre(lignes.get(1, {}).get("A", "")).startswith(LEGENDE):
        sys.exit(f"{lieu} : la feuille ne dit plus ses montants en millions d'euros (cellule A1)")
    entetes = [propre(lignes.get(n, {}).get(c, "")) for n in (3, 4) for c in COLONNES]
    if plf in ANNEES_DECLAREES:
        if entetes[:3] != ["Réalisation", "Prévision de réalisation", "Prévision"] or any(entetes[3:]):
            sys.exit(f"{lieu} : en-têtes inattendus {entetes}")
        return ANNEES_DECLAREES[plf]
    if entetes[:3] != ["Réalisation", "Prévision", "Prévision"]:
        sys.exit(f"{lieu} : en-têtes inattendus {entetes}")
    annees = tuple(int(float(a)) if re.fullmatch(r"[0-9]{4}(\.0)?", a) else None for a in entetes[3:])
    if annees != (plf - 2, plf - 1, plf):
        sys.exit(f"{lieu} : années {entetes[3:]}, attendues {plf - 2}, {plf - 1} et {plf}")
    return annees


def lignes_du_fichier(fichier, fonctions):
    trouve = SOURCE.fullmatch(fichier["source_id"])
    if trouve is None:
        sys.exit(f"{fichier['id']} : la source n'est pas une liste des dépenses fiscales")
    plf, lieu = int(trouve.group(1)), f"{fichier['id']}, feuille {FEUILLE}"
    lignes = lignes_de_la_feuille(lire_xlsx(BASE / fichier["chemin"], FEUILLE)[1])
    annees = annees_du_classeur(lignes, plf, lieu)
    vus = set()
    for n in sorted(lignes):
        ligne = lignes[n]
        if n <= 4 or not any(propre(v) for v in ligne.values()):
            continue
        numero, categorie, libelle = ligne.get("D"), propre(ligne.get("A", "")), propre(ligne.get("E", ""))
        if not isinstance(numero, float) or numero != int(numero) or not 0 < numero < 1000000 or not categorie \
                or not libelle:
            sys.exit(f"{lieu}, ligne {n} : ligne sans numéro à six chiffres, sans catégorie ou sans libellé")
        numero = f"{int(numero):06d}"
        if numero in vus:
            sys.exit(f"{lieu}, ligne {n} : la dépense fiscale {numero} revient deux fois")
        vus.add(numero)
        fonction = f"{RACINE}.{numero}"
        if fonction not in fonctions:
            fonctions[fonction] = {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": RACINE}
        for colonne, annee, statut in zip(COLONNES, annees, STATUTS):
            valeur = ligne.get(colonne, "")
            if not isinstance(valeur, float):
                if propre(valeur) not in SANS_MONTANT:
                    sys.exit(f"{lieu}, cellule {colonne}{n} : contenu inattendu « {valeur} »")
                continue
            texte, decimales = nombre(valeur)
            chiffre = {
                "source_id": fichier["source_id"], "fichier_id": fichier["id"],
                "emplacement": f"feuille={FEUILLE};cellule={colonne}{n}", "zone": "FR", "perimetre_id": "ETAT_LF",
                "concept_id": CONCEPT, "fonction_id": fonction, "traitements": "", "unite_id": "MIO_EUR",
                "periode": str(annee), "valeur": texte, "decimales": decimales, "statut": statut,
                "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": "sans_objet",
                "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(),
                "notes": f"Catégorie : {categorie}",
            }
            chiffre["id"] = identifiant(chiffre)
            yield chiffre
    if not vus:
        sys.exit(f"{lieu} : aucune dépense fiscale")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    if RACINE not in fonctions:
        sys.exit(f"fonction {RACINE} absente de tables/fonctions.csv")
    avant = set(fonctions)
    nouveaux = list(lignes_du_fichier(fichier, fonctions))
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, nouveaux, fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte "
          f"{len(existants)} ; {len(set(fonctions) - avant)} fonctions nouvelles")


if __name__ == "__main__":
    main()
