#!/usr/bin/env python3
"""Enregistre dans la base les comptes de chaque département et de chaque région que publie la Direction générale des
collectivités locales (DGCL) dans « Les finances des départements » et « Les finances des régions », à partir de la
copie archivée d'un classeur xlsx annuel.

    python3 outils/importer_dgcl.py <fichier_id>

Chaque classeur donne, pour une année, les comptes de gestion de chaque collectivité, budget principal, en opérations
réelles et hors gestion active de la dette, en millions d'euros à leur précision d'origine (le centime), et leurs
totaux. L'import lit les tableaux T01 à T06, T09 et T10.1 : dépenses et recettes de fonctionnement et d'investissement,
leur détail par nature, emprunts, remboursements, intérêts et encours de la dette, soldes de gestion. Il ne lit pas les
prélèvements et reversements de fiscalité (T07, T08), les dépenses par fonction (T11, T12), ni les ratios et les données
de contexte (T10.2, T13 et suivants). Dans les tableaux lus, les montants par habitant, les parts et les évolutions, que
la source calcule à partir des montants, ne sont pas enregistrés.

Chaque titre de tableau, en-tête de colonne et ligne doit avoir une correspondance ci-dessous, et chaque collectivité
le nom de son code : un inconnu arrête l'import. Les recettes de fonctionnement, charges financières et remboursements
de dette que les soldes de gestion (T10.1) reprennent des tableaux T02, T03.2 et T09 ne sont lus que dans ceux-ci : les
identités des soldes, au rapport de cohérence, montrent si les deux présentations diffèrent. Les collectivités de Corse,
de Martinique et de Guyane figurent dans les deux publications, sous le même périmètre. La version d'un chiffre est la date de modification inscrite dans le classeur ;
ce sont des comptes de gestion, définitifs.
"""

import re
import sys
import unicodedata

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_xlsx, nombre, position,
                    table_des_chiffres)


def forme(texte):
    """Texte comparable d'un classeur à l'autre : minuscules sans accents, espaces simples."""
    texte = unicodedata.normalize("NFD", str(texte).replace("’", "'"))
    return " ".join("".join(c for c in texte if not unicodedata.combining(c)).lower().split())


# Les collectivités, sous leur code et leur nom dans la source → périmètre. « 69D » est le Rhône, hors métropole de Lyon ;
# la Collectivité européenne d'Alsace (« 67A ») réunit depuis 2021 le Bas-Rhin et le Haut-Rhin.
DEPARTEMENTS = {"01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes",
                "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes", "09": "Ariège", "10": "Aube", "11": "Aude",
                "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal", "16": "Charente",
                "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "21": "Côte-d'Or", "22": "Côtes-d'Armor",
                "23": "Creuse", "24": "Dordogne", "25": "Doubs", "26": "Drôme", "27": "Eure", "28": "Eure-et-Loir",
                "29": "Finistère", "30": "Gard", "31": "Haute-Garonne", "32": "Gers", "33": "Gironde", "34": "Hérault",
                "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire", "38": "Isère", "39": "Jura",
                "40": "Landes", "41": "Loir-et-Cher", "42": "Loire", "43": "Haute-Loire", "44": "Loire-Atlantique",
                "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", "49": "Maine-et-Loire",
                "50": "Manche", "51": "Marne", "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle",
                "55": "Meuse", "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord", "60": "Oise",
                "61": "Orne", "62": "Pas-de-Calais", "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques",
                "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin",
                "69D": "Rhône", "70": "Haute-Saône", "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie",
                "74": "Haute-Savoie", "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines",
                "79": "Deux-Sèvres", "80": "Somme", "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse",
                "85": "Vendée", "86": "Vienne", "87": "Haute-Vienne", "88": "Vosges", "89": "Yonne",
                "90": "Territoire de Belfort", "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis",
                "94": "Val-de-Marne", "95": "Val-d'Oise", "971": "Guadeloupe", "974": "La Réunion", "976": "Mayotte"}
