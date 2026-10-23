#!/usr/bin/env python3
"""Enregistre dans la base les chiffres d'un projet ou d'une loi relative aux résultats de la gestion et portant
approbation des comptes de l'année (ancienne loi de règlement), à partir de son texte publié par le Sénat
(page HTML archivée).

    python3 outils/importer_lois_resultats.py <fichier_id>

Tableaux pris en charge :
- l'article 1er : résultat budgétaire de l'État, recettes et dépenses du budget général, des budgets annexes
  et des comptes spéciaux ;
- l'article 4 : autorisations d'engagement consommées et dépenses du budget général, par mission et par
  programme, avec les ouvertures et annulations de crédits que la loi y ajoute.

Les missions et les programmes sont les « fonctions » de la norme LOLF : l'import les inscrit dans la table
des fonctions à leur première apparition, sous un identifiant formé de leur libellé. Chaque libellé de ligne et
de colonne doit avoir une correspondance ci-dessous : un libellé inconnu arrête l'import. Une case vide n'est
pas un chiffre. La version d'un chiffre est la date que le texte porte (enregistrement, transmission ou
adoption) ; les montants exécutés sont définitifs, comme le texte les qualifie, les ajustements de crédits ne
reçoivent pas de statut.
"""

import re
import sys
import unicodedata

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire,
                    lire_tableaux_html, nombre_texte, table_des_chiffres, texte_html)

# Article 1er : libellé de ligne → {colonne : concept}. Dans la rubrique des budgets annexes, une ligne qui n'est pas
# ci-dessous est un budget annexe, c'est-à-dire une mission : ses colonnes vont dans BUDGET_ANNEXE.
ARTICLE_1 = {
    "Recettes fiscales brutes": {"Recettes": "LOLF.BG_RECETTES_FISCALES_BRUTES"},
    "À déduire : Remboursements et dégrèvements d’impôts d’État": {"Recettes": "LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS",
                                                                   "Dépenses": "LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS"},
    "Recettes fiscales nettes (a)": {"Recettes": "LOLF.BG_RECETTES_FISCALES_NETTES"},
    "Recettes non fiscales (b)": {"Recettes": "LOLF.BG_RECETTES_NON_FISCALES"},
    "Montant net des recettes hors fonds de concours (c = a + b)": {"Recettes": "LOLF.BG_RECETTES_NETTES_HORS_FDC"},
    "À déduire : Prélèvements sur recettes au profit des collectivités territoriales et de l’Union européenne (d)":
        {"Recettes": "LOLF.BG_PRELEVEMENTS_SUR_RECETTES"},
    "Total net des recettes hors prélèvements sur recettes (e = c - d)": {"Recettes": "LOLF.BG_RECETTES_NETTES_HORS_PSR"},
    "Fonds de concours (f)": {"Recettes": "LOLF.BG_FONDS_DE_CONCOURS_RECETTES"},
    "Montant net des recettes y compris fonds de concours (g = e + f)": {"Recettes": "LOLF.BG_RECETTES_NETTES"},
    "Dépenses brutes hors fonds de concours": {"Dépenses": "LOLF.BG_DEPENSES_BRUTES_HORS_FDC"},
    "Montant net des dépenses (h)": {"Dépenses": "LOLF.BG_DEPENSES_NETTES_HORS_FDC"},
    "Fonds de concours (i)": {"Dépenses": "LOLF.BG_FONDS_DE_CONCOURS_DEPENSES"},
    "Montant net des dépenses y compris fonds de concours (j = h + i)": {"Dépenses": "LOLF.BG_DEPENSES_NETTES"},
    "Total du budget général y compris fonds de concours": {"Dépenses": "LOLF.BG_DEPENSES_NETTES",
                                                            "Recettes": "LOLF.BG_RECETTES_NETTES",
                                                            "Soldes": "LOLF.SOLDE_BUDGET_GENERAL"},
    "Fonds de concours": {"Dépenses": "LOLF.BA_FDC_DEPENSES", "Recettes": "LOLF.BA_FDC_RECETTES",
                          "Soldes": "LOLF.BA_FDC_SOLDE"},
    "Total des budgets annexes y compris fonds de concours": {"Dépenses": "LOLF.BA_DEPENSES", "Recettes": "LOLF.BA_RECETTES",
                                                              "Soldes": "LOLF.SOLDE_BUDGETS_ANNEXES"},
    "Comptes d’affectation spéciale": {"Dépenses": "LOLF.CAS_DEPENSES", "Recettes": "LOLF.CAS_RECETTES",
                                       "Soldes": "LOLF.CAS_SOLDE"},
    "Comptes de concours financiers": {"Dépenses": "LOLF.CCF_DEPENSES", "Recettes": "LOLF.CCF_RECETTES",
                                       "Soldes": "LOLF.CCF_SOLDE"},
    "Comptes de commerce (solde)": {"Dépenses": "LOLF.COMPTES_COMMERCE_SOLDE_EN_DEPENSES",
                                    "Soldes": "LOLF.COMPTES_COMMERCE_SOLDE"},
    "Comptes d’opérations monétaires hors opérations avec le Fonds monétaire international (solde)":
        {"Dépenses": "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_DEPENSES", "Soldes": "LOLF.OPERATIONS_MONETAIRES_SOLDE"},
    "Total des comptes spéciaux hors opérations avec le Fonds monétaire international":
        {"Dépenses": "LOLF.CS_DEPENSES", "Recettes": "LOLF.CS_RECETTES", "Soldes": "LOLF.SOLDE_COMPTES_SPECIAUX"},
    "Résultat budgétaire de l’État hors opérations avec le Fonds monétaire international":
        {"Soldes": "LOLF.RESULTAT_BUDGETAIRE"},
}
RUBRIQUES_ARTICLE_1 = {"Budget général", "Recettes", "Dépenses", "Budgets annexes", "Comptes spéciaux"}
BUDGET_ANNEXE = {"Dépenses": "LOLF.BA_DEPENSES_HORS_FDC", "Recettes": "LOLF.BA_RECETTES_HORS_FDC",
                 "Soldes": "LOLF.BA_SOLDE_HORS_FDC"}

