"""Fonctions partagées par les outils de la base : chemins, lecture et écriture des tables, empreintes."""

import csv
import datetime
import hashlib
import html
import json
import math
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser

RACINE = pathlib.Path(__file__).resolve().parent.parent
BASE = RACINE / "base"
PAQUET = BASE / "datapackage.json"
SCHEMA_CHIFFRES = "schemas/chiffres.json"

# Certains serveurs (dont celui de l'OCDE) refusent l'agent par défaut de Python.
AGENT = "comptes-nationaux (+https://github.com/g-pliberal/comptes-nationaux)"

# Composantes de l'identifiant d'un chiffre, dans l'ordre. Une composante vide s'écrit « - ».
COMPOSANTES_ID = ["source_id", "zone", "perimetre_id", "concept_id", "fonction_id", "traitements",
                  "unite_id", "periode", "version"]


def empreinte(chemin):
    return hashlib.sha256(pathlib.Path(chemin).read_bytes()).hexdigest()


def maintenant():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def aujourdhui():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def identifiant(ligne):
    return ":".join(ligne.get(c) or "-" for c in COMPOSANTES_ID)


def paquet():
    """Le paquet de données : liste des tables, avec le schéma de chacune."""
    description = json.loads(PAQUET.read_text(encoding="utf-8"))
    for ressource in description["resources"]:
        ressource["schema_chemin"] = ressource["schema"]
        ressource["schema"] = json.loads((BASE / ressource["schema"]).read_text(encoding="utf-8"))
    return description


def champs(nom):
    return [c["name"] for c in ressource(nom)["schema"]["fields"]]


def ressources_chiffres():
    """Les tables de chiffres : une par source, toutes au même schéma."""
    return [r for r in paquet()["resources"] if r["schema_chemin"] == SCHEMA_CHIFFRES]


def champs_chiffres():
    return [c["name"] for c in json.loads((BASE / SCHEMA_CHIFFRES).read_text(encoding="utf-8"))["fields"]]


def table_des_chiffres(source_id):
    """Chemin de la table des chiffres d'une source (« insee.t3201 » → tables/chiffres/insee/t3201.csv),
    déclarée dans le paquet de données à sa première écriture."""
    producteur, nom = source_id.split(".", 1)
    chemin = f"tables/chiffres/{producteur}/{nom}.csv"
    description = json.loads(PAQUET.read_text(encoding="utf-8"))
    if not any(r["path"] == chemin for r in description["resources"]):
        description["resources"].append({"name": f"chiffres-{producteur}-{nom}", "path": chemin, "schema": SCHEMA_CHIFFRES})
        ecrire_paquet(description)
    return chemin


def ecrire_paquet(description):
    """Réécrit datapackage.json, une table par ligne : les tables de référence, celles des chiffres par ordre
    alphabétique, puis le journal des corrections."""
    def rang(element):
        i, r = element
        if r["schema"] == SCHEMA_CHIFFRES:
            return 1, r["name"]
        return (2 if r["name"] == "corrections" else 0), f"{i:04d}"
    ressources = [r for _, r in sorted(enumerate(description["resources"]), key=rang)]
    entete = json.dumps({k: v for k, v in description.items() if k != "resources"}, ensure_ascii=False, indent=2)
    texte = (entete[:-2] + ',\n  "resources": [\n' + ",\n".join("    " + json.dumps(r, ensure_ascii=False) for r in ressources)
             + "\n  ]\n}\n")
    PAQUET.write_text(texte, encoding="utf-8")


def ressource(nom):
    return next(r for r in paquet()["resources"] if r["name"] == nom)


def lire(chemin):
    chemin = BASE / chemin if not pathlib.Path(chemin).is_absolute() else pathlib.Path(chemin)
    if not chemin.exists():
        return []
    with chemin.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ecrire(chemin, champs, lignes, cle="id"):
    """Écrit une table triée par sa clé, pour que les différences d'une version à l'autre restent lisibles."""
    chemin = BASE / chemin
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=champs, lineterminator="\n")
        ecrivain.writeheader()
        ecrivain.writerows(sorted(lignes, key=lambda l: l[cle]))


