#!/usr/bin/env python3
"""Inscrit dans la base les fichiers de recensement des éléments d'imposition à la fiscalité directe locale (REI) que
publie la DGFiP, à partir de leurs copies archivées.

    python3 outils/importer_rei.py <fichier_id>

Chaque année d'imposition est une archive zip : le fichier lui-même, une ligne par commune et une colonne par variable,
sa notice et son tracé, qui donne le code, le titre et le format de chaque variable (pour les impositions de 2012 à
2016, le tracé est une feuille du classeur). Le fichier est un classeur xlsx jusqu'aux impositions de 2022, un fichier
csv depuis. Son en-tête porte les codes des variables, dans l'ordre du tracé ou non (2013) ; certaines années, il porte
leurs titres, dans l'ordre du tracé, que le fichier reformule parfois : il s'associe alors au tracé rang par rang, si au
moins 80 % de ses titres sont ceux du tracé. L'import lit le tracé, puis le fichier en flux, sans le charger, vérifie
l'en-tête et que chaque ligne désigne une commune et une seule, et compte les valeurs d'une variable numérique qui ne
sont pas des nombres (« , » en 2012, « . » de 2013 à 2015, les marques d'une valeur manquante), que la base lit comme
vides. Dans le fichier de 2012, l'export a fondu deux champs en un sur les lignes des communes de Franche-Comté,
décalant d'un rang les champs suivants : ces lignes sont rétablies, et le code de la commune qui les termine alors le
confirme. L'import inscrit la copie dans tables/fichiers_rei.csv, avec l'exercice, la version, le nombre de communes,
celui des variables, celui des titres de l'en-tête différents du tracé, celui des valeurs illisibles et celui des lignes
rétablies. La version est la date la plus récente des fichiers que porte l'archive. Ces copies sont les chiffres
eux-mêmes : la base ne les recopie pas, elle les lit.
"""

import collections
import csv
import functools
import io
import re
import sys
import unicodedata
import zipfile

from commun import BASE, champs, ecrire, feuilles_xlsx, lignes_xlsx, lire, lire_xlsx, ouvrir_copie, texte_xlsx

SOURCE = "dgfip.rei"
DONNEES = re.compile(r"(?:.*/)?REI(?:_COMPLET)?_([0-9]{4})(?:_V[0-9]+)?\.(csv|xlsx)", re.I)
TRACE = re.compile(r"(?:.*/)?TRACE_REI(?:_COMPLET)?_([0-9]{4})(?:_V[0-9]+)?\.xlsx", re.I)
FEUILLE_TRACE = re.compile(r"variables_([0-9]{4})", re.I)
# Les colonnes du tracé, sous leurs noms d'une année à l'autre (« NOM_DE_LA_VARIABLE », « NOM DE VARIABLE », « NOM »…).
COLONNES_TRACE = {"code": r"NOM(_(DE_)?(LA_)?VARIABLE)?", "titre": r"TITRE|LIBELLE(_DE_(LA_)?VARIABLE)?",
                  "format": r"FORMAT"}
COMMUNE = r"[0-9][0-9AB][0-9]{3}"  # code de la commune, formé du département et du numéro
# Un en-tête qui porte les titres des variables plutôt que leurs codes s'associe au tracé rang par rang, s'il en a autant
# de colonnes et qu'au moins cette part de ses titres sont ceux du tracé : un fichier peut reformuler un titre.
SEUIL_TITRES = 0.8
NOMBRE = re.compile(r"-?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?")
# La fiche de chaque commune : colonne de la table communes_rei → variable du REI. Un classeur donne parfois en nombres
# les codes du département, de la région et du groupement, qui perdent alors leurs zéros de tête : ils sont complétés
# jusqu'à leur longueur.
FICHE = {"nom": "LIBCOM", "departement": "DEP", "region": "REG", "groupement": "Q02", "nom_groupement": "Q03",
         "siren_groupement": "SIREPCI", "regime_groupement": "OPTEPCI", "forme_groupement": "FORJEPCI",
         "teom_niveau": "F71", "teom_beneficiaire": "TEOMBENEF"}