REGIONS = {"84": "Auvergne-Rhône-Alpes", "27": "Bourgogne-Franche-Comté", "53": "Bretagne", "24": "Centre-Val de Loire",
           "44": "Grand Est", "32": "Hauts-de-France", "11": "Île-de-France", "28": "Normandie",
           "75": "Nouvelle-Aquitaine", "76": "Occitanie", "52": "Pays de la Loire", "93": "Provence-Alpes-Côte d'Azur",
           "01": "Guadeloupe", "04": "La Réunion"}
PARTICULIERES = {"COLLECTIVITE_DE_CORSE_BP": "Corse", "CTU_MARTINIQUE_BP": "Martinique", "CTU_GUYANE_BP": "Guyane",
                 "CEA_BP": "Collectivité europ. d'Alsace", "METROPOLE_LYON_BP": "Métropole de Lyon",
                 "VILLE_DE_PARIS_BP": "Ville de Paris"}
PUBLICATIONS = {
    "dgcl.finances-departements": {
        "qui": "departements",
        "collectivites": {**{c: (f"DEP_{c.rstrip('D')}_BP", n) for c, n in DEPARTEMENTS.items()},
                          **{c: (p, PARTICULIERES[p]) for c, p in {
                              "20": "COLLECTIVITE_DE_CORSE_BP", "972": "CTU_MARTINIQUE_BP", "973": "CTU_GUYANE_BP",
                              "67A": "CEA_BP", "69M": "METROPOLE_LYON_BP", "75": "VILLE_DE_PARIS_BP"}.items()}},
        "totaux": {forme(t): p for t, p in {
            "Total hors DOM": "DEPARTEMENTS_METROPOLE_BP", "Outre-mer": "DEPARTEMENTS_OUTRE_MER_BP",
            "Total": "DEPARTEMENTS_BP", "Total départements et CTU": "DEPARTEMENTS_CTU_BP"}.items()}},
    "dgcl.finances-regions": {
        "qui": "regions",
        "collectivites": {**{c: (f"REG_{c}_BP", n) for c, n in REGIONS.items()},
                          **{c: (p, PARTICULIERES[p]) for c, p in {
                              "94": "COLLECTIVITE_DE_CORSE_BP", "02": "CTU_MARTINIQUE_BP",
                              "03": "CTU_GUYANE_BP"}.items()}},
        "totaux": {forme(t): p for t, p in {
            "Fce métropolitaine hors ÎdF et Corse": "REGIONS_METROPOLE_HORS_IDF_BP",
            "France métropolitaine hors Corse": "REGIONS_METROPOLE_BP", "Outre-mer hors 02 et 03": "REGIONS_OUTRE_MER_BP",
            "Total": "REGIONS_BP", "TOTAL régions et CTU": "REGIONS_CTU_BP"}.items()}},
}

# Tableaux lus, et leur titre (« {} » : « départements » ou « régions »).
TABLEAUX = {"T01": "T01 - Les dépenses des {} (1)", "T02": "T02 - Les recettes des {} (1)",
            "T03.1": "T03.1 - Ventilation des dépenses de fonctionnement par nature (1/2)",
            "T03.2": "T03.2 - Ventilation des dépenses de fonctionnement par nature (2/2)",
            "T04.1": "T04.1 - Ventilation des recettes de fonctionnement par nature (1/2)",
            "T04.2": "T04.2 - Ventilation des recettes de fonctionnement par nature (2/2)",
            "T05": "T05 - Ventilation des dépenses d'investissement par nature",
            "T06": "T06 - Ventilation des recettes d'investissement par nature",
            "T09": "T09 - Emprunts et endettement", "T10.1": "T10.1 - Soldes de gestion et indicateurs (1/2)"}
