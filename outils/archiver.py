#!/usr/bin/env python3
"""Télécharge des fichiers d'une source, en archive une copie dans base/archives/ et les inscrit
dans la table des fichiers avec leur empreinte.

    python3 outils/archiver.py <source_id> "<url>" ["<url>"…] [--compresser] [--decouper]
    python3 outils/archiver.py <source_id> "<url>" --depose <chemin>

Avec --depose, la copie n'est pas téléchargée : c'est un fichier qu'une personne a téléchargé à la main à l'adresse
donnée, sur un site qui refuse les robots (budget.gouv.fr), puis déposé dans le dépôt par un commit. Sa date de
téléchargement est celle de ce commit, que garde l'historique du dépôt.

Un fichier identique à une copie déjà archivée pour la même source n'est pas dupliqué. Avec
--compresser, pour un gros fichier, la copie est enregistrée compressée (bzip2) : son empreinte et
sa taille restent celles du contenu reçu, que le contrôle retrouve en la décompressant. Avec --decouper, un
fichier trop gros pour le dépôt (GitHub refuse les fichiers de plus de 100 Mo) est enregistré en morceaux
(« .partie01 », « .partie02 »…), que la lecture recolle : son empreinte et sa taille restent celles du
contenu reçu. Une connexion
coupée avant la fin du téléchargement est réessayée ; une erreur renvoyée par le serveur ne l'est pas.
Pour un export de data.ofgl.fr, de data.economie.gouv.fr ou de data.drees, la date de modification du jeu de données
est lue avant son premier fichier et après chacun : si elle change, l'archivage s'arrête, et les fichiers déjà
inscrits gardent la date sous laquelle ils ont été téléchargés. La DREES ne change pas la date de modification de ses
jeux quand leurs données changent : pour data.drees, la date retenue est celle du dernier traitement des données.
Plusieurs archivages peuvent tourner en même temps : chacun inscrit ses copies dans la table des fichiers à son tour.
"""

import argparse
import bz2
import datetime
import fcntl
import gzip
import hashlib
import http.client
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

from commun import (AGENT, BASE, TAILLE_MORCEAU, aujourdhui, champs, date_html, date_ods, date_pdf, date_xlsx, date_zip,
                    decoder_html, ecrire, lire, lire_pdf, lire_sdmx, maintenant, texte_html, texte_pdf)

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


def date_portail(url):
    """Pour un export de data.ofgl.fr ou de data.economie.gouv.fr, la date de modification du jeu de données
    qu'annonce le portail ; pour un export de data.drees, la date du dernier traitement de ses données."""
    jeu = re.match(r"(https://(data\.ofgl\.fr|data\.economie\.gouv\.fr|data\.drees\.solidarites-sante\.gouv\.fr)"
                   r"/api/explore/v2\.1/catalog/datasets/[^/]+)/exports/", url)
    if jeu is None:
        return ""
    fiche = json.loads(telecharger(jeu.group(1))[0])["metas"]["default"]
    return fiche["data_processed"] if jeu.group(2).startswith("data.drees") else fiche["modified"]


# Type de contenu d'un fichier déposé à la main, d'après son extension.
TYPES_DEPOSES = {"pdf": "application/pdf", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                 "ods": "application/vnd.oasis.opendocument.spreadsheet", "csv": "text/csv", "zip": "application/zip"}


def depot(chemin):
    """(contenu, type de contenu, heure du commit qui l'a déposé, en UTC) d'un fichier déposé à la main dans le dépôt."""
    extension = chemin.rsplit(".", 1)[-1].lower()
    if extension not in TYPES_DEPOSES:
        sys.exit(f"{chemin} : extension inconnue (attendu : {', '.join(TYPES_DEPOSES)})")
    if subprocess.run(["git", "status", "--porcelain", "--", chemin], capture_output=True, text=True,
                      check=True).stdout.strip():
        sys.exit(f"{chemin} : fichier modifié ou absent de l'historique ; il doit être tel que l'a déposé son commit")
    heures = subprocess.run(["git", "log", "--format=%aI", "--", chemin], capture_output=True, text=True,
                            check=True).stdout.split()
    ajouts = subprocess.run(["git", "log", "--diff-filter=A", "--format=%aI", "--", chemin], capture_output=True,
                            text=True, check=True).stdout.split()
    if len(heures) != 1 or ajouts != heures:
        sys.exit(f"{chemin} : {len(heures)} commits le touchent dans l'historique ; il en faut un, celui qui l'ajoute")
    heure = datetime.datetime.fromisoformat(heures[0]).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(chemin, "rb") as f:
        return f.read(), TYPES_DEPOSES[extension], heure


def archiver(source_id, url, contenu, type_contenu, mis_a_jour, compresser, decouper, telecharge_le=None):
    """Inscrit une copie dans la table des fichiers ; renvoie son identifiant. La table reste verrouillée de sa
    lecture à son écriture, pour qu'un autre archivage n'y efface pas cette inscription."""
    with (BASE / "tables" / "fichiers.csv").open("a") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        return inscrire(source_id, url, contenu, type_contenu, mis_a_jour, compresser, decouper, telecharge_le)


