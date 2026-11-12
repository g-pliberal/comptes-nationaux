"""Fonctions partagées par les outils de la base : chemins, lecture et écriture des tables, empreintes."""

import bisect
import bz2
import concurrent.futures
import csv
import datetime
import hashlib
import html
import io
import itertools
import json
import math
import os
import pathlib
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
import zlib
from html.parser import HTMLParser

RACINE = pathlib.Path(__file__).resolve().parent.parent
BASE = RACINE / "base"
PAQUET = BASE / "datapackage.json"
SCHEMA_CHIFFRES = "schemas/chiffres.json"

# Le dépôt GitHub de la base, où ses « Releases » publient la base construite.
DEPOT = "g-pliberal/comptes-nationaux"

# Certains serveurs (dont celui de l'OCDE) refusent l'agent par défaut de Python.
AGENT = f"comptes-nationaux (+https://github.com/{DEPOT})"

# Composantes de l'identifiant d'un chiffre, dans l'ordre. Une composante vide s'écrit « - ».
COMPOSANTES_ID = ["source_id", "zone", "perimetre_id", "concept_id", "fonction_id", "traitements",
                  "unite_id", "periode", "version"]


# Une copie trop grosse pour tenir dans un seul fichier du dépôt (GitHub refuse les fichiers de plus de 100 Mo) est
# archivée en morceaux de TAILLE_MORCEAU octets au plus, nommés d'après son chemin : « .partie01 », « .partie02 »… ; on
# la lit en les recollant, et son empreinte est celle du contenu recollé.
TAILLE_MORCEAU = 45 << 20


def morceaux(chemin):
    """Les morceaux d'une copie découpée, dans l'ordre ; aucun pour une copie d'un seul tenant."""
    chemin = pathlib.Path(chemin)
    if not chemin.parent.is_dir():
        return []
    motif = re.compile(re.escape(chemin.name) + r"\.partie[0-9]{2}")
    return sorted(p for p in chemin.parent.iterdir() if motif.fullmatch(p.name))


def copie_presente(chemin):
    """Vrai si la copie est archivée, d'un seul tenant ou en morceaux."""
    return pathlib.Path(chemin).exists() or bool(morceaux(chemin))


class _Recollee(io.RawIOBase):
    """Les morceaux d'une copie découpée, lus comme un seul fichier, où l'on peut se déplacer comme dans un fichier
    (zipfile lit le répertoire d'une archive à sa fin)."""

    def __init__(self, parties):
        super().__init__()
        self._fichiers = [p.open("rb") for p in parties]
        self._tailles = [p.stat().st_size for p in parties]
        self._debuts = list(itertools.accumulate([0] + self._tailles[:-1]))
        self._taille, self._position = sum(self._tailles), 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self._position

    def seek(self, decalage, origine=io.SEEK_SET):
        depart = {io.SEEK_SET: 0, io.SEEK_CUR: self._position, io.SEEK_END: self._taille}[origine]
        self._position = max(0, depart + decalage)
        return self._position

    def readinto(self, tampon):
        if self._position >= self._taille:
            return 0
        k = bisect.bisect_right(self._debuts, self._position) - 1
        self._fichiers[k].seek(self._position - self._debuts[k])
        reste = self._debuts[k] + self._tailles[k] - self._position
        n = self._fichiers[k].readinto(memoryview(tampon)[:min(len(tampon), reste)])
        self._position += n
        return n

    def close(self):
        for f in self._fichiers:
            f.close()
        super().close()


def ouvrir_copie(chemin):
    """Une copie archivée, ouverte en lecture binaire telle que reçue : décompressée si elle a été archivée compressée
    (« .bz2 »), recollée si elle l'a été en morceaux."""
    chemin = pathlib.Path(chemin)
    if chemin.suffix == ".bz2":
        return bz2.open(chemin, "rb")
    if not chemin.exists() and (parties := morceaux(chemin)):
        return io.BufferedReader(_Recollee(parties), buffer_size=1 << 20)
    return chemin.open("rb")


def empreinte_et_taille(chemin):
    """Empreinte SHA-256 et taille en octets du contenu reçu, décompressé pour une copie compressée, recollé pour une
    copie découpée."""
    h, n = hashlib.sha256(), 0
    with ouvrir_copie(chemin) as f:
        while bloc := f.read(1 << 20):
            h.update(bloc)
            n += len(bloc)
    return h.hexdigest(), n


def empreinte(chemin):
    return empreinte_et_taille(chemin)[0]


def lire_export_ofgl(chemin):
    """Les lignes d'un export csv d'un portail Opendatasoft, data.ofgl.fr, data.economie.gouv.fr ou data.drees
    (point-virgule, marque d'ordre des octets en tête) : (en-tête, lignes)."""
    with ouvrir_copie(chemin) as f:
        lecteur = csv.reader(io.TextIOWrapper(f, encoding="utf-8-sig", newline=""), delimiter=";")
        entete = next(lecteur, [])
        return entete, list(lecteur)


def en_parallele(fonction, appels, poids=None):
    """Les résultats de fonction(*a) pour chaque a de `appels`, dans leur ordre, calculés par autant de processus que la
    machine a de processeurs (ou que le dit la variable d'environnement PROCESSUS) ; `poids` donne un nombre par appel,
    et les plus lourds partent d'abord. Avec un seul processus, ou pour un seul appel, tout se calcule ici. La fonction
    et ses arguments passent d'un processus à l'autre : la fonction est définie au niveau d'un module, et rend son
    résultat plutôt que d'arrêter le programme."""
    appels = [tuple(a) for a in appels]
    processus = min(int(os.environ.get("PROCESSUS") or os.cpu_count() or 1), len(appels))
    if processus < 2:
        return [fonction(*a) for a in appels]
    ordre = sorted(range(len(appels)), key=lambda k: -(poids[k] if poids else 0))
    resultats = [None] * len(appels)
    with concurrent.futures.ProcessPoolExecutor(processus) as bassin:
        taches = {bassin.submit(fonction, *appels[k]): k for k in ordre}
        for tache in concurrent.futures.as_completed(taches):
            resultats[taches[tache]] = tache.result()
    return resultats


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
    """Écrit une table triée par sa clé, pour que les différences d'une version à l'autre restent lisibles ; la clé est
    le nom d'un champ, ou la fonction qui la donne pour une ligne."""
    chemin = BASE / chemin
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=champs, lineterminator="\n")
        ecrivain.writeheader()
        ecrivain.writerows(sorted(lignes, key=cle if callable(cle) else lambda l: l[cle]))


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


def lire_xlsx_dans_zip(chemin, membre, feuille=None):
    """lire_xlsx d'un classeur que porte une archive zip archivée, désigné par son chemin dans l'archive."""
    with zipfile.ZipFile(ouvrir_copie(chemin)) as archive:
        return lire_xlsx(io.BytesIO(archive.read(membre)), feuille)


def feuilles_xlsx(chemin):
    with zipfile.ZipFile(chemin) as classeur:
        return [f.get("name") for f in ET.fromstring(classeur.read("xl/workbook.xml")).find("m:sheets", _XLSX)]


