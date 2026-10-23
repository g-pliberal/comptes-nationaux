#!/usr/bin/env python3
"""Enregistre dans la base les comptes des collectivités locales des annexes 2A à 2D des rapports de l'Observatoire
des finances et de la gestion publique locales (OFGL), à partir de la copie archivée d'un classeur xlsx.

    python3 outils/importer_ofgl.py <fichier_id>

Chaque édition présente, en milliards d'euros, sur quatre à six années :
- annexe 2A : les budgets principaux de chaque niveau de collectivités (tableaux 1 à 8 : communes, groupements de
  communes à fiscalité propre, secteur communal, départements, régions et collectivités territoriales uniques, ensemble
  des collectivités territoriales et des groupements, syndicats, ensemble y compris syndicats), et, en millions d'euros,
  ceux de chaque type de groupement pour sa dernière année (tableau 2b) ;
- annexe 2B : les budgets annexes des mêmes niveaux (tableaux B1 à B8), et, pour sa dernière année, le nombre de budgets
  principaux et annexes de chaque niveau et leurs principales dépenses (feuille « Poids des budgets annexes ») ;
- annexe 2C : les budgets principaux et annexes de chaque niveau, consolidés des flux croisés (tableaux C1 à C5) ;
- annexe 2D : le bloc communal et l'ensemble des collectivités locales, budgets principaux et annexes consolidés des flux
  croisés, entre budgets et entre niveaux (tableaux D1 et D2).
Les montants sont en opérations réelles, hors gestion active de la dette, d'après les comptes de gestion de la DGFiP.
Le tableau régionalisé de l'annexe 2D, qui ne donne que des montants par habitant, des ratios et leurs évolutions, n'est
pas lu.

Chaque titre de tableau, en-tête de colonne et libellé de ligne doit avoir une correspondance ci-dessous : un inconnu
arrête l'import, pour que rien ne soit écarté en silence. Ne sont pas enregistrés, parce que la source les calcule à partir
des montants : les taux d'évolution (colonnes « 2025 / 2024 ») et les ratios (taux d'épargne et d'endettement, délai de
désendettement, trésorerie en jours de dépenses, part des budgets annexes), ni les montants des budgets annexes de la
feuille « Poids des budgets annexes », vérifiés égaux à ceux des tableaux B1 à B8. Un en-tête d'année que les autres
tableaux de l'édition contredisent n'est corrigé que s'il figure dans ANNEES_CORRIGEES, avec une note. La version d'un
chiffre est la date de modification inscrite dans le classeur. Les montants de la colonne « Valeurs provisoires » sont
provisoires, comme ceux du tableau 2b et de la feuille « Poids des budgets annexes », qui sont de la même année ; les
autres sont définitifs. Les éditions s'importent dans l'ordre de leur parution : un montant qu'une édition reprend sans
changement n'est enregistré qu'à sa première parution.
"""

import re
import sys
import unicodedata

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, feuilles_xlsx, fusionner, identifiant, lire, lire_xlsx,
                    nombre, position, table_des_chiffres)


def forme(texte):
    """Libellé comparable d'une édition à l'autre : minuscules sans accents, espaces simples, sans renvoi de note final."""
    texte = unicodedata.normalize("NFD", str(texte).replace("’", "'"))
    texte = " ".join("".join(c for c in texte if not unicodedata.combining(c)).lower().split())
    return re.sub(r"(\s*\([a-e]\))+$", "", texte)


