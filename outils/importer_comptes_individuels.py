#!/usr/bin/env python3
"""Inscrit dans la base les comptes individuels des collectivités locales que publie la DGFiP sur data.economie.gouv.fr,
à partir des copies archivées des exports de ses jeux de données et de leurs maquettes.

    python3 outils/importer_comptes_individuels.py --requetes <source_id> <maquette|inventaire|comptes>
    python3 outils/importer_comptes_individuels.py <fichier_id>

Les comptes individuels donnent, pour chaque commune depuis 2000, chaque groupement à fiscalité propre depuis 2007, chaque
département et chaque région depuis 2008, l'analyse des équilibres financiers fondamentaux de l'exercice et les éléments
de sa fiscalité directe locale : ceux du budget principal, ou, pour un groupement, du budget principal et des budgets
annexes réunis. Chaque jeu de données du portail réunit un ou plusieurs exercices d'un niveau, une ligne par collectivité
et par exercice, une colonne par variable. Une maquette jointe, un classeur ods, décrit les variables, une feuille par
suite d'exercices : une ligne par rubrique, son libellé, et, dans des colonnes aux en-têtes explicites, la variable qui
en donne le montant (en milliers d'euros), le montant par habitant, la moyenne de la strate, le ratio de structure ; pour
la fiscalité, la base nette, les réductions de base accordées sur délibération, le produit et le taux voté (en %).
L'import ne lit que les montants, les bases, les réductions et les taux : les autres variables se déduisent des
montants, ou portent sur d'autres collectivités que celle de la ligne.

Trois sortes de copies sont archivées, et s'importent dans cet ordre :
- la maquette jointe au jeu le plus récent de chaque niveau, qui reprend les feuilles de toutes les années, et, pour les
  groupements et les départements, celle des établissements publics territoriaux ou des collectivités territoriales
  uniques, aux mêmes variables ;
- l'inventaire de chaque jeu : le nombre de lignes de chacun de ses exercices ;
- pour chaque exercice, les comptes : les champs qui désignent et décrivent chaque collectivité, et les variables que
  retient tables/variables_comptes_individuels.csv.
L'import vérifie que les variables que ce référentiel retient pour un exercice sont exactement celles que la feuille de
la maquette qui le couvre donne en montant, en base, en réduction ou en taux, avec le libellé et la grandeur qu'il leur
prête ; que chaque ligne de la copie est de l'exercice et désigne une collectivité et une seule ; que chaque valeur est
un nombre, ou la marque d'une valeur absente (« - », ou rien) ; et que la copie a le nombre de lignes que l'inventaire
annonce. Il inscrit la copie dans tables/fichiers_comptes_individuels.csv. La version d'une copie d'un export est la date
de modification du jeu de données qu'annonce le portail, celle d'une maquette la date de modification inscrite dans le
classeur ; l'inventaire qui contrôle des comptes est le plus récent du même jeu dont la version ne dépasse pas la leur.
Ces copies sont les chiffres eux-mêmes : la base ne les recopie pas, elle les lit.
"""

import math
import re
import sys
import urllib.parse

from commun import BASE, champs, ecrire, lire, lire_export_ofgl, lire_ods

