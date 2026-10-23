#!/usr/bin/env python3
"""Enregistre dans la base les comptes de l'exercice clos de la sécurité sociale, qu'approuve une loi de financement
de la sécurité sociale (comptes de 2004 à 2021) ou que présente un projet de loi d'approbation des comptes de la
sécurité sociale (depuis ceux de 2022), à partir de son texte publié par le Sénat (page HTML archivée).

    python3 outils/importer_lois_secu.py <fichier_id>

Seule la partie relative à l'exercice clos est lue :
- les tableaux d'équilibre de l'article qui approuve les comptes de l'exercice : celui, par branche, de l'ensemble
  des régimes obligatoires de base, celui, par branche, du régime général (jusqu'aux comptes de 2021) et celui des
  organismes concourant à leur financement ; recettes, dépenses et solde, en milliards d'euros ;
- les montants que l'article énonce dans son texte : dépenses constatées dans le champ de l'objectif national de
  dépenses d'assurance maladie (ONDAM), recettes affectées au Fonds de réserve pour les retraites (FRR), recettes
  mises en réserve par le Fonds de solidarité vieillesse (FSV) quand l'article les mentionne, dette amortie par la
  Caisse d'amortissement de la dette sociale (CADES) ; des recettes « nulles » valent zéro ;
- l'article liminaire d'un projet de loi d'approbation des comptes : recettes, dépenses et solde des
  administrations de sécurité sociale au sens de la comptabilité nationale, en points de produit intérieur brut ;
- l'annexe A, depuis les comptes de 2010 : la situation patrimoniale des régimes de base, du FSV, de la CADES et du
  FRR au 31 décembre de l'exercice et de l'exercice précédent (voir lignes_situation_patrimoniale) et, depuis ceux
  de 2013, le tableau qui retrace depuis 2009 leur passif net, leur endettement financier net et leur résultat.
Les autres parties d'une loi de financement portent sur l'année en cours et l'année à venir : ce sont des
prévisions, qui ne sont pas lues. Dans la partie relative à l'exercice clos, un tableau à montants qu'aucune de ces
règles ne lit arrête l'import, de même qu'un libellé inconnu, une unité absente ou un montant attendu introuvable.

Les branches sont les « fonctions » de la norme COMPTES_SECU. Les recettes et les dépenses d'une branche comprennent
les transferts entre branches ; la ligne « toutes branches » les exclut : elle est consolidée, et seul son solde
égale la somme de ceux des branches. La version d'un chiffre est la date que porte le texte (transmission au Sénat,
ou adoption par le Sénat) ; les comptes de l'exercice clos sont définitifs, les grandeurs de comptabilité nationale
de l'article liminaire provisoires.
"""

import re
import sys
import unicodedata

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_page_html,
                    nombre_de_phrase, nombre_texte, table_des_chiffres, texte_html)

APPROBATION = r"Au titre de l['’]exercice ([0-9]{4}) ?, sont approuvés"
# Les tableaux d'équilibre de l'article, d'après la phrase qui annonce chacun : (motif, périmètre de ses branches).
EQUILIBRES = [(r"tableau d['’]équilibre, par branche, de l['’]ensemble des régimes obligatoires de base", "ROBSS"),
              (r"tableau d['’]équilibre, par branche, du régime général", "REGIME_GENERAL_HORS_FSV"),
              (r"tableau d['’]équilibre des organismes concourant au financement des régimes obligatoires de base", "")]
UNITE = r"\(en milliards d['’]euros\)"
# Libellés de colonne et de ligne, sous leur forme de reconnaissance (voir forme).
COLONNES = {"recettes": "COMPTES_SECU.RECETTES", "depenses": "COMPTES_SECU.DEPENSES",
            "solde": "COMPTES_SECU.RESULTAT_COMPTABLE"}
BRANCHES = {"maladie": "COMPTES_SECU.MALADIE", "accidents du travail et maladies professionnelles": "COMPTES_SECU.AT_MP",
            "vieillesse": "COMPTES_SECU.VIEILLESSE", "famille": "COMPTES_SECU.FAMILLE",
            "autonomie": "COMPTES_SECU.AUTONOMIE"}
TOUTES_BRANCHES = "toutes branches (hors transferts entre branches)"
# Ensemble des branches et Fonds de solidarité vieillesse, hors transferts entre eux, depuis les comptes de 2015.
AVEC_FSV = {"toutes branches (hors transferts entre branches) y compris fonds de solidarite vieillesse",
            "toutes branches y compris fonds de solidarite vieillesse (hors transferts entre branches ou fonds)"}
