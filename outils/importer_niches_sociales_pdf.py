#!/usr/bin/env python3
"""Enregistre dans la base le coût des « niches sociales » d'avant 2021, mesure par mesure et branche par branche, tel
que le donnent les tableaux financiers de l'annexe 5 des projets de loi de financement de la sécurité sociale (PLFSS)
pour 2008 à 2022, « Présentation des mesures d'exonération de cotisations et contributions et de leurs mesures de
compensation », que la direction de la sécurité sociale publie en PDF sur securite-sociale.fr. Les classeurs des
éditions suivantes sont lus par outils/importer_niches_sociales.py.

    python3 outils/importer_niches_sociales_pdf.py <fichier_id>

Chaque annexe donne, pour chaque branche (maladie, accidents du travail et maladies professionnelles, vieillesse,
famille, et autonomie depuis l'édition pour 2021), le coût des allègements généraux et des exonérations ciblées de
cotisations, une ligne par mesure, sous des lignes de titre qui en portent la somme, pour trois années : celle des
derniers comptes connus et les deux suivantes, en prévision. Les pages lues, la branche de chacune et le statut de
chaque année sont déclarés édition par édition (EDITIONS) ; le reste se lit sur la page, et tout ce qui ne s'y lit pas
comme prévu arrête l'import :

- l'en-tête du tableau nomme ses années, dans l'ordre déclaré, et, dans les éditions qui en ont, ses colonnes
  d'évolution (« Évolution 2007/2006 ») ; la page ne doit pas dire ses montants dans une autre unité que le million
  d'euros (les tableaux des éditions récentes ne la rappellent pas : l'annexe la dit) ;
- les colonnes se lisent sur la page, que le lecteur lit avec la fin de chaque morceau de texte (lire_pdf(…,
  fins=True)) : les nombres du tableau, alignés à droite, rangés selon l'abscisse où ils finissent, doivent former
  autant de groupes que l'en-tête nomme de colonnes, séparés par un blanc au moins double de la largeur du plus large
  groupe. Chaque cellule va dans la colonne où elle finit ; deux cellules dans une même colonne d'une ligne arrêtent
  l'import. L'emplacement d'un chiffre est sa page, le rang de sa ligne dans la page et l'étendue des abscisses de sa
  cellule, à un point près (commun.montant_colonne_pdf), où le contrôle le relit ;
- le libellé d'une mesure est le texte de sa ligne à gauche des colonnes, sans le numéro de fiche ou le code de la
  mesure, et celui des lignes sans nombre qui l'entourent de près : un libellé sur deux ou trois lignes encadre ses
  montants. Une ligne sans nombre plus éloignée d'une ligne de montants est un titre ;
- une cellule qui ne porte pas de nombre doit être vide, un tiret, « ns », « nd » ou un signe (« + », « ++ ») ; les
  colonnes d'évolution des éditions pour 2008 à 2016 ne sont pas lues.

Une page qui continue le tableau de la précédente ne rappelle pas toujours sa branche : seule la première page de chaque
branche doit la nommer.

Une mesure est la fonction COMPTES_SECU.EXO_<libellé>, comme dans les classeurs ; une ligne de titre (en capitales, ou
« Sous-total », « Total ») aussi. La branche est le périmètre du chiffre (les régimes obligatoires de base, branche par
branche : ROBSS_MALADIE, ROBSS_ATMP, ROBSS_VIEILLESSE, ROBSS_FAMILLE, ROBSS_AUTONOMIE) ; les tableaux couvrent tous les
régimes. Chaque chiffre garde dans ses notes la ligne de titre sous laquelle son tableau le range. Une ligne « Dont… »
prend le nom de la mesure qui la précède ; une mesure que le tableau répète sous une autre rubrique prend le nom de
cette rubrique. Les sommes ne sont pas refaites ici : le rapport de cohérence les fait, et compare les éditions entre
elles. La période d'un chiffre est son année, sa version la date de modification inscrite dans le PDF.

Sont lues les annexes pour 2008 et pour 2010 à 2022 ; ne le sont pas celle pour 2007, dont les tableaux sont des
dessins et non du texte, ni celle pour 2009, écrite dans une police sans table de ses caractères.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_pdf,
                    montant_colonne_pdf, table_des_chiffres, texte_pdf)
from importer_lois_resultats import code_lolf

R, P = "definitif", "prevision"
BRANCHES = {"maladie": "ROBSS_MALADIE", "atmp": "ROBSS_ATMP", "vieillesse": "ROBSS_VIEILLESSE",
            "famille": "ROBSS_FAMILLE", "autonomie": "ROBSS_AUTONOMIE"}
# Ce que l'en-tête d'un tableau dit de sa branche.
NOMS_BRANCHES = {"maladie": r"branche\s*maladie", "atmp": r"branche\s*(AT-MP|accidents?\s*du\s*travail)",
                 "vieillesse": r"branche\s*vieillesse", "famille": r"branche\s*famille",
                 "autonomie": r"branche\s*autonomie"}


def _colonnes(annee, evolutions=True):
    """Les colonnes d'un tableau : l'année des derniers comptes connus, puis les deux suivantes, en prévision, chacune
    suivie, dans les éditions qui en ont, de la colonne de son évolution (None : une colonne qui n'est pas lue)."""
    if evolutions:
        return ((annee, R), (annee + 1, P), None, (annee + 2, P), None)
    return ((annee, R), (annee + 1, P), (annee + 2, P))


def _pages(*groupes):
    """{page : branche} de groupes (branche, première page, dernière page)."""
    return {p: b for b, debut, fin in groupes for p in range(debut, fin + 1)}


# Source → ({page : branche}, colonnes, {page : colonnes d'une page qui n'a pas celles de son édition}).
EDITIONS = {
    "secu.plfss2008-annexe5": (_pages(("maladie", 181, 182), ("atmp", 183, 184), ("vieillesse", 185, 186),
                                      ("famille", 187, 188)), _colonnes(2006), {}),
    "secu.plfss2010-annexe5": (_pages(("maladie", 200, 201), ("atmp", 202, 203), ("vieillesse", 204, 205),
                                      ("famille", 206, 207)), _colonnes(2008), {}),
    "secu.plfss2011-annexe5": (_pages(("maladie", 216, 217), ("atmp", 218, 219), ("vieillesse", 220, 221),
                                      ("famille", 222, 223)), _colonnes(2009), {}),
    "secu.plfss2012-annexe5": (_pages(("maladie", 252, 253), ("atmp", 254, 254), ("vieillesse", 255, 256),
                                      ("famille", 257, 258)), _colonnes(2010), {}),
    "secu.plfss2013-annexe5": (_pages(("maladie", 256, 257), ("atmp", 258, 258), ("vieillesse", 259, 260),
                                      ("famille", 261, 262)), _colonnes(2011), {}),
    "secu.plfss2014-annexe5": (_pages(("maladie", 284, 285), ("atmp", 286, 286), ("famille", 287, 288),
                                      ("vieillesse", 289, 290)), _colonnes(2012), {}),
    "secu.plfss2015-annexe5": (_pages(("maladie", 306, 306), ("atmp", 307, 307), ("famille", 308, 308),
                                      ("vieillesse", 309, 309)), _colonnes(2013), {}),
    # La page de la branche vieillesse de l'édition pour 2016 n'a pas de colonne d'évolution après sa dernière année.
    "secu.plfss2016-annexe5": (_pages(("maladie", 316, 316), ("atmp", 317, 317), ("famille", 318, 318),
                                      ("vieillesse", 319, 319)), _colonnes(2014),
                               {319: ((2014, R), (2015, P), None, (2016, P))}),
    "secu.plfss2017-annexe5": (_pages(("maladie", 44, 44), ("atmp", 45, 45), ("famille", 46, 46),
                                      ("vieillesse", 47, 47)), _colonnes(2015, False), {}),
    "secu.plfss2018-annexe5": (_pages(("maladie", 45, 45), ("atmp", 46, 46), ("famille", 47, 47),
                                      ("vieillesse", 48, 48)), _colonnes(2016, False), {}),
    "secu.plfss2019-annexe5": (_pages(("maladie", 46, 46), ("atmp", 47, 47), ("famille", 48, 48),
                                      ("vieillesse", 49, 49)), _colonnes(2017, False), {}),
    "secu.plfss2020-annexe5": (_pages(("maladie", 46, 46), ("atmp", 47, 47), ("famille", 48, 48),
                                      ("vieillesse", 49, 49)), _colonnes(2018, False), {}),
    # La branche autonomie, créée en 2021, n'a que la colonne de cette année.
    "secu.plfss2021-annexe5": (_pages(("maladie", 44, 44), ("atmp", 45, 45), ("famille", 46, 46),
                                      ("vieillesse", 47, 47), ("autonomie", 48, 48)), _colonnes(2019, False),
                               {48: ((2021, P),)}),
    "secu.plfss2022-annexe5": (_pages(("maladie", 47, 47), ("atmp", 48, 48), ("famille", 49, 49),
                                      ("vieillesse", 50, 50), ("autonomie", 51, 51)), _colonnes(2020, False), {}),
}
CONCEPT = "LFSS.EXONERATION_COUT"
RACINE = "COMPTES_SECU.EXONERATIONS"
SANS_MONTANT = {"", "-", "–", "ns", "n.s.", "nd", "n.d.", "+", "++", "--", "#DIV/0!"}
# Ce qu'écrit l'en-tête d'un tableau au-dessus de ses colonnes.
ENTETE = re.compile(r"(Co[uû]ts?\s*\*?|[ÉEé]volution|\(M€\)|\(%\)|(19|20)[0-9]{2}\s*(\((p|P)\))?\*?|"
                    r"(19|20)[0-9]{2}\s*/\s*(19|20)[0-9]{2})(\s+\S.*)?", re.I)
# Abscisse en deçà de laquelle rien n'est une cellule de montant : le libellé et le numéro de la mesure.
MARGE = 15
# Deux colonnes de montants alignés à droite finissent à au moins ce blanc l'une de l'autre.
ECART_COLONNES = 9
# Écart vertical au-delà duquel une ligne sans nombre n'appartient plus au libellé d'une ligne de montants.
ECART_LIBELLE = 5.5
NOMBRE = re.compile(r"%?\s*[-−–+]?\s*[0-9][0-9 \u00a0]*(,[0-9]+)?\s*%?|[-–]|ns|n\.?s\.?|n\.?d\.?|\+\+?|--|#DIV/0!")


def propre(texte):
    return " ".join(str(texte).split())


def joindre(morceaux):
    """Le texte de morceaux d'une ligne (abscisse, texte, fin), mis bout à bout : un blanc d'au moins un point entre la
    fin de l'un et le début du suivant est une espace, que la page ne dessine pas quand elle place chaque lettre."""
    texte, fin = "", None
    for x, t, f in morceaux:
        if fin is not None and x - fin >= 1 and not texte.endswith(" ") and not t.startswith(" "):
            texte += " "
        texte, fin = texte + t, f
    return propre(texte)


def sans_code(texte):
    """Le texte d'une ligne de libellé sans le numéro de fiche ou le code de la mesure qui le précède dans sa colonne
    (« 24/27/40/60 », « 01100 », « C du 2 ») ni l'en-tête de cette colonne (« n° de fiche », « Code »)."""
    code = r"(n°\s*de\s*fiche|Codes?)?\s*([0-9]{1,5}(\s*/\s*[0-9]{1,2})*|[A-Z] du [0-9]+)?"
    if re.fullmatch(code + r"\s*", texte):
        return ""
    return re.sub(r"^" + code + r"\s*(?=[^\s0-9/])", "", texte, count=1)


def en_capitales(libelle):
    lettres = re.sub(r"[^A-Za-zÀ-ÿ]", "", libelle)
    return len(lettres) >= 3 and lettres == lettres.upper()


def entete(lignes, annees, lieu):
    """(abscisse où commencent les colonnes, ordonnée) de la ligne d'en-tête qui nomme les années du tableau, et elles
    seules, dans l'ordre : la première de ces années commence la première colonne de montants."""
    for y, morceaux in lignes:
        texte = re.sub(r"\s", "", "".join(t for _, t, *_ in sorted(morceaux)))
        if [int(a) for a in re.findall(r"(?:19|20)[0-9]{2}", texte)] != list(annees):
            continue
        cumul = ""
        for x, t, *_ in sorted(morceaux):
            cumul += re.sub(r"\s", "", t)
            if str(annees[0]) in cumul:
                return x, y
    sys.exit(f"{lieu} : aucun en-tête ne nomme les années {', '.join(map(str, annees))}")


def colonnes_de_la_page(fins, lieu, attendus):
    """Les fins des colonnes : les abscisses où finissent les cellules de montants, qui sont alignés à droite, rangées en
    groupes séparés d'au moins ECART_COLONNES ; il doit y en avoir autant que de colonnes déclarées, et le blanc entre
    deux groupes doit faire au moins deux fois le plus large d'entre eux (des entiers et des décimaux, un signe %, ne
    finissent pas tout à fait au même endroit), sinon les colonnes ne se distinguent pas sûrement."""
    xs = sorted(fins)
    groupes = [[xs[0]]]
    for x in xs[1:]:
        if x - groupes[-1][-1] >= ECART_COLONNES:
            groupes.append([x])
        else:
            groupes[-1].append(x)
    largeur = max(g[-1] - g[0] for g in groupes)
    blanc = min((b[0] - a[-1] for a, b in zip(groupes, groupes[1:])), default=1000)
    if len(groupes) != attendus or blanc < 2 * largeur:
        sys.exit(f"{lieu} : les montants finissent en {len(groupes)} groupes "
                 f"({', '.join(f'{g[0]:.0f}-{g[-1]:.0f}' for g in groupes)}) pour {attendus} colonnes déclarées")
    return [(g[0] - ECART_COLONNES / 2, g[-1] + ECART_COLONNES / 2) for g in groupes]


def lignes_du_tableau(fichier, page, branche, colonnes, lignes, fonctions, cles, suite=False):
    """Les chiffres du tableau d'une page ; `suite` : la page continue le tableau de la précédente, qu'elle ne renomme
    pas toujours."""
    lieu = f"{fichier['id']}, page {page}"
    texte = propre(" ".join(texte_pdf(m) for _, m in lignes))
    if not suite and not re.search(NOMS_BRANCHES[branche], texte, re.I):
        sys.exit(f"{lieu} : la page ne nomme pas la branche {branche}")
    if re.search(r"milliards|Md€|en euros|milliers", texte, re.I):
        sys.exit(f"{lieu} : la page dit ses montants dans une autre unité que le million d'euros")
    colonnes = list(colonnes)
    x_entete, y_entete = entete(lignes, [c[0] for c in colonnes if c is not None], lieu)
    limite = x_entete - MARGE
    # Les cellules de montants : sous l'en-tête, à droite de la limite des libellés ; des morceaux que séparent moins de
    # trois points (des chiffres qu'une page dessine un à un, l'espace des milliers), ou un signe % qui suit un nombre,
    # forment une même cellule.
    par_ligne = {}
    for n, (y, morceaux) in enumerate(lignes, 1):
        if y >= y_entete - 1:
            continue
        courant = None
        for x, t, fin in sorted(morceaux):
            if x < limite or not t.strip() or re.fullmatch(r"\s*\[[0-9IVX]+\]\s*", t):
                continue  # un appel de note (« [1] ») n'est pas une cellule
            if courant and (x - courant[-1][2] < 3 or t.strip() == "%" and x - courant[-1][2] < 8):
                courant.append((x, t, fin))
            else:
                courant = [(x, t, fin)]
                par_ligne.setdefault(n, []).append(courant)
    contenu = lambda cellule: propre("".join(t for _, t, _ in cellule))
    # Une ligne dont une cellule n'est pas un montant n'est pas une ligne du tableau : elle doit le précéder (la fin de
    # l'en-tête : « Coût », « Évolution ») ou le suivre (le pied de page, une note) ; un texte au milieu du tableau, à
    # droite de ses libellés, arrête l'import.
    # Un tableau qui en suit un autre sur la même page répète son en-tête : ses lignes ne sont pas des lignes de montants.
    for n in [n for n, c in par_ligne.items() if all(ENTETE.fullmatch(contenu(x)) for x in c)]:
        del par_ligne[n]
    autres = [n for n, c in par_ligne.items() if not all(NOMBRE.fullmatch(contenu(x)) for x in c)]
    nombres = [n for n in par_ligne if n not in autres]
    for n in autres:
        if nombres and min(nombres) < n < max(nombres):
            mauvaise = next(contenu(x) for x in par_ligne[n] if not NOMBRE.fullmatch(contenu(x)))
            sys.exit(f"{lieu}, ligne {n} : « {mauvaise} » n'est pas un montant")
        del par_ligne[n]
    if not par_ligne:
        sys.exit(f"{lieu} : aucun montant")
    # Les cellules sans montant (un tiret, souvent centré) ne comptent pas pour situer les colonnes, et ne donnent pas de
    # chiffre.
    etendues = colonnes_de_la_page([c[-1][2] for cs in par_ligne.values() for c in cs
                                    if contenu(c) not in SANS_MONTANT], lieu, len(colonnes))
    # Chaque cellule dans sa colonne, d'après l'abscisse où elle finit ; deux cellules dans une même colonne d'une ligne
    # arrêtent l'import.
    cellules = {}
    for n, cs in par_ligne.items():
        for cellule in cs:
            if contenu(cellule) in SANS_MONTANT:
                continue
            k = next(k for k, (a, b) in enumerate(etendues) if a <= cellule[-1][2] <= b)
            if (n, k) in cellules:
                sys.exit(f"{lieu}, ligne {n} : deux montants dans la colonne {k + 1}")
            cellules[(n, k)] = cellule
    # Les lignes de montants et les lignes de texte, sous l'en-tête.
    montants, textes = {}, []
    for n, (y, morceaux) in enumerate(lignes, 1):
        if y >= y_entete - 1:
            continue
        libelle = joindre([m for m in sorted(morceaux) if m[0] < limite])
        if n in par_ligne:
            montants[n] = (y, [(y, libelle)] if libelle else [])
        elif libelle:
            textes.append((n, y, libelle))
    titres = []
    for n, y, libelle in textes:
        proche = min(montants, key=lambda m: abs(montants[m][0] - y), default=None)
        if proche is not None and abs(montants[proche][0] - y) <= ECART_LIBELLE:
            montants[proche][1].append((y, libelle))
        else:
            titres.append((n, libelle))
    rubrique, mesure, lues = "", "", 0
    evenements = sorted([(n, "titre", l) for n, l in titres] + [(n, "montants", None) for n in montants])
    for n, sorte, libelle in evenements:
        if sorte == "titre":
            if en_capitales(re.sub(r"\(.*?\)|\[.*?\]", "", libelle)):
                rubrique = libelle
            continue
        libelle = propre(" ".join(sans_code(t) for _, t in sorted(montants[n][1], key=lambda p: -p[0])))
        libelle = propre(re.sub(r"\*+|\([0-9]\)|\[[0-9IVX]+\]\s*(\+\s*\[[0-9IVX]+\])?$", "", libelle))
        if not libelle:
            sys.exit(f"{lieu}, ligne {n} : montants sans libellé")
        titre = en_capitales(re.sub(r"\(.*?\)|\[.*?\]", "", libelle)) or re.match(r"(sous-)?total", libelle, re.I)
        # Deux libellés qui ne diffèrent que par la casse ou les accents (un titre et sa seule mesure) donnent la même
        # fonction : c'est elle qui ne doit pas revenir.
        cle = f"{libelle} ({mesure})" if libelle.lower().startswith("dont ") else libelle
        if code_lolf(cle) in cles:
            cle = f"{libelle} ({rubrique})"
        if code_lolf(cle) in cles:
            cle = f"{libelle} ({mesure})"
        if code_lolf(cle) in cles:
            sys.exit(f"{lieu}, ligne {n} : le libellé « {libelle} » revient deux fois sous « {rubrique} »")
        cles.add(code_lolf(cle))
        fonction = f"COMPTES_SECU.EXO_{code_lolf(cle)}"
        if fonction not in fonctions:
            fonctions[fonction] = {"id": fonction, "libelle": cle, "norme_id": "LFSS", "parent_id": RACINE}
        note = "Ligne de titre du tableau." if titre else f"Sous : {rubrique}" if rubrique else ""
        for k, colonne in enumerate(colonnes):
            if colonne is None or (n, k) not in cellules:
                continue
            annee, statut = colonne
            cellule = cellules[(n, k)]
            # L'étendue déborde d'un point de part et d'autre de la cellule (que trois points au moins séparent de ses
            # voisines), pour que l'arrondi de l'emplacement au dixième ne la coupe pas.
            debut, fin = round(cellule[0][0] - 1, 1), round(cellule[-1][0] + 1, 1)
            valeur = montant_colonne_pdf(lignes[n - 1][1], debut, fin)
            if valeur is None:
                if contenu(cellule) not in SANS_MONTANT:
                    sys.exit(f"{lieu}, ligne {n} : « {contenu(cellule)} » n'est pas un montant")
                continue
            texte_valeur, decimales = valeur
            chiffre = {
                "source_id": fichier["source_id"], "fichier_id": fichier["id"],
                "emplacement": f"page={page};ligne={n};colonne={debut:.1f}-{fin:.1f}", "zone": "FR",
                "perimetre_id": BRANCHES[branche], "concept_id": CONCEPT, "fonction_id": fonction, "traitements": "",
                "unite_id": "MIO_EUR", "periode": str(annee), "valeur": texte_valeur, "decimales": decimales,
                "statut": statut, "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10],
                "consolidation": "sans_objet", "denominateur_id": "", "nature": "publie", "calcul_id": "",
                "saisi_le": aujourdhui(), "notes": note,
            }
            chiffre["id"] = identifiant(chiffre)
            lues += 1
            yield chiffre
        if titre and not re.match(r"(sous-)?total", libelle, re.I):
            rubrique = libelle
        elif not libelle.lower().startswith("dont "):
            mesure = libelle
    if not lues:
        sys.exit(f"{lieu} : aucun montant")


def lignes_du_fichier(fichier, fonctions):
    if fichier["source_id"] not in EDITIONS:
        sys.exit(f"{fichier['id']} : source sans pages déclarées (EDITIONS)")
    pages, colonnes, particulieres = EDITIONS[fichier["source_id"]]
    lu = lire_pdf(BASE / fichier["chemin"], set(pages), fins=True)
    cles = {}
    for page, branche in pages.items():
        # Un tableau qui s'étend sur deux pages garde ses libellés d'une page à l'autre.
        yield from lignes_du_tableau(fichier, page, branche, particulieres.get(page, colonnes), lu[page - 1],
                                     fonctions, cles.setdefault(branche, set()), pages.get(page - 1) == branche)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    if RACINE not in fonctions:
        sys.exit(f"fonction {RACINE} absente de tables/fonctions.csv")
    perimetres = {p["id"] for p in lire("tables/perimetres.csv")}
    if set(BRANCHES.values()) - perimetres:
        sys.exit(f"périmètres absents de tables/perimetres.csv : {sorted(set(BRANCHES.values()) - perimetres)}")
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