LONGUEURS = {"DEP": 2, "REG": 2, "Q02": 6}
GRANDEURS = ["base", "taux_net", "taux_vote", "produit"]
ADDITIVES = {"base", "produit"}  # les grandeurs que plusieurs variables peuvent donner ensemble, par leur somme
# Ce que doit dire le titre au tracé d'une variable que le référentiel retient, selon la grandeur qu'elle donne.
TITRES_GRANDEURS = {"base": r"\bBASES?\b|VALEUR LOCATIVE", "taux_net": r"\bTAUX\b", "taux_vote": r"\bTAUX VOTE",
                    "produit": r"MONTANT|PRODUIT|COTISATION|DROIT FIXE|TASCOM|CVAE|FONDS|PRELEVEMENT|FRAIS"}
# Une variable dont le montant est celui d'une collectivité, répété sur chacune de ses communes, ne doit pas être
# retenue : on la reconnaît à ce qu'elle donne un même montant non nul à toutes les communes de presque chaque
# département, ou de presque chaque groupement (cette part au moins de ceux de plusieurs communes, et ceux-ci au moins
# au nombre de GROUPES_REPETITION) ; la part de CVAE des chambres de commerce et d'industrie régionales, que le REI
# donne jusqu'en 2018, est ainsi le montant de la chambre, sauf dans un département partagé entre deux chambres.
PART_REPETITION = 0.9
GROUPES_REPETITION = 3


def normaliser(texte):
    """Un titre sans accents, en capitales, ses blancs réduits : les en-têtes et les tracés l'écrivent diversement."""
    sans_accents = "".join(c for c in unicodedata.normalize("NFKD", str(texte)) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sans_accents).strip().upper()


def membres(archive, fichier):
    """(exercice, membre du fichier, son format, membre du tracé ou None si le tracé est une feuille du classeur)."""
    donnees = [(m.group(1), n, m.group(2).lower()) for n in archive.namelist() if (m := DONNEES.fullmatch(n))]
    traces = [n for n in archive.namelist() if TRACE.fullmatch(n)]
    if len(donnees) != 1 or len(traces) > 1:
        sys.exit(f"{fichier['id']} : l'archive porte {len(donnees)} fichiers de données et {len(traces)} tracés")
    exercice, nom, format_ = donnees[0]
    if traces and TRACE.fullmatch(traces[0]).group(1) != exercice:
        sys.exit(f"{fichier['id']} : le tracé n'est pas celui de {exercice}")
    return exercice, nom, format_, (traces[0] if traces else None)


def lignes_feuille(cellules):
    """Les lignes d'une feuille lue par lire_xlsx : [{colonne: valeur}], dans l'ordre, les caractères échappés d'un
    texte (« _x0020_ ») rétablis."""
    lignes = collections.defaultdict(dict)
    for ref, v in cellules.items():
        m = re.fullmatch(r"([A-Z]+)([0-9]+)", ref)
        lignes[int(m.group(2))][m.group(1)] = texte_xlsx(v) if isinstance(v, str) else v
    return [lignes[n] for n in sorted(lignes)]


def lire_trace(feuille, lieu):
    """[(code, titre, format)] d'un tracé, dans l'ordre de ses lignes."""
    entete, *lignes = lignes_feuille(feuille)
    colonnes = {}
    for nom, motif in COLONNES_TRACE.items():
        trouvees = [c for c, v in entete.items() if re.fullmatch(motif, normaliser(v).replace(" ", "_"))]
        if len(trouvees) != 1:
            sys.exit(f"{lieu} : colonne « {nom} » du tracé introuvable ({sorted(map(str, entete.values()))})")
        colonnes[nom] = trouvees[0]
    trace = [tuple(str(l.get(colonnes[k], "")).strip() for k in ("code", "titre", "format")) for l in lignes
             if str(l.get(colonnes["code"], "")).strip()]
    codes = [c for c, _, _ in trace]
    if len(set(codes)) != len(codes):
        sys.exit(f"{lieu} : le tracé donne deux fois un même code de variable")
    return trace


@functools.cache
def indice(colonne):
    """Le rang (0 pour A) d'une colonne de classeur."""
    n = 0
    for lettre in colonne:
        n = 26 * n + ord(lettre) - 64
    return n - 1


