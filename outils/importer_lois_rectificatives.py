#!/usr/bin/env python3
"""Enregistre dans la base les crédits qu'ouvre et qu'annule une loi de finances rectificative, ou de fin de gestion,
à partir de son texte définitif, tel que le publie l'assemblée qui l'a adopté en dernier (page HTML archivée du Sénat
ou de l'Assemblée nationale).

    python3 outils/importer_lois_rectificatives.py <fichier_id>

Tableaux lus : les états qui répartissent, par mission et par programme, les autorisations d'engagement et les crédits
de paiement que la loi ouvre (« supplémentaires ») et ceux qu'elle annule : budget général, budgets annexes, comptes
d'affectation spéciale et comptes de concours financiers. Jusqu'à la deuxième loi de 2009, un état donne les ouvertures
(B, C, D) et un autre les annulations (B', C', D') ; depuis, un même état donne les deux, en quatre colonnes. La lettre
d'un état ne dit pas toujours sa catégorie (l'état C est celui des comptes spéciaux quand la loi n'a pas d'état des
budgets annexes) : la catégorie d'un tableau est la dernière que nomment le titre de l'état et les intertitres qui le
précèdent (« I. – Comptes d'affectation spéciale »). Sous un programme, une ligne « dont titre 2 » (« dont charges de
personnel ») donne la part des crédits qui va aux dépenses de personnel. L'état A (les évaluations de recettes
révisées), l'article d'équilibre, le tableau de financement, les plafonds d'emplois et les autorisations de découvert
ne sont pas lus.

Un état se reconnaît à son intitulé (« ÉTAT B (Article 7 de la loi) »). Ses tableaux sont ceux qui s'ouvrent entre son
intitulé et celui de l'état suivant, hors ceux qui portent l'intitulé d'un état ; un tableau que la page coupe en
plusieurs continue jusqu'à sa ligne de total. Chaque colonne doit être l'une des quatre que l'import connaît (COLONNES),
et l'unité, l'euro (une page qui ne l'annonce pas se déclare dans UNITE_TUE). Une mission égale la somme de ses
programmes, et la ligne de total celle des missions, dans chaque colonne ; une case vide, nulle ou « néant » vaut zéro
dans ces sommes, et ne donne pas de chiffre. Les missions sont les lignes en gras quand le tableau en marque, sinon elles
se reconnaissent à leurs montants, comme dans outils/importer_lois_finances.py ; une mission dont la page n'imprime pas
le montant vaut la somme de ses programmes. Jusqu'en 2009, chaque budget annexe ouvre sur une ligne à son nom, sans
montant, et se ferme sur une ligne « Totaux hors amortissement », qui donne son montant et doit égaler ses programmes.
Une ligne « dont » ne peut dépasser le programme qu'elle détaille.

Le total de chaque tableau doit égaler ce que les articles de la loi ouvrent ou annulent pour sa catégorie et son état
(« Il est annulé pour 2024, au titre du budget général, des autorisations d'engagement et des crédits de paiement
s'élevant respectivement aux montants de … € et de … €, conformément à la répartition par mission donnée à l'état B
annexé à la présente loi ») ; plusieurs articles qui renvoient au même état s'additionnent, et un article « au titre
des comptes spéciaux » couvre les deux catégories de comptes. Un article que l'import ne sait pas lire, un tableau dont
un total n'a pas d'article, ou un article sans tableau, arrête l'import ; « un crédit » (« des crédits ») est un
montant de crédits de paiement, avec autant d'autorisations d'engagement ou aucune, ce que le tableau doit dire. Une page
qui ne reproduit pas les articles de la loi, ou pas ses états, se déclare dans SANS_ARTICLES ou SANS_ETATS ; dans le
second cas, les totaux de chaque catégorie se lisent dans les articles, chacun dans la phrase qui l'énonce. Un état dont
les crédits s'ajoutent à ceux d'un autre état de la même catégorie, sur les mêmes missions (l'état B'' de 2009), donne
ses chiffres sous un traitement, déclaré dans TRAITEMENTS.

Les missions, les budgets annexes, les comptes spéciaux et leurs programmes sont les fonctions de la norme LOLF, sous
l'identifiant que leur donnent les imports des lois d'approbation des comptes et des lois de finances initiales ; un
libellé qu'un état écrit autrement que ces lois la même année se déclare dans LIBELLES. La période d'un chiffre est
l'année de la loi, sa version la date du texte ; les crédits ouverts et annulés sont des autorisations, sans statut de
prévision ou d'exécution.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_page_html,
                    lire_texte_html, nombre_de_phrase, nombre_texte, table_des_chiffres, texte_html)
from importer_lois_finances import cle_titre, montant, nom
from importer_lois_resultats import code_lolf, colonnes, propre, unite_annoncee

# Catégories de crédits, telles que les nomment le titre d'un état, ses intertitres et les articles de la loi.
NOMS_CATEGORIES = {"BG": r"budget général", "BA": r"budgets? annexes?", "CAS": r"comptes? d’affectation spéciale",
                   "CCF": r"comptes? de concours financiers"}
# Intitulé d'une colonne → (autorisations d'engagement ou crédits de paiement, ouvertures ou annulations).
COLONNES = {r"Autorisations d’engagement supplémentaires (?:accordées|ouvertes)": ("AE", "OUVERTURES"),
            r"Crédits de paiement supplémentaires ouverts": ("CP", "OUVERTURES"),
            r"Autorisations d’engagement annulées": ("AE", "ANNULATIONS"),
            r"Crédits de paiement annulés": ("CP", "ANNULATIONS")}
ETAT = r"[ÉE][Tt][Aa][Tt]\s+([A-G])\s*(['’′″]{0,2})\s*\(\s*(?:[Aa]rticles?|ARTICLES?)\s+[0-9]"
DONT = r"dont (?:titre 2|charges de personnel)"
SOUS_TOTAL = r"totaux hors amortissements?"
# Caractères invisibles que certaines pages laissent dans le texte : marques de direction, espaces sans chasse, et
# symboles de mise en page d'une police de la zone d'usage privé d'Unicode.
INVISIBLES = re.compile(r"[​-‏‪-‮⁠-⁩﻿-]")
# Pages qui ne reproduisent pas tout le texte de la loi : source → ce qui manque, dit dans la note de chaque chiffre.
SANS_ARTICLES = {
    "an.ta15-0032": "La page de l’Assemblée nationale ne reproduit pas les articles de la loi, seulement ses états : "
                    "le total de l’état n’a pas pu être comparé à l’article qui ouvre et annule ces crédits.",
}
# États dont les crédits s'ajoutent à ceux d'un autre état de la même catégorie, sur les mêmes missions : (source,
# état) → traitement qui les distingue (table des traitements).
TRAITEMENTS = {("senat.tas08-076", "B''"): "lfr_2009_04_etat_b_seconde"}
# Libellés qu'un état écrit autrement que la loi de finances initiale et la loi d'approbation des comptes de la même
# année, pour la même mission ou le même programme : (source, libellé de la page) → libellé de ces lois. Le chiffre
# prend la fonction du second ; son emplacement garde le libellé de la page. Un libellé déclaré que la page ne porte
# pas arrête l'import.
LIBELLES = {
    ("senat.tas06-037", "Remboursements et dégrèvements d’impôts d’État (crédits évaluatifs)"):
        "Remboursements et dégrèvements d’impôts d’État",
    ("senat.tas06-037", "Remboursements et dégrèvements d’impôts locaux (crédits évaluatifs)"):
        "Remboursements et dégrèvements d’impôts locaux",
    ("senat.tas07-043", "Enseignement privé du premier et du second degré"):
        "Enseignement privé du premier et du second degrés",
    ("senat.tas08-037", "Sécurité et qualité sanitaire de l’alimentation"):
        "Sécurité et qualité sanitaires de l’alimentation",
    ("senat.tas08-076", "Prêt pour le développement économique et social"):
        "Prêts pour le développement économique et social",
    ("senat.tas08-076", "Concours spécifiques et administrations"): "Concours spécifiques et administration",
    ("senat.tas09-079", "Démonstrateurs et plateformes technologiques en énergies renouvelables et décarbonées et "
                        "chimie verte"):
        "Démonstrateurs et plates-formes technologiques en énergies renouvelables et décarbonées et chimie verte",
    ("senat.tas09-104", "Enseignement scolaire public du premier degrés"): "Enseignement scolaire public du premier degré",
    ("senat.tas09-104", "Recherche dans le domaine de l’énergie, du développement et de l’aménagement durables"):
        "Recherche dans les domaines de l’énergie, du développement et de l’aménagement durables",
    ("an.ta14-0268", "Versement de la France à la Grèce au titre de la restitution à cet État des revenus perçus par la "
                     "Banque de France sur les titres grecs"):
        "Versement de la France à la Grèce au titre de la restitution à cet État des revenus perçus par la Banque de "
        "France sur les titres grecs détenus en compte propre",
    ("an.ta14-0460", "Services nationaux de transport conventionnés"):
        "Services nationaux de transport conventionnés de voyageurs",
    ("an.ta14-0460", "Exploitation des services nationaux de transport conventionnés de voyageurs"):
        "Exploitation des services nationaux de transport conventionnés",
    ("an.ta15-0067", "Dotation du Mécanisme européen de stabilité"):
        "Dotation en capital du Mécanisme européen de stabilité",
    ("senat.tas20-025", "Avances remboursables de droits de mutation à titre onéreux destinées à soutenir les départements "
                        "et d’autres collectivités affectés par les conséquences économiques de l’épidémie de covid-19"):
        "Avances remboursables de droits de mutation à titre onéreux destinées à soutenir les départements et d’autres "
        "collectivités territoriales affectés par les conséquences économiques de l’épidémie de covid-19",
    ("senat.tas23-024", "Avances remboursables et prêts bonifiés aux entreprises touchées par la crise de la covid-19 ou "
                        "par le conflit en Ukraine"):
        "Avances remboursables et prêts bonifiés aux entreprises touchées par la crise de la Covid-19",
}
LIBELLES_VUS = set()
# Pages qui n'annoncent pas l'unité d'un état : ses totaux égalent alors, à l'euro, les montants des articles.
UNITE_TUE = {"senat.tas20-136"}
SANS_ETATS = {
    "senat.tas08-001": "Le texte définitif ne reproduit pas les états de la loi : le montant est celui de l’article "
                       "qui ouvre ou annule ces crédits, pour toute la catégorie.",
}


def normaliser(texte):
    """Le texte d'une page, une seule apostrophe, sans blancs autour d'elle ni devant une virgule, et sans
    caractères invisibles."""
    texte = INVISIBLES.sub("", texte).replace("'", "’")
    return re.sub(r"\s+", " ", re.sub(r"\s+,", ",", re.sub(r"\s*’\s*", "’", texte))).strip()


def lettre_etat(lettre, primes):
    """« B », « B' » ou « B'' », quelle que soit la façon dont la page écrit ses primes."""
    n = len(primes) + primes.count("″")
    return lettre + "'" * n