PERIMETRES_AVEC_FSV = {"ROBSS": "ROBSS_FSV", "REGIME_GENERAL_HORS_FSV": "REGIME_GENERAL"}
ORGANISMES = {"fonds de solidarite vieillesse": "FSV", "fsv": "FSV",
              "fonds de financement des prestations sociales des non-salaries agricoles": "FFIPSA",
              # mot coupé en fin de ligne dans le texte qui approuve les comptes de 2006
              "fonds de financement des presta-tions sociales des non-salaries agricoles": "FFIPSA",
              "caisse nationale de solidarite pour l'autonomie": "CNSA"}

# Montants que l'article énonce dans son texte : (concept, périmètre, phrase, obligatoire).
_MONTANT = r"s['’]élevant à [0-9]+(?:,[0-9]+)? milliards? d['’]euros"
ENONCES = [
    ("LFSS.ONDAM_CONSTATE", "ROBSS",
     r"Les dépenses constatées relevant du champ de l['’]objectif national de dépenses d['’]assurance maladie, " + _MONTANT,
     True),
    ("LFSS.FRR_RECETTES_AFFECTEES", "FRR",
     r"Les recettes affectées au Fonds de réserve pour les retraites, (?:" + _MONTANT + r"|lesquelles sont nulles)", True),
    ("LFSS.FSV_RECETTES_MISES_EN_RESERVE", "FSV",
     r"Les recettes mises en réserve par le Fonds de solidarité vieillesse, (?:" + _MONTANT + r"|lesquelles sont nulles)",
     False),
    ("LFSS.CADES_DETTE_AMORTIE", "CADES",
     r"Le montant de la dette amortie par la Caisse d['’]amortissement de la dette sociale, " + _MONTANT, True),
]

# Article liminaire des projets de loi d'approbation des comptes : ligne → (concept, consolidation).
LIMINAIRE = {"recettes": ("SEC2010.TR", "consolide"), "depenses": ("SEC2010.TE", "consolide"),
             "solde": ("SEC2010.B9", "sans_objet")}
UNITE_LIMINAIRE = r"\((?:en pourcentage du|ramené au|en points de) (?:produit intérieur brut|PIB)\)"

# Annexe A, situation patrimoniale. Chaque côté du tableau se lit de haut en bas : un agrégat, puis ses postes, et
# sous un poste les lignes de chaque entité. Un libellé est reconnu sous sa clé (voir cle) ; un libellé qu'aucune
# table ne connaît, ou un poste hors de son agrégat, arrête l'import. Agrégats et totaux : clé → concept.
_S = "COMPTES_SECU."
AGREGATS = {"actif": {"immobilisations": "IMMOBILISATIONS", "actif financier": "ACTIF_FINANCIER",
                      "actif circulant": "ACTIF_CIRCULANT", "total de l'actif": "TOTAL_ACTIF"},
            "passif": {"capitaux propres": "FONDS_PROPRES", "fonds propres": "FONDS_PROPRES",
                       "provisions pour risques et charges": "PROVISIONS_RISQUES_CHARGES",
                       "passif financier": "PASSIF_FINANCIER", "passif circulant": "PASSIF_CIRCULANT",
                       "total du passif": "TOTAL_PASSIF"}}