PORTAIL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
COMMUNES = "dgfip.comptes-individuels-communes"
GFP = "dgfip.comptes-individuels-gfp"
DEPARTEMENTS = "dgfip.comptes-individuels-departements"
REGIONS = "dgfip.comptes-individuels-regions"
_C = "comptes-individuels-des-communes-fichier-global-"
_G = "comptes-individuels-des-groupements-a-fiscalite-propre-fichier-global-"
_D = "comptes-individuels-des-departements-fichier-global-"
_DC = "comptes-individuels-des-departements-et-des-collectivites-territoriales-uniques-fichier-global-"
_R = "comptes-individuels-des-regions-fichier-global-"
# Jeux de données de chaque niveau : (jeu, premier et dernier exercice). Le nom d'un jeu ne dit pas toujours ses
# exercices : celui des communes « 2008 » réunit 2000 à 2008, celui des groupements « 2023-2024 » 2023 à 2025.
JEUX = {
    COMMUNES: [(_C + "2008", 2000, 2008), (_C + "20090", 2009, 2009), (_C + "2010", 2010, 2010),
               (_C + "2011-2015", 2011, 2015), (_C + "2016", 2016, 2016), (_C + "2017", 2017, 2017),
               (_C + "2018", 2018, 2018), (_C + "2019-2020", 2019, 2020), (_C + "2021", 2021, 2021),
               (_C + "2022", 2022, 2022), (_C + "2023-2024", 2023, 2024), (_C + "2025", 2025, 2025)],
    GFP: [(_G + "2007-2008", 2007, 2008), (_G + "2009", 2009, 2009), (_G + "2010", 2010, 2010),
          (_G + "2011-2015", 2011, 2015), (_G + "2016", 2016, 2016), (_G + "2017", 2017, 2017),
          (_G + "2018-2019", 2018, 2019), (_G + "2020", 2020, 2020), (_G + "2021", 2021, 2021),
          (_G + "2022", 2022, 2022), (_G + "2023-2024", 2023, 2025)],
    DEPARTEMENTS: [(_D + "2008", 2008, 2008), (_D + "2009", 2009, 2009), (_D + "2010", 2010, 2010),
                   (_D + "2011-2012", 2011, 2012), (_D + "2013", 2013, 2015), (_DC + "2016", 2016, 2016),
                   (_DC + "2017-2018", 2017, 2018), (_DC + "2019-2020", 2019, 2020), (_DC + "2021-2022", 2021, 2022),
                   (_DC + "2023-2024", 2023, 2024), (_DC + "2025", 2025, 2025)],
    REGIONS: [(_R + "2008", 2008, 2008), (_R + "2009", 2009, 2009), (_R + "2010", 2010, 2010),
              (_R + "2011-2012", 2011, 2012), (_R + "2013", 2013, 2014), (_R + "2015", 2015, 2015),
              (_R + "2016", 2016, 2016), (_R + "2017", 2017, 2018), (_R + "2019-2020", 2019, 2020),
              (_R + "2021-2024", 2021, 2024), (_R + "2025", 2025, 2025)],
}
# Maquettes archivées : (jeu, pièce jointe). La première de chaque niveau décrit ses variables ; les autres, aux mêmes
# variables, les établissements publics territoriaux de la métropole du Grand Paris, parmi les groupements, et les
# collectivités territoriales uniques, parmi les départements (la seconde nomme « tvactu » la fraction de TVA, que le jeu
# donne, pour toutes ses lignes, dans « tvad »).
MAQUETTES = {
    COMMUNES: [(_C + "2025", "maquette_commune_vfods")],
    GFP: [(_G + "2023-2024", "maquette_groupement_a_fiscalite_propre_vfods"), (_G + "2023-2024", "maquette_eptods")],
    DEPARTEMENTS: [(_DC + "2025", "maquette_departement_vfods"), (_DC + "2025", "maquette_ctu_vfods")],
    REGIONS: [(_R + "2025", "maquette_region_vfods")],
}
# Champs qui désignent et décrivent chaque collectivité : (champ, colonne de sa fiche dans la base construite, premier et
# dernier exercice où il figure). Le premier est l'exercice ; viennent ensuite ceux qui la désignent.
FICHES = {
    COMMUNES: [("an", "", 2000, 2025), ("dep", "departement", 2000, 2025), ("icom", "", 2000, 2025),
               ("inom", "nom", 2000, 2025), ("reg", "region", 2000, 2025), ("pop1", "population", 2000, 2025),
               ("pop2", "population_dgf", 2000, 2009), ("nomsst1", "strate", 2000, 2025),
               ("nomsst2", "groupement", 2000, 2025)],
    GFP: [("exer", "", 2007, 2025), ("siren", "", 2007, 2025), ("lbudg", "nom", 2007, 2025),
          ("ndept", "departement", 2007, 2025), ("mpoid", "population", 2007, 2025),
          ("nbtotba", "budgets_annexes", 2007, 2025), ("nbbaspic", "budgets_spic", 2007, 2025)],
    DEPARTEMENTS: [("exer", "", 2008, 2025), ("dep", "departement", 2008, 2025), ("lbudg", "nom", 2008, 2025),
                   ("mpoid_bp", "population", 2008, 2025), ("strate", "strate", 2008, 2025)],
    REGIONS: [("exer", "", 2008, 2025), ("reg", "region", 2008, 2025), ("lbudg", "nom", 2008, 2025),
              ("mpoid_bp", "population", 2008, 2025), ("strate", "strate", 2008, 2025)],
}
CLES = {COMMUNES: ["dep", "icom"], GFP: ["siren"], DEPARTEMENTS: ["dep"], REGIONS: ["reg"]}
FORMES = {"dep": r"0[0-9]{2}|02[AB]|10[1-46]", "icom": r"[0-9]{3}", "siren": r"[0-9]{9}", "reg": r"[0-9]{3}"}
# Nombres entiers, ou rien ; l'export écrit parfois un entier comme un nombre décimal (« 718.0 »).
POPULATIONS = {"pop1", "pop2", "mpoid", "mpoid_bp", "nbtotba", "nbbaspic"}
ENTIER = re.compile(r"[0-9]+(?:\.0+)?")
# Le code Insee d'une commune : son département sans le zéro de tête, puis son numéro ; outre-mer, « 97 » puis son
# numéro, dont le premier chiffre est celui du département (la DGFiP numérote 101 la Guadeloupe, 102 la Guyane, 103 la
# Martinique, 104 La Réunion et 106 Mayotte, que l'Insee numérote 971, 973, 972, 974 et 976).
OUTRE_MER = {"101": "1", "102": "3", "103": "2", "104": "4", "106": "6"}
ABSENTES = {"-", ""}  # marques d'une valeur absente
GRANDEURS = ("montant", "base", "reduction", "taux")
# Sorte d'un en-tête de colonne de la maquette, dans l'ordre où on les cherche : un titre de partie (« Les taux et les
# produits de la fiscalité directe locale ») n'en est pas un.
SORTES = [("par_habitant", r"habitant"), ("strate", r"\bmoyen"), ("ratio", r"\bratios?\b|\ben %|% des"),
          ("taux", r"\btaux\b"), ("reduction", r"\bréductions?\b"), ("base", r"^bases nettes"),
          ("milliers", r"\bmilliers\b"), ("produits", r"^produits\b|^fractions? de tva$|impôts de répartition")]