def lire_jsonstat(chemin):
    """Renvoie (dimensions, {tuple de codes: (valeur, drapeau)}, date de mise à jour) d'un fichier JSON-stat 2.0."""
    jeu = json.loads(pathlib.Path(chemin).read_text(encoding="utf-8"))
    dims, tailles = jeu["id"], jeu["size"]
    codes = {d: {pos: code for code, pos in jeu["dimension"][d]["category"]["index"].items()} for d in dims}
    drapeaux = jeu.get("status", {})
    valeurs = {}
    for position, valeur in jeu["value"].items():
        n, cle = int(position), []
        for d, taille in zip(reversed(dims), reversed(tailles)):
            cle.append(codes[d][n % taille])
            n //= taille
        valeurs[tuple(reversed(cle))] = (valeur, drapeaux.get(position, ""))
    return dims, valeurs, jeu.get("updated", "")


# --- Fichiers Excel (xlsx), lus sans bibliothèque extérieure ---------------------------------------

_XLSX = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
         "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
         "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
         "dcterms": "http://purl.org/dc/terms/"}


def _textes(element):
    return "".join(t.text or "" for t in element.iter(f"{{{_XLSX['m']}}}t"))


def lire_xlsx(chemin, feuille=None):
    """Renvoie (nom de la feuille, {référence de cellule: valeur}) pour une feuille d'un classeur xlsx.

    Les valeurs sont celles enregistrées dans le fichier : nombres en float, textes en str."""
    with zipfile.ZipFile(chemin) as classeur:
        partagees = []
        if "xl/sharedStrings.xml" in classeur.namelist():
            partagees = [_textes(si) for si in ET.fromstring(classeur.read("xl/sharedStrings.xml"))
                         .findall("m:si", _XLSX)]
        cibles = {lien.get("Id"): lien.get("Target")
                  for lien in ET.fromstring(classeur.read("xl/_rels/workbook.xml.rels"))}
        feuilles = {f.get("name"): cibles[f.get(f"{{{_XLSX['r']}}}id")]
                    for f in ET.fromstring(classeur.read("xl/workbook.xml")).find("m:sheets", _XLSX)}
        nom = feuille or next(iter(feuilles))
        cible = feuilles[nom]
        xml_feuille = classeur.read(cible.lstrip("/") if cible.startswith("/") else f"xl/{cible}")
    cellules = {}
    for c in ET.fromstring(xml_feuille).iter(f"{{{_XLSX['m']}}}c"):
        type_, v = c.get("t"), c.find("m:v", _XLSX)
        if type_ == "inlineStr":
            cellules[c.get("r")] = _textes(c)
        elif v is None or v.text is None:
            continue
        elif type_ == "s":
            cellules[c.get("r")] = partagees[int(v.text)]
        elif type_ in ("str", "e", "b"):
            cellules[c.get("r")] = v.text
        else:
            cellules[c.get("r")] = float(v.text)
    return nom, cellules


def feuilles_xlsx(chemin):
    with zipfile.ZipFile(chemin) as classeur:
        return [f.get("name") for f in ET.fromstring(classeur.read("xl/workbook.xml")).find("m:sheets", _XLSX)]


def date_xlsx(chemin):
    """Date de dernière modification inscrite par le producteur dans les propriétés du classeur, à défaut
    date de création (les classeurs générés par programme n'ont souvent que celle-ci)."""
    with zipfile.ZipFile(chemin) as classeur:
        proprietes = ET.fromstring(classeur.read("docProps/core.xml"))
    for propriete in ("dcterms:modified", "dcterms:created"):
        date = proprietes.find(propriete, _XLSX)
        if date is not None and date.text:
            return date.text
    return ""


def position(reference):
    """« BQ7 » → (7, « BQ »)."""
    lettres, chiffres = re.fullmatch(r"([A-Z]+)([0-9]+)", reference).groups()
    return int(chiffres), lettres


def nombre(valeur):
    """Texte d'un nombre lu dans un fichier, débarrassé des artefacts de la virgule flottante, et ses décimales."""
    texte = repr(round(float(valeur), 9))
    texte = texte[:-2] if texte.endswith(".0") else texte
    return texte, len(texte.split(".")[1]) if "." in texte else 0


# --- Pages HTML (textes de loi publiés par le Sénat) et séries SDMX de l'Insee ---------------------------