# Postes : (agrégat, clé) → concept.
POSTES = {("IMMOBILISATIONS", "immobilisations non financieres"): "IMMOBILISATIONS_NON_FINANCIERES",
          ("IMMOBILISATIONS", "prets depots de garantie"): "PRETS_DEPOTS_GARANTIE",
          ("IMMOBILISATIONS", "prets depots de garantie et autres"): "PRETS_DEPOTS_GARANTIE",
          ("IMMOBILISATIONS", "avances prets accordes a des organismes de la sphere sociale"): "AVANCES_SPHERE_SOCIALE",
          ("ACTIF_FINANCIER", "valeurs mobilieres et titres de placement"): "VALEURS_MOBILIERES",
          ("ACTIF_FINANCIER", "encours bancaire"): "ENCOURS_BANCAIRE",
          ("ACTIF_FINANCIER", "creances nettes au titre des instruments financiers"): "CREANCES_INSTRUMENTS_FINANCIERS",
          ("ACTIF_CIRCULANT", "creances sur prestations"): "CREANCES_PRESTATIONS",
          ("ACTIF_CIRCULANT", "creances de prestations"): "CREANCES_PRESTATIONS",
          ("ACTIF_CIRCULANT", "creances et produits a recevoir sur cotisations contributions sociales impots"):
              "CREANCES_ET_PRODUITS_A_RECEVOIR_COTISATIONS",
          ("ACTIF_CIRCULANT", "creances de cotisations contributions sociales et d'impots de securite sociale"):
              "CREANCES_COTISATIONS",
          ("ACTIF_CIRCULANT", "produits a recevoir de cotisations contributions sociales et impots de securite sociale"):
              "PRODUITS_A_RECEVOIR_COTISATIONS",
          ("ACTIF_CIRCULANT", "produits a recevoir de cotisations contributions sociales et autres impositions"):
              "PRODUITS_A_RECEVOIR_COTISATIONS",
          ("ACTIF_CIRCULANT", "creances et par sur l'etat et autres entites publiques"):
              "CREANCES_ET_PRODUITS_A_RECEVOIR_ENTITES_PUBLIQUES",
          ("ACTIF_CIRCULANT", "creances sur l'etat et autres entites publiques"): "CREANCES_ENTITES_PUBLIQUES",
          ("ACTIF_CIRCULANT", "creances sur entites publiques"): "CREANCES_ENTITES_PUBLIQUES",
          ("ACTIF_CIRCULANT", "creances sur entites publiques et organismes de securite sociale"):
              "CREANCES_ENTITES_PUBLIQUES",
          ("ACTIF_CIRCULANT", "produits a recevoir de l'etat"): "PRODUITS_A_RECEVOIR_ETAT",
          ("ACTIF_CIRCULANT", "autres actifs"): "AUTRES_ACTIFS",
          ("FONDS_PROPRES", "dotations"): "DOTATIONS", ("FONDS_PROPRES", "reserves"): "RESERVES",
          ("FONDS_PROPRES", "report a nouveau"): "REPORT_A_NOUVEAU",
          ("FONDS_PROPRES", "resultat de l'exercice"): "RESULTAT_EXERCICE_BILAN",
          ("FONDS_PROPRES", "resultat de l'exercice n en instance d'affectation"): "RESULTAT_EN_INSTANCE_AFFECTATION",
          ("FONDS_PROPRES", "ecart d'estimation"): "ECART_ESTIMATION_FRR",
          ("FONDS_PROPRES", "autres"): "AUTRES_FONDS_PROPRES",
          ("PASSIF_FINANCIER", "dettes representees par un titre"): "DETTES_REPRESENTEES_PAR_UN_TITRE",
          ("PASSIF_FINANCIER", "dettes a l'egard d'etablissements de credit"): "DETTES_ETABLISSEMENTS_CREDIT",
          ("PASSIF_FINANCIER", "dettes a l'egard d'etablissements de credits"): "DETTES_ETABLISSEMENTS_CREDIT",
          ("PASSIF_FINANCIER", "depots"): "DEPOTS_RECUS", ("PASSIF_FINANCIER", "depots recus"): "DEPOTS_RECUS",
          ("PASSIF_FINANCIER", "dettes nettes au titre des instruments financiers"): "DETTES_INSTRUMENTS_FINANCIERS",
          ("PASSIF_FINANCIER", "autres"): "AUTRES_DETTES_FINANCIERES",
          ("PASSIF_CIRCULANT", "dettes et charges a payer a l'egard des beneficiaires"): "DETTES_BENEFICIAIRES",
          ("PASSIF_CIRCULANT", "dettes et charges a payer a l'egard des beneficiaires de prestations"):
              "DETTES_BENEFICIAIRES",
          ("PASSIF_CIRCULANT", "dettes a l'egard des cotisants"): "DETTES_COTISANTS",
          ("PASSIF_CIRCULANT", "dettes et charges a payer a l'egard des cotisants"): "DETTES_COTISANTS",
          ("PASSIF_CIRCULANT", "dettes et cap a l'egard de l'etat et autres entites publiques"): "DETTES_ENTITES_PUBLIQUES",
          ("PASSIF_CIRCULANT", "dettes a l'egard d'entites publiques"): "DETTES_ENTITES_PUBLIQUES",
          ("PASSIF_CIRCULANT", "dettes et charges a payer a l'egard d'entites publiques"): "DETTES_ENTITES_PUBLIQUES",
          ("PASSIF_CIRCULANT", "dettes et charges a payer a l'egard d'entites publiques et organismes de securite "
                               "sociale"): "DETTES_ENTITES_PUBLIQUES",
          ("PASSIF_CIRCULANT", "autres passifs"): "AUTRES_PASSIFS"}
# Entités : clé → périmètre. La ligne « Régime général / autres régimes » de 2012 réunit les deux.
ENTITES = {"regime general": "REGIME_GENERAL_HORS_FSV", "autres regimes": "AUTRES_REGIMES_BASE",
           "regime general autres regimes": "ROBSS", "fsv": "FSV", "fonds de solidarite vieillesse": "FSV",
           "cades": "CADES", "caisse d'amortissement de la dette sociale": "CADES",
           "caisse d'amortissement de la dette sociale cades": "CADES",  # parenthèse ouvrante manquante en 2017
           "frr": "FRR", "fonds de reserve pour les retraites": "FRR",
           "acoss": "ACOSS", "agence centrale des organismes de securite sociale": "ACOSS"}
# Tableau qui retrace depuis 2009 le passif net, l'endettement financier net et le résultat : clé → concept.
EVOLUTION = {"passif net au 31 12": "PASSIF_NET", "passif net au 31 decembre": "PASSIF_NET",
             "endettement financier net": "ENDETTEMENT_FINANCIER_NET",
             "endettement financier net au 31 12": "ENDETTEMENT_FINANCIER_NET",
             "endettement financier net au 31 decembre": "ENDETTEMENT_FINANCIER_NET",
             "resultat comptable consolide de l'exercice": "RESULTAT_COMPTABLE"}