# Article 4 : intitulé de colonne → concept, pour le tableau des autorisations d'engagement et celui des dépenses.
ARTICLE_4 = {
    "Autorisations d’engagement consommées": "LOLF.BG_AE_CONSOMMEES",
    "Ouvertures d’autorisations d’engagement complémentaires": "LOLF.BG_AE_OUVERTURES",
    "Annulations d’autorisations d’engagement non consommées et non reportées": "LOLF.BG_AE_ANNULATIONS",
    "Dépenses": "LOLF.BG_DEPENSES_BRUTES",
    "Ouvertures de crédits complémentaires": "LOLF.BG_CP_OUVERTURES",
    "Annulations de crédits non consommés et non reportés": "LOLF.BG_CP_ANNULATIONS",
}
AJUSTEMENTS = {"LOLF.BG_AE_OUVERTURES", "LOLF.BG_AE_ANNULATIONS", "LOLF.BG_CP_OUVERTURES", "LOLF.BG_CP_ANNULATIONS"}
SOLDES = {c for lignes in ARTICLE_1.values() for colonne, c in lignes.items() if colonne == "Soldes"} | {"LOLF.BA_SOLDE_HORS_FDC"}


def propre(texte):
    """Libellé sans points de conduite, avec un seul type de tiret."""
    return re.sub(r"(\s*\.)+\s*$", "", texte.replace("–", "-").replace("−", "-")).strip()


def code_lolf(libelle):
    """Identifiant formé d'un libellé : « Action extérieure de l’État » → ACTION_EXTERIEURE_DE_L_ETAT."""
    ascii_ = unicodedata.normalize("NFKD", libelle).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "_", ascii_.upper()).strip("_")


def colonnes(tableau, entete):
    """Intitulé de chaque colonne : le dernier texte non vide des lignes d'en-tête."""
    noms = {}
    for ligne in tableau[:entete]:
        for c, texte in enumerate(ligne):
            if propre(texte) and c > 0:
                noms[c] = propre(texte)
    return noms


def article_1(tableaux):
    """(indice, tableau) de l'article 1er : celui qui se termine par le résultat budgétaire."""
    for i, t in enumerate(tableaux):
        if any(propre(l[0]).startswith("Résultat budgétaire de l’État") for l in t if l):
            return i, t
    sys.exit("tableau de l'article 1er introuvable")


