#!/usr/bin/env python3
"""Télécharge des fichiers d'une source, en archive une copie dans base/archives/ et les inscrit
dans la table des fichiers avec leur empreinte.

    python3 outils/archiver.py <source_id> "<url>" ["<url>"…] [--compresser] [--decouper]

Un fichier identique à une copie déjà archivée pour la même source n'est pas dupliqué. Avec
--compresser, pour un gros fichier, la copie est enregistrée compressée (bzip2) : son empreinte et
sa taille restent celles du contenu reçu, que le contrôle retrouve en la décompressant. Avec --decouper, un
fichier trop gros pour le dépôt (GitHub refuse les fichiers de plus de 100 Mo) est enregistré en morceaux
(« .partie01 », « .partie02 »…), que la lecture recolle : son empreinte et sa taille restent celles du
contenu reçu. Une connexion
coupée avant la fin du téléchargement est réessayée ; une erreur renvoyée par le serveur ne l'est pas.
Pour un export de data.ofgl.fr, la date de modification du jeu de données est lue avant son premier
fichier et après chacun : si elle change, l'archivage s'arrête, et les fichiers déjà inscrits gardent
la date sous laquelle ils ont été téléchargés. Plusieurs archivages peuvent tourner en même temps :
chacun inscrit ses copies dans la table des fichiers à son tour.
"""

import argparse
import bz2
import fcntl
import gzip
import hashlib
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.request

from commun import (AGENT, BASE, TAILLE_MORCEAU, aujourdhui, champs, date_html, date_pdf, date_xlsx, date_zip, ecrire, lire,
                    lire_sdmx, maintenant, texte_html)

ESSAIS = 80  # certains portails ne répondent qu'à une tentative de connexion sur plusieurs


def telecharger(url):
    """(contenu, type de contenu). Le transfert peut être compressé (gzip) : le contenu est celui qu'il porte."""
    for essai in range(1, ESSAIS + 1):
        try:
            requete = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(requete, timeout=300) as reponse:
                recu = reponse.read()
                attendu = reponse.headers.get("Content-Length")
                if attendu is not None and int(attendu) != len(recu):
                    raise http.client.IncompleteRead(recu, int(attendu) - len(recu))
                contenu = gzip.decompress(recu) if reponse.headers.get("Content-Encoding") == "gzip" else recu
                return contenu, reponse.headers.get_content_type()
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, http.client.HTTPException, ConnectionError, TimeoutError, EOFError,
                gzip.BadGzipFile) as e:
            if essai == ESSAIS:
                raise
            print(f"essai {essai} : connexion coupée ({type(e).__name__}) ; nouvel essai", file=sys.stderr)
            time.sleep(5)


def date_ofgl(url):
    """Pour un export de data.ofgl.fr, la date de modification du jeu de données qu'annonce le portail."""
    jeu = re.match(r"https://data\.ofgl\.fr/api/explore/v2\.1/catalog/datasets/([^/]+)/exports/", url)
    if jeu is None:
        return ""
    fiche = json.loads(telecharger(f"https://data.ofgl.fr/api/explore/v2.1/catalog/datasets/{jeu.group(1)}")[0])
    return fiche["metas"]["default"]["modified"]


def archiver(source_id, url, contenu, type_contenu, mis_a_jour, compresser, decouper):
    """Inscrit une copie dans la table des fichiers ; renvoie son identifiant. La table reste verrouillée de sa
    lecture à son écriture, pour qu'un autre archivage n'y efface pas cette inscription."""
    with (BASE / "tables" / "fichiers.csv").open("a") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        return inscrire(source_id, url, contenu, type_contenu, mis_a_jour, compresser, decouper)


