#!/usr/bin/env python3
"""Enregistre dans la base les chiffres d'un projet ou d'une loi d'approbation des comptes de l'État pour une année
(loi de règlement jusqu'aux comptes de 2022, loi relative aux résultats de la gestion et portant approbation des
comptes de l'année depuis), à partir de son texte publié par le Sénat (page HTML archivée).

    python3 outils/importer_lois_resultats.py <fichier_id>

Tableaux pris en charge :
- l'article 1er : résultat budgétaire de l'État, recettes et dépenses du budget général, des budgets annexes
  et des comptes spéciaux ;
- l'article 4 : autorisations d'engagement consommées et dépenses du budget général, par mission et par
  programme, avec les ouvertures et annulations de crédits que la loi y ajoute ;
- les articles 5 et 6 : les mêmes grandeurs pour chaque budget annexe et chaque compte spécial, compte par
  compte et programme par programme, avec les recettes, les majorations de découvert et les soldes des comptes
  spéciaux au 31 décembre, ainsi que les articles qui arrêtent à part les comptes spéciaux clos dans l'année
  (voir lignes_articles_5_6).

Les missions, les budgets annexes, les comptes spéciaux et leurs programmes sont les « fonctions » de la norme
LOLF : l'import les inscrit dans la table des fonctions à leur première apparition, sous un identifiant formé de
leur libellé. Dans l'article 4, une
mission est une ligne en gras, un programme une ligne maigre ou précédée d'un tiret ; un tableau sans gras
distingue ses programmes par le seul tiret. Un en-tête que le tableau répète après un saut de page du texte
imprimé est ignoré. Chaque libellé de ligne et de colonne doit avoir une correspondance
ci-dessous : un libellé inconnu arrête l'import, de même qu'une unité inconnue. Une case vide n'est pas un
chiffre. La version d'un chiffre est la date que le texte porte (enregistrement, transmission ou adoption) ;
les montants exécutés sont définitifs, comme le texte les qualifie, les ajustements de crédits ne reçoivent pas
de statut.
"""

import collections
import difflib
import re
import sys
import unicodedata

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire,
                    lire_tableaux_html, nombre_texte, table_des_chiffres, texte_html)

# Article 1er : libellé de ligne, sous sa forme de reconnaissance (voir cle), → {colonne : concept}. Dans la rubrique
# des budgets annexes, une ligne qui n'est pas ci-dessous est un budget annexe, c'est-à-dire une mission : ses
# colonnes vont dans BUDGET_ANNEXE.
BUDGET_ANNEXE = {"Dépenses": "LOLF.BA_DEPENSES_HORS_FDC", "Recettes": "LOLF.BA_RECETTES_HORS_FDC",
                 "Soldes": "LOLF.BA_SOLDE_HORS_FDC"}
REMBOURSEMENTS = {"Recettes": "LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS", "Dépenses": "LOLF.BG_REMBOURSEMENTS_DEGREVEMENTS"}
# Les comptes de 2006 portent en recettes le solde positif des comptes de commerce et d'opérations monétaires, les
# suivants en dépenses, de signe opposé.
OPERATIONS_MONETAIRES = {"Dépenses": "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_DEPENSES",
                         "Recettes": "LOLF.OPERATIONS_MONETAIRES_SOLDE_EN_RECETTES",
                         "Soldes": "LOLF.OPERATIONS_MONETAIRES_SOLDE"}
COMPTES_SPECIAUX = {"Dépenses": "LOLF.CS_DEPENSES", "Recettes": "LOLF.CS_RECETTES", "Soldes": "LOLF.SOLDE_COMPTES_SPECIAUX"}
ARTICLE_1 = {
    "Recettes fiscales brutes": {"Recettes": "LOLF.BG_RECETTES_FISCALES_BRUTES"},
    "À déduire : Remboursements et dégrèvements d’impôts d’État": REMBOURSEMENTS,
    "À déduire : Remboursements et dégrèvements d’impôts": REMBOURSEMENTS,  # libellé des textes jusqu'à 2023
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
    "Montant des budgets annexes hors fonds de concours": BUDGET_ANNEXE,  # sous-total des textes jusqu'à 2015
    "Total des budgets annexes y compris fonds de concours": {"Dépenses": "LOLF.BA_DEPENSES", "Recettes": "LOLF.BA_RECETTES",
                                                              "Soldes": "LOLF.SOLDE_BUDGETS_ANNEXES"},
    "Comptes d’affectation spéciale": {"Dépenses": "LOLF.CAS_DEPENSES", "Recettes": "LOLF.CAS_RECETTES",
                                       "Soldes": "LOLF.CAS_SOLDE"},
    "Comptes de concours financiers": {"Dépenses": "LOLF.CCF_DEPENSES", "Recettes": "LOLF.CCF_RECETTES",
                                       "Soldes": "LOLF.CCF_SOLDE"},
    "Comptes de commerce (solde)": {"Dépenses": "LOLF.COMPTES_COMMERCE_SOLDE_EN_DEPENSES",
                                    "Recettes": "LOLF.COMPTES_COMMERCE_SOLDE_EN_RECETTES",
                                    "Soldes": "LOLF.COMPTES_COMMERCE_SOLDE"},
    "Comptes d’opérations monétaires hors opérations avec le Fonds monétaire international (solde)": OPERATIONS_MONETAIRES,
    "Comptes d’opérations monétaires hors Fonds monétaire international (solde)": OPERATIONS_MONETAIRES,
    "Total des comptes spéciaux hors opérations avec le Fonds monétaire international": COMPTES_SPECIAUX,
    "Total des comptes spéciaux hors Fonds monétaire international": COMPTES_SPECIAUX,
    "Résultat budgétaire de l’État hors opérations avec le Fonds monétaire international":
        {"Soldes": "LOLF.RESULTAT_BUDGETAIRE"},
    # Jusqu'aux comptes de 2012, le tableau se termine par le solde d'exécution des lois de finances, sans les budgets
    # annexes, présentés en équilibre.
    "Solde d’exécution des lois de finances hors Fonds monétaire international": {"Soldes": "LOLF.RESULTAT_EXECUTION"},
    "À déduire : Prélèvements sur recettes au profit des collectivités territoriales et des Communautés européennes (d)":
        {"Recettes": "LOLF.BG_PRELEVEMENTS_SUR_RECETTES"},
    # Lignes propres aux comptes de 2006 et de 2007.
    "Recettes non fiscales hors fonds de stabilisation des changes (b)": {"Recettes": "LOLF.BG_RECETTES_NON_FISCALES"},
    "Total net des recettes hors fonds de stabilisation des changes hors prélèvements sur recettes (e = c - d)":
        {"Recettes": "LOLF.BG_RECETTES_NETTES_HORS_PSR"},
    "Montant net des recettes hors fonds de stabilisation des changes y compris fonds de concours (g = e + f)":
        {"Recettes": "LOLF.BG_RECETTES_NETTES"},
    "Montant net des dépenses y compris fonds de concours hors mesure de régularisation concernant les pensions "
    "(j’) = (h) + (i)": {"Dépenses": "LOLF.BG_DEPENSES_NETTES_HORS_REGULARISATION_PENSIONS"},
    "Total du budget général y compris fonds de concours hors mesure de régularisation concernant les pensions":
        {"Dépenses": "LOLF.BG_DEPENSES_NETTES_HORS_REGULARISATION_PENSIONS", "Recettes": "LOLF.BG_RECETTES_NETTES",
         "Soldes": "LOLF.SOLDE_BUDGET_GENERAL_HORS_REGULARISATION_PENSIONS"},
    "Solde d’exécution des lois de finances hors Fonds de stabilisation des changes hors Fonds monétaire international":
        {"Soldes": "LOLF.RESULTAT_EXECUTION"},
    "Solde d’exécution des lois de finances hors Fonds de stabilisation des changes hors Fonds monétaire international "
    "et hors mesure de régularisation concernant les pensions":
        {"Soldes": "LOLF.RESULTAT_EXECUTION_HORS_REGULARISATION_PENSIONS"},
    "Solde d’exécution des lois de finances hors Fonds monétaire international et hors produits de cession des titres "
    "EDF": {"Soldes": "LOLF.RESULTAT_EXECUTION_HORS_CESSION_TITRES_EDF"},
}
# Précision qu'un libellé ajoute au concept commun auquel il se rattache, portée par la note du chiffre.
PRECISIONS = {
    "hors fonds de stabilisation des changes": "Le texte de 2006 présente ses recettes non fiscales, et les totaux et "
        "soldes qui en découlent, hors fonds de stabilisation des changes.",
}
RUBRIQUES_ARTICLE_1 = {"Budget général", "Recettes", "Dépenses", "Budgets annexes", "Comptes spéciaux"}

