#!/usr/bin/env python3
"""Enregistre dans la base le coût des « niches sociales », mesure par mesure : les allègements généraux et les
exonérations ciblées de cotisations et de contributions de sécurité sociale, et les exemptions d'assiette, tels que les
donnent les classeurs de données de l'annexe 4 des projets de loi de financement de la sécurité sociale (PLFSS) et de
l'annexe 2 des projets de loi d'approbation des comptes de la sécurité sociale (PLACSS), que publie la direction de la
sécurité sociale sur securite-sociale.fr.

    python3 outils/importer_niches_sociales.py <fichier_id>

Deux sortes de tableaux sont lues dans chaque classeur, déclarés source par source (TABLEAUX) parce que leur feuille, leurs
colonnes et leurs années changent d'une édition à l'autre.

Les premiers donnent le coût des allègements généraux et des exonérations ciblées, en millions d'euros et en droits
constatés, sur le champ des régimes obligatoires de base : une ligne par mesure, sous des lignes de titre en capitales
qui en portent la somme (« ALLÈGEMENTS GÉNÉRAUX… », « EXONÉRATIONS CIBLÉES COMPENSÉES… », une ligne par mission du budget
de l'État qui compense, « EXONÉRATIONS NON COMPENSÉES », « TOTAL »). Chaque colonne lue est déclarée avec son année et
son statut (réalisé ou prévision), et son en-tête doit nommer cette année ; les colonnes d'évolution ne sont pas lues,
ni la prévision que les annexes des PLACSS rappellent à côté du réalisé. Une mesure est la fonction
COMPTES_SECU.EXO_<libellé>, une ligne de titre aussi, créées s'il le faut ; chaque chiffre garde dans ses notes la
ligne de titre sous laquelle son classeur le range (« Sous : MISSION SPORT »), car une mesure change parfois de rubrique
d'une édition à l'autre. Une ligne « Dont… », qui précise la mesure qui la précède, en prend le nom dans le sien ; une
mesure que le classeur répète sous une autre rubrique prend le nom de cette rubrique ; deux lignes qui gardent le même
nom arrêtent l'import. Les exonérations non compensées, que certaines éditions donnent dans un tableau à part, sont
lues à la suite des autres.

Le second donne le coût des exemptions d'assiette, en milliards d'euros : pour chaque dispositif et chaque année,
l'assiette exemptée et les cotisations qu'elle aurait portées, brutes puis nettes de ce que rapportent les
prélèvements qui la frappent quand même (forfait social, contributions spécifiques). Les années sont celles que nomment
les en-têtes, « (p) » pour une prévision ; sous chacune, les trois colonnes doivent s'intituler « Assiette exemptée »,
« Cotisations équivalentes », « Brutes » et « Nettes ». Un dispositif est la fonction COMPTES_SECU.EXEMPTION_<libellé>.
La feuille du PLFSS pour 2024 ne dit pas son unité : c'est celle des autres éditions, les montants en témoignent.

Une cellule vide ou un tiret ne donne pas de chiffre ; tout autre contenu qui n'est pas un nombre arrête l'import. Les
valeurs sont celles que gardent les cellules, débarrassées des artefacts de la virgule flottante (commun.nombre) : les
classeurs récents les gardent avec toutes leurs décimales. Les sommes ne sont pas refaites ici : le rapport de
cohérence les fait, et compare les éditions entre elles. La période d'un chiffre est son année, sa version la date de
modification inscrite dans le classeur, ou celle de son téléchargement quand il n'en porte pas (celui du PLFSS pour
2027). Une ligne qu'un classeur donne deux fois avec le même montant n'est enregistrée qu'une fois.

Les annexes 5 des PLFSS pour 2007 à 2022, qui précèdent ces classeurs, n'existent qu'en PDF et ne sont pas lues ; le
classeur de l'annexe 2 du PLACSS pour 2025 ne porte que la grille d'analyse des mesures, sans leur coût.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_xlsx, nombre,
                    position, table_des_chiffres)
from importer_lois_resultats import code_lolf

R, P = "definitif", "prevision"
# Source → (tableaux des coûts, tableau des exemptions).
# Coûts : [(feuille, colonne des libellés, {colonne : (année, statut, cellule de l'en-tête qui nomme l'année ou None,
# sous-titre attendu sous l'en-tête ou None)})]. Un tableau sans en-tête d'années (None) est la suite du précédent, aux
# mêmes colonnes : son titre doit nommer la première et la dernière de ses années.
# Exemptions : (feuille, colonne des libellés, ligne des années).
def _trois(c1, c2, c3, annee, ligne):
    return {c1: (annee, R, f"{c1}{ligne}", None), c2: (annee + 1, P, f"{c2}{ligne}", None),
            c3: (annee + 2, P, f"{c3}{ligne}", None)}


TABLEAUX = {
    "secu.plfss2023-annexe4": ([("III.tab15", "C", _trois("D", "E", "G", 2021, 3)),
                                ("III.tab16", "C", {"D": (2021, R, None, None), "E": (2022, P, None, None),
                                                    "G": (2023, P, None, None)})], ("I.tab9", "B", 3)),
    "secu.plfss2024-annexe4": ([("II.tab13", "B", _trois("C", "D", "F", 2022, 5)),
                                ("II.tab14", "B", _trois("C", "D", "F", 2022, 5))], ("I.tab9", "C", 2)),
    "secu.plfss2025-annexe4": ([("II.tab13", "B", _trois("C", "D", "F", 2023, 5)),
                                ("II.tab14", "B", _trois("C", "D", "F", 2023, 5))], ("I.tab9", "C", 3)),
    "secu.plfss2026-annexe4": ([("III.tab13", "B", _trois("C", "D", "F", 2024, 4)),
                                ("III.tab14", "B", _trois("C", "D", "F", 2024, 4))], ("I.tab9", "C", 3)),
    "secu.plfss2027-annexe4": ([("I.tab13", "B", {**_trois("C", "D", "F", 2025, 3), "H": (2028, P, "H3", None),
                                                  "I": (2029, P, "I3", None), "J": (2030, P, "J3", None)})],
                               ("I.tab9", "C", 3)),
    "secu.placss2023-annexe2": ([("T1_Tab_11", "B", {"C": (2022, R, "C4", "Réalisé"), "E": (2023, R, "D4", "Réalisé")}),
                                 ("T1_Tab_12", "B", {"D": (2023, R, "C4", "Réalisé")})], ("T1_Tab_9", "C", 3)),
    "secu.placss2024-annexe2": ([("T1_Tab_11", "B", {"C": (2023, R, "C4", "Réalisé"), "E": (2024, R, "D4", "Réalisé")}),
                                 ("T1_Tab_12", "B", {"D": (2024, R, "C4", "Réalisé")})], ("T1_Tab_9", "C", 3)),
}
CONCEPT_COUT = "LFSS.EXONERATION_COUT"
CONCEPTS_EXEMPTION = ("LFSS.EXEMPTION_ASSIETTE", "LFSS.EXEMPTION_COTISATIONS_BRUTES",
                      "LFSS.EXEMPTION_COTISATIONS_NETTES")
RACINE_COUT, RACINE_EXEMPTION = "COMPTES_SECU.EXONERATIONS", "COMPTES_SECU.EXEMPTIONS_ASSIETTE"
SANS_MONTANT = {"", "-", "–", "n.d.", "nd", "ns", "x"}
# Ce qui suit un tableau et n'en est pas : notes, champ, source.
APRES = re.compile(r"(\*|Champs? |Note|Source|Lecture|\(\*\)|\(p\))", re.I)

def propre(valeur):
    return " ".join(str(valeur).split())


def libelle_propre(valeur):
    """Le libellé d'une ligne, sans les astérisques de ses appels de note."""
    return propre(re.sub(r"\*+", "", str(valeur)))