def cle_colonne(libelle):
    for motif, cle in COLONNES.items():
        if re.fullmatch(motif, libelle.replace("'", "’")):
            return cle
    return None


def entete(tableau):
    """Nombre de lignes d'en-tête d'un tableau de crédits : jusqu'à celle qui nomme ses colonnes d'autorisations
    d'engagement et de crédits de paiement ; None si le tableau n'en a pas."""
    for r, ligne in enumerate(tableau[:4]):
        cles = {cle_colonne(propre(x)) for x in ligne} - {None}
        if {"AE", "CP"} <= {c[0] for c in cles}:
            return r + 1
    return None


def categorie_nommee(texte):
    """La dernière catégorie de crédits que nomme un texte, ou None."""
    trouvees = [(m.start(), c) for c, motif in NOMS_CATEGORIES.items() for m in re.finditer(motif, cle_titre(texte))]
    return max(trouvees)[1] if trouvees else None


def unite_du_tableau(tableau, e, forme, avant, source_id):
    """L'unité des montants d'un tableau, qu'annoncent ses lignes d'en-tête, sa légende ou le texte qui le précède :
    l'euro, seule unité des états de crédits ; une page qui ne l'annonce pas se déclare dans UNITE_TUE."""
    textes = [x for l in tableau[:e] for x in l] + [forme["legende"]] + re.findall(r"\([^()]{0,30}\)", avant[-200:])
    annoncees = {unite_annoncee(x) for x in textes} - {None}
    if annoncees == {"en euros"}:
        return "EUR"
    if not annoncees and source_id in UNITE_TUE:
        return "EUR"
    sys.exit(f"tableau de crédits : unité annoncée inconnue ou absente ({', '.join(sorted(annoncees)) or 'aucune'})")