# Article 4 : intitulé de colonne → concept, pour le tableau des autorisations d'engagement et celui des dépenses.
ARTICLE_4 = {
    "Autorisations d’engagement consommées": "LOLF.BG_AE_CONSOMMEES",
    "Autorisations d’engagement engagées": "LOLF.BG_AE_CONSOMMEES",  # libellé des textes jusqu'aux comptes de 2012
    "Ouvertures d’autorisations d’engagement complémentaires": "LOLF.BG_AE_OUVERTURES",
    "Annulations d’autorisations d’engagement non consommées et non reportées": "LOLF.BG_AE_ANNULATIONS",
    "Annulations d’autorisations d’engagement non engagées et non reportées": "LOLF.BG_AE_ANNULATIONS",
    "Dépenses": "LOLF.BG_DEPENSES_BRUTES",
    "Ouvertures de crédits complémentaires": "LOLF.BG_CP_OUVERTURES",
    "Annulations de crédits non consommés et non reportés": "LOLF.BG_CP_ANNULATIONS",
}
NOTE_ASTERISQUE = "Le montant porte un astérisque d’appel de note : la note sous le tableau le précise."
# Libellés fautifs de l'un des deux tableaux de l'article 4, que l'autre donne correctement : (source, libellé) →
# libellé correct. L'emplacement du chiffre garde le libellé de la page.
LIBELLES_CORRIGES = {
    ("senat.pjl15-785", "- Conduite et pilotage des politiques économique et financière"):
        "- Conduite et pilotage des politiques économiques et financières",
    ("senat.pjl24-032", "- Haute Cour. . . . . . . . . . . . . . . . . . . . . . . .u"): "- Haute Cour",
}
# Articles 5 et 6 : budgets annexes et comptes spéciaux, compte par compte. Intitulé de colonne → mesure ; le concept
# d'un chiffre est « LOLF.<catégorie>_<mesure> ».
MESURES = {
    "Autorisations d’engagement consommées": "AE_CONSOMMEES",
    "Autorisations d’engagement engagées": "AE_CONSOMMEES",
    "Autorisations d’engagement": "AE_CONSOMMEES",
    "Ouvertures d’autorisations d’engagement complémentaires": "AE_OUVERTURES",
    "Annulations d’autorisations d’engagement non consommées et non reportées": "AE_ANNULATIONS",
    "Annulations d’autorisations d’engagement non engagées et non reportées": "AE_ANNULATIONS",
    "Dépenses": "DEPENSES",
    "Recettes": "RECETTES",
    "Ouvertures de crédits complémentaires": "CP_OUVERTURES",
    "Annulations de crédits non consommés et non reportés": "CP_ANNULATIONS",
    "Annulations des crédits non consommés et non reportés": "CP_ANNULATIONS",
    "Annulations des crédits non consommés et non reportes": "CP_ANNULATIONS",
    "Majorations du découvert": "MAJORATIONS_DECOUVERT",
    "Débiteurs": "SOLDES_DEBITEURS",
    "Débiteur": "SOLDES_DEBITEURS",
    "Créditeurs": "SOLDES_CREDITEURS",
    "Créditeur": "SOLDES_CREDITEURS",
}
# Rubriques des comptes spéciaux → catégorie. Les comptes de commerce et d'opérations monétaires n'ont pas de programmes.
CATEGORIES = {"Comptes d’affectation spéciale": "CAS", "Comptes de concours financiers": "CCF",
              "Comptes de commerce": "COMPTES_COMMERCE", "Comptes d’opérations monétaires": "OPERATIONS_MONETAIRES",
              "Compte de commerce": "COMPTES_COMMERCE"}  # au singulier dans le tableau d'un compte clos
