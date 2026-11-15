#!/usr/bin/env python3
"""Cherche, chez chaque source, une version plus récente que sa copie archivée.

    python3 outils/surveiller.py [--rapport <fichier.md>] [--commandes] [--source <début d'identifiant>]…

Pour chaque adresse de la table des fichiers, compare ce que la source publie aujourd'hui à sa copie archivée la plus
récente. Pour un jeu de données d'un portail (data.ofgl.fr, data.economie.gouv.fr, data.drees), la date de
modification qu'annonce le portail est comparée à celle sous laquelle chaque copie a été archivée ou vérifiée, sans rien
télécharger ; une pièce jointe d'un jeu est à revoir si le jeu a été modifié depuis son téléchargement. Pour toute autre
adresse, le fichier est téléchargé de nouveau et son empreinte comparée à celle de la copie ; une réponse que le serveur
compose à chaque requête (séries SDMX, JSON-stat) est comparée sans l'heure qu'il y inscrit, une page HTML par son
texte, sans ses balises. Sont aussi signalés une
adresse qui n'existe plus, et, pour une série de jeux millésimés (« …-fichier-global-2025 »), un jeu d'un millésime
plus récent que ceux que la base a archivés.

Ce que l'outil ne voit pas : une nouvelle édition publiée à une nouvelle adresse (un tableau de l'Insee change
d'adresse à chaque campagne de comptes, une loi de finances est un nouveau texte).

L'outil ne modifie rien. Avec --rapport, il écrit ce qui a changé dans le fichier, qu'il supprime s'il n'y a rien à
signaler. Avec --commandes, il écrit les commandes qui archivent les nouvelles versions : `archiver.py` inscrit une copie
nouvelle, ou, si le contenu reçu est celui d'une copie déjà archivée, inscrit dans la table des vérifications que cette
copie est encore à jour à la date qu'annonce la source.

Une source qui ne répond pas n'arrête pas la veille : elle est nommée, et comptée. Lancé par GitHub, l'outil lui dit
aussi combien de sources sont à revoir et combien n'ont pas répondu (`a_revoir` et `sans_reponse`, dans le fichier que
désigne GITHUB_OUTPUT).
"""

import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse

from archiver import date_annoncee, telecharger
from commun import BASE, decoder_html, lire, morceaux, ouvrir_copie, texte_html

ESSAIS = 6  # une veille n'insiste pas autant qu'un archivage : une source muette aujourd'hui sera revue la prochaine fois
PAUSE = 0.5  # secondes entre deux requêtes à un même serveur

PORTAIL = re.compile(r"https://(data\.ofgl\.fr|data\.economie\.gouv\.fr|data\.drees\.solidarites-sante\.gouv\.fr)"
                     r"/api/(?:explore/v2\.1|v2)/catalog/datasets/([^/?]+)/(exports|attachments)/")
# Un jeu millésimé : « comptes-individuels-des-regions-fichier-global-2021-2024 », « …-2025 », et « …-20090 », que le
# portail nomme ainsi pour 2009.
MILLESIME = re.compile(r"(.+?)-((?:19|20)[0-9]{2})(?:-((?:19|20)[0-9]{2}))?0?")


def instant(texte):
    """La date que porte un texte, avec son fuseau (UTC à défaut) ; None s'il n'en porte pas."""
    try:
        date = datetime.datetime.fromisoformat(texte.replace("Z", "+00:00"))
    except ValueError:
        return None
    return date if date.tzinfo else date.replace(tzinfo=datetime.timezone.utc)


def dernieres_copies(fichiers):
    """Pour chaque adresse, sa copie archivée la plus récente."""
    copies = {}
    for f in fichiers:
        if f["url"] not in copies or f["telecharge_le"] > copies[f["url"]]["telecharge_le"]:
            copies[f["url"]] = f
    return copies


def date_connue(copie, verifications, jointe=False):
    """La date de la source sous laquelle une copie a été archivée, ou la plus récente sous laquelle elle a été
    vérifiée. Une pièce jointe ne porte pas la date de son jeu : la sienne est celle de son téléchargement."""
    dates = [copie["telecharge_le" if jointe else "mis_a_jour_source"]]
    dates += [v["mis_a_jour_source"] for v in verifications.get(copie["id"], [])]
    return max(filter(None, map(instant, dates)), default=None)