def lignes_de_la_feuille(cellules):
    lignes = {}
    for reference, valeur in cellules.items():
        n, colonne = position(reference)
        lignes.setdefault(n, {})[colonne] = valeur
    return lignes


def en_capitales(libelle):
    return libelle == libelle.upper() and re.search(r"[A-Z]{3}", libelle) is not None


def annee_d_entete(valeur):
    """(année, vrai si prévision) d'un en-tête : « 2021.0 », « 2021* », « 2022 (p) », « 2023(p) » ; None sinon."""
    trouve = re.fullmatch(r"([0-9]{4})(?:\.0)?\s*\*?\s*(\(p\))?\s*\*?", propre(valeur), re.I)
    return (int(trouve.group(1)), trouve.group(2) is not None) if trouve else None


def chiffre(fichier, emplacement, concept, fonction, unite, annee, valeur, statut, note):
    texte, decimales = nombre(valeur)
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement, "zone": "FR",
        "perimetre_id": "ROBSS", "concept_id": concept, "fonction_id": fonction, "traitements": "",
        "unite_id": unite, "periode": str(annee), "valeur": texte, "decimales": decimales, "statut": statut,
        "drapeau_source": "", "version": (fichier["mis_a_jour_source"] or fichier["telecharge_le"])[:10],
        "consolidation": "sans_objet",
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def montant(valeur, lieu):
    """La valeur d'une cellule de montant : un nombre, ou None pour une cellule sans montant."""
    if isinstance(valeur, float):
        return valeur
    if propre(valeur) not in SANS_MONTANT:
        sys.exit(f"{lieu} : contenu inattendu « {valeur} »")
    return None