SANS_PROGRAMMES = {"COMPTES_COMMERCE", "OPERATIONS_MONETAIRES"}
# Lignes d'un budget annexe qui ne sont pas des programmes mais des composantes de son total → libellé retenu.
COMPOSANTES_BUDGET_ANNEXE = {"Augmentation du fonds de roulement": "Augmentation du fonds de roulement",
                             "Augmentation du fonds de roulement (ligne d’équilibre)": "Augmentation du fonds de roulement",
                             "Fonds de concours": "Fonds de concours"}
# Regroupements des textes jusqu'aux comptes de 2010 : comptes dotés de crédits, comptes dotés de découverts. Le total
# général d'un tableau porte sur les catégories qu'il présente.
GROUPES = {"crédits": "CS_A_CREDITS", "découvert": "CS_A_DECOUVERT"}
TOTAUX_GENERAUX = {frozenset({"CAS", "CCF"}): "CS_A_CREDITS", frozenset({"COMPTES_COMMERCE", "OPERATIONS_MONETAIRES"}): "CS_A_DECOUVERT",
                   frozenset(CATEGORIES.values()): "CS_ENSEMBLE"}
# Mesures de chaque catégorie : les comptes à crédits (budgets annexes, comptes d'affectation spéciale, de concours
# financiers) ont des autorisations d'engagement et des crédits, les comptes à découvert (de commerce, d'opérations
# monétaires) des découverts. Une mesure hors de sa catégorie arrête l'import.
MESURES_A_CREDITS = {"AE_CONSOMMEES", "AE_OUVERTURES", "AE_ANNULATIONS", "DEPENSES", "RECETTES", "CP_OUVERTURES",
                     "CP_ANNULATIONS", "SOLDES_DEBITEURS", "SOLDES_CREDITEURS"}
MESURES_A_DECOUVERT = {"DEPENSES", "RECETTES", "MAJORATIONS_DECOUVERT", "SOLDES_DEBITEURS", "SOLDES_CREDITEURS"}
# Intitulés de colonne que le texte contredit : (source, catégorie, intitulé) → (intitulé retenu, explication).
NOTE_2022 = ("Le texte présente les comptes de commerce et d’opérations monétaires sous l’en-tête des comptes dotés de "
             "crédits (« Annulations de crédits non consommés et non reportés »), dans la page du Sénat comme dans le "
             "texte imprimé. Ces comptes sont dotés de découverts et non de crédits, et l’article 6 dit que les "
             "découverts autorisés sont modifiés comme l’indiquent ses tableaux : le montant est une majoration du "
             "découvert, comme les autres années.")
COLONNES_CONTREDITES = {
    ("senat.pjl22-684", "COMPTES_COMMERCE", "Annulations de crédits non consommés et non reportés"):
        ("Majorations du découvert", NOTE_2022),
    ("senat.pjl22-684", "OPERATIONS_MONETAIRES", "Annulations de crédits non consommés et non reportés"):
        ("Majorations du découvert", NOTE_2022),
}
# Le texte de 2006 présente les budgets annexes de l'article 5 hors fonds de concours, les suivants fonds de concours
# compris : les identifiants partagés avec l'article 1er et les ventilations le vérifient.
BUDGETS_ANNEXES_HORS_FDC = {"senat.pjl06-389"}
MESURES_AJUSTEMENTS = {"AE_OUVERTURES", "AE_ANNULATIONS", "CP_OUVERTURES", "CP_ANNULATIONS", "MAJORATIONS_DECOUVERT"}
MESURES_SOLDES = {"SOLDES_DEBITEURS", "SOLDES_CREDITEURS"}

AJUSTEMENTS = {"LOLF.BG_AE_OUVERTURES", "LOLF.BG_AE_ANNULATIONS", "LOLF.BG_CP_OUVERTURES", "LOLF.BG_CP_ANNULATIONS"}
SOLDES = {c for lignes in ARTICLE_1.values() for colonne, c in lignes.items() if colonne == "Soldes"} | {"LOLF.BA_SOLDE_HORS_FDC"}

# Unité annoncée en tête de tableau, « (En euros) » par exemple.
UNITES = {"en euros": "EUR", "en millions d’euros": "MIO_EUR"}
# Unités annoncées que les montants du tableau contredisent : (source, intitulé de sa première colonne de montants,
# unité annoncée) → (unité des montants, explication portée par chacun d'eux).
UNITES_CONTREDITES = {
    ("senat.pjl24-032", "Autorisations d’engagement consommées", "en millions d’euros"): (
        "EUR", "Le tableau annonce des millions d’euros, dans la page du Sénat comme dans le texte imprimé, mais ses "
               "montants sont en euros : ils ont des centimes, et leur total (590 784 984 819,29) est du même ordre "
               "que celui des dépenses du tableau suivant, annoncé en euros (591 887 384 714,81)."),
}


# Année des comptes : la seule que le texte désigne par « budget de l'année » ou « comptes de l'année ».
ANNEE = r"(?:budget|comptes) de l[’'] ?année ([0-9]{4})"


def propre(texte):
    """Libellé sans points de conduite, avec un seul type de tiret et d'apostrophe."""
    texte = texte.replace("–", "-").replace("−", "-").replace("'", "’")
    return re.sub(r"^(\s*\.)+|(\s*\.)+\s*$", "", texte).strip()


def cle(libelle):
    """Forme d'un libellé qui sert à le reconnaître : ponctuation et formules écrites d'une seule façon.
    « Montant net des recettes, hors fonds de concours (c) = (a) + (b) » se reconnaît comme
    « Montant net des recettes hors fonds de concours (c = a + b) »."""
    texte = re.sub(r"\s*,\s+(hors|y compris)\b", r" \1", re.sub(r"\s*:\s*", " : ", libelle))
    texte = re.sub(r"\s+", " ", texte).strip()
    formule = re.search(r"\(([a-z]) ?\) ?= ?((?:\([a-z] ?\) ?[-+] ?)+\([a-z] ?\))$", texte)
    if formule:
        termes = re.sub(r" ?([-+]) ?", r" \1 ", re.sub(r"\(([a-z]) ?\)", r"\1", formule.group(2)))
        texte = f"{texte[:formule.start()]}({formule.group(1)} = {termes})"
    return texte