def options_archivage(copie):
    """Les options sous lesquelles la copie a été archivée : compressée, ou découpée."""
    if copie["chemin"].endswith(".bz2"):
        return " --compresser"
    return " --decouper" if morceaux(BASE / copie["chemin"]) else ""


def fiche_du_jeu(serveur, jeu):
    return json.loads(telecharger(f"https://{serveur}/api/explore/v2.1/catalog/datasets/{jeu}", ESSAIS)[0])


def jeux_de_la_serie(serveur, serie):
    """Les identifiants des jeux du portail dont le nom commence par celui de la série."""
    requete = urllib.parse.urlencode({"where": f'startswith(dataset_id, "{serie}-")', "select": "dataset_id",
                                      "limit": 100})
    reponse = json.loads(telecharger(f"https://{serveur}/api/explore/v2.1/catalog/datasets?{requete}", ESSAIS)[0])
    return sorted(r["dataset_id"] for r in reponse["results"])


def panne(erreur):
    """(disparue, texte) : une adresse que le serveur dit ne plus connaître, ou une source qui n'a pas répondu."""
    if isinstance(erreur, urllib.error.HTTPError):
        return erreur.code in (404, 410), f"erreur HTTP {erreur.code}"
    return False, f"sans réponse ({type(erreur).__name__})"


def surveiller_portail(serveur, copies, verifications):
    """Les constats sur les jeux d'un portail : jeux modifiés, pièces jointes à revoir, nouveaux millésimes."""
    constats = collections.defaultdict(list)
    par_jeu = collections.defaultdict(list)
    for copie in copies:
        par_jeu[PORTAIL.match(copie["url"]).group(2)].append(copie)
    for jeu, du_jeu in sorted(par_jeu.items()):
        time.sleep(PAUSE)
        try:
            # Pour un export, la date qu'inscrit l'archivage ; pour une pièce jointe, la date de modification du jeu.
            exports = [c for c in du_jeu if PORTAIL.match(c["url"]).group(3) == "exports"]
            jointes = [c for c in du_jeu if c not in exports]
            fiche = fiche_du_jeu(serveur, jeu)
            annoncee = instant(date_annoncee(serveur, fiche)) if exports else None
            modifie = instant(fiche["metas"]["default"]["modified"]) if jointes else None
        except Exception as e:  # une source muette n'arrête pas la veille des autres
            disparue, texte = panne(e)
            constats["disparues" if disparue else "muettes"].append((du_jeu[0]["source_id"],
                                                                     f"https://{serveur}/explore/dataset/{jeu}/", texte))
            continue
        depassees = [c for c in exports if annoncee and (date_connue(c, verifications) or annoncee) < annoncee]
        depassees += [c for c in jointes if modifie and date_connue(c, verifications, jointe=True) < modifie]
        if depassees:
            constats["jeux"].append({"source_id": du_jeu[0]["source_id"], "serveur": serveur, "jeu": jeu,
                                     "copies": depassees, "sur": len(du_jeu),
                                     "date": (annoncee or modifie).isoformat()})
    series = collections.defaultdict(set)
    for jeu in par_jeu:
        if trouve := MILLESIME.fullmatch(jeu):
            series[trouve.group(1)].add(jeu)
    for serie, connus in sorted(series.items()):
        time.sleep(PAUSE)
        try:
            publies = jeux_de_la_serie(serveur, serie)
        except Exception as e:
            constats["muettes"].append((par_jeu[min(connus)][0]["source_id"],
                                        f"https://{serveur}/explore/?q={serie}", panne(e)[1]))
            continue
        millesime = lambda j: max(filter(None, MILLESIME.fullmatch(j).groups()[1:]))
        dernier = max(millesime(j) for j in connus)
        for jeu in publies:
            if jeu not in connus and MILLESIME.fullmatch(jeu) and millesime(jeu) > dernier:
                constats["millesimes"].append((par_jeu[min(connus)][0]["source_id"], serveur, jeu))
    return constats


