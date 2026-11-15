#!/usr/bin/env python3
"""Prépare la base construite pour sa publication : compressée, découpée, avec ses empreintes.

    python3 outils/publier.py

À lancer après `construire.py`. Écrit dans base/publication/ ce qu'une « Release » de GitHub publie :

- la base SQLite compressée (xz), en parties de moins de 2 Go, la limite d'un fichier de « Release » :
  `comptes.sqlite.xz.partie01`, `comptes.sqlite.xz.partie02`… ; mises bout à bout, elles font un fichier xz ordinaire
  (`cat comptes.sqlite.xz.partie* | xz -d > comptes.sqlite`) ;
- `empreintes.csv`, l'empreinte du contenu de chaque table, à comparer à celle d'une base reconstruite ;
- `publication.json`, la fiche de la publication : son étiquette (« base-2026-11-12-e8d2dff » : le jour et le commit
  du dépôt dont vient la base), la taille et l'empreinte de la base et de chaque partie ;
- `notes.md`, le texte qui accompagne la publication.

`telecharger.py` fait le chemin inverse et vérifie chaque empreinte.
"""

import concurrent.futures
import hashlib
import json
import lzma
import os
import shutil
import subprocess

from commun import BASE, DEPOT, RACINE, aujourdhui, lire, maintenant

CONSTRUITE = BASE / "construite"
SORTIE = BASE / "publication"
NOM = "comptes.sqlite"
# La base est compressée par blocs, chacun à part : plusieurs à la fois, sur tous les processeurs. Les blocs compressés,
# mis bout à bout, font un fichier xz ordinaire, que `xz` et Python décompressent d'une traite.
BLOC = 32 << 20
PARTIE = 1_900_000_000  # GitHub refuse un fichier de « Release » de 2 Go ou plus
NIVEAU = 1  # au-delà, la compression prend plusieurs fois plus de temps pour quelques pour cent de moins


def compresser(bloc):
    return lzma.compress(bloc, preset=NIVEAU)


def blocs(chemin, empreinte):
    with chemin.open("rb") as f:
        while bloc := f.read(BLOC):
            empreinte.update(bloc)
            yield bloc


class Parties:
    """Écrit un flux en parties de PARTIE octets au plus, et retient la taille et l'empreinte de chacune."""

    def __init__(self, dossier, nom):
        self.dossier, self.nom, self.ecrites, self.fichier = dossier, nom, [], None

    def ecrire(self, octets):
        vue = memoryview(octets)
        while len(vue):
            if self.fichier is None or self.ecrites[-1]["octets"] == PARTIE:
                self.fermer()
                nom = f"{self.nom}.partie{len(self.ecrites) + 1:02d}"
                self.fichier, self.empreinte = (self.dossier / nom).open("wb"), hashlib.sha256()
                self.ecrites.append({"nom": nom, "octets": 0})
            morceau = vue[:PARTIE - self.ecrites[-1]["octets"]]
            self.fichier.write(morceau)
            self.empreinte.update(morceau)
            self.ecrites[-1]["octets"] += len(morceau)
            vue = vue[len(morceau):]

    def fermer(self):
        if self.fichier is not None:
            self.fichier.close()
            self.ecrites[-1]["sha256"] = self.empreinte.hexdigest()
            self.fichier = None


def commit():
    """Le commit du dépôt dont vient la base, s'il se laisse lire."""
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE, capture_output=True, text=True,
                              check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return os.environ.get("GITHUB_SHA", "")


def notes(fiche, compressee, chiffres):
    """Le texte qui accompagne la publication : ce qu'elle contient, comment la télécharger et la vérifier."""
    go = lambda octets: f"{octets / 1e9:.2f}".replace(".", ",") + " Go"
    lignes = [f"La base SQLite construite au commit [`{fiche['commit'][:7]}`](https://github.com/{DEPOT}/tree/"
              f"{fiche['commit']}) : {format(chiffres, ',').replace(',', ' ')} chiffres et {len(fiche['tables'])} tables, "
              f"{go(fiche['base']['octets'])} "
              f"une fois décompressée ({go(compressee)} à télécharger).", "",
              "## Télécharger", "", "Avec l'outil du dépôt, qui vérifie chaque empreinte :", "",
              "```sh", f"python3 outils/telecharger.py --version {fiche['etiquette']}", "```", "",
              "Ou à la main, en téléchargeant chaque partie ci-dessous :", "",
              "```sh", f"cat {NOM}.xz.partie* | xz -d > {NOM}", f"sha256sum {NOM}   # {fiche['base']['sha256']}", "```",
              "", "## Vérifier", "",
              "`empreintes.csv` donne l'empreinte du contenu de chaque table. Reconstruire la base au même commit "
              "(`python3 outils/construire.py`) écrit le même fichier dans `base/construite/` : les deux se comparent "
              "ligne à ligne.", "",
              "| Fichier | Octets | SHA-256 |", "|---|---:|---|"]
    lignes += [f"| `{p['nom']}` | {p['octets']} | `{p['sha256']}` |" for p in fiche["parties"]]
    return "\n".join(lignes) + "\n"


def main():
    base = CONSTRUITE / NOM
    if not base.exists() or not (CONSTRUITE / "empreintes.csv").exists():
        raise SystemExit("base non construite : lancer d'abord python3 outils/construire.py")
    shutil.rmtree(SORTIE, ignore_errors=True)
    SORTIE.mkdir(parents=True)
    empreinte, parties = hashlib.sha256(), Parties(SORTIE, NOM + ".xz")
    with concurrent.futures.ProcessPoolExecutor() as processus:
        # Les blocs sont compressés en même temps et écrits dans l'ordre ; pas plus de blocs en mémoire que deux par
        # processeur.
        en_cours, attente = [], 2 * (os.cpu_count() or 1)
        for bloc in blocs(base, empreinte):
            en_cours.append(processus.submit(compresser, bloc))
            if len(en_cours) >= attente:
                parties.ecrire(en_cours.pop(0).result())
        for tache in en_cours:
            parties.ecrire(tache.result())
    parties.fermer()
    shutil.copyfile(CONSTRUITE / "empreintes.csv", SORTIE / "empreintes.csv")
    jour, origine = aujourdhui(), commit()
    etiquette = f"base-{jour}" + (f"-{origine[:7]}" if origine else "")
    fiche = {"depot": DEPOT, "etiquette": etiquette, "titre": f"Base du {jour}", "commit": origine,
             "preparee_le": maintenant(),
             "base": {"nom": NOM, "octets": base.stat().st_size, "sha256": empreinte.hexdigest()},
             "compression": "xz", "parties": parties.ecrites,
             "tables": [{"table": e["table"], "lignes": int(e["lignes"]), "sha256": e["sha256"]}
                        for e in lire(CONSTRUITE / "empreintes.csv")]}
    (SORTIE / "publication.json").write_text(json.dumps(fiche, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    compressee = sum(p["octets"] for p in parties.ecrites)
    chiffres = next((t["lignes"] for t in fiche["tables"] if t["table"] == "chiffres"), 0)
    (SORTIE / "notes.md").write_text(notes(fiche, compressee, chiffres), encoding="utf-8")
    print(f"Publication prête : {SORTIE.relative_to(RACINE)}, {len(parties.ecrites)} partie(s), "
          f"{compressee / 1e9:.2f} Go compressés pour {fiche['base']['octets'] / 1e9:.2f} Go.")


if __name__ == "__main__":
    main()