# Colonnes en millions d'euros : (tableau, intitulé du groupe de colonnes, sous-titre) → concept de la norme
# COMPTES_LOCAUX, ou None pour un montant repris d'un autre tableau. Le sous-titre est vide pour le montant de l'année,
# « dont … » pour une de ses parties.
COLONNES = {(t, forme(g), forme(s)): c for (t, g, s), c in {
    ("T01", "Dépenses totales", ""): "DEP_TOTALES_HORS_REMBOURSEMENTS",
    ("T01", "Dépenses réelles totales", ""): "DEP_TOTALES_HORS_REMBOURSEMENTS",
    ("T01", "Dépenses de fonctionnement", ""): "DEP_FONCTIONNEMENT",
    ("T01", "Dépenses d'investissement", ""): "DEP_INVESTISSEMENT",
    ("T02", "Recettes réelles totales", ""): "REC_TOTALES_HORS_EMPRUNTS",
    ("T02", "Recettes de fonctionnement", ""): "REC_FONCTIONNEMENT",
    ("T02", "Recettes d'investissement", ""): "REC_INVESTISSEMENT",
    ("T03.1", "Charges de personnel (1)", ""): "FRAIS_PERSONNEL",
    ("T03.1", "Achats et charges externes (2)", ""): "ACHATS_CHARGES_EXTERNES",
    ("T03.2", "Dépenses d'intervention (1)", ""): "DEPENSES_INTERVENTION",
    ("T03.2", "Charges financières (2)", ""): "CHARGES_FINANCIERES",
    ("T03.2", "Charges financières (2)", "dont intérêt de la dette"): "INTERETS_DETTE",
    ("T03.2", "Autres (3)", ""): "AUTRES_DEP_FONCTIONNEMENT",
    ("T04.1", "Impôts locaux (1)", ""): "IMPOTS_LOCAUX",
    ("T04.1", "Autres impôts et taxes (2)", ""): "AUTRES_IMPOTS_TAXES",
    ("T04.1", "Autres impôts et taxes (2)", "dont DMTO"): "DMTO",
    ("T04.1", "Autres impôts et taxes (2)", "dont TSCA"): "TSCA",
    ("T04.1", "Autres impôts et taxes (2)", "dont TICPE"): "TICPE",
    ("T04.1", "Autres impôts et taxes (2)", "dont cartes grises"): "CARTES_GRISES",
    ("T04.2", "Concours de l'Etat (1)", ""): "CONCOURS_ETAT",
    ("T04.2", "Concours de l'Etat (1)", "dont DGF"): "DGF",
    ("T04.2", "Concours de l'Etat (1)", "dont PCF"): "PEREQUATIONS_COMPENSATIONS",
    ("T04.2", "Concours de l'Etat (1)", "dont autres dotations"): "AUTRES_DOTATIONS",
    ("T04.2", "Subventions reçues et participations (2)", ""): "SUBVENTIONS_PARTICIPATIONS_RECUES",
    ("T04.2", "Ventes de biens et services (3)", ""): "VENTES_BIENS_SERVICES",
    ("T04.2", "Autres (4)", ""): "AUTRES_REC_FONCTIONNEMENT",
    ("T05", "Dépenses d'équipement (1)", ""): "DEPENSES_EQUIPEMENT",
    ("T05", "Subventions d'équipement (2)", ""): "SUBVENTIONS_EQUIPEMENT_VERSEES",
    ("T05", "Autres (3)", ""): "AUTRES_DEP_INVESTISSEMENT",
    ("T06", "Dotations, subventions et fonds divers (1)", ""): "DOTATIONS_SUBVENTIONS_INVESTISSEMENT",
    ("T06", "FCTVA (2)", ""): "FCTVA",
    ("T06", "Autres (3)", ""): "AUTRES_REC_INVESTISSEMENT",
    ("T09", "Remboursement de dette (1)", ""): "REMBOURSEMENTS_DETTE",
    ("T09", "Produits des emprunts (2)", ""): "EMPRUNTS",
    ("T09", "Dette au 31/12 (3)", ""): "DETTE",
    ("T09", "Dette au 31/12/AAAA", ""): "DETTE",
    ("T09", "Dette au 31/12/AAAA (3)", ""): "DETTE",
    ("T09", "Annuité de la dette (3)", ""): "ANNUITE_DETTE",
    ("T10.1", "Dépenses de gestion (1) (a)", ""): "DEPENSES_GESTION",
    ("T10.1", "Recettes de fonctionnement (b)", ""): None,
    ("T10.1", "Recettes de fonctionne- ment (b)", ""): None,
    ("T10.1", "Epargne de gestion (c) = (b) - (a)", ""): "EPARGNE_GESTION",
    ("T10.1", "Epargne de gestion (c ) = (b) - (a)", ""): "EPARGNE_GESTION",
    ("T10.1", "Charges financières (d)", ""): None,
    ("T10.1", "Charges financières ( d )", ""): None,
    ("T10.1", "Epargne brute (e) = (c) - (d)", ""): "EPARGNE_BRUTE",
    ("T10.1", "Rembour- sement de dette (f)", ""): None,
    ("T10.1", "Rembourse- ment de dette (f)", ""): None,
    ("T10.1", "Rembourse-ment de dette (f)", ""): None,
    ("T10.1", "Epargne nette (e) - (f)", ""): "EPARGNE_NETTE",
}.items()}
NON_LUES = {"€/h", "%", "(%)"}  # montants par habitant et parts


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
    """Contenu d'une cellule d'en-tête, une année enregistrée comme nombre redevenant « 2024 »."""
    return str(int(valeur)) if isinstance(valeur, float) and valeur.is_integer() else " ".join(str(valeur).split())