def code_lolf(libelle):
    """Identifiant formé d'un libellé : « Action extérieure de l’État » → ACTION_EXTERIEURE_DE_LETAT."""
    ascii_ = unicodedata.normalize("NFKD", libelle).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "_", ascii_.upper()).strip("_")


def unite_annoncee(texte):
    trouve = re.fullmatch(r"\((en [^)*]+)\*?\)", propre(texte), re.I)
    return trouve.group(1).lower() if trouve else None


def colonnes(tableau, entete, largeurs):
    """Intitulé de chaque colonne : le dernier texte non vide des lignes d'en-tête qui la couvre, unité exceptée."""
    noms = {}
    for r, ligne in enumerate(tableau[:entete]):
        for c, texte in enumerate(ligne):
            if propre(texte) and c > 0 and unite_annoncee(texte) is None:
                for dc in range(largeurs.get((r, c), 1)):
                    noms[c + dc] = propre(texte)
    return noms


def unite(tableau, entete, noms, forme, source_id):
    """(unité, note) des montants d'un tableau, d'après l'unité annoncée dans ses lignes d'en-tête ou, à défaut, dans
    sa légende."""
    annoncees = {unite_annoncee(x) for l in tableau[:entete] for x in l} - {None} or \
        {unite_annoncee(forme["legende"])} - {None}
    if len(annoncees) != 1 or next(iter(annoncees)) not in UNITES:
        sys.exit(f"tableau « {noms.get(1)} » : unité annoncée inconnue ou absente ({annoncees or 'aucune'})")
    annoncee = next(iter(annoncees))
    return UNITES_CONTREDITES.get((source_id, noms.get(1), annoncee), (UNITES[annoncee], ""))


def montants(tableau, entete, noms, largeurs):
    """(ligne, colonne, nombre) de chaque montant sous l'en-tête ; une case à cheval sur deux colonnes d'intitulés
    différents arrête l'import."""
    for r in range(entete, len(tableau)):
        for c, x in enumerate(tableau[r]):
            nombre = nombre_texte(x) if c > 0 else None
            if c > 0 and not nombre and re.search(r"[0-9]", x):
                sys.exit(f"tableau « {noms.get(1)} », ligne {r} : montant illisible (« {x} »)")
            if not nombre:
                continue
            if len({noms.get(c + dc) for dc in range(largeurs.get((r, c), 1))}) > 1:
                sys.exit(f"tableau « {noms.get(1)} », ligne {r} : case à cheval sur deux colonnes")
            yield r, c, nombre


def article_1(tableaux):
    """(indice, tableau) de l'article 1er : celui qui se termine par le résultat budgétaire, ou jusqu'aux comptes de
    2012 par le solde d'exécution des lois de finances."""
    for i, t in enumerate(tableaux):
        if any(propre(l[0]).startswith(("Résultat budgétaire de l’État", "Solde d’exécution des lois de finances"))
               for l in t if l):
            return i, t
    sys.exit("tableau de l'article 1er introuvable")


def lignes_article_1(i, tableau, forme, source_id):
    """Un libellé coupé sur deux lignes, dont la seconde commence par une minuscule et la première ne porte aucun
    montant, se lit d'un seul tenant quand il a ainsi une correspondance ; une ligne sans libellé qui porte des
    montants, sous un libellé connu qui n'en porte aucun, prend ce libellé. Un montant pris dans une case fusionnée sur plusieurs lignes, dont le texte
    reste dans la première, va à la seule ligne du bloc dont le libellé a une correspondance pour sa colonne ;
    l'emplacement reste celui de la case."""
    entete = next(r for r, l in enumerate(tableau) if "Soldes" in [propre(x) for x in l]) + 1
    noms = colonnes(tableau, entete, forme["largeurs"])
    unite_, note_unite = unite(tableau, entete, noms, forme, source_id)
    libelles, rubriques, rubrique, decales = {}, {}, "", set()
    for r in range(entete, len(tableau)):
        libelle, precedent = propre(tableau[r][0]), libelles.get(r - 1, "")
        precedent_vide = r > entete and not any(nombre_texte(x) for x in tableau[r - 1][1:])
        if not libelle and cle(precedent) in ARTICLE_1 and precedent_vide and any(nombre_texte(x) for x in tableau[r][1:]):
            libelle = precedent
            decales.add(r)
        elif libelle[:1].islower() and cle(f"{precedent} {libelle}") in ARTICLE_1 and precedent_vide:
            libelle = f"{precedent} {libelle}"
        libelles[r] = libelle
        rubrique = cle(libelle) if cle(libelle) in RUBRIQUES_ARTICLE_1 else rubrique
        rubriques[r] = rubrique

    def correspondance(r):
        if cle(libelles[r]) in ARTICLE_1:
            return ARTICLE_1[cle(libelles[r])], ""
        if rubriques[r] == "Budgets annexes" and libelles[r] and cle(libelles[r]) not in RUBRIQUES_ARTICLE_1 and \
                not libelles[r].lower().startswith(("total", "fonds", "dont")):
            return BUDGET_ANNEXE, (libelles[r], "")
        return {}, ""

    for r, c, nombre in montants(tableau, entete, noms, forme["largeurs"]):
        bloc = range(r, r + forme["fusions"].get((r, c), 1))
        cibles = [s for s in bloc if noms.get(c) in correspondance(s)[0]]
        if len(cibles) != 1:
            sys.exit(f"article 1er, ligne {r}, colonne « {noms.get(c)} » : {len(cibles)} correspondance(s) pour "
                     f"« {' / '.join(libelles[s] for s in bloc)} »")
        concepts, fonction = correspondance(cibles[0])
        notes = [f"Case fusionnée sur les lignes {r} à {bloc[-1]} du tableau ; le montant est celui de la seule ligne "
                 f"chiffrée du bloc." if len(bloc) > 1 else "",
                 "Montant porté une ligne sous son libellé." if cibles[0] in decales else "", note_unite]
        notes += [n for motif, n in PRECISIONS.items() if motif in cle(libelles[cibles[0]]).lower()]
        yield {"tableau": i, "ligne": r, "colonne": c, "libelle": libelles[cibles[0]], "intitule": noms[c],
               "concept": concepts[noms[c]], "fonction": fonction, "nombre": nombre, "unite": unite_,
               "note": " ".join(n for n in notes if n)}


