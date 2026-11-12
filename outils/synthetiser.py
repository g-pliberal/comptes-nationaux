#!/usr/bin/env python3
"""Écrit la synthèse lisible de la base : les grands chiffres des comptes publics, chacun avec sa source.

    python3 outils/synthetiser.py

Écrit SYNTHESE.md à la racine du dépôt, à partir des seules tables de chiffres. Chaque nombre est un chiffre publié
par sa source, dans sa version la plus récente, arrondi à l'affichage ; seules les parts en % d'un total sont
calculées ici, à partir des chiffres publiés. Un chiffre que la base n'a pas s'écrit « — ».
"""

import collections

from commun import RACINE, lire, ressources_chiffres

SYNTHESE = RACINE / "SYNTHESE.md"
EN_MILLIARDS = {"EUR": 1e-9, "K_EUR": 1e-6, "MIO_EUR": 1e-3, "MD_EUR": 1}

SOUS_SECTEURS = [("S13111", "État"), ("S13112", "Organismes divers d'administration centrale"),
                 ("S1313", "Administrations publiques locales"), ("S1314", "Administrations de sécurité sociale"),
                 ("S13", "**Ensemble des administrations publiques**")]
# (concept, libellé, retrait) : une ligne en retrait est une partie de la ligne sans retrait qui la précède.
NATURES = [("INSEE_APU.DEP_FONCTIONNEMENT", "Dépenses de fonctionnement", 0),
           ("SEC2010.D1PAY", "dont rémunération des salariés", 1),
           ("SEC2010.P2", "dont consommations intermédiaires", 1),
           ("INSEE_APU.DEP_PRESTATIONS_TRANSFERTS", "Prestations et autres transferts", 0),
           ("SEC2010.D62PAY", "dont prestations sociales en espèces", 1),
           ("SEC2010.D632PAY", "dont transferts sociaux en nature de produits marchands (soins de ville, "
                               "médicaments, aides au logement…)", 1),
           ("SEC2010.D3PAY", "dont subventions", 1),
           ("SEC2010.D41PAY", "Intérêts versés", 0),
           ("INSEE_APU.DEP_ACTIFS_NON_FINANCIERS", "Acquisitions moins cessions d'actifs non financiers", 0),
           ("SEC2010.P51G", "dont formation brute de capital fixe (investissement)", 1),
           ("SEC2010.TE", "**Dépenses totales**", 0)]
RECETTES = [("INSEE_APU.REC_IMPOTS_COTISATIONS", "Impôts et cotisations sociales", 0),
            ("SEC2010.D2REC", "dont impôts sur la production et les importations (TVA, accises, taxes foncières…)", 1),
            ("SEC2010.D5REC", "dont impôts courants sur le revenu et le patrimoine (impôt sur le revenu, CSG, impôt sur "
                              "les sociétés…)", 1),
            ("SEC2010.D61REC", "dont cotisations sociales nettes", 1),
            ("SEC2010.D91REC", "dont impôts en capital (droits de succession et de donation)", 1),
            ("INSEE_APU.REC_PRODUCTION", "Recettes de production", 0),
            ("INSEE_APU.REC_REVENUS_PROPRIETE", "Revenus de la propriété", 0),
            ("INSEE_APU.REC_AUTRES_TRANSFERTS", "Autres transferts reçus", 0),
            ("SEC2010.TR", "**Recettes totales**", 0)]
PRELEVEMENTS = [("INSEE_PO.COTISATIONS_EFFECTIVES", "Cotisations sociales effectives"),
                ("SEC2010.D211REC", "Taxe sur la valeur ajoutée (TVA)"),
                ("INSEE_PO.CSG", "Contribution sociale généralisée (CSG)"),
                ("INSEE_PO.IRPP", "Impôt sur le revenu, avant crédits d'impôt"),
                ("INSEE_PO.IS", "Impôt sur les sociétés, avant crédits d'impôt"),
                ("INSEE_PO.TAXE_FONCIERE", "Taxe foncière"),
                ("INSEE_PO.TICPE", "Accises sur les produits énergétiques (TICPE)"),
                ("INSEE_PO.DMTG", "Droits de succession et de donation"),
                ("INSEE_PO.TAXE_SALAIRES", "Taxe sur les salaires"),
                ("INSEE_PO.PO", "**Ensemble des prélèvements obligatoires**")]