# Titre de chaque tableau → périmètre ; le tableau 2b a un périmètre par colonne. La première lettre du titre est celle
# de l'annexe.
TABLEAUX = {forme(t): p for t, p in {
    "A1. Communes": "COMMUNES_BP",
    "A2a. Groupements de communes à fiscalité propre": "GFP_BP",
    "A2b. Groupements de communes à fiscalité propre, par type de groupement": None,
    "A3. Secteur communal (communes, groupements à fiscalité propre)": "SECTEUR_COMMUNAL_BP",
    "A4. Départements": "DEPARTEMENTS_BP",
    "A5. Régions et collectivités territoriales uniques (CTU)": "REGIONS_CTU_BP",
    "A6. Ensemble des collectivités territoriales et de leurs groupements à fiscalité propre":
        "COLLECTIVITES_TERRITORIALES_GFP_BP",
    "A7. Syndicats": "SYNDICATS_BP",
    "A8. Les comptes des collectivités locales y compris syndicats": "COLLECTIVITES_LOCALES_BP",
    "B1. Communes": "COMMUNES_BA",
    "B2. Groupements de communes à fiscalité propre": "GFP_BA",
    "B3. Secteur communal (communes, groupements à fiscalité propre)": "SECTEUR_COMMUNAL_BA",
    "B4. Départements": "DEPARTEMENTS_BA",
    "B5. Régions et collectivités territoriales uniques (CTU)": "REGIONS_CTU_BA",
    "B6. Ensemble des collectivités territoriales et de leurs groupements à fiscalité propre":
        "COLLECTIVITES_TERRITORIALES_GFP_BA",
    "B7. Syndicats": "SYNDICATS_BA",
    "B8. Ensemble des collectivités locales (y compris syndicats)": "COLLECTIVITES_LOCALES_BA",
    "B8. Ensemble des collectivités locales (a) (y compris syndicats (b))": "COLLECTIVITES_LOCALES_BA",
    "C1. Consolidation BP et BA des communes": "COMMUNES_BP_BA",
    "C2. Consolidation BP et BA des groupements de communes à fiscalité propre": "GFP_BP_BA",
    "C3. Consolidation BP et BA des départements": "DEPARTEMENTS_BP_BA",
    "C4. Consolidation BP et BA des régions et des CTU": "REGIONS_CTU_BP_BA",
    "C5. Consolidation BP BA des syndicats": "SYNDICATS_BP_BA",
    "D1. Consolidation du bloc communal (hors syndicats)": "SECTEUR_COMMUNAL_BP_BA",
    "D2. Consolidation de l'ensemble des collectivités (y compris syndicats)": "COLLECTIVITES_LOCALES_BP_BA",
}.items()}
# Débuts de titre des feuilles qui ne sont pas lues : définitions des agrégats (annexe 2A), tableaux régionalisés de
# l'annexe 2D (montants par habitant, ratios et évolutions).
NON_LUES = tuple(forme(t) for t in ("ANNEXE : DEFINITION DES AGRÉGATS COMPTABLES", "D2 Régionalisé.", "D3 Régionalisé."))
# En-têtes d'année erronés : (source, version du classeur, feuille) → {colonne: (en-tête lu, année, note)}.
ANNEES_CORRIGEES = {
    ("ofgl.annexe-2c", "2021-06-11", "5-Synd"): {"H": (
        "2019", "2020", "L'en-tête de la colonne des valeurs provisoires porte « 2019 », comme celui de la colonne qui la "
                        "précède : ses montants sont ceux de 2020, année des valeurs provisoires des autres tableaux de "
                        "l'édition, comme le confirme l'édition suivante.")},
}
ANNEXES = {"ofgl.annexe-2a": "a", "ofgl.annexe-2b": "b", "ofgl.annexe-2c": "c", "ofgl.annexe-2d": "d"}  # source → lettre
# Feuille « Poids des budgets annexes » de l'annexe 2B : niveaux, types de budgets (None : la part des budgets annexes,
# un ratio), colonnes → (concept, unité).
POIDS = forme("Poids des budgets annexes")
POIDS_NIVEAUX = {forme(t): p for t, p in {
    "Ensemble des collectivités locales (y compris syndicats)": "COLLECTIVITES_LOCALES", "dont : Communes": "COMMUNES",
    "GFP": "GFP", "Départements": "DEPARTEMENTS", "Régions et CTU": "REGIONS_CTU", "Syndicats": "SYNDICATS"}.items()}
POIDS_BUDGETS = {forme("Budgets principaux (BP)"): "BP", forme("Budgets annexes (BA)"): "BA", forme("BA / BP (en %)"): None}
POIDS_COLONNES = {forme(t): c for t, c in {
    "Nombre de budgets": ("NOMBRE_BUDGETS", "NOMBRE"),
    "Dépenses totales (y compris remboursements d'emprunts)": ("DEP_TOTALES", "MD_EUR"),
    "Dépenses de fonctionnement": ("DEP_FONCTIONNEMENT", "MD_EUR"),
    "Dépenses d'investissement (hors rembourse-ments d'emprunts)": ("DEP_INVESTISSEMENT", "MD_EUR")}.items()}
NOTE_POIDS = ("La feuille n'indique pas l'unité de ses montants : ce sont des milliards d'euros, comme le montrent ses "
              "montants de budgets annexes, ceux des tableaux B1 à B8 à l'euro près.")