def contenu(fichier):
    """(exercice, variables [(code, titre, titre du tracé, format)] dans l'ordre des colonnes, titres de l'en-tête
    différents de ceux du tracé, lignes) d'une copie archivée : le titre d'une variable est celui de l'en-tête du fichier
    quand il porte les titres, sinon celui du tracé ; les lignes, lues en flux, sont des listes de textes dans l'ordre
    des colonnes, l'en-tête retiré."""
    archive = zipfile.ZipFile(ouvrir_copie(BASE / fichier["chemin"]))
    exercice, nom, format_, nom_trace = membres(archive, fichier)
    octets = archive.read(nom) if format_ == "xlsx" else None
    classeur = zipfile.ZipFile(io.BytesIO(octets)) if octets else None
    noms = feuilles_xlsx(io.BytesIO(octets)) if octets else []
    if nom_trace:
        _, feuille = lire_xlsx(io.BytesIO(archive.read(nom_trace)))
    else:
        if len([n for n in noms if FEUILLE_TRACE.fullmatch(n)]) != 1:
            sys.exit(f"{fichier['id']} : ni tracé, ni feuille du tracé dans le classeur")
        _, feuille = lire_xlsx(io.BytesIO(octets), next(n for n in noms if FEUILLE_TRACE.fullmatch(n)))
    trace = lire_trace(feuille, fichier["id"])

    def rangees():
        if classeur is None:
            with archive.open(nom) as f:
                yield from csv.reader(io.TextIOWrapper(f, encoding="cp1252", newline=""), delimiter=";")
            return
        donnees = [n for n in noms if not FEUILLE_TRACE.fullmatch(n)]
        if len(donnees) != 1:
            sys.exit(f"{fichier['id']} : le classeur porte {len(donnees)} feuilles de données")
        largeur = len(trace)
        for valeurs in lignes_xlsx(classeur, donnees[0]):
            ligne = [""] * largeur
            for c, v in valeurs.items():
                k = indice(c)
                if k >= len(ligne):
                    ligne += [""] * (k + 1 - len(ligne))
                ligne[k] = v
            yield ligne

    lecteur = rangees()
    entete = [str(e).strip() for e in next(lecteur, [])]
    while entete and not entete[-1]:
        entete.pop()
    if sorted(entete) == sorted(c for c, _, _ in trace):
        par_code = {c: (c, t, t, f) for c, t, f in trace}
        return exercice, [par_code[c] for c in entete], 0, lecteur
    egaux = sum(normaliser(e) == normaliser(t) for e, (_, t, _) in zip(entete, trace))
    if len(entete) != len(trace) or egaux < SEUIL_TITRES * len(trace):
        sys.exit(f"{fichier['id']} : l'en-tête du fichier ({len(entete)} colonnes) n'est ni les codes ni les titres du "
                 f"tracé ({len(trace)} variables, {egaux} titres identiques)")
    return exercice, [(c, e, t, f) for e, (c, t, f) in zip(entete, trace)], len(trace) - egaux, lecteur


def complete(variable, texte):
    """Un code que le fichier peut donner en nombre, complété de ses zéros de tête (« 1 » pour le département 01)."""
    texte = texte.strip()
    return texte.zfill(LONGUEURS[variable]) if texte.isdigit() and variable in LONGUEURS else texte


def commune(valeurs, lieu):
    """Le code de la commune d'une ligne {code de variable: texte} : le département et le numéro de la commune,
    complétés de leurs zéros (un classeur les donne parfois en nombres, « 1 » et « 1 » pour 01001) ; trois chiffres
    pour la commune, deux dans les départements d'outre-mer, dont le code en a trois. Le code concaténé que donne le
    fichier (IDCOM), quand il a ses cinq caractères, doit être le même."""
    departement, numero = complete("DEP", valeurs["DEP"]), valeurs["COM"].strip()
    code = departement + numero.zfill(2 if len(departement) == 3 else 3)
    if not re.fullmatch(COMMUNE, code):
        sys.exit(f"{lieu} : commune illisible « {code} »")
    concatene = valeurs.get("IDCOM", "").strip()
    if len(concatene) == 5 and concatene != code:
        sys.exit(f"{lieu} : le fichier donne le code {concatene} à la commune {code}")
    return code


def realignee(ligne, codes, lieu):
    """La ligne rétablie, ou None, si l'export du fichier y a fondu deux champs en un : un texte porte un point-virgule,
    le dernier champ, le code concaténé de la commune (IDCOM), est vide, et tous les champs qui suivent le texte fondu
    sont décalés d'un rang (le REI de 2012, dans les communes de Franche-Comté, où « CRCI Franche-Comt・;25056" »
    occupe le champ du libellé de la chambre de commerce régionale). Le texte est coupé au point-virgule, ses deux
    parties sans leurs guillemets ; l'appelant vérifie que le code concaténé est alors celui de la commune."""
    if not codes or codes[-1] != "IDCOM" or ligne[len(codes) - 1].strip():
        return None
    fondus = [k for k, v in enumerate(ligne[:len(codes)]) if ";" in v]
    if len(fondus) > 1:
        sys.exit(f"{lieu} : plusieurs champs portent un point-virgule")
    if not fondus:
        return None
    k = fondus[0]
    avant, _, apres = ligne[k].partition(";")
    return ligne[:k] + [avant.strip('"'), apres.strip('"')] + ligne[k + 1:len(codes) - 1]