def inscrire(source_id, url, contenu, type_contenu, mis_a_jour, compresser, decouper, telecharge_le=None):
    sha256 = hashlib.sha256(contenu).hexdigest()
    fichiers = lire("tables/fichiers.csv")
    deja = next((f for f in fichiers if f["sha256"] == sha256 and f["source_id"] == source_id), None)
    if deja:
        return f"déjà archivé : {deja['id']}"
    extension = ("json" if "json" in type_contenu else "xlsx" if "spreadsheetml" in type_contenu
                 else "ods" if "opendocument.spreadsheet" in type_contenu
                 else "csv" if "csv" in type_contenu else "html" if "html" in type_contenu
                 else "xml" if "xml" in type_contenu else "zip" if "zip" in type_contenu
                 else "pdf" if "pdf" in type_contenu else "bin")
    # Un serveur qui envoie un type générique (« application/octet-stream ») : l'extension est celle de l'adresse,
    # quand c'est l'une des précédentes.
    connue = re.search(r"\.(json|xlsx|ods|csv|html|xml|zip|pdf)$", url.split("?")[0])
    if extension == "bin" and type_contenu == "application/octet-stream" and connue:
        extension = connue.group(1)
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
    # d'adoption d'un texte publié par le Sénat ou par l'Assemblée nationale, dernière mise à jour des séries SDMX
    # de l'Insee, date de modification du jeu de données pour un export de data.ofgl.fr ou de data.economie.gouv.fr
    # (date du dernier traitement de ses données pour data.drees), date la plus récente des fichiers que porte une
    # archive zip, date de modification inscrite dans un classeur ods ; pour un PDF, la date que porte le texte d'un
    # document du Sénat ou de l'Assemblée nationale, comme pour leurs pages, à défaut sa date de modification.
    mis_a_jour = mis_a_jour or {"json": lambda: json.loads(contenu).get("updated", ""),
                                "xlsx": lambda: date_xlsx(BASE / chemin),
                                "html": lambda: date_html(texte_html(decoder_html(contenu))),
                                "xml": lambda: max(a.get("LAST_UPDATE", "") for a, _ in lire_sdmx(BASE / chemin).values()),
                                "zip": lambda: date_zip(contenu),
                                "pdf": lambda: date_html(" ".join(texte_pdf(m) for page in lire_pdf(BASE / chemin)
                                                                  for _, m in page)) or date_pdf(contenu),
                                "ods": lambda: date_ods(BASE / chemin)
                                }.get(extension, lambda: "")()
    identifiant = f"{source_id}@{date}-{sha256[:8]}"
    fichiers.append({"id": identifiant, "source_id": source_id, "url": url, "telecharge_le": telecharge_le or maintenant(),
                     "mis_a_jour_source": mis_a_jour, "sha256": sha256, "octets": len(contenu), "chemin": chemin})
    ecrire("tables/fichiers.csv", champs("fichiers"), fichiers)
    return identifiant


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source_id", help="identifiant de la source, déclaré dans tables/sources.csv")
    parser.add_argument("urls", nargs="+", metavar="url", help="requête exacte à archiver")
    parser.add_argument("--compresser", action="store_true", help="archiver les copies compressées (bzip2)")
    parser.add_argument("--decouper", action="store_true", help="archiver en morceaux une copie trop grosse pour le dépôt")
    parser.add_argument("--depose", metavar="chemin", help="fichier téléchargé à la main à l'adresse donnée et déposé "
                                                          "dans le dépôt par un commit, à archiver tel quel")
    args = parser.parse_args()

    if args.source_id not in {s["id"] for s in lire("tables/sources.csv")}:
        sys.exit(f"source inconnue : {args.source_id} (la déclarer d'abord dans tables/sources.csv)")
    if args.depose:
        if len(args.urls) != 1:
            sys.exit("--depose : une seule adresse, celle d'où vient le fichier déposé")
        contenu, type_contenu, heure = depot(args.depose)
        print(archiver(args.source_id, args.urls[0], contenu, type_contenu, "", args.compresser, args.decouper, heure))
        return

    dates = {}  # jeu de données d'un portail → date de modification lue avant le premier de ses exports
    for url in args.urls:
        jeu = url.split("/exports/")[0] if "/exports/" in url else None  # la fiche d'un jeu n'est pas un export
        if jeu is not None and jeu not in dates:
            dates[jeu] = date_portail(url)
        contenu, type_contenu = telecharger(url)
        if jeu is not None and date_portail(url) != dates[jeu]:
            sys.exit(f"le jeu de données a été modifié pendant le téléchargement de {url} : recommencer")
        print(archiver(args.source_id, url, contenu, type_contenu, dates.get(jeu, ""), args.compresser, args.decouper),
              flush=True)


if __name__ == "__main__":
    main()