_SANS_FIN = {"br", "img", "hr", "col", "input", "meta", "link", "wbr"}
_BLOCS = {"p", "br", "div", "td", "th", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6"}  # séparent les mots


def _graisse(balise, attributs):
    """True si la balise met son texte en gras, False si elle l'annule, None si elle hérite de son parent."""
    poids = re.search(r"font-weight:(\w+)", re.sub(r"\s+", "", (attributs.get("style") or "").lower()))
    if poids:
        return poids.group(1) in ("bold", "bolder", "600", "700", "800", "900")
    return True if balise in ("b", "strong", "th") else None


class _Tableaux(HTMLParser):
    """Les tableaux d'une page, numérotés dans l'ordre où ils s'ouvrent ; un tableau imbriqué a son propre numéro.
    Chaque cellule garde ses paragraphes, sa hauteur (rowspan), sa largeur (colspan), et si tout son texte est en
    gras. Chaque tableau garde aussi sa légende : le paragraphe, hors tableau, qui le précède immédiatement. Le flux
    est le texte de la page dans l'ordre de lecture, cellules comprises, où « ⟦k⟧ » marque l'ouverture du tableau k
    et « ⟦/k⟧ » sa fermeture."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tableaux, self.ouverts, self.cellule, self.balises = [], [], None, []
        self.legendes, self.libre, self.dernier_libre = [], [], ""
        self.flux, self.numeros = [], []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): v for k, v in attrs}
        if tag in _BLOCS:
            self.flux.append(" ")
        if tag == "p" and self.cellule is None:
            self.libre = []
        if tag == "table":
            self.flux.append(f" ⟦{len(self.tableaux)}⟧ ")
            self.numeros.append(len(self.tableaux))
            self.ouverts.append([])
            self.tableaux.append(self.ouverts[-1])
            self.legendes.append(self.dernier_libre)
            self.dernier_libre = ""
        elif tag == "tr" and self.ouverts:
            self.ouverts[-1].append([])
        elif tag in ("td", "th") and self.ouverts:
            self.cellule = {"paragraphes": [[]], "hauteur": int(a.get("rowspan") or 1), "largeur": int(a.get("colspan") or 1),
                            "gras": []}
            self.balises = [(tag, bool(_graisse(tag, a)))]
        elif self.cellule is not None and tag not in _SANS_FIN:
            graisse = _graisse(tag, a)
            self.balises.append((tag, self.balises[-1][1] if graisse is None else graisse))
        if tag in ("p", "br") and self.cellule is not None:
            self.cellule["paragraphes"].append([])

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cellule is not None and self.ouverts:
            if not self.ouverts[-1]:
                self.ouverts[-1].append([])
            paragraphes = [" ".join("".join(p).split()) for p in self.cellule["paragraphes"]]
            self.cellule["paragraphes"] = [p for p in paragraphes if p] if self.cellule["hauteur"] == 1 else \
                [p for i, p in enumerate(paragraphes) if p or i > 0]
            self.cellule["gras"] = bool(self.cellule["gras"]) and all(self.cellule["gras"])
            self.ouverts[-1][-1].append(self.cellule)
            self.cellule = None
        elif tag == "table" and self.ouverts:
            self.ouverts.pop()
            self.flux.append(f" ⟦/{self.numeros.pop()}⟧ ")
        elif tag == "p" and self.cellule is None:
            self.dernier_libre = " ".join("".join(self.libre).split()) or self.dernier_libre
        elif self.cellule is not None and tag not in _SANS_FIN:
            ouverte = next((k for k in range(len(self.balises) - 1, 0, -1) if self.balises[k][0] == tag), None)
            if ouverte is not None:
                del self.balises[ouverte:]
        if tag in _BLOCS:
            self.flux.append(" ")

    def handle_data(self, data):
        self.flux.append(data)
        if self.cellule is None:
            self.libre.append(data)
        else:
            self.cellule["paragraphes"][-1].append(data)
            if data.strip():
                self.cellule["gras"].append(self.balises[-1][1])


def _grille(lignes):
    """Place les cellules d'un tableau sur sa grille, fusions comprises. Une cellule fusionnée sur n lignes qui
    contient n paragraphes donne un paragraphe à chacune de ces lignes ; sinon, son texte va à sa case de départ,
    et la cellule est notée parmi les fusions : {(ligne, colonne) de départ : nombre de lignes}. Le texte d'une cellule
    fusionnée sur plusieurs colonnes va à la première. Renvoie la grille et sa mise en forme : ces fusions, les
    largeurs des cellules qui couvrent plusieurs colonnes ({(ligne, colonne) : nombre de colonnes}, pour chaque case
    qui reçoit leur texte), et l'ensemble des cases dont le texte est en gras ; lire_tableaux_html y ajoute la légende
    du tableau."""
    grille, occupees, fusions, largeurs, gras = {}, set(), {}, {}, set()
    for r, ligne in enumerate(lignes):
        c = 0
        for cellule in ligne:
            while (r, c) in occupees:
                c += 1
            h, l, paragraphes = cellule["hauteur"], cellule["largeur"], cellule["paragraphes"]
            for dr in range(h):
                for dc in range(l):
                    occupees.add((r + dr, c + dc))
            cases = range(h) if h > 1 and len(paragraphes) == h else range(1)
            if h > 1 and len(paragraphes) == h:
                for dr, texte in enumerate(paragraphes):
                    grille[(r + dr, c)] = texte
            else:
                grille[(r, c)] = " ".join(paragraphes)
                if h > 1:
                    fusions[(r, c)] = h
            if l > 1:
                largeurs.update(((r + dr, c), l) for dr in cases)
            if cellule["gras"]:
                gras.update((r + dr, c) for dr in cases)
            c += l
    largeur = max((c for _, c in occupees), default=-1) + 1
    hauteur = max((r for r, _ in occupees), default=-1) + 1
    return [[grille.get((r, c), "") for c in range(largeur)] for r in range(max(hauteur, len(lignes)))], \
        {"fusions": fusions, "largeurs": largeurs, "gras": gras}


def lire_page_html(chemin):
    """Tableaux d'une page HTML, chacun sous forme de grille (liste de lignes, chacune liste des textes de ses
    colonnes), la mise en forme de chaque tableau (voir _grille) et le texte de la page dans l'ordre de lecture, où
    « ⟦k⟧ » marque l'ouverture du tableau k et « ⟦/k⟧ » sa fermeture."""
    lecteur = _Tableaux()
    lecteur.feed(pathlib.Path(chemin).read_text(encoding="utf-8"))
    lus = [_grille(t) for t in lecteur.tableaux]
    return [g for g, _ in lus], [{**f, "legende": l} for (_, f), l in zip(lus, lecteur.legendes)], \
        " ".join("".join(lecteur.flux).split())