BRANCHES = [("COMPTES_SECU.MALADIE", "Maladie"), ("COMPTES_SECU.AT_MP", "Accidents du travail et maladies "
                                                                         "professionnelles"),
            ("COMPTES_SECU.VIEILLESSE", "Vieillesse"), ("COMPTES_SECU.FAMILLE", "Famille"),
            ("COMPTES_SECU.AUTONOMIE", "Autonomie"), ("", "**Ensemble des régimes de base**")]
NIVEAUX = [("COMMUNES_BP_BA", "Communes"), ("GFP_BP_BA", "Groupements de communes à fiscalité propre"),
           ("DEPARTEMENTS_BP_BA", "Départements"), ("REGIONS_CTU_BP_BA", "Régions et collectivités territoriales uniques"),
           ("SYNDICATS_BP_BA", "Syndicats"),
           ("COLLECTIVITES_LOCALES_BP_BA", "**Ensemble, sans double compte**")]
VERSANTS = [("FPE", "Fonction publique de l'État"), ("FPT", "Fonction publique territoriale"),
            ("FPH", "Fonction publique hospitalière"), ("FP", "**Ensemble**")]
PRODUCTEURS = {"insee": "Insee", "eurostat": "Eurostat", "senat": "Sénat (textes de loi)",
               "an": "Assemblée nationale (textes de loi)", "ccomptes": "Cour des comptes", "dgafp": "DGAFP",
               "dgcl": "DGCL", "drees": "DREES", "ofgl": "OFGL", "tiers": "Chiffres cités par des tiers"}


def fr(x, decimales=1, signe=False):
    texte = format(x, f"{'+' if signe else ''},.{decimales}f")
    return texte.replace(",", " ").replace(".", ",").replace("-", "−")


class Base:
    """Les chiffres publiés, dans leur version la plus récente, et le relevé de ceux que chaque partie cite."""

    def __init__(self):
        self.derniers, self.cites, self.nombre = {}, [], 0
        self.par_producteur = collections.defaultdict(lambda: [set(), 0, set()])
        for r in ressources_chiffres():
            for l in lire(r["path"]):
                self.nombre += 1
                producteur = self.par_producteur[l["source_id"].split(".")[0] if l["nature"] != "cite" else "tiers"]
                producteur[0].add(l["source_id"])
                producteur[1] += 1
                producteur[2].add(l["periode"][:4])
                if l["nature"] != "publie" or l["traitements"]:
                    continue
                cle = (l["perimetre_id"], l["concept_id"], l["fonction_id"], l["unite_id"], l["periode"])
                self.derniers.setdefault(cle, []).append(l)

    def chiffre(self, perimetre, concept, periode, unites=("MD_EUR",), fonction="", sources=()):
        """Le chiffre de cette fiche dans sa version la plus récente, chez les sources dont l'identifiant commence par
        l'un de `sources` (toutes à défaut), dans la première des unités où il existe ; None s'il n'existe pas."""
        for unite in unites:
            lignes = [l for l in self.derniers.get((perimetre, concept, fonction, unite, str(periode)), [])
                      if not sources or l["source_id"].startswith(tuple(sources))]
            if lignes:
                ligne = max(lignes, key=lambda l: (l["version"], l["source_id"]))
                self.cites.append(ligne)
                return ligne
        return None

    def valeur(self, *fiche, **options):
        """La valeur du chiffre, en milliards d'euros pour un montant ; None s'il n'existe pas."""
        ligne = self.chiffre(*fiche, **options)
        return None if ligne is None else float(ligne["valeur"]) * EN_MILLIARDS.get(ligne["unite_id"], 1)

    def annees(self, perimetre, concept, unite="MD_EUR", fonction="", sources=()):
        """Les années pour lesquelles la base a ce chiffre."""
        return sorted(p for (per, c, f, u, p), lignes in self.derniers.items()
                      if (per, c, f, u) == (perimetre, concept, fonction, unite) and len(p) == 4
                      and (not sources or any(l["source_id"].startswith(tuple(sources)) for l in lignes)))

    def sources_citees(self, titres):
        """La ligne « Source » d'une partie : les sources des chiffres cités depuis le dernier appel, avec leur version."""
        versions = collections.defaultdict(set)
        for l in self.cites:
            versions[l["source_id"]].add(l["version"])
        self.cites = []
        if not versions:
            return []
        if len(versions) > 6:
            producteurs = sorted({s.split(".")[0] for s in versions})
            return [f"Sources : {len(versions)} publications ("
                    + ", ".join(f"{PRODUCTEURS.get(p, p)} : `base/tables/chiffres/{p}/`" for p in producteurs) + ").", ""]
        cites = []
        for s, v in sorted(versions.items()):
            titre = titres[s]
            if s.startswith("insee.t"):  # « Tableau 3.101 : Dette des administrations… » → « Insee, tableau 3.101 »
                titre = "Insee, t" + titre.split(" : ")[0][1:]
            cites.append(f"{titre} (`{s}`, version du {max(v)})")
        return [f"Source{'s' if len(cites) > 1 else ''} : " + " ; ".join(cites) + ".", ""]


