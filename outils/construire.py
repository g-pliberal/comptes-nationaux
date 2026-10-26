#!/usr/bin/env python3
"""Construit la base SQLite interrogeable à partir des tables texte.

    python3 outils/construire.py

Écrit base/construite/comptes.sqlite, à ouvrir avec n'importe quel outil SQLite, et
base/construite/empreintes.csv : une empreinte du contenu de chaque table, qui permet à
chacun de vérifier qu'une base reconstruite contient exactement les mêmes données. Les comptes
de chaque collectivité y sont lus dans les copies archivées des exports de data.ofgl.fr
(tables comptes_collectivites et collectivites), ceux des jeux publiés budget par budget dans les
tables comptes_budgets et budgets, les dépenses de chaque budget des départements par fonction dans
les tables comptes_fonctions et budgets, la fiscalité directe locale de chaque commune dans les
tables fiscalite et communes_fiscalite, et les dotations que l'État notifie à chaque collectivité
dans les tables dotations et beneficiaires. Les impositions que recense la DGFiP sur le territoire de
chaque commune (REI) y sont lues dans les copies archivées de ses fichiers : tables impositions_rei,
postes_rei, communes_rei et traces_rei. Les comptes individuels de chaque commune, groupement à fiscalité
propre, département et région que publie la DGFiP y sont lus dans les copies archivées de leurs exports :
tables comptes_individuels et fiches_individuelles. Les balances des comptes de l'État que publie la DGFiP y
sont lues dans les copies archivées de leurs exports, et le plan comptable de l'État dans celle de son classeur :
tables balances_etat et plan_comptable_etat. La vue v_organismes donne les organismes que nomment les listes
officielles, avec les libellés de leur sous-secteur et de leur fonction.
"""

import csv
import hashlib
import io
import itertools
import sqlite3

import importer_balances_etat as balances
import importer_comptes_individuels as individuels
import importer_ofgl_collectivites as ofgl
import importer_rei as rei
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

-- La fiscalité directe locale sur le territoire de chaque commune, dans la version la plus récente de chaque exercice,
-- avec la fiche de la commune. Le produit d'une taxe intercommunale est la part que versent les contribuables de la
-- commune.
CREATE VIEW v_fiscalite AS
SELECT f.source_id, f.exercice, f.version, f.statut, f.fichier_id, x.commune, c.nom, c.siren, c.regime_epci,
       c.commune_2025, c.epci_2025, c.departement, c.region, x.taxe, x.destinataire, x.base, x.taux_net, x.taux_vote,
       x.produit, x.secret
FROM fiscalite x
JOIN fichiers_collectivites f ON f.rowid = x.lot
LEFT JOIN communes_fiscalite c ON c.commune = x.commune AND c.lot = (
    SELECT g.rowid FROM fichiers_collectivites g
    WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'collectivites'
    ORDER BY g.version DESC LIMIT 1)
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

-- Les impositions que recense la DGFiP (REI) sur le territoire de chaque commune, d'après la copie la plus récente de
-- chaque année, avec le libellé de la taxe et la fiche de la commune. Le produit d'une part intercommunale,
-- départementale ou régionale, ou d'un organisme, est ce que paient les contribuables de la commune.
CREATE VIEW v_impositions_rei AS
SELECT f.exercice, f.version, f.fichier_id, x.commune, c.nom, c.departement, c.region, c.groupement, c.nom_groupement,
       c.siren_groupement, c.regime_groupement, p.taxe, t.libelle AS taxe_libelle, p.destinataire, x.base, x.taux_net,
       x.taux_vote, x.produit
FROM impositions_rei x
JOIN fichiers_rei f ON f.rowid = x.lot
JOIN postes_rei p ON p.rowid = x.poste
JOIN taxes_rei t ON t.taxe = p.taxe
LEFT JOIN communes_rei c ON c.lot = x.lot AND c.commune = x.commune
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_rei g WHERE g.exercice = f.exercice);

-- Le tracé de chaque fichier du REI, avec, pour chaque variable que la base retient, la taxe, le destinataire et la
-- grandeur qu'elle donne ; une variable peut en donner plusieurs, le taux de la taxe d'habitation valant aussi pour
-- les logements vacants.
CREATE VIEW v_traces_rei AS
SELECT f.exercice, f.version, f.fichier_id, v.rang, v.code, v.titre, v.titre_trace, v.format, r.taxe, r.destinataire,
       r.grandeur