def couts(fichier, feuille, colonne_libelle, colonnes, fonctions, vus):
    lieu = f"{fichier['id']}, feuille {feuille}"
    cellules = lire_xlsx(BASE / fichier["chemin"], feuille)[1]
    lignes = lignes_de_la_feuille(cellules)
    debut = 0
    for colonne, (annee, _, entete, sous_titre) in colonnes.items():
        if entete is None:
            continue
        lu = annee_d_entete(cellules.get(entete, ""))
        if lu is None or lu[0] != annee:
            sys.exit(f"{lieu} : l'en-tête {entete} ne nomme pas {annee} (« {cellules.get(entete, '')} »)")
        n = position(entete)[0]
        if sous_titre is not None:
            n += 1
            if propre(cellules.get(f"{colonne}{n}", "")) != sous_titre:
                sys.exit(f"{lieu} : la cellule {colonne}{n} n'est pas « {sous_titre} »")
        debut = max(debut, n)
    if not debut:  # la suite du tableau précédent : son titre nomme ses années extrêmes
        annees = sorted(a for a, _, _, _ in colonnes.values())
        debut = min(n for n in lignes if n > 1 and colonne_libelle in lignes[n]) - 1
        if f"{annees[0]}-{annees[-1]}" not in propre(cellules.get("A1", "")):
            sys.exit(f"{lieu} : le titre ne nomme pas les années {annees[0]}-{annees[-1]}")
    if not re.search(r"M€|millions d'euros", " ".join(propre(v) for n in range(1, debut + 2)
                                                      for v in lignes.get(n, {}).values())):
        sys.exit(f"{lieu} : le tableau ne dit pas ses montants en millions d'euros")
    rubrique, mesure, lues = "", "", 0
    for n in sorted(lignes):
        libelle = libelle_propre(lignes[n].get(colonne_libelle, ""))
        if n <= debut or not libelle or re.fullmatch(r"%|[0-9]{4}-[0-9]{4}|\(.*en droits constatés\)", libelle):
            continue
        if APRES.match(libelle):
            break
        titre = en_capitales(libelle)
        # Une ligne « Dont… » précise la mesure qui la précède, et son libellé revient sous plusieurs mesures : elle
        # en prend le nom. Une mesure que le tableau répète sous une autre rubrique prend le nom de cette rubrique.
        cle = f"{libelle} ({mesure})" if libelle.lower().startswith("dont ") else libelle
        if cle in vus:
            cle = f"{libelle} ({rubrique})"
        if cle in vus:
            sys.exit(f"{lieu}, ligne {n} : le libellé « {libelle} » revient deux fois sous « {rubrique} »")
        vus.add(cle)
        fonction = f"COMPTES_SECU.EXO_{code_lolf(cle)}"
        if fonction not in fonctions:
            fonctions[fonction] = {"id": fonction, "libelle": cle, "norme_id": "LFSS", "parent_id": RACINE_COUT}
        note = "Ligne de titre du tableau." if titre else f"Sous : {rubrique}" if rubrique else ""
        for colonne, (annee, statut, _, _) in colonnes.items():
            valeur = montant(lignes[n].get(colonne, ""), f"{lieu}, cellule {colonne}{n}")
            if valeur is not None:
                lues += 1
                yield chiffre(fichier, f"feuille={feuille};cellule={colonne}{n}", CONCEPT_COUT, fonction, "MIO_EUR",
                              annee, valeur, statut, note)
        if titre:
            rubrique = libelle
        elif not libelle.lower().startswith("dont "):
            mesure = libelle
    if not lues:
        sys.exit(f"{lieu} : aucun montant")


