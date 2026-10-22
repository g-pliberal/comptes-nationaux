#!/usr/bin/env python3
"""Enregistre dans la base les chiffres d'un tableau des comptes nationaux de l'Insee archivé (classeur xlsx).

    python3 outils/importer_insee.py <fichier_id>

Tableaux pris en charge :
- 3.201 à 3.214 : dépenses et recettes par nature, pour l'ensemble des administrations publiques et
  chacun de leurs sous-secteurs, jusqu'aux communes, départements, régions et syndicats ;
- 3.106 : déficit au sens de Maastricht par sous-secteur, et PIB utilisé pour le ratio ;
- 3.101 : dette au sens de Maastricht par sous-secteur, et PIB utilisé pour le ratio.

Chaque libellé de ligne doit avoir une correspondance ci-dessous : une ligne inconnue arrête l'import,
pour que rien ne soit écarté en silence. La version d'un chiffre est la date de modification que
l'Insee inscrit dans le classeur. Son statut suit le calendrier des comptes annuels de l'Insee : la
dernière année publiée est provisoire, l'avant-dernière semi-définitive, les précédentes définitives.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, ecrire, feuilles_xlsx, fusionner, identifiant, lire, lire_xlsx,
                    nombre, position)

CIBLE = "tables/chiffres/insee.csv"

PERIMETRES_32XX = {"3201": "S13", "3202": "S1311", "3203": "S13111", "3204": "S13112", "3205": "S1313",
                   "3206": "S13131", "3207": "S131311", "3208": "S131312", "3209": "S131313",
                   "3210": "S131314", "3211": "S13132", "3212": "S1314", "3213": "S13141", "3214": "S13142"}

# Lignes des tableaux 3.201 à 3.214 : (section, libellé de l'Insee) → concept de la base.
LIGNES_32XX = {
    ("DEPENSES", "Dépenses de fonctionnement"): "INSEE_APU.DEP_FONCTIONNEMENT",
    ("DEPENSES", "Consommation intermédiaire (P2)"): "SEC2010.P2",
    ("DEPENSES", "Rémunération des salariés (D1)"): "SEC2010.D1PAY",
    ("DEPENSES", "Autres impôts sur la production (D29)"): "SEC2010.D29PAY",
    ("DEPENSES", "Revenus de la propriété autres que les intérêts (D4 hors D41)"): "SEC2010.D4_HORS_D41PAY",
    ("DEPENSES", "Impôts courants sur le revenu et le patrimoine (D5)"): "SEC2010.D5PAY",
    ("DEPENSES", "Intérêts (D41)"): "SEC2010.D41PAY",
    ("DEPENSES", "Intérêts hors correction au titre des services d'intermédiation financière indirectement "
                 "mesurés (D41G)"): "SEC2010.D41GPAY",
    ("DEPENSES", "Prestations et autres transferts"): "INSEE_APU.DEP_PRESTATIONS_TRANSFERTS",
    ("DEPENSES", "Prestations sociales autres que transferts sociaux en nature (D62)"): "SEC2010.D62PAY",
    ("DEPENSES", "Transferts sociaux en nature de produits marchands (D632)"): "SEC2010.D632PAY",
    ("DEPENSES", "Subventions (D3)"): "SEC2010.D3PAY",
    ("DEPENSES", "Transferts courants entre administrations publiques (D73)"): "SEC2010.D73PAY",
    ("DEPENSES", "Autres transferts courants (D7 hors D73)"): "SEC2010.D7_HORS_D73PAY",
    ("DEPENSES", "Transferts en capital à payer (D9p hors D995p)"): "SEC2010.D9_HORS_D995PAY",
    ("DEPENSES", "Acquisitions moins cessions d'actifs non financiers"): "INSEE_APU.DEP_ACTIFS_NON_FINANCIERS",
    ("DEPENSES", "Formation brute de capital fixe (P51g)"): "SEC2010.P51G",
    ("DEPENSES", "Autres acquisitions moins cessions d'actifs non financiers (P52, P53, NP)"): "SEC2010.P52_P53_NP",
    ("DEPENSES", "Total des dépenses"): "SEC2010.TE",
    ("DEPENSES", "dont (a) - Cotisations sociales imputées (D122)"): "SEC2010.D122PAY",
    ("DEPENSES", "dont (b) - Capitalisation de la production pour emploi final propre (P51g)"):
        "INSEE_APU.DEP_PRODUCTION_COMPTE_PROPRE",
    ("DEPENSES", "dont (c) - Crédits d'impôts enregistrés en dépenses (**)"): "INSEE_APU.DEP_CREDITS_IMPOT",
    ("DEPENSES", "Dépenses hors éléments imputés (a, b et c) (***)"): "INSEE_APU.DEP_HORS_ELEMENTS_IMPUTES",
    ("RECETTES", "Recettes de production"): "INSEE_APU.REC_PRODUCTION",
    ("RECETTES", "Production des branches marchandes et ventes résiduelles (P11)"): "SEC2010.P11",
    ("RECETTES", "Production pour emploi final propre (P12)"): "SEC2010.P12",
    ("RECETTES", "Paiements partiels des ménages (partie du P13)"): "INSEE_APU.REC_PAIEMENTS_PARTIELS",
    ("RECETTES", "Autres subventions sur la production (D39)"): "SEC2010.D39REC",
    ("RECETTES", "Revenus de la propriété"): "INSEE_APU.REC_REVENUS_PROPRIETE",
    ("RECETTES", "Intérêts (D41)"): "SEC2010.D41REC",
    ("RECETTES", "Intérêts hors correction au titre des services d'intermédiation financière indirectement "
                 "mesurés (D41G)"): "SEC2010.D41GREC",
    ("RECETTES", "Revenus de la propriété autres que les intérêts (D4 hors D41)"): "SEC2010.D4_HORS_D41REC",
    ("RECETTES", "Impôts et cotisations sociales"): "INSEE_APU.REC_IMPOTS_COTISATIONS",
    ("RECETTES", "Impôts sur la production et les importations (D2)"): "SEC2010.D2REC",
    ("RECETTES", "Impôts courants sur le revenu et le patrimoine (D5)"): "SEC2010.D5REC",
    ("RECETTES", "Impôts en capital à recevoir (D91r)"): "SEC2010.D91REC",
    ("RECETTES", "Transferts de recettes fiscales (D733)"): "SEC2010.D733REC",
    ("RECETTES", "Cotisations sociales nettes (D61)"): "SEC2010.D61REC",
    ("RECETTES", "Impôts et cotisations dus non recouvrables nets (D995r)"): "SEC2010.D995REC",
    ("RECETTES", "Autres transferts"): "INSEE_APU.REC_AUTRES_TRANSFERTS",
    ("RECETTES", "Transferts courants entre administrations publiques (D73 hors D733)"): "SEC2010.D73_HORS_D733REC",
    ("RECETTES", "Autres transferts courants (D7 hors D73)"): "SEC2010.D7_HORS_D73REC",
    ("RECETTES", "Transferts en capital (D9r hors D91r, D995r)"): "SEC2010.D9_HORS_D91_D995REC",
    ("RECETTES", "Total des recettes"): "SEC2010.TR",
    ("RECETTES", "dont (a) - Cotisations sociales imputées (D612)"): "SEC2010.D612REC",
    ("RECETTES", "dont (b) - Production pour emploi final propre (P12)"): "SEC2010.P12",
    ("RECETTES", "dont (c') - Crédits d'impôts enregistrés en recettes (**)"): "INSEE_APU.REC_CREDITS_IMPOT",
    ("RECETTES", "Recettes hors éléments imputés (a,b et c') (***)"): "INSEE_APU.REC_HORS_ELEMENTS_IMPUTES",
    ("SOLDES", "Epargne brute (B8g)"): "SEC2010.B8G",
    ("SOLDES", "Capacité (+) ou besoin (-) de financement (B9NF)"): "SEC2010.B9",
}

SECTEURS = {"S13", "S1311", "S13111", "S13112", "S1313", "S1314"}


def libelle(cellules, colonne, n):
    return " ".join(str(cellules.get(f"{colonne}{n}", "")).split())


def entete_des_annees(cellules):
    """Colonne → année, d'après la première ligne qui contient une suite d'années."""
    lignes = {}
    for ref, valeur in cellules.items():
        texte = str(int(valeur)) if isinstance(valeur, float) and valeur.is_integer() else str(valeur).strip()
        if re.fullmatch(r"(19|20)[0-9]{2}", texte):
            n, colonne = position(ref)
            lignes.setdefault(n, {})[colonne] = texte
    n = min(n for n, annees in lignes.items() if len(annees) >= 3)
    return lignes[n]


def valeurs_de_la_ligne(cellules, n, annees):
    """Valeurs numériques d'une ligne, par colonne ; vide pour une ligne d'en-tête qui répète les années."""
    valeurs = {colonne: cellules[f"{colonne}{n}"] for colonne in annees if isinstance(cellules.get(f"{colonne}{n}"), float)}
    if valeurs and all(v.is_integer() and str(int(v)) == annees[colonne] for colonne, v in valeurs.items()):
        return {}
    return valeurs


def tableau_32xx(numero, cellules, annees):
    perimetre, section = PERIMETRES_32XX[numero], None
    for n in sorted({position(ref)[0] for ref in cellules}):
        texte = libelle(cellules, "B", n)
        if texte.upper() in ("DEPENSES", "RECETTES", "SOLDES"):
            section = texte.upper()
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs or section is None:
            continue
        concept = LIGNES_32XX.get((section, texte))
        if concept is None:
            sys.exit(f"tableau {numero}, ligne {n} : libellé sans correspondance ({section}, « {texte} »)")
        for colonne, valeur in valeurs.items():
            yield {"perimetre_id": perimetre, "concept_id": concept, "unite_id": "MD_EUR", "valeur": valeur,
                   "cellule": f"{colonne}{n}", "libelle": texte, "annee": annees[colonne],
                   "consolidation": "consolide", "ratio": False}


def tableau_dette_ou_deficit(numero, cellules, annees):
    """Tableaux 3.101 (dette) et 3.106 (déficit) : une ligne par sous-secteur, en Md€ puis en % du PIB."""
    concept = {"3101": "PDE.GD", "3106": "SEC2010.B9"}[numero]
    consolidation = {"3101": "consolide", "3106": "sans_objet"}[numero]
    unite = None
    for n in sorted({position(ref)[0] for ref in cellules}):
        code, texte = libelle(cellules, "A", n), libelle(cellules, "B", n)
        if texte.startswith("En milliards"):
            unite = "MD_EUR"
            continue
        if texte.startswith("En % du produit intérieur brut"):
            unite = "PC_PIB"
            continue
        valeurs = valeurs_de_la_ligne(cellules, n, annees)
        if not valeurs:
            continue
        if texte.startswith(("Série de PIB", "Série du PIB")):
            ligne = {"perimetre_id": "S1", "concept_id": "SEC2010.B1GQ", "unite_id": "MD_EUR",
                     "consolidation": "sans_objet", "ratio": False}
        else:
            secteur = code or texte.split(" - ")[0]
            if secteur not in SECTEURS or unite is None:
                sys.exit(f"tableau {numero}, ligne {n} : ligne non reconnue (« {code} », « {texte} »)")
            ligne = {"perimetre_id": secteur, "concept_id": concept, "unite_id": unite,
                     "consolidation": consolidation, "ratio": unite == "PC_PIB"}
        for colonne, valeur in valeurs.items():
            yield {**ligne, "valeur": valeur, "cellule": f"{colonne}{n}", "libelle": texte, "annee": annees[colonne]}


def statut(annee, derniere):
    return {derniere: "provisoire", derniere - 1: "semi_definitif"}.get(annee, "definitif")


def lignes_du_fichier(fichier):
    numero = fichier["source_id"].removeprefix("insee.t")
    version = fichier["mis_a_jour_source"][:10]
    if not version:
        sys.exit(f"{fichier['id']} : date de modification du classeur absente, version inconnue")
    chemin = BASE / fichier["chemin"]
    # La feuille de données est la première qui n'est pas une feuille de métadonnées (tableau 3.101).
    nom = next(f for f in feuilles_xlsx(chemin) if f.strip().lower() != "métadonnées")
    nom, cellules = lire_xlsx(chemin, nom)
    annees = entete_des_annees(cellules)
    derniere = max(int(a) for a in annees.values())
    if numero in PERIMETRES_32XX:
        brutes = tableau_32xx(numero, cellules, annees)
    elif numero in ("3101", "3106"):
        brutes = tableau_dette_ou_deficit(numero, cellules, annees)
    else:
        sys.exit(f"tableau {numero} non pris en charge")
    brutes = list(brutes)
    # Un zéro est exact : il prend la précision de sa ligne, celle de la valeur la plus précise de la ligne.
    precision = {}
    for brute in brutes:
        n = position(brute["cellule"])[0]
        precision[n] = max(precision.get(n, 0), nombre(brute["valeur"])[1])
    for brute in brutes:
        texte, decimales = nombre(brute["valeur"])
        if float(texte) == 0:
            decimales = precision[position(brute["cellule"])[0]]
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"feuille={nom};cellule={brute['cellule']};ligne={brute['libelle']};annee={brute['annee']}",
            "zone": "FR", "perimetre_id": brute["perimetre_id"], "concept_id": brute["concept_id"],
            "fonction_id": "", "traitements": "", "unite_id": brute["unite_id"], "periode": brute["annee"],
            "valeur": texte, "decimales": decimales, "statut": statut(int(brute["annee"]), derniere),
            "drapeau_source": "", "version": version, "consolidation": brute["consolidation"],
            "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": "",
        }
        if brute["ratio"]:  # le PIB utilisé pour le ratio figure dans le même tableau
            ligne["denominateur_id"] = identifiant({**ligne, "perimetre_id": "S1", "concept_id": "SEC2010.B1GQ",
                                                    "unite_id": "MD_EUR"})
        ligne["id"] = identifiant(ligne)
        yield ligne


def resoudre_denominateurs(existants):
    """Un PIB inchangé d'une version à l'autre n'est enregistré qu'une fois : le dénominateur d'un ratio
    renvoie alors à la version la plus récente du PIB qui précède celle du ratio."""
    for ligne in existants.values():
        d = ligne["denominateur_id"]
        if d and d not in existants:
            prefixe = d.rsplit(":", 1)[0] + ":"
            candidats = [i for i in existants if i.startswith(prefixe) and i.rsplit(":", 1)[1] <= ligne["version"]]
            ligne["denominateur_id"] = max(candidats, key=lambda i: i.rsplit(":", 1)[1]) if candidats else d


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    existants = {l["id"]: l for l in lire(CIBLE)}
    ajoutes, inchanges = fusionner(existants, lignes_du_fichier(fichier), fichier["id"])
    resoudre_denominateurs(existants)
    ecrire(CIBLE, champs("chiffres-insee"), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {CIBLE} en compte {len(existants)}")


if __name__ == "__main__":
    main()