def lire_tableaux_html(chemin, mise_en_forme=False):
    """Tableaux d'une page HTML, chacun sous forme de grille : liste de lignes, chacune liste des textes de ses
    colonnes. Avec mise_en_forme=True, renvoie aussi la mise en forme de chaque tableau (voir _grille)."""
    grilles, formes, _ = lire_page_html(chemin)
    return (grilles, formes) if mise_en_forme else grilles


def texte_html(contenu):
    """Le texte d'une page HTML, sans balises ni entités."""
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", contenu)).split())


def nombre_texte(texte):
    """« -3 377 967 838,47 » → (« -3377967838.47 », 2) ; None si le texte n'est pas un nombre. Un appel de note,
    astérisque avant ou après le nombre ou numéro entre parenthèses après lui (« 164,0 (1) »), n'en fait pas
    partie, ni le signe + d'un nombre positif, ni le signe % d'un pourcentage (« 26,7 % » → 26,7)."""
    t = re.sub(r"[\s\u00a0\u202f]", "", texte).replace("−", "-").replace("–", "-").replace(",", ".")
    t = re.sub(r"^\(?\*\)?|\(?\*\)?$|(?<=[0-9])\([0-9]\)$|(?<=[0-9])%$", "", t)
    if not re.fullmatch(r"[-+]?[0-9]+(\.[0-9]+)?", t):
        return None
    t = t.lstrip("+")
    return t, len(t.split(".")[1]) if "." in t else 0