VARIATION = "variation"  # colonnes et lignes de variation d'une année sur l'autre : la différence des montants
SITUATION = r"Situation patrimoniale de la sécurité sociale au 31 décembre ([0-9]{4})"


def propre(texte):
    """Un libellé sans ses points de conduite (« Maladie. . . . . »)."""
    return " ".join(re.sub(r"(?:\s*\.){2,}", " ", texte).split())


def forme(texte):
    """Forme de reconnaissance d'un libellé : sans points de conduite, accents, majuscules ni ponctuation."""
    t = unicodedata.normalize("NFD", propre(texte).replace("’", "'"))
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return " ".join(re.sub(r"[,;:]", " ", t).split()).strip(" .")


def tableaux_entre(flux, debut, fin):
    """Numéros des tableaux qui s'ouvrent entre deux positions du flux, et le texte qui précède chacun depuis le
    repère de tableau précédent."""
    for m in re.finditer(r"⟦([0-9]+)⟧", flux[debut:fin]):
        precedent = max(flux.rfind("⟦", 0, debut + m.start()), 0)
        yield int(m.group(1)), re.sub(r"^⟦/?[0-9]+⟧", "", flux[precedent:debut + m.start()]).strip()


def a_montants(grille):
    return any(nombre_texte(x) for ligne in grille for x in ligne)


def lignes_equilibre(k, grille, perimetre_branches, avant, origine):
    """Les chiffres d'un tableau d'équilibre : une ligne par branche, l'ensemble des branches, et les organismes."""
    if not (re.search(UNITE, avant, re.I) or any(re.fullmatch(UNITE, x.strip(), re.I) for l in grille for x in l)):
        sys.exit(f"{origine}, tableau {k} : unité « (en milliards d'euros) » introuvable")
    entetes = [r for r, l in enumerate(grille) if [forme(x) for x in l if x.strip()] == list(COLONNES)]
    if len(entetes) != 1:
        sys.exit(f"{origine}, tableau {k} : en-tête « Recettes | Dépenses | Solde » introuvable")
    colonnes = {c: COLONNES[forme(x)] for c, x in enumerate(grille[entetes[0]]) if x.strip()}
    for r, ligne in enumerate(grille):
        cases = [c for c, x in enumerate(ligne) if nombre_texte(x)]
        if not cases:
            if r > entetes[0] and any(x.strip() not in ("", ";") for x in ligne):
                sys.exit(f"{origine}, tableau {k}, ligne {r} : ligne sans montant « {ligne[0]} »")
            continue
        if r < entetes[0] or set(cases) != set(colonnes):
            sys.exit(f"{origine}, tableau {k}, ligne {r} : montants hors des colonnes Recettes, Dépenses et Solde")
        libelle = forme(ligne[0])
        if perimetre_branches and libelle in BRANCHES:
            perimetre, fonction, consolide = perimetre_branches, BRANCHES[libelle], False
        elif perimetre_branches and libelle == TOUTES_BRANCHES:
            perimetre, fonction, consolide = perimetre_branches, "", True
        elif perimetre_branches and libelle in AVEC_FSV:
            perimetre, fonction, consolide = PERIMETRES_AVEC_FSV[perimetre_branches], "", True
        elif libelle in ORGANISMES:
            perimetre, fonction, consolide = ORGANISMES[libelle], "", False
        else:
            sys.exit(f"{origine}, tableau {k}, ligne {r} : libellé inconnu « {ligne[0]} »")
        for c in cases:
            concept = colonnes[c]
            solde = concept == "COMPTES_SECU.RESULTAT_COMPTABLE"
            yield {"emplacement": f"tableau={k};ligne={r};colonne={c};libelle={propre(ligne[0])};"
                                  f"colonne_libelle={grille[entetes[0]][c]}",
                   "perimetre": perimetre, "concept": concept, "fonction": fonction, "unite": "MD_EUR",
                   "nombre": nombre_texte(ligne[c]), "statut": "definitif",
                   "consolidation": "sans_objet" if solde else "consolide" if consolide else "non_consolide"}


