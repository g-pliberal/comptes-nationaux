#!/usr/bin/env python3
"""Enregistre dans la base les listes et les décomptes officiels des organismes publics archivés.

    python3 outils/importer_organismes.py <fichier_id>

Copies prises en charge :
- la liste des organismes divers d'administration centrale (ODAC) de l'Insee (PDF) : chaque organisme, inscrit dans la
  table des organismes avec son rang dans la liste, la fonction sous laquelle elle le range et la page où il figure ;
- la liste des organismes divers d'administration locale (ODAL) de l'Insee (PDF), qui ne les nomme pas : le nombre
  d'organismes de chaque catégorie et leur total, en chiffres ;
- le chapitre 2 des « Collectivités locales en chiffres » de la DGCL (xlsx) : le nombre de collectivités territoriales
  et de groupements de communes au 1er janvier, par catégorie (tableau 2.2), et celui des groupements à fiscalité
  propre et des syndicats par type (tableau 2.5a), en chiffres.

Une ligne, une fonction ou une catégorie inconnue arrête l'import, comme un total que ne font pas ses parties ou un
nombre que deux tableaux donnent différemment. Une liste déjà inscrite dans la table des organismes n'y est pas
réinscrite ; si la copie en donne une autre, l'import s'arrête.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_pdf, lire_xlsx,
                    nombre, nombre_texte, position, table_des_chiffres, texte_pdf)

ODAC, ODAL, DGCL = "insee.liste-odac", "insee.liste-odal", "dgcl.collectivites-locales-en-chiffres"

# Liste des ODAC : sous l'en-tête de chaque fonction, un tableau dont chaque ligne porte le sigle d'un organisme à gauche,
# son nom à droite ; une ligne sans sigle continue le nom de la précédente. Chaque tableau a sa colonne des noms : la
# seule abscisse, à droite de celle des sigles, où commence un morceau de texte sur chacune de ses lignes. L'en-tête doit
# avoir le numéro et le libellé ci-dessous (la liste écrit « Logement », la COFOG « Logements »). Ce qui précède le
# premier en-tête est la présentation de la liste, qui dit l'année à laquelle elle se rapporte.
FONCTIONS_ODAC = {1: ("GF01", "Services généraux des administrations publiques"), 2: ("GF02", "Défense"),
                  3: ("GF03", "Ordre et sécurité publics"), 4: ("GF04", "Affaires économiques"),
                  5: ("GF05", "Protection de l’environnement"), 6: ("GF06", "Logement et équipements collectifs"),
                  7: ("GF07", "Santé"), 8: ("GF08", "Loisirs, culture et culte"), 9: ("GF09", "Enseignement"),
                  10: ("GF10", "Protection sociale")}
EN_TETE_FONCTION = re.compile(r"Fonction ([0-9]+) ?: ?(.+)")
ANNEE_ODAC = re.compile(r"liste des ODAC relative à l.année ([0-9]{4})")

# Liste des ODAL : le tableau du nombre d'organismes par catégorie, de son en-tête à son total. Libellé de la ligne →
# périmètre.
CATEGORIES_ODAL = {
    "Agences d'urbanisme": "ODAL_AGENCES_URBANISME",
    "Centre de gestion de la propriété forestière": "ODAL_PROPRIETE_FORESTIERE",
    "Chambres consulaires": "ODAL_CHAMBRES_CONSULAIRES", "Etablissements publics fonciers": "ODAL_EP_FONCIERS",
    "ODAL divers": "ODAL_DIVERS", "Services départementaux d'incendie et de secours": "ODAL_SDIS",
    "Electricité de Mayotte": "ODAL_ELECTRICITE_MAYOTTE",
    "Etablissements publics d'aménagement": "ODAL_EP_AMENAGEMENT", "Ile-de-France Mobilités": "ODAL_IDF_MOBILITES",
    "Offices de tourisme": "ODAL_OFFICES_TOURISME",
    "Société de la ligne nouvelle Montpellier Perpignan": "ODAL_LN_MONTPELLIER_PERPIGNAN",
    "Société de la ligne nouvelle Provence Côte d'Azur": "ODAL_LN_PROVENCE_COTE_AZUR",
    "Société de livraison des ouvrages olympiques": "ODAL_SOLIDEO",
    "Société du canal Seine-Nord Europe": "ODAL_CANAL_SEINE_NORD",
    "Sociétés d'aménagement foncier et d'établissement rural": "ODAL_SAFER",
    "Sociétés de grands projets": "ODAL_SOCIETES_GRANDS_PROJETS", "Agences et offices de l'eau": "ODAL_AGENCES_EAU",
    "Etablissements publics culturels locaux": "ODAL_EP_CULTURELS", "Caisses des écoles": "ODAL_CAISSES_ECOLES",
    "Centres de gestion de la fonction publique territoriale": "ODAL_CDG_FPT",
    "Etablissements publics locaux d'enseignement": "ODAL_EPLE",
    "Centres communaux d'action sociale": "ODAL_CCAS",
    "Maisons départementales des personnes handicapées": "ODAL_MDPH"}
TOTAL_ODAL = "Total"
PERIMETRES_ODAL = {**CATEGORIES_ODAL, TOTAL_ODAL: "S13132"}
EN_TETE_ODAL = "Catégories Nombre d’organismes"
ANNEE_ODAL = re.compile(r"le champ des ODAL en ([0-9]{4})")
LIGNE_ODAL = re.compile(r"(.*?) ?([0-9][0-9 ]*)")  # un libellé, puis un nombre écrit par tranches de trois chiffres

# Chapitre 2 de la DGCL. Tableau 2.2 : libellé de la ligne (sans son appel de note) → périmètre ; les lignes « dont :
# France métropolitaine » et « Outre-mer » se rapportent à la catégorie qui les précède.
FEUILLE_2_2 = "2.2 nb CL"
LIGNES_2_2 = {"Ensemble des collectivités locales": "COLLECTIVITES_ET_GROUPEMENTS",
              "Collectivité territoriales": "COLLECTIVITES_TERRITORIALES", "Communes": "COMMUNES",
              "Conseils départementaux": "CONSEILS_DEPARTEMENTAUX", "Conseils régionaux": "CONSEILS_REGIONAUX",
              "Collectivités à statut particulier": "COLLECTIVITES_STATUT_PARTICULIER",
              "Collectivité de Corse": "COLLECTIVITE_DE_CORSE", "Métropole de Lyon": "METROPOLE_LYON",
              "Martinique": "CTU_MARTINIQUE", "Guyane": "CTU_GUYANE", "Département de Mayotte": "DEPARTEMENT_MAYOTTE",
              "Groupements de communes": "GROUPEMENTS_COMMUNES",
              "Groupements de communes à fiscalité propre": "GFP", "Syndicats": "SYNDICATS"}
SOUS_LIGNES_2_2 = {"dont : France métropolitaine": "_METROPOLE", "Outre-mer": "_OUTRE_MER"}
# Tableau 2.5a : les deux tableaux de nombres, chacun désigné par son titre, au-dessus de la ligne des années (le
# troisième donne la population des groupements). Libellé de la ligne → périmètre ; « = » : nombre que le tableau 2.2
# donne déjà, et qui doit être le même ; rien : ligne non lue (les communes regroupées, et les groupements à fiscalité
# professionnelle unique).
FEUILLE_2_5A = "2.5a EPCI"
TABLEAUX_2_5A = {
    "Nombre de groupements de communes à fiscalité propre": {
        "Métropoles": "METROPOLES", "Communautés urbaines (CU)": "COMMUNAUTES_URBAINES",
        "Communautés d'agglomération (CA)": "COMMUNAUTES_AGGLOMERATION",
        "Communautés de communes (CC)": "COMMUNAUTES_COMMUNES", "Nombre d'EPCI à fiscalité propre": "=GFP",
        "Métropole de Lyon": "=METROPOLE_LYON", "Nombre de communes regroupées": "", "Nombre de communes isolées": "",
        "Nombre total de communes": "=COMMUNES", "EPCI à fiscalité professionnelle unique :": "",
        "Nombre de groupements": ""},
    "Nombre de syndicats": {
        "Syndicats intercommunaux à vocation unique (SIVU)": "SIVU",
        "Syndicats intercommunaux à vocation multiple (SIVOM)": "SIVOM",
        "Etablissements publics territoriaux (EPT)": "EPT", "Syndicats mixtes": "SYNDICATS_MIXTES",
        "Pôles métropolitains": "POLES_METROPOLITAINS", "Pôles d'équilibre territorial et rural (PETR)": "PETR",
        "Total": "=SYNDICATS"}}
FIN_DE_TABLEAU = re.compile(r"Sources? :")


def arreter(fichier, message):
    sys.exit(f"{fichier['id']} : {message}")


# --- Liste des ODAC ------------------------------------------------------------------------------------

def colonne_des_noms(fichier, fonction, lignes):
    """L'abscisse de la colonne des noms d'un tableau de la liste des ODAC, ses lignes données par leurs morceaux."""
    debuts = [[x for x, t in morceaux if t.strip()] for _, morceaux in lignes]
    sigles = min(d[0] for d in debuts)
    communes = [x for x in debuts[0] if x > sigles + 1 and all(any(abs(x - y) <= 1 for y in d) for d in debuts)]
    if len(communes) != 1:
        arreter(fichier, f"{fonction} : pas de colonne des noms unique ({communes})")
    return communes[0]


def organismes_odac(fichier):
    """Les organismes de la liste des ODAC, dans leur ordre : les lignes de la table des organismes."""
    presentation, tableaux = [], []  # tableaux : (fonction, [(page, morceaux)…])
    for numero, page in enumerate(lire_pdf(BASE / fichier["chemin"]), start=1):
        for _, morceaux in page:
            ligne = texte_pdf(morceaux)
            if not ligne:
                continue
            en_tete = EN_TETE_FONCTION.fullmatch(ligne)
            if en_tete:
                rang = int(en_tete.group(1))
                if FONCTIONS_ODAC.get(rang, ("", ""))[1] != en_tete.group(2):
                    arreter(fichier, f"page {numero} : fonction inconnue « {ligne} »")
                tableaux.append((FONCTIONS_ODAC[rang][0], []))
            elif tableaux:
                tableaux[-1][1].append((numero, morceaux))
            else:
                presentation.append(ligne)
    organismes = []
    for fonction, lignes in tableaux:
        noms = colonne_des_noms(fichier, fonction, lignes)
        for numero, morceaux in lignes:
            sigle = texte_pdf([m for m in morceaux if m[0] < noms - 1])
            nom = "".join(t for x, t in morceaux if x >= noms - 1)
            debut = min(x for x, t in morceaux if t.strip())
            if sigle and nom.strip():
                organismes.append({"sigle": sigle, "nom": nom, "page": numero, "fonction_id": fonction})
            elif abs(debut - noms) <= 1 and organismes and organismes[-1]["fonction_id"] == fonction:
                organismes[-1]["nom"] += nom
            else:
                arreter(fichier, f"page {numero} : ligne qui n'est ni un organisme ni la suite de son nom : "
                                 f"« {texte_pdf(morceaux)} »")
    annees = set(ANNEE_ODAC.findall(" ".join(presentation)))
    if len(annees) != 1 or not organismes:
        arreter(fichier, f"liste sans année ({sorted(annees)}) ou sans organisme ({len(organismes)})")
    annee = annees.pop()
    return [{"fichier_id": fichier["id"], "rang": str(rang), "annee": annee, "perimetre_id": "S13112",
             "fonction_id": o["fonction_id"], "sigle": o["sigle"], "nom": " ".join(o["nom"].split()),
             "page": str(o["page"])} for rang, o in enumerate(organismes, start=1)]


def inscrire_organismes(fichier, lus):
    """Inscrit dans la table des organismes la liste d'une copie ; renvoie le nombre d'organismes inscrits."""
    deja = [o for o in lire("tables/organismes.csv") if o["fichier_id"] == fichier["id"]]
    if deja:
        if sorted(deja, key=lambda o: int(o["rang"])) != lus:
            arreter(fichier, "liste déjà inscrite, que la copie donne autrement : contrôler l'import")
        return 0
    ecrire("tables/organismes.csv", champs("organismes"), lire("tables/organismes.csv") + lus,
           cle=lambda o: (o["fichier_id"], int(o["rang"])))
    return len(lus)


# --- Nombres d'organismes et de collectivités, en chiffres -----------------------------------------------

def chiffre(fichier, emplacement, perimetre, concept, periode, valeur):
    texte, decimales = nombre(valeur)
    ligne = {"source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement, "zone": "FR",
             "perimetre_id": perimetre, "concept_id": concept, "fonction_id": "", "traitements": "",
             "unite_id": "NOMBRE", "periode": periode, "valeur": texte, "decimales": decimales,
             "statut": "non_precise", "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10],
             "consolidation": "sans_objet", "denominateur_id": "", "nature": "publie", "calcul_id": "",
             "saisi_le": aujourdhui(), "notes": ""}
    ligne["id"] = identifiant(ligne)
    return ligne


def chiffres_odal(fichier):
    """Le nombre d'organismes de chaque catégorie de la liste des ODAL, et leur total."""
    pages = lire_pdf(BASE / fichier["chemin"])
    annees = set(ANNEE_ODAL.findall(" ".join(texte_pdf(m) for page in pages for _, m in page)))
    if len(annees) != 1:
        arreter(fichier, f"liste sans année du champ ({sorted(annees)})")
    annee, lignes, dans_le_tableau = annees.pop(), {}, False
    for numero, page in enumerate(pages, start=1):
        for _, morceaux in page:
            ligne = texte_pdf(morceaux)
            if ligne == EN_TETE_ODAL:
                dans_le_tableau = True
            elif dans_le_tableau and ligne:
                trouve = LIGNE_ODAL.fullmatch(ligne)
                if trouve is None or trouve.group(1) not in PERIMETRES_ODAL or trouve.group(1) in lignes:
                    arreter(fichier, f"page {numero} : ligne inconnue, sans nombre ou répétée « {ligne} »")
                lignes[trouve.group(1)] = (numero, nombre_texte(trouve.group(2))[0])
                dans_le_tableau = trouve.group(1) != TOTAL_ODAL
    if set(lignes) != set(PERIMETRES_ODAL):
        arreter(fichier, f"catégories absentes : {sorted(set(PERIMETRES_ODAL) - set(lignes))}")
    if sum(int(v) for l, (_, v) in lignes.items() if l != TOTAL_ODAL) != int(lignes[TOTAL_ODAL][1]):
        arreter(fichier, "le total n'est pas la somme des catégories")
    return [chiffre(fichier, f"page={page};libelle={libelle}", PERIMETRES_ODAL[libelle],
                    "UNITES_PUBLIQUES.NOMBRE_DANS_LE_CHAMP", annee, valeur) for libelle, (page, valeur) in lignes.items()]