def lignes_communes(fichier, illisibles=None, realignees=None):
    """(exercice, variables, titres différents, lignes) d'une copie, chaque ligne étant (code de la commune, {code de
    variable: texte}) ; vérifie qu'une commune n'a qu'une ligne. Une variable numérique qui n'est pas un nombre est
    comptée dans `illisibles` (Counter : (variable, texte) → nombre) et vaut alors vide ; une ligne dont l'export a
    fondu deux champs est rétablie, et son code de commune ajouté à `realignees`."""
    exercice, variables, differents, lecteur = contenu(fichier)
    illisibles = collections.Counter() if illisibles is None else illisibles
    realignees = [] if realignees is None else realignees
    codes = [c for c, _, _, _ in variables]
    numeriques = {c for c, _, _, f in variables if not f.startswith("$")}

    def lignes():
        vues = set()
        for n, ligne in enumerate(lecteur, start=2):
            lieu = f"{fichier['id']}, ligne {n}"
            if not any(v.strip() for v in ligne):
                continue
            if len(ligne) < len(codes) or any(v.strip() for v in ligne[len(codes):]):
                sys.exit(f"{lieu} : {len(ligne)} champs au lieu de {len(codes)}")
            retablie = realignee(ligne, codes, lieu)
            valeurs = dict(zip(codes, ligne if retablie is None else retablie))
            code = commune(valeurs, lieu)
            if retablie is not None:
                if valeurs["IDCOM"].strip() != code:
                    sys.exit(f"{lieu} : la ligne rétablie ne finit pas par le code de la commune {code}")
                realignees.append(code)
            if code in vues:
                sys.exit(f"{lieu} : deuxième ligne pour la commune {code}")
            vues.add(code)
            for c in numeriques:
                v = valeurs[c].strip()
                if v and not v.isdigit() and not NOMBRE.fullmatch(v):
                    illisibles[(c, v)] += 1
                    valeurs[c] = ""
            yield code, valeurs

    return exercice, variables, differents, lignes()


def fiche(valeurs):
    """La fiche d'une commune : {colonne de la table communes_rei: texte}, vide pour une variable que l'année n'a pas."""
    return {colonne: complete(variable, valeurs.get(variable, "")) for colonne, variable in FICHE.items()}


def postes(exercice, variables, referentiel, lieu):
    """Les impositions qu'une année du REI permet de lire, d'après le référentiel (tables/variables_rei.csv) :
    {(taxe, destinataire): {grandeur: [codes de variables]}}. Chaque variable doit figurer au tracé de l'année, et
    seules la base et le produit peuvent être donnés par plusieurs variables, qui s'additionnent."""
    titres = {c: titre for c, _, titre, _ in variables}
    resultat = collections.defaultdict(lambda: collections.defaultdict(list))
    for v in referentiel:
        if not v["premier_exercice"] <= exercice <= v["dernier_exercice"]:
            continue
        if v["code"] not in titres:
            sys.exit(f"{lieu} : la variable {v['code']} ({v['taxe']}, {v['destinataire']}, {v['grandeur']}) n'est pas "
                     f"au tracé de {exercice}")
        if not re.search(TITRES_GRANDEURS[v["grandeur"]], normaliser(titres[v["code"]])):
            sys.exit(f"{lieu} : le titre de la variable {v['code']} au tracé de {exercice}, « {titres[v['code']]} », ne "
                     f"dit pas sa grandeur ({v['grandeur']})")
        grandeurs = resultat[(v["taxe"], v["destinataire"])]
        if grandeurs[v["grandeur"]] and v["grandeur"] not in ADDITIVES:
            sys.exit(f"{lieu} : plusieurs variables donnent le {v['grandeur']} de {v['taxe']}, {v['destinataire']}")
        grandeurs[v["grandeur"]].append(v["code"])
    return resultat


def marge(texte):
    """La demi-unité de la dernière décimale d'une valeur écrite, ses chiffres de calcul en virgule flottante ignorés
    (un classeur écrit « 26.370000000000001 » pour 26,37) ; une valeur nulle est exacte."""
    x = float(texte)
    if x == 0:
        return 0.0
    decimales = next((d for d in range(7) if round(x, d) == x), 7)
    return 0.5 * 10 ** -decimales