# Annexes dont les comptes sont consolidés des flux croisés : leurs dépenses et leurs recettes le sont ; leur dette et leur
# trésorerie restent la somme de celles des budgets.
CONSOLIDEES = {"ofgl.annexe-2c", "ofgl.annexe-2d"}
TYPES_DE_GROUPEMENTS = {forme(t): p for t, p in {
    "Métropoles": "GFP_METROPOLES_BP", "Communautés urbaines (CU)": "GFP_CU_BP",
    "Communautés d'agglomération (CA)": "GFP_CA_BP", "Communautés de communes (CC)": "GFP_CC_BP",
    "Ensemble des GFP": "GFP_BP"}.items()}
UNITES = {forme("(en milliards d'euros)"): "MD_EUR", forme("(en millions d'euros)"): "MIO_EUR"}

# Libellés de ligne, sous toutes leurs formes, → concept de la norme COMPTES_LOCAUX.
LIGNES = {forme(l): c for c, ls in {
    "DEP_FONCTIONNEMENT": ["DÉPENSES DE FONCTIONNEMENT (1)"],
    "ACHATS_CHARGES_EXTERNES": ["Achats et charges externes"],
    "FRAIS_PERSONNEL": ["Frais de personnel"],
    "CHARGES_FINANCIERES": ["Charges financières"],
    "DEPENSES_INTERVENTION": ["Dépenses d'intervention"],
    "AUTRES_DEP_FONCTIONNEMENT": ["Autres dépenses de fonctionnement"],
    "REC_FONCTIONNEMENT": ["RECETTES DE FONCTIONNEMENT (2)"],
    "IMPOTS_TAXES": ["Impôts et taxes"],
    "IMPOTS_LOCAUX": ["- Impôts locaux"],
    "FISCALITE_REVERSEE": ["dont : fiscalité reversée", "(Dont : fiscalité reversée)"],
    "AUTRES_IMPOTS_TAXES": ["- Autres impôts et taxes"],
    "FRACTION_TVA": ["dont : fraction de TVA"],
    "DMTO": [": DMTO", "(Dont : DMTO)"],
    "TICPE": [": TICPE", "(TICPE)", "- dont : TICPE"],
    "TSCA": [": TSCA", "(TSCA)"],
    "CARTES_GRISES": [": cartes grises", "- dont : Cartes grises"],
    "CONCOURS_ETAT": ["Concours de l'État"],
    "DGF": ["- Dotations globales de fonctionnement (DGF)", "- Dotation globale de fonctionnement (DGF)"],
    "AUTRES_DOTATIONS": ["- Autres dotations"],
    "PEREQUATIONS_COMPENSATIONS": ["- Péréquations et compensations fiscales", "- Péréquation et compensations fiscales"],
    "SUBVENTIONS_PARTICIPATIONS_RECUES": ["Subventions reçues et participations"],
    "VENTES_BIENS_SERVICES": ["Ventes de biens et services"],
    "AUTRES_REC_FONCTIONNEMENT": ["Autres recettes de fonctionnement"],
    "EPARGNE_BRUTE": ["Épargne brute (3) = (2)-(1)"],
    "EPARGNE_NETTE": ["Épargne nette = (3)-(8)"],
    "DEP_INVESTISSEMENT": ["DÉPENSES D'INVESTISSEMENT hors remboursements (4)"],
    "DEPENSES_EQUIPEMENT": ["Dépenses d'équipement"],
    "SUBVENTIONS_EQUIPEMENT_VERSEES": ["Subventions d'équipement versées"],
    "AUTRES_DEP_INVESTISSEMENT": ["Autres dépenses d'investissement"],
    "REC_INVESTISSEMENT": ["RECETTES D'INVESTISSEMENT hors emprunts (5)"],
    "FCTVA": ["FCTVA"],
    "DOTATIONS_SUBVENTIONS_INVESTISSEMENT": ["Dotations et subventions d'équipement", "Dotations et subventions d'investissement",
                                             "Autres dotations et subventions d'équipement"],
    "AUTRES_REC_INVESTISSEMENT": ["Autres recettes d'investissement"],
    "DEP_TOTALES_HORS_REMBOURSEMENTS": ["DÉPENSES TOTALES hors remboursements (6) = (1)+(4)"],
    "REC_TOTALES_HORS_EMPRUNTS": ["RECETTES TOTALES hors emprunts (7) = (2)+(5)"],
    "CAPACITE_BESOIN_FINANCEMENT": ["Capacité ou besoin de financement = (7)-(6)"],
    "REMBOURSEMENTS_DETTE": ["Remboursements de dette (8)"],
    "EMPRUNTS": ["Emprunts (9)"],
    "FLUX_NET_DETTE": ["Flux net de dette = (9)-(8)", "Flux net de dette =(9)-(8)"],
    "DEP_TOTALES": ["DÉPENSES TOTALES (10)=(6)+(8)"],
    "REC_TOTALES": ["RECETTES TOTALES (11)=(7)+(9)"],
    "VARIATION_FONDS_ROULEMENT": ["Variation du fonds de roulement = (11)-(10)"],
    "DETTE": ["Dette au 31 décembre (12)"],
    "TRESORERIE_NETTE": ["Trésorerie nette au 31 décembre (13)"],
}.items() for l in ls}
# Ratios que la source calcule à partir des montants du même tableau : non enregistrés.
RATIOS = {forme(l) for l in ["Taux d'épargne brute = (3) / (2)", "Taux d'épargne nette = [(3)-(8)] / (2)",
                             "Taux d'endettement = (12) / (2)", "Délai de désendettement = (12) / (3)",
                             "Capacité de désendettement = (12) / (3)",
                             "Trésorerie nette en jours de dépenses = (13) / (1)"]}