def inscrire(source_id, url, contenu, type_contenu, mis_a_jour, compresser, decouper):
    sha256 = hashlib.sha256(contenu).hexdigest()
    fichiers = lire("tables/fichiers.csv")
    deja = next((f for f in fichiers if f["sha256"] == sha256 and f["source_id"] == source_id), None)
    if deja:
        return f"déjà archivé : {deja['id']}"
    extension = ("json" if "json" in type_contenu else "xlsx" if "spreadsheetml" in type_contenu
                 else "csv" if "csv" in type_contenu else "html" if "html" in type_contenu
                 else "xml" if "xml" in type_contenu else "zip" if "zip" in type_contenu
                 else "pdf" if "pdf" in type_contenu else "bin")
    if compresser and extension != "csv":
        sys.exit("seul un fichier csv s'archive compressé")
    if compresser and decouper:
        sys.exit("une copie s'archive compressée ou découpée, pas les deux")
    date = aujourdhui()
    chemin = f"archives/{source_id}/{date}-{sha256[:8]}.{extension}" + (".bz2" if compresser else "")
    (BASE / chemin).parent.mkdir(parents=True, exist_ok=True)
    if decouper and len(contenu) > TAILLE_MORCEAU:
        for k in range(0, len(contenu), TAILLE_MORCEAU):
            (BASE / f"{chemin}.partie{k // TAILLE_MORCEAU + 1:02d}").write_bytes(contenu[k:k + TAILLE_MORCEAU])
    else:
        (BASE / chemin).write_bytes(bz2.compress(contenu, 9) if compresser else contenu)
    # Date de mise à jour annoncée par la source : champ « updated » du JSON-stat d'Eurostat, date de
    # modification inscrite dans le classeur pour un fichier xlsx, date d'enregistrement, de transmission ou
    # d'adoption d'un texte publié par le Sénat, dernière mise à jour des séries SDMX de l'Insee, date de
    # modification du jeu de données pour un export de data.ofgl.fr, date la plus récente des fichiers que porte une
    # archive zip, date de modification inscrite dans un PDF.
    mis_a_jour = mis_a_jour or {"json": lambda: json.loads(contenu).get("updated", ""),
                                "xlsx": lambda: date_xlsx(BASE / chemin),
                                "html": lambda: date_html(texte_html(contenu.decode("utf-8"))),
                                "xml": lambda: max(a.get("LAST_UPDATE", "") for a, _ in lire_sdmx(BASE / chemin).values()),
                                "zip": lambda: date_zip(contenu),
                                "pdf": lambda: date_pdf(contenu)
                                }.get(extension, lambda: "")()
    identifiant = f"{source_id}@{date}-{sha256[:8]}"
    fichiers.append({"id": identifiant, "source_id": source_id, "url": url, "telecharge_le": maintenant(),
                     "mis_a_jour_source": mis_a_jour, "sha256": sha256, "octets": len(contenu), "chemin": chemin})
    ecrire("tables/fichiers.csv", champs("fichiers"), fichiers)
    return identifiant


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source_id", help="identifiant de la source, déclaré dans tables/sources.csv")
    parser.add_argument("urls", nargs="+", metavar="url", help="requête exacte à archiver")
    parser.add_argument("--compresser", action="store_true", help="archiver les copies compressées (bzip2)")
    parser.add_argument("--decouper", action="store_true", help="archiver en morceaux une copie trop grosse pour le dépôt")
    args = parser.parse_args()

    if args.source_id not in {s["id"] for s in lire("tables/sources.csv")}:
        sys.exit(f"source inconnue : {args.source_id} (la déclarer d'abord dans tables/sources.csv)")

    dates = {}  # jeu de données de data.ofgl.fr → date de modification lue avant son premier fichier
    for url in args.urls:
        jeu = url.split("/exports/")[0]
        if jeu not in dates:
            dates[jeu] = date_ofgl(url)
        contenu, type_contenu = telecharger(url)
        if date_ofgl(url) != dates[jeu]:
            sys.exit(f"le jeu de données a été modifié pendant le téléchargement de {url} : recommencer")
        print(archiver(args.source_id, url, contenu, type_contenu, dates[jeu], args.compresser, args.decouper), flush=True)


if __name__ == "__main__":
    main()