def lignes_liminaire(k, grille, avant, annee, origine):
    """Les chiffres de l'article liminaire : recettes, dépenses et solde des administrations de sécurité sociale."""
    if not (re.search(UNITE_LIMINAIRE, avant, re.I) or re.search(UNITE_LIMINAIRE, " ".join(grille[0]), re.I)):
        sys.exit(f"{origine}, tableau {k} : unité de l'article liminaire introuvable")
    annees = set(re.findall(r"l['’]année ([0-9]{4})", avant)) | {x for x in grille[0] if re.fullmatch(r"[0-9]{4}", x)}
    if annees != {str(annee)}:
        sys.exit(f"{origine}, tableau {k} : article liminaire de l'année {', '.join(sorted(annees)) or '?'}, "
                 f"comptes de {annee}")
    lus = set()
    for r, ligne in enumerate(grille):
        cases = [c for c, x in enumerate(ligne) if nombre_texte(x) and not (r == 0 and x == str(annee))]
        if not cases:
            if r > 0 and any(x.strip() for x in ligne):
                sys.exit(f"{origine}, tableau {k}, ligne {r} : ligne sans montant « {ligne[0]} »")
            continue
        libelle = forme(ligne[0])
        if libelle not in LIMINAIRE or len(cases) != 1 or libelle in lus:
            sys.exit(f"{origine}, tableau {k}, ligne {r} : ligne inattendue « {ligne[0]} »")
        lus.add(libelle)
        concept, consolidation = LIMINAIRE[libelle]
        yield {"emplacement": f"tableau={k};ligne={r};colonne={cases[0]};libelle={propre(ligne[0])};"
                              f"colonne_libelle={grille[0][cases[0]] or annee}",
               "perimetre": "S1314", "concept": concept, "fonction": "", "unite": "PC_PIB",
               "nombre": nombre_texte(ligne[cases[0]]), "statut": "provisoire", "consolidation": consolidation}
    if lus != set(LIMINAIRE):
        sys.exit(f"{origine}, tableau {k} : article liminaire incomplet")


def lignes_enoncees(texte, origine):
    """Les montants que l'article énonce dans son texte, chacun par la phrase qui le contient."""
    approbation = re.search(APPROBATION, texte)
    if approbation is None:
        sys.exit(f"{origine} : approbation des comptes introuvable dans le texte de la page")
    debut = approbation.start()
    for concept, perimetre, motif, obligatoire in ENONCES:
        trouvees = list(re.finditer(motif, texte))
        if len(trouvees) > 1 or (obligatoire and not trouvees) or any(m.start() < debut for m in trouvees):
            sys.exit(f"{origine} : {len(trouvees)} phrase(s) pour {concept} dans la partie relative à l'exercice clos")
        for m in trouvees:
            nombre = nombre_de_phrase(m.group(0))
            if nombre is None or ";" in m.group(0):
                sys.exit(f"{origine} : montant illisible dans « {m.group(0)} »")
            yield {"emplacement": f"phrase={m.group(0)}", "perimetre": perimetre, "concept": concept, "fonction": "",
                   "unite": "MD_EUR", "nombre": nombre, "statut": "definitif", "consolidation": "sans_objet"}


def cle(texte):
    """Clé d'un libellé de la situation patrimoniale : sa forme, sans ses parenthèses ni ce qui suit « dont », les
    barres obliques et les années remplacées."""
    t = forme(texte).replace("/", " ")
    while re.search(r"\([^()]*\)", t):
        t = re.sub(r"\([^()]*\)", " ", t)
    t = re.sub(r"\(.*$", " ", t).replace(")", " ")  # parenthèse restée ouverte ou fermante seule
    t = re.sub(r" dont .*$", "", re.sub(r"\b(?:19|20)[0-9]{2}\b", "n", t))
    return " ".join(t.split())


def precision(texte):
    """La précision qu'un libellé d'entité donne entre parenthèses (« Régime général (y compris prêts CDC) »)."""
    trouvees = [p.strip() for p in re.findall(r"\(([^()]*)\)", propre(texte)) if p.strip() not in ("ACOSS", "CADES",
                                                                                                     "FRR", "FSV")]
    return f"Le libellé précise : {'; '.join(trouvees)}." if trouvees else ""


def colonnes_d_annees(entete, annees, origine, k):
    """Les colonnes d'une ligne d'en-tête qui portent une année (« 2022 », « 2022 (net) ») ; une colonne de variation
    est écartée, toute autre arrête l'import."""
    colonnes = {}
    for c, x in enumerate(entete):
        f = forme(x)
        trouve = re.fullmatch(r"([0-9]{4})(?: \(net\))?", f)
        if trouve and int(trouve.group(1)) in annees:
            colonnes[c] = trouve.group(1)
        elif f and f != VARIATION:
            sys.exit(f"{origine}, tableau {k} : colonne inattendue « {x} »")
    return colonnes