def n(x, decimales=1, signe=False):
    return "—" if x is None else fr(x, decimales, signe)


def part(x, total):
    return "—" if x is None or not total else fr(100 * x / total, 1)


def retrait(libelle, niveau):
    return ("&nbsp;&nbsp;&nbsp;&nbsp;" * niveau) + libelle


def partie_essentiel(base, annee):
    apu = lambda c, u, s: base.valeur("S13", c, annee, (u,), sources=(s,))
    lignes = [f"## L'essentiel en {annee}", "",
              "L'ensemble des administrations publiques : l'État, les organismes qui en dépendent, les collectivités "
              "locales et la sécurité sociale, au sens des comptes nationaux (SEC 2010).", "",
              "| | Milliards d'euros | % du PIB |", "|---|---:|---:|"]
    for libelle, concept, source in [("Dépenses", "SEC2010.TE", "insee.t3215"), ("Recettes", "SEC2010.TR", "insee.t3215"),
                                     ("Solde (un déficit est négatif)", "SEC2010.B9", "insee.t3106"),
                                     ("Dette au sens de Maastricht, en fin d'année", "PDE.GD", "insee.t3101")]:
        signe = concept == "SEC2010.B9"
        lignes.append(f"| {libelle} | {n(apu(concept, 'MD_EUR', source), 1, signe)} | "
                      f"{n(apu(concept, 'PC_PIB', source), 1, signe)} |")
    po = lambda u: base.valeur("S13_S212", "INSEE_PO.PO", annee, (u,), sources=("insee.t3216",))
    lignes.append(f"| Prélèvements obligatoires, y compris ceux que perçoit l'Union européenne | {n(po('MD_EUR'))} | "
                  f"{n(po('PC_PIB'))} |")
    lignes.append(f"| Produit intérieur brut | {n(base.valeur('S1', 'SEC2010.B1GQ', annee, sources=('insee.t3101',)))} | |")
    statut = base.chiffre("S13", "SEC2010.TE", annee, sources=("insee.t3215",))
    etats = {"provisoire": "provisoires", "semi_definitif": "semi-définitifs", "definitif": "définitifs"}
    if statut and statut["statut"] in etats:
        lignes += ["", f"Les comptes de {annee} sont {etats[statut['statut']]}."]
    return lignes + [""]