# Lecture en flux d'une feuille trop grande pour lire_xlsx (des dizaines de millions de cellules) : les lignes une à une,
# sans construire l'arbre XML. La valeur d'une cellule qui n'a qu'elle (« <v>…</v> », le cas de presque toutes) se lit
# d'emblée ; celle d'une autre (texte en ligne, formule) dans son contenu. Un texte peut y échapper un caractère sous la
# forme « _x0030_ » (ici « 0 »).
_CELLULE = re.compile(rb'<c r="([A-Z]+)[0-9]+"([^>]*?)(?:/>|><v>([^<]*)</v></c>|>(.*?)</c>)', re.S)
_VALEUR = re.compile(rb"<v>([^<]*)</v>")
_TEXTE = re.compile(rb"<t[^>]*>([^<]*)</t>")
_TYPE = re.compile(rb' t="([a-zA-Z]+)"')
_ECHAPPEMENT = re.compile(r"_x([0-9A-Fa-f]{4})_")


def texte_xlsx(texte):
    """Un texte d'une cellule, ses caractères échappés (« _x0030_ ») rétablis."""
    return _ECHAPPEMENT.sub(lambda m: chr(int(m.group(1), 16)), texte)


def lignes_xlsx(classeur, feuille):
    """Les lignes d'une feuille d'un classeur xlsx ouvert (zipfile.ZipFile), lues en flux : pour chacune, {colonne:
    texte} ; un nombre reste écrit comme dans le fichier, une cellule vide est absente."""
    cibles = {lien.get("Id"): lien.get("Target")
              for lien in ET.fromstring(classeur.read("xl/_rels/workbook.xml.rels"))}
    feuilles = {f.get("name"): cibles[f.get(f"{{{_XLSX['r']}}}id")]
                for f in ET.fromstring(classeur.read("xl/workbook.xml")).find("m:sheets", _XLSX)}
    cible = feuilles[feuille]
    partagees = []
    if "xl/sharedStrings.xml" in classeur.namelist():
        partagees = [texte_xlsx(_textes(si)) for si in ET.fromstring(classeur.read("xl/sharedStrings.xml"))
                     .findall("m:si", _XLSX)]
    reste = b""
    with classeur.open(cible.lstrip("/") if cible.startswith("/") else f"xl/{cible}") as flux:
        while bloc := flux.read(1 << 24):
            reste += bloc
            fin = reste.rfind(b"</row>")
            if fin < 0:
                continue
            complet, reste = reste[:fin + 6], reste[fin + 6:]
            for rangee in complet.split(b"</row>")[:-1]:
                debut = rangee.find(b"<row")
                if debut < 0:
                    continue
                valeurs = {}
                for colonne, attributs, valeur, contenu in _CELLULE.findall(rangee, debut):
                    type_ = _TYPE.search(attributs) if b" t=" in attributs else None
                    type_ = type_.group(1) if type_ else b"n"
                    if type_ == b"inlineStr":
                        valeurs[colonne.decode()] = texte_xlsx(html.unescape(
                            "".join(t.decode() for t in _TEXTE.findall(contenu))))
                        continue
                    if not valeur:
                        v = _VALEUR.search(contenu) if contenu else None
                        if v is None or not v.group(1):
                            continue
                        valeur = v.group(1)
                    texte = valeur.decode()
                    valeurs[colonne.decode()] = (partagees[int(texte)] if type_ == b"s" else
                                                 texte_xlsx(html.unescape(texte)) if type_ == b"str" else texte)
                yield valeurs


def date_zip(contenu):
    """Date de modification la plus récente des fichiers que porte une archive zip, telle que l'y a inscrite son
    producteur."""
    with zipfile.ZipFile(io.BytesIO(contenu)) as archive:
        dates = [i.date_time for i in archive.infolist() if not i.is_dir()]
    return "%04d-%02d-%02dT%02d:%02d:%02d" % max(dates) if dates else ""


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


# --- Classeurs OpenDocument (ods), lus sans bibliothèque extérieure -------------------------------------

_ODS = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0", "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
        "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0", "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
        "dc": "http://purl.org/dc/elements/1.1/"}


def lire_ods(chemin):
    """Les feuilles d'un classeur ods : {nom de la feuille: [ligne, …]}, chaque ligne étant la liste des textes de ses
    cellules, de gauche à droite (une cellule répétée l'est autant de fois, sans les cellules vides qui finissent la
    ligne) ; les lignes vides qui finissent une feuille ne sont pas rendues."""
    t = "{%s}" % _ODS["table"]
    with zipfile.ZipFile(ouvrir_copie(chemin)) as classeur:
        racine = ET.fromstring(classeur.read("content.xml"))
    feuilles = {}
    for feuille in racine.iter(t + "table"):
        lignes, vides = [], 0  # vides : lignes vides en attente, rendues seulement si une ligne pleine les suit
        for rangee in feuille.iter(t + "table-row"):
            cellules, attente = [], 0  # attente : cellules vides en attente, de même
            for cellule in rangee:
                if cellule.tag not in (t + "table-cell", t + "covered-table-cell"):
                    continue
                texte = "\n".join("".join(p.itertext()) for p in cellule.findall("text:p", _ODS))
                repetee = int(cellule.get(t + "number-columns-repeated", "1"))
                if texte:
                    cellules += [""] * attente + [texte] * repetee
                    attente = 0
                else:
                    attente += repetee
            repetee = int(rangee.get(t + "number-rows-repeated", "1"))
            if cellules:
                lignes += [[]] * vides + [cellules] * repetee
                vides = 0
            else:
                vides += repetee
        feuilles[feuille.get(t + "name")] = lignes
    return feuilles


def date_ods(chemin):
    """Date de dernière modification inscrite dans les propriétés d'un classeur ods, à défaut date de création."""
    with zipfile.ZipFile(ouvrir_copie(chemin)) as classeur:
        proprietes = ET.fromstring(classeur.read("meta.xml"))
    for propriete in ("office:meta/dc:date", "office:meta/meta:creation-date"):
        date = proprietes.find(propriete, _ODS)
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


def decoder_html(octets):
    """Le texte d'une page HTML, décodé selon le jeu de caractères qu'elle déclare, UTF-8 à défaut. Les anciennes pages
    de l'Assemblée nationale se déclarent en ISO-8859-1 : comme un navigateur, on les lit en windows-1252, qui
    l'étend (apostrophes typographiques, « œ », « € »)."""
    declare = re.search(rb"<meta[^>]+charset=[\"']?([A-Za-z0-9_-]+)", octets[:4096], re.I)
    jeu = declare.group(1).decode("ascii").lower() if declare else "utf-8"
    if jeu in ("iso-8859-1", "latin-1", "latin1"):
        try:
            return octets.decode("cp1252")
        except UnicodeDecodeError:
            return octets.decode("latin-1")
    return octets.decode(jeu)


def lire_texte_html(chemin):
    """Le contenu d'une page HTML archivée, décodé (voir decoder_html)."""
    return decoder_html(pathlib.Path(chemin).read_bytes())