def lignes_situation_patrimoniale(k, grille, avant, annee, origine):
    """Le bilan de l'annexe A, au 31 décembre de l'exercice et de l'exercice précédent : chaque côté (actif, passif)
    a ses agrégats, ses postes et, sous un poste, les lignes de chaque entité, enregistrées au périmètre de l'entité
    sous le concept du poste. Le total de chaque ligne d'agrégat ou de poste est celui de l'ensemble (périmètre
    SECU_LFSS). Une note de bas de tableau (« Nota : … ») accompagne les chiffres de la colonne qu'elle vise."""
    annoncee = bool(re.search(UNITE, avant, re.I) or any(re.fullmatch(UNITE, x.strip(), re.I) for l in grille[:2] for x in l))
    entetes = [r for r, l in enumerate(grille) if {"actif", "passif"} <= {forme(x) for x in l}]
    if len(entetes) != 1:
        sys.exit(f"{origine}, tableau {k} : en-tête « Actif … Passif » introuvable")
    h = entetes[0]
    debuts = {forme(x): c for c, x in enumerate(grille[h]) if forme(x) in ("actif", "passif")}
    cotes = {"actif": (debuts["actif"], debuts["passif"]), "passif": (debuts["passif"], len(grille[h]))}
    notes = {}
    for ligne in grille[h + 1:]:
        if forme(ligne[0]).startswith("nota "):
            visees = set(re.findall(r"« ([0-9]{4}) »", ligne[0]))
            notes.update({a: propre(ligne[0]) for a in visees})
    for cote, (c0, c1) in cotes.items():
        colonnes = colonnes_d_annees(grille[h][c0 + 1:c1], {annee, annee - 1}, origine, k)
        colonnes = {c0 + 1 + c: a for c, a in colonnes.items()}
        if sorted(colonnes.values()) != [str(annee - 1), str(annee)]:
            sys.exit(f"{origine}, tableau {k} : colonnes de l'{cote} {sorted(colonnes.values())}, attendues "
                     f"{annee - 1} et {annee}")
        agregat, concept, sous_lignes = None, None, []
        for r in range(h + 1, len(grille)):
            libelle = grille[r][c0] if c0 < len(grille[r]) else ""
            montants = {c: nombre_texte(grille[r][c]) for c in colonnes if c < len(grille[r]) and nombre_texte(grille[r][c])}
            autres = [x for x in grille[r][c0 + 1:c1] if x.strip() and not nombre_texte(x)]
            if forme(libelle).startswith("nota ") or not (libelle.strip() or montants):
                continue
            if autres:
                sys.exit(f"{origine}, tableau {k}, ligne {r} : case inattendue « {autres[0]} »")
            cle_ = cle(libelle)
            if cle_ in AGREGATS[cote]:
                agregat = concept = AGREGATS[cote][cle_]
                perimetre, note, sous_lignes = "SECU_LFSS", "", []
            elif (agregat, cle_) in POSTES:
                concept = POSTES[(agregat, cle_)]
                perimetre, note, sous_lignes = "SECU_LFSS", "", []
            elif cle_ in ENTITES and concept:
                perimetre, note = ENTITES[cle_], precision(libelle)
                sous_lignes.append(perimetre)
            else:
                sys.exit(f"{origine}, tableau {k}, ligne {r} : libellé inconnu « {libelle} » ({cote}, sous "
                         f"{concept or 'aucun agrégat'})")
            for c, nombre in montants.items():
                yield {"emplacement": f"tableau={k};ligne={r};colonne={c};libelle={propre(libelle)};"
                                      f"colonne_libelle={grille[h][c]}",
                       "perimetre": perimetre, "concept": _S + concept, "fonction": "", "unite": "MD_EUR",
                       "nombre": nombre, "statut": "definitif", "consolidation": "sans_objet", "periode": colonnes[c],
                       "note": " ".join(n for n in (note, notes.get(colonnes[c], "")) if n), "sous_lignes": sous_lignes,
                       "tableau": k, "unite_annoncee": annoncee}


def lignes_evolution(k, grille, avant, annee, origine):
    """Le tableau qui retrace depuis 2009 le passif net, l'endettement financier net et le résultat comptable de
    l'ensemble des régimes de base, du FSV, de la CADES et du FRR. Les lignes de variation ne sont pas lues."""
    annoncee = bool(re.search(UNITE, avant, re.I) or any(re.fullmatch(UNITE, x.strip(), re.I) for l in grille for x in l))
    entetes = [r for r, l in enumerate(grille) if sum(bool(re.fullmatch(r"[0-9]{4}", x.strip())) for x in l) >= 3]
    if len(entetes) != 1:
        sys.exit(f"{origine}, tableau {k} : ligne des années introuvable")
    h = entetes[0]
    colonnes = colonnes_d_annees(grille[h], set(range(2009, annee + 1)), origine, k)
    if max(map(int, colonnes.values())) != annee:
        sys.exit(f"{origine}, tableau {k} : la série ne va pas jusqu'à {annee}")
    lus = set()
    for r, ligne in enumerate(grille):
        montants = {c: nombre_texte(ligne[c]) for c in colonnes if nombre_texte(ligne[c])}
        if r <= h:
            if montants and r < h:
                sys.exit(f"{origine}, tableau {k}, ligne {r} : montants avant la ligne des années")
            continue
        cle_ = cle(ligne[0])
        if cle_.startswith(VARIATION):
            continue
        if cle_ not in EVOLUTION or EVOLUTION[cle_] in lus or set(montants) != set(colonnes):
            sys.exit(f"{origine}, tableau {k}, ligne {r} : ligne inattendue « {ligne[0]} »")
        lus.add(EVOLUTION[cle_])
        for c, nombre in montants.items():
            yield {"emplacement": f"tableau={k};ligne={r};colonne={c};libelle={propre(ligne[0])};"
                                  f"colonne_libelle={grille[h][c]}",
                   "perimetre": "SECU_LFSS", "concept": _S + EVOLUTION[cle_], "fonction": "", "unite": "MD_EUR",
                   "nombre": nombre, "statut": "definitif", "periode": colonnes[c],
                   "consolidation": "sans_objet", "note": "", "tableau": k, "unite_annoncee": annoncee}


