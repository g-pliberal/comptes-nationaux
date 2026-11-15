#!/usr/bin/env python3
"""Range dans les « Releases » du dépôt GitHub les copies archivées trop grosses pour le dépôt lui-même.

    python3 outils/ranger.py            # sur GitHub, avec les variables GH_TOKEN et GH_REPO

Une copie archivée avec `archiver.py --release` est inscrite dans la table des fichiers sous le chemin
« releases/<étiquette>/<nom> » : son fichier doit être joint, sous ce nom, à la Release de cette étiquette. Pour chaque
copie qui n'y est pas encore, l'outil la reprend dans base/releases/ si elle y est (sur la machine qui l'a archivée), et
sinon la télécharge de nouveau à son adresse d'origine ; il vérifie qu'elle a l'empreinte et la taille inscrites, puis la
joint à la Release, qu'il crée au besoin (sans en faire la dernière publication de la base). Un fichier déjà joint doit
avoir la taille inscrite. Si la source a changé depuis l'archivage, l'empreinte ne correspond plus : l'outil s'arrête,
et la copie est à archiver de nouveau.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

from archiver import telecharger
from commun import BASE, DEPOT, RELEASES, lire

NOTES = ("Copies archivées des sources trop grosses pour le dépôt (les balances comptables des communes, des groupements "
         "à fiscalité propre, des syndicats et des établissements publics locaux), telles que reçues. La table "
         "base/tables/fichiers.csv donne, pour chacune, son adresse d'origine, sa date de téléchargement, son empreinte "
         "SHA-256 et sa taille. Ce n'est pas une publication de la base.")


def gh(*arguments, verifier=True):
    return subprocess.run(["gh", *arguments], capture_output=True, text=True, check=verifier)


def joints(etiquette, depot):
    """{nom: taille} des fichiers joints à la Release, None si elle n'existe pas."""
    reponse = gh("api", f"repos/{depot}/releases/tags/{etiquette}", verifier=False)
    if reponse.returncode != 0:
        if "Not Found" in reponse.stdout + reponse.stderr:
            return None
        sys.exit(f"Release {etiquette} illisible : {reponse.stderr.strip()}")
    fiche = json.loads(reponse.stdout)
    resultat = {a["name"]: a["size"] for a in fiche["assets"]}
    page = 2
    while len(resultat) == 100 * (page - 1):  # l'API donne les fichiers joints par pages de cent
        suite = json.loads(gh("api", f"repos/{depot}/releases/{fiche['id']}/assets?per_page=100&page={page}").stdout)
        resultat.update({a["name"]: a["size"] for a in suite})
        page += 1
    return resultat


def contenu_verifie(copie):
    """Le contenu d'une copie, repris de base/releases/ ou téléchargé de nouveau, après vérification de son empreinte et
    de sa taille."""
    local = BASE / copie["chemin"]
    contenu = local.read_bytes() if local.exists() else telecharger(copie["url"])[0]
    if hashlib.sha256(contenu).hexdigest() != copie["sha256"] or len(contenu) != int(copie["octets"]):
        sys.exit(f"{copie['id']} : le fichier de {copie['url']} n'a plus l'empreinte ni la taille inscrites ; la source "
                 f"l'a changé depuis l'archivage : l'archiver de nouveau")
    return contenu


def main():
    depot = os.environ.get("GH_REPO") or DEPOT
    copies = [f for f in lire("tables/fichiers.csv") if f["chemin"].startswith(RELEASES + "/")]
    par_etiquette = {}
    for copie in copies:
        _, etiquette, nom = copie["chemin"].split("/")
        par_etiquette.setdefault(etiquette, []).append((nom, copie))
    for etiquette, liste in sorted(par_etiquette.items()):
        presents = joints(etiquette, depot)
        if presents is None:
            gh("release", "create", etiquette, "--repo", depot, "--title", "Copies archivées des grosses sources",
               "--notes", NOTES, "--latest=false")
            presents = {}
        rangees = 0
        for nom, copie in sorted(liste):
            if nom in presents:
                if presents[nom] != int(copie["octets"]):
                    sys.exit(f"{copie['id']} : le fichier joint {nom} fait {presents[nom]} octets, la table en inscrit "
                             f"{copie['octets']}")
                continue
            contenu = contenu_verifie(copie)
            with tempfile.TemporaryDirectory() as dossier:
                chemin = os.path.join(dossier, nom)
                with open(chemin, "wb") as f:
                    f.write(contenu)
                for _ in range(3):
                    envoi = gh("release", "upload", etiquette, chemin, "--repo", depot, verifier=False)
                    if envoi.returncode == 0 or (joints(etiquette, depot) or {}).get(nom) == int(copie["octets"]):
                        break
            if envoi.returncode != 0:
                # Deux contrôles qui tournent en même temps (une modification et sa demande de fusion) peuvent joindre
                # le même fichier : il suffit qu'il y soit, entier.
                if (joints(etiquette, depot) or {}).get(nom) != int(copie["octets"]):
                    sys.exit(f"{copie['id']} : envoi impossible ({envoi.stderr.strip()})")
            rangees += 1
            print(f"{copie['id']} : joint à la Release {etiquette} ({nom})", flush=True)
        print(f"Release {etiquette} : {len(liste)} copies, dont {rangees} jointes maintenant.")


if __name__ == "__main__":
    main()
