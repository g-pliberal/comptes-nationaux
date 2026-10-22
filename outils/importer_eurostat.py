#!/usr/bin/env python3
"""Enregistre dans la base les chiffres d'un fichier Eurostat archivé (format JSON-stat).

    python3 outils/importer_eurostat.py <fichier_id>

Chaque valeur devient une ligne de tables/chiffres/eurostat.csv, avec sa fiche d'identité.
Une valeur déjà enregistrée à l'identique est ignorée. Une valeur différente pour le même
identifiant arrête l'import : une même version d'un chiffre ne peut pas avoir deux valeurs.
"""

import sys

from commun import BASE, aujourdhui, champs, ecrire, identifiant, lire, lire_jsonstat

CIBLE = "tables/chiffres/eurostat.csv"

# Correspondance entre les codes d'Eurostat et ceux de la base.
CONCEPTS = {"TE": "SEC2010.TE", "TR": "SEC2010.TR", "B9": "SEC2010.B9", "D41PAY": "SEC2010.D41",
            "B1GQ": "SEC2010.B1GQ"}
UNITES = {"MIO_EUR": "MIO_EUR", "CP_MEUR": "MIO_EUR", "PC_GDP": "PC_PIB", "PC_TOT": "PC_DEPENSE"}
DECIMALES = {"MIO_EUR": 1, "PC_PIB": 1, "PC_DEPENSE": 1}
CONSOLIDATION = {"gov_10a_main": "consolide", "gov_10a_exp": "consolide", "nama_10_gdp": "sans_objet"}


def statut(drapeau):
    """Traduit l'indicateur d'Eurostat (p provisoire, e et s estimations, f prévision)."""
    for lettre, valeur in (("f", "prevision"), ("p", "provisoire"), ("e", "estimation"), ("s", "estimation")):
        if lettre in drapeau:
            return valeur
    return "non_precise"


def lignes_du_fichier(fichier):
    jeu = fichier["source_id"].split(".", 1)[1]
    dims, valeurs, mise_a_jour = lire_jsonstat(BASE / fichier["chemin"])
    if not mise_a_jour:
        sys.exit(f"{fichier['id']} : date de mise à jour absente, version inconnue")
    for cle, (valeur, drapeau) in valeurs.items():
        d = dict(zip(dims, cle))
        if d["na_item"] not in CONCEPTS or d["unit"] not in UNITES:
            sys.exit(f"{fichier['id']} : code sans correspondance dans la base ({d['na_item']}, {d['unit']})")
        unite = UNITES[d["unit"]]
        ligne = {
            "source_id": fichier["source_id"], "fichier_id": fichier["id"],
            "emplacement": ";".join(f"{k}={v}" for k, v in d.items()),
            "zone": d["geo"], "perimetre_id": d.get("sector", "S1"), "concept_id": CONCEPTS[d["na_item"]],
            "fonction_id": "" if d.get("cofog99", "TOTAL") == "TOTAL" else d["cofog99"], "traitements": "",
            "unite_id": unite, "periode": d["time"], "valeur": str(valeur), "decimales": DECIMALES[unite],
            "statut": statut(drapeau), "drapeau_source": drapeau, "version": mise_a_jour[:10],
            "consolidation": CONSOLIDATION[jeu], "denominateur_id": "", "nature": "publie", "calcul_id": "",
            "saisi_le": aujourdhui(), "notes": "",
        }
        ligne["id"] = identifiant(ligne)
        yield ligne


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")

    existants = {l["id"]: l for l in lire(CIBLE)}
    nouveaux, conflits = 0, []
    for ligne in lignes_du_fichier(fichier):
        ancien = existants.get(ligne["id"])
        if ancien is None:
            existants[ligne["id"]] = ligne
            nouveaux += 1
        elif (float(ancien["valeur"]), ancien["statut"]) != (float(ligne["valeur"]), ligne["statut"]):
            conflits.append(f"{ligne['id']} : {ancien['valeur']} déjà enregistré, {ligne['valeur']} dans {fichier['id']}")
    if conflits:
        sys.exit("Import interrompu, valeurs contradictoires pour une même version :\n" + "\n".join(conflits))
    ecrire(CIBLE, champs("chiffres-eurostat"), existants.values())
    print(f"{fichier['id']} : {nouveaux} chiffres ajoutés ; {CIBLE} en compte {len(existants)}")


if __name__ == "__main__":
    main()