def lignes_annexe(grilles, flux, debut, fin, annee, origine):
    """L'annexe A, entre deux positions du flux : sa situation patrimoniale, puis, depuis les comptes de 2013, le
    tableau qui retrace l'évolution du passif net. Tout autre tableau à montants de l'annexe arrête l'import."""
    titres = [m for m in re.finditer(SITUATION, flux[debut:fin], re.I) if m.group(1) == str(annee)]
    if len(titres) != 1:
        sys.exit(f"{origine} : situation patrimoniale au 31 décembre {annee} introuvable dans l'annexe")
    tableaux = [(k, avant) for k, avant in tableaux_entre(flux, debut, fin) if a_montants(grilles[k])]
    if not 1 <= len(tableaux) <= 2 or flux.find(f"⟦{tableaux[0][0]}⟧") < debut + titres[0].start():
        sys.exit(f"{origine} : {len(tableaux)} tableaux à montants dans l'annexe, situation patrimoniale attendue")
    k, avant = tableaux[0]
    brutes = list(lignes_situation_patrimoniale(k, grilles[k], avant, annee, origine))
    # L'Acoss a, pour certains postes, sa propre ligne : celle du régime général n'en comprend pas le montant.
    for b in brutes:
        if b["perimetre"] == "REGIME_GENERAL_HORS_FSV" and "ACOSS" in b["sous_lignes"]:
            b["note"] = " ".join(n for n in ("Sans l'Acoss, que le tableau présente à part pour ce poste.", b["note"]) if n)
    if len(tableaux) == 2:
        k, avant = tableaux[1]
        brutes += lignes_evolution(k, grilles[k], avant, annee, origine)
    # Un tableau qui n'indique pas son unité est en milliards d'euros si le texte de l'annexe donne ainsi le montant de
    # son passif (fonds propres négatifs) ou de son endettement financier net au 31 décembre de l'exercice.
    enonces = {nombre_texte(m)[0] for m in re.findall(r"([0-9]+(?:,[0-9]+)?) milliards? d['’]euros", flux[debut:fin])}
    for k in sorted({b["tableau"] for b in brutes if not b["unite_annoncee"]}):
        cles = [b for b in brutes if b["tableau"] == k and b["periode"] == str(annee) and b["perimetre"] == "SECU_LFSS"
                and b["concept"] in (_S + "FONDS_PROPRES", _S + "PASSIF_NET", _S + "ENDETTEMENT_FINANCIER_NET")]
        if not any(b["nombre"][0].lstrip("-") in enonces for b in cles):
            sys.exit(f"{origine}, tableau {k} : unité « (en milliards d'euros) » introuvable")
        for b in brutes:
            if b["tableau"] == k:
                b["note"] = " ".join(n for n in (b["note"], "Le tableau n'indique pas son unité : le texte de l'annexe "
                                                 "donne en milliards d'euros son passif net ou son endettement "
                                                 "financier net de l'année.") if n)
    return brutes, {k for k, _ in tableaux}


