#!/usr/bin/env python3
"""Enregistre dans la base les effectifs de la fonction publique et la consommation des emplois de l'État que publie la
Direction générale de l'administration et de la fonction publique (DGAFP) avec son rapport annuel sur l'état de la
fonction publique : les classeurs de données de sa vue « L'évolution des effectifs de la fonction publique », que
réunit l'archive zip de chaque édition.

    python3 outils/importer_dgafp.py <fichier_id>

Dans chaque édition, la figure 4 du classeur de la fonction publique de l'État (« …donnees_comp_FPE.xlsx ») donne la
consommation des emplois de l'État de l'année précédente, en équivalents temps plein travaillé (ETPT), par ministère,
par budget annexe et au total, et son écart au plafond de la loi de finances rectificative de l'année, « corrigé des
transferts d'emplois intervenus en cours de gestion ». Un ministère est la fonction LOLF.EMPLOIS.<nom>, formée du nom
que lui donne la DGAFP, créée s'il le faut ; un budget annexe, la fonction de son nom, qui doit exister. La figure doit
présenter ses lignes dans cet ordre : les ministères, « Total Budget général », les budgets annexes, « Total budgets
annexes », « Total » ; son titre et ses en-têtes doivent nommer l'année, et chaque ligne porter au moins un nombre (une
case vide ou « / » ne donne pas de chiffre), sinon l'import s'arrête. Ses sommes ne sont pas vérifiées ici : le rapport
de cohérence les refait.

L'édition 2026 donne aussi, dans le classeur de l'ensemble de la fonction publique (« …donnees_comp_FP.xlsx »), les
effectifs physiques au 31 décembre, en milliers de personnes : de 1996 à 2024, hors bénéficiaires de contrats aidés,
pour l'ensemble, chaque versant et leurs parties (figure 5) ; de 2011 à 2024, avec les contrats aidés, pour l'ensemble
et chaque versant (figure 4). Les lignes et leurs libellés sont déclarés (FIGURE_5, FIGURE_4) ; les lignes hors contrats
aidés de la figure 4 doivent égaler celles de la figure 5, sinon l'import s'arrête. Une note de la figure 5 appelée par
une année (« 2009(2) ») ou par un versant (« FPE(3) ») est reprise par les chiffres de cette année ou de ce versant.

Les valeurs sont celles que gardent les cellules du classeur, débarrassées des artefacts de la virgule flottante
(commun.nombre) : le classeur les affiche arrondies, la consommation des emplois à l'unité et les effectifs au dixième
de millier, mais garde leurs décimales. Un zéro est exact : il prend la précision de sa ligne, celle de sa valeur la
plus précise. La période d'un chiffre est son année, sa version la date de l'archive (celle du plus récent de ses
fichiers). La DGAFP ne dit pas de statut pour les effectifs (non_precise) ; la consommation des emplois d'une année
close est définitive.
"""

import re
import sys
import zipfile

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_xlsx_dans_zip,
                    nombre, ouvrir_copie, table_des_chiffres)
from importer_lois_resultats import code_lolf

CLASSEUR_FPE = re.compile(r"(?:.*/)?[^/~]*donnees_comp_FPE\.xlsx", re.I)
CLASSEUR_FP = re.compile(r"(?:.*/)?[^/~]*donnees_comp_FP\.xlsx", re.I)
EDITION = re.compile(r"dgafp\.raefp-([0-9]{4})")
# Les éditions dont l'import lit aussi les effectifs physiques : la plus récente, qui rétropole toute la série.
AVEC_EFFECTIFS = {"dgafp.raefp-2026"}
# Consommation des emplois : la partie de la figure → (concept de la consommation, concept de l'écart au plafond).
CONCEPTS_EMPLOIS = {"BG": ("LOLF.BG_EMPLOIS_CONSOMMES", "LOLF.BG_EMPLOIS_ECART_PLAFOND"),
                    "BA": ("LOLF.BA_EMPLOIS_CONSOMMES", "LOLF.BA_EMPLOIS_ECART_PLAFOND"),
                    "ETAT": ("LOLF.EMPLOIS_CONSOMMES", "LOLF.EMPLOIS_ECART_PLAFOND")}
