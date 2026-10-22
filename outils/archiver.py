#!/usr/bin/env python3
"""Télécharge un fichier source, en archive une copie dans base/archives/ et l'inscrit
dans la table des fichiers avec son empreinte.

    python3 outils/archiver.py <source_id> "<url>"

Un fichier identique à une copie déjà archivée pour la même source n'est pas dupliqué.
"""

import argparse
import hashlib
import json
import sys
import urllib.request

from commun import AGENT, BASE, aujourdhui, champs, date_xlsx, ecrire, lire, maintenant


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source_id", help="identifiant de la source, déclaré dans tables/sources.csv")
    parser.add_argument("url", help="requête exacte à archiver")
    args = parser.parse_args()

    if args.source_id not in {s["id"] for s in lire("tables/sources.csv")}:
        sys.exit(f"source inconnue : {args.source_id} (la déclarer d'abord dans tables/sources.csv)")

    requete = urllib.request.Request(args.url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(requete, timeout=180) as reponse:
        contenu = reponse.read()
        type_contenu = reponse.headers.get_content_type()
    sha256 = hashlib.sha256(contenu).hexdigest()

    fichiers = lire("tables/fichiers.csv")
    deja = next((f for f in fichiers if f["sha256"] == sha256 and f["source_id"] == args.source_id), None)
    if deja:
        print(f"déjà archivé : {deja['id']}")
        return

    extension = ("json" if "json" in type_contenu else "xlsx" if "spreadsheetml" in type_contenu
                 else "csv" if "csv" in type_contenu else "bin")
    date = aujourdhui()
    chemin = f"archives/{args.source_id}/{date}-{sha256[:8]}.{extension}"
    (BASE / chemin).parent.mkdir(parents=True, exist_ok=True)
    (BASE / chemin).write_bytes(contenu)
    # Date de mise à jour annoncée par la source : champ « updated » du JSON-stat d'Eurostat,
    # date de modification inscrite dans le classeur pour un fichier xlsx.
    mis_a_jour = {"json": lambda: json.loads(contenu).get("updated", ""),
                  "xlsx": lambda: date_xlsx(BASE / chemin)}.get(extension, lambda: "")()

    identifiant = f"{args.source_id}@{date}-{sha256[:8]}"
    fichiers.append({"id": identifiant, "source_id": args.source_id, "url": args.url,
                     "telecharge_le": maintenant(), "mis_a_jour_source": mis_a_jour, "sha256": sha256,
                     "octets": len(contenu), "chemin": chemin})
    ecrire("tables/fichiers.csv", champs("fichiers"), fichiers)
    print(identifiant)


if __name__ == "__main__":
    main()
