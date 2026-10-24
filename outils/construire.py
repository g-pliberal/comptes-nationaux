#!/usr/bin/env python3
"""Construit la base SQLite interrogeable à partir des tables texte.

    python3 outils/construire.py

Écrit base/construite/comptes.sqlite, à ouvrir avec n'importe quel outil SQLite, et
base/construite/empreintes.csv : une empreinte du contenu de chaque table, qui permet à
chacun de vérifier qu'une base reconstruite contient exactement les mêmes données. Les comptes
de chaque collectivité y sont lus dans les copies archivées des exports de data.ofgl.fr
(tables comptes_collectivites et collectivites), ceux des jeux publiés budget par budget dans les
tables comptes_budgets et budgets, les dépenses de chaque budget des départements par fonction dans
les tables comptes_fonctions et budgets, et les dotations que l'État notifie à chaque collectivité
dans les tables dotations et beneficiaires.
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

-- Les comptes de chaque collectivité, dans la version la plus récente de chaque exercice, avec leurs libellés et le nom,
-- le territoire et la population de la collectivité.
CREATE VIEW v_comptes_collectivites AS
SELECT f.source_id, f.exercice, f.version, f.statut, f.fichier_id, c.siren, co.id AS concept_id,
       co.libelle AS concept_libelle, c.montant_bp, c.montant_ba, c.montant_flux, c.montant,
       k.insee, k.insee_2025, k.nom, k.denomination, k.categorie, k.nature_juridique, k.activite, k.departement,
       k.region, k.epci, k.population
FROM comptes_collectivites c
JOIN fichiers_collectivites f ON f.rowid = c.lot
JOIN concepts co ON co.rowid = c.concept
LEFT JOIN collectivites k ON k.siren = c.siren AND k.lot = (
    SELECT g.rowid FROM fichiers_collectivites g
    WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'collectivites'
    ORDER BY g.version DESC LIMIT 1)
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_collectivites g
                   WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'montants');

-- Les comptes de chaque budget des jeux publiés budget par budget (SDIS, centres d'action sociale), dans la version la
-- plus récente de chaque exercice, avec leurs libellés et la fiche du budget.
CREATE VIEW v_comptes_budgets AS
SELECT f.source_id, f.exercice, f.version, f.statut, f.fichier_id, c.siren, c.budget, co.id AS concept_id,
       co.libelle AS concept_libelle, c.montant, b.nom, b.collectivite, b.categorie, b.type_budget, b.nature,
       b.nomenclature, b.departement, b.region, b.population
FROM comptes_budgets c
JOIN fichiers_collectivites f ON f.rowid = c.lot
JOIN concepts co ON co.rowid = c.concept
LEFT JOIN budgets b ON b.budget = c.budget AND b.lot = (
    SELECT g.rowid FROM fichiers_collectivites g
    WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'collectivites'
    ORDER BY g.version DESC LIMIT 1)
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_collectivites g
                   WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'montants');

-- Les dépenses de chaque budget des départements par fonction, dans la version la plus récente de chaque exercice, avec
-- leurs libellés, la fiche du budget et le nom de sa collectivité (le libellé de son budget principal). Chaque montant
-- figure à chacun des niveaux de sa fonction : n'additionner que les fonctions d'un même niveau.
CREATE VIEW v_comptes_fonctions AS
SELECT f.source_id, f.exercice, f.version, f.statut, f.fichier_id, c.siren, p.nom AS collectivite, c.budget, b.nom,
       b.type_budget, b.categorie, b.departement, b.region, b.population, c.nomenclature, c.niveau, c.fonction,
       c.libelle AS fonction_libelle, c.regroupement, co.id AS concept_id, co.libelle AS concept_libelle, c.montant
FROM comptes_fonctions c
JOIN fichiers_collectivites f ON f.rowid = c.lot
JOIN concepts co ON co.rowid = c.concept
LEFT JOIN budgets b ON b.budget = c.budget AND b.lot = (
    SELECT g.rowid FROM fichiers_collectivites g
    WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'collectivites'
    ORDER BY g.version DESC LIMIT 1)
LEFT JOIN budgets p ON p.lot = b.lot AND p.siren = c.siren AND p.type_budget = '1'
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_collectivites g
                   WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'montants');

-- Les dotations que l'État notifie à chaque collectivité, dans la version la plus récente de chaque exercice, avec le
-- nom et le territoire de la collectivité.
CREATE VIEW v_dotations AS
SELECT f.source_id, f.exercice, f.version, f.statut, f.fichier_id, d.code, b.nom, b.departement, b.epci,
       b.nature_juridique, d.variable, d.montant
FROM dotations d
JOIN fichiers_collectivites f ON f.rowid = d.lot
LEFT JOIN beneficiaires b ON b.code = d.code AND b.lot = (
    SELECT g.rowid FROM fichiers_collectivites g
    WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'collectivites'
    ORDER BY g.version DESC LIMIT 1)
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_collectivites g
                   WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'montants');

-- Pour chaque chiffre, sa version la plus récente chez la même source.
CREATE VIEW v_dernieres_versions AS
SELECT * FROM v_chiffres c
WHERE c.version = (
    SELECT MAX(d.version) FROM chiffres d
    WHERE d.source_id = c.source_id AND d.zone = c.zone AND d.perimetre_id = c.perimetre_id
      AND d.concept_id = c.concept_id AND d.fonction_id IS c.fonction_id
      AND d.traitements IS c.traitements AND d.unite_id = c.unite_id AND d.periode = c.periode);
"""


