#!/usr/bin/env python3
"""Télécharge la base construite, prête à interroger, sans avoir à la reconstruire.

    python3 outils/telecharger.py [--version <étiquette>] [--depuis <dossier>]

Télécharge la dernière publication de la base dans les « Releases » du dépôt sur GitHub (ou celle de l'étiquette
donnée, « base-2026-11-12-e8d2dff »), vérifie l'empreinte de chaque partie, les décompresse et écrit
base/construite/comptes.sqlite, dont l'empreinte est vérifiée à son tour, et base/construite/empreintes.csv. Avec
--depuis, les fichiers de la publication sont pris dans un dossier, déjà téléchargés.

La base téléchargée est celle que construit `python3 outils/construire.py` au commit qu'indique la publication : en la
reconstruisant, chacun peut comparer les empreintes de ses tables à celles de la publication.
"""

import argparse
import csv
import hashlib
import json
import lzma
import pathlib
import shutil
import sys
import urllib.error
import urllib.request

from commun import AGENT, BASE, DEPOT, RACINE

CONSTRUITE = BASE / "construite"
API = f"https://api.github.com/repos/{DEPOT}/releases"


def ouvrir(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=300)


def empreinte(chemin):
    h = hashlib.sha256()
    with chemin.open("rb") as f:
        while bloc := f.read(1 << 20):
            h.update(bloc)
    return h.hexdigest()


def publication(version):
    """(étiquette, {nom du fichier: adresse}) de la publication : la dernière, ou celle de l'étiquette donnée."""
    try:
        with ouvrir(f"{API}/tags/{version}" if version else f"{API}/latest") as reponse:
            fiche = json.load(reponse)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"publication introuvable : {version or 'aucune base publiée'} (https://github.com/{DEPOT}/releases)")
        raise
    return fiche["tag_name"], {a["name"]: a["browser_download_url"] for a in fiche["assets"]}


def rapatrier(nom, adresses, dossier, attendu=None):
    """Télécharge un fichier de la publication dans le dossier, sauf s'il y est déjà avec la bonne empreinte."""
    chemin = dossier / nom
    if attendu and chemin.exists() and empreinte(chemin) == attendu:
        return chemin
    if nom not in adresses:
        sys.exit(f"la publication n'a pas de fichier {nom}")
    print(f"téléchargement : {nom}", flush=True)
    with ouvrir(adresses[nom]) as reponse, chemin.open("wb") as f:
        shutil.copyfileobj(reponse, f, 1 << 20)
    return chemin


class Recollees:
    """Les parties d'un fichier, lues bout à bout."""

    def __init__(self, chemins):
        self.restants, self.courant = list(chemins), None

    def read(self, taille=-1):
        while True:
            if self.courant is None:
                if not self.restants:
                    return b""
                self.courant = self.restants.pop(0).open("rb")
            lu = self.courant.read(taille)
            if lu:
                return lu
            self.courant.close()
            self.courant = None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--version", help="étiquette de la publication à télécharger ; la dernière à défaut")
    parser.add_argument("--depuis", type=pathlib.Path, help="dossier où se trouvent déjà les fichiers de la publication")
    parser.add_argument("--sortie", type=pathlib.Path, default=CONSTRUITE,
                        help="dossier où écrire la base (base/construite à défaut)")
    args = parser.parse_args()

    args.sortie.mkdir(parents=True, exist_ok=True)
    if args.depuis:
        dossier, adresses, etiquette = args.depuis, {}, str(args.depuis)
    else:
        dossier = args.sortie / "telechargement"
        dossier.mkdir(exist_ok=True)
        etiquette, adresses = publication(args.version)
        rapatrier("publication.json", adresses, dossier)
    if not (dossier / "publication.json").exists():
        sys.exit(f"{dossier} n'a pas de fichier publication.json")
    fiche = json.loads((dossier / "publication.json").read_text(encoding="utf-8"))

    parties = []
    for partie in fiche["parties"]:
        chemin = dossier / partie["nom"] if args.depuis else rapatrier(partie["nom"], adresses, dossier, partie["sha256"])
        if not chemin.exists():
            sys.exit(f"partie absente : {chemin}")
        if (chemin.stat().st_size, empreinte(chemin)) != (partie["octets"], partie["sha256"]):
            sys.exit(f"{partie['nom']} n'a pas l'empreinte qu'annonce la publication : téléchargement à refaire")
        parties.append(chemin)

    base, partielle = args.sortie / fiche["base"]["nom"], args.sortie / (fiche["base"]["nom"] + ".partiel")
    h, octets = hashlib.sha256(), 0
    with lzma.open(Recollees(parties)) as compressee, partielle.open("wb") as f:
        while bloc := compressee.read(1 << 22):
            f.write(bloc)
            h.update(bloc)
            octets += len(bloc)
    if (octets, h.hexdigest()) != (fiche["base"]["octets"], fiche["base"]["sha256"]):
        partielle.unlink()
        sys.exit("la base décompressée n'a pas l'empreinte qu'annonce la publication")
    partielle.replace(base)
    with (args.sortie / "empreintes.csv").open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=["table", "lignes", "sha256"], lineterminator="\n")
        ecrivain.writeheader()
        ecrivain.writerows(fiche["tables"])
    if not args.depuis:
        shutil.rmtree(dossier)
    chemin = base.relative_to(RACINE) if base.is_relative_to(RACINE) else base
    print(f"Base téléchargée : {chemin} ({octets / 1e9:.2f} Go, publication {etiquette}, commit "
          f"{fiche['commit'][:7] or 'inconnu'}), empreinte vérifiée.")


if __name__ == "__main__":
    main()