def lignes_du_texte(chemin, origine):
    """(année des comptes, chiffres bruts) d'un texte : la partie relative à l'exercice clos, ou l'import s'arrête."""
    grilles, _, flux = lire_page_html(chemin)
    texte = texte_html(chemin.read_text(encoding="utf-8"))
    annees = set(re.findall(APPROBATION, flux))
    if len(annees) != 1:
        sys.exit(f"{origine} : exercice approuvé introuvable ou ambigu ({', '.join(sorted(annees)) or 'aucun'})")
    annee = int(annees.pop())
    approbation = re.search(APPROBATION, flux)
    deuxieme = re.search(r"DEUXI[ÈEË]ME PARTIE", flux[approbation.end():])  # « DEUXIËME » en 2011
    if deuxieme:  # loi de financement : la première partie porte sur l'exercice clos
        premiere = list(re.finditer(r"PREMI[ÈEË]RE PARTIE", flux[:approbation.start()]))
        debut, fin = (premiere[-1].start() if premiere else approbation.start()), approbation.end() + deuxieme.start()
    else:  # projet de loi d'approbation des comptes : tout le texte, jusqu'à l'annexe
        annexe = re.search(r"Annexe\s+Rapport retraçant la situation patrimoniale", flux[approbation.end():], re.I)
        if annexe is None:
            sys.exit(f"{origine} : ni deuxième partie ni annexe : texte de forme inconnue")
        debut, fin = 0, approbation.end() + annexe.start()
    article_2 = re.search(r"Article 2\b", flux[approbation.end():fin])
    fin_article_1 = approbation.end() + article_2.start() if article_2 else fin
    brutes, lus, trouves = [], set(), {}
    for k, avant in tableaux_entre(flux, approbation.start(), fin_article_1):
        if not a_montants(grilles[k]):
            continue
        genres = [p for motif, p in EQUILIBRES if re.search(motif, avant)]
        if len(genres) != 1 or genres[0] in trouves:
            sys.exit(f"{origine}, tableau {k} : tableau inattendu dans l'article qui approuve les comptes")
        trouves[genres[0]] = k
        brutes += lignes_equilibre(k, grilles[k], genres[0], avant, origine)
        lus.add(k)
    attendus = {"ROBSS", "REGIME_GENERAL_HORS_FSV", ""} if deuxieme else {"ROBSS", ""}
    if set(trouves) != attendus:
        sys.exit(f"{origine} : tableaux d'équilibre trouvés {sorted(trouves.values())}, attendus pour "
                 f"{', '.join(sorted(p or 'les organismes concourant' for p in attendus))}")
    if not deuxieme:
        liminaire = flux.find("Article liminaire", 0, approbation.start())
        tableaux = [(k, avant) for k, avant in tableaux_entre(flux, max(liminaire, 0), approbation.start())
                    if a_montants(grilles[k])]
        if liminaire < 0 or len(tableaux) != 1:
            sys.exit(f"{origine} : article liminaire introuvable")
        k, avant = tableaux[0]
        brutes += lignes_liminaire(k, grilles[k], flux[liminaire:flux.find(f"⟦{k}⟧")], annee, origine)
        lus.add(k)
    oublies = [k for k, _ in tableaux_entre(flux, debut, fin) if a_montants(grilles[k]) and k not in lus]
    if oublies:
        sys.exit(f"{origine} : tableaux à montants non lus dans la partie relative à l'exercice clos : {oublies}")
    brutes += lignes_enoncees(texte, origine)
    # L'annexe A de la loi de financement, ou l'annexe du projet de loi d'approbation des comptes : depuis les comptes
    # de 2010, l'article qui l'approuve annonce qu'elle présente la situation patrimoniale.
    if deuxieme:
        annexe = re.search(r"\b(?:ANNEXE|Annexe) A\s+(?:RAPPORT|Rapport)", flux[fin:])
        if annexe is None:
            sys.exit(f"{origine} : annexe A introuvable")
        debut_annexe = fin + annexe.start()
        suite = re.search(r"\b(?:ANNEXE|Annexe) B\s+(?:RAPPORT|Rapport)", flux[debut_annexe:])
        fin_annexe = debut_annexe + suite.start() if suite else len(flux)
    else:
        debut_annexe, fin_annexe = fin, len(flux)
    if re.search(r"Est approuvé le rapport figurant en annexe[^.]*situation patrimoniale", flux):
        annexe_brutes, annexe_lus = lignes_annexe(grilles, flux, debut_annexe, fin_annexe, annee, origine)
        brutes += annexe_brutes
    elif any(a_montants(grilles[k]) for k, _ in tableaux_entre(flux, debut_annexe, fin_annexe)):
        sys.exit(f"{origine} : tableau à montants dans une annexe A sans situation patrimoniale")
    return annee, brutes


def lignes_du_fichier(fichier):
    """Les chiffres d'une copie archivée."""
    annee, brutes = lignes_du_texte(BASE / fichier["chemin"], fichier["id"])
    version = fichier["mis_a_jour_source"][:10]
    if not version or not annee < int(version[:4]) <= annee + 2:
        sys.exit(f"{fichier['id']} : comptes de {annee} dans un texte daté « {version} »")
    for brute in brutes:
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": brute["emplacement"],
            "zone": "FR", "perimetre_id": brute["perimetre"], "concept_id": brute["concept"],
            "fonction_id": brute["fonction"], "traitements": "", "unite_id": brute["unite"],
            "periode": brute.get("periode", str(annee)),
            "valeur": brute["nombre"][0], "decimales": brute["nombre"][1], "statut": brute["statut"],
            "drapeau_source": "", "version": version, "consolidation": brute["consolidation"], "denominateur_id": "",
            "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": brute.get("note", ""),
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
    ajoutes, inchanges = fusionner(existants, list(lignes_du_fichier(fichier)), fichier["id"])
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