# Les comptes de chaque collectivité, lus dans les copies archivées. Pour que la base reste maniable (près de vingt-trois
# millions de lignes), une ligne de compte ne porte que le numéro de sa copie (`lot`, la ligne de fichiers_collectivites
# qui l'inscrit) et celui de son concept (`concept`, la ligne de concepts) ; la vue v_comptes_collectivites rétablit
# les libellés.
COMPTES = [("lot", "INTEGER"), ("siren", "TEXT"), ("concept", "INTEGER"), ("montant_bp", "REAL"),
           ("montant_ba", "REAL"), ("montant_flux", "REAL"), ("montant", "REAL")]
COLLECTIVITES = [("lot", "INTEGER"), ("siren", "TEXT"), ("insee", "TEXT"), ("insee_2025", "TEXT"), ("nom", "TEXT"),
                 ("denomination", "TEXT"), ("categorie", "TEXT"), ("nature_juridique", "TEXT"), ("activite", "TEXT"),
                 ("mode_financement", "TEXT"), ("departement", "TEXT"), ("region", "TEXT"), ("epci", "TEXT"),
                 ("population", "INTEGER")]
# Champ de l'export de data.ofgl.fr → colonne de la table collectivites ; la catégorie d'un syndicat (SIVU, SIVOM, syndicat
# mixte, pôle, maison départementale des personnes handicapées) ou d'un établissement public local (EPA, régie, GIP) y
# tient lieu de nature juridique.
CHAMPS_COLLECTIVITES = {"siren": "siren", "insee": "insee", "com_code": "insee_2025", "lbudg": "nom",
                        "nom_epl": "denomination", "categ": "categorie", "nat_juridique": "nature_juridique",
                        "categorie_synd": "nature_juridique", "categorie_epl_abr": "nature_juridique",
                        "libelle_cacti_simplifie": "activite", "mode_financement": "mode_financement",
                        "dep_code": "departement", "dep_current_code": "departement", "reg_code": "region",
                        "epci_code": "epci", "ptot": "population"}