def partie_histoire(base, titres):
    annees_ = base.annees("S13", "SEC2010.TE", sources=("insee.t3215",))
    if not annees_:
        return []
    lignes = [f"## De {annees_[0]} à {annees_[-1]}", "",
              "Les mêmes grandeurs, année par année, en milliards d'euros courants et en % du PIB.", "",
              "| Année | Dépenses | % du PIB | Recettes | % du PIB | Solde | % du PIB | Dette | % du PIB |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for a in annees_:
        cases = []
        for concept, source, signe in [("SEC2010.TE", "insee.t3215", False), ("SEC2010.TR", "insee.t3215", False),
                                       ("SEC2010.B9", "insee.t3106", True), ("PDE.GD", "insee.t3101", False)]:
            cases += [n(base.valeur("S13", concept, a, (u,), sources=(source,)), 1, signe) for u in ("MD_EUR", "PC_PIB")]
        lignes.append(f"| {a} | " + " | ".join(cases) + " |")
    return lignes + [""] + base.sources_citees(titres)


def partie_sous_secteurs(base, annee, titres):
    lignes = [f"## Qui dépense : les sous-secteurs en {annee}", "",
              "En milliards d'euros. Les dépenses et les recettes d'un sous-secteur comprennent ce qu'il verse aux autres "
              "administrations et ce qu'il en reçoit : leur somme dépasse celles de l'ensemble, où ces transferts "
              "s'annulent.", "",
              "| Sous-secteur | Dépenses | Recettes | Solde | Dette |", "|---|---:|---:|---:|---:|"]
    for perimetre, libelle in SOUS_SECTEURS:
        v = lambda c, s: base.valeur(perimetre, c, annee, sources=(s,))
        lignes.append(f"| {libelle} | {n(v('SEC2010.TE', 'insee.t3215'))} | {n(v('SEC2010.TR', 'insee.t3215'))} | "
                      f"{n(v('SEC2010.B9', 'insee.t3106'), 1, True)} | {n(v('PDE.GD', 'insee.t3101'))} |")
    return lignes + [""] + base.sources_citees(titres)


def partie_ventilation(base, annee, titre, intro, postes, total, perimetre, source, titres):
    """Un tableau des postes d'une dépense ou d'une recette de l'année, avec la part de chacun dans le total."""
    reference = base.valeur(perimetre, total, annee, sources=(source,))
    lignes = [f"## {titre}", "", intro, "", "| | Milliards d'euros | % du total |", "|---|---:|---:|"]
    for concept, libelle, niveau in postes:
        v = base.valeur(perimetre, concept, annee, sources=(source,))
        lignes.append(f"| {retrait(libelle, niveau)} | {n(v)} | {part(v, reference)} |")
    return lignes + [""] + base.sources_citees(titres)


def partie_fonctions(base, titres):
    annees_ = base.annees("S13", "SEC2010.TE", sources=("insee.t3301",))
    if not annees_:
        return []
    annee = annees_[-1]
    fonctions = {f["id"]: f["libelle"] for f in lire("tables/fonctions.csv")}
    v = lambda f: base.valeur("S13", "SEC2010.TE", annee, fonction=f, sources=("insee.t3301",))
    total = v("")
    divisions = sorted((f for f in fonctions if len(f) == 4 and f.startswith("GF")), key=lambda f: -(v(f) or 0))
    lignes = [f"## À quoi sert la dépense : les fonctions en {annee}", "",
              f"La dépense de l'ensemble des administrations publiques selon les dix fonctions de la classification "
              f"internationale COFOG, de la plus grande à la plus petite ; {annee} est la dernière année publiée.", "",
              "| Fonction | Milliards d'euros | % du total |", "|---|---:|---:|"]
    lignes += [f"| {fonctions[f]} | {n(v(f))} | {part(v(f), total)} |" for f in divisions]
    lignes.append(f"| **Dépenses totales** | {n(total)} | {part(total, total)} |")
    return lignes + [""] + base.sources_citees(titres)


def partie_prelevements(base, annee, titres):
    v = lambda c: base.valeur("S13_S212", c, annee, sources=("insee.t3217",))
    total = v("INSEE_PO.PO")
    lignes = [f"## Les principaux prélèvements en {annee}", "",
              "Les plus gros impôts et cotisations, tous bénéficiaires confondus, institutions de l'Union européenne "
              "comprises.", "", "| | Milliards d'euros | % des prélèvements obligatoires |", "|---|---:|---:|"]
    lignes += [f"| {libelle} | {n(v(c))} | {part(v(c), total)} |" for c, libelle in PRELEVEMENTS]
    return lignes + [""] + base.sources_citees(titres)


def partie_budget_etat(base, titres):
    lois = ("senat.", "an.")
    annees_ = sorted(set(base.annees("ETAT_LF", "LOLF.SOLDE_BUDGET_GENERAL_LFI", "MIO_EUR", sources=lois))
                     | set(base.annees("ETAT_LF", "LOLF.SOLDE_BUDGET_GENERAL", "EUR", sources=lois)))
    if not annees_:
        return []
    lignes = ["## Le budget de l'État : voté et exécuté", "",
              "Le solde du budget général de l'État, en milliards d'euros, en comptabilité budgétaire : celui que prévoit "
              "la loi de finances initiale, puis celui que constate la loi qui approuve les comptes de l'année. Ce solde "
              "n'est pas le déficit de l'État au sens des comptes nationaux, qui suit d'autres règles.", "",
              "| Année | Solde prévu par la loi de finances initiale | Solde exécuté | Exécuté − prévu |",
              "|---|---:|---:|---:|"]
    for a in annees_:
        prevu = base.valeur("ETAT_LF", "LOLF.SOLDE_BUDGET_GENERAL_LFI", a, ("MIO_EUR",), sources=lois)
        execute = base.valeur("ETAT_LF", "LOLF.SOLDE_BUDGET_GENERAL", a, ("EUR",), sources=lois)
        ecart = None if prevu is None or execute is None else execute - prevu
        lignes.append(f"| {a} | {n(prevu, 1, True)} | {n(execute, 1, True)} | {n(ecart, 1, True)} |")
    lignes += ["", "La dernière colonne est calculée ici. Les lois de finances rectificatives, que la base enregistre "
               "aussi, révisent la prévision en cours d'année.", ""]
    return lignes + base.sources_citees(titres)


def partie_secu(base, titres):
    annees_ = base.annees("ROBSS", "COMPTES_SECU.RESULTAT_COMPTABLE")
    if not annees_:
        return []
    annee = annees_[-1]
    lignes = [f"## La sécurité sociale : les régimes de base en {annee}", "",
              "Les recettes, les dépenses et le résultat de l'ensemble des régimes obligatoires de base de sécurité "
              "sociale, par branche, en milliards d'euros, tels que les approuve la loi. Les transferts entre branches "
              "s'annulent dans l'ensemble, qui n'est donc pas la somme des branches.", "",
              "| Branche | Recettes | Dépenses | Résultat |", "|---|---:|---:|---:|"]
    for branche, libelle in BRANCHES:
        v = lambda c: base.valeur("ROBSS", c, annee, fonction=branche)
        lignes.append(f"| {libelle} | {n(v('COMPTES_SECU.RECETTES'))} | {n(v('COMPTES_SECU.DEPENSES'))} | "
                      f"{n(v('COMPTES_SECU.RESULTAT_COMPTABLE'), 1, True)} |")
    fsv = base.valeur("ROBSS_FSV", "COMPTES_SECU.RESULTAT_COMPTABLE", annee)
    if fsv is not None:
        lignes += ["", f"Avec le Fonds de solidarité vieillesse, le résultat est de {fr(fsv, 1, True)} milliards "
                   f"d'euros."]
    lignes += ["", "Le résultat de l'ensemble des régimes de base, année par année :", "",
               "| Année | " + " | ".join(annees_) + " |", "|---" * (len(annees_) + 1) + "|",
               "| Résultat | " + " | ".join(n(base.valeur("ROBSS", "COMPTES_SECU.RESULTAT_COMPTABLE", a), 1, True)
                                             for a in annees_) + " |", ""]
    return lignes + base.sources_citees(titres)


def partie_collectivites(base, titres):
    ofgl = ("ofgl.annexe-2c", "ofgl.annexe-2d")
    annees_ = base.annees("COLLECTIVITES_LOCALES_BP_BA", "COMPTES_LOCAUX.DEP_TOTALES_HORS_REMBOURSEMENTS", sources=ofgl)
    if not annees_:
        return []
    annee = annees_[-1]
    lignes = [f"## Les collectivités locales en {annee}", "",
              "Les comptes des collectivités locales, budgets principaux et annexes consolidés, en milliards d'euros, "
              "d'après l'Observatoire des finances et de la gestion publique locales. Ce sont leurs comptes propres, pas "
              "le sous-secteur des comptes nationaux. Les versements entre niveaux s'annulent dans l'ensemble, qui n'est "
              "donc pas la somme des niveaux.", "",
              "| Niveau | Dépenses de fonctionnement | Dépenses d'investissement | Dépenses totales, hors "
              "remboursements de dette | Dette |", "|---|---:|---:|---:|---:|"]
    for perimetre, libelle in NIVEAUX:
        v = lambda c: base.valeur(perimetre, f"COMPTES_LOCAUX.{c}", annee, sources=ofgl)
        lignes.append(f"| {libelle} | {n(v('DEP_FONCTIONNEMENT'))} | {n(v('DEP_INVESTISSEMENT'))} | "
                      f"{n(v('DEP_TOTALES_HORS_REMBOURSEMENTS'))} | {n(v('DETTE'))} |")
    return lignes + [""] + base.sources_citees(titres)


def partie_fonction_publique(base, titres):
    concept = "FONCTION_PUBLIQUE.EFFECTIFS_PHYSIQUES"
    annees_ = base.annees("FP", concept, "K_PERSONNES")
    if not annees_:
        return []
    reperes = [a for a in annees_ if a == annees_[0] or a == annees_[-1] or int(a) % 5 == 0]
    v = lambda p, a: base.valeur(p, concept, a, ("K_PERSONNES",))
    lignes = ["## La fonction publique", "",
              "Les agents des trois versants de la fonction publique au 31 décembre, en milliers de personnes, hors "
              "bénéficiaires de contrats aidés, d'après la DGAFP. La série a des ruptures, que disent les notes des "
              "chiffres.", "", "| Versant | " + " | ".join(reperes) + " |", "|---" + "|---:" * len(reperes) + "|"]
    lignes += [f"| {libelle} | " + " | ".join(n(v(p, a), 0) for a in reperes) + " |" for p, libelle in VERSANTS]
    return lignes + [""] + base.sources_citees(titres)


def partie_contenu(base):
    lignes = ["## Ce que contient la base", "",
              f"{fr(base.nombre, 0)} chiffres enregistrés un par un, chacun avec sa fiche d'identité et l'endroit exact où "
              f"le relire dans la copie archivée de sa source :", "",
              "| Producteur | Publications | Chiffres | Années couvertes |", "|---|---:|---:|---|"]
    for producteur, (sources, nombre, annees_) in sorted(base.par_producteur.items(), key=lambda p: -p[1][1]):
        lignes.append(f"| {PRODUCTEURS.get(producteur, producteur)} | {len(sources)} | {fr(nombre, 0)} | "
                      f"{min(annees_)}-{max(annees_)} |")
    copies = {c: sum(int(f["lignes"]) for f in lire(f"tables/{t}.csv") if f.get("contenu", c) == c)
              for t, c in [("fichiers_collectivites", "montants"), ("fichiers_comptes_individuels", "comptes"),
                           ("fichiers_balances_etat", "balance")]}
    communes = sum(int(f["communes"]) for f in lire("tables/fichiers_rei.csv"))
    lignes += ["", "S'y ajoutent, lus dans les copies archivées quand la base se construit :", "",
               f"- {fr(copies['montants'], 0)} lignes de comptes, de fiscalité et de dotations de chaque collectivité "
               f"locale, d'après l'OFGL ;",
               f"- {fr(copies['comptes'], 0)} lignes de collectivités dans les comptes individuels de la DGFiP ;",
               f"- {fr(copies['balance'], 0)} lignes des balances des comptes de l'État ;",
               f"- {fr(communes, 0)} lignes de communes dans le recensement des éléments d'imposition (REI).", "",
               f"Le tout repose sur {fr(len(lire('tables/fichiers.csv')), 0)} copies archivées des sources, dont "
               f"l'empreinte prouve qu'elles sont intactes. Le détail de chaque table est dans "
               f"[base/README.md](base/README.md), les contrôles de cohérence dans "
               f"[controles/coherence.md](controles/coherence.md)."]
    return lignes


def synthese():
    base = Base()
    titres = {s["id"]: s["titre"] for s in lire("tables/sources.csv")}
    annees_ = base.annees("S13", "SEC2010.TE", sources=("insee.t3215",))
    annee = annees_[-1] if annees_ else ""
    lignes = ["# Synthèse des comptes publics de la France", "",
              "Fichier généré par `outils/synthetiser.py` à partir de la base : ne pas le modifier à la main.", "",
              "Les grands chiffres des comptes publics, tels que les publient leurs sources. Chaque nombre est un "
              "chiffre de la base, dans la version la plus récente de sa source, arrondi ici à l'affichage ; seules les "
              "parts en % d'un total, et une colonne d'écart signalée comme telle, sont calculées. Un déficit s'écrit "
              "avec le signe « − ». Pour relire un chiffre dans sa source, le chercher dans la table de la source "
              "citée sous chaque tableau (`base/tables/chiffres/<producteur>/<tableau>.csv`), qui donne son emplacement "
              "exact dans la copie archivée.", ""]
    if annee:
        lignes += partie_essentiel(base, annee) + base.sources_citees(titres) + partie_histoire(base, titres)
        lignes += partie_sous_secteurs(base, annee, titres)
        lignes += partie_ventilation(
            base, annee, f"Ce que les administrations dépensent : la nature des dépenses en {annee}",
            "Les dépenses de l'ensemble des administrations publiques selon leur nature.", NATURES, "SEC2010.TE", "S13",
            "insee.t3201", titres)
        lignes += partie_fonctions(base, titres)
        lignes += partie_ventilation(
            base, annee, f"D'où vient l'argent : les recettes en {annee}",
            "Les recettes de l'ensemble des administrations publiques.", RECETTES, "SEC2010.TR", "S13", "insee.t3201",
            titres)
        lignes += partie_prelevements(base, annee, titres)
    lignes += partie_budget_etat(base, titres) + partie_secu(base, titres) + partie_collectivites(base, titres)
    lignes += partie_fonction_publique(base, titres) + partie_contenu(base)
    return "\n".join(lignes).rstrip("\n") + "\n"


if __name__ == "__main__":
    SYNTHESE.write_text(synthese(), encoding="utf-8")
    print(f"écrit : {SYNTHESE.relative_to(RACINE)}")