def montants_des_cases(tableau, entete_, noms, largeurs):
    """(ligne, colonne, nombre) de chaque montant sous l'en-tête ; une case à cheval sur deux colonnes nommées
    différemment arrête l'import (une colonne sans intitulé, que certaines pages ajoutent pour la mise en page, ne
    compte pas)."""
    for r in range(entete_, len(tableau)):
        for c, x in enumerate(tableau[r]):
            nombre = nombre_texte(x) if c > 0 else None
            if c > 0 and not nombre and re.search(r"[0-9]", x):
                sys.exit(f"tableau de crédits, ligne {r} : montant illisible (« {x} »)")
            if not nombre:
                continue
            couvertes = {noms.get(c + dc) for dc in range(largeurs.get((r, c), 1))} - {None}
            if len(couvertes) != 1:
                sys.exit(f"tableau de crédits, ligne {r} : case à cheval sur deux colonnes, ou hors colonne")
            yield r, c, nombre


def blocs_des_etats(grilles, formes, flux, source_id):
    """Les tableaux de crédits de chaque état, chacun avec sa lettre d'état, sa catégorie et ses lignes."""
    intitules = list(re.finditer(ETAT, flux))
    resultat = []
    for n, m in enumerate(intitules):
        etat = lettre_etat(m.group(1), m.group(2))
        fin = intitules[n + 1].start() if n + 1 < len(intitules) else len(flux)
        tableaux = [int(k) for k in re.findall(r"⟦([0-9]+)⟧", flux[m.start():fin])]
        tableaux = [k for k in tableaux if not re.search(ETAT, " ".join(x for l in grilles[k] for x in l))]
        if not any(entete(grilles[k]) for k in tableaux):
            continue  # état sans tableau de crédits : recettes, autorisations de découvert
        ouvert, debut = None, m.start()  # debut : où commence le texte qui précède le prochain tableau
        for k in tableaux:
            t, forme = grilles[k], formes[k]
            e = entete(t)
            if e is None and ouvert is None:
                continue
            if e is not None:
                noms = {c: x for c, x in colonnes(t, e, forme["largeurs"]).items()
                        if categorie_nommee(x) is None or cle_colonne(x)}  # un intertitre n'est pas une colonne
                cles = {c: cle_colonne(x) for c, x in noms.items()}
                inconnues = sorted({x for c, x in noms.items() if cles[c] is None})
                if inconnues:
                    sys.exit(f"état {etat}, tableau {k} : colonne(s) inconnue(s) ({' ; '.join(inconnues)})")
                if ouvert is None:
                    avant = flux[debut:flux.index(f"⟦{k}⟧", debut)]
                    # L'intertitre qui nomme la catégorie précède le tableau, ou en ouvre la première ligne.
                    categorie = categorie_nommee(avant + " " + " ".join(x for l in t[:e] for x in l
                                                                        if not cle_colonne(propre(x))))
                    if categorie is None:
                        sys.exit(f"état {etat}, tableau {k} : catégorie de crédits introuvable")
                    ouvert = {"etat": etat, "categorie": categorie, "lignes": [], "noms": noms, "cles": cles,
                              "unite": unite_du_tableau(t, e, forme, avant, source_id), "total": None, "gras": set()}
                elif set(cles.values()) != set(ouvert["cles"].values()):
                    sys.exit(f"état {etat}, tableau {k} : colonnes autres que celles du tableau qu'il continue")
            else:
                e, noms, cles = 0, ouvert["noms"], ouvert["cles"]
                if max(len(l) for l in t) != max(noms) + 1:
                    sys.exit(f"état {etat}, tableau {k} : {max(len(l) for l in t)} colonnes, quand le tableau qu'il "
                             f"continue en a {max(noms) + 1}")
            textes_entete = {propre(x) for l in t[:e] for x in l if propre(x)} | set(noms.values())
            ouvert["gras"] |= {(k, r) for r, c in forme["gras"] if c == 0}
            par_ligne = {}
            for r, c, nombre in montants_des_cases(t, e, noms, forme["largeurs"]):
                par_ligne.setdefault(r, {})[cles[c]] = (c, nombre)
            for r in range(e, len(t)):
                libelle = propre(t[r][0])
                cases = {}
                for c, x in enumerate(t[r]):
                    if c in cles and not cases.get(cles[c], "").strip():
                        cases[cles[c]] = x  # une case fusionnée sur deux colonnes laisse vide la seconde
                valeurs = {cle: montant(x) for cle, x in cases.items()}
                vide = all(v is None for v in valeurs.values())
                if ouvert is None:
                    if libelle or not vide:
                        sys.exit(f"état {etat}, tableau {k}, ligne {r} : ligne après le total (« {libelle} »)")
                    continue
                if not libelle and vide:
                    continue
                if "(ligne supprimée)" in libelle:
                    if any(valeurs.values()):
                        sys.exit(f"état {etat}, tableau {k}, ligne {r} : ligne supprimée qui porte des crédits")
                    continue
                if vide and {propre(x) for x in t[r] if propre(x)} <= textes_entete:
                    continue  # en-tête répété
                if not libelle:
                    sys.exit(f"état {etat}, tableau {k}, ligne {r} : montants sans libellé")
                genre = "total" if re.fullmatch(r"(?i)totaux?|total", libelle) else \
                    "sous_total" if re.fullmatch(rf"(?i){SOUS_TOTAL}", libelle) else \
                    "dont" if re.fullmatch(rf"(?i){DONT}", libelle) else None
                if genre is None and re.match(r"(?i)(dont|totaux?|sous-total)\b", libelle):
                    sys.exit(f"état {etat}, tableau {k}, ligne {r} : ligne « {libelle} » inconnue")
                if genre == "dont" and vide:
                    continue  # une ligne « dont » sans montant : le programme ne touche pas aux dépenses de personnel
                if genre in ("total", "sous_total") and vide:
                    sys.exit(f"état {etat}, tableau {k}, ligne {r} : total sans montant")
                ligne = {"tableau": k, "ligne": r, "libelle": libelle, "nom": nom(libelle), "genre": genre,
                         "valeurs": {cle: v or 0 for cle, v in valeurs.items()}, "cases": par_ligne.get(r, {}),
                         "noms": noms, "vide": vide}
                ouvert["lignes"].append(ligne)
                if genre == "total":
                    ouvert["total"] = ligne
                    resultat.append(ouvert)
                    ouvert = None
            debut = flux.index(f"⟦/{k}⟧", debut) if f"⟦/{k}⟧" in flux[debut:] else debut
        if ouvert is not None:
            sys.exit(f"état {etat} : tableau sans ligne de total")
    return resultat