# Les jeux publiés budget par budget : une ligne par budget, désigné par son SIRET, et par agrégat ; la table budgets
# donne la fiche de chaque budget, chaque exercice : son libellé, le nom de sa collectivité, sa catégorie (de SDIS, ou
# CCAS, CIAS), son type (« 1 » ou « 3 » pour le budget principal ou un budget annexe d'un SDIS, « Budget principal »
# ou « Budget annexe » pour un centre d'action sociale), sa nature (établissement social ou médico-social…) et sa
# nomenclature comptable.
COMPTES_BUDGETS = [("lot", "INTEGER"), ("siren", "TEXT"), ("budget", "TEXT"), ("concept", "INTEGER"), ("montant", "REAL")]
BUDGETS = [("lot", "INTEGER"), ("siren", "TEXT"), ("budget", "TEXT"), ("nom", "TEXT"), ("collectivite", "TEXT"),
           ("categorie", "TEXT"), ("type_budget", "TEXT"), ("nature", "TEXT"), ("nomenclature", "TEXT"),
           ("departement", "TEXT"), ("region", "TEXT"), ("population", "INTEGER")]
CHAMPS_BUDGETS = {"siren": "siren", "ident": "budget", "lbudg": "nom", "nom_ccas": "collectivite",
                  "categorie_sdis": "categorie", "type": "categorie", "categ": "categorie", "cbudg": "type_budget",
                  "type_de_budget": "type_budget", "ctype": "nature", "nomen": "nomenclature", "code_dep": "departement",
                  "dep_code": "departement", "code_region": "region", "code_reg": "region", "reg_code": "region",
                  "population_totale": "population", "ptot": "population"}
# Les dépenses par fonction : une ligne par budget, par fonction de la nomenclature du budget (M52 ou M57), à chacun de
# ses niveaux (le nombre de ses chiffres), et par agrégat, avec le libellé de la fonction et le regroupement du portail ;
# la fiche de chaque budget, chaque exercice, est dans la table budgets, sa catégorie étant celle de sa collectivité
# (« DEPT », « ML » pour la métropole de Lyon, « PARIS »).
COMPTES_FONCTIONS = [("lot", "INTEGER"), ("siren", "TEXT"), ("budget", "TEXT"), ("nomenclature", "TEXT"),
                     ("niveau", "INTEGER"), ("fonction", "TEXT"), ("libelle", "TEXT"), ("regroupement", "TEXT"),
                     ("concept", "INTEGER"), ("montant", "REAL")]
# Les dotations notifiées : une ligne par collectivité, désignée par son code Insee, son numéro Siren ou son code de
# département (`code`), et par variable ; la table beneficiaires donne le nom de chaque collectivité, chaque exercice,
# son département, et le groupement d'une commune ou la nature juridique d'un groupement.
DOTATIONS = [("lot", "INTEGER"), ("code", "TEXT"), ("variable", "TEXT"), ("montant", "REAL")]
BENEFICIAIRES = [("lot", "INTEGER"), ("code", "TEXT"), ("nom", "TEXT"), ("departement", "TEXT"), ("epci", "TEXT"),
                 ("nature_juridique", "TEXT")]
CHAMPS_BENEFICIAIRES = {
    "ofgl.dotations-communes": {"exercice": "exercice", "code_insee": "code", "commune": "nom",
                                "code_departement": "departement", "siren_epci": "epci"},
    "ofgl.dotations-gfp": {"exercice": "exercice", "siren": "code", "nom_epci": "nom",
                           "nature_juridique": "nature_juridique", "code_departement": "departement"},
    "ofgl.dotations-departements": {"exercice": "exercice", "code_departement": "code", "nom_departement": "nom"}}