def grille(cellules):
    """{ligne: {colonne: valeur}}."""
    lignes = {}
    for ref, v in cellules.items():
        n, colonne = position(ref)
        lignes.setdefault(n, {})[colonne] = v
    return lignes


def rang(colonne):
    n = 0
    for lettre in colonne:
        n = n * 26 + ord(lettre) - 64
    return n


def texte(valeur):
    """Contenu d'un en-tête, une année enregistrée comme nombre redevenant « 2025 »."""
    return str(int(valeur)) if isinstance(valeur, float) and valeur.is_integer() else str(valeur)


def colonnes(nom, lignes, corrigees):
    """Les colonnes d'un tableau par niveau : {colonne: (année, provisoire, note)} pour les montants, et celles des taux
    d'évolution, dont l'en-tête est une fraction (« 2025 / 2024 »). L'en-tête d'une année peut porter un renvoi de note
    (« 2019 (e) ») ; `corrigees` donne l'année de celles dont l'en-tête est faux (voir ANNEES_CORRIGEES)."""
    annees, notes, evolutions = {}, {}, set()
    for colonne, valeur in lignes.get(3, {}).items():
        entete = " ".join(texte(valeur).split())
        if colonne == "A":
            continue
        if "/" in entete:
            evolutions.add(colonne)
            continue
        trouve = re.fullmatch(r"([0-9]{4})(?: ?\([a-e]\))*", entete)
        if trouve is None:
            sys.exit(f"{nom} : en-tête de colonne inconnu en {colonne}3 (« {entete} »)")
        annees[colonne] = trouve.group(1)
        if colonne in corrigees:
            lu, annee, note = corrigees[colonne]
            if annees[colonne] != lu:
                sys.exit(f"{nom} : l'en-tête corrigé de la colonne {colonne} n'est plus « {lu} » (« {entete} »)")
            annees[colonne], notes[colonne] = annee, note
    if len(set(annees.values())) < len(annees):
        sys.exit(f"{nom} : deux colonnes portent la même année")
    marque = [c for c, v in lignes.get(2, {}).items() if forme(v) in ("valeurs provisoires", "donnees provisoires")]
    if len(marque) != 1 or not annees:
        sys.exit(f"{nom} : colonne des valeurs provisoires ou des années introuvable")
    return {c: (a, rang(c) >= rang(marque[0]), notes.get(c, "")) for c, a in annees.items()}, evolutions


def colonnes_par_type(nom, lignes):
    """Les colonnes du tableau 2b, une par type de groupement, toutes de l'année de son titre : {colonne: (périmètre,
    en-tête)}, et cette année."""
    trouve = re.fullmatch(r"budgets principaux - ([0-9]{4})", forme(lignes.get(3, {}).get("A", "")))
    if trouve is None:
        sys.exit(f"{nom} : année du tableau introuvable en A3")
    types = {}
    for colonne, valeur in lignes[3].items():
        if colonne == "A":
            continue
        if forme(valeur) not in TYPES_DE_GROUPEMENTS:
            sys.exit(f"{nom} : type de groupement inconnu en {colonne}3 (« {' '.join(str(valeur).split())} »)")
        types[colonne] = (TYPES_DE_GROUPEMENTS[forme(valeur)], " ".join(str(valeur).split()))
    return types, trouve.group(1)