def egal(a, b):
    return all(abs(a.get(c, 0) - b.get(c, 0)) < 0.5 for c in set(a) | set(b))


def somme(lignes):
    total = {}
    for l in lignes:
        for c, v in l["valeurs"].items():
            total[c] = total.get(c, 0) + v
    return total


def nulle(ligne):
    return not any(ligne["valeurs"].values())


def montant_mission(mission, programmes):
    """Le montant d'une mission : celui de sa ligne, ou, quand la page ne l'imprime pas, celui de ses programmes."""
    return somme(programmes) if mission["vide"] else mission["valeurs"]


def par_marque(ordinaires, marquees):
    """[(mission, programmes)] si les lignes marquées (en gras, ou au contraire non en gras) sont les missions : la
    première ligne en est une, et chacune égale la somme des lignes qui la suivent jusqu'à la suivante, sauf si la page
    n'imprime pas son montant ; None sinon."""
    if not ordinaires or (ordinaires[0]["tableau"], ordinaires[0]["ligne"]) not in marquees:
        return None
    missions = []
    for l in ordinaires:
        if (l["tableau"], l["ligne"]) in marquees:
            missions.append((l, []))
        else:
            missions[-1][1].append(l)
    return missions if all(programmes and (m["vide"] or egal(somme(programmes), m["valeurs"]))
                           for m, programmes in missions) else None