FROM traces_rei v
JOIN fichiers_rei f ON f.rowid = v.lot
LEFT JOIN variables_rei r ON r.code = v.code AND f.exercice BETWEEN r.premier_exercice AND r.dernier_exercice;

-- Les comptes individuels que publie la DGFiP, dans la version la plus récente de chaque exercice de chaque niveau, avec
-- le libellé de chaque variable dans la maquette, sa grandeur (montant, base et réduction en milliers d'euros, taux en
-- %), le concept qu'elle mesure, et la fiche de la collectivité.
CREATE VIEW v_comptes_individuels AS
SELECT f.source_id, f.exercice, f.version, f.fichier_id, c.collectivite, k.nom, k.departement, k.region, k.population,
       k.strate, k.groupement, v.variable, v.grandeur, v.concept_id, co.libelle AS concept_libelle, v.libelle, c.valeur
FROM comptes_individuels c
JOIN fichiers_comptes_individuels f ON f.rowid = c.lot
JOIN variables_comptes_individuels v ON v.rowid = c.variable
JOIN concepts co ON co.id = v.concept_id
LEFT JOIN fiches_individuelles k ON k.lot = c.lot AND k.collectivite = c.collectivite
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_comptes_individuels g
                   WHERE g.source_id = f.source_id AND g.exercice = f.exercice AND g.contenu = 'comptes');

-- Les balances des comptes de l'État, dans la version la plus récente de chaque exercice : chaque ligne avec le libellé
-- de son compte dans le plan comptable de l'État le plus récent, la catégorie, le poste et l'indicateur de synthèse qui
-- la rattachent aux états financiers, la ligne du bilan ou du compte de résultat qu'elle alimente, son solde (un solde
-- créditeur est négatif) et son montant dans le sens de cette ligne : le solde multiplié par le signe de l'indicateur.
CREATE VIEW v_balances_etat AS
SELECT f.exercice, f.version, f.fichier_id, b.compte, p.libelle AS compte_libelle, b.mission, b.mission_libelle,
       b.programme, b.nature_budgetaire, b.ministere, i.categorie, i.poste, b.sous_poste, i.indicateur,
       b.indicateur_detail, i.concept_id, c.libelle AS concept_libelle, b.solde, i.signe * b.solde AS montant
FROM balances_etat b
JOIN fichiers_balances_etat f ON f.rowid = b.lot
JOIN indicateurs_balances_etat i ON i.rowid = b.indicateur
LEFT JOIN concepts c ON c.id = i.concept_id
LEFT JOIN plan_comptable_etat p ON p.compte = b.compte
     AND p.lot = (SELECT g.rowid FROM fichiers_balances_etat g WHERE g.contenu = 'plan' ORDER BY g.version DESC LIMIT 1)
WHERE f.version = (SELECT MAX(g.version) FROM fichiers_balances_etat g
                   WHERE g.contenu = 'balance' AND g.exercice = f.exercice);

-- Les organismes que nomment les listes officielles, avec les libellés de leur sous-secteur et de leur fonction, et la
-- source et la version de leur liste.
CREATE VIEW v_organismes AS
SELECT o.annee, o.rang, o.sigle, o.nom, o.perimetre_id, p.libelle AS perimetre_libelle, o.fonction_id,
       f.libelle AS fonction_libelle, o.page, x.source_id, x.mis_a_jour_source AS version, o.fichier_id
FROM organismes o
JOIN perimetres p ON p.id = o.perimetre_id
JOIN fichiers x ON x.id = o.fichier_id
LEFT JOIN fonctions f ON f.id = o.fonction_id;

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
# La fiscalité directe locale : une ligne par commune, désignée par son code Insee de l'exercice, par taxe et par
# bénéficiaire, avec la base, les taux net et voté et le produit (vides si la DGFiP les masque, la ligne portant alors
# « sec_stat ») ; la table communes_fiscalite donne le nom de chaque commune, chaque exercice, son numéro Siren et le
# régime fiscal de son groupement, et ses codes de 2025, ceux de son groupement, de son département et de sa région.
FISCALITE = [("lot", "INTEGER"), ("commune", "TEXT"), ("taxe", "TEXT"), ("destinataire", "TEXT"), ("base", "REAL"),
             ("taux_net", "REAL"), ("taux_vote", "REAL"), ("produit", "REAL"), ("secret", "TEXT")]
