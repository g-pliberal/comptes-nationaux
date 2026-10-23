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
  administrations de sécurité sociale au sens de la comptabilité nationale, en points de produit intérieur brut.
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
            "fonction_id": brute["fonction"], "traitements": "", "unite_id": brute["unite"], "periode": str(annee),
            "valeur": brute["nombre"][0], "decimales": brute["nombre"][1], "statut": brute["statut"],
            "drapeau_source": "", "version": version, "consolidation": brute["consolidation"], "denominateur_id": "",
            "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": "",
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