def par_sommes(quoi, ordinaires, missions_connues):
    """[(mission, programmes)] d'après les seuls montants : une mission se ferme dès que ses programmes font son
    montant dans chaque colonne ; une ligne nulle qui suit est un programme de plus, sauf si c'est une mission connue
    de la base."""
    missions, i = [], 0
    while i < len(ordinaires):
        mission, programmes = ordinaires[i], []
        if mission["vide"]:
            sys.exit(f"{quoi} : la ligne « {mission['libelle']} », sans montant, ouvre une mission que rien ne marque")
        i += 1
        while not (programmes and egal(somme(programmes), mission["valeurs"])):
            if i == len(ordinaires):
                sys.exit(f"{quoi} : les programmes de la mission « {mission['libelle']} » ne font pas son montant")
            programmes.append(ordinaires[i])
            i += 1
        while i < len(ordinaires) and nulle(ordinaires[i]) and \
                f"LOLF.{code_lolf(ordinaires[i]['nom'])}" not in missions_connues:
            programmes.append(ordinaires[i])
            i += 1
        missions.append((mission, programmes))
    return missions


def par_sous_totaux(quoi, lignes):
    """[(mission, programmes, sous-total)] d'un état des budgets annexes jusqu'en 2009 : chaque budget annexe ouvre
    sur une ligne à son nom, sans montant, et se ferme sur sa ligne « Totaux hors amortissement », qui donne son
    montant et doit égaler la somme de ses programmes."""
    missions, courant = [], []
    for l in lignes:
        if l["genre"] is None:
            courant.append(l)
        elif l["genre"] == "sous_total":
            if len(courant) < 2 or not egal(somme(courant[1:]), l["valeurs"]) or \
                    not (courant[0]["vide"] or egal(courant[0]["valeurs"], l["valeurs"])):
                sys.exit(f"{quoi} : la ligne « {l['libelle']} » n'égale pas la somme des programmes qui la précèdent")
            missions.append((courant[0], courant[1:], l))
            courant = []
    if courant:
        sys.exit(f"{quoi} : des lignes après le dernier sous-total (« {courant[0]['libelle']} »)")
    return missions


def structure(bloc, missions_connues):
    """Rattache chaque ligne d'un tableau à sa mission : {(tableau, ligne) : (libellé, mission ou "")} ; vérifie les
    sommes. Les missions sont les lignes en gras, ou les autres, quand le tableau en marque ; sinon, elles se déduisent
    des montants (par_sommes)."""
    quoi = f"état {bloc['etat']}, {bloc['categorie']}"
    ordinaires = [l for l in bloc["lignes"] if l["genre"] is None]
    total = bloc["total"]["valeurs"]
    cles = {(l["tableau"], l["ligne"]) for l in ordinaires}
    gras = cles & bloc["gras"]
    rattache = {}
    if any(l["genre"] == "sous_total" for l in bloc["lignes"]):
        missions = []
        for mission, programmes, sous_total in par_sous_totaux(quoi, bloc["lignes"]):
            missions.append((mission, programmes))
            rattache[(sous_total["tableau"], sous_total["ligne"])] = (mission["nom"], "")
    else:
        missions = None
        if gras:
            for marquees in (gras, cles - gras):
                missions = par_marque(ordinaires, marquees)
                if missions and egal(somme([{"valeurs": montant_mission(m, p)} for m, p in missions]), total):
                    break
                missions = None
        if missions is None:
            if any(l["vide"] and not nulle(l) for l in ordinaires):
                sys.exit(f"{quoi} : ligne sans montant")
            if egal(somme(ordinaires), total):  # des missions seules
                if gras and gras != cles:
                    sys.exit(f"{quoi} : des missions seules, dont certaines seulement en gras")
                missions = [(l, []) for l in ordinaires]
            elif egal({c: v / 2 for c, v in somme(ordinaires).items()}, total):
                missions = par_sommes(quoi, ordinaires, missions_connues)
            else:
                sys.exit(f"{quoi} : ses lignes ne font ni son total ni deux fois son total")
    if not egal(somme([{"valeurs": montant_mission(m, p)} for m, p in missions]), total):
        sys.exit(f"{quoi} : la somme des missions ne fait pas le total")
    for mission, programmes in missions:
        for p in programmes:
            if nulle(p) and f"LOLF.{code_lolf(p['nom'])}" in missions_connues and \
                    code_lolf(p["nom"]) != code_lolf(mission["nom"]):
                sys.exit(f"{quoi} : la ligne nulle « {p['libelle']} », une mission connue, se range parmi les "
                         f"programmes de la mission « {mission['libelle']} »")
    for mission, programmes in missions:
        rattache[(mission["tableau"], mission["ligne"])] = (mission["nom"], "")
        for p in programmes:
            rattache[(p["tableau"], p["ligne"])] = (p["nom"], mission["nom"])
    # Une ligne « dont » appartient au programme qui la précède, et ne peut dépasser aucun de ses montants.
    precedent, lignes = None, {(l["tableau"], l["ligne"]): l for l in bloc["lignes"]}
    for l in bloc["lignes"]:
        if l["genre"] == "dont":
            if precedent is None or not rattache[precedent][1]:
                sys.exit(f"{quoi} : ligne « {l['libelle']} » hors programme (tableau {l['tableau']}, ligne {l['ligne']})")
            rattache[(l["tableau"], l["ligne"])] = rattache[precedent]
            programme = lignes[precedent]["valeurs"]
            if any(v > programme.get(c, 0) + 0.5 for c, v in l["valeurs"].items()):
                sys.exit(f"{quoi} : la ligne « {l['libelle']} » dépasse le programme « {lignes[precedent]['libelle']} » "
                         f"qu'elle détaille (tableau {l['tableau']}, ligne {l['ligne']})")
        elif l["genre"] is None:
            precedent = (l["tableau"], l["ligne"])
    return rattache