CODE = re.compile(r"[a-z][a-z0-9_]*")
FEUILLE = re.compile(r"([0-9]{4})(?:-([0-9]{4}))?")
MAQUETTES_LUES = {}  # copie d'une maquette → ses feuilles, lues une fois


def normal(texte):
    return re.sub(r"\s+", " ", texte).strip()


def sorte(texte):
    if texte.startswith("Les "):
        return None
    return next((s for s, motif in SORTES if re.search(motif, texte, re.I)), None)


def grandeur(pile):
    """La grandeur d'une variable d'après les en-têtes de sa colonne, du plus récent au plus ancien : un montant sous
    « En milliers d'euros », sauf sous des réductions ou des bases ; le produit d'un impôt est un montant."""
    if not pile:
        return None
    if pile[-1] in ("par_habitant", "strate", "ratio", "taux", "reduction", "base"):
        return pile[-1]
    if pile[-1] == "produits":
        return "montant"
    dessous = pile[-2] if len(pile) > 1 else None
    return dessous if dessous in ("reduction", "base") else "montant"


def decrites(lignes, lieu):
    """{variable: (grandeur, libellé)} : les variables qu'une feuille de maquette donne en montant, en base, en réduction
    ou en taux, chacune avec le libellé de la première ligne où elle figure. Un texte qui n'est pas le libellé de sa
    ligne et qui nomme une sorte de colonne en est l'en-tête, pour les lignes qui suivent."""
    resultat, piles = {}, {}
    for ligne in lignes:
        cellules = [(i, normal(c)) for i, c in enumerate(ligne) if normal(c)]
        codes = [(i, c) for i, c in cellules if CODE.fullmatch(c)]
        textes = [(i, c) for i, c in cellules if not CODE.fullmatch(c) and c != "-"]
        libelle = textes[0][1] if codes and textes else ""
        for i, code in codes:
            g = grandeur(piles.get(i, []))
            if g not in GRANDEURS:
                continue
            if code in resultat and resultat[code][0] != g:
                sys.exit(f"{lieu} : {code} figure en {resultat[code][0]} et en {g}")
            resultat.setdefault(code, (g, libelle))
        for i, texte in textes:
            if not (codes and i == textes[0][0]) and (s := sorte(texte)):
                piles.setdefault(i, []).append(s)
    return resultat