def libelle_dgcl(texte):
    """Un libellé de ligne, sans ses blancs de bord ni son appel de note (« (a) »)."""
    return re.sub(r" ?\([a-z]\)$", "", str(texte).strip())


def annees_de_la_ligne(cellules, n):
    """{colonne: année} des années que porte la ligne n, si c'est la ligne des années d'un tableau : sans libellé, ou
    « Au 1er janvier »."""
    if libelle_dgcl(cellules.get(f"A{n}", "")) not in ("", "Au 1er janvier"):
        return {}
    return {position(r)[1]: str(int(v)) for r, v in cellules.items()
            if position(r)[0] == n and isinstance(v, float) and 1900 < v < 2100 and v == int(v)}


def valeurs_de_la_ligne(fichier, feuille, cellules, n, annees):
    """{année: (cellule, valeur)} d'une ligne de nombres ; il en faut un pour chaque année."""
    valeurs = {a: (f"{c}{n}", cellules.get(f"{c}{n}")) for c, a in annees.items()}
    if any(not isinstance(v, float) for _, v in valeurs.values()):
        arreter(fichier, f"{feuille}, ligne {n} : une année sans nombre ({valeurs})")
    return valeurs


def chiffres_dgcl(fichier):
    """Le nombre de collectivités et de groupements au 1er janvier de chaque année des tableaux 2.2 et 2.5a."""
    concept, lus = "UNITES_PUBLIQUES.NOMBRE_1ER_JANVIER", {}
    _, cellules = lire_xlsx(BASE / fichier["chemin"], FEUILLE_2_2)
    lignes = sorted({position(r)[0] for r in cellules})
    entete = next((n for n in lignes if len(annees_de_la_ligne(cellules, n)) >= 2), None)
    if entete is None:
        arreter(fichier, f"{FEUILLE_2_2} : pas de ligne des années")
    annees, categorie = annees_de_la_ligne(cellules, entete), None
    for n in (n for n in lignes if n > entete):
        libelle = libelle_dgcl(cellules.get(f"A{n}", ""))
        if FIN_DE_TABLEAU.match(libelle):
            break
        if not libelle:
            continue
        if libelle in SOUS_LIGNES_2_2 and categorie in ("COMMUNES", "CONSEILS_DEPARTEMENTAUX", "CONSEILS_REGIONAUX"):
            perimetre = categorie + SOUS_LIGNES_2_2[libelle]
        elif libelle in LIGNES_2_2:
            perimetre = categorie = LIGNES_2_2[libelle]
        else:
            arreter(fichier, f"{FEUILLE_2_2}, ligne {n} : libellé inconnu « {libelle} »")
        for annee, (cellule, valeur) in valeurs_de_la_ligne(fichier, FEUILLE_2_2, cellules, n, annees).items():
            if (perimetre, annee) in lus:
                arreter(fichier, f"{FEUILLE_2_2}, {cellule} : {perimetre} déjà lu pour {annee}")
            lus[(perimetre, annee)] = chiffre(fichier, f"feuille={FEUILLE_2_2};cellule={cellule}", perimetre, concept,
                                              annee, valeur)
    _, cellules = lire_xlsx(BASE / fichier["chemin"], FEUILLE_2_5A)
    lignes, tableau, vus = sorted({position(r)[0] for r in cellules}), None, set()
    for n in lignes:
        libelle = libelle_dgcl(cellules.get(f"A{n}", ""))
        precedent = libelle_dgcl(cellules.get(f"A{n - 1}", ""))
        if len(annees_de_la_ligne(cellules, n)) >= 2:
            tableau = TABLEAUX_2_5A.get(precedent)
            annees = annees_de_la_ligne(cellules, n)
            vus.add(precedent if tableau is not None else None)
        elif FIN_DE_TABLEAU.match(libelle):
            tableau = None
        elif tableau is not None and libelle:
            if libelle not in tableau:
                arreter(fichier, f"{FEUILLE_2_5A}, ligne {n} : libellé inconnu « {libelle} »")
            if not tableau[libelle]:
                continue
            for annee, (cellule, valeur) in valeurs_de_la_ligne(fichier, FEUILLE_2_5A, cellules, n, annees).items():
                perimetre = tableau[libelle].lstrip("=")
                if tableau[libelle].startswith("="):
                    deja = lus.get((perimetre, annee))
                    if deja is None or float(deja["valeur"]) != valeur:
                        arreter(fichier, f"{FEUILLE_2_5A}, {cellule} : {perimetre} vaut {valeur} en {annee}, "
                                         f"{deja and deja['valeur']} au tableau 2.2")
                    continue
                if (perimetre, annee) in lus:
                    arreter(fichier, f"{FEUILLE_2_5A}, {cellule} : {perimetre} déjà lu pour {annee}")
                lus[(perimetre, annee)] = chiffre(fichier, f"feuille={FEUILLE_2_5A};cellule={cellule}", perimetre,
                                                  concept, annee, valeur)
    if vus - {None} != set(TABLEAUX_2_5A):
        arreter(fichier, f"{FEUILLE_2_5A} : tableaux absents : {sorted(set(TABLEAUX_2_5A) - vus)}")
    return list(lus.values())


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    if fichier["source_id"] == ODAC:
        lus = organismes_odac(fichier)
        inscrits = inscrire_organismes(fichier, lus)
        print(f"{fichier['id']} : {len(lus)} organismes de la liste de {lus[0]['annee']}, {inscrits} inscrits")
        return
    lecteurs = {ODAL: chiffres_odal, DGCL: chiffres_dgcl}
    if fichier["source_id"] not in lecteurs:
        sys.exit(f"{fichier['id']} : source sans lecteur ici ({fichier['source_id']})")
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, lecteurs[fichier["source_id"]](fichier), fichier["id"])
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