def impositions(valeurs, postes_, marges=False):
    """Les impositions d'une commune : [(taxe, destinataire, base, taux net, taux voté, produit)], une grandeur que le
    fichier laisse vide valant None, et, si `marges`, la marge d'arrondi de chacune des quatre à la suite (celle d'une
    somme étant la somme des leurs) ; une imposition sans base ni produit non nuls n'est pas retenue."""
    resultat = []
    for (taxe, destinataire), grandeurs in postes_.items():
        ligne, ecarts = [], []
        for g in GRANDEURS:
            textes = [t for t in (valeurs[c].strip() for c in grandeurs.get(g, [])) if t]
            ligne.append(sum(float(t) for t in textes) if textes else None)
            ecarts.append(sum(marge(t) for t in textes) if textes else None)
        if ligne[0] or ligne[3]:
            resultat.append((taxe, destinataire, *ligne) + (tuple(ecarts) if marges else ()))
    return resultat


def repetees(montants):
    """Les variables dont le montant est celui d'une collectivité répété sur ses communes, d'après `montants` :
    {(variable, (« département » ou « groupement », code)): [montants non nuls de ses communes, nombre de communes]}."""
    groupes = collections.defaultdict(list)
    for (variable, (nature, groupe)), (valeurs, communes) in montants.items():
        if groupe and communes > 1:
            groupes[(variable, nature)].append(len(valeurs) == 1)
    return sorted({v for (v, _), uniques in groupes.items()
                   if len(uniques) >= GROUPES_REPETITION and sum(uniques) >= PART_REPETITION * len(uniques)})


def inscription(fichier):
    """La ligne de tables/fichiers_rei.csv d'une copie, après contrôle de tout son contenu et de ce qu'en retient le
    référentiel (tables/variables_rei.csv)."""
    if fichier["source_id"] != SOURCE:
        sys.exit(f"{fichier['id']} : la source {fichier['source_id']} n'est pas lue par cet import")
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas la date de ses fichiers")
    illisibles, realignees = collections.Counter(), []
    exercice, variables, differents, lignes = lignes_communes(fichier, illisibles, realignees)
    retenues = {c for grandeurs in postes(exercice, variables, lire("tables/variables_rei.csv"), fichier["id"]).values()
                for g, codes in grandeurs.items() if g in ADDITIVES for c in codes}
    montants = collections.defaultdict(lambda: [set(), 0])
    communes = 0
    for _, valeurs in lignes:
        communes += 1
        groupes = [("département", complete("DEP", valeurs["DEP"])),
                   ("groupement", complete("Q02", valeurs.get("Q02", "")))]
        for c in retenues:
            texte = valeurs[c].strip()
            if texte and float(texte):
                for groupe in groupes:
                    entree = montants[(c, groupe)]
                    entree[0].add(texte)
                    entree[1] += 1
    if not communes:
        sys.exit(f"{fichier['id']} : aucune commune")
    if repetes := repetees(montants):
        sys.exit(f"{fichier['id']} : les variables {', '.join(repetes)} donnent un même montant à toutes les communes "
                 "de presque chaque département ou de presque chaque groupement : c'est celui d'une collectivité, qu'il "
                 "ne faut pas retenir commune par commune")
    return {"fichier_id": fichier["id"], "exercice": exercice, "version": version, "communes": str(communes),
            "variables": str(len(variables)), "titres_differents": str(differents),
            "illisibles": str(sum(illisibles.values())), "lignes_realignees": str(len(realignees))}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    inscrits = [i for i in lire("tables/fichiers_rei.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]])
    if any(i["exercice"] == ligne["exercice"] and i["version"] == ligne["version"] for i in inscrits):
        sys.exit(f"{sys.argv[1]} : une copie de {ligne['exercice']} de même version est déjà inscrite")
    ecrire("tables/fichiers_rei.csv", champs("fichiers_rei"), inscrits + [ligne], cle="fichier_id")
    print(f"{ligne['fichier_id']} : impositions de {ligne['exercice']} ({ligne['version']}), {ligne['communes']} communes, "
          f"{ligne['variables']} variables ({ligne['titres_differents']} titres différents du tracé), "
          f"{ligne['illisibles']} valeurs illisibles, {ligne['lignes_realignees']} lignes rétablies")


if __name__ == "__main__":
    main()