def bornes(feuille, lieu):
    trouve = FEUILLE.fullmatch(feuille)
    if trouve is None:
        sys.exit(f"{lieu} : feuille « {feuille} » qui ne dit pas ses exercices")
    return int(trouve.group(1)), int(trouve.group(2) or trouve.group(1))


def maquette(fichier):
    if fichier["id"] not in MAQUETTES_LUES:
        MAQUETTES_LUES[fichier["id"]] = lire_ods(BASE / fichier["chemin"])
    return MAQUETTES_LUES[fichier["id"]]


def feuille_de(fichier, exercice):
    """Les lignes de la feuille d'une maquette qui couvre un exercice."""
    couvrantes = [f for f in maquette(fichier) if bornes(f, fichier["id"])[0] <= int(exercice) <= bornes(f, fichier["id"])[1]]
    if len(couvrantes) != 1:
        sys.exit(f"{fichier['id']} : {len(couvrantes)} feuilles couvrent l'exercice {exercice}")
    return couvrantes[0], maquette(fichier)[couvrantes[0]]


def retenues(source, exercice, referentiel):
    """{variable: ligne du référentiel} : les variables que retient le référentiel pour un exercice d'un niveau."""
    resultat = {}
    for v in referentiel:
        if v["source_id"] == source and v["premier_exercice"] <= exercice <= v["dernier_exercice"]:
            if v["variable"] in resultat:
                sys.exit(f"tables/variables_comptes_individuels.csv : deux lignes de {v['variable']} ({source}) couvrent "
                         f"{exercice}")
            resultat[v["variable"]] = v
    return resultat


def champs_fiche(source, exercice):
    return [c for c, _, debut, fin in FICHES[source] if debut <= int(exercice) <= fin]


def requete(jeu, **parametres):
    return PORTAIL + jeu + "/exports/csv?" + urllib.parse.urlencode(parametres, quote_via=urllib.parse.quote, safe=",*()")


def jeu_de(source, exercice):
    return next(j for j, debut, fin in JEUX[source] if debut <= int(exercice) <= fin)


def requetes(source, contenu, referentiel):
    """Les requêtes à archiver pour un niveau : ses maquettes, l'inventaire de chacun de ses jeux, ou, pour chaque
    exercice, ses comptes : {requête: (jeu, exercice)}."""
    exercice = FICHES[source][0][0]
    if contenu == "maquette":
        return {f"{PORTAIL}{jeu}/attachments/{piece}": (jeu, "") for jeu, piece in MAQUETTES[source]}
    if contenu == "inventaire":
        return {requete(jeu, select=f"{exercice},count(*) as lignes", group_by=exercice, order_by=exercice): (jeu, "")
                for jeu, _, _ in JEUX[source]}
    resultat = {}
    for jeu, debut, fin in JEUX[source]:
        for annee in map(str, range(debut, fin + 1)):
            selection = champs_fiche(source, annee) + sorted(retenues(source, annee, referentiel))
            resultat[requete(jeu, select=",".join(selection), where=f'{exercice}="{annee}"',
                             order_by=",".join(CLES[source]))] = (jeu, annee)
    return resultat