def tableau(nom, cellules):
    """Les montants d'un tableau, ligne par ligne : (concept, libellé, n° de ligne, {colonne: valeur})."""
    lignes = grille(cellules)
    for n in sorted(lignes):
        if n <= 3:
            continue
        valeurs = {c: v for c, v in lignes[n].items() if c != "A" and isinstance(v, float)}
        libelle = " ".join(str(lignes[n].get("A", "")).split())
        if not valeurs:
            continue  # intertitre, note ou ligne vide
        if forme(libelle) in RATIOS:
            continue
        if forme(libelle) == "ratios":
            # L'intertitre des ratios porte parfois des zéros égarés, qui ne sont pas des montants.
            if any(v != 0 for v in valeurs.values()):
                sys.exit(f"{nom}, ligne {n} : nombre sous l'intertitre « {libelle} »")
            continue
        if forme(libelle) not in LIGNES:
            sys.exit(f"{nom}, ligne {n} : libellé sans correspondance (« {libelle} »)")
        yield LIGNES[forme(libelle)], libelle, n, valeurs


def poids_des_budgets_annexes(nom, lignes):
    """La feuille « Poids des budgets annexes », pour l'année de son en-tête : [(périmètre, concept, unité, libellé,
    colonne, n° de ligne, valeur)], et cette année. Le niveau est écrit sur la ligne de ses budgets principaux ; la part
    des budgets annexes n'est pas lue."""
    entete = lignes.get(3, {})
    if forme(entete.get("A", "")) != "exercice" or not re.fullmatch(r"20[0-9]{2}", texte(entete.get("B", ""))):
        sys.exit(f"{nom} : année de la feuille introuvable en B3")
    colonnes = {}
    for colonne, valeur in entete.items():
        if colonne in ("A", "B"):
            continue
        if forme(valeur) not in POIDS_COLONNES:
            sys.exit(f"{nom} : colonne inconnue en {colonne}3 (« {' '.join(str(valeur).split())} »)")
        colonnes[colonne] = POIDS_COLONNES[forme(valeur)]
    niveau, resultat = None, []
    for n in sorted(lignes):
        if n <= 3:
            continue
        valeurs = {c: v for c, v in lignes[n].items() if c in colonnes and isinstance(v, float)}
        if forme(lignes[n].get("A", "")) in POIDS_NIVEAUX:
            niveau = (" ".join(str(lignes[n]["A"]).split()), POIDS_NIVEAUX[forme(lignes[n]["A"])])
        elif valeurs and lignes[n].get("A") not in (None, ""):
            sys.exit(f"{nom}, ligne {n} : niveau inconnu (« {lignes[n]['A']} »)")
        if not valeurs:
            continue  # source
        budgets = POIDS_BUDGETS.get(forme(lignes[n].get("B", "")), "?")
        if budgets == "?" or niveau is None:
            sys.exit(f"{nom}, ligne {n} : type de budgets inconnu (« {lignes[n].get('B', '')} »)")
        if budgets is None:
            continue  # part des budgets annexes
        libelle = f"{niveau[0]} / {' '.join(str(lignes[n]['B']).split())}"
        for colonne, v in sorted(valeurs.items()):
            concept, unite = colonnes[colonne]
            resultat.append((f"{niveau[1]}_{budgets}", concept, unite, libelle, colonne, n, v))
    return resultat, texte(entete["B"])