def lire_page_html(chemin):
    """Tableaux d'une page HTML, chacun sous forme de grille (liste de lignes, chacune liste des textes de ses
    colonnes), la mise en forme de chaque tableau (voir _grille) et le texte de la page dans l'ordre de lecture, où
    « ⟦k⟧ » marque l'ouverture du tableau k et « ⟦/k⟧ » sa fermeture."""
    lecteur = _Tableaux()
    lecteur.feed(lire_texte_html(chemin))
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
    # Les marques de direction du texte, invisibles, que certaines pages laissent dans un nombre n'en font pas partie ;
    # un trait d'union, insécable ou non, devant un nombre en est le signe moins.
    t = re.sub(r"[\s\u00a0\u202f\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", texte)
    t = re.sub(r"^[\u2010\u2011]", "-", t.replace("−", "-").replace("–", "-")).replace(",", ".")
    t = re.sub(r"^\(?\*\)?|\(?\*\)?$|(?<=[0-9])\([0-9]\)$|(?<=[0-9])%$", "", t)
    if not re.fullmatch(r"[-+]?[0-9]+(\.[0-9]+)?", t):
        return None
    t = t.lstrip("+")
    return t, len(t.split(".")[1]) if "." in t else 0


def nombre_de_phrase(phrase):
    """Le montant qu'énonce une phrase d'un texte (« …, s'élevant à 2,2 milliards d'euros ») : son seul nombre, lu
    comme par nombre_texte, ou zéro si elle le dit nul (« …, lesquelles sont nulles ») ; None sinon. Un nombre dont
    les milliers sont séparés par des blancs (« 2 351 034 ») compte pour un."""
    if re.search(r"\bnul(?:le)?s?$", phrase):
        return None if re.search(r"[0-9]", phrase) else ("0", 0)
    nombres = re.findall(r"[0-9]{1,3}(?:[ \u00a0\u202f][0-9]{3})+(?:,[0-9]+)?|[0-9]+(?:,[0-9]+)?", phrase)
    return nombre_texte(nombres[0]) if len(nombres) == 1 else None


def montants_de_case(texte):
    """Les montants d'une case qui réunit ceux de plusieurs lignes, séparés par des blancs (« 70,6 82,6 -12,0 1,8 »),
    chacun lu comme par nombre_texte ; None si l'un d'eux n'est pas un nombre."""
    nombres = [nombre_texte(x) for x in texte.split()]
    return nombres if nombres and None not in nombres else None


MOIS = {m: i for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
                                     "octobre", "novembre", "décembre"], start=1)}


def date_html(texte):
    """Date qu'un texte publié par le Sénat ou par l'Assemblée nationale porte lui-même : enregistrement, transmission
    ou adoption ; à défaut, celle de la séance au procès-verbal de laquelle il est annexé, ou celle qui suit la session
    dans l'en-tête d'un texte adopté. Les pages de l'Assemblée nationale coupent parfois un nombre en morceaux
    (« le 1 9 décembre 20 19 », « SESSION ORDINAIRE DE 20 17 -20 18 ») : la date se lit sans ces blancs."""
    date = r"([0-9](?: ?[0-9])?)(?: ?er)? (" + "|".join(MOIS) + r") ([0-9](?: ?[0-9]){3})"
    for annonce in (r"(?:Enregistré à la Présidence du Sénat|transmis au Sénat|adopté (?:définitivement )?par le Sénat) le ",
                    r"considéré comme adopté par l[’']Assemblée nationale le ", r"Délibéré en séance publique, à Paris, le ",
                    r"Annexe au procès-verbal de la séance du ",
                    r"SESSION (?:ORDINAIRE|EXTRAORDINAIRE) DE [0-9](?: ?[0-9]){3} ?- ?[0-9](?: ?[0-9]){3} "):
        trouve = re.search(annonce + date, texte)
        if trouve:
            jour, mois, annee = (x.replace(" ", "") for x in trouve.groups())
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


# --- Fichiers PDF, lus sans bibliothèque extérieure ----------------------------------------------------
#
# Le lecteur suffit aux PDF qu'écrivent les traitements de texte et les logiciels de mise en page, comme les listes
# d'organismes de l'Insee ou les rapports de la Cour des comptes : flux compressés (FlateDecode), objets rangés dans des
# flux d'objets, toute police munie d'une table ToUnicode, polices simples à l'encodage WinAnsi ou standard, ou que
# leurs « Differences » décrivent par des noms de glyphes, polices de symboles, polices composites (Identity-H) dont la
# police TrueType embarquée donne ses caractères. Il rend le texte tel que la page le dessine, morceau par morceau, à la
# position où commence chacun ; ce qu'il ne sait pas lire l'arrête, plutôt que de lui faire rendre un texte faux, et un
# signe qu'il ne sait pas lire dans une police de symboles (une puce) se lit « � ». Le texte d'une page faite d'images
# ne se lit pas.

_BLANCS_PDF = b" \t\r\n\f\x00"
_MOT_PDF = re.compile(rb"[^\s()<>\[\]{}/%]+")
_NOMBRE_PDF = re.compile(rb"[-+]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)$")
_REFERENCE_PDF = re.compile(rb"([0-9]+)\s+[0-9]+\s+R(?![^\s()<>\[\]{}/%])")
_OBJET_PDF = re.compile(rb"(?<![0-9])([0-9]+)\s+[0-9]+\s+obj\b")
_IDENTITE_PDF = (1, 0, 0, 1, 0, 0)


class _NomPdf(str):
    """Un nom PDF (« /Font »), sans sa barre oblique."""


class _OperateurPdf(bytes):
    """Un opérateur d'un flux de contenu (« BT », « Tj »…)."""


def _blancs_pdf(texte, i):
    """La position du prochain élément, après les blancs et les commentaires."""
    while i < len(texte):
        if texte[i] in _BLANCS_PDF:
            i += 1
        elif texte[i] == 0x25:  # « % » : un commentaire, jusqu'à la fin de la ligne
            while i < len(texte) and texte[i] not in b"\r\n":
                i += 1
        else:
            break
    return i


def _chaine_pdf(texte, i):
    """(octets, position qui suit) de la chaîne littérale qui commence en `i`, sur « ( » : ses parenthèses équilibrées
    en font partie, ses caractères échappés sont rétablis."""
    sortie, profondeur, i = bytearray(), 1, i + 1
    echappes = {ord("n"): b"\n", ord("r"): b"\r", ord("t"): b"\t", ord("b"): b"\b", ord("f"): b"\f"}
    while i < len(texte):
        c = texte[i]
        if c == 0x5C:  # « \ »
            suivant = texte[i + 1:i + 2]
            if suivant and suivant[0] in echappes:
                sortie += echappes[suivant[0]]
                i += 2
            elif suivant and suivant in b"01234567":
                octal = re.match(rb"[0-7]{1,3}", texte[i + 1:i + 4]).group(0)
                sortie.append(int(octal, 8) & 0xFF)
                i += 1 + len(octal)
            elif suivant in (b"\r", b"\n"):  # fin de ligne échappée : la chaîne continue sur la ligne suivante
                i += 3 if texte[i + 1:i + 3] == b"\r\n" else 2
            else:
                sortie += suivant
                i += 2
            continue
        profondeur += {0x28: 1, 0x29: -1}.get(c, 0)
        if profondeur == 0:
            return bytes(sortie), i + 1
        sortie.append(c)
        i += 1
    raise ValueError("chaîne PDF non fermée")