COMMUNES_FISCALITE = [("lot", "INTEGER"), ("commune", "TEXT"), ("nom", "TEXT"), ("siren", "TEXT"),
                      ("regime_epci", "TEXT"), ("commune_2025", "TEXT"), ("siren_2025", "TEXT"), ("epci_2025", "TEXT"),
                      ("departement", "TEXT"), ("region", "TEXT")]
CHAMPS_COMMUNES_FISCALITE = {"exer": "exercice", "idcom": "commune", "nom": "nom", "siren": "siren",
                             "optepci": "regime_epci", "insee_n": "commune_2025", "siren_n": "siren_2025",
                             "epci_code": "epci_2025", "dep_code": "departement", "reg_code": "region"}
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
# Le recensement des éléments d'imposition (REI) : une ligne par commune, par taxe et par destinataire, avec la base, les
# taux net et voté et le produit (vides si le fichier les laisse vides), d'après les variables que retient
# tables/variables_rei.csv, une imposition sans base ni produit n'étant pas retenue. Pour que la table reste maniable,
# une ligne ne porte que le numéro de sa copie (`lot`, la ligne de fichiers_rei) et celui de son imposition (`poste`, la
# ligne de postes_rei, qui en donne la taxe et le destinataire) ; la vue v_impositions_rei rétablit les libellés. La
# table communes_rei donne la fiche de chaque commune, chaque année : son nom, son département, sa région, son
# groupement, le régime fiscal et la forme juridique de celui-ci, et le niveau de collectivité qui perçoit la taxe
# d'enlèvement des ordures ménagères ; traces_rei, le tracé de chaque fichier : le rang, le code, le titre (celui de
# l'en-tête du fichier quand il porte les titres) et le format de chaque variable.
IMPOSITIONS_REI = [("lot", "INTEGER"), ("commune", "TEXT"), ("poste", "INTEGER"), ("base", "REAL"),
                   ("taux_net", "REAL"), ("taux_vote", "REAL"), ("produit", "REAL")]
POSTES_REI = [("taxe", "TEXT"), ("destinataire", "TEXT")]
COMMUNES_REI = [("lot", "INTEGER"), ("commune", "TEXT")] + [(c, "TEXT") for c in rei.FICHE]
TRACES_REI = [("lot", "INTEGER"), ("rang", "INTEGER"), ("code", "TEXT"), ("titre", "TEXT"), ("titre_trace", "TEXT"),
              ("format", "TEXT")]
# Les comptes individuels de la DGFiP : une ligne par collectivité et par variable que retient
# tables/variables_comptes_individuels.csv, une valeur absente n'ayant pas de ligne. Une ligne ne porte que le numéro de
# sa copie (`lot`, la ligne de fichiers_comptes_individuels) et celui de sa variable (`variable`, la ligne de
# variables_comptes_individuels, qui en donne la grandeur, le libellé et le concept) ; la collectivité est désignée par
# son code Insee pour une commune, son numéro Siren pour un groupement, son numéro de département ou de région selon la
# DGFiP. La table fiches_individuelles donne la fiche de chaque collectivité, chaque exercice : son nom, son département,
# sa région, sa population (population légale pour une commune, et population DGF jusqu'en 2009), sa strate, le type de
# son groupement pour une commune, le nombre de ses budgets annexes pour un groupement.
COMPTES_INDIVIDUELS = [("lot", "INTEGER"), ("collectivite", "TEXT"), ("variable", "INTEGER"), ("valeur", "REAL")]
FICHES_INDIVIDUELLES = [("lot", "INTEGER"), ("collectivite", "TEXT"), ("nom", "TEXT"), ("departement", "TEXT"),
                        ("region", "TEXT"), ("population", "INTEGER"), ("population_dgf", "INTEGER"), ("strate", "TEXT"),
                        ("groupement", "TEXT"), ("budgets_annexes", "INTEGER"), ("budgets_spic", "INTEGER")]