def lignes_article_4(tableaux, formes, source_id, recolle):
    """Les deux tableaux de l'article 4, autorisations d'engagement puis dépenses, listent les mêmes missions et
    programmes dans le même ordre : chaque ligne doit désigner la même fonction dans l'un et l'autre, et une ligne en
    gras dans l'un est une mission dans les deux."""
    numeros = [i for i, t in enumerate(tableaux) if t and any(propre(x).startswith("Désignation des missions")
                                                               for l in t[:3] for x in l)]
    if len(numeros) != 2:
        sys.exit(f"article 4 : {len(numeros)} tableau(x) de missions au lieu de deux")
    lus = []
    for i in numeros:
        t, forme = tableaux[i], formes[i]
        entete = next(r for r, l in enumerate(t) if any("Ouvertures" in x for x in l)) + 1
        noms = colonnes(t, entete, forme["largeurs"])
        textes_entete = {propre(x) for l in t[:entete] for x in l if propre(x)}
        # Une ligne vide, ou un en-tête répété après un saut de page du texte imprimé, ne compte pas.
        lignes = [r for r in range(entete, len(t)) if propre(t[r][0]) and
                  not {propre(x) for x in t[r] if propre(x)} <= textes_entete]
        lus.append({"i": i, "t": t, "forme": forme, "entete": entete, "noms": noms, "lignes": lignes,
                    "unite": unite(t, entete, noms, forme, source_id)})
    if len(lus[0]["lignes"]) != len(lus[1]["lignes"]):
        sys.exit(f"article 4 : {len(lus[0]['lignes'])} lignes dans un tableau, {len(lus[1]['lignes'])} dans l'autre")
    gras_present = any((r, 0) in lu["forme"]["gras"] for lu in lus for r in lu["lignes"])
    structure, mission = [], None
    for position, rangs in enumerate(zip(*(lu["lignes"] for lu in lus))):
        bruts = [propre(lu["t"][r][0]) for lu, r in zip(lus, rangs)]
        nets = [recolle(re.sub(r"^[-+]+\s*", "", LIBELLES_CORRIGES.get((source_id, b), b))) for b in bruts]
        if code_lolf(nets[0]) != code_lolf(nets[1]):
            sys.exit(f"article 4, ligne {position + 1} : « {bruts[0]} » d'un côté, « {bruts[1]} » de l'autre")
        tiret = any(b.startswith(("-", "+")) for b in bruts)
        gras = any((r, 0) in lu["forme"]["gras"] for lu, r in zip(lus, rangs))
        if nets[0].lower().startswith("total"):
            if nets[0].lower() != "total":
                sys.exit(f"article 4, ligne {position + 1} : total inattendu (« {bruts[0]} »)")
            structure.append("")
        elif tiret and gras:
            sys.exit(f"article 4, ligne {position + 1} : ligne en gras précédée d'un tiret (« {bruts[0]} »)")
        elif gras or not (gras_present or tiret):
            mission = nets[0]
            structure.append((nets[0], ""))
        elif mission is None:
            sys.exit(f"article 4, ligne {position + 1} : programme hors mission (« {bruts[0]} »)")
        else:
            structure.append((nets[0], mission))
    for lu in lus:
        types = dict(zip(lu["lignes"], structure))
        unite_, note = lu["unite"]
        for r, c, nombre in montants(lu["t"], lu["entete"], lu["noms"], lu["forme"]["largeurs"]):
            if r not in types:
                sys.exit(f"article 4, tableau {lu['i']}, ligne {r} : montant sans libellé")
            if lu["noms"].get(c) not in ARTICLE_4:
                sys.exit(f"article 4, tableau {lu['i']}, ligne {r} : colonne « {lu['noms'].get(c)} » sans correspondance")
            yield {"tableau": lu["i"], "ligne": r, "colonne": c, "libelle": propre(lu["t"][r][0]),
                   "intitule": lu["noms"][c], "concept": ARTICLE_4[lu["noms"][c]], "fonction": types[r],
                   "nombre": nombre, "unite": unite_, "note": note}


def est_entete(cellules):
    """Une ligne d'en-tête : tous ses textes sont la désignation, l'unité ou des intitulés de colonne."""
    textes = [propre(c) for c in cellules if propre(c)]
    return bool(textes) and all(t in MESURES or unite_annoncee(t) or t.startswith(
        ("Désignation", "des comptes spéciaux", "des budgets annexes", "Ajustements de la loi", "Opérations de l’année",
         "Soldes au 31 décembre", "Solde au 31 décembre")) for t in textes)


def famille(tableau, forme):
    """BA (budgets annexes), CS (comptes spéciaux) ou CLOS (compte spécial clos, arrêté par un article à part)."""
    designation = next(propre(c) for l in tableau[:4] for c in l if propre(c).startswith("Désignation"))
    legende = forme["legende"]
    if "compte spécial" in designation or re.search(r"\b(?:du|sur le) compte spécial\b", legende):
        return "CLOS"
    for texte in (designation, legende):
        if "budgets annexes" in texte:
            return "BA"
        if re.search(r"comptes spécia", texte):
            return "CS"
    sys.exit(f"tableau « {designation} » : budgets annexes ou comptes spéciaux ?")


