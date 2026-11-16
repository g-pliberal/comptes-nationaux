#!/usr/bin/env python3
"""Enregistre dans la base le coût de chaque dépense fiscale (« niche fiscale »), tel que le chiffre le tome II de
l'annexe « Évaluations des voies et moyens » d'un projet de loi de finances, lu dans le PDF du tome quand la direction du
budget n'en publie pas la liste en classeur avec ses montants (projets de loi pour 2019 et pour 2024 à 2027). Les classeurs des
projets de loi pour 2020 à 2023 sont lus par outils/importer_depenses_fiscales.py, avec les mêmes conventions.

    python3 outils/importer_depenses_fiscales_pdf.py <fichier_id>

La « Liste des dépenses fiscales » du tome donne une fiche par dépense : son numéro à six chiffres et son libellé
(« 100101 – Déduction des versements… », sur une ou plusieurs lignes), puis un cadre « Impact budgétaire (en millions
d'euros) » dont la gauche porte trois colonnes, « Réalisation », « Prévision », « Prévision », leurs années et leurs
montants. Les fiches sont rangées sous l'impôt dont elles relèvent, un titre seul sur sa ligne (CATEGORIES). Tout ce qui
ne se lit pas comme prévu arrête l'import :

- les en-têtes des trois colonnes doivent être « Réalisation », « Prévision », « Prévision », et leurs années les deux
  qui précèdent celle du projet de loi, puis celle-ci ;
- chaque montant va dans la colonne dont il est le plus près ; une colonne sans montant, ou avec deux, arrête l'import.
  Le lecteur de PDF lit la page avec la fin de chaque morceau de texte (lire_pdf(…, fins=True)) ; les milliers, que
  certaines pages dessinent à part (« 1 » et « 836 »), sont recollés. Un montant que la page dessine sur une autre ligne
  que ses voisins (« ε », d'une autre police) est lu sur la sienne ;
- une case sans montant doit être l'une de celles que le tome explique : « - » (aucun effet budgétaire), « ε » (moins de
  0,5 million d'euros), « nc » (non chiffré), en capitales ou non ;
- un numéro ne doit pas revenir deux fois, et chaque fiche doit avoir son cadre.

Une dépense fiscale est la fonction LOLF.DEPENSE_FISCALE.<numéro>, créée s'il le faut avec le libellé du premier tome
importé qui la porte ; chaque chiffre garde dans ses notes l'impôt sous lequel son tome la range (« Catégorie : Impôt sur
le revenu »). Le chiffre est une estimation pour l'année de la « Réalisation », une prévision pour les deux autres. Son
emplacement est sa page, le rang de sa ligne dans la page et l'étendue des abscisses de sa case, à un point près
(commun.montant_colonne_pdf), où le contrôle le relit. La période d'un chiffre est son année, sa version la date de
modification inscrite dans le PDF.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_pdf,
                    montant_colonne_pdf, table_des_chiffres)

SOURCE = re.compile(r"budget\.depenses-fiscales-plf([0-9]{4})")
RACINE = CONCEPT = "LOLF.DEPENSE_FISCALE"
CATEGORIES = {"Impôt sur le revenu", "Impôt sur le revenu et impôt sur les sociétés", "Impôt sur les sociétés",
              "Autres impôts directs", "Droits d'enregistrement et de timbre", "Taxe sur la valeur ajoutée",
              "Accise sur les énergies", "Autres droits", "Impôts locaux"}
# Projets de loi dont le tome range ses dépenses en tableaux (lignes_en_tableau), et l'impôt que nomme le titre courant
# de ses pages, sous le nom que lui donnent les listes des projets de loi suivants.
EN_TABLEAU = {2019}
TITRES_COURANTS = {"IMPÔT SUR LE REVENU": "Impôt sur le revenu",
                   "IMPÔT SUR LE REVENU ET IMPÔT SUR LES SOCIÉTÉS": "Impôt sur le revenu et impôt sur les sociétés",
                   "IMPÔT SUR LES SOCIÉTÉS": "Impôt sur les sociétés", "AUTRES IMPÔTS DIRECTS": "Autres impôts directs",
                   "DROITS D'ENREGISTREMENT ET DE TIMBRE": "Droits d'enregistrement et de timbre",
                   "TAXE SUR LA VALEUR AJOUTÉE": "Taxe sur la valeur ajoutée",
                   "TAXE INTÉRIEURE DE CONSOMMATION SUR LES PRODUITS":
                       "Taxe intérieure de consommation sur les produits énergétiques",
                   "AUTRES DROITS": "Autres droits", "IMPÔTS LOCAUX": "Impôts locaux"}
SANS_MONTANT = {"-", "ε", "nc"}  # sans égard à la casse : le tome pour 2027 écrit aussi « Ε » et « Nc »
STATUTS = ("estimation", "prevision", "prevision")
FICHE = re.compile(r"([0-9]{6}) – (.+)")
MONTANT = re.compile(r"-?[0-9]{1,3}( [0-9]{3})*")


def texte(morceaux):
    """Les morceaux d'une ligne bout à bout, une espace entre deux morceaux qu'écarte un blanc."""
    resultat, fin = "", None
    for x, t, f in sorted(morceaux):
        resultat += (" " if fin is not None and x - fin >= 1.5 else "") + t
        fin = f
    return " ".join(resultat.split())


def cadre(page, lignes, n, plf, lieu):
    """Les trois cases du cadre dont l'en-tête est la ligne n (0 pour la première) : [(année, statut, [(ligne, morceaux
    de la case)])], la ligne comptée à partir de 1."""
    tete = [m for m in sorted(lignes[n][1]) if m[1].strip()][:3]
    if [m[1].strip() for m in tete] != ["Réalisation", "Prévision", "Prévision"]:
        sys.exit(f"{lieu} : en-têtes inattendus {[m[1] for m in tete]}")
    limite = tete[2][2] + 15
    gauche = lambda k: [m for m in sorted(lignes[k][1]) if m[1].strip() and m[0] < limite]
    pleines = [k for k in range(n + 1, min(n + 12, len(lignes))) if gauche(k)]
    if len(pleines) < 2:
        sys.exit(f"{lieu} : cadre sans années ou sans montants")
    annees = gauche(pleines[0])
    if [m[1].strip() for m in annees] != [str(a) for a in range(plf - 2, plf + 1)]:
        sys.exit(f"{lieu} : années {[m[1] for m in annees]}, attendues {plf - 2}, {plf - 1} et {plf}")
    centres = [(m[0] + m[2]) / 2 for m in annees]
    y = lignes[pleines[1]][0]
    cases = [[] for _ in centres]
    for k in pleines[1:]:
        if abs(lignes[k][0] - y) > 3:
            break
        precedent = None
        for m in gauche(k):
            # Un groupe de trois chiffres collé au nombre qui le précède en est le millier.
            if precedent and re.fullmatch(r"[0-9]{3}", m[1].strip()) and m[0] - precedent[2] < 4:
                cases[i][-1][1].append(m)
            else:
                i = min(range(len(centres)), key=lambda j: abs(centres[j] - (m[0] + m[2]) / 2))
                cases[i].append((k + 1, [m]))
            precedent = m
    for annee, case in zip(annees, cases):
        if len(case) != 1:
            sys.exit(f"{lieu} : {len(case)} montants sous {annee[1].strip()}")
    return [(int(a[1]), statut, case[0]) for a, statut, case in zip(annees, STATUTS, cases)]


def lignes_du_fichier(fichier, fonctions):
    trouve = SOURCE.fullmatch(fichier["source_id"])
    if trouve is None:
        sys.exit(f"{fichier['id']} : la source n'est pas une liste des dépenses fiscales")
    plf = int(trouve.group(1))
    pages = lire_pdf(BASE / fichier["chemin"], fins=True)
    if plf in EN_TABLEAU:
        yield from lignes_en_tableau(fichier, pages, plf, fonctions)
        return
    categorie, fiche, vus = None, None, set()
    for page, lignes in enumerate(pages, 1):
        for n, (_, morceaux) in enumerate(lignes):
            ligne = texte(morceaux)
            lieu = f"{fichier['id']}, page {page}, ligne {n + 1}"
            if ligne in CATEGORIES:
                categorie = ligne
                continue
            trouve = FICHE.fullmatch(ligne)
            if trouve and categorie:
                if fiche:
                    sys.exit(f"{lieu} : la fiche {fiche['numero']} n'a pas de cadre « Impact budgétaire »")
                if trouve.group(1) in vus:
                    sys.exit(f"{lieu} : la dépense fiscale {trouve.group(1)} revient deux fois")
                vus.add(trouve.group(1))
                fiche = {"numero": trouve.group(1), "libelle": [trouve.group(2)], "categorie": categorie}
            elif fiche and re.match(r"Finalité|Impact budgétaire", ligne):  # la fin du libellé
                fiche["complet"] = True
            elif fiche and not fiche.get("complet") and ligne:
                fiche["libelle"].append(ligne)
            elif fiche and re.match(r"Réalisation Prévision Prévision", ligne):
                yield from chiffres(fichier, fiche, page, cadre(page, lignes, n, plf, lieu), lignes, fonctions)
                fiche = None
    if fiche:
        sys.exit(f"{fichier['id']} : la fiche {fiche['numero']} n'a pas de cadre « Impact budgétaire »")
    if not vus:
        sys.exit(f"{fichier['id']} : aucune dépense fiscale")


def lignes_en_tableau(fichier, pages, plf, fonctions):
    """Les tomes d'avant 2020 (EN_TABLEAU) : des pages « Chiffrages des dépenses fiscales », dont le titre courant nomme
    l'impôt, et des tableaux dont l'en-tête nomme les trois années, une ligne par dépense : son numéro en marge, son
    libellé, sur une ou plusieurs lignes, et ses montants à droite, sous leurs années, sur la ligne du numéro ; puis les
    rubriques de la fiche (« Mission et programme : », « Bénéficiaires »…), qui ne sont pas lues."""
    vus, colonnes = set(), None
    for page, lignes in enumerate(pages, 1):
        tete = [texte(m) for _, m in lignes[:5]]
        if "Chiffrages des dépenses fiscales" not in tete:
            continue
        impot = next((t.replace("Voies et Moyens II", "").strip() for t in tete if "Voies et Moyens II" in t), "")
        if impot not in TITRES_COURANTS:
            continue  # les mesures que le tome ne compte pas comme des dépenses fiscales (« Norme fiscale de référence »)
        fiche = None
        for n, (_, morceaux) in enumerate(lignes):
            lieu = f"{fichier['id']}, page {page}, ligne {n + 1}"
            pleins = [m for m in sorted(morceaux) if m[1].strip()]
            if len(pleins) >= 3 and all(re.fullmatch(r"(19|20)[0-9]{2}", m[1].strip()) for m in pleins[-3:]):
                annees = [int(m[1]) for m in pleins[-3:]]
                if annees != list(range(plf - 2, plf + 1)):
                    sys.exit(f"{lieu} : années {annees}, attendues {plf - 2}, {plf - 1} et {plf}")
                colonnes = pleins[-3:]
                continue
            if pleins and re.fullmatch(r"[0-9]{6}", pleins[0][1].strip()) and pleins[0][0] < 100:
                if colonnes is None:
                    sys.exit(f"{lieu} : dépense fiscale avant l'en-tête de son tableau")
                numero = pleins[0][1].strip()
                if numero in vus:
                    sys.exit(f"{lieu} : la dépense fiscale {numero} revient deux fois")
                vus.add(numero)
                limite = colonnes[0][0] - 25
                libelle = [texte([m for m in pleins[1:] if m[0] < limite])]
                centres = [(m[0] + m[2]) / 2 for m in colonnes]
                cases, precedent = [[] for _ in centres], None
                for m in [m for m in pleins[1:] if m[0] >= limite]:
                    if precedent and re.fullmatch(r"[0-9]{3}", m[1].strip()) and m[0] - precedent[2] < 4:
                        cases[i][-1][1].append(m)  # le millier d'un nombre que la page dessine à part
                    else:
                        i = min(range(3), key=lambda j: abs(centres[j] - (m[0] + m[2]) / 2))
                        cases[i].append((n + 1, [m]))
                    precedent = m
                if any(len(c) > 1 for c in cases) or not any(cases):
                    sys.exit(f"{lieu} : montants {[len(c) for c in cases]} sous les trois années")
                fiche = {"numero": numero, "libelle": libelle, "categorie": TITRES_COURANTS[impot],
                         "cases": [(a, statut, c[0]) for a, statut, c in zip(annees, STATUTS, cases) if c]}
                continue
            if fiche and pleins and pleins[0][0] > 100 and texte(morceaux) and not fiche.get("complet"):
                fiche["libelle"].append(texte(morceaux))
            elif fiche:
                fiche["complet"] = True
                yield from chiffres(fichier, fiche, page, fiche["cases"], lignes, fonctions)
                fiche = None
        if fiche:
            yield from chiffres(fichier, fiche, page, fiche["cases"], lignes, fonctions)
    if not vus:
        sys.exit(f"{fichier['id']} : aucune dépense fiscale")


def chiffres(fichier, fiche, page, cases, lignes, fonctions):
    fonction = f"{RACINE}.{fiche['numero']}"
    if fonction not in fonctions:
        fonctions[fonction] = {"id": fonction, "libelle": " ".join(fiche["libelle"]), "norme_id": "LOLF",
                               "parent_id": RACINE}
    for annee, statut, (n, morceaux) in cases:
        contenu = " ".join(m[1].strip() for m in morceaux)
        lieu = f"{fichier['id']}, page {page}, ligne {n}"
        if contenu.lower() in SANS_MONTANT:
            continue
        if not MONTANT.fullmatch(contenu):
            sys.exit(f"{lieu} : « {contenu} » n'est pas un montant")
        # L'étendue déborde d'un point de part et d'autre de la case, pour que l'arrondi au dixième ne la coupe pas.
        debut, fin = round(morceaux[0][0] - 1, 1), round(morceaux[-1][0] + 1, 1)
        valeur = montant_colonne_pdf(lignes[n - 1][1], debut, fin)
        if valeur is None or float(valeur[0]) != float(contenu.replace(" ", "")):
            sys.exit(f"{lieu} : « {contenu} » relu {valeur}")
        texte_valeur, decimales = valeur
        chiffre = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": f"page={page};ligne={n};colonne={debut:.1f}-{fin:.1f}", "zone": "FR",
            "perimetre_id": "ETAT_LF", "concept_id": CONCEPT, "fonction_id": fonction, "traitements": "",
            "unite_id": "MIO_EUR", "periode": str(annee), "valeur": texte_valeur, "decimales": decimales,
            "statut": statut, "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10],
            "consolidation": "sans_objet", "denominateur_id": "", "nature": "publie", "calcul_id": "",
            "saisi_le": aujourdhui(), "notes": f"Catégorie : {fiche['categorie']}",
        }
        chiffre["id"] = identifiant(chiffre)
        yield chiffre


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    if RACINE not in fonctions:
        sys.exit(f"fonction {RACINE} absente de tables/fonctions.csv")
    avant = set(fonctions)
    nouveaux = list(lignes_du_fichier(fichier, fonctions))
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, nouveaux, fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte "
          f"{len(existants)} ; {len(set(fonctions) - avant)} fonctions nouvelles")


if __name__ == "__main__":
    main()