def lignes_du_fichier(fichier):
    """Les chiffres d'une copie archivée d'une annexe, tableau par tableau."""
    lettre = ANNEXES.get(fichier["source_id"])
    if lettre is None:
        sys.exit(f"{fichier['id']} : source non prise en charge")
    version = fichier["mis_a_jour_source"][:10]
    if not version:
        sys.exit(f"{fichier['id']} : date du classeur absente, version inconnue")
    chemin = BASE / fichier["chemin"]
    sens = {c["id"]: c["sens"] for c in lire("tables/concepts.csv")}
    consolidee = fichier["source_id"] in CONSOLIDEES

    def chiffre(nom, cellule, libelle, lieu, perimetre, concept, unite, annee, valeur, decimales, provisoire, note=""):
        concept_id = f"COMPTES_LOCAUX.{concept}"
        consolidation = {"solde": "sans_objet", "stock": "non_consolide"}.get(
            sens[concept_id], "consolide" if consolidee else "non_consolide")
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"feuille={nom};cellule={cellule};ligne={libelle};{lieu}",
            "zone": "FR", "perimetre_id": perimetre, "concept_id": concept_id, "fonction_id": "", "traitements": "",
            "unite_id": unite, "periode": annee, "valeur": nombre(valeur)[0], "decimales": decimales,
            "statut": "provisoire" if provisoire else "definitif", "drapeau_source": "", "version": version,
            "consolidation": consolidation, "denominateur_id": "", "nature": "publie", "calcul_id": "",
            "saisi_le": aujourdhui(), "notes": note,
        }
        ligne["id"] = identifiant(ligne)
        return ligne

    resultat, poids = [], []  # la feuille du poids des budgets annexes se lit après les tableaux B1 à B8
    for nom in feuilles_xlsx(chemin):
        _, cellules = lire_xlsx(chemin, nom)
        if not cellules:
            continue  # feuille vide
        lignes = grille(cellules)
        titre = forme(lignes.get(1, {}).get("A", ""))
        if titre.startswith(NON_LUES):
            continue
        if titre == POIDS and lettre == "b":
            # L'année de la feuille est la dernière de l'édition, celle des valeurs provisoires.
            montants, annee = poids_des_budgets_annexes(nom, lignes)
            for colonne in sorted({m[4] for m in montants}):
                decimales = max(nombre(m[6])[1] for m in montants if m[4] == colonne)
                for perimetre, concept, unite, libelle, c, n, v in (m for m in montants if m[4] == colonne):
                    poids.append(chiffre(nom, f"{c}{n}", libelle, f"annee={annee}", perimetre, concept, unite, annee,
                                            v, decimales, True, NOTE_POIDS if unite == "MD_EUR" else ""))
            continue
        if titre not in TABLEAUX or not titre.startswith(lettre):
            sys.exit(f"{nom} : titre de tableau inconnu (« {lignes.get(1, {}).get('A', '')} »)")
        unite = UNITES.get(forme(lignes.get(2, {}).get("A", "")))
        if unite is None:
            sys.exit(f"{nom} : unité des montants introuvable en A2")
        perimetre = TABLEAUX[titre]
        if perimetre is None:
            types, annee = colonnes_par_type(nom, lignes)
            lieux = {c: (p, annee, True, f"colonne={entete};annee={annee}", "") for c, (p, entete) in types.items()}
            evolutions = set()
        else:
            annees, evolutions = colonnes(nom, lignes, ANNEES_CORRIGEES.get((fichier["source_id"], version, nom), {}))
            lieux = {c: (perimetre, a, provisoire, f"annee={a}", note) for c, (a, provisoire, note) in annees.items()}
        for concept, libelle, n, valeurs in tableau(nom, cellules):
            valeurs = {c: v for c, v in valeurs.items() if c not in evolutions}
            if not valeurs:
                continue  # taux d'évolution seulement
            inconnues = set(valeurs) - set(lieux)
            if inconnues:
                sys.exit(f"{nom}, ligne {n} : montant hors des colonnes reconnues ({', '.join(sorted(inconnues))})")
            # Les montants sont arrondis à l'euro : la précision d'une ligne est celle de sa valeur la plus précise.
            decimales = max(nombre(v)[1] for v in valeurs.values())
            for colonne, v in sorted(valeurs.items()):
                perimetre_, annee, provisoire, lieu, note = lieux[colonne]
                resultat.append(chiffre(nom, f"{colonne}{n}", libelle, lieu, perimetre_, concept, unite, annee, v,
                                        decimales, provisoire, note))
    # Les montants de budgets annexes de la feuille du poids des budgets annexes sont ceux des tableaux B1 à B8, à l'euro
    # près de leurs arrondis : ils ne sont pas enregistrés une seconde fois, mais l'import vérifie qu'ils concordent, ce
    # qui établit l'unité de la feuille. Restent ses montants de budgets principaux et ses nombres de budgets.
    tableaux = {l["id"]: l for l in resultat}
    for l in poids:
        if l["perimetre_id"].endswith("_BA") and l["unite_id"] == "MD_EUR":
            repris = tableaux.get(l["id"])
            if repris is None or abs(float(repris["valeur"]) - float(l["valeur"])) > 1.5e-9:
                sys.exit(f"{l['emplacement']} : montant différent de celui des tableaux B1 à B8")
    return resultat + [l for l in poids if not (l["perimetre_id"].endswith("_BA") and l["unite_id"] == "MD_EUR")]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, lignes_du_fichier(fichier), fichier["id"])
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