TOTAUX = {"Total Budget général": ("BG", "BA"), "Total budgets annexes": ("BA", "ETAT"), "Total": ("ETAT", None)}
# Une case vide, ou « / », ne donne pas de chiffre : la Transformation et la fonction publiques en 2021 (consommation
# « / »), la Cohésion des territoires et les relations avec les collectivités territoriales en 2023 (consommation vide,
# mais un écart au plafond).
SANS_CHIFFRE = {"", "/"}
# Effectifs physiques, figure 5 (en milliers, lignes 15 à 22) : (ligne, colonne A, colonne B, périmètre). La colonne A
# porte le versant sur la première ligne de son bloc, avec l'appel de sa note.
FIGURE_5 = [(15, "FPE(3)", "Ministères", "FPE_MINISTERES"), (16, "", "EPA de la FPE", "FPE_EPA"),
            (17, "", "Total", "FPE"),
            (18, "FPT", "Collectivités territoriales (communes, départements, régions)", "FPT_COLLECTIVITES"),
            (19, "", "EPA de la FPT", "FPT_EPA"), (20, "", "Total", "FPT"), (21, "FPH", "Total", "FPH"),
            (22, "Total", "", "FP")]
# Figure 4 (en milliers, lignes 15 à 22) : avec contrats aidés, puis hors contrats aidés, ligne de la figure 5 qu'elle
# doit égaler.
FIGURE_4 = [(15, "avec contrats aidés", "FPE", "FPE", None), (16, "", "FPT", "FPT", None), (17, "", "FPH", "FPH", None),
            (18, "", "Total", "FP", None), (19, "hors contrats aidés", "FPE", "FPE", 17), (20, "", "FPT", "FPT", 20),
            (21, "", "FPH", "FPH", 21), (22, "", "Total", "FP", 22)]
TITRE_5 = "Effectifs physiques par versant de la fonction publique (en distinguant les EPA)"
TITRE_4 = "Effectifs physiques par versant de la fonction publique (en distinguant les contrats aidés)"
CHAMP = "Champ : Emplois principaux, tous statuts,"


def propre(valeur):
    return " ".join(str(valeur if valeur is not None else "").split())


def chiffre(fichier, emplacement, perimetre, concept_, fonction, unite, annee, valeur, statut, consolidation,
            precision_ligne, note=""):
    texte, decimales = nombre(valeur)
    if float(texte) == 0:
        decimales = precision_ligne  # un zéro est exact : il prend la précision de sa ligne
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement, "zone": "FR",
        "perimetre_id": perimetre, "concept_id": concept_, "fonction_id": fonction, "traitements": "",
        "unite_id": unite, "periode": str(annee), "valeur": texte, "decimales": decimales, "statut": statut,
        "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": consolidation,
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def precision(valeurs):
    """La précision d'une ligne : les décimales de sa valeur la plus précise."""
    return max((nombre(v)[1] for v in valeurs if isinstance(v, float)), default=0)


def membre(fichier, motif):
    """Le seul classeur de l'archive dont le chemin répond au motif."""
    with zipfile.ZipFile(ouvrir_copie(BASE / fichier["chemin"])) as archive:
        noms = [n for n in archive.namelist() if motif.fullmatch(n)]
    if len(noms) != 1:
        sys.exit(f"{fichier['id']} : {len(noms)} classeurs répondent à {motif.pattern} dans l'archive ({noms})")
    return noms[0]


