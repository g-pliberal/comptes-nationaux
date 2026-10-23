#!/usr/bin/env python3
"""Construit la base SQLite interrogeable à partir des tables texte.

    python3 outils/construire.py

Écrit base/construite/comptes.sqlite, à ouvrir avec n'importe quel outil SQLite, et
base/construite/empreintes.csv : une empreinte du contenu de chaque table, qui permet à
chacun de vérifier qu'une base reconstruite contient exactement les mêmes données. Les comptes
de chaque collectivité y sont lus dans les copies archivées des exports de data.ofgl.fr
(tables comptes_collectivites et collectivites).
"""

import csv
import hashlib
import io
import sqlite3

import importer_ofgl_collectivites as ofgl
from commun import BASE, lire, paquet

SORTIE = BASE / "construite"
TYPES_SQL = {"integer": "INTEGER", "number": "REAL"}

VUES = """
CREATE VIEW v_chiffres AS
SELECT c.*, s.producteur, s.titre AS source_titre, co.libelle AS concept_libelle,
       p.libelle AS perimetre_libelle, f.libelle AS fonction_libelle, u.libelle AS unite_libelle
FROM chiffres c
JOIN sources s ON s.id = c.source_id
JOIN concepts co ON co.id = c.concept_id
JOIN perimetres p ON p.id = c.perimetre_id
JOIN unites u ON u.id = c.unite_id
LEFT JOIN fonctions f ON f.id = c.fonction_id;

-- Les comptes de chaque collectivité, dans la version la plus récente de chaque exercice, avec le nom, le territoire et
-- la population de la collectivité.
CREATE VIEW v_comptes_collectivites AS
SELECT c.*, k.insee, k.insee_2025, k.nom, k.categorie, k.nature_juridique, k.departement, k.region, k.epci, k.population
FROM comptes_collectivites c
LEFT JOIN collectivites k ON k.source_id = c.source_id AND k.exercice = c.exercice AND k.siren = c.siren
  AND k.version = (SELECT MAX(g.version) FROM fichiers_collectivites g
                   WHERE g.source_id = c.source_id AND g.exercice = c.exercice AND g.contenu = 'collectivites')
WHERE c.version = (SELECT MAX(g.version) FROM fichiers_collectivites g
                   WHERE g.source_id = c.source_id AND g.exercice = c.exercice AND g.contenu = 'montants');

-- Pour chaque chiffre, sa version la plus récente chez la même source.
CREATE VIEW v_dernieres_versions AS
SELECT * FROM v_chiffres c
WHERE c.version = (
    SELECT MAX(d.version) FROM chiffres d
    WHERE d.source_id = c.source_id AND d.zone = c.zone AND d.perimetre_id = c.perimetre_id
      AND d.concept_id = c.concept_id AND d.fonction_id IS c.fonction_id
      AND d.traitements IS c.traitements AND d.unite_id = c.unite_id AND d.periode = c.periode);
"""


# Les comptes de chaque collectivité : colonnes et lignes, lues dans les copies archivées.
COMPTES = ["source_id", "fichier_id", "version", "statut", "exercice", "siren", "agregat", "concept_id", "montant_bp",
           "montant_ba", "montant_flux", "montant"]
COLLECTIVITES = ["source_id", "fichier_id", "version", "exercice", "siren", "insee", "insee_2025", "nom", "categorie",
                 "nature_juridique", "mode_financement", "departement", "region", "epci", "population"]
# Champ de l'export de data.ofgl.fr → colonne de la table collectivites.
CHAMPS_COLLECTIVITES = {"siren": "siren", "insee": "insee", "com_code": "insee_2025", "lbudg": "nom", "categ": "categorie",
                        "nat_juridique": "nature_juridique", "mode_financement": "mode_financement",
                        "dep_code": "departement", "reg_code": "region", "epci_code": "epci", "ptot": "population"}