def nature(fichier, referentiel):
    """(contenu, jeu, exercice) de la requête qui a produit la copie : l'une de celles que cet import sait lire."""
    source = fichier["source_id"]
    if source not in JEUX:
        sys.exit(f"{fichier['id']} : la source {source} n'est pas lue par cet import")
    for contenu in ("maquette", "inventaire", "comptes"):
        if fichier["url"] in (connues := requetes(source, contenu, referentiel)):
            return (contenu, *connues[fichier["url"]])
    sys.exit(f"{fichier['id']} : requête que cet import ne sait pas lire ({fichier['url']})")


def lignes(fichier, attendu):
    """Les lignes d'une copie, après contrôle de son en-tête."""
    entete, contenu = lire_export_ofgl(BASE / fichier["chemin"])
    if entete != attendu:
        sys.exit(f"{fichier['id']} : en-tête {entete}, attendu {attendu}")
    for n, ligne in enumerate(contenu, start=2):
        if len(ligne) != len(attendu):
            sys.exit(f"{fichier['id']}, ligne {n} : {len(ligne)} champs au lieu de {len(attendu)}")
    return contenu


def inventaire(fichier):
    """{exercice: nombre de lignes}."""
    resultat = {}
    for n, (exercice, nombre) in enumerate(lignes(fichier, [FICHES[fichier["source_id"]][0][0], "lignes"]), start=2):
        if not re.fullmatch(r"[0-9]{4}", exercice) or exercice in resultat or not nombre.isdigit():
            sys.exit(f"{fichier['id']}, ligne {n} : ligne d'inventaire illisible")
        resultat[exercice] = int(nombre)
    if not resultat:
        sys.exit(f"{fichier['id']} : inventaire vide")
    return resultat


def collectivite(source, valeurs, lieu):
    """Le code qui désigne la collectivité d'une ligne : code Insee d'une commune, numéro Siren d'un groupement, numéro
    de département ou de région tel que la DGFiP l'écrit (« 001 », « 02A », « 101 »)."""
    for c in CLES[source]:
        if not re.fullmatch(FORMES[c], valeurs[c]):
            sys.exit(f"{lieu} : {c} illisible « {valeurs[c]} »")
    if source != COMMUNES:
        return valeurs[CLES[source][0]]
    dep, icom = valeurs["dep"], valeurs["icom"]
    if dep in OUTRE_MER:
        if icom[0] != OUTRE_MER[dep]:
            sys.exit(f"{lieu} : commune {icom} hors de son département {dep}")
        return "97" + icom
    return dep[1:] + icom