def suivante(colonne, pas):
    return chr(ord(colonne) + pas)


def exemptions(fichier, feuille, colonne_libelle, ligne_annees, fonctions):
    lieu = f"{fichier['id']}, feuille {feuille}"
    cellules = lire_xlsx(BASE / fichier["chemin"], feuille)[1]
    lignes = lignes_de_la_feuille(cellules)
    annees = {}
    for colonne, valeur in lignes.get(ligne_annees, {}).items():
        lu = annee_d_entete(valeur)
        if lu is None:
            continue
        attendus = {f"{colonne}{ligne_annees + 1}": "Assiette exemptée",
                    f"{suivante(colonne, 1)}{ligne_annees + 1}": "Cotisations équivalentes",
                    f"{suivante(colonne, 1)}{ligne_annees + 2}": "Brutes",
                    f"{suivante(colonne, 2)}{ligne_annees + 2}": "Nettes"}
        for cellule, texte in attendus.items():
            if propre(cellules.get(cellule, "")) != texte:
                sys.exit(f"{lieu} : la cellule {cellule} n'est pas « {texte} » (« {cellules.get(cellule, '')} »)")
        annees[colonne] = lu
    if len(annees) < 3 or len({a for a, _ in annees.values()}) != len(annees):
        sys.exit(f"{lieu} : années introuvables ou répétées en ligne {ligne_annees}")
    vus, total = set(), False
    for n in sorted(lignes):
        libelle = libelle_propre(lignes[n].get(colonne_libelle, ""))
        if n <= ligne_annees + 2 or not libelle:
            continue
        if total or APRES.match(libelle):
            break
        if libelle in vus:
            sys.exit(f"{lieu}, ligne {n} : le libellé « {libelle} » revient deux fois")
        vus.add(libelle)
        fonction = f"COMPTES_SECU.EXEMPTION_{code_lolf(libelle)}"
        if fonction not in fonctions:
            fonctions[fonction] = {"id": fonction, "libelle": libelle, "norme_id": "LFSS",
                                   "parent_id": RACINE_EXEMPTION}
        for colonne, (annee, prevision) in annees.items():
            for pas, concept in enumerate(CONCEPTS_EXEMPTION):
                cellule = f"{suivante(colonne, pas)}{n}"
                valeur = montant(lignes[n].get(suivante(colonne, pas), ""), f"{lieu}, cellule {cellule}")
                if valeur is not None:
                    yield chiffre(fichier, f"feuille={feuille};cellule={cellule}", concept, fonction, "MD_EUR", annee,
                                  valeur, P if prevision else R, "")
        total = libelle.upper().startswith("TOTAL")
    if not total:
        sys.exit(f"{lieu} : le tableau ne finit pas par sa ligne de total")


def lignes_du_fichier(fichier, fonctions):
    if fichier["source_id"] not in TABLEAUX:
        sys.exit(f"{fichier['id']} : source sans tableaux déclarés (TABLEAUX)")
    tableaux, (feuille_ex, colonne_ex, ligne_ex) = TABLEAUX[fichier["source_id"]]
    vus = set()
    for feuille, colonne, colonnes in tableaux:
        yield from couts(fichier, feuille, colonne, colonnes, fonctions, vus)
    yield from exemptions(fichier, feuille_ex, colonne_ex, ligne_ex, fonctions)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    for racine in (RACINE_COUT, RACINE_EXEMPTION):
        if racine not in fonctions:
            sys.exit(f"fonction {racine} absente de tables/fonctions.csv")
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