def _objet_pdf(texte, i=0):
    """(objet, position qui suit) de l'objet PDF qui commence en `i` : dictionnaire (dict), tableau (list), nom
    (_NomPdf), nombre, chaîne (bytes), référence ((numéro,)), booléen, None ; un autre mot est un opérateur
    (_OperateurPdf)."""
    i = _blancs_pdf(texte, i)
    if texte[i:i + 2] == b"<<":
        dictionnaire, i = {}, i + 2
        while (i := _blancs_pdf(texte, i)) < len(texte) and texte[i:i + 2] != b">>":
            cle, i = _objet_pdf(texte, i)
            dictionnaire[cle], i = _objet_pdf(texte, i)
        if i >= len(texte):
            raise ValueError("dictionnaire PDF non fermé")
        return dictionnaire, i + 2
    if texte[i:i + 1] == b"[":
        tableau, i = [], i + 1
        while (i := _blancs_pdf(texte, i)) < len(texte) and texte[i:i + 1] != b"]":
            element, i = _objet_pdf(texte, i)
            tableau.append(element)
        if i >= len(texte):
            raise ValueError("tableau PDF non fermé")
        return tableau, i + 1
    if texte[i:i + 1] == b"(":
        return _chaine_pdf(texte, i)
    if texte[i:i + 1] == b"<":
        fin = texte.index(b">", i)
        hexa = re.sub(rb"\s", b"", texte[i + 1:fin])
        return bytes.fromhex((hexa + b"0" * (len(hexa) % 2)).decode("ascii")), fin + 1
    if texte[i:i + 1] == b"/":
        mot = _MOT_PDF.match(texte, i + 1)
        nom = mot.group(0) if mot else b""
        return _NomPdf(re.sub(rb"#([0-9A-Fa-f]{2})", lambda m: bytes([int(m.group(1), 16)]), nom).decode("latin-1")), \
            i + 1 + len(nom)
    if reference := _REFERENCE_PDF.match(texte, i):
        return (int(reference.group(1)),), reference.end()
    mot = _MOT_PDF.match(texte, i)
    if mot is None:
        raise ValueError(f"objet PDF illisible à la position {i}")
    mot = mot.group(0)
    if _NOMBRE_PDF.match(mot):
        return (float(mot) if b"." in mot else int(mot)), i + len(mot)
    return {b"true": True, b"false": False, b"null": None}.get(mot, _OperateurPdf(mot)), i + len(mot)


def _objets_pdf(donnees):
    """{numéro: (valeur, flux brut ou None)} des objets d'un PDF, ceux de ses flux d'objets compris. Un objet défini
    deux fois (un PDF mis à jour) garde sa définition la plus tardive dans le fichier."""
    objets, positions = {}, {}
    for entete in _OBJET_PDF.finditer(donnees):
        try:
            valeur, i = _objet_pdf(donnees, entete.end())
        except (ValueError, IndexError, RecursionError, UnicodeDecodeError):
            continue  # pas un objet : ces octets appartiennent au flux d'un autre
        brut = None
        if donnees.startswith(b"stream", debut := _blancs_pdf(donnees, i)):
            debut += len(b"stream")
            debut += 2 if donnees[debut:debut + 2] == b"\r\n" else 1
            longueur = valeur.get("Length") if isinstance(valeur, dict) else None
            if isinstance(longueur, int) and re.match(rb"\s*endstream", donnees[debut + longueur:debut + longueur + 12]):
                brut = donnees[debut:debut + longueur]
            else:
                fin = donnees.index(b"endstream", debut)
                brut = donnees[debut:fin - (2 if donnees[fin - 2:fin] == b"\r\n" else 1 if donnees[fin - 1:fin] in b"\r\n"
                                            else 0)]
        objets[int(entete.group(1))] = (valeur, brut)
        positions[int(entete.group(1))] = entete.start()
    for numero, (valeur, brut) in list(objets.items()):
        if isinstance(valeur, dict) and valeur.get("Type") == "ObjStm":
            contenu, premier, n = _flux_pdf(objets, (numero,)), *(_resoudre_pdf(objets, valeur[c]) for c in ("First", "N"))
            nombres = [int(x) for x in contenu[:premier].split()]
            for numero_contenu, decalage in zip(nombres[0:2 * n:2], nombres[1:2 * n:2]):
                if positions.get(numero_contenu, -1) < positions[numero]:
                    objets[numero_contenu] = (_objet_pdf(contenu, premier + decalage)[0], None)
                    positions[numero_contenu] = positions[numero]
    return objets


def _resoudre_pdf(objets, valeur):
    """La valeur d'un objet, la référence qui la désigne suivie."""
    while isinstance(valeur, tuple):
        valeur = objets[valeur[0]][0] if valeur[0] in objets else None
    return valeur


def _flux_pdf(objets, reference):
    """Le contenu, décompressé, du flux que désigne une référence."""
    dictionnaire, brut = objets.get(reference[0], (None, None))
    if brut is None:
        raise ValueError(f"l'objet PDF {reference[0]} n'est pas un flux")
    filtres = _resoudre_pdf(objets, dictionnaire.get("Filter"))
    parametres = _resoudre_pdf(objets, dictionnaire.get("DecodeParms"))
    for filtre in filtres if isinstance(filtres, list) else [filtres] if filtres else []:
        if filtre != "FlateDecode":
            raise ValueError(f"flux PDF compressé par un filtre que le lecteur ne connaît pas : {filtre}")
        brut = zlib.decompressobj().decompress(brut)
    if any(isinstance(p, dict) and p.get("Predictor", 1) > 1 for p in (parametres if isinstance(parametres, list)
                                                                         else [parametres])):
        raise ValueError("flux PDF à prédicteur, que le lecteur ne connaît pas")
    return brut


def _table_tounicode(texte):
    """La table d'une CMap ToUnicode : code (entier) → texte."""
    table = {}
    for bloc in re.findall(rb"beginbfchar(.*?)endbfchar", texte, re.S):
        for code, destination in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", bloc):
            table[int(code, 16)] = bytes.fromhex(destination.decode("ascii")).decode("utf-16-be")
    for bloc in re.findall(rb"beginbfrange(.*?)endbfrange", texte, re.S):
        for debut, fin, destination in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(<[0-9A-Fa-f]*>|\[[^\]]*\])",
                                                   bloc):
            debut, fin = int(debut, 16), int(fin, 16)
            if destination.startswith(b"["):
                for k, d in enumerate(re.findall(rb"<([0-9A-Fa-f]*)>", destination)):
                    table[debut + k] = bytes.fromhex(d.decode("ascii")).decode("utf-16-be")
            else:  # la destination du premier code, dont le dernier octet augmente d'un code à l'autre
                octets = bytes.fromhex(destination[1:-1].decode("ascii"))
                for k in range(fin - debut + 1):
                    suivant = octets[:-1] + bytes([octets[-1] + k]) if octets else b""
                    table[debut + k] = suivant.decode("utf-16-be")
    return table