def lignes_article_1(i, tableau):
    entete = next(r for r, l in enumerate(tableau) if "Soldes" in [propre(x) for x in l]) + 1
    noms, rubrique = colonnes(tableau, entete), ""
    for r, ligne in enumerate(tableau[entete:], start=entete):
        libelle = propre(ligne[0])
        valeurs = {c: nombre_texte(x) for c, x in enumerate(ligne) if c > 0 and nombre_texte(x)}
        if libelle in RUBRIQUES_ARTICLE_1:
            rubrique = libelle
        if not valeurs:
            continue
        if libelle in ARTICLE_1:
            concepts, fonction = ARTICLE_1[libelle], ""
        elif rubrique == "Budgets annexes" and not libelle.lower().startswith(("total", "fonds", "dont")):
            concepts, fonction = BUDGET_ANNEXE, (libelle, "")
        else:
            sys.exit(f"article 1er, ligne {r} : libellé sans correspondance (« {libelle} »)")
        for c, nombre in valeurs.items():
            if noms.get(c) not in concepts:
                sys.exit(f"article 1er, ligne {r} : colonne « {noms.get(c)} » sans correspondance")
            yield {"tableau": i, "ligne": r, "colonne": c, "libelle": libelle, "intitule": noms[c],
                   "concept": concepts[noms[c]], "fonction": fonction, "nombre": nombre}


def lignes_article_4(tableaux):
    for i, t in enumerate(tableaux):
        if not t or not any("Désignation des missions et des programmes" in x for l in t[:3] for x in l):
            continue
        entete = next(r for r, l in enumerate(t) if any("Ouvertures" in x for x in l)) + 1
        noms, mission = colonnes(t, entete), None
        for r, ligne in enumerate(t[entete:], start=entete):
            brut = propre(ligne[0])
            valeurs = {c: nombre_texte(x) for c, x in enumerate(ligne) if c > 0 and nombre_texte(x)}
            if brut.startswith("-"):
                if mission is None:
                    sys.exit(f"article 4, tableau {i}, ligne {r} : programme hors mission (« {brut} »)")
                fonction = (brut.lstrip("- ").strip(), mission)
            elif brut == "Total":
                fonction = ""
            elif brut:
                mission, fonction = brut, (brut, "")
            else:
                continue
            for c, nombre in valeurs.items():
                if noms.get(c) not in ARTICLE_4:
                    sys.exit(f"article 4, tableau {i}, ligne {r} : colonne « {noms.get(c)} » sans correspondance")
                yield {"tableau": i, "ligne": r, "colonne": c, "libelle": brut, "intitule": noms[c],
                       "concept": ARTICLE_4[noms[c]], "fonction": fonction, "nombre": nombre}


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions et programmes."""
    chemin = BASE / fichier["chemin"]
    page = chemin.read_text(encoding="utf-8")
    titre = re.search(r"<title>(.*?)</title>", page, re.S)
    annee = re.search(r"comptes de l[’']année ([0-9]{4})", texte_html(titre.group(1) if titre else "")) or \
        re.search(r"comptes de l[’']année ([0-9]{4})", texte_html(page))
    if annee is None or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année des comptes ou date du texte introuvable")
    tableaux = lire_tableaux_html(chemin)
    for brute in list(lignes_article_1(*article_1(tableaux))) + list(lignes_article_4(tableaux)):
        fonction = ""
        if brute["fonction"]:
            libelle, mission = brute["fonction"]
            parent = f"LOLF.{code_lolf(mission)}" if mission else ""
            fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
            fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": parent})
        concept = brute["concept"]
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"tableau={brute['tableau']};ligne={brute['ligne']};colonne={brute['colonne']};"
                           f"libelle={brute['libelle']};colonne_libelle={brute['intitule']}",
            "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept, "fonction_id": fonction, "traitements": "",
            "unite_id": "EUR", "periode": annee.group(1), "valeur": brute["nombre"][0], "decimales": brute["nombre"][1],
            "statut": "non_precise" if concept in AJUSTEMENTS else "definitif", "drapeau_source": "",
            "version": fichier["mis_a_jour_source"][:10],
            "consolidation": "sans_objet" if concept in SOLDES else "non_consolide",
            "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": "",
        }
        ligne["id"] = identifiant(ligne)
        yield ligne


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    ajoutes, inchanges = fusionner(existants, list(lignes_du_fichier(fichier, fonctions)), fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
