#!/usr/bin/env python3
"""Enregistre dans la base les séries de la Banque de données macro-économiques de l'Insee archivées (SDMX).

    python3 outils/importer_insee_bdm.py <fichier_id>

Séries prises en charge :
- la situation mensuelle du budget de l'État (jeu COMPTES-ETAT), que l'Insee reprend de la publication de
  l'administration des finances ; ses montants sont cumulés depuis le début de l'année ;
- la dette trimestrielle des administrations publiques (jeu DETTE-TRIM-APU-2020) : encours en fin de trimestre de
  la dette au sens de Maastricht, par sous-secteur et par instrument, et en % du PIB, de la dette nette, des actions
  cotées et titres d'OPC que les administrations détiennent, et de la dette brute au sens du FMI ;
- la dette négociable de l'État (jeu DETTE-NEGOCIABLE-ETAT), que l'Insee reprend de l'Agence France Trésor : encours en
  fin de mois, total, en euros et en devises, à court terme et à moyen et long terme, à taux fixe et indexé sur
  l'inflation, et variations de chacun depuis le début de l'année.

Chaque série et chaque attribut doivent avoir une correspondance ci-dessous : une série, une unité, une nature
ou une qualité d'observation inconnue arrête l'import. La version d'un chiffre est la date de dernière mise à
jour de sa série ; son statut, la qualité que l'Insee attache à l'observation. Un trimestre, que l'Insee note
« 2026-Q2 », s'écrit « 2026-T2 » dans la base ; l'emplacement garde la notation de la source.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_sdmx, nombre_texte,
                    table_des_chiffres)

# Série (IDBANK) → (concept, périmètre, consolidation). La dette au sens de Maastricht d'un sous-secteur est, comme dans
# les comptes annuels, sa contribution à la dette consolidée de l'ensemble.
SERIES = {
    "001717255": ("LOLF.RESULTAT_EXECUTION", "ETAT_LF", "sans_objet"),           # Solde général d'exécution
    "001717256": ("LOLF.BG_DEPENSES_Y_COMPRIS_PSR", "ETAT_LF", "non_consolide"),  # Dépenses
    "001717257": ("LOLF.BG_RECETTES_AVANT_PSR", "ETAT_LF", "non_consolide"),      # Recettes
    "001717258": ("LOLF.SOLDE_COMPTES_SPECIAUX", "ETAT_LF", "sans_objet"),       # Solde des comptes spéciaux
    "010777616": ("PDE.GD", "S13", "consolide"),       # Dette de Maastricht, ensemble
    "010777608": ("PDE.GD", "S13", "consolide"),       # Ensemble, en point de PIB
    "010777610": ("PDE.GD", "S13111", "consolide"),    # État
    "010777613": ("PDE.GD", "S13112", "consolide"),    # Organismes divers d'administration centrale
    "010777626": ("PDE.GD", "S1313", "consolide"),     # Administrations publiques locales
    "010777625": ("PDE.GD", "S1314", "consolide"),     # Administrations de sécurité sociale
    "010777606": ("PDE.GD_F2", "S13", "consolide"),    # Dépôts
    "010777624": ("PDE.GD_F3", "S13", "consolide"),    # Titres autres qu'actions et participations
    "010777609": ("PDE.GD_F31", "S13", "consolide"),   # Titres de court terme (F331)
    "010777619": ("PDE.GD_F32", "S13", "consolide"),   # Titres de long terme (F332)
    "010777607": ("PDE.GD_F4", "S13", "consolide"),    # Crédits
    "010777618": ("PDE.GD_F41", "S13", "consolide"),   # Crédits à court terme
    "010777617": ("PDE.GD_F42", "S13", "consolide"),   # Crédits à long terme
    "010777611": ("INSEE_DETTE.DETTE_NETTE", "S13", "consolide"),               # Dette nette
    "010777621": ("INSEE_DETTE.AUTRES_ACTIFS_LIQUIDES", "S13", "non_precise"),  # Actions cotées et titres d'OPC détenus
    "010777622": ("GFSM2014.DETTE_BRUTE", "S13", "non_precise"),          # Dette brute au sens du FMI : total des passifs
    "010777623": ("GFSM2014.DETTE_BRUTE_EUROS", "S13", "non_precise"),    # … en euros
    "010777620": ("GFSM2014.DETTE_BRUTE_DEVISES", "S13", "non_precise"),  # … en devises étrangères
    "010777612": ("GFSM2014.DETTE_BRUTE_F6", "S13", "non_precise"),       # … réserves techniques d'assurance
    "010777614": ("GFSM2014.DETTE_BRUTE_F8", "S13", "non_precise"),       # … autres comptes à payer
    "010777615": ("GFSM2014.DETTE_BRUTE_F12", "S13", "non_precise"),      # … droits de tirage spéciaux
}
# La dette négociable de l'État : l'encours de chaque série, et sa variation depuis le début de l'année (nature
# VARIATIONS_DEBUT_ANNEE), que l'Insee publie pour toutes sauf le total.
_DETTE_NEGOCIABLE = {"001739081": "ENCOURS",
                     "001711531": "ENCOURS_EUROS", "001738855": "ENCOURS_EUROS",
                     "001711532": "COURT_TERME_EUROS", "001738856": "COURT_TERME_EUROS",
                     "001711533": "MOYEN_LONG_TERME_EUROS", "001738857": "MOYEN_LONG_TERME_EUROS",
                     "001719708": "ENCOURS_DEVISES", "001738858": "ENCOURS_DEVISES",
                     "001719709": "COURT_TERME_DEVISES", "001738859": "COURT_TERME_DEVISES",
                     "001719710": "MOYEN_LONG_TERME_DEVISES", "001738860": "MOYEN_LONG_TERME_DEVISES",
                     "001738853": "TAUX_FIXE", "001738861": "TAUX_FIXE",
                     "001738854": "INDEXEE_INFLATION", "001738862": "INDEXEE_INFLATION"}
SERIES.update({i: (f"DETTE_NEGOCIABLE.{c}", "ETAT_AFT", "non_consolide") for i, c in _DETTE_NEGOCIABLE.items()})
UNITES = {("EUROS", "6"): "MIO_EUR", ("EUROS", "9"): "MD_EUR", ("POURCENT", "0"): "PC_PIB"}
NATURES = {"CUMUL_DEBUT_ANNEE": "cumul_depuis_janvier", "VALEUR_ABSOLUE": "", "PROPORTION": "", "ENCOURS": "",
           "VARIATIONS_DEBUT_ANNEE": "variation_depuis_decembre"}
QUALITES = {"DEF": "definitif", "PROV": "provisoire"}
ZONES = {"FE": "FR"}  # France entière


def periode_de_la_base(periode):
    """« 2026-Q2 » → « 2026-T2 » ; un mois ou une année reste tel quel."""
    return re.sub(r"-Q([1-4])$", r"-T\1", periode)


def lignes_du_fichier(fichier):
    for idbank, (serie, observations) in lire_sdmx(BASE / fichier["chemin"]).items():
        if idbank not in SERIES:
            sys.exit(f"{fichier['id']} : série {idbank} sans correspondance (« {serie.get('TITLE_FR')} »)")
        concept, perimetre, consolidation = SERIES[idbank]
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
                "traitements": traitement, "unite_id": unite, "periode": periode_de_la_base(periode),
                "valeur": nombre[0], "decimales": int(serie.get("DECIMALS") or nombre[1]),
                "statut": QUALITES[observation["OBS_QUAL"]], "drapeau_source": observation["OBS_QUAL"],
                "version": serie["LAST_UPDATE"][:10], "consolidation": consolidation,
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