def contenu_utile(chemin, contenu):
    """Ce qui compte dans une réponse qu'un serveur compose à chaque requête : les séries SDMX de l'Insee sans leur
    en-tête, qui porte l'heure de la requête ; un jeu JSON-stat d'Eurostat sans sa date de mise à jour, qui change
    chaque fois que le jeu entier est recalculé, même si les chiffres demandés ne changent pas ; le texte d'une page
    HTML, sans ses balises, qu'un site change en changeant d'habillage."""
    if chemin.endswith(".html"):
        try:
            return texte_html(decoder_html(contenu)).encode()
        except (UnicodeDecodeError, LookupError):
            return contenu
    if chemin.endswith(".xml"):
        return re.sub(rb"<message:Header>.*?</message:Header>", b"", contenu, flags=re.S)
    if chemin.endswith(".json"):
        try:
            jeu = json.loads(contenu)
        except ValueError:
            return contenu
        if isinstance(jeu, dict):
            return json.dumps({c: jeu[c] for c in ("id", "size", "dimension", "value", "status") if c in jeu},
                              sort_keys=True).encode()
    return contenu


def surveiller_fichiers(copies):
    """Les constats sur les fichiers d'un serveur : contenu changé, adresse disparue."""
    constats = collections.defaultdict(list)
    for copie in copies:
        time.sleep(PAUSE)
        try:
            contenu, _ = telecharger(copie["url"], ESSAIS)
        except Exception as e:
            disparue, texte = panne(e)
            constats["disparues" if disparue else "muettes"].append((copie["source_id"], copie["url"], texte))
            continue
        empreinte = hashlib.sha256(contenu).hexdigest()
        if empreinte == copie["sha256"]:
            continue
        with ouvrir_copie(BASE / copie["chemin"]) as f:
            archive = f.read()
        if contenu_utile(copie["chemin"], contenu) != contenu_utile(copie["chemin"], archive):
            constats["fichiers"].append({"copie": copie, "sha256": empreinte, "octets": len(contenu)})
    return constats


def surveiller(copies, verifications):
    """Les constats sur toutes les copies, un serveur après l'autre dans chaque fil, les serveurs en même temps."""
    par_serveur = collections.defaultdict(list)
    for copie in copies:
        portail = PORTAIL.match(copie["url"])
        par_serveur[(portail.group(1), True) if portail else (urllib.parse.urlsplit(copie["url"]).netloc, False)] \
            .append(copie)
    constats = collections.defaultdict(list)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(par_serveur) or 1) as fils:
        taches = [fils.submit(surveiller_portail, serveur, du_serveur, verifications) if portail
                  else fils.submit(surveiller_fichiers, du_serveur)
                  for (serveur, portail), du_serveur in sorted(par_serveur.items())]
        for tache in taches:
            for nature, trouves in tache.result().items():
                constats[nature] += trouves
    return constats


def court(url, largeur=110):
    return url if len(url) <= largeur else url[:largeur - 1] + "…"


