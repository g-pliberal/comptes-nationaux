#!/usr/bin/env python3
"""Ce que l'État verse à chaque collectivité, et ce qu'il lui prélève, d'après les fichiers de recensement des éléments
d'imposition (REI) de la DGFiP.

    python3 outils/versements_rei.py <exercice>   # les versements d'une année, par nature et par niveau

Outre les impositions de chaque commune, le REI donne, chaque année, des montants qui ne sont pas des impôts : les
allocations compensatrices que l'État verse pour les exonérations et les abattements qu'il décide, la dotation de
compensation de la réforme de la taxe professionnelle (DCRTP), les reversements et prélèvements du fonds national de
garantie individuelle des ressources (FNGIR), les fractions de TVA que l'État verse depuis 2021 en compensation de la
taxe d'habitation, de la taxe foncière des départements et de la CVAE, et l'effet du coefficient correcteur, qui
compense aux communes la perte de leur taxe d'habitation. Ces montants sont ceux d'une collectivité : celui d'une
commune figure sur sa ligne, celui d'un groupement, d'un département ou d'une région est répété sur la ligne de chacune
de ses communes. Le référentiel tables/variables_versements_rei.csv dit, pour chaque nature de versement
(tables/versements_rei.csv), chaque niveau de collectivité et chaque grandeur, la variable qui le donne, de son premier
à son dernier exercice.

La collectivité d'un montant se lit sur la ligne de la commune : son code pour une commune, le numéro Siren du groupement
(SIREPCI), le code du département (DEP) ou de la région (REG). Dans la métropole du Grand Paris, la DCRTP, le FNGIR et
les allocations compensatrices de CFE sont celles de l'établissement public territorial de la commune (SIREPT, que le
REI donne depuis 2016) : le niveau « ept_ou_groupement » désigne l'établissement public territorial quand la ligne en
nomme un, le groupement sinon. La métropole de Lyon, qui exerce sur son territoire les compétences du département, est
désignée par son numéro Siren (celui du groupement de ses communes) ; les collectivités territoriales uniques de Corse, de
Martinique et de Guyane par le code de leur région.

Chaque variable du référentiel doit figurer au tracé de chacune de ses années, et son titre y dire sa nature, son niveau
et sa grandeur. Le montant d'une collectivité doit être le même sur chacune de ses communes qui en donnent un non nul :
une commune peut le laisser nul (les communes de la métropole de Lyon pour le département du Rhône, celles de
Haute-Corse pour la collectivité de Corse) ; un montant non nul sans collectivité, ou deux montants différents pour la
même, arrêtent la lecture. Un montant nul n'est pas retenu.
"""

import collections
import re
import sys

import importer_rei as rei
from commun import lire

NIVEAUX = ["commune", "groupement", "ept_ou_groupement", "departement", "region", "metropole_lyon",
           "collectivite_unique"]
# Ce que doit dire le titre d'une variable, selon son niveau : l'effet du coefficient correcteur, propre aux communes,
# ne le dit pas toujours.
TITRES_NIVEAUX = {"commune": r"\bCOMMUNE\b|COEFFICIENT CORRECTEUR", "groupement": r"INTERCOMMUNALITE|\bEPCI\b|\bGFP\b",
                  "ept_ou_groupement": r"INTERCOMMUNALITE|\bEPCI\b|\bGFP\b", "departement": r"DEPARTEMENT|\bDEP\b",
                  "region": r"\bREGION\b|\bREG\b", "metropole_lyon": r"\bMGL\b|METROPOLE DE LYON",
                  "collectivite_unique": r"\bCTU\b"}
# Ce que doit dire le titre d'une variable, selon la nature du versement.
TITRES_VERSEMENTS = {
    "ALLOCATIONS_TH": r"^TH\b.*(ALLOCATION|DOTATION)", "ALLOCATIONS_TFPB": r"^FB\b.*(ALLOCATION|DOTATION)",
    "ALLOCATIONS_TFPNB": r"^FNB\b.*(ALLOCATION|DOTATION)", "ALLOCATIONS_CFE": r"^CFE\b.*(ALLOCATION|DOTATION)",
    "ALLOCATIONS_TP": r"^TP\b.*(ALLOCATION|DOTATION)", "DCRTP": r"\bDCRTP\b",
    "FNGIR_REVERSEMENT": r"\b(RE)?VERSEMENT GIR\b", "FNGIR_PRELEVEMENT": r"\bPRELEVEMENT GIR\b",
    "TVA": r"\bFRACTION (DE )?TVA\b", "TVA_TH": r"\bTVA\b.*\bTHP?\b", "TVA_TFPB": r"\bTVA\b.*(\bTFB\b|\bFB\b)",
    "TVA_CVAE": r"\bTVA\b.*\bCVAE\b", "COCO_VERSEMENT": r"COEFFICIENT CORRECTEUR.*\bVERSEMENT\b",
    "COCO_PRELEVEMENT": r"COEFFICIENT CORRECTEUR.*\bPRELEVEMENT\b"}
# Ce que doit dire le titre d'une variable, selon sa grandeur : le montant de l'année, ou, pour une fraction de TVA
# depuis 2023, le montant définitif de l'année précédente et le solde qui en résulte, versé ou repris dans l'année.
TITRES_GRANDEURS = {"definitif_precedent": r"\bDEFINITIVE? N-1\b", "solde_precedent": r"\bSOLDE\b"}
GRANDEURS = ["montant", "definitif_precedent", "solde_precedent"]
SIREN = re.compile(r"[0-9]{9}")


