"""Fonctions partagées par les outils de la base : chemins, lecture et écriture des tables, empreintes."""

import csv
import datetime
import hashlib
import json
import math
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
BASE = RACINE / "base"
PAQUET = BASE / "datapackage.json"

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
    """Les tables de chiffres : une par famille de sources, toutes au même schéma."""
    return [r for r in paquet()["resources"] if r["schema_chemin"] == "schemas/chiffres.json"]


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
    """Date de dernière modification inscrite par le producteur dans les propriétés du classeur."""
    with zipfile.ZipFile(chemin) as classeur:
        proprietes = ET.fromstring(classeur.read("docProps/core.xml"))
    modifie = proprietes.find("dcterms:modified", _XLSX)
    return modifie.text if modifie is not None else ""


def position(reference):
    """« BQ7 » → (7, « BQ »)."""
    lettres, chiffres = re.fullmatch(r"([A-Z]+)([0-9]+)", reference).groups()
    return int(chiffres), lettres


def nombre(valeur):
    """Texte d'un nombre lu dans un fichier, débarrassé des artefacts de la virgule flottante, et ses décimales."""
    texte = repr(round(float(valeur), 9))
    texte = texte[:-2] if texte.endswith(".0") else texte
    return texte, len(texte.split(".")[1]) if "." in texte else 0


# --- Fusion des chiffres importés ----------------------------------------------------------------------

def meme_valeur(a, b):
    return (math.isclose(float(a["valeur"]), float(b["valeur"]), rel_tol=1e-12, abs_tol=1e-9)
            and a["statut"] == b["statut"])


def fusionner(existants, nouveaux, origine):
    """Ajoute à `existants` (identifiant → ligne) les chiffres nouveaux d'une copie archivée.

    Une valeur déjà enregistrée à l'identique est ignorée, de même qu'une valeur qu'une version plus
    récente de la source reprend sans changement : seule la version où elle apparaît est enregistrée.
    Deux valeurs différentes pour un même identifiant arrêtent l'import.
    Renvoie (nombre de chiffres ajoutés, nombre de chiffres inchangés)."""
    cle = lambda l: tuple(l[c] for c in COMPOSANTES_ID[:-1])
    dernieres = {}
    for l in existants.values():
        if cle(l) not in dernieres or l["version"] > dernieres[cle(l)]["version"]:
            dernieres[cle(l)] = l
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
        precedent = dernieres.get(cle(l))
        if precedent is not None and precedent["version"] < l["version"] and meme_valeur(precedent, l):
            inchanges += 1
            continue
        existants[l["id"]] = l
        dernieres[cle(l)] = l
        ajoutes += 1
    if conflits:
        sys.exit("Import interrompu, valeurs contradictoires pour une même version :\n" + "\n".join(conflits))
    return ajoutes, inchanges