def lignes_collectivites():
    """(table, colonnes, lignes) des comptes de chaque collectivité et des collectivités, une copie après l'autre."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    agregats = {a["agregat"]: a["concept_id"] for a in lire("tables/agregats_ofgl.csv")}
    for inscrit in lire("tables/fichiers_collectivites.csv"):
        fichier = fichiers[inscrit["fichier_id"]]
        tete = [inscrit["source_id"], fichier["id"], inscrit["version"]]
        if inscrit["contenu"] == "montants":
            yield "comptes_collectivites", [tete + [inscrit["statut"], inscrit["exercice"], s, a, agregats[a], *v]
                                            for s, a, *v in ofgl.montants(fichier, agregats)]
        elif inscrit["contenu"] == "collectivites":
            fiches, _ = ofgl.collectivites(fichier)
            lues = []
            for siren, fiche in sorted(fiches.items()):
                colonnes = {CHAMPS_COLLECTIVITES[c]: v for c, v in fiche.items()}
                colonnes["population"] = int(colonnes["population"]) if colonnes.get("population") else None
                lues.append(tete + [inscrit["exercice"]] + [colonnes.get(c) for c in COLLECTIVITES[4:]])
            yield "collectivites", lues


def valeur_sql(champ, texte):
    if texte == "":
        return None
    return {"integer": int, "number": float}.get(champ.get("type"), str)(texte)


def main():
    tables = {}
    for r in paquet()["resources"]:
        nom = "chiffres" if r["schema_chemin"] == "schemas/chiffres.json" else r["name"]
        tables.setdefault(nom, (r["schema"], []))[1].extend(lire(r["path"]))

    SORTIE.mkdir(exist_ok=True)
    chemin = SORTIE / "comptes.sqlite"
    chemin.unlink(missing_ok=True)
    connexion = sqlite3.connect(chemin)
    empreintes = []
    for nom, (schema, lignes) in tables.items():
        champs = schema["fields"]
        colonnes = ", ".join(f'"{c["name"]}" {TYPES_SQL.get(c.get("type"), "TEXT")}' for c in champs)
        cle = schema.get("primaryKey", [])
        connexion.execute(f'CREATE TABLE "{nom}" ({colonnes}{", PRIMARY KEY (" + ", ".join(cle) + ")" if cle else ""})')
        lignes = sorted(lignes, key=lambda l: tuple(l[c] for c in cle))
        connexion.executemany(f'INSERT INTO "{nom}" VALUES ({", ".join("?" * len(champs))})',
                              [[valeur_sql(c, l[c["name"]]) for c in champs] for l in lignes])
        texte = io.StringIO()
        ecrivain = csv.writer(texte, lineterminator="\n")
        ecrivain.writerow([c["name"] for c in champs])
        ecrivain.writerows([l[c["name"]] for c in champs] for l in lignes)
        empreintes.append({"table": nom, "lignes": len(lignes),
                           "sha256": hashlib.sha256(texte.getvalue().encode("utf-8")).hexdigest()})
    connexion.execute(f"CREATE TABLE comptes_collectivites ({', '.join(COMPTES)})")
    connexion.execute(f"CREATE TABLE collectivites ({', '.join(COLLECTIVITES)})")
    hachages = {"comptes_collectivites": [hashlib.sha256(), 0], "collectivites": [hashlib.sha256(), 0]}
    for table, lues in lignes_collectivites():
        if not lues:
            continue
        connexion.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' * len(lues[0]))})", lues)
        texte = io.StringIO()
        csv.writer(texte, lineterminator="\n").writerows(lues)
        hachages[table][0].update(texte.getvalue().encode("utf-8"))
        hachages[table][1] += len(lues)
    connexion.execute("CREATE INDEX comptes_collectivites_cle ON comptes_collectivites (source_id, exercice, siren)")
    connexion.execute("CREATE INDEX collectivites_cle ON collectivites (source_id, exercice, siren)")
    empreintes += [{"table": t, "lignes": n, "sha256": h.hexdigest()} for t, (h, n) in hachages.items()]
    connexion.executescript(VUES)
    connexion.commit()
    connexion.close()

    with (SORTIE / "empreintes.csv").open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=["table", "lignes", "sha256"], lineterminator="\n")
        ecrivain.writeheader()
        ecrivain.writerows(empreintes)
    total = sum(e["lignes"] for e in empreintes if e["table"] == "chiffres")
    print(f"Base construite : {chemin.relative_to(BASE.parent)} ({total} chiffres)")


if __name__ == "__main__":
    main()