def retenues(exercice, variables, referentiel, lieu):
    """Les variables qu'une année du REI permet de lire, d'après le référentiel : {code: (versement, niveau, grandeur)}.
    Chaque variable doit figurer au tracé de l'année et son titre y dire sa nature, son niveau et sa grandeur ; une
    nature, un niveau et une grandeur n'ont qu'une variable chaque année."""
    titres = {c: rei.normaliser(titre) for c, _, titre, _ in variables}
    resultat, vus = {}, {}
    for v in referentiel:
        if not v["premier_exercice"] <= exercice <= v["dernier_exercice"]:
            continue
        cle = (v["versement"], v["niveau"], v["grandeur"])
        if v["code"] not in titres:
            sys.exit(f"{lieu} : la variable {v['code']} ({', '.join(cle)}) n'est pas au tracé de {exercice}")
        titre = titres[v["code"]]
        if not re.search(TITRES_VERSEMENTS[v["versement"]], titre):
            sys.exit(f"{lieu} : le titre de la variable {v['code']} au tracé de {exercice}, « {titre} », ne dit pas sa "
                     f"nature ({v['versement']})")
        if not re.search(TITRES_NIVEAUX[v["niveau"]], titre):
            sys.exit(f"{lieu} : le titre de la variable {v['code']} au tracé de {exercice}, « {titre} », ne dit pas son "
                     f"niveau ({v['niveau']})")
        autres = [g for g, motif in TITRES_GRANDEURS.items() if re.search(motif, titre)]
        if autres != ([] if v["grandeur"] == "montant" else [v["grandeur"]]):
            sys.exit(f"{lieu} : le titre de la variable {v['code']} au tracé de {exercice}, « {titre} », ne dit pas sa "
                     f"grandeur ({v['grandeur']})")
        if cle in vus or v["code"] in resultat:
            sys.exit(f"{lieu} : deux lignes du référentiel pour {', '.join(cle)} ou pour {v['code']} en {exercice}")
        vus[cle] = v["code"]
        resultat[v["code"]] = cle
    return resultat


def collectivite(niveau, commune, valeurs):
    """La collectivité d'un montant de ce niveau sur la ligne d'une commune, ou "" si la ligne n'en nomme pas."""
    if niveau == "commune":
        return commune
    if niveau in ("groupement", "metropole_lyon"):
        return valeurs.get("SIREPCI", "").strip()
    if niveau == "ept_ou_groupement":
        return valeurs.get("SIREPT", "").strip() or valeurs.get("SIREPCI", "").strip()
    if niveau == "departement":
        return rei.complete("DEP", rei.valeur(valeurs, "DEP"))
    return rei.complete("REG", valeurs["REG"])  # région, collectivité territoriale unique


class Collecte:
    """Les versements d'une année du REI, ligne de commune après ligne de commune : `ajouter` chaque ligne, puis
    `resultat`."""

    def __init__(self, exercice, variables, referentiel, lieu):
        self.exercice, self.lieu = exercice, lieu
        self.retenues = retenues(exercice, variables, referentiel, lieu)
        # (versement, niveau, grandeur, collectivité) → [montants non nuls distincts, communes qui les donnent]
        self.montants = collections.defaultdict(lambda: [set(), 0])

    def ajouter(self, commune, valeurs):
        for code, (versement, niveau, grandeur) in self.retenues.items():
            texte = valeurs[code].strip()
            if not texte or not float(texte):
                continue
            qui = collectivite(niveau, commune, valeurs)
            if not qui or (niveau in ("groupement", "ept_ou_groupement", "metropole_lyon")
                           and not SIREN.fullmatch(qui)):
                sys.exit(f"{self.lieu}, commune {commune} : {code} donne {texte} sans désigner de collectivité "
                         f"({niveau} « {qui} »)")
            entree = self.montants[(versement, niveau, grandeur, qui)]
            entree[0].add(float(texte))
            entree[1] += 1

    def resultat(self):
        """[(versement, niveau, grandeur, collectivité, montant, communes qui le donnent)], dans l'ordre ; deux montants
        différents pour une même collectivité arrêtent la lecture."""
        lignes = []
        for (versement, niveau, grandeur, qui), (valeurs, communes) in sorted(self.montants.items()):
            if len(valeurs) > 1:
                sys.exit(f"{self.lieu} : {versement} ({niveau}, {grandeur}) de {qui} vaut "
                         f"{', '.join(map(str, sorted(valeurs)))} selon ses communes")
            lignes.append((versement, niveau, grandeur, qui, valeurs.pop(), communes))
        return lignes


def collecter(exercice, variables, lignes, referentiel, lieu):
    """Les versements d'une année du REI, à partir de ses lignes de communes (importer_rei.lignes_communes)."""
    collecte = Collecte(exercice, variables, referentiel, lieu)
    for commune, valeurs in lignes:
        collecte.ajouter(commune, valeurs)
    return collecte.resultat()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    copies = [i for i in lire("tables/fichiers_rei.csv") if i["exercice"] == sys.argv[1]]
    if not copies:
        sys.exit(f"aucune copie du REI pour {sys.argv[1]}")
    inscrit = max(copies, key=lambda i: i["version"])
    fichier = fichiers[inscrit["fichier_id"]]
    exercice, variables, _, lignes = rei.lignes_communes(fichier)
    totaux = collections.defaultdict(lambda: [0, 0.0])
    for versement, niveau, grandeur, _, montant, _ in collecter(exercice, variables, lignes,
                                                                lire("tables/variables_versements_rei.csv"),
                                                                fichier["id"]):
        totaux[(versement, niveau, grandeur)][0] += 1
        totaux[(versement, niveau, grandeur)][1] += montant
    for (versement, niveau, grandeur), (n, total) in sorted(totaux.items()):
        print(f"{exercice} {versement:18} {niveau:20} {grandeur:20} {n:6} collectivités {total / 1e6:12.1f} M€")


if __name__ == "__main__":
    main()