MONTANT = r"([0-9]{1,3}(?:[   ][0-9]{3})*) ?€"


def lire_montant(texte):
    return float(re.sub(r"\D", "", texte))


def articles(texte, annee):
    """[(état, catégories, sens, {colonne : montant}, phrase)] : ce qu'ouvre ou annule chaque article de la loi qui
    renvoie à un état. La phrase va de « Il est ouvert » (« Sont ouverts », « Il est annulé »…) à l'état ; une
    autorisation de découvert n'est pas un crédit."""
    lus = []
    for m in re.finditer(r"(?:Il est|Sont) (ouverts et annulés|ouvert|ouverts|ouvertes|annulé|annulés|annulées)\b", texte):
        fin = re.search(r"l’état ([A-G])((?:’|′|″){0,2}) ?annexé", texte[m.end():m.end() + 700])
        if fin is None:
            continue  # un article qui ne renvoie pas à un état : ouverture d'un compte, ratification d'un décret
        phrase = texte[m.start():m.end() + fin.end()]
        if re.search(r"(?:Il est|Sont) (?:ouvert|annul)", phrase[2:]):
            sys.exit(f"deux articles avant l'état qu'ils annoncent : « {phrase} »")
        if "découvert" in phrase:
            continue
        sens = {"OUVERTURES", "ANNULATIONS"} if "et annulés" in m.group(1) else \
            {"OUVERTURES"} if m.group(1).startswith("ouvert") else {"ANNULATIONS"}
        annees = set(re.findall(r"pour ([0-9]{4})", phrase))
        if annees - {annee}:  # un article peut taire l'année, que dit celui qui le précède
            sys.exit(f"article pour {', '.join(sorted(annees)) or 'aucune année'} dans une loi pour {annee} : « {phrase} »")
        titre = re.search(r"\b(?:au titre (?:des missions )?(?:du|des)|au) (budget général|budgets annexes|budget "
                          r"annexe «|comptes d’affectation spéciale|compte d’affectation spéciale «|comptes de concours "
                          r"financiers|compte de concours financiers «|comptes spéciaux)", phrase)
        if titre is None:
            sys.exit(f"article sans catégorie de crédits connue : « {phrase} »")
        categories = ("CAS", "CCF") if titre.group(1) == "comptes spéciaux" else \
            tuple(c for c, motif in NOMS_CATEGORIES.items() if re.search(motif, titre.group(1)))
        nombres = [lire_montant(x) for x in re.findall(MONTANT, phrase)]
        deux = re.search(r"des autorisations d’engagement et des crédits de paiement|une autorisation d’engagement et un "
                         r"crédit de paiement", phrase)
        separes = re.search(rf"des autorisations d’engagement (?:supplémentaires )?s’élevant à {MONTANT} et des crédits "
                            rf"de paiement (?:supplémentaires )?s’élevant à {MONTANT}", phrase)
        if deux and len(nombres) == 2 and "respectivement" in phrase:
            montants_ = {"AE": nombres[0], "CP": nombres[1]}
        elif deux and len(nombres) == 1:
            montants_ = {"AE": nombres[0], "CP": nombres[0]}
        elif separes and len(nombres) == 2:
            montants_ = {"AE": nombres[0], "CP": nombres[1]}
        elif re.search(r"(?:des autorisations|une autorisation) d’engagement", phrase) and \
                "crédit" not in re.split(r"autorisations? d’engagement", phrase, maxsplit=1)[1] and len(nombres) == 1:
            montants_ = {"AE": nombres[0]}
        elif re.search(r"\bdes crédits de paiement\b", phrase) and "autorisation" not in phrase and len(nombres) == 1:
            montants_ = {"CP": nombres[0]}
        elif re.search(r"\b(?:un crédit|des crédits) (?:supplémentaires? )?(?:de|s’élevant)", phrase) and \
                "autorisation" not in phrase and len(nombres) == 1:
            montants_ = {"CP": nombres[0], "un crédit": True}
        else:
            sys.exit(f"article illisible : « {phrase} »")
        lus.append((lettre_etat(fin.group(1), fin.group(2)), categories, sens, montants_, phrase))
    return lus


