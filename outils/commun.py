"""Fonctions partagées par les outils de la base : chemins, lecture et écriture des tables, empreintes."""

import csv
import datetime
import hashlib
import json
import pathlib

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