ENTIERS_FICHES = {"population", "population_dgf", "budgets_annexes", "budgets_spic"}
# Les balances des comptes de l'État : une ligne par ligne de chaque balance, avec le numéro de sa copie (`lot`, la ligne
# de fichiers_balances_etat) et celui de son indicateur de synthèse (`indicateur`, la ligne de indicateurs_balances_etat
# qui le rattache, pour l'exercice, à une catégorie, un poste et une ligne des états financiers), son solde en euros au
# centime. La table plan_comptable_etat donne le libellé de chaque compte et de chaque regroupement de comptes de chaque
# copie du plan comptable de l'État.
BALANCES_ETAT = [("lot", "INTEGER"), ("compte", "TEXT"), ("mission", "TEXT"), ("mission_libelle", "TEXT"),
                 ("programme", "TEXT"), ("nature_budgetaire", "TEXT"), ("ministere", "TEXT"), ("indicateur", "INTEGER"),
                 ("sous_poste", "TEXT"), ("indicateur_detail", "TEXT"), ("solde", "REAL")]
PLAN_COMPTABLE_ETAT = [("lot", "INTEGER"), ("compte", "TEXT"), ("libelle", "TEXT")]


def lignes_collectivites(lots, concepts):
    """(table, lignes) des comptes de chaque collectivité et des collectivités, une copie après l'autre ; `lots` et
    `concepts` donnent le numéro de ligne de chaque copie inscrite et de chaque concept."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    agregats = {a["agregat"]: a["concept_id"] for a in lire("tables/agregats_ofgl.csv")}
    for inscrit in lire("tables/fichiers_collectivites.csv"):
        fichier, lot = fichiers[inscrit["fichier_id"]], lots[inscrit["fichier_id"]]
        par_fonction = inscrit["source_id"] in ofgl.PAR_FONCTION
        par_budget = inscrit["source_id"] in ofgl.PAR_BUDGET or par_fonction
        dotations, fiscalite = inscrit["source_id"] in ofgl.DOTATIONS, inscrit["source_id"] in ofgl.FISCALITE
        if inscrit["contenu"] == "montants" and dotations:
            yield "dotations", [[lot, *l] for l in ofgl.montants_dotations(fichier)]
        elif inscrit["contenu"] == "montants" and fiscalite:
            yield "fiscalite", [[lot, *l[:7], l[7] or None] for l in ofgl.montants_fiscalite(fichier)]
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
                                          if dotations else
                                          (COMMUNES_FISCALITE, CHAMPS_COMMUNES_FISCALITE, "communes_fiscalite")
                                          if fiscalite else (BUDGETS, CHAMPS_BUDGETS, "budgets") if par_budget
                                          else (COLLECTIVITES, CHAMPS_COLLECTIVITES, "collectivites"))
            lues = []
            for _, fiche in sorted(fiches.items()):
                colonnes = {correspondance[c]: v for c, v in fiche.items()}
                colonnes["population"] = int(colonnes["population"]) if colonnes.get("population") else None
                lues.append([lot] + [colonnes.get(c) for c, _ in table[1:]])
            yield nom, lues


def lignes_rei(lots, postes):
    """(table, lignes) du REI, une copie après l'autre : son tracé, la fiche de chaque commune et ses impositions ;
    `lots` et `postes` donnent le numéro de ligne de chaque copie inscrite et de chaque imposition (taxe, destinataire)."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/variables_rei.csv")
    for inscrit in lire("tables/fichiers_rei.csv"):
        lot = lots[inscrit["fichier_id"]]
        exercice, variables, _, lignes = rei.lignes_communes(fichiers[inscrit["fichier_id"]])
        yield "traces_rei", [[lot, rang, *v] for rang, v in enumerate(variables, start=1)]
        retenus = rei.postes(exercice, variables, referentiel, inscrit["fichier_id"])
        communes, impositions = [], []
        for commune, valeurs in lignes:
            fiche = rei.fiche(valeurs)
            communes.append([lot, commune] + [fiche[c] or None for c in rei.FICHE])
            impositions += [[lot, commune, postes[(t, d)], *g] for t, d, *g in rei.impositions(valeurs, retenus)]
        yield "communes_rei", communes
        yield "impositions_rei", impositions


