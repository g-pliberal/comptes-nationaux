#!/usr/bin/env python3
"""Enregistre dans la base les séries de la Banque de données macro-économiques de l'Insee archivées (SDMX).

    python3 outils/importer_insee_bdm.py <fichier_id>

Séries prises en charge : la situation mensuelle du budget de l'État (jeu COMPTES-ETAT), que l'Insee reprend
de la publication de l'administration des finances. Ses montants sont cumulés depuis le début de l'année.

Chaque série et chaque attribut doivent avoir une correspondance ci-dessous : une série, une unité, une nature
ou une qualité d'observation inconnue arrête l'import. La version d'un chiffre est la date de dernière mise à
jour de sa série ; son statut, la qualité que l'Insee attache à l'observation.
"""

import sys

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_sdmx, nombre_texte,
                    table_des_chiffres)

# Série (IDBANK) → (concept, périmètre).
SERIES = {
    "001717255": ("LOLF.RESULTAT_EXECUTION", "ETAT_LF"),       # Solde général d'exécution
    "001717256": ("LOLF.BG_DEPENSES_Y_COMPRIS_PSR", "ETAT_LF"),  # Dépenses
    "001717257": ("LOLF.BG_RECETTES_AVANT_PSR", "ETAT_LF"),      # Recettes
    "001717258": ("LOLF.SOLDE_COMPTES_SPECIAUX", "ETAT_LF"),   # Solde des comptes spéciaux
}
UNITES = {("EUROS", "6"): "MIO_EUR"}
NATURES = {"CUMUL_DEBUT_ANNEE": "cumul_depuis_janvier"}
QUALITES = {"DEF": "definitif", "PROV": "provisoire"}
ZONES = {"FE": "FR"}  # France entière
SOLDES = {"LOLF.RESULTAT_EXECUTION", "LOLF.SOLDE_COMPTES_SPECIAUX"}


def lignes_du_fichier(fichier):
    for idbank, (serie, observations) in lire_sdmx(BASE / fichier["chemin"]).items():
        if idbank not in SERIES:
            sys.exit(f"{fichier['id']} : série {idbank} sans correspondance (« {serie.get('TITLE_FR')} »)")
        concept, perimetre = SERIES[idbank]
        unite = UNITES.get((serie.get("UNIT_MEASURE"), serie.get("UNIT_MULT")))
        traitement = NATURES.get(serie.get("NATURE"))
        zone = ZONES.get(serie.get("REF_AREA"))
        if unite is None or traitement is None or zone is None or not serie.get("LAST_UPDATE"):
            sys.exit(f"{fichier['id']} : série {idbank}, attributs sans correspondance ({serie})")
        for periode, observation in observations.items():
            nombre = nombre_texte(observation.get("OBS_VALUE", ""))
            if nombre is None:
                sys.exit(f"{fichier['id']} : série {idbank}, {periode} : valeur « {observation.get('OBS_VALUE')} »")
            if observation.get("OBS_QUAL") not in QUALITES:
                sys.exit(f"{fichier['id']} : série {idbank}, {periode} : qualité « {observation.get('OBS_QUAL')} » inconnue")
            ligne = {
                "source_id": fichier["source_id"], "fichier_id": fichier["id"],
                "emplacement": f"idbank={idbank};periode={periode}",
                "zone": zone, "perimetre_id": perimetre, "concept_id": concept, "fonction_id": "",
                "traitements": traitement, "unite_id": unite, "periode": periode, "valeur": nombre[0],
                "decimales": int(serie.get("DECIMALS") or nombre[1]), "statut": QUALITES[observation["OBS_QUAL"]],
                "drapeau_source": observation["OBS_QUAL"], "version": serie["LAST_UPDATE"][:10],
                "consolidation": "sans_objet" if concept in SOLDES else "non_consolide",
                "denominateur_id": "", "nature": "publie", "calcul_id": "",
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
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, lignes_du_fichier(fichier), fichier["id"])
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