def verifier_articles(blocs, lus, source_id):
    """Le total de chaque tableau contre ce qu'ouvrent et annulent les articles qui renvoient à son état. Un article
    qui n'ouvre que des autorisations d'engagement laisse nuls les crédits de paiement, et inversement ; « un crédit »
    est un montant de crédits de paiement, avec autant d'autorisations d'engagement ou aucune."""
    attendus, libres = {}, set()  # (état, catégories) → {(colonne, sens) : montant} ; colonnes que l'article ne fixe pas
    for etat, categories, sens, montants_, phrase in lus:
        cible = attendus.setdefault((etat, categories), {})
        for s in sens:
            for colonne in ("AE", "CP"):
                if colonne in montants_:
                    cible[(colonne, s)] = cible.get((colonne, s), 0) + montants_[colonne]
                elif montants_.get("un crédit"):
                    libres.add((etat, categories, colonne, s))
                    cible.setdefault((colonne, s), 0)
                else:
                    cible.setdefault((colonne, s), 0)
    vus = set()
    for (etat, categories), montants_ in attendus.items():
        concernes = [b for b in blocs if b["etat"] == etat and b["categorie"] in categories]
        if not concernes:
            sys.exit(f"{source_id} : un article renvoie à l'état {etat} ({'+'.join(categories)}), qui n'a pas de tableau "
                     f"de ces crédits")
        for b in concernes:
            vus.add(id(b))
        for (colonne, s), attendu in montants_.items():
            lu = sum(b["total"]["valeurs"].get((colonne, s), 0) for b in concernes)
            if (etat, categories, colonne, s) in libres:
                cp = sum(b["total"]["valeurs"].get(("CP", s), 0) for b in concernes)
                if min(abs(lu), abs(lu - cp)) >= 0.5:
                    sys.exit(f"{source_id} : « un crédit » de l'état {etat} ({'+'.join(categories)}), avec {lu:,.0f} € "
                             f"d'autorisations d'engagement {s.lower()} dans l'état, ni zéro ni {cp:,.0f} €")
            elif abs(lu - attendu) >= 0.5:
                sys.exit(f"{source_id} : état {etat} ({'+'.join(categories)}), {colonne} {s.lower()} : {lu:,.0f} € dans "
                         f"l'état, {attendu:,.0f} € dans les articles")
    for b in blocs:
        if id(b) not in vus and any(b["total"]["valeurs"].values()):
            sys.exit(f"{source_id} : état {b['etat']}, {b['categorie']} : aucun article n'ouvre ni n'annule ces crédits")


def concept(categorie, colonne, sens, dont):
    return f"LOLF.{categorie}_{colonne}_LFR_{sens}" + ("_TITRE_2" if dont else "")


