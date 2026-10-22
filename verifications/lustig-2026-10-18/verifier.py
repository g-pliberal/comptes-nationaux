#!/usr/bin/env python3
"""Vérification des chiffres de l'article « The French state crowded out by
government spending » (Hanno Lustig, The Two Cents, 18 octobre 2026).

Recalcule chaque chiffre vérifiable de l'article à partir des données publiques
d'Eurostat et de l'OCDE archivées dans sources/, puis écrit resultats.md.

    python3 verifier.py                # recalcule à partir des fichiers archivés
    python3 verifier.py --telecharger  # télécharge de nouveau les sources, puis recalcule

Seule la bibliothèque standard de Python est utilisée.
"""

import argparse
import csv
import datetime
import hashlib
import json
import pathlib
import sys
import urllib.parse
import urllib.request

ICI = pathlib.Path(__file__).resolve().parent
DOSSIER_SOURCES = ICI / "sources"
MANIFESTE = DOSSIER_SOURCES / "manifeste.csv"
RESULTATS = ICI / "resultats.md"

ARTICLE = "https://thetwocents.substack.com/p/the-french-state-crowded-out-by-government"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
OCDE_SOCX = ("https://sdmx.oecd.org/public/rest/data/OECD.ELS.SPD,DSD_SOCX_AGG@DF_PUB_PRV,1.0/"
             "FRA.A.SOCX.PT_B1GQ.ES10._T._T._Z?startPeriod=1980&format=csvfile")

# Certains serveurs (dont celui de l'OCDE) refusent l'agent par défaut de Python.
AGENT = "comptes-nationaux/verifier (+https://github.com/g-pliberal/comptes-nationaux)"

FONCTIONS = [f"GF{n:02d}" for n in range(1, 11)]
SOUS_SECTEURS = ["S1311", "S1313", "S1314"]  # administrations centrales, locales, de sécurité sociale


def requete_eurostat(jeu, **filtres):
    params = [(cle, valeur) for cle, valeurs in filtres.items() for valeur in valeurs]
    return f"{EUROSTAT}/{jeu}?{urllib.parse.urlencode(params)}"


TELECHARGEMENTS = {
    "eurostat_gov_10a_exp.json": requete_eurostat(
        "gov_10a_exp", geo=["FR"], unit=["MIO_EUR"], sector=["S13", *SOUS_SECTEURS],
        na_item=["TE", "D1", "D3"],
        cofog99=["TOTAL", *FONCTIONS, "GF0107", "GF0405", "GF1001", "GF1002", "GF1003"], lang=["en"]),
    "eurostat_gov_10a_main.json": requete_eurostat(
        "gov_10a_main", geo=["FR"], unit=["MIO_EUR"], sector=["S13", *SOUS_SECTEURS],
        na_item=["TE", "B9", "D1PAY", "D41PAY", "D61REC", "D611REC", "D613REC"], lang=["en"]),
    "eurostat_nama_10_gdp.json": requete_eurostat(
        "nama_10_gdp", geo=["FR"], unit=["CP_MEUR"], na_item=["B1GQ"], lang=["en"]),
    "ocde_socx_france.csv": OCDE_SOCX,
}


# --- Archivage et intégrité ---------------------------------------------------

def empreinte(chemin):
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def telecharger():
    DOSSIER_SOURCES.mkdir(exist_ok=True)
    lignes = []
    for fichier, url in TELECHARGEMENTS.items():
        requete = urllib.request.Request(url, headers={"User-Agent": AGENT})
        with urllib.request.urlopen(requete, timeout=120) as reponse:
            contenu = reponse.read()
        chemin = DOSSIER_SOURCES / fichier
        chemin.write_bytes(contenu)
        lignes.append({
            "fichier": fichier,
            "url": url,
            "telecharge_le": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sha256": empreinte(chemin),
            "octets": len(contenu),
        })
        print(f"téléchargé : {fichier} ({len(contenu)} octets)")
    with MANIFESTE.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=list(lignes[0]))
        ecrivain.writeheader()
        ecrivain.writerows(lignes)