def nombre_de_phrase(phrase):
    """Le montant qu'énonce une phrase d'un texte (« …, s'élevant à 2,2 milliards d'euros ») : son seul nombre, lu
    comme par nombre_texte, ou zéro si elle le dit nul (« …, lesquelles sont nulles ») ; None sinon."""
    if re.search(r"\bnul(?:le)?s?$", phrase):
        return None if re.search(r"[0-9]", phrase) else ("0", 0)
    nombres = re.findall(r"[0-9]+(?:,[0-9]+)?", phrase)
    return nombre_texte(nombres[0]) if len(nombres) == 1 else None


MOIS = {m: i for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
                                     "octobre", "novembre", "décembre"], start=1)}


def date_html(texte):
    """Date qu'un texte publié par le Sénat porte lui-même : enregistrement, transmission ou adoption ; à défaut,
    celle de la séance au procès-verbal de laquelle il est annexé, ou celle qui suit la session dans l'en-tête d'un
    texte adopté par le Sénat."""
    date = r"([0-9]{1,2})(?:er)? (" + "|".join(MOIS) + r") ([0-9]{4})"
    for annonce in (r"(?:Enregistré à la Présidence du Sénat|transmis au Sénat|adopté (?:définitivement )?par le Sénat) le ",
                    r"Annexe au procès-verbal de la séance du ", r"SESSION (?:ORDINAIRE|EXTRAORDINAIRE) DE [0-9]{4}-[0-9]{4} "):
        trouve = re.search(annonce + date, texte)
        if trouve:
            jour, mois, annee = trouve.groups()
            return f"{annee}-{MOIS[mois]:02d}-{int(jour):02d}"
    return ""


def lire_sdmx(chemin):
    """Série SDMX 2.1 de l'Insee (StructureSpecificData) : {idbank: (attributs de la série, {période: attributs de
    l'observation})}."""
    series = {}
    for serie in ET.parse(chemin).getroot().iter():
        if serie.tag.split("}")[-1] == "Series":
            observations = {o.get("TIME_PERIOD"): dict(o.attrib) for o in serie if o.tag.split("}")[-1] == "Obs"}
            series[serie.get("IDBANK")] = (dict(serie.attrib), observations)
    return series


# --- Fusion des chiffres importés ----------------------------------------------------------------------

def meme_valeur(a, b):
    return (math.isclose(float(a["valeur"]), float(b["valeur"]), rel_tol=1e-12, abs_tol=1e-9)
            and a["statut"] == b["statut"])


def fusionner(existants, nouveaux, origine):
    """Ajoute à `existants` (identifiant → ligne) les chiffres nouveaux d'une copie archivée.

    Une valeur déjà enregistrée à l'identique est ignorée, de même qu'une valeur qu'une version plus
    récente de la source reprend sans changement : seule la version où elle apparaît est enregistrée. La
    comparaison se fait avec la version qui précède, pour qu'importer de nouveau un fichier n'ajoute rien.
    Deux valeurs différentes pour un même identifiant arrêtent l'import.
    Renvoie (nombre de chiffres ajoutés, nombre de chiffres inchangés)."""
    cle = lambda l: tuple(l[c] for c in COMPOSANTES_ID[:-1])
    versions = {}  # clé sans la version → lignes enregistrées
    for l in existants.values():
        versions.setdefault(cle(l), []).append(l)
    ajoutes, inchanges, conflits = 0, 0, []
    for l in nouveaux:
        ancien = existants.get(l["id"])
        if ancien is not None:
            if meme_valeur(ancien, l):
                inchanges += 1
            else:
                conflits.append(f"{l['id']} : {ancien['valeur']} ({ancien['statut']}) déjà enregistré, "
                                f"{l['valeur']} ({l['statut']}) dans {origine}")
            continue
        anterieures = [v for v in versions.get(cle(l), []) if v["version"] < l["version"]]
        precedent = max(anterieures, key=lambda v: v["version"]) if anterieures else None
        if precedent is not None and meme_valeur(precedent, l):
            inchanges += 1
            continue
        existants[l["id"]] = l
        versions.setdefault(cle(l), []).append(l)
        ajoutes += 1
    if conflits:
        sys.exit("Import interrompu, valeurs contradictoires pour une même version :\n" + "\n".join(conflits))
    return ajoutes, inchanges