def chiffre(fichier, annee, concept_, fonction, unite_, nombre, emplacement, note="", traitement=""):
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement,
        "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept_, "fonction_id": fonction,
        "traitements": traitement,
        "unite_id": unite_, "periode": annee, "valeur": nombre[0], "decimales": nombre[1], "statut": "non_precise",
        "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": "non_consolide",
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions et les programmes."""
    chemin = BASE / fichier["chemin"]
    source_id = fichier["source_id"]
    grilles, formes, flux = lire_page_html(chemin)
    flux = INVISIBLES.sub("", flux)
    contenu = lire_texte_html(chemin)
    texte_brut = texte_html(contenu)
    # Pour lire les articles, une balise de mise en forme ne coupe pas un mot (« financ<span>iers</span> »).
    texte = normaliser(texte_html(re.sub(r"</?(?:span|a|b|i|em|strong|u|font)\b[^>]*>", "", contenu)))
    annees = set(re.findall(r"(?i)crédits?(?: supplémentaires?)?(?: ouverts?)?(?: et annulés)?(?: annulés)? pour "
                            r"([0-9]{4})|pour ([0-9]{4})(?:,)? par mission", flux))
    annees = {a or b for a, b in annees}
    if source_id in SANS_ETATS:
        annees = set(re.findall(r"Il est ouvert aux ministres, pour ([0-9]{4})", texte))
    if len(annees) != 1 or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année de la loi ({', '.join(sorted(annees)) or 'aucune'}) ou date du texte "
                 f"introuvable")
    annee = annees.pop()
    if fichier["mis_a_jour_source"][:4] != annee:
        sys.exit(f"{fichier['id']} : loi de finances rectificative pour {annee} dans un texte daté "
                 f"{fichier['mis_a_jour_source']}")
    lus = [] if source_id in SANS_ARTICLES else articles(texte, annee)
    if source_id in SANS_ETATS:
        yield from totaux_des_articles(fichier, annee, lus, texte_brut)
        return
    blocs = blocs_des_etats(grilles, formes, flux, source_id)
    if not blocs:
        sys.exit(f"{fichier['id']} : aucun état de crédits")
    if source_id not in SANS_ARTICLES:
        verifier_articles(blocs, lus, source_id)
    # Une coupure de mot de fin de ligne du texte imprimé, restée dans la page (« dévelop-pement »), se recolle quand
    # le mot entier figure ailleurs dans le texte.
    mots = set(re.findall(r"\w+", texte.lower()))
    recolle = lambda libelle: re.sub(r"(\w+)-(\w+)", lambda m: m.group(1) + m.group(2) if m.group(1)[-1].islower() and
                                     m.group(2)[0].islower() and (m.group(1) + m.group(2)).lower() in mots
                                     else m.group(0), libelle)
    missions_connues = {f for f, l in fonctions.items() if f.startswith("LOLF.") and not l["parent_id"]
                        and not f.startswith(("LOLF.RECETTES.", "LOLF.EMPLOIS."))}
    vus = {}
    note_page = SANS_ARTICLES.get(source_id, "")
    for bloc in blocs:
        rattache = structure(bloc, missions_connues)
        traitement = TRAITEMENTS.get((source_id, bloc["etat"]), "")
        note_unite = "La page n’annonce pas l’unité de l’état : ses totaux égalent, à l’euro, les montants des " \
                     "articles de la loi." if source_id in UNITE_TUE else ""
        for l in bloc["lignes"]:
            fonction = ""
            if l["genre"] != "total":
                libelle, mission = (recolle(x) for x in rattache[(l["tableau"], l["ligne"])])
                for x in (libelle, mission):
                    if (source_id, x) in LIBELLES:
                        LIBELLES_VUS.add((source_id, x))
                libelle, mission = (LIBELLES.get((source_id, x), x) for x in (libelle, mission))
                parent = f"LOLF.{code_lolf(mission)}" if mission else ""
                fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
                if parent:
                    fonctions.setdefault(parent, {"id": parent, "libelle": mission, "norme_id": "LOLF", "parent_id": ""})
                fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF",
                                                "parent_id": parent})
            for (colonne, sens), (c, nombre) in sorted(l["cases"].items()):
                if float(nombre[0]) == 0:
                    continue  # une case nulle dit qu'aucun crédit n'est ouvert ou annulé, comme une case vide
                concept_ = concept(bloc["categorie"], colonne, sens, l["genre"] == "dont")
                if (concept_, fonction, traitement) in vus:
                    sys.exit(f"{fichier['id']} : {concept_} de « {fonction or 'ensemble'} » lu deux fois (états "
                             f"{vus[(concept_, fonction, traitement)]} et {bloc['etat']})")
                vus[(concept_, fonction, traitement)] = bloc["etat"]
                yield chiffre(fichier, annee, concept_, fonction, "EUR", nombre,
                              f"tableau={l['tableau']};ligne={l['ligne']};colonne={c};libelle={l['libelle']};"
                              f"colonne_libelle={l['noms'][c]}",
                              " ".join(n for n in (note_unite, note_page) if n), traitement)
    absents = [x for s, x in LIBELLES if s == source_id and (s, x) not in LIBELLES_VUS]
    if absents:
        sys.exit(f"{fichier['id']} : libellé déclaré absent de la page ({' ; '.join(absents)})")


def totaux_des_articles(fichier, annee, lus, texte_brut):
    """Quand la page ne reproduit pas les états : le total de chaque catégorie, lu dans la phrase de l'article qui
    l'énonce. La phrase retenue va de la catégorie au montant, pour n'en porter qu'un nombre, et doit figurer telle
    quelle dans la page."""
    note = SANS_ETATS[fichier["source_id"]]
    vus = set()
    for etat, categories, sens, montants_, phrase in lus:
        if len(categories) != 1 or len(sens) != 1 or len({v for c, v in montants_.items() if c in ("AE", "CP")}) != 1:
            sys.exit(f"{fichier['id']} : article que l'import ne sait pas relire sans son état : « {phrase} »")
        montant_ = re.search(MONTANT, phrase)
        # L'extrait commence à la catégorie, ou après l'année quand elle la suit, pour ne porter qu'un nombre.
        debut = max([re.search(r"\bau titre\b|\bau compte\b", phrase).start()] +
                    [m.end() for m in re.finditer(r"pour [0-9]{4},? ", phrase[:montant_.start()])])
        # Le même extrait, tel que l'écrit la page : ses blancs et ses apostrophes peuvent différer du texte normalisé.
        motif = "".join(r"\s*['’]\s*" if x == "’" else r"\s+" if x == " " else re.escape(x)
                        for x in phrase[debut:montant_.end()])
        trouves = [m.group(0) for m in re.finditer(motif, texte_brut)]
        extrait = trouves[0] if len(trouves) == 1 else None
        if extrait is None or nombre_de_phrase(extrait) is None:
            sys.exit(f"{fichier['id']} : phrase introuvable, ou plusieurs fois, dans la page : "
                     f"« {phrase[debut:montant_.end()]} »")
        quoi = "L’article annule « un crédit », que la base lit comme des crédits de paiement. " \
            if montants_.get("un crédit") else ""
        for colonne in ("AE", "CP"):
            if colonne in montants_:
                concept_ = concept(categories[0], colonne, next(iter(sens)), False)
                if concept_ in vus:
                    sys.exit(f"{fichier['id']} : deux articles pour {concept_}")
                vus.add(concept_)
                yield chiffre(fichier, annee, concept_, "", "EUR", nombre_de_phrase(extrait), f"phrase={extrait}",
                              quoi + note)


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