def lire_manifeste():
    """Vérifie que chaque fichier archivé est intact avant tout calcul."""
    with MANIFESTE.open(newline="", encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    for ligne in lignes:
        chemin = DOSSIER_SOURCES / ligne["fichier"]
        if not chemin.exists():
            sys.exit(f"fichier archivé manquant : {chemin}")
        if empreinte(chemin) != ligne["sha256"]:
            sys.exit(f"empreinte différente du manifeste, fichier modifié : {chemin}")
    return lignes


# --- Lecture des sources --------------------------------------------------------

def lire_jsonstat(chemin):
    """Renvoie (dimensions, {tuple de codes: valeur}, date de mise à jour) d'un fichier JSON-stat 2.0."""
    jeu = json.loads(chemin.read_text(encoding="utf-8"))
    dims, tailles = jeu["id"], jeu["size"]
    codes = {d: {pos: code for code, pos in jeu["dimension"][d]["category"]["index"].items()} for d in dims}
    valeurs = {}
    for position, valeur in jeu["value"].items():
        n, cle = int(position), []
        for d, taille in zip(reversed(dims), reversed(tailles)):
            cle.append(codes[d][n % taille])
            n //= taille
        valeurs[tuple(reversed(cle))] = valeur
    return dims, valeurs, jeu.get("updated")


class Donnees:
    def __init__(self):
        self.dims_exp, self.exp, self.maj_exp = lire_jsonstat(DOSSIER_SOURCES / "eurostat_gov_10a_exp.json")
        self.dims_main, self.main, self.maj_main = lire_jsonstat(DOSSIER_SOURCES / "eurostat_gov_10a_main.json")
        self.dims_pib, self.pib_brut, self.maj_pib = lire_jsonstat(DOSSIER_SOURCES / "eurostat_nama_10_gdp.json")
        with (DOSSIER_SOURCES / "ocde_socx_france.csv").open(newline="", encoding="utf-8-sig") as f:
            self.socx = {int(l["TIME_PERIOD"]): float(l["OBS_VALUE"]) for l in csv.DictReader(f) if l["OBS_VALUE"]}

    @staticmethod
    def _valeur(dims, valeurs, **cle):
        return valeurs.get(tuple(cle.get(d, "A" if d == "freq" else None) for d in dims))

    def depense(self, secteur, fonction, operation, annee):
        """gov_10a_exp, millions d'euros ; 0 si la case n'est pas publiée."""
        v = self._valeur(self.dims_exp, self.exp, unit="MIO_EUR", sector=secteur, cofog99=fonction,
                         na_item=operation, geo="FR", time=str(annee))
        return v or 0.0

    def compte(self, secteur, operation, annee):
        """gov_10a_main, millions d'euros."""
        return self._valeur(self.dims_main, self.main, unit="MIO_EUR", sector=secteur, na_item=operation,
                            geo="FR", time=str(annee))

    def pib(self, annee):
        return self._valeur(self.dims_pib, self.pib_brut, unit="CP_MEUR", na_item="B1GQ", geo="FR", time=str(annee))


# --- Méthode de l'article ---------------------------------------------------------

def cotisations_imputees(d, secteur, annee):
    """Cotisations retraite imputées reçues, calculées comme dans l'article : D.61 − D.611 − D.613."""
    return d.compte(secteur, "D61REC", annee) - d.compte(secteur, "D611REC", annee) - d.compte(secteur, "D613REC", annee)


def retrait(d, fonction, annee, secteurs):
    """Part des cotisations imputées comprise dans la rémunération des agents d'une fonction."""
    return sum(cotisations_imputees(d, s, annee) / d.compte(s, "D1PAY", annee) * d.depense(s, fonction, "D1", annee)
               for s in secteurs)


def nette(d, fonctions, annee, secteurs):
    return sum(d.depense("S13", f, "TE", annee) - retrait(d, f, annee, secteurs) for f in fonctions)


def parts_tableau(d, annee):
    """Tableau 1 de l'article : parts de la dépense totale, hors cotisations imputées de l'État."""
    etat = ["S1311"]
    total = nette(d, FONCTIONS, annee, etat)
    parts = {
        "social": nette(d, ["GF07", "GF10"], annee, etat),
        "regalien": nette(d, ["GF09", "GF02", "GF03"], annee, etat),
        "transport": nette(d, ["GF0405"], annee, etat),
        "interets": d.depense("S13", "GF0107", "TE", annee),
        "subventions": d.depense("S13", "TOTAL", "D3", annee) - d.depense("S13", "GF0405", "D3", annee),
    }
    parts = {cle: 100 * v / total for cle, v in parts.items()}
    parts["reste"] = 100 - sum(parts.values())
    return parts


def pct_pib(d, montant, annee):
    return 100 * montant / d.pib(annee)


def social_cofog_pib(d, annee):
    return pct_pib(d, nette(d, ["GF07", "GF10"], annee, ["S1311"]), annee)


def part_retiree(d, fonction, annee):
    return 100 * retrait(d, fonction, annee, SOUS_SECTEURS) / d.depense("S13", fonction, "TE", annee)


# --- Chiffres de l'article ----------------------------------------------------------
# (emplacement dans l'article, libellé, année, valeur publiée, nombre de décimales, recalcul)

AFFIRMATIONS = [
    ("Tableau 1", "Santé et protection sociale, % de la dépense", 1995, 53.1, 1, lambda d: parts_tableau(d, 1995)["social"]),
    ("Tableau 1", "Santé et protection sociale, % de la dépense", 2024, 58.7, 1, lambda d: parts_tableau(d, 2024)["social"]),
    ("Tableau 1", "Éducation, défense, ordre public, % de la dépense", 1995, 15.2, 1, lambda d: parts_tableau(d, 1995)["regalien"]),
    ("Tableau 1", "Éducation, défense, ordre public, % de la dépense", 2024, 13.2, 1, lambda d: parts_tableau(d, 2024)["regalien"]),
    ("Tableau 1", "Transports, % de la dépense", 1995, 5.3, 1, lambda d: parts_tableau(d, 1995)["transport"]),
    ("Tableau 1", "Transports, % de la dépense", 2024, 3.8, 1, lambda d: parts_tableau(d, 2024)["transport"]),
    ("Tableau 1", "Intérêts, % de la dépense", 1995, 6.6, 1, lambda d: parts_tableau(d, 1995)["interets"]),
    ("Tableau 1", "Intérêts, % de la dépense", 2024, 3.6, 1, lambda d: parts_tableau(d, 2024)["interets"]),
    ("Tableau 1", "Subventions hors transports, % de la dépense", 1995, 2.0, 1, lambda d: parts_tableau(d, 1995)["subventions"]),
    ("Tableau 1", "Subventions hors transports, % de la dépense", 2024, 2.7, 1, lambda d: parts_tableau(d, 2024)["subventions"]),
    ("Tableau 1", "Tout le reste, % de la dépense", 1995, 17.7, 1, lambda d: parts_tableau(d, 1995)["reste"]),
    ("Tableau 1", "Tout le reste, % de la dépense", 2024, 18.0, 1, lambda d: parts_tableau(d, 2024)["reste"]),
    ("Note du tableau 1", "Cotisations imputées de l'État, % du PIB", 1995, 1.7, 1, lambda d: pct_pib(d, cotisations_imputees(d, "S1311", 1995), 1995)),
    ("Note du tableau 1", "Cotisations imputées de l'État, % du PIB", 2024, 1.7, 1, lambda d: pct_pib(d, cotisations_imputees(d, "S1311", 2024), 2024)),
    ("Graphique 2", "Éducation, % du PIB, net", 2024, 4.26, 2, lambda d: pct_pib(d, nette(d, ["GF09"], 2024, SOUS_SECTEURS), 2024)),
    ("Graphique 2", "Transports, % du PIB, net", 2024, 2.01, 2, lambda d: pct_pib(d, nette(d, ["GF0405"], 2024, SOUS_SECTEURS), 2024)),
    ("Graphique 2", "Défense, % du PIB, net", 2024, 1.65, 2, lambda d: pct_pib(d, nette(d, ["GF02"], 2024, SOUS_SECTEURS), 2024)),
    ("Graphique 2", "Ordre et sécurité publics, % du PIB, net", 2024, 1.50, 2, lambda d: pct_pib(d, nette(d, ["GF03"], 2024, SOUS_SECTEURS), 2024)),
    ("Note du graphique 2", "Part retirée de l'éducation, %", 2023, 16, 0, lambda d: part_retiree(d, "GF09", 2023)),
    ("Note du graphique 2", "Part retirée de l'ordre public, %", 2023, 15, 0, lambda d: part_retiree(d, "GF03", 2023)),
    ("Note du graphique 2", "Part retirée de la défense, %", 2023, 11, 0, lambda d: part_retiree(d, "GF02", 2023)),
    ("Texte", "Retraites (vieillesse et survivants), % du PIB", 1995, 12.7, 1,
     lambda d: pct_pib(d, d.depense("S13", "GF1002", "TE", 1995) + d.depense("S13", "GF1003", "TE", 1995), 1995)),
    ("Texte", "Retraites (vieillesse et survivants), % du PIB", 2024, 14.8, 1,
     lambda d: pct_pib(d, d.depense("S13", "GF1002", "TE", 2024) + d.depense("S13", "GF1003", "TE", 2024), 2024)),
    ("Texte", "Dépenses sociales, moyenne des quinze années, % du PIB (OCDE)", "1994-2008", 28.5, 1,
     lambda d: sum(d.socx[a] for a in range(1994, 2009)) / 15),
    ("Graphique 4", "Solde primaire, % du PIB", 1995, -1.6, 1, lambda d: solde_primaire(d, 1995)),
    ("Graphique 4", "Solde primaire, % du PIB", 2000, 1.7, 1, lambda d: solde_primaire(d, 2000)),
    ("Graphique 4", "Solde primaire, % du PIB", 2019, -0.9, 1, lambda d: solde_primaire(d, 2019)),
    ("Graphique 4", "Solde primaire, % du PIB", 2024, -3.8, 1, lambda d: solde_primaire(d, 2024)),
]

# Dépenses sociales en % du PIB citées dans le texte (année, valeur, décimales),
# comparées aux deux séries possibles.
TEXTE_SOCIAL = [(1980, 20, 0), (1985, 25.6, 1), (1990, 24.6, 1), (1993, 27.3, 1), (2008, 29.6, 1),
                (2009, 31.9, 1), (2014, 32.8, 1), (2020, 36.2, 1), (2023, 32.1, 1)]

ESTIMATIONS_2026 = [
    "part de la santé et de la protection sociale dans la dépense : 59,7 %",
    "part de l'éducation, de la défense et de l'ordre public : 13,7 %",
    "part des transports : 3,8 % ; des intérêts : 4,3 % ; des subventions : 2,5 %",
    "dépenses sociales : environ 33,2 % du PIB ; retraites : 15,0 % du PIB",
    "solde primaire : −3,0 % du PIB (déficit du PLF 2027, intérêts de l'OFCE)",
]

def observations(d, verdicts):
    """Constats tirés des calculs ; les nombres cités sont recalculés, jamais saisis."""
    def liste(filtre):
        return [f"{libelle} ({annee})" for (ou, libelle, annee, *_), v in zip(AFFIRMATIONS, verdicts) if filtre(ou, v)]

    textes = [
        "**Méthode.** L'article retire de chaque fonction les cotisations retraite que l'État s'impute pour ses "
        "fonctionnaires, puisque les pensions versées sont déjà comptées dans la protection sociale. Ce montant est "
        "calculé comme D.61 reçues − D.611 − D.613, puis réparti au prorata de la rémunération des agents de chaque "
        "fonction. L'article le nomme « D612 » : c'est la même somme vue côté recettes ; côté dépenses, le code est "
        "D.122, que son graphique 2 emploie bien.",
    ]
    graphique2 = [v for (ou, *_), v in zip(AFFIRMATIONS, verdicts) if "raphique 2" in ou]
    if all(v == "conforme" for v in graphique2):
        textes.append("**Graphique 2 entièrement reproduit** : ses valeurs 2024 et ses parts retirées en 2023 se "
                      "retrouvent à l'arrondi près.")
    non_reproduits = liste(lambda ou, v: ou == "Tableau 1" and v == "non reproduit")
    if non_reproduits:
        g2 = {libelle.split(",")[0]: publie for ou, libelle, annee, publie, *_ in AFFIRMATIONS if ou == "Graphique 2"}
        total = pct_pib(d, nette(d, FONCTIONS, 2024, SOUS_SECTEURS), 2024)
        regalien = 100 * (g2["Éducation"] + g2["Défense"] + g2["Ordre et sécurité publics"]) / total
        transport = 100 * g2["Transports"] / total
        textes.append(
            f"**Non reproduit dans le tableau 1** : {', '.join(non_reproduits)}. Rapportées au même total, les "
            f"valeurs publiées dans le graphique 2 de l'article donnent, pour 2024, {fr(regalien)} % pour "
            f"l'éducation, la défense et l'ordre public et {fr(transport)} % pour les transports : l'écart est "
            f"interne à l'article. Pour 1995, il ne peut pas venir d'une révision récente des données.")
    ecart_min = min(social_cofog_pib(d, a) - d.socx[a] for a in range(2008, 2025))
    textes.append(
        "**Le texte change de source en cours de route.** Jusqu'à la moyenne des années 1994-2008, ses dépenses "
        "sociales sont celles de l'OCDE (SOCX), comme son graphique 3 ; à partir de 2008, ce sont celles "
        "d'Eurostat (santé et protection sociale de la COFOG), plus larges d'au moins "
        f"{fr(ecart_min)} point de PIB chaque année. Pour 2008, l'OCDE donne {fr(d.socx[2008])} % et Eurostat "
        f"{fr(social_cofog_pib(d, 2008))} % : la marche entre la moyenne citée et le niveau de 2008 vient du "
        "changement de série, pas d'une hausse des dépenses.")
    arrondis = liste(lambda ou, v: v == "à l'arrondi près")
    if arrondis:
        textes.append(f"**À l'arrondi près** : {', '.join(arrondis)}. La valeur recalculée tombe juste sur la "
                      "limite d'arrondi du chiffre publié.")
    unites = liste(lambda ou, v: v == "écart d'une unité")
    if unites:
        textes.append(
            f"**Écart d'une unité du dernier chiffre** : {', '.join(unites)}. Les données archivées ici sont celles "
            f"de la mise à jour d'Eurostat du {d.maj_main[:10]}, postérieure à l'article : ces écarts sont "
            "compatibles avec cette révision des années récentes.")
    return textes


def solde_primaire(d, annee):
    return pct_pib(d, d.compte("S13", "B9", annee) + d.compte("S13", "D41PAY", annee), annee)


def verdict(publie, recalcul, decimales):
    """Compare un recalcul au chiffre publié, en unités de son dernier chiffre affiché."""
    unites = abs(recalcul - publie) / 10 ** -decimales
    if unites <= 0.5 + 1e-9:
        return "conforme"
    if unites <= 0.6:
        return "à l'arrondi près"
    if unites <= 1.0 + 1e-9:
        return "écart d'une unité"
    return "non reproduit"


def fr(x, decimales=1, signe=False):
    texte = f"{x:+.{decimales}f}" if signe else f"{x:.{decimales}f}"
    return texte.replace("-", "−").replace(".", ",")


def ecrire_resultats(d, manifeste):
    lignes = [
        "# Vérification : « The French state crowded out by government spending »",
        "",
        "Fichier généré par `verifier.py` : ne pas le modifier à la main.",
        "",
        f"Article : [{ARTICLE}]({ARTICLE}) (Hanno Lustig, The Two Cents, 18 octobre 2026).",
        "",
        "## Sources archivées",
        "",
        "| Fichier | Téléchargé le | Empreinte SHA-256 (début) |",
        "|---|---|---|",
    ]
    for m in manifeste:
        lignes.append(f"| [{m['fichier']}](sources/{m['fichier']}) | {m['telecharge_le']} | `{m['sha256'][:16]}` |")
    lignes += [
        "",
        f"Mises à jour des jeux Eurostat : gov_10a_exp {d.maj_exp}, gov_10a_main {d.maj_main}, nama_10_gdp {d.maj_pib}.",
        "",
        "## Chiffres de l'article recalculés",
        "",
        "| Où | Chiffre | Année | Article | Recalcul | Écart | Verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    compte, verdicts = {}, []
    for ou, libelle, annee, publie, dec, calcul in AFFIRMATIONS:
        r = calcul(d)
        v = verdict(publie, r, dec)
        verdicts.append(v)
        compte[v] = compte.get(v, 0) + 1
        lignes.append(f"| {ou} | {libelle} | {annee} | {fr(publie, dec)} | {fr(r, max(dec, 2))} | "
                      f"{fr(r - publie, max(dec, 2), signe=True)} | {v} |")
    lignes += [
        "",
        "Bilan : " + " ; ".join(f"{v} : {n}" for v, n in compte.items()) + ".",
        "",
        "Verdicts, en unités du dernier chiffre publié : « conforme » jusqu'à une demi-unité, « à l'arrondi près » "
        "jusqu'à 0,6, « écart d'une unité » jusqu'à 1, « non reproduit » au-delà.",
        "",
        "## Dépenses sociales en % du PIB citées dans le texte",
        "",
        "| Année | Texte de l'article | OCDE (SOCX), série du graphique 3 | Eurostat (COFOG santé + protection sociale) | Série qui correspond |",
        "|---|---|---|---|---|",
    ]
    for annee, publie, dec in TEXTE_SOCIAL:
        socx = d.socx.get(annee)
        cofog = social_cofog_pib(d, annee) if annee >= 1995 else None
        candidats = [(nom, v) for nom, v in (("OCDE", socx), ("Eurostat", cofog)) if v is not None]
        series = [nom if v_ == "conforme" else f"{nom} ({v_})"
                  for nom, v in candidats if (v_ := verdict(publie, v, dec)) != "non reproduit"]
        if not series:
            nom, v = min(candidats, key=lambda c: abs(c[1] - publie))
            series = [f"aucune ; la plus proche : {nom}, écart {fr(v - publie, 2, signe=True)}"]
        lignes.append(f"| {annee} | {fr(publie, dec)} | {fr(socx, 2) if socx is not None else 'n.d.'} | "
                      f"{fr(cofog, 2) if cofog is not None else 'n.d.'} | {' et '.join(series)} |")
    lignes += ["", "## Observations", ""]
    lignes += [f"- {o}" for o in observations(d, verdicts)]
    lignes += ["", "## Non vérifiable à ce jour", "",
               "Estimations 2026 de l'article. La ventilation par fonction de 2025 paraît en décembre 2026, "
               "les comptes de 2026 au printemps 2027.", ""]
    lignes += [f"- {e}" for e in ESTIMATIONS_2026]
    RESULTATS.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"écrit : {RESULTATS.name} ({', '.join(f'{n} {v}' for v, n in compte.items())})")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--telecharger", action="store_true", help="télécharger de nouveau les sources avant le calcul")
    args = parser.parse_args()
    if args.telecharger:
        telecharger()
    manifeste = lire_manifeste()
    ecrire_resultats(Donnees(), manifeste)


if __name__ == "__main__":
    main()
