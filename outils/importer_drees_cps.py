#!/usr/bin/env python3
"""Enregistre dans la base les comptes de la protection sociale de la DREES archivés : les prestations sociales de
chaque régime, risque par risque, et les emplois et les ressources de la protection sociale.

    python3 outils/importer_drees_cps.py <fiche du jeu> <export> <classeur>

Les trois copies sont celles du jeu 305_les-comptes-de-la-protection-sociale du portail data.drees : sa fiche, où le
portail dit en quelle unité sont les montants de l'export ; l'export de ses données, les prestations de l'ensemble des
régimes, de chaque secteur et de chaque régime, une ligne par année, prestation et régime ; le classeur qu'il joint,
« La protection sociale en France de 1959 à … », dont l'import lit les emplois et les ressources de l'ensemble des
régimes et de chaque groupe de secteurs (ses feuilles de prestations reprennent celles de l'export). L'import
s'arrête :
- si la fiche ne dit pas les montants de l'export en millions d'euros ;
- sur un secteur, un régime, une prestation, une feuille ou une ligne du classeur sans correspondance ci-dessous ou
  dans les tables de la base, ou sur un libellé de prestation qui n'est pas celui de la table des fonctions ;
- si le niveau d'une prestation n'est pas celui que donne son code ;
- si l'export et le classeur ne sont pas de la même édition : mêmes années et, pour les deux dernières, mêmes
  prestations de l'ensemble des régimes ; le classeur, qui ne dit pas son unité, est alors en millions d'euros ;
- si le statut de chaque année n'est pas celui que le classeur énonce dans sa notice.
Le statut d'une année est celui que donne l'en-tête du classeur (« 1959R » : rétropolée, « 2020DEF » : définitive,
« 2024SD » : semi-définitive) ; la notice du classeur dit définitives les années rétropolées. La version d'un chiffre
est la date de mise à jour de sa copie. Les montants sont enregistrés débarrassés des artefacts de la virgule flottante
(jusqu'à quinze décimales avant 2020), comme ceux des autres classeurs.
"""

import json
import re
import sys

from commun import (BASE, aujourdhui, champs_chiffres, ecrire, feuilles_xlsx, fusionner, identifiant, lire,
                    lire_export_ofgl, lire_xlsx, nombre, position, table_des_chiffres)

