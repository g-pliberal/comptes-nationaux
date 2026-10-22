#!/usr/bin/env python3
"""Construit la base SQLite interrogeable à partir des tables texte.

    python3 outils/construire.py

Écrit base/construite/comptes.sqlite, à ouvrir avec n'importe quel outil SQLite, et
base/construite/empreintes.csv : une empreinte du contenu de chaque table, qui permet à
chacun de vérifier qu'une base reconstruite contient exactement les mêmes données.
"""

import csv
import hashlib
import io
import sqlite3

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

-- Pour chaque chiffre, sa version la plus récente chez la même source.
CREATE VIEW v_dernieres_versions AS
SELECT * FROM v_chiffres c
WHERE c.version = (
    SELECT MAX(d.version) FROM chiffres d
    WHERE d.source_id = c.source_id AND d.zone = c.zone AND d.perimetre_id = c.perimetre_id
      AND d.concept_id = c.concept_id AND d.fonction_id IS c.fonction_id
      AND d.traitements IS c.traitements AND d.unite_id = c.unite_id AND d.periode = c.periode);
"""


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