# Polices simples sans table ToUnicode. Leur encodage dit, pour chaque code, le nom d'un glyphe (« eacute »), que
# _unicode_glyphe traduit : l'encodage WinAnsi, l'encodage standard d'Adobe, propre aux polices de texte standard
# (Times, Helvetica, Courier) qui n'en déclarent pas d'autre, et les noms qu'y substituent ses « Differences ». Une
# police de symboles (Symbol, ZapfDingbats, Wingdings…) ne rend que ses codes sûrs (chiffres et ponctuation, et pour la
# police Symbol sans autre encodage, signe moins, puce, ≥…) et ceux que ses « Differences » nomment ; un autre de ses
# codes, la puce ou la flèche d'une police Wingdings, se lit « � », jamais comme un autre caractère.
_STANDARD_PDF = dict(zip(range(0x20, 0x7F), (
    "space exclam quotedbl numbersign dollar percent ampersand quoteright parenleft parenright asterisk plus comma "
    "hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater "
    "question at " + " ".join("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + " bracketleft backslash bracketright asciicircum "
    "underscore quoteleft " + " ".join("abcdefghijklmnopqrstuvwxyz") + " braceleft bar braceright asciitilde").split()))
_STANDARD_PDF.update({
    0xA1: "exclamdown", 0xA2: "cent", 0xA3: "sterling", 0xA4: "fraction", 0xA5: "yen", 0xA6: "florin", 0xA7: "section",
    0xA8: "currency", 0xA9: "quotesingle", 0xAA: "quotedblleft", 0xAB: "guillemotleft", 0xAC: "guilsinglleft",
    0xAD: "guilsinglright", 0xAE: "fi", 0xAF: "fl", 0xB1: "endash", 0xB2: "dagger", 0xB3: "daggerdbl",
    0xB4: "periodcentered", 0xB6: "paragraph", 0xB7: "bullet", 0xB8: "quotesinglbase", 0xB9: "quotedblbase",
    0xBA: "quotedblright", 0xBB: "guillemotright", 0xBC: "ellipsis", 0xBD: "perthousand", 0xBF: "questiondown",
    0xC1: "grave", 0xC2: "acute", 0xC3: "circumflex", 0xC4: "tilde", 0xC5: "macron", 0xC6: "breve", 0xC7: "dotaccent",
    0xC8: "dieresis", 0xCA: "ring", 0xCB: "cedilla", 0xCD: "hungarumlaut", 0xCE: "ogonek", 0xCF: "caron",
    0xD0: "emdash", 0xE1: "AE", 0xE3: "ordfeminine", 0xE8: "Lslash", 0xE9: "Oslash", 0xEA: "OE", 0xEB: "ordmasculine",
    0xF1: "ae", 0xF5: "dotlessi", 0xF8: "lslash", 0xF9: "oslash", 0xFA: "oe", 0xFB: "germandbls"})
# Noms de glyphes qui ne se déduisent pas d'une lettre et de son accent ; une ligature se lit en ses lettres.
_GLYPHES_PDF = {
    "space": " ", "exclam": "!", "quotedbl": '"', "numbersign": "#", "dollar": "$", "percent": "%", "ampersand": "&",
    "quotesingle": "'", "quoteright": "’", "quoteleft": "‘", "parenleft": "(", "parenright": ")", "asterisk": "*",
    "plus": "+", "comma": ",", "hyphen": "-", "period": ".", "slash": "/", "zero": "0", "one": "1", "two": "2",
    "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "colon": ":",
    "semicolon": ";", "less": "<", "equal": "=", "greater": ">", "question": "?", "at": "@", "bracketleft": "[",
    "backslash": "\\", "bracketright": "]", "asciicircum": "^", "underscore": "_", "grave": "`", "braceleft": "{",
    "bar": "|", "braceright": "}", "asciitilde": "~", "exclamdown": "¡", "cent": "¢", "sterling": "£", "fraction": "⁄",
    "yen": "¥", "florin": "ƒ", "section": "§", "currency": "¤", "quotedblleft": "“", "quotedblright": "”",
    "quotesinglbase": "‚", "quotedblbase": "„", "guillemotleft": "«", "guillemotright": "»", "guilsinglleft": "‹",
    "guilsinglright": "›", "fi": "fi", "fl": "fl", "ff": "ff", "ffi": "ffi", "ffl": "ffl", "endash": "–",
    "emdash": "—", "dagger": "†", "daggerdbl": "‡", "periodcentered": "·", "paragraph": "¶", "bullet": "•",
    "ellipsis": "…", "perthousand": "‰", "questiondown": "¿", "acute": "´", "circumflex": "ˆ", "tilde": "˜",
    "macron": "¯", "breve": "˘", "dotaccent": "˙", "dieresis": "¨", "ring": "˚", "cedilla": "¸", "hungarumlaut": "˝",
    "ogonek": "˛", "caron": "ˇ", "AE": "Æ", "ae": "æ", "OE": "Œ", "oe": "œ", "Oslash": "Ø", "oslash": "ø",
    "Lslash": "Ł", "lslash": "ł", "germandbls": "ß", "dotlessi": "ı", "Eth": "Ð", "eth": "ð", "Thorn": "Þ",
    "thorn": "þ", "ordfeminine": "ª", "ordmasculine": "º", "degree": "°", "copyright": "©", "registered": "®",
    "trademark": "™", "plusminus": "±", "multiply": "×", "divide": "÷", "onehalf": "½", "onequarter": "¼",
    "threequarters": "¾", "onesuperior": "¹", "twosuperior": "²", "threesuperior": "³", "mu": "µ", "Euro": "€",
    "brokenbar": "¦", "logicalnot": "¬", "minus": "−", "nbspace": " ", "nonbreakingspace": " ",
    "sfthyphen": "­", "asteriskmath": "∗", "greaterequal": "≥", "lessequal": "≤", "notequal": "≠",
    "approxequal": "≈", "infinity": "∞", "arrowright": "→", "arrowleft": "←", "arrowboth": "↔", "dotmath": "⋅"}
_ACCENTS_PDF = {"acute": "ACUTE", "grave": "GRAVE", "circumflex": "CIRCUMFLEX", "dieresis": "DIAERESIS",
                "tilde": "TILDE", "ring": "RING ABOVE", "cedilla": "CEDILLA", "caron": "CARON", "macron": "MACRON",
                "breve": "BREVE", "ogonek": "OGONEK", "dotaccent": "DOT ABOVE", "hungarumlaut": "DOUBLE ACUTE"}
# Codes d'une police de symboles qu'on sait lire : ceux qu'elle partage avec l'ASCII, et ses signes les plus courants
# (encodage de la police Symbol d'Adobe) ; ZapfDingbats et Wingdings n'en ont pas d'autre que l'espace.
_SYMBOLES_SURS = set(b" !#%&()+,./0123456789:;<=>?")
_SYMBOL_PDF = {**{c: chr(c) for c in _SYMBOLES_SURS}, 0x2D: "−", 0xA3: "≤", 0xB0: "°", 0xB1: "±",
               0xB3: "≥", 0xB4: "×", 0xB7: "•", 0xB8: "÷", 0xB9: "≠", 0xBB: "≈", 0xBC: "…", 0xAC: "←", 0xAE: "→"}
_POLICES_SYMBOLES = re.compile(r"(?:[A-Z]{6}\+)?(Symbol|ZapfDingbats|Dingbats|Wingdings|Webdings|MonotypeSorts)")
_POLICES_STANDARD = re.compile(r"(?:[A-Z]{6}\+)?(Times|Helvetica|Courier)(-|$)")


def _unicode_glyphe(nom):
    """Le texte d'un nom de glyphe (« eacute » → « é », « uni00E9 », « f_i » → « fi », « one.numr » → « 1 ») ; None
    pour un nom qui ne dit pas son caractère (« g123 », « .notdef »)."""
    texte = []
    for partie in nom.split(".")[0].split("_") if nom and not nom.startswith(".") else [None]:
        if partie in _GLYPHES_PDF:
            texte.append(_GLYPHES_PDF[partie])
        elif partie and re.fullmatch(r"[A-Za-z]", partie):
            texte.append(partie)
        elif partie and (m := re.fullmatch(r"uni((?:[0-9A-F]{4})+)", partie)):
            texte += [chr(int(m.group(1)[k:k + 4], 16)) for k in range(0, len(m.group(1)), 4)]
        elif partie and (m := re.fullmatch(r"u([0-9A-F]{4,6})", partie)):
            texte.append(chr(int(m.group(1), 16)))
        elif partie and (m := re.fullmatch(r"([A-Za-z])(" + "|".join(_ACCENTS_PDF) + ")", partie)):
            casse = "CAPITAL" if m.group(1).isupper() else "SMALL"
            try:
                texte.append(unicodedata.lookup(f"LATIN {casse} LETTER {m.group(1).upper()} WITH "
                                                f"{_ACCENTS_PDF[m.group(2)]}"))
            except KeyError:
                return None
        else:
            return None
    return "".join(texte)


def _table_simple(objets, police):
    """(table code → texte, symbolique) d'une police simple sans table ToUnicode, d'après son encodage ; None quand le
    lecteur ne sait pas l'établir (une police embarquée qui ne déclare pas son encodage)."""
    nom = str(police.get("BaseFont") or "")
    symboles = _POLICES_SYMBOLES.match(nom)
    encodage = _resoudre_pdf(objets, police.get("Encoding"))
    base, differences = (encodage.get("BaseEncoding"), _resoudre_pdf(objets, encodage.get("Differences")) or []) \
        if isinstance(encodage, dict) else (encodage, [])
    descripteur = _resoudre_pdf(objets, police.get("FontDescriptor")) or {}
    embarquee = any(k in descripteur for k in ("FontFile", "FontFile2", "FontFile3"))
    if base == "WinAnsiEncoding":
        table = {}
        for c in range(256):
            try:
                table[c] = bytes([c]).decode("cp1252")
            except UnicodeDecodeError:
                pass
    elif base == "StandardEncoding" or base is None and not embarquee and _POLICES_STANDARD.match(nom):
        table = {c: _unicode_glyphe(g) for c, g in _STANDARD_PDF.items()}
    elif base is None and symboles:
        table = dict(_SYMBOL_PDF) if symboles.group(1) == "Symbol" else {0x20: " "}
    else:
        return None
    if symboles and base is not None:
        # Une police de symboles qui déclare l'encodage d'une police de texte : seuls ses chiffres et sa ponctuation
        # s'y lisent sûrement ; un autre de ses codes, que ses « Differences » ne nomment pas, se lit « � ».
        table = {c: t for c, t in table.items() if c in _SYMBOLES_SURS}
    code = None
    for element in differences:
        if isinstance(element, int):
            code = element
        elif isinstance(element, str) and code is not None:
            table[code] = _unicode_glyphe(element)
            code += 1
    return {c: t for c, t in table.items() if t is not None}, bool(symboles)


def _unicode_truetype(donnees):
    """La table glyphe → texte d'une police TrueType, d'après ses tables cmap Unicode (formats 4 et 12) : un glyphe
    que plusieurs caractères désignent se lit comme le premier d'entre eux, hors zone d'usage privé."""
    nombre = int.from_bytes(donnees[4:6], "big")
    tables = {donnees[12 + 16 * k:16 + 16 * k]: int.from_bytes(donnees[20 + 16 * k:24 + 16 * k], "big")
              for k in range(nombre)}
    if b"cmap" not in tables:
        return {}
    debut = tables[b"cmap"]
    u16 = lambda i: int.from_bytes(donnees[i:i + 2], "big")
    u32 = lambda i: int.from_bytes(donnees[i:i + 4], "big")
    glyphes = {}
    for k in range(u16(debut + 2)):
        plateforme, codage, decalage = u16(debut + 4 + 8 * k), u16(debut + 6 + 8 * k), u32(debut + 8 + 8 * k)
        if (plateforme, codage) not in ((3, 1), (3, 10), (0, 3), (0, 4)):
            continue
        t = debut + decalage
        if u16(t) == 4:
            n = u16(t + 6) // 2
            fins, debuts = t + 14, t + 16 + 2 * n
            deltas, plages = debuts + 2 * n, debuts + 4 * n
            for s in range(n):
                premier, dernier = u16(debuts + 2 * s), u16(fins + 2 * s)
                delta, plage = u16(deltas + 2 * s), u16(plages + 2 * s)
                for c in range(premier, min(dernier, 0xFFFE) + 1):
                    g = (c + delta) & 0xFFFF if plage == 0 else u16(plages + 2 * s + plage + 2 * (c - premier))
                    if plage and g:
                        g = (g + delta) & 0xFFFF
                    if g:
                        glyphes.setdefault(g, []).append(c)
        elif u16(t) == 12:
            for k2 in range(u32(t + 12)):
                premier, dernier, g = u32(t + 16 + 12 * k2), u32(t + 20 + 12 * k2), u32(t + 24 + 12 * k2)
                for c in range(premier, dernier + 1):
                    glyphes.setdefault(g + c - premier, []).append(c)
    table = {}
    for g, codes in glyphes.items():
        codes = sorted(set(codes), key=lambda c: (0xE000 <= c <= 0xF8FF, c))
        if not 0xE000 <= codes[0] <= 0xF8FF:
            table[g] = chr(codes[0])
    return table


def _table_composite(objets, police):
    """La table code → texte d'une police composite Identity-H sans table ToUnicode, dont la police descendante est
    une police TrueType embarquée (CIDFontType2) : chaque code est un identifiant, qui désigne un glyphe directement ou
    par la table CIDToGIDMap ; None sinon."""
    if police.get("Encoding") not in ("Identity-H", "Identity-V"):
        return None
    descendante = _resoudre_pdf(objets, (_resoudre_pdf(objets, police.get("DescendantFonts")) or [None])[0])
    descripteur = _resoudre_pdf(objets, (descendante or {}).get("FontDescriptor")) or {}
    if not descendante or descendante.get("Subtype") != "CIDFontType2" or "FontFile2" not in descripteur:
        return None
    glyphes = _unicode_truetype(_flux_pdf(objets, descripteur["FontFile2"]))
    correspondance = descendante.get("CIDToGIDMap", "Identity")
    if correspondance == "Identity":
        return glyphes
    table_cid = _flux_pdf(objets, correspondance)
    return {cid: glyphes[g] for cid in range(len(table_cid) // 2)
            if (g := int.from_bytes(table_cid[2 * cid:2 * cid + 2], "big")) in glyphes}


def _polices_pdf(objets, ressources):
    """{nom: (octets par code, table code → texte ou None, encodage simple ou None, repli)} des polices de ressources.
    Le repli vaut « � » pour une police de symboles, dont un code inconnu se lit ainsi ; pour une police que le lecteur
    ne sait pas lire, c'est le message de l'erreur, qui ne survient qu'au premier texte qu'elle dessine."""
    polices = {}
    for nom, reference in (_resoudre_pdf(objets, ressources.get("Font")) or {}).items():
        police = _resoudre_pdf(objets, reference)
        table = _table_tounicode(_flux_pdf(objets, police["ToUnicode"])) if "ToUnicode" in police else None
        if police.get("Subtype") == "Type0":
            if police.get("Encoding") in ("Identity-H", "Identity-V") and table is not None:
                polices[nom] = (2, table, None, None)
            elif table is None and (composite := _table_composite(objets, police)) is not None:
                polices[nom] = (2, composite, None, None)
            else:
                polices[nom] = (2, {}, None, f"police composite {police.get('BaseFont')} sans table ToUnicode ou à "
                                             f"l'encodage {police.get('Encoding')}, que le lecteur ne connaît pas")
            continue
        encodage = _resoudre_pdf(objets, police.get("Encoding"))
        if isinstance(encodage, dict):
            encodage = None if "Differences" in encodage else encodage.get("BaseEncoding")
        if encodage == "WinAnsiEncoding" or table is not None:
            # Un code que la table ToUnicode ne donne pas se lit d'après l'encodage de la police, quand il le décrit.
            simple = _table_simple(objets, police) if table is not None and encodage != "WinAnsiEncoding" else None
            polices[nom] = (1, {**simple[0], **table} if simple else table,
                            "cp1252" if encodage == "WinAnsiEncoding" else None, "\ufffd" if simple and simple[1] else None)
            continue
        simple = _table_simple(objets, police)
        polices[nom] = (1, simple[0], None, "\ufffd" if simple[1] else None) if simple else \
            (1, {}, None, f"police {police.get('BaseFont')} à l'encodage {encodage}, que le lecteur ne connaît pas")
    return polices


def _decoder_pdf(octets, police):
    largeur, table, encodage, repli = police
    if len(octets) % largeur:
        raise ValueError("chaîne PDF d'une longueur qui ne convient pas à sa police")
    texte = []
    for k in range(0, len(octets), largeur):
        code = int.from_bytes(octets[k:k + largeur], "big")
        if table is not None and code in table:
            texte.append(table[code])
        elif encodage is not None:
            texte.append(bytes([code]).decode(encodage))
        elif repli == "\ufffd":
            texte.append(repli)
        else:
            raise ValueError(repli or f"code {code:#x} sans correspondance dans sa police")
    return "".join(texte)


def _produit_pdf(m, n):
    """Le produit de deux matrices de transformation [a b c d e f] : m, puis n."""
    a, b, c, d, e, f = m
    a2, b2, c2, d2, e2, f2 = n
    return (a * a2 + b * c2, a * b2 + b * d2, c * a2 + d * c2, c * b2 + d * d2, e * a2 + f * c2 + e2, e * b2 + f * d2 + f2)


def _morceaux_pdf(objets, contenu, ressources, matrice, morceaux):
    """Ajoute à `morceaux` ceux d'un flux de contenu : (x, y, texte), à la position où commence chacun, dans l'espace de
    la page ; un formulaire (XObject) que dessine le flux y ajoute les siens."""
    polices, pile, etats = _polices_pdf(objets, ressources), [], []
    police, tm, tlm, interligne, i = None, _IDENTITE_PDF, _IDENTITE_PDF, 0, 0
    while (i := _blancs_pdf(contenu, i)) < len(contenu):
        element, i = _objet_pdf(contenu, i)
        if not isinstance(element, _OperateurPdf):
            pile.append(element)
            continue
        operateur = bytes(element)
        if operateur == b"BI":  # une image en ligne : ses données, jusqu'à « EI », ne sont pas des objets
            i = re.compile(rb"\sEI(?![^\s()<>\[\]{}/%])").search(contenu, contenu.index(b"ID", i) + 3).end()
        elif operateur == b"q":
            etats.append(matrice)
        elif operateur == b"Q" and etats:
            matrice = etats.pop()
        elif operateur == b"cm":
            matrice = _produit_pdf(pile[-6:], matrice)
        elif operateur == b"BT":
            tm = tlm = _IDENTITE_PDF
        elif operateur == b"Tf":
            if pile[-2] not in polices:
                raise ValueError(f"police {pile[-2]} absente des ressources de la page")
            police = polices[pile[-2]]
        elif operateur == b"TL":
            interligne = pile[-1]
        elif operateur == b"Tm":
            tm = tlm = tuple(pile[-6:])
        elif operateur in (b"Td", b"TD", b"T*", b"'", b'"'):
            if operateur == b"TD":
                interligne = -pile[-1]
            dx, dy = pile[-2:] if operateur in (b"Td", b"TD") else (0, -interligne)
            tm = tlm = _produit_pdf((1, 0, 0, 1, dx, dy), tlm)
        if operateur in (b"Tj", b"TJ", b"'", b'"'):
            if police is None:
                raise ValueError("texte PDF dessiné sans police")
            chaines = pile[-1] if operateur == b"TJ" else [pile[-1]]
            x, y = _produit_pdf(tm, matrice)[4:]
            morceaux.append((x, y, "".join(_decoder_pdf(c, police) for c in chaines if isinstance(c, bytes))))
        elif operateur == b"Do":
            reference = (_resoudre_pdf(objets, ressources.get("XObject")) or {}).get(pile[-1])
            formulaire = _resoudre_pdf(objets, reference)
            if isinstance(formulaire, dict) and formulaire.get("Subtype") == "Form":
                _morceaux_pdf(objets, _flux_pdf(objets, reference),
                              _resoudre_pdf(objets, formulaire.get("Resources")) or ressources,
                              _produit_pdf(formulaire.get("Matrix", _IDENTITE_PDF), matrice), morceaux)
        pile = []
    return morceaux


def _pages_pdf(donnees, objets):
    """Les pages d'un PDF dans l'ordre, chacune (dictionnaire, ressources, héritées au besoin de l'arbre des pages)."""
    racine = re.findall(rb"/Root\s+([0-9]+)\s+[0-9]+\s+R", donnees)
    catalogue = _resoudre_pdf(objets, (int(racine[-1]),)) if racine else None
    if not isinstance(catalogue, dict) or "Pages" not in catalogue:
        raise ValueError("PDF sans catalogue de ses pages")
    noeuds = [(catalogue["Pages"], {})]
    pages = []
    while noeuds:
        noeud, ressources = noeuds.pop(0)
        noeud = _resoudre_pdf(objets, noeud)
        ressources = _resoudre_pdf(objets, noeud.get("Resources")) or ressources
        if noeud.get("Type") == "Pages":
            noeuds[:0] = [(fils, ressources) for fils in _resoudre_pdf(objets, noeud["Kids"])]
        else:
            pages.append((noeud, ressources))
    return pages


def lignes_pdf(morceaux, tolerance=1.0):
    """Les morceaux d'une page en lignes, de haut en bas : (ordonnée, [(abscisse, texte)…]), de gauche à droite ; deux
    morceaux sont sur une même ligne si leurs ordonnées diffèrent d'au plus `tolerance` points."""
    lignes = []
    for x, y, texte in sorted(morceaux, key=lambda m: -m[1]):
        if lignes and lignes[-1][0] - y <= tolerance:
            lignes[-1][1].append((x, texte))
        else:
            lignes.append((y, [(x, texte)]))
    return [(y, sorted(ligne, key=lambda m: m[0])) for y, ligne in lignes]


def lire_pdf(chemin):
    """Le texte d'un PDF, page par page : pour chaque page, ses lignes de haut en bas (voir lignes_pdf)."""
    with ouvrir_copie(chemin) as f:
        donnees = f.read()
    objets, pages = _objets_pdf(donnees), []
    for page, ressources in _pages_pdf(donnees, objets):
        contenus = page.get("Contents")
        if isinstance(_resoudre_pdf(objets, contenus), list):  # un tableau de flux, désigné par une référence
            contenus = _resoudre_pdf(objets, contenus)
        references = contenus if isinstance(contenus, list) else [contenus] if contenus is not None else []
        contenu = b"\n".join(_flux_pdf(objets, r) for r in references)
        pages.append(lignes_pdf(_morceaux_pdf(objets, contenu, ressources, _IDENTITE_PDF, [])))
    return pages


def texte_pdf(morceaux):
    """Le texte de morceaux d'une ligne, (abscisse, texte) : mis bout à bout, ses blancs réduits à une espace."""
    return " ".join("".join(t for _, t in morceaux).split())


def texte_page_pdf(page):
    """Le texte d'une page de PDF (lignes_pdf), ses lignes mises bout à bout."""
    return " ".join(texte_pdf(m) for _, m in page)


def nombre_phrase_pdf(pages, page, phrase):
    """Le nombre qu'énonce un extrait d'une page de PDF (« page=42;phrase=… ») : l'extrait doit figurer une seule fois
    dans le texte de la page, sans couper un nombre (_coupe_un_nombre), et ne porter qu'un nombre, lu comme par
    nombre_de_phrase, où des milliers séparés par des points (« 2.088.767 ») font un seul nombre ; None sinon."""
    texte = texte_page_pdf(pages[page - 1]) if 1 <= page <= len(pages) else ""
    if not phrase or texte.count(phrase) != 1:
        return None
    i = texte.index(phrase)
    if _coupe_un_nombre(texte[:i], phrase, texte[i + len(phrase):]):
        return None
    return nombre_de_phrase(re.sub(r"(?<![0-9.,])([0-9]{1,3}(?:\.[0-9]{3})+)(?![0-9]|[.,][0-9])",
                                   lambda m: m.group(1).replace(".", " "), phrase))


def _coupe_un_nombre(avant, phrase, apres):
    """Vrai si un extrait commence ou finit au milieu d'un nombre du texte : un chiffre collé à lui, un groupe de
    milliers qui le prolonge (« 2 » avant « 166 900 », « 900 » après « 2 166 ») ou des décimales après lui. Un nombre
    qui ne commence pas par trois chiffres ne peut pas prolonger les milliers d'un autre : « 79 1 954 921 » est l'appel
    de note 79, puis 1 954 921."""
    debut, fin = re.match(r"[0-9]+", phrase), re.search(r"[0-9]+$", phrase)
    if debut and (re.search(r"[0-9]$", avant) or len(debut.group()) == 3 and re.search(r"[0-9][ \u00a0.]$", avant)):
        return True
    return bool(fin and re.match(r"[0-9]|[ \u00a0.][0-9]{3}(?![0-9])|,[0-9]", apres))


# Un montant qui finit un texte : chiffres groupés par trois, signe moins et décimales compris ; ce qui le précède ne
# finit pas par un chiffre (les points de conduite d'un libellé, eux, peuvent le toucher).
NOMBRE_FINAL = re.compile(r"(?<![0-9,])[-\u2011\u2212]?[0-9]{1,3}(?:[ \u00a0][0-9]{3})*(?:,[0-9]+)?$")


def montant_pdf(morceaux, debut, fin):
    """Le montant qui finit le texte des morceaux d'une ligne de PDF dont l'abscisse est dans [debut, fin[, lu comme
    par nombre_texte ; None s'il n'y en a pas. Un montant que la page coupe en plusieurs morceaux (« 62 », « 888 »,
    « 000 »), ou qu'elle écrit dans le morceau de son libellé, se lit en entier."""
    trouve = NOMBRE_FINAL.search(texte_pdf([(x, t) for x, t in sorted(morceaux) if debut <= x < fin]))
    return nombre_texte(trouve.group(0)) if trouve else None


def date_pdf(donnees):
    """Date de dernière modification que le producteur a inscrite dans un PDF, à défaut date de création : « D:2026051815
    4927+02'00' » → « 2026-05-18T15:49:27+02:00 » ; vide s'il n'en porte pas."""
    infos = re.findall(rb"/Info\s+([0-9]+)\s+[0-9]+\s+R", donnees)
    info = _resoudre_pdf(_objets_pdf(donnees), (int(infos[-1]),)) if infos else None
    for cle in ("ModDate", "CreationDate"):
        date = info.get(cle) if isinstance(info, dict) else None
        if isinstance(date, bytes):
            date = date[2:].decode("utf-16-be") if date.startswith(b"\xfe\xff") else date.decode("latin-1")
            m = re.match(r"D:([0-9]{4})([0-9]{2})?([0-9]{2})?([0-9]{2})?([0-9]{2})?([0-9]{2})?(Z|[-+][0-9]{2}'?[0-9]{2})?",
                         date)
            if m:
                annee, mois, jour, heure, minute, seconde, zone = m.groups()
                texte = "-".join(p for p in (annee, mois, jour) if p)
                if heure:
                    texte += f"T{heure}:{minute or '00'}:{seconde or '00'}"
                    texte += "" if zone is None else "Z" if zone == "Z" else f"{zone[:3]}:{zone[-2:]}"
                return texte
    return ""


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