def rapport(constats, nombre):
    """Le rapport de ce qui a changé, en Markdown ; rien s'il n'y a rien à signaler."""
    if not any(constats[n] for n in ("jeux", "fichiers", "millesimes", "disparues")):
        return ""
    lignes = ["# Sources à revoir", "",
              f"`outils/surveiller.py` a comparé les {nombre} adresses archivées à ce que publient leurs sources. "
              "Une source qui a changé ne change rien à la base : ses copies archivées restent intactes, et la nouvelle "
              "version s'ajoute en l'archivant puis en l'important.", ""]
    if constats["jeux"]:
        lignes += ["## Jeux de données modifiés sur leur portail", "",
                   "Le portail annonce une date de modification plus récente que celle des copies archivées. Un jeu peut "
                   "avoir changé sans que chacun de ses exports ait changé : en archivant de nouveau, un export identique "
                   "à sa copie est seulement inscrit comme vérifié.", "",
                   "| Source | Jeu | Copies à revoir | Modifié le |", "|---|---|---|---|"]
        lignes += [f"| `{j['source_id']}` | [{j['jeu']}](https://{j['serveur']}/explore/dataset/{j['jeu']}/) | "
                   f"{len(j['copies'])} sur {j['sur']} | {j['date'][:10]} |"
                   for j in sorted(constats["jeux"], key=lambda j: (j["source_id"], j["jeu"]))]
        lignes.append("")
    if constats["fichiers"]:
        lignes += ["## Fichiers dont le contenu a changé", "",
                   "Le fichier reçu aujourd'hui n'a plus l'empreinte de sa copie archivée.", "",
                   "| Source | Adresse | Copie archivée | Octets archivés | Octets reçus |", "|---|---|---|---|---|"]
        lignes += [f"| `{f['copie']['source_id']}` | {court(f['copie']['url'])} | `{f['copie']['id']}` | "
                   f"{f['copie']['octets']} | {f['octets']} |"
                   for f in sorted(constats["fichiers"], key=lambda f: f["copie"]["id"])]
        lignes.append("")
    if constats["millesimes"]:
        lignes += ["## Nouveaux millésimes", "",
                   "Un jeu d'un millésime plus récent que ceux que la base a archivés dans la même série.", "",
                   "| Source | Jeu |", "|---|---|"]
        lignes += [f"| `{s}` | [{j}](https://{serveur}/explore/dataset/{j}/) |"
                   for s, serveur, j in sorted(constats["millesimes"])]
        lignes.append("")
    if constats["disparues"]:
        lignes += ["## Adresses qui n'existent plus", "",
                   "La source ne publie plus rien à cette adresse : la copie archivée reste la preuve du chiffre, et la "
                   "nouvelle adresse est à chercher.", "", "| Source | Adresse | Réponse |", "|---|---|---|"]
        lignes += [f"| `{s}` | {court(u)} | {t} |" for s, u, t in sorted(constats["disparues"])]
        lignes.append("")
    lignes += ["## Pour mettre la base à jour", "", "```sh",
               "python3 outils/surveiller.py --commandes > a_archiver.sh   # les commandes d'archivage",
               "sh a_archiver.sh                                           # archive ce qui a changé, vérifie le reste",
               "```", "",
               "Chaque nouvelle copie s'importe ensuite avec l'importateur de sa source (voir `base/README.md`), puis "
               "`python3 outils/valider.py` et `python3 outils/controler_coherence.py`."]
    return "\n".join(lignes) + "\n"


def commandes(constats):
    """Les commandes qui archivent ce qui a changé : une par source et par façon d'archiver, dans l'ordre des sources."""
    a_archiver = collections.defaultdict(list)
    for copie in [c for j in constats["jeux"] for c in j["copies"]] + [f["copie"] for f in constats["fichiers"]]:
        a_archiver[(copie["source_id"], options_archivage(copie))].append(copie["url"])
    return [f"python3 outils/archiver.py {source}{options} " + " ".join(f"'{u}'" for u in sorted(urls))
            for (source, options), urls in sorted(a_archiver.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--rapport", type=pathlib.Path, help="fichier où écrire ce qui a changé, supprimé s'il n'y a rien")
    parser.add_argument("--commandes", action="store_true", help="écrire les commandes d'archivage de ce qui a changé")
    parser.add_argument("--source", action="append", default=[], metavar="début",
                        help="ne surveiller que les sources dont l'identifiant commence ainsi (« ofgl. », « insee.t32 »)")
    args = parser.parse_args()

    copies = [c for c in dernieres_copies(lire("tables/fichiers.csv")).values()
              if not args.source or c["source_id"].startswith(tuple(args.source))]
    verifications = collections.defaultdict(list)
    for v in lire("tables/verifications.csv"):
        verifications[v["fichier_id"]].append(v)
    constats = surveiller(copies, verifications)

    texte = rapport(constats, len(copies))
    if args.rapport:
        if texte:
            args.rapport.write_text(texte, encoding="utf-8")
        else:
            args.rapport.unlink(missing_ok=True)
    if args.commandes:
        print("\n".join(commandes(constats)))
    journal = sys.stderr if args.commandes else sys.stdout
    for source, url, raison in sorted(constats["muettes"]):
        print(f"sans réponse : {source} {url} ({raison})", file=journal)
    print(f"{len(copies)} adresses comparées : {len(constats['jeux'])} jeux de données modifiés, "
          f"{len(constats['fichiers'])} fichiers changés, {len(constats['millesimes'])} nouveaux millésimes, "
          f"{len(constats['disparues'])} adresses disparues, {len(constats['muettes'])} sources sans réponse.",
          file=journal)
    if texte and not args.rapport and not args.commandes:
        print("\n" + texte, end="")
    if os.environ.get("GITHUB_OUTPUT"):
        a_revoir = sum(len(constats[n]) for n in ("jeux", "fichiers", "millesimes", "disparues"))
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"a_revoir={a_revoir}\nsans_reponse={len(constats['muettes'])}\n")


if __name__ == "__main__":
    main()