UNITE = "(en millions d'euros)"  # ce que la fiche du jeu dit du champ val
ENTETE = ["annee", "ps_niveau", "ps_code", "ps_lib", "risque", "regime_nom", "si_niveau", "si_code", "si_nom", "val"]
ENSEMBLE = ("S1", "Total tous secteurs institutionnels", "Total tous régimes")
# Secteur institutionnel de l'export (si_code) → (nom que lui donne l'export, périmètre). La DREES nomme « Régime général
# de la Sécurité sociale » le secteur S13141, qui réunit tous les régimes d'assurance sociale.
SECTEURS = {
    "S11_S12A": ("Autres sociétés financières et non financières", "CPS_S11_S12A"),
    "S12_FP": ("Fonds de pension", "CPS_S12_FP"),
    "S12_OA": ("Organismes d'assurance", "CPS_S12_OA"),
    "S1311": ("Administrations publiques centrales", "CPS_S1311"),
    "S13111": ("État", "CPS_S13111"),
    "S13112": ("ODAC", "CPS_S13112"),
    "S1313": ("Administrations publiques locales", "CPS_S1313"),
    "S13141": ("Régime général de la Sécurité sociale", "CPS_S13141"),
    "S13142": ("Autres organismes dépendants des assurances sociales", "CPS_S13142"),
    "S13_S11": ("Régimes de l'État et des entreprises publiques", "CPS_S13_S11"),
    "S15": ("ISBLSM", "CPS_S15"),
}
# (secteur, régime de l'export) → périmètre du régime.
REGIMES = {
    ("S11_S12A", "Autres régimes privés"): "CPS_AUTRES_REGIMES_PRIVES",
    ("S12_FP", "Fonds de pension"): "CPS_FONDS_DE_PENSION",
    ("S12_FP", "Institutions de retraite supplémentaire"): "CPS_INSTITUTIONS_RETRAITE_SUPPLEMENTAIRE",
    ("S12_FP", "Organismes de retraite professionnelle supplémentaire - contrats collectifs"): "CPS_ORPS",
    ("S12_FP", "Régime additionnel de la fonction publique"): "CPS_RAFP",
    ("S12_OA", "Entreprises d'assurance - contrats collectifs"): "CPS_ENTREPRISES_ASSURANCE",
    ("S12_OA", "Institutions de prévoyance - contrats collectifs"): "CPS_INSTITUTIONS_PREVOYANCE",
    ("S12_OA", "Mutuelles - contrats collectifs"): "CPS_MUTUELLES",
    ("S12_OA", "Organismes d'assurance"): "CPS_ORGANISMES_ASSURANCE",
    ("S1311", "Régimes issus des administrations publiques centrales"): "CPS_REGIMES_APUC",
    ("S13111", "Régime d'intervention sociale de l'État"): "CPS_ETAT_INTERVENTION_SOCIALE",
    ("S13111", "Régime des crédits d'impôt de l'État"): "CPS_ETAT_CREDITS_IMPOT",
    ("S13111", "Régimes pour les agents de l'État (y compris ex-L)"): "CPS_ETAT_AGENTS",
    ("S13112", "ODAC"): "CPS_ODAC",
    ("S1313", "Régime d'intervention sociale des communes"): "CPS_COMMUNES_INTERVENTION_SOCIALE",
    ("S1313", "Régime d'intervention sociale des départements"): "CPS_DEPARTEMENTS_INTERVENTION_SOCIALE",
    ("S1313", "Régime d'intervention sociale des régions"): "CPS_REGIONS_INTERVENTION_SOCIALE",
    ("S1313", "Régime des prestations extra-légales d'employeurs versées aux agents des collectivités locales"):
        "CPS_COLLECTIVITES_PRESTATIONS_EXTRA_LEGALES",
    ("S13141", "Agence centrale des organismes de Sécurité sociale"): "CPS_ACOSS",
    ("S13141", "Association des régimes de retraite complémentaire des salariés"): "CPS_ARRCO",
    ("S13141", "Association générale des institutions de retraite des cadres"): "CPS_AGIRC",
    ("S13141", "Association générale des institutions de retraite des cadres et association des régimes de retraite "
               "complémentaire des salariés"): "CPS_AGIRC_ARRCO",
    ("S13141", "Autres fonds spéciaux"): "CPS_AUTRES_FONDS_SPECIAUX",
    ("S13141", "Autres organismes du régime général"): "CPS_AUTRES_ORGANISMES_REGIME_GENERAL",
    ("S13141", "Autres régimes complémentaires de salariés"): "CPS_AUTRES_REGIMES_COMPLEMENTAIRES",
    ("S13141", "Autres régimes non salariés"): "CPS_AUTRES_REGIMES_NON_SALARIES",
    ("S13141", "Autres régimes spéciaux"): "CPS_AUTRES_REGIMES_SPECIAUX",
    ("S13141", "CNAVPL base complementaire"): "CPS_CNAVPL",
    ("S13141", "Caisse nationale de solidarité pour l'autonomie"): "CPS_CNSA",
    ("S13141", "Caisse nationale des allocations familiales"): "CPS_CNAF",
    ("S13141", "Caisse nationale d’assurance maladie"): "CPS_CNAM",
    ("S13141", "Caisse nationale d’assurance vieillesse"): "CPS_CNAV",
    ("S13141", "Complémentaire santé solidaire"): "CPS_C2S",
    ("S13141", "Exploitants agricoles"): "CPS_EXPLOITANTS_AGRICOLES",
    ("S13141", "Fonds spéciaux"): "CPS_FONDS_SPECIAUX",
    ("S13141", "Institution de retraite complémentaire des agents non titulaires de l’État et des collectivités "
               "publiques"): "CPS_IRCANTEC",
    ("S13141", "Régime des salariés agricoles"): "CPS_SALARIES_AGRICOLES",
    ("S13141", "Régime général de la Sécurité sociale"): "CPS_REGIME_GENERAL",
    ("S13141", "Régimes complémentaires de salariés"): "CPS_REGIMES_COMPLEMENTAIRES",
    ("S13141", "Régimes d'indemnisation du chômage"): "CPS_INDEMNISATION_CHOMAGE",
    ("S13141", "Régimes de base des non-salariés"): "CPS_REGIMES_BASE_NON_SALARIES",
    ("S13141", "Régimes spéciaux"): "CPS_REGIMES_SPECIAUX",
    ("S13141", "UNEDIC et autres régimes"): "CPS_UNEDIC",
    ("S13142", "Autres ODASS"): "CPS_AUTRES_ODASS",
    ("S13142", "Pôle emploi"): "CPS_POLE_EMPLOI",
    ("S13142", "Régime d'intervention sociale des hôpitaux publics"): "CPS_HOPITAUX_INTERVENTION_SOCIALE",
    ("S13_S11", "Régimes de l'État et des entreprises publiques"): "CPS_ETAT_ENTREPRISES_PUBLIQUES",
    ("S15", "Régime d'intervention sociale des institutions sans but lucratif au service des ménages"):
        "CPS_ISBLSM_INTERVENTION_SOCIALE",
}
# Feuilles du classeur : emplois et ressources d'un périmètre, ou feuilles que l'import ne lit pas (la notice, le
# sommaire, et les prestations, que l'export donne régime par régime).
FEUILLES_OPERATIONS = {r"opérations_1959_[0-9]{4}": "CPS_ENSEMBLE", "opérations_SF_SNF": "CPS_SF_SNF",
                       "opérations_ISBLSM": "CPS_S15", "opérations_ASSO": "CPS_ASSO",
                       "opérations_APUC_APUL": "CPS_APUC_APUL"}