def segments_de_comptes(tableaux, formes, source_id):
    """Les tableaux des articles 5 et 6, découpés en segments : chacun sous son bloc d'en-tête, car une même grille
    en réunit parfois deux. Un tableau sans désignation, dont l'en-tête ne porte que des intitulés de colonne de ces
    articles, prolonge le tableau de comptes qui le précède. Un tableau à montants sans en-tête qui suit un tableau de
    comptes, sans texte entre eux, le prolonge aussi, sur les mêmes colonnes : la page de 2008 coupe ainsi en trois,
    sans en répéter l'en-tête, le tableau des autorisations d'engagement des comptes spéciaux. Un autre tableau à
    montants entre deux tableaux de comptes arrête l'import. Les tableaux d'un compte spécial clos dans l'année, que
    le texte arrête à part, forment la famille CLOS."""
    segments, precedente, lus, ignores = [], None, [], []
    for i, t in enumerate(tableaux):
        if not t:
            continue
        suite, a_montants = None, any(nombre_texte(x) for l in t for x in l[1:])
        if any(propre(c).startswith("Désignation") and "missions" not in propre(c) for l in t[:4] for c in l):
            fam = famille(t, formes[i])
        elif precedente and est_entete(t[0]) and any(propre(c) in MESURES for l in t[:4] if est_entete(l) for c in l):
            fam = precedente
        elif a_montants and segments and segments[-1]["i"] == i - 1 and not formes[i]["legende"] and not est_entete(t[0]):
            suite, fam = segments[-1], precedente
            if len(t[0]) != len(suite["t"][0]):
                sys.exit(f"tableau {i} : suite sans en-tête du tableau {i - 1}, sur {len(t[0])} colonnes au lieu de "
                         f"{len(suite['t'][0])}")
        else:
            if a_montants:
                ignores.append(i)
            continue
        precedente = fam
        lus.append(i)
        bloc, unite_tableau = [], suite and suite["unite"]
        courant = {**suite, "i": i, "t": t, "forme": formes[i], "lignes": []} if suite else None
        for r, ligne in enumerate(t):
            if est_entete(ligne):
                if courant is not None:
                    segments.append(courant)
                    courant, bloc = None, []
                bloc.append(r)
            elif any(propre(c) for c in ligne):
                if courant is None:
                    if not bloc:
                        sys.exit(f"tableau {i}, ligne {r} : montants sans en-tête")
                    noms = colonnes(t[bloc[0]:bloc[-1] + 1], bloc[-1] - bloc[0] + 1,
                                    {(rr - bloc[0], c): l for (rr, c), l in formes[i]["largeurs"].items()})
                    mesures = {MESURES[n] for n in noms.values() if n in MESURES}
                    genre = "AE" if any(m.startswith("AE_") for m in mesures) else \
                        "SOLDES" if mesures & MESURES_SOLDES else "OPERATIONS"
                    # L'unité annoncée en tête du tableau vaut pour tous ses segments.
                    entete_ = t[bloc[0]:bloc[-1] + 1]
                    if bloc[0] > 0 and not any(unite_annoncee(c) for l in entete_ for c in l) and unite_tableau:
                        unite_ = unite_tableau
                    else:
                        unite_ = unite(entete_, len(entete_), noms, formes[i] if bloc[0] == 0 else
                                       {**formes[i], "legende": ""}, source_id)
                    unite_tableau = unite_tableau or unite_
                    courant = {"famille": fam, "genre": genre, "i": i, "t": t, "forme": formes[i], "noms": noms,
                               "unite": unite_, "lignes": []}
                courant["lignes"].append(r)
        if courant is not None:
            segments.append(courant)
    entre = [i for i in ignores if lus and lus[0] < i < lus[-1]]
    if entre:
        sys.exit(f"tableaux {entre} : montants entre deux tableaux de comptes, ni en-tête ni suite d'un tableau")
    return segments


def structure_des_comptes(segs, fam, recolle, source_id):
    """Les lignes d'un tableau de comptes (segments d'une même famille et d'un même genre), avec leur rôle : rubrique
    de catégorie, total, composante d'un budget annexe, ou ligne de compte ou de programme, à départager ensuite."""
    lignes, categorie = [], "BA" if fam == "BA" else None
    for seg in segs:
        t = seg["t"]
        for r in seg["lignes"]:
            brut = propre(t[r][0])
            chiffres = any(nombre_texte(x) for x in t[r][1:])
            if not brut:
                if chiffres:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : montants sans libellé")
                continue
            cle_ = cle(brut)
            groupe = re.fullmatch(r"(?i)(?:[ab]\.?\s*-?\s*)?comptes à (crédits|découvert)", cle_)
            total = re.fullmatch(r"(?i)tota(?:l|ux)(?: (?:des?|du) | )?(.*)", cle_)
            if fam in ("CS", "CLOS") and cle_ in CATEGORIES:
                categorie = CATEGORIES[cle_]
                lignes.append({"seg": seg, "r": r, "role": "rubrique", "cible": categorie})
            elif groupe:
                if chiffres:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : montants sur la rubrique « {brut} »")
            elif total:
                reste = total.group(1).lower()
                cibles = {k.lower(): v for k, v in CATEGORIES.items()}
                if reste in cibles:
                    cible = cibles[reste]
                elif reste == "budgets annexes" and fam == "BA":
                    cible = "BA"
                elif re.fullmatch(r"comptes à (crédits|découvert)", reste):
                    cible = GROUPES[reste.split()[-1]]
                elif reste in ("", "général", "comptes spéciaux"):
                    cible = "BA" if fam == "BA" else None  # total général, fixé d'après les rubriques présentes
                else:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : total inattendu (« {brut} »)")
                lignes.append({"seg": seg, "r": r, "role": "total", "cible": cible})
            elif categorie is None or re.match(r"(?i)tota", cle_):
                sys.exit(f"tableau {seg['i']}, ligne {r} : compte hors rubrique ou total inconnu (« {brut} »)")
            elif fam == "BA" and cle_ in COMPOSANTES_BUDGET_ANNEXE:
                lignes.append({"seg": seg, "r": r, "role": "composante", "categorie": categorie, "brut": brut,
                               "net": COMPOSANTES_BUDGET_ANNEXE[cle_]})
            else:
                lignes.append({"seg": seg, "r": r, "role": "ligne", "categorie": categorie, "brut": brut,
                               "tiret": brut.startswith(("-", "+")), "gras": (r, 0) in seg["forme"]["gras"],
                               "net": recolle(re.sub(r"^(?:[-+]+|\d+\.\s*-)\s*", "",
                                                     LIBELLES_CORRIGES.get((source_id, brut), brut)))})
    presentes = frozenset(l["cible"] for l in lignes if l["role"] == "rubrique")
    for l in lignes:
        if l["role"] == "total" and l["cible"] is None:
            if fam == "CLOS" and len(presentes) == 1:
                l["cible"] = next(iter(presentes))
            elif presentes in TOTAUX_GENERAUX:
                l["cible"] = TOTAUX_GENERAUX[presentes]
            else:
                sys.exit(f"tableau {l['seg']['i']}, ligne {l['r']} : total général de {sorted(presentes)}")
    return lignes