def lignes_collectivites(lots, concepts):
    """(table, lignes) des comptes de chaque collectivité et des collectivités, une copie après l'autre ; `lots` et
    `concepts` donnent le numéro de ligne de chaque copie inscrite et de chaque concept."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    agregats = {a["agregat"]: a["concept_id"] for a in lire("tables/agregats_ofgl.csv")}
    for inscrit in lire("tables/fichiers_collectivites.csv"):
        fichier, lot = fichiers[inscrit["fichier_id"]], lots[inscrit["fichier_id"]]
        par_fonction = inscrit["source_id"] in ofgl.PAR_FONCTION
        par_budget = inscrit["source_id"] in ofgl.PAR_BUDGET or par_fonction
        dotations = inscrit["source_id"] in ofgl.DOTATIONS
        if inscrit["contenu"] == "montants" and dotations:
            yield "dotations", [[lot, *l] for l in ofgl.montants_dotations(fichier)]
        elif inscrit["contenu"] == "montants" and par_fonction:
            yield "comptes_fonctions", [[lot, s, b, n, len(f), f, l, r, concepts[agregats[a]], v]
                                        for s, b, n, f, l, r, a, v in ofgl.montants_fonctions(fichier, agregats)]
        elif inscrit["contenu"] == "montants" and par_budget:
            yield "comptes_budgets", [[lot, s, b, concepts[agregats[a]], v]
                                      for s, b, a, v in ofgl.montants_budgets(fichier, agregats)]
        elif inscrit["contenu"] == "montants":
            yield "comptes_collectivites", [[lot, s, concepts[agregats[a]], *v]
                                            for s, a, *v in ofgl.montants(fichier, agregats)]
        elif inscrit["contenu"] == "collectivites":
            fiches, _ = ofgl.collectivites(fichier)
            table, correspondance, nom = ((BENEFICIAIRES, CHAMPS_BENEFICIAIRES[inscrit["source_id"]], "beneficiaires")
                                          if dotations else (BUDGETS, CHAMPS_BUDGETS, "budgets") if par_budget
                                          else (COLLECTIVITES, CHAMPS_COLLECTIVITES, "collectivites"))
            lues = []
            for _, fiche in sorted(fiches.items()):
                colonnes = {correspondance[c]: v for c, v in fiche.items()}
                colonnes["population"] = int(colonnes["population"]) if colonnes.get("population") else None
                lues.append([lot] + [colonnes.get(c) for c, _ in table[1:]])
            yield nom, lues


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
    nouvelles = {"comptes_collectivites": COMPTES, "collectivites": COLLECTIVITES, "comptes_budgets": COMPTES_BUDGETS,
                 "budgets": BUDGETS, "comptes_fonctions": COMPTES_FONCTIONS, "dotations": DOTATIONS,
                 "beneficiaires": BENEFICIAIRES}
    for table, colonnes in nouvelles.items():
        connexion.execute(f"CREATE TABLE {table} ({', '.join(f'{c} {t}' for c, t in colonnes)})")
    lots = {f: r for r, f in connexion.execute("SELECT rowid, fichier_id FROM fichiers_collectivites")}
    concepts = {c: r for r, c in connexion.execute("SELECT rowid, id FROM concepts")}
    hachages = {table: [hashlib.sha256(), 0] for table in nouvelles}
    for table, lues in lignes_collectivites(lots, concepts):
        if not lues:
            continue
        connexion.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' * len(lues[0]))})", lues)
        texte = io.StringIO()
        csv.writer(texte, lineterminator="\n").writerows(lues)
        hachages[table][0].update(texte.getvalue().encode("utf-8"))
        hachages[table][1] += len(lues)
    connexion.execute("CREATE INDEX comptes_collectivites_lot ON comptes_collectivites (lot, concept)")
    connexion.execute("CREATE INDEX comptes_collectivites_siren ON comptes_collectivites (siren)")
    connexion.execute("CREATE INDEX collectivites_cle ON collectivites (lot, siren)")
    connexion.execute("CREATE INDEX comptes_budgets_lot ON comptes_budgets (lot, concept)")
    connexion.execute("CREATE INDEX comptes_budgets_siren ON comptes_budgets (siren)")
    connexion.execute("CREATE INDEX budgets_cle ON budgets (lot, budget)")
    connexion.execute("CREATE INDEX comptes_fonctions_lot ON comptes_fonctions (lot, concept, niveau)")
    connexion.execute("CREATE INDEX comptes_fonctions_siren ON comptes_fonctions (siren)")
    connexion.execute("CREATE INDEX dotations_lot ON dotations (lot, variable)")
    connexion.execute("CREATE INDEX dotations_code ON dotations (code)")
    connexion.execute("CREATE INDEX beneficiaires_cle ON beneficiaires (lot, code)")
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