FEUILLES_NON_LUES = [r"Lisez-moi", r"Sommaire", r"prestations_1959_[0-9]{4}", r"prestations_SF_SNF",
                     r"prestations_ISBLSM", r"prestations_ASSO", r"prestations_APUC_APUL"]
NOTICE = "Lisez-moi"
# Ligne d'une feuille d'opérations → concept. Les deux totaux excluent les transferts internes entre régimes.
LIGNES = {
    "TOTAL DES EMPLOIS HORS TRANSFERTS *": "CPS.EMPLOIS",
    "Prestations sociales en espèces": "CPS.PRESTATIONS_ESPECES",
    "Prestations sociales en nature": "CPS.PRESTATIONS_NATURE",
    "Frais non financiers": "CPS.FRAIS_NON_FINANCIERS",
    "Frais financiers (depuis 1981)": "CPS.FRAIS_FINANCIERS",
    "Frais financiers et autres emplois (avant 1981)": "CPS.FRAIS_FINANCIERS_AUTRES_EMPLOIS",
    "Autres emplois (depuis 1981)": "CPS.AUTRES_EMPLOIS",
    "Emplois du compte de capital (depuis 2006)": "CPS.EMPLOIS_CAPITAL",
    "Ajustement comptable": "CPS.AJUSTEMENT_COMPTABLE",
    "TOTAL DES RESSOURCES HORS TRANSFERTS *": "CPS.RESSOURCES",
    "Cotisations sociales d'employeurs": "CPS.COTISATIONS_EMPLOYEURS",
    "Cotisations sociales de salariés": "CPS.COTISATIONS_SALARIES",
    "Autres cotisations sociales": "CPS.AUTRES_COTISATIONS",
    "Cotisations sociales imputées": "CPS.COTISATIONS_IMPUTEES",
    "Impôts et taxes affectés": "CPS.IMPOTS_TAXES_AFFECTES",
    "Contributions publiques": "CPS.CONTRIBUTIONS_PUBLIQUES",
    "Produits financiers (depuis 1981)": "CPS.PRODUITS_FINANCIERS",
    "Produits financiers et autres recettes (avant 1981)": "CPS.PRODUITS_FINANCIERS_AUTRES_RECETTES",
    "Autres recettes (depuis 1981)": "CPS.AUTRES_RECETTES",
    "Recettes du compte de capital (depuis 2006)": "CPS.RECETTES_CAPITAL",
}
# Les lignes de notes d'une feuille, sans montant.
NOTES = re.compile(r"\* Cette ligne exclut |Source : Drees")
STATUTS = {"R": "definitif", "DEF": "definitif", "SD": "semi_definitif"}
MILLESIME = re.compile(r"Les données de ([0-9]{4}) à ([0-9]{4}) sont des données dites définitives, l'année ([0-9]{4}) "
                       r"est une année semi-définitive\.")
PRESTATIONS = "CPS.PRESTATIONS"


def fonction(code):
    """« E11-0 » (l'ensemble des prestations) → « » ; « E11-11.1.01 » → « CPS.E11_11_1_01 »."""
    return "" if code == "E11-0" else "CPS." + re.sub(r"[-.]", "_", code)


def niveau(code):
    """Le niveau d'une prestation que donne son code : 0 pour E11-0, 1 pour E11-1, 2 pour E11-11, 3 pour E11-11.1, 4
    pour E11-11.1.01."""
    risque, _, detail = code.removeprefix("E11-").partition(".")
    return 0 if risque == "0" else len(risque) + (detail.count(".") + 1 if detail else 0)