def consommation(fichier, annee, fonctions):
    """Les chiffres de la figure 4 du classeur de la fonction publique de l'État : consommation des emplois et écart au
    plafond, par ministère, par budget annexe et au total."""
    nom = membre(fichier, CLASSEUR_FPE)
    _, c = lire_xlsx_dans_zip(BASE / fichier["chemin"], nom, "Figure 4")
    attendus = {"A1": f"Consommation des emplois par ministère en {annee}",
                "B2": f"Consommation des emplois {annee} (en ETPT)",
                "C2": f"Écart constaté entre consommation {annee} et plafond LFR {annee}(1) (en ETPT)"}
    for cellule, texte in attendus.items():
        if propre(c.get(cellule)) != texte:
            sys.exit(f"{fichier['id']}, {nom}, figure 4, {cellule} : « {propre(c.get(cellule))} », attendu « {texte} »")
    partie, r = "BG", 3
    while partie is not None:
        libelle, conso, ecart = propre(c.get(f"A{r}")), c.get(f"B{r}"), c.get(f"C{r}")
        if not libelle or any(not isinstance(v, float) and propre(v) not in SANS_CHIFFRE for v in (conso, ecart)) \
                or not any(isinstance(v, float) for v in (conso, ecart)):
            sys.exit(f"{fichier['id']}, {nom}, figure 4, ligne {r} : « {libelle} », « {propre(conso)} », "
                     f"« {propre(ecart)} » : une ligne sans libellé, ou sans nombre, avant la ligne « Total »")
        if libelle in TOTAUX:
            if TOTAUX[libelle][0] != partie:
                sys.exit(f"{fichier['id']}, {nom}, figure 4, ligne {r} : « {libelle} » à sa place inattendue")
            fonction, suivante = "", TOTAUX[libelle][1]
        elif partie == "ETAT":
            sys.exit(f"{fichier['id']}, {nom}, figure 4, ligne {r} : « {libelle} » entre « Total budgets annexes » et "
                     f"« Total »")
        elif partie == "BG":
            fonction, suivante = f"LOLF.EMPLOIS.{code_lolf(libelle)}", partie
            if fonction not in fonctions:
                fonctions[fonction] = {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": ""}
        else:
            fonction, suivante = f"LOLF.{code_lolf(libelle)}", partie
            if fonction not in fonctions:
                sys.exit(f"{fichier['id']}, {nom}, figure 4, ligne {r} : budget annexe inconnu « {libelle} »")
        for colonne, valeur, concept_ in (("B", conso, CONCEPTS_EMPLOIS[partie][0]),
                                          ("C", ecart, CONCEPTS_EMPLOIS[partie][1])):
            if not isinstance(valeur, float):
                continue
            yield chiffre(fichier, f"classeur={nom};feuille=Figure 4;cellule={colonne}{r}", "ETAT_LF", concept_,
                          fonction, "ETPT", annee, valeur, "definitif", "non_consolide", precision((conso, ecart)))
        partie, r = suivante, r + 1
    if not propre(c.get(f"A{r}")).startswith("Source"):
        sys.exit(f"{fichier['id']}, {nom}, figure 4, ligne {r} : « {propre(c.get(f'A{r}'))} » après la ligne "
                 f"« Total », où la source était attendue")


def ligne_a(cellule):
    """Le numéro de ligne d'une cellule de la colonne A, 0 pour une autre colonne."""
    trouve = re.fullmatch(r"A([0-9]+)", cellule)
    return int(trouve.group(1)) if trouve else 0


def annees(c, ligne_):
    """{colonne: (année, appel de note ou None)} de la ligne des années d'une figure."""
    resultat = {}
    for cellule, valeur in c.items():
        m = re.fullmatch(r"([C-Z]|[A-Z][A-Z])([0-9]+)", cellule)
        if not m or int(m.group(2)) != ligne_:
            continue
        texte = propre(valeur)
        trouve = re.fullmatch(r"([0-9]{4})(?:\.0)?(?:\(([0-9])\))?", texte)
        if trouve is None:
            sys.exit(f"ligne des années, {cellule} : « {texte} »")
        resultat[m.group(1)] = (int(trouve.group(1)), trouve.group(2))
    return resultat


def effectifs(fichier):
    """Les chiffres des figures 5 et 4 du classeur de l'ensemble de la fonction publique."""
    nom = membre(fichier, CLASSEUR_FP)
    chemin = BASE / fichier["chemin"]
    _, f5 = lire_xlsx_dans_zip(chemin, nom, "Figure 5")
    _, f4 = lire_xlsx_dans_zip(chemin, nom, "Figure 4")
    for figure, c, titre in (("5", f5, TITRE_5), ("4", f4, TITRE_4)):
        if propre(c.get("A1")) != titre or propre(c.get("A13")) != "en milliers":
            sys.exit(f"{fichier['id']}, {nom}, figure {figure} : titre « {propre(c.get('A1'))} » ou unité "
                     f"« {propre(c.get('A13'))} » inattendus")
        if not any(propre(v).startswith(CHAMP) for k, v in c.items() if ligne_a(k) > 22):
            sys.exit(f"{fichier['id']}, {nom}, figure {figure} : pas de champ « {CHAMP} … »")
    # Les notes de la figure 5 : « (2) Depuis 2009, … ».
    notes = {}
    for cellule, valeur in f5.items():
        trouve = re.fullmatch(r"\(([0-9])\)\s*(.+)", propre(valeur))
        if ligne_a(cellule) > 22 and trouve:
            notes[trouve.group(1)] = trouve.group(2)
    colonnes5 = annees(f5, 14)
    valeurs5 = {}
    note_versant = None
    for ligne_, versant, partie, perimetre in FIGURE_5:
        a, b = propre(f5.get(f"A{ligne_}")), propre(f5.get(f"B{ligne_}"))
        if (a, b) != (versant, partie):
            sys.exit(f"{fichier['id']}, {nom}, figure 5, ligne {ligne_} : « {a} » « {b} », attendu « {versant} » "
                     f"« {partie} »")
        appel = re.search(r"\(([0-9])\)$", versant)
        note_versant = appel.group(1) if appel else (note_versant if not versant else None)
        precision5 = precision(f5.get(f"{colonne}{ligne_}") for colonne in colonnes5)
        for colonne, (annee, appel_annee) in colonnes5.items():
            valeur = f5.get(f"{colonne}{ligne_}")
            if not isinstance(valeur, float):
                sys.exit(f"{fichier['id']}, {nom}, figure 5, {colonne}{ligne_} : « {propre(valeur)} » n'est pas un "
                         f"nombre")
            appels = [n for n in (note_versant, appel_annee) if n]
            if any(n not in notes for n in appels):
                sys.exit(f"{fichier['id']}, {nom}, figure 5, {colonne}{ligne_} : note {appels} introuvable")
            valeurs5[(ligne_, annee)] = valeur
            yield chiffre(fichier, f"classeur={nom};feuille=Figure 5;cellule={colonne}{ligne_}", perimetre,
                          "FONCTION_PUBLIQUE.EFFECTIFS_PHYSIQUES", "", "K_PERSONNES", annee, valeur, "non_precise",
                          "sans_objet", precision5, " ".join(notes[n] for n in appels))
    colonnes4 = annees(f4, 14)
    for ligne_, groupe, versant, perimetre, egale in FIGURE_4:
        a, b = propre(f4.get(f"A{ligne_}")), propre(f4.get(f"B{ligne_}"))
        if (a, b) != (groupe, versant):
            sys.exit(f"{fichier['id']}, {nom}, figure 4, ligne {ligne_} : « {a} » « {b} », attendu « {groupe} » "
                     f"« {versant} »")
        precision4 = precision(f4.get(f"{colonne}{ligne_}") for colonne in colonnes4)
        for colonne, (annee, appel_annee) in colonnes4.items():
            valeur = f4.get(f"{colonne}{ligne_}")
            if not isinstance(valeur, float) or appel_annee:
                sys.exit(f"{fichier['id']}, {nom}, figure 4, {colonne}{ligne_} : « {propre(valeur)} » inattendu")
            if egale is not None:
                if (egale, annee) not in valeurs5 or nombre(valeurs5[(egale, annee)]) != nombre(valeur):
                    sys.exit(f"{fichier['id']}, {nom}, figure 4, {colonne}{ligne_} : {valeur} hors contrats aidés, "
                             f"quand la figure 5 donne {valeurs5.get((egale, annee))}")
                continue
            yield chiffre(fichier, f"classeur={nom};feuille=Figure 4;cellule={colonne}{ligne_}", perimetre,
                          "FONCTION_PUBLIQUE.EFFECTIFS_PHYSIQUES_YC_CONTRATS_AIDES", "", "K_PERSONNES", annee, valeur,
                          "non_precise", "sans_objet", precision4)


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une archive d'une édition."""
    edition = EDITION.fullmatch(fichier["source_id"])
    if edition is None or not fichier["chemin"].endswith(".zip"):
        sys.exit(f"{fichier['id']} : copie qui n'est pas l'archive zip d'une édition du rapport annuel")
    yield from consommation(fichier, int(edition.group(1)) - 1, fonctions)
    if fichier["source_id"] in AVEC_EFFECTIFS:
        yield from effectifs(fichier)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    avant = set(fonctions)
    ajoutes, inchanges = fusionner(existants, list(lignes_du_fichier(fichier, fonctions)), fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    nouvelles = sorted(set(fonctions) - avant)
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte "
          f"{len(existants)} ; fonctions nouvelles : {', '.join(nouvelles) or 'aucune'}")


if __name__ == "__main__":
    main()