def comptes(fichier, referentiel):
    """(exercice, [(collectivité, fiche, {variable: valeur}), …], nombre de valeurs absentes, {variable: décimales})
    d'une copie de comptes : la fiche donne chaque champ qui décrit la collectivité ; une valeur absente n'est pas
    rendue. Les décimales d'une variable sont le plus grand nombre de décimales de ses valeurs, sans les zéros finaux :
    l'export écrit « 124.0 » un montant au millier d'euros près."""
    contenu, _, exercice = nature(fichier, referentiel)
    if contenu != "comptes":
        sys.exit(f"{fichier['id']} : copie de {contenu}, pas de comptes")
    source = fichier["source_id"]
    fiche, variables = champs_fiche(source, exercice), sorted(retenues(source, exercice, referentiel))
    resultat, vues, absentes, decimales = [], set(), 0, dict.fromkeys(variables, 0)
    for n, ligne in enumerate(lignes(fichier, fiche + variables), start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        decrits = dict(zip(fiche, ligne))
        if decrits[fiche[0]] != exercice:
            sys.exit(f"{lieu} : exercice « {decrits[fiche[0]]} » au lieu de {exercice}")
        code = collectivite(source, decrits, lieu)
        if code in vues:
            sys.exit(f"{lieu} : deuxième ligne pour {code}")
        vues.add(code)
        for c in POPULATIONS & set(decrits):
            if decrits[c] and not ENTIER.fullmatch(decrits[c]):
                sys.exit(f"{lieu} : {c} illisible « {decrits[c]} »")
        valeurs = {}
        for variable, texte in zip(variables, ligne[len(fiche):]):
            if texte in ABSENTES:
                absentes += 1
                continue
            try:
                valeurs[variable] = float(texte)
            except ValueError:
                sys.exit(f"{lieu} : {variable} illisible « {texte} »")
            if not math.isfinite(valeurs[variable]):
                sys.exit(f"{lieu} : {variable} illisible « {texte} »")
            if "." in texte:
                decimales[variable] = max(decimales[variable], len(texte.split(".")[1].rstrip("0")))
        resultat.append((code, decrits, valeurs))
    return exercice, resultat, absentes, decimales


def controler_variables(fichier, maquette_, exercice, referentiel):
    """Les variables que le référentiel retient pour l'exercice doivent être celles que la feuille de la maquette qui le
    couvre donne en montant, en base, en réduction ou en taux, avec le même libellé et la même grandeur ; une variable
    que la maquette nomme autrement que le jeu porte ce nom dans le référentiel (« variable_maquette »)."""
    source = fichier["source_id"]
    nom, feuille = feuille_de(maquette_, exercice)
    lieu = f"{maquette_['id']}, feuille {nom}"
    trouvees = decrites(feuille, lieu)
    attendues = retenues(source, exercice, referentiel)
    nommees = {v["variable_maquette"] or v["variable"]: v for v in attendues.values()}
    if set(trouvees) != set(nommees):
        sys.exit(f"{fichier['id']} : la feuille {nom} de la maquette donne {sorted(set(trouvees) - set(nommees))} que le "
                 f"référentiel ne retient pas pour {exercice}, et pas {sorted(set(nommees) - set(trouvees))}")
    for code, v in sorted(nommees.items()):
        g, libelle = trouvees[code]
        if (g, normal(libelle)) != (v["grandeur"], v["libelle"]):
            sys.exit(f"{lieu} : {code} y est {g} « {normal(libelle)} », le référentiel le dit {v['grandeur']} "
                     f"« {v['libelle']} »")


def controler_maquette(fichier, source, principale):
    """Une maquette : des feuilles qui disent leurs exercices ; celles de la maquette principale couvrent chacun des
    exercices du niveau, une fois. Rend le nombre de variables qu'elle donne en montant, base, réduction ou taux."""
    variables = set()
    for nom, feuille in maquette(fichier).items():
        bornes(nom, fichier["id"])
        variables |= set(decrites(feuille, f"{fichier['id']}, feuille {nom}"))
    if principale:
        for _, debut, fin in JEUX[source]:
            for annee in range(debut, fin + 1):
                feuille_de(fichier, str(annee))
    return len(variables)


def maquette_principale(source, inscrits, fichiers):
    """La copie inscrite la plus récente de la maquette principale d'un niveau."""
    jeu, piece = MAQUETTES[source][0]
    candidats = [i for i in inscrits if i["source_id"] == source and i["contenu"] == "maquette"
                 and fichiers[i["fichier_id"]]["url"] == f"{PORTAIL}{jeu}/attachments/{piece}"]
    if not candidats:
        sys.exit(f"aucune maquette de {source} inscrite (l'importer d'abord)")
    return fichiers[max(candidats, key=lambda i: i["version"])["fichier_id"]]


def controleur(fichier, inscrits, jeu):
    """L'inventaire inscrit qui contrôle une copie de comptes : du même jeu, le plus récent dont la version ne dépasse pas
    la sienne."""
    version = fichier["mis_a_jour_source"][:10]
    candidats = [i for i in inscrits if i["source_id"] == fichier["source_id"] and i["contenu"] == "inventaire"
                 and i["jeu"] == jeu and i["version"] <= version]
    if not candidats:
        sys.exit(f"{fichier['id']} : aucun inventaire de {jeu} inscrit à cette version (l'importer d'abord)")
    return max(candidats, key=lambda i: i["version"])["fichier_id"]


def inscription(fichier, inscrits, fichiers, referentiel):
    """La ligne de tables/fichiers_comptes_individuels.csv d'une copie, après contrôle de son contenu ; `inscrits` est la
    table déjà écrite, où l'on cherche les copies qui la contrôlent."""
    contenu, jeu, exercice = nature(fichier, referentiel)
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas sa version")
    ligne = {"fichier_id": fichier["id"], "source_id": fichier["source_id"], "jeu": jeu, "contenu": contenu,
             "exercice": exercice, "version": version, "lignes": "", "variables": "", "valeurs_absentes": ""}
    source = fichier["source_id"]
    if contenu == "maquette":
        principale = fichier["url"].endswith("/attachments/" + MAQUETTES[source][0][1])
        ligne.update(lignes=str(len(maquette(fichier))), variables=str(controler_maquette(fichier, source, principale)))
        return ligne
    if contenu == "inventaire":
        exercices = inventaire(fichier)
        debut, fin = next((d, f) for j, d, f in JEUX[source] if j == jeu)
        if sorted(exercices) != [str(a) for a in range(debut, fin + 1)]:
            sys.exit(f"{fichier['id']} : le jeu porte les exercices {sorted(exercices)}, pas ceux de {debut} à {fin}")
        ligne["lignes"] = str(len(exercices))
        return ligne
    annonce = inventaire(fichiers[controleur(fichier, inscrits, jeu)])
    controler_variables(fichier, maquette_principale(source, inscrits, fichiers), exercice, referentiel)
    _, lues, absentes, _ = comptes(fichier, referentiel)
    if len(lues) != annonce[exercice]:
        sys.exit(f"{fichier['id']} : {len(lues)} lignes, l'inventaire en annonce {annonce[exercice]}")
    ligne.update(lignes=str(len(lues)), variables=str(len(retenues(source, exercice, referentiel))),
                 valeurs_absentes=str(absentes))
    return ligne


def main():
    referentiel = lire("tables/variables_comptes_individuels.csv")
    if len(sys.argv) == 4 and sys.argv[1] == "--requetes":
        if sys.argv[2] not in JEUX or sys.argv[3] not in ("maquette", "inventaire", "comptes"):
            sys.exit(__doc__)
        for url in requetes(sys.argv[2], sys.argv[3], referentiel):
            print(url)
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    inscrits = [i for i in lire("tables/fichiers_comptes_individuels.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]], inscrits, fichiers, referentiel)
    ecrire("tables/fichiers_comptes_individuels.csv", champs("fichiers_comptes_individuels"), inscrits + [ligne],
           cle="fichier_id")
    unite = {"maquette": "feuille", "inventaire": "exercice", "comptes": "ligne"}[ligne["contenu"]]
    print(f"{ligne['fichier_id']} : {ligne['contenu']} {ligne['exercice'] or ligne['jeu']} ({ligne['version']}), "
          f"{ligne['lignes']} {unite}{'s' if int(ligne['lignes']) > 1 else ''}"
          + (f", {ligne['variables']} variables" if ligne["variables"] else "")
          + (f", {ligne['valeurs_absentes']} valeurs absentes" if ligne["valeurs_absentes"] not in ("", "0") else ""))


if __name__ == "__main__":
    main()