def copie(identifiant_):
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == identifiant_), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {identifiant_}")
    return fichier


def cellules(fichier, feuille):
    """{ligne: {colonne: valeur}} d'une feuille du classeur."""
    lignes = {}
    for reference, valeur in lire_xlsx(BASE / fichier["chemin"], feuille)[1].items():
        n, colonne = position(reference)
        lignes.setdefault(n, {})[colonne] = valeur
    return lignes


def statuts(fichier):
    """{année: (statut, colonne)} d'après l'en-tête de la feuille des emplois et des ressources de l'ensemble, contre ce
    que la notice du classeur énonce."""
    feuille = next(f for f in feuilles_xlsx(BASE / fichier["chemin"]) if re.fullmatch(r"opérations_1959_[0-9]{4}", f))
    resultat = {}
    for colonne, texte in cellules(fichier, feuille)[1].items():
        trouve = re.fullmatch(r"([0-9]{4})(R|DEF|SD)", str(texte))
        if colonne != "A" and trouve is None:
            sys.exit(f"{fichier['id']}, {feuille} : en-tête « {texte} » sans statut connu")
        if trouve:
            resultat[trouve.group(1)] = (STATUTS[trouve.group(2)], colonne)
    notice = " ".join(str(v) for l in cellules(fichier, NOTICE).values() for v in l.values())
    enonce = MILLESIME.search(notice)
    if enonce is None:
        sys.exit(f"{fichier['id']} : la notice n'énonce plus le statut des années comme l'import l'attend")
    debut, fin, semi = enonce.groups()
    attendu = {a: "definitif" if debut <= a <= fin else "semi_definitif" if a == semi else None for a in resultat}
    if attendu != {a: s for a, (s, _) in resultat.items()}:
        sys.exit(f"{fichier['id']} : l'en-tête ne donne pas aux années le statut que la notice énonce")
    return resultat


def chiffre(fichier, emplacement, perimetre, concept, fonction_, annee, texte, statut):
    valeur, decimales = nombre(texte)
    ligne = {"source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement, "zone": "FR",
             "perimetre_id": perimetre, "concept_id": concept, "fonction_id": fonction_, "traitements": "",
             "unite_id": "MIO_EUR", "periode": annee, "valeur": valeur, "decimales": decimales, "statut": statut,
             "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": "consolide",
             "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": ""}
    ligne["id"] = identifiant(ligne)
    return ligne


def operations(fichier, statuts_):
    """Les emplois et les ressources du classeur, feuille par feuille."""
    for feuille in feuilles_xlsx(BASE / fichier["chemin"]):
        perimetre = next((p for motif, p in FEUILLES_OPERATIONS.items() if re.fullmatch(motif, feuille)), None)
        if perimetre is None:
            if not any(re.fullmatch(motif, feuille) for motif in FEUILLES_NON_LUES):
                sys.exit(f"{fichier['id']} : feuille « {feuille} » sans correspondance")
            continue
        lignes = cellules(fichier, feuille)
        annees = {}
        for colonne, texte in lignes[1].items():
            if colonne == "A":
                continue
            trouve = re.fullmatch(r"([0-9]{4})(R|DEF|SD)", str(texte))
            if trouve is None or statuts_.get(trouve.group(1), (None,))[0] != STATUTS[trouve.group(2)]:
                sys.exit(f"{fichier['id']}, {feuille} : en-tête « {texte} » différent de la feuille de l'ensemble")
            annees[colonne] = trouve.group(1)
        for n in sorted(lignes)[1:]:
            libelle = str(lignes[n].get("A", ""))
            montants = {c: v for c, v in lignes[n].items() if c != "A"}
            if not montants and (NOTES.match(libelle) or not libelle):
                continue
            if libelle not in LIGNES or any(c not in annees for c in montants):
                sys.exit(f"{fichier['id']}, {feuille}, ligne {n} : « {libelle} » sans correspondance")
            for colonne, valeur in montants.items():
                if not isinstance(valeur, float):
                    sys.exit(f"{fichier['id']}, {feuille}, cellule {colonne}{n} : « {valeur} » n'est pas un montant")
                yield chiffre(fichier, f"feuille={feuille};cellule={colonne}{n}", perimetre, LIGNES[libelle], "",
                              annees[colonne], valeur, statuts_[annees[colonne]][0])