def lignes_individuelles(lots, variables):
    """(table, lignes) des comptes individuels, une copie de comptes après l'autre : la fiche de chaque collectivité et
    ses valeurs ; `lots` et `variables` donnent le numéro de ligne de chaque copie inscrite et de chaque ligne du
    référentiel des variables, sous (source, variable, premier exercice)."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/variables_comptes_individuels.csv")
    for inscrit in lire("tables/fichiers_comptes_individuels.csv"):
        if inscrit["contenu"] != "comptes":
            continue
        lot, source = lots[inscrit["fichier_id"]], inscrit["source_id"]
        exercice, lues, _, _ = individuels.comptes(fichiers[inscrit["fichier_id"]], referentiel)
        numeros = {v: variables[(source, v, l["premier_exercice"])]
                   for v, l in individuels.retenues(source, exercice, referentiel).items()}
        colonnes = {c: colonne for c, colonne, _, _ in individuels.FICHES[source] if colonne}
        fiches, valeurs = [], []
        for code, decrits, montants in lues:
            fiche = {colonnes[c]: v for c, v in decrits.items() if c in colonnes}
            fiches.append([lot, code] + [(int(fiche[c].split(".")[0]) if fiche.get(c) and c in ENTIERS_FICHES
                                          else fiche.get(c) or None) for c, _ in FICHES_INDIVIDUELLES[2:]])
            valeurs += [[lot, code, numeros[v], m] for v, m in montants.items()]
        yield "fiches_individuelles", fiches
        yield "comptes_individuels", valeurs


def lignes_balances(lots, indicateurs):
    """(table, lignes) des balances des comptes de l'État et du plan comptable, une copie après l'autre ; `lots` et
    `indicateurs` donnent le numéro de ligne de chaque copie inscrite et de chaque ligne du référentiel des indicateurs,
    sous (indicateur, premier exercice)."""
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    referentiel = lire("tables/indicateurs_balances_etat.csv")
    for inscrit in lire("tables/fichiers_balances_etat.csv"):
        lot, fichier = lots[inscrit["fichier_id"]], fichiers[inscrit["fichier_id"]]
        if inscrit["contenu"] == "plan":
            yield "plan_comptable_etat", [[lot, c, l or None] for c, l in sorted(balances.plan(fichier).items())]
        elif inscrit["contenu"] == "balance":
            exercice, decrites, soldes = balances.balance(fichier, referentiel)
            numeros = {i: indicateurs[(i, l["premier_exercice"])]
                       for i, l in balances.indicateurs_de(exercice, referentiel).items()}
            yield "balances_etat", [[lot, d["compte"]] + [d[c] or None for c in (
                "mission", "libellemission", "programme", "nature_budgetaire", "libelle_ministere")]
                + [numeros[d["indicateurs_de_synthese"]], d["sous_postes"] or None, d["indicateurs_de_detail"] or None,
                   float(s)] for d, s in zip(decrites, soldes)]


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
        cle, par_nom = schema.get("primaryKey", []), {c["name"]: c for c in champs}
        connexion.execute(f'CREATE TABLE "{nom}" ({colonnes}{", PRIMARY KEY (" + ", ".join(cle) + ")" if cle else ""})')
        # Les lignes dans l'ordre de leur clé, chaque champ selon son type : un rang se trie en nombre.
        lignes = sorted(lignes, key=lambda l: tuple(valeur_sql(par_nom[c], l[c]) for c in cle))
        connexion.executemany(f'INSERT INTO "{nom}" VALUES ({", ".join("?" * len(champs))})',
                              [[valeur_sql(c, l[c["name"]]) for c in champs] for l in lignes])
        texte = io.StringIO()
        ecrivain = csv.writer(texte, lineterminator="\n")
        ecrivain.writerow([c["name"] for c in champs])
        ecrivain.writerows([l[c["name"]] for c in champs] for l in lignes)
        empreintes.append({"table": nom, "lignes": len(lignes),
                           "sha256": hashlib.sha256(texte.getvalue().encode("utf-8")).hexdigest()})
    nouvelles = {"comptes_collectivites": COMPTES, "collectivites": COLLECTIVITES, "comptes_budgets": COMPTES_BUDGETS,
                 "budgets": BUDGETS, "comptes_fonctions": COMPTES_FONCTIONS, "fiscalite": FISCALITE,
                 "communes_fiscalite": COMMUNES_FISCALITE, "dotations": DOTATIONS, "beneficiaires": BENEFICIAIRES,
                 "postes_rei": POSTES_REI, "impositions_rei": IMPOSITIONS_REI, "communes_rei": COMMUNES_REI,
                 "traces_rei": TRACES_REI, "comptes_individuels": COMPTES_INDIVIDUELS,
                 "fiches_individuelles": FICHES_INDIVIDUELLES, "balances_etat": BALANCES_ETAT,
                 "plan_comptable_etat": PLAN_COMPTABLE_ETAT}
    for table, colonnes in nouvelles.items():
        connexion.execute(f"CREATE TABLE {table} ({', '.join(f'{c} {t}' for c, t in colonnes)})")
    lots = {f: r for r, f in connexion.execute("SELECT rowid, fichier_id FROM fichiers_collectivites")}
    concepts = {c: r for r, c in connexion.execute("SELECT rowid, id FROM concepts")}
    hachages = {table: [hashlib.sha256(), 0] for table in nouvelles}
    lots_rei = {f: r for r, f in connexion.execute("SELECT rowid, fichier_id FROM fichiers_rei")}
    lues_postes = [list(p) for p in sorted({(v["taxe"], v["destinataire"]) for v in lire("tables/variables_rei.csv")})]
    connexion.executemany("INSERT INTO postes_rei VALUES (?, ?)", lues_postes)
    postes = {(t, d): r for r, t, d in connexion.execute("SELECT rowid, taxe, destinataire FROM postes_rei")}
    texte = io.StringIO()
    csv.writer(texte, lineterminator="\n").writerows(lues_postes)
    hachages["postes_rei"] = [hashlib.sha256(texte.getvalue().encode("utf-8")), len(lues_postes)]
    lots_individuels = {f: r for r, f in connexion.execute("SELECT rowid, fichier_id FROM fichiers_comptes_individuels")}
    variables = {(s, v, p): r for r, s, v, p in
                 connexion.execute("SELECT rowid, source_id, variable, premier_exercice FROM variables_comptes_individuels")}
    lots_balances = {f: r for r, f in connexion.execute("SELECT rowid, fichier_id FROM fichiers_balances_etat")}
    indicateurs = {(i, p): r for r, i, p in
                   connexion.execute("SELECT rowid, indicateur, premier_exercice FROM indicateurs_balances_etat")}
    for table, lues in itertools.chain(lignes_collectivites(lots, concepts), lignes_rei(lots_rei, postes),
                                       lignes_individuelles(lots_individuels, variables),
                                       lignes_balances(lots_balances, indicateurs)):
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
    connexion.execute("CREATE INDEX fiscalite_lot ON fiscalite (lot, taxe, destinataire)")
    connexion.execute("CREATE INDEX fiscalite_commune ON fiscalite (commune)")
    connexion.execute("CREATE INDEX communes_fiscalite_cle ON communes_fiscalite (lot, commune)")
    connexion.execute("CREATE INDEX dotations_lot ON dotations (lot, variable)")
    connexion.execute("CREATE INDEX dotations_code ON dotations (code)")
    connexion.execute("CREATE INDEX beneficiaires_cle ON beneficiaires (lot, code)")
    connexion.execute("CREATE INDEX impositions_rei_lot ON impositions_rei (lot, poste)")
    connexion.execute("CREATE INDEX impositions_rei_commune ON impositions_rei (commune)")
    connexion.execute("CREATE INDEX communes_rei_cle ON communes_rei (lot, commune)")
    connexion.execute("CREATE INDEX traces_rei_cle ON traces_rei (lot, code)")
    connexion.execute("CREATE INDEX comptes_individuels_lot ON comptes_individuels (lot, variable)")
    connexion.execute("CREATE INDEX comptes_individuels_collectivite ON comptes_individuels (collectivite)")
    connexion.execute("CREATE INDEX fiches_individuelles_cle ON fiches_individuelles (lot, collectivite)")
    connexion.execute("CREATE INDEX balances_etat_lot ON balances_etat (lot, indicateur)")
    connexion.execute("CREATE INDEX balances_etat_compte ON balances_etat (compte)")
    connexion.execute("CREATE INDEX plan_comptable_etat_cle ON plan_comptable_etat (lot, compte)")
    empreintes += [{"table": t, "lignes": n, "sha256": h.hexdigest()} for t, (h, n) in hachages.items()]
    connexion.executescript(VUES)
    # Les statistiques des tables et de leurs index, pour que SQLite choisisse son chemin : sans elles, une requête sur la
    # vue des comptes individuels parcourt leurs cinquante millions de lignes.
    connexion.execute("ANALYZE")
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