def colonnes(nom, lignes, annee):
    """Les colonnes de montants d'un tableau : {colonne: (concept, intitulé, note)}. L'intitulé d'un groupe de colonnes
    (ligne 3) vaut pour les colonnes vides qui le suivent ; la ligne 4 donne l'année ou « dont … », la ligne 5 l'unité."""
    resultat, groupe = {}, ""
    for colonne in sorted({c for n in (3, 4, 5) for c in lignes.get(n, {})} - {"A"}, key=rang):
        if lignes.get(3, {}).get(colonne) not in (None, ""):
            groupe = texte(lignes[3][colonne])
        sous, unite = texte(lignes.get(4, {}).get(colonne, "")), forme(lignes.get(5, {}).get(colonne, ""))
        if forme(sous).startswith(("evolution", "variation")) or unite in NON_LUES:
            continue
        donnees = any(isinstance(lignes[n].get(colonne), float) for n in lignes if n > 5)
        if unite == "" and not donnees:
            continue  # colonne vide
        if unite != "m€":
            sys.exit(f"{nom} : colonne {colonne} d'unité inconnue (« {unite} »)")
        if sous not in ("", annee) and not forme(sous).startswith("dont"):
            sys.exit(f"{nom} : colonne {colonne} d'une autre année que {annee} (« {sous} »)")
        # L'intitulé de la colonne de la dette peut porter une autre année que celle du classeur : la ligne des années
        # et les montants sont ceux de l'année du classeur.
        an = re.search(r"\b(20[0-9]{2})\b", groupe)
        note = ""
        if an and an.group(1) != annee:
            if not forme(groupe).startswith("dette au 31/12"):
                sys.exit(f"{nom} : colonne {colonne} d'une autre année que {annee} (« {groupe} »)")
            note = (f"L'intitulé de la colonne porte « {groupe} », mais la ligne des années indique {annee} : le "
                    f"montant est celui du 31 décembre {annee}.")
        cle = (nom, forme(re.sub(r"\b20[0-9]{2}\b", "AAAA", groupe)), "" if sous == annee else forme(sous))
        if cle not in COLONNES:
            sys.exit(f"{nom} : colonne {colonne} sans correspondance (« {groupe} », « {sous} »)")
        if COLONNES[cle] is None:
            continue
        resultat[colonne] = (COLONNES[cle], f"{groupe}{' / ' + sous if sous and sous != annee else ''}", note)
    return resultat