def prestations(fichier, statuts_):
    """Les prestations de l'export, régime par régime."""
    entete, lignes = lire_export_ofgl(BASE / fichier["chemin"])
    if entete != ENTETE:
        sys.exit(f"{fichier['id']} : en-tête {entete}, l'import attend {ENTETE}")
    fonctions = {f["id"]: f["libelle"] for f in lire("tables/fonctions.csv")}
    perimetres = {p["id"] for p in lire("tables/perimetres.csv")}
    for n, valeurs in enumerate(lignes, start=2):
        l = dict(zip(ENTETE, valeurs))
        lieu = f"{fichier['id']}, ligne {n}"
        if (l["si_code"], l["si_nom"], l["regime_nom"]) == ENSEMBLE and l["si_niveau"] == "0":
            perimetre = "CPS_ENSEMBLE"
        elif l["si_niveau"] == "1" and l["si_code"] in SECTEURS and l["regime_nom"] == f"Total {l['si_code']}":
            perimetre = SECTEURS[l["si_code"]][1]
        elif l["si_niveau"] == "2" and (l["si_code"], l["regime_nom"]) in REGIMES:
            perimetre = REGIMES[(l["si_code"], l["regime_nom"])]
        else:
            sys.exit(f"{lieu} : régime « {l['regime_nom']} » du secteur {l['si_code']} sans correspondance")
        if (l["si_code"] in SECTEURS and l["si_nom"] != SECTEURS[l["si_code"]][0]) or perimetre not in perimetres:
            sys.exit(f"{lieu} : secteur « {l['si_nom']} » ({l['si_code']}) ou périmètre {perimetre} inattendu")
        if not re.fullmatch(r"E11-[0-9]+(\.[0-9]+){0,2}", l["ps_code"]) or str(niveau(l["ps_code"])) != l["ps_niveau"]:
            sys.exit(f"{lieu} : prestation {l['ps_code']} au niveau {l['ps_niveau']}")
        fonction_ = fonction(l["ps_code"])
        if fonction_ and fonctions.get(fonction_) != l["ps_lib"]:
            sys.exit(f"{lieu} : prestation {l['ps_code']} « {l['ps_lib']} », la table des fonctions dit "
                     f"« {fonctions.get(fonction_)} »")
        if l["annee"] not in statuts_:
            sys.exit(f"{lieu} : année {l['annee']} absente du classeur")
        yield chiffre(fichier, f"ligne={n};colonne=val", perimetre, PRESTATIONS, fonction_, l["annee"],
                      float(l["val"]), statuts_[l["annee"]][0])


def meme_edition(export, classeur, prestations_, operations_):
    """L'export et le classeur sont de la même édition : mêmes années, et, pour les deux dernières, les mêmes
    prestations de l'ensemble des régimes (prestations en espèces et en nature du classeur)."""
    total = {l["periode"]: float(l["valeur"]) for l in prestations_
             if l["perimetre_id"] == "CPS_ENSEMBLE" and not l["fonction_id"]}
    especes_nature = {}
    for l in operations_:
        if l["perimetre_id"] == "CPS_ENSEMBLE" and l["concept_id"] in ("CPS.PRESTATIONS_ESPECES", "CPS.PRESTATIONS_NATURE"):
            especes_nature[l["periode"]] = especes_nature.get(l["periode"], 0) + float(l["valeur"])
    dernieres = sorted(total)[-2:]
    if sorted(total) != sorted(especes_nature) or any(abs(total[a] - especes_nature[a]) > 0.005 for a in dernieres):
        sys.exit(f"{export['id']} et {classeur['id']} ne sont pas de la même édition")


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    fiche, export, classeur = (copie(i) for i in sys.argv[1:])
    if len({fiche["source_id"], export["source_id"], classeur["source_id"]}) != 1:
        sys.exit("les trois copies doivent être de la même source")
    champs_ = {c["name"]: c for c in json.loads((BASE / fiche["chemin"]).read_text(encoding="utf-8"))["fields"]}
    if UNITE not in (champs_.get("val", {}).get("description") or ""):
        sys.exit(f"{fiche['id']} : la fiche ne dit pas le champ val {UNITE}")
    statuts_ = statuts(classeur)
    operations_ = list(operations(classeur, statuts_))
    prestations_ = list(prestations(export, statuts_))
    meme_edition(export, classeur, prestations_, operations_)
    cible = table_des_chiffres(export["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    for fichier, lignes in ((classeur, operations_), (export, prestations_)):
        ajoutes, inchanges = fusionner(existants, lignes, fichier["id"])
        print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés")
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