def proches(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= 0.85


def apparier(a, b, quoi):
    """Les lignes de deux tableaux qui se correspondent, alignées dans l'ordre : (ligne de a, ligne de b) ; une ligne
    que l'autre tableau ne présente pas reste seule. Deux lignes appariées doivent avoir des libellés presque
    identiques ; un remplacement de plusieurs lignes par un autre nombre de lignes arrête l'import."""
    cles = lambda lignes: [(l["categorie"], code_lolf(l["net"])) for l in lignes]
    paires = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, cles(a), cles(b), autojunk=False).get_opcodes():
        if op == "equal" or op == "replace" and i2 - i1 == j2 - j1:
            for x, y in zip(a[i1:i2], b[j1:j2]):
                if x["categorie"] != y["categorie"] or not proches(x["net"], y["net"]):
                    sys.exit(f"{quoi} : « {x['brut']} » d'un côté, « {y['brut']} » de l'autre")
                paires.append((x, y))
        elif op == "replace":
            sys.exit(f"{quoi} : {[l['brut'] for l in a[i1:i2]]} d'un côté, {[l['brut'] for l in b[j1:j2]]} de l'autre")
        else:
            paires += [(x,) for x in a[i1:i2]] + [(y,) for y in b[j1:j2]]
    return paires


def lignes_articles_5_6(tableaux, formes, source_id, recolle):
    """Budgets annexes (article 5) et comptes spéciaux (article 6), compte par compte et programme par programme.
    Les segments d'une même famille (budgets annexes ou comptes spéciaux) et d'un même genre (autorisations
    d'engagement, opérations de l'année, soldes au 31 décembre) forment un seul tableau, dont les rubriques donnent la
    catégorie des comptes.

    Les budgets annexes, comptes d'affectation spéciale et comptes de concours financiers ont des programmes ; leurs
    tableaux des autorisations d'engagement et des opérations présentent les mêmes lignes, que l'on départage
    ensemble : une ligne précédée d'un tiret dans l'un ou l'autre est un programme ; sinon, une ligne en gras dans l'un
    ou l'autre est un compte, de même qu'une ligne maigre quand les programmes de sa catégorie portent un tiret ; le
    reste, ce sont des programmes. Une même ligne y prend le libellé du tableau des opérations, à condition que les deux
    libellés soient presque identiques ; une ligne que l'un des deux tableaux ne présente pas y reste seule.
    L'augmentation du fonds de roulement et les fonds de concours d'un budget annexe en sont des composantes, à côté de
    ses programmes. Les comptes de commerce et d'opérations monétaires n'ont pas de programmes, ni le tableau des
    soldes, dont chaque compte prend de même le libellé du tableau des opérations."""
    tables = {}
    for seg in segments_de_comptes(tableaux, formes, source_id):
        tables.setdefault((seg["famille"], seg["genre"]), []).append(seg)
    structures = {cle_: structure_des_comptes(segs, cle_[0], recolle, source_id) for cle_, segs in tables.items()}
    for fam in ("BA", "CS", "CLOS"):
        ae, operations = structures.get((fam, "AE"), []), structures.get((fam, "OPERATIONS"), [])
        a = [l for l in ae if l["role"] == "ligne"]
        b = [l for l in operations if l["role"] == "ligne" and l["categorie"] not in SANS_PROGRAMMES]
        tirets = {l["categorie"] for l in a + b if l["tiret"]}
        for paire in apparier(a, b, f"{fam}, autorisations d'engagement et opérations"):
            if any(l["tiret"] for l in paire):
                if any(l["tiret"] and l["gras"] for l in paire):
                    sys.exit(f"{fam} : ligne en gras précédée d'un tiret (« {paire[0]['brut']} »)")
                role = "programme"
            else:
                role = "compte" if any(l["gras"] for l in paire) or paire[0]["categorie"] in tirets else "programme"
            for l in paire:
                l["role"], l["net"] = role, paire[-1]["net"]
    for (fam, genre), lignes in structures.items():
        for l in lignes:
            if l["role"] == "ligne":
                l["role"] = "compte"  # comptes de commerce et d'opérations monétaires, soldes
        compte = None
        for l in lignes:
            if l["role"] in ("rubrique", "total"):
                compte = None
            elif l["role"] == "compte":
                compte, l["fonction"] = l["net"], (l["net"], "")
            elif compte is None:
                sys.exit(f"tableau {l['seg']['i']}, ligne {l['r']} : {l['role']} hors compte (« {l['brut']} »)")
            else:
                l["fonction"] = (l["net"], compte)
    for fam in ("BA", "CS", "CLOS"):
        comptes_op = [l for l in structures.get((fam, "OPERATIONS"), []) if l["role"] == "compte"]
        comptes_so = [l for l in structures.get((fam, "SOLDES"), []) if l["role"] == "compte"]
        for paire in apparier(comptes_so, comptes_op, f"{fam}, soldes et opérations"):
            if len(paire) == 2:
                paire[0]["net"], paire[0]["fonction"] = paire[1]["net"], (paire[1]["net"], "")
    # Les comptes clos dans l'année sont des comptes de leur catégorie ; les totaux de l'article 6 ne portent alors
    # que sur les comptes qui se poursuivent (« hors comptes clos »), ceux des tableaux des comptes clos sur ces seuls
    # comptes. Le rapport de cohérence ne peut pas rapprocher ces totaux de leurs comptes, qui portent le concept de
    # leur catégorie : chacun doit égaler la somme des comptes de son tableau qu'il couvre.
    clos = {l["categorie"] for (fam, genre), lignes in structures.items() if fam == "CLOS" for l in lignes
            if l["role"] in ("compte", "programme")}
    touches = clos | ({"CS_A_CREDITS"} if clos & {"CAS", "CCF"} else set()) | \
        ({"CS_A_DECOUVERT"} if clos & SANS_PROGRAMMES else set()) | ({"CS_ENSEMBLE"} if clos else set())
    composition = {v: k for k, v in TOTAUX_GENERAUX.items()}
    sommes, a_verifier = collections.defaultdict(float), []
    for (fam, genre), lignes in structures.items():
        for l in lignes:
            seg, r = l["seg"], l["r"]
            t, noms, largeurs = seg["t"], seg["noms"], seg["forme"]["largeurs"]
            for c, x in enumerate(t[r]):
                nombre = nombre_texte(x) if c > 0 else None
                if c > 0 and not nombre and re.search(r"[0-9]", x):
                    sys.exit(f"tableau {seg['i']}, ligne {r} : montant illisible (« {x} »)")
                if not nombre:
                    continue
                if len({noms.get(c + dc) for dc in range(largeurs.get((r, c), 1))}) > 1:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : case à cheval sur deux colonnes")
                if noms.get(c) not in MESURES:
                    sys.exit(f"tableau {seg['i']}, ligne {r} : colonne « {noms.get(c)} » sans correspondance")
                if l["role"] in ("rubrique", "total"):
                    categorie, fonction = l["cible"], ""
                else:
                    categorie, fonction = l["categorie"], l["fonction"]
                intitule, note_colonne = COLONNES_CONTREDITES.get((source_id, categorie, noms[c]), (noms[c], ""))
                mesure = MESURES[intitule]
                if mesure not in (MESURES_A_DECOUVERT if categorie in SANS_PROGRAMMES | {"CS_A_DECOUVERT"} else
                                  MESURES_A_CREDITS):
                    if float(nombre[0]) == 0:
                        continue  # un zéro dans une colonne étrangère à la catégorie n'en est pas un chiffre
                    sys.exit(f"tableau {seg['i']}, ligne {r} : « {noms[c]} » pour la catégorie {categorie}")
                concept = f"LOLF.{categorie}_{mesure}"
                if categorie == "BA" and source_id in BUDGETS_ANNEXES_HORS_FDC and mesure in ("DEPENSES", "RECETTES"):
                    concept += "_HORS_FDC"
                if l["role"] in ("rubrique", "total") and (fam == "CLOS" or categorie in touches):
                    concept += "_COMPTES_CLOS" if fam == "CLOS" else "_HORS_COMPTES_CLOS"
                    a_verifier.append((seg["i"], r, fam, genre, categorie, mesure, float(nombre[0])))
                elif l["role"] == "compte":
                    sommes[(fam, genre, categorie, mesure)] += float(nombre[0])
                unite_, note = seg["unite"]
                note = " ".join(n for n in (note, note_colonne, NOTE_ASTERISQUE if "*" in x else "") if n)
                yield {"tableau": seg["i"], "ligne": r, "colonne": c, "libelle": propre(t[r][0]), "intitule": noms[c],
                       "concept": concept, "fonction": fonction, "nombre": nombre, "unite": unite_, "note": note,
                       "ajustement": mesure in MESURES_AJUSTEMENTS, "solde": mesure in MESURES_SOLDES}
    for i, r, fam, genre, categorie, mesure, valeur in a_verifier:
        somme = sum(sommes[(fam, genre, c, mesure)] for c in composition.get(categorie, {categorie}))
        if abs(valeur - somme) > 0.005:
            sys.exit(f"tableau {i}, ligne {r} : total {valeur:.2f}, somme des comptes qu'il couvre {somme:.2f}")


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions et programmes."""
    chemin = BASE / fichier["chemin"]
    annees = set(re.findall(ANNEE, texte_html(chemin.read_text(encoding="utf-8"))))
    if len(annees) != 1 or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année des comptes ({', '.join(sorted(annees)) or 'aucune'}) ou date du texte "
                 f"introuvable")
    annee = annees.pop()
    if not int(annee) < int(fichier["mis_a_jour_source"][:4]) <= int(annee) + 2:
        sys.exit(f"{fichier['id']} : comptes de {annee} dans un texte daté {fichier['mis_a_jour_source']}")
    # Une coupure de mot de fin de ligne du texte imprimé, restée dans la page (« dévelop-pement »), se recolle quand
    # le mot entier figure ailleurs dans le texte.
    mots = set(re.findall(r"\w+", texte_html(chemin.read_text(encoding="utf-8")).lower()))
    recolle = lambda libelle: re.sub(r"(\w+)-(\w+)", lambda m: m.group(1) + m.group(2) if m.group(1)[-1].islower() and
                                     m.group(2)[0].islower() and (m.group(1) + m.group(2)).lower() in mots
                                     else m.group(0), libelle)
    tableaux, formes = lire_tableaux_html(chemin, mise_en_forme=True)
    i, tableau = article_1(tableaux)
    for brute in list(lignes_article_1(i, tableau, formes[i], fichier["source_id"])) + \
            list(lignes_article_4(tableaux, formes, fichier["source_id"], recolle)) + \
            list(lignes_articles_5_6(tableaux, formes, fichier["source_id"], recolle)):
        fonction = ""
        if brute["fonction"]:
            libelle, mission = brute["fonction"]
            parent = f"LOLF.{code_lolf(mission)}" if mission else ""
            fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
            if parent:
                fonctions.setdefault(parent, {"id": parent, "libelle": mission, "norme_id": "LOLF", "parent_id": ""})
            fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": parent})
        concept = brute["concept"]
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"tableau={brute['tableau']};ligne={brute['ligne']};colonne={brute['colonne']};"
                           f"libelle={brute['libelle']};colonne_libelle={brute['intitule']}",
            "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept, "fonction_id": fonction, "traitements": "",
            "unite_id": brute["unite"], "periode": annee, "valeur": brute["nombre"][0],
            "decimales": brute["nombre"][1], "statut": "non_precise" if concept in AJUSTEMENTS or brute.get("ajustement") else "definitif",
            "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10],
            "consolidation": "sans_objet" if concept in SOLDES or brute.get("solde") else "non_consolide",
            "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": brute["note"],
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