def collectivite(publication, nom, n, libelle):
    """Le périmètre d'une ligne : une collectivité, sous son code et son nom, ou un total."""
    if forme(libelle) in publication["totaux"]:
        return publication["totaux"][forme(libelle)]
    trouve = re.fullmatch(r"([0-9]{2,3}[ADM]?) (.+)", libelle)
    attendu = publication["collectivites"].get(trouve.group(1)) if trouve else None
    if attendu is None or forme(trouve.group(2)) != forme(attendu[1]):
        sys.exit(f"{nom}, ligne {n} : collectivité inconnue (« {libelle} »)")
    return attendu[0]


def annee_du_classeur(chemin):
    """L'année des montants, que donne la ligne 4 du tableau T01."""
    lignes = grille(lire_xlsx(chemin, "T01")[1])
    annees = {texte(v) for c, v in lignes.get(4, {}).items() if re.fullmatch(r"20[0-9]{2}", texte(v))}
    if len(annees) != 1:
        sys.exit(f"{chemin.name} : année du classeur introuvable dans le tableau T01")
    return annees.pop()


def lignes_du_fichier(fichier):
    """Les chiffres d'une copie archivée, tableau par tableau."""
    publication = PUBLICATIONS.get(fichier["source_id"])
    if publication is None:
        sys.exit(f"{fichier['id']} : source non prise en charge")
    version = fichier["mis_a_jour_source"][:10]
    if not version:
        sys.exit(f"{fichier['id']} : date du classeur absente, version inconnue")
    chemin = BASE / fichier["chemin"]
    annee = annee_du_classeur(chemin)
    sens = {c["id"]: c["sens"] for c in lire("tables/concepts.csv")}
    qui = {"departements": "départements", "regions": "régions"}[publication["qui"]]
    resultat = []
    for nom, titre in TABLEAUX.items():
        lignes = grille(lire_xlsx(chemin, nom)[1])
        if forme(lignes.get(1, {}).get("A", "")) != forme(titre.format(qui)):
            sys.exit(f"{nom} : titre inattendu (« {lignes.get(1, {}).get('A', '')} »)")
        lues = colonnes(nom, lignes, annee)
        montants = {}  # n° de ligne → (libellé, périmètre, {colonne: valeur})
        for n in sorted(lignes):
            libelle = " ".join(str(lignes[n].get("A", "")).split())
            valeurs = {c: lignes[n][c] for c in lues if c in lignes[n]}
            if n <= 5 or not any(isinstance(v, float) for v in valeurs.values()):
                continue  # en-tête, source ou ligne vide
            if any(not isinstance(v, float) for v in valeurs.values()):
                sys.exit(f"{nom}, ligne {n} : montant illisible")
            montants[n] = (libelle, collectivite(publication, nom, n, libelle), valeurs)
        for colonne, (concept, intitule, note) in sorted(lues.items(), key=lambda e: rang(e[0])):
            valeurs = [m[2][colonne] for m in montants.values() if colonne in m[2]]
            # Une colonne a la précision de sa valeur la plus précise : un zéro est exact.
            decimales = max((nombre(v)[1] for v in valeurs), default=0)
            for n, (libelle, perimetre, vals) in montants.items():
                if colonne not in vals:
                    continue
                concept_id = f"COMPTES_LOCAUX.{concept}"
                ligne = {
                    "source_id": fichier["source_id"], "fichier_id": fichier["id"],
                    "emplacement": f"feuille={nom};cellule={colonne}{n};ligne={libelle};colonne={intitule};annee={annee}",
                    "zone": "FR", "perimetre_id": perimetre, "concept_id": concept_id, "fonction_id": "",
                    "traitements": "", "unite_id": "MIO_EUR", "periode": annee, "valeur": nombre(vals[colonne])[0],
                    "decimales": decimales, "statut": "definitif", "drapeau_source": "", "version": version,
                    "consolidation": "sans_objet" if sens[concept_id] == "solde" else "non_consolide",
                    "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
                }
                ligne["id"] = identifiant(ligne)
                resultat.append(ligne)
    return resultat


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
