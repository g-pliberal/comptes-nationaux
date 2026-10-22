#!/usr/bin/env python3
"""Contrôle la cohérence des chiffres enregistrés et écrit controles/coherence.md.

    python3 outils/controler_coherence.py

Le contrôle de la base (valider.py) garantit que chaque chiffre est celui de sa source. Celui-ci
vérifie ce que disent les sources elles-mêmes :
1. les sommes comptables des tableaux de l'Insee (un total égale la somme de ses composantes) ;
2. les soldes des sous-secteurs, qui s'additionnent ;
3. les ratios, qu'on doit retrouver à partir de leur dénominateur ;
4. les écarts entre sources pour une même grandeur.

Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la
demi-unité de la dernière décimale de chaque valeur en jeu. Une incohérence trouvée ici n'est pas une
erreur de la base : c'est un constat sur la source, publié tel quel. Le rapport ne contient aucune date
d'exécution, pour qu'un rapport à jour ne change pas.
"""

import collections
import math

from commun import RACINE, lire, ressources_chiffres

RAPPORT = RACINE / "controles" / "coherence.md"

# Identités des tableaux 3.201 à 3.214 de l'Insee : total = somme signée des composantes.
IDENTITES = [
    ("INSEE_APU.DEP_FONCTIONNEMENT", ["SEC2010.P2", "SEC2010.D1PAY", "SEC2010.D29PAY", "SEC2010.D4_HORS_D41PAY", "SEC2010.D5PAY"]),
    ("INSEE_APU.DEP_PRESTATIONS_TRANSFERTS", ["SEC2010.D62PAY", "SEC2010.D632PAY", "SEC2010.D3PAY", "SEC2010.D73PAY",
                                              "SEC2010.D7_HORS_D73PAY", "SEC2010.D9_HORS_D995PAY"]),
    ("INSEE_APU.DEP_ACTIFS_NON_FINANCIERS", ["SEC2010.P51G", "SEC2010.P52_P53_NP"]),
    ("SEC2010.TE", ["INSEE_APU.DEP_FONCTIONNEMENT", "SEC2010.D41PAY", "INSEE_APU.DEP_PRESTATIONS_TRANSFERTS",
                    "INSEE_APU.DEP_ACTIFS_NON_FINANCIERS"]),
    ("INSEE_APU.DEP_HORS_ELEMENTS_IMPUTES", ["SEC2010.TE", "-SEC2010.D122PAY", "-INSEE_APU.DEP_PRODUCTION_COMPTE_PROPRE",
                                             "-INSEE_APU.DEP_CREDITS_IMPOT"]),
    ("INSEE_APU.REC_PRODUCTION", ["SEC2010.P11", "SEC2010.P12", "INSEE_APU.REC_PAIEMENTS_PARTIELS", "SEC2010.D39REC"]),
    ("INSEE_APU.REC_REVENUS_PROPRIETE", ["SEC2010.D41REC", "SEC2010.D4_HORS_D41REC"]),
    ("INSEE_APU.REC_IMPOTS_COTISATIONS", ["SEC2010.D2REC", "SEC2010.D5REC", "SEC2010.D91REC", "SEC2010.D733REC",
                                          "SEC2010.D61REC", "SEC2010.D995REC"]),
    ("INSEE_APU.REC_AUTRES_TRANSFERTS", ["SEC2010.D73_HORS_D733REC", "SEC2010.D7_HORS_D73REC", "SEC2010.D9_HORS_D91_D995REC"]),
    ("SEC2010.TR", ["INSEE_APU.REC_PRODUCTION", "INSEE_APU.REC_REVENUS_PROPRIETE", "INSEE_APU.REC_IMPOTS_COTISATIONS",
                    "INSEE_APU.REC_AUTRES_TRANSFERTS"]),
    ("INSEE_APU.REC_HORS_ELEMENTS_IMPUTES", ["SEC2010.TR", "-SEC2010.D612REC", "-SEC2010.P12", "-INSEE_APU.REC_CREDITS_IMPOT"]),
    ("SEC2010.B9", ["SEC2010.TR", "-SEC2010.TE"]),
]

# Soldes : celui d'un ensemble égale la somme de ceux de ses parties.
DECOMPOSITIONS = [("S13", ["S1311", "S1313", "S1314"]), ("S1311", ["S13111", "S13112"]), ("S1313", ["S13131", "S13132"]),
                  ("S1314", ["S13141", "S13142"]), ("S13131", ["S131311", "S131312", "S131313", "S131314"])]

# Unités comparables entre elles une fois converties ; les autres ne se comparent qu'à elles-mêmes.
FAMILLES = {"EUR": ("euros", 1), "MIO_EUR": ("euros", 1e6), "MD_EUR": ("euros", 1e9),
            "MIO_ECU_EUR": ("écus puis euros", 1e6)}
NOMS_RATIOS = {"PC_PIB": "% du PIB", "PC_DEPENSE": "% de la dépense totale"}
REGLES = {"indique": "le PIB indiqué par la source, dans le même tableau",
          "depense": "la dépense totale du même périmètre, chez la même source",
          "libre": "non indiqué par la source : chaque série de PIB enregistrée pour l'année est essayée"}


def charger():
    """Pour chaque chiffre, sa version la plus récente chez sa source."""
    derniers = {}
    for r in ressources_chiffres():
        for l in lire(r["path"]):
            cle = (l["source_id"], l["zone"], l["perimetre_id"], l["concept_id"], l["fonction_id"], l["traitements"],
                   l["unite_id"], l["periode"])
            if cle not in derniers or l["version"] > derniers[cle]["version"]:
                derniers[cle] = l
    return derniers


def valeur(ligne):
    """(valeur dans l'unité de base de sa famille, demi-unité de sa dernière décimale, famille d'unités)."""
    nom, echelle = FAMILLES.get(ligne["unite_id"], (ligne["unite_id"], 1))
    return float(ligne["valeur"]) * echelle, 0.5 * 10 ** -int(ligne["decimales"]) * echelle, nom


def depasse(ecart, marge):
    """Vrai si l'écart dépasse la marge des arrondis, au-delà des imprécisions du calcul en virgule flottante."""
    return abs(ecart) > marge * (1 + 1e-9) + 1e-9


def montant(derniers, cle):
    """Le chiffre de même fiche que `cle`, exprimé en euros : le numérateur d'un ratio."""
    for unite in ("MD_EUR", "MIO_EUR", "EUR"):
        ligne = derniers.get(cle[:6] + (unite, cle[7]))
        if ligne:
            return valeur(ligne)
    return None


# --- Les contrôles -------------------------------------------------------------------------------------

def sommes(derniers):
    controles, ecarts = 0, []
    groupes = sorted({(k[0], k[1], k[2], k[7]) for k in derniers if k[0].startswith("insee.t32") and k[6] == "MD_EUR"})
    for source, zone, perimetre, periode in groupes:
        cherche = lambda concept: derniers.get((source, zone, perimetre, concept, "", "", "MD_EUR", periode))
        for total, composantes in IDENTITES:
            parties = [(-1 if c.startswith("-") else 1, cherche(c.lstrip("-"))) for c in composantes]
            if cherche(total) is None or any(l is None for _, l in parties):
                continue
            controles += 1
            t, pt, _ = valeur(cherche(total))
            somme = sum(s * valeur(l)[0] for s, l in parties)
            if depasse(t - somme, pt + sum(valeur(l)[1] for _, l in parties)):
                ecarts.append((source, perimetre, periode, total, t, somme))
    return controles, ecarts


def soldes(derniers):
    # Les tableaux 3.201 à 3.214 publient un sous-secteur chacun : on les réunit par année.
    par_annee = collections.defaultdict(dict)
    for k, l in derniers.items():
        if k[3] == "SEC2010.B9" and k[6] == "MD_EUR" and k[0].startswith("insee."):
            famille = "insee.t3201 à t3214" if k[0].startswith("insee.t32") else k[0]
            par_annee[(famille, k[7])][k[2]] = valeur(l)[:2] + (k[0],)
    controles, ecarts = 0, []
    for (famille, periode), valeurs in sorted(par_annee.items()):
        for ensemble, parties in DECOMPOSITIONS:
            if ensemble in valeurs and all(p in valeurs for p in parties):
                controles += 1
                ecart = valeurs[ensemble][0] - sum(valeurs[p][0] for p in parties)
                if depasse(ecart, valeurs[ensemble][1] + sum(valeurs[p][1] for p in parties)):
                    tableaux = sorted({valeurs[p][2] for p in [ensemble] + parties})
                    ecarts.append((famille, periode, ensemble, parties, tableaux, ecart))
    return controles, ecarts


def ratios(derniers):
    """Recalcule chaque ratio : le même chiffre en montant, divisé par chacun de ses dénominateurs possibles."""
    par_id = {l["id"]: l for l in derniers.values()}
    pib = collections.defaultdict(dict)  # (zone, année) → {source: (valeur, précision)}
    for k, l in derniers.items():
        if k[3] == "SEC2010.B1GQ" and valeur(l)[2] == "euros":
            pib[(k[1], k[7])][k[0]] = valeur(l)[:2]
    resultats = []
    for k, l in sorted(derniers.items()):
        numerateur = montant(derniers, k) if k[6] in NOMS_RATIOS else None
        if numerateur is None:
            continue
        indique = par_id.get(l["denominateur_id"])
        if indique:
            regle, attendu, candidats = "indique", indique["source_id"], dict(pib[(k[1], k[7])])
            candidats[attendu] = valeur(indique)[:2]
        elif k[6] == "PC_DEPENSE":
            total = montant(derniers, k[:4] + ("",) + k[5:])
            regle, attendu, candidats = "depense", k[0], {k[0]: total[:2]} if total else {}
        else:
            regle, attendu, candidats = "libre", None, dict(pib[(k[1], k[7])])
        (n, pn), r, pr = numerateur[:2], float(l["valeur"]), 0.5 * 10 ** -int(l["decimales"])
        par = sorted(s for s, (d, pd) in candidats.items()
                     if d and not depasse(100 * n / d - r, pr + 100 * (pn / d + abs(n) * pd / d ** 2)))
        # Les dénominateurs qui donneraient le ratio publié, arrondis compris.
        implicite = (100 * max(abs(n) - pn, 0) / (abs(r) + pr), 100 * (abs(n) + pn) / (abs(r) - pr)) if abs(r) > pr else None
        resultats.append({"cle": k, "regle": regle, "attendu": attendu, "par": par,
                          "retrouve": attendu in par if attendu else bool(par), "implicite": implicite,
                          "pib": pib[(k[1], k[7])] if k[6] == "PC_PIB" else {}})
    return resultats


def concordances(derniers):
    """Compare, pour une même grandeur dans la même famille d'unités, les valeurs de sources différentes."""
    groupes = collections.defaultdict(lambda: collections.defaultdict(dict))
    for k, l in derniers.items():
        v, precision, unite = valeur(l)
        if unite != "écus puis euros":
            groupes[k[1:6] + (unite,)][k[7]][k[0]] = (v, precision, l["consolidation"])
    paires = collections.defaultdict(lambda: {"comparaisons": 0, "ecarts": []})
    for grandeur, annees in groupes.items():
        for annee, sources in annees.items():
            noms = sorted(sources)
            for i, a in enumerate(noms):
                for b in noms[i + 1:]:
                    (va, pa, ca), (vb, pb, cb) = sources[a], sources[b]
                    if {ca, cb} == {"consolide", "non_consolide"}:
                        continue  # pas la même grandeur
                    p = paires[(a, b, grandeur)]
                    p["comparaisons"] += 1
                    if depasse(va - vb, pa + pb):
                        p["ecarts"].append((annee, va - vb))
    return paires


# --- Le rapport ----------------------------------------------------------------------------------------

def fr(x, decimales, signe=False):
    texte = format(x, f"{'+' if signe else ''},.{decimales}f")
    return texte.replace(",", " ").replace(".", ",").replace("-", "−")


def ecart_lisible(ecart, unite):
    if unite == "euros":
        return f"{fr(ecart / 1e6, 1, True)} M€"
    nom = {"PC_PIB": "de PIB", "PC_DEPENSE": "de dépense"}.get(unite, unite)
    return f"{fr(ecart, 1, True)} point{'s' if abs(ecart) >= 2 else ''} {nom}"


def plage(annees):
    annees = sorted(set(annees))
    if len(annees) <= 4:
        return annees[0] if len(annees) == 1 else ", ".join(annees[:-1]) + " et " + annees[-1]
    return f"{len(annees)} années entre {annees[0]} et {annees[-1]}"


def partie_sources(derniers):
    titres = {s["id"]: s["titre"] for s in lire("tables/sources.csv")}
    versions = collections.defaultdict(str)
    for l in derniers.values():
        versions[l["source_id"]] = max(versions[l["source_id"]], l["version"])
    nombre = collections.Counter(k[0] for k in derniers)
    lignes = ["## Les sources contrôlées", "",
              "Pour chaque chiffre, la version la plus récente enregistrée chez sa source.", "",
              "| Source | Titre | Version la plus récente | Chiffres |", "|---|---|---|---|"]
    lignes += [f"| {s} | {titres.get(s, '')} | {versions[s]} | {nombre[s]} |" for s in sorted(nombre)]
    return lignes + [""]


def partie_sommes(derniers):
    n, ecarts = sommes(derniers)
    lignes = ["## 1. Sommes comptables des tableaux de l'Insee", "",
              f"{n} sommes vérifiées (un total contre la somme de ses composantes) : {n - len(ecarts)} justes, "
              f"{len(ecarts)} en écart.", ""]
    if ecarts:
        lignes += ["| Source | Périmètre | Année | Total | Total publié (Md€) | Somme des composantes (Md€) | Écart |",
                   "|---|---|---|---|---|---|---|"]
        lignes += [f"| {s} | {p} | {a} | {t} | {fr(v / 1e9, 4)} | {fr(somme / 1e9, 4)} | {ecart_lisible(v - somme, 'euros')} |"
                   for s, p, a, t, v, somme in ecarts]
        lignes.append("")
    return lignes


def partie_soldes(derniers):
    n, ecarts = soldes(derniers)
    lignes = ["## 2. Soldes des sous-secteurs", "",
              f"{n} additions vérifiées (le solde d'un ensemble contre la somme des soldes de ses parties) : "
              f"{n - len(ecarts)} justes, {len(ecarts)} en écart.", ""]
    regroupes = collections.defaultdict(list)
    for famille, annee, ensemble, parties, tableaux, ecart in ecarts:
        regroupes[(famille, ensemble, tuple(parties))].append((annee, ecart, tableaux))
    if regroupes:
        lignes += ["| Tableaux | Ensemble | Parties | Années en écart | Plus grand écart |", "|---|---|---|---|---|"]
        for (famille, ensemble, parties), liste in sorted(regroupes.items()):
            annee, ecart, _ = max(liste, key=lambda e: abs(e[1]))
            tableaux = ", ".join(sorted({t for _, _, ts in liste for t in ts}))
            lignes.append(f"| {tableaux} | {ensemble} | {' + '.join(parties)} | {plage([a for a, _, _ in liste])} | "
                          f"{ecart_lisible(ecart, 'euros')} en {annee} |")
        lignes.append("")
    return lignes


def partie_ratios(derniers):
    resultats = ratios(derniers)
    lignes = ["## 3. Ratios", "",
              "Chaque ratio est recalculé : le même chiffre en montant, divisé par son dénominateur. Il est retrouvé "
              "si l'écart ne dépasse pas ce que permettent les arrondis du ratio, du montant et du dénominateur.", "",
              "| Dénominateur | Ratios | Retrouvés | Non retrouvés |", "|---|---|---|---|"]
    for regle, texte in REGLES.items():
        liste = [x for x in resultats if x["regle"] == regle]
        if liste:
            ok = sum(x["retrouve"] for x in liste)
            lignes.append(f"| {texte} | {len(liste)} | {ok} | {len(liste) - ok} |")
    lignes.append("")
    groupes = collections.defaultdict(list)
    for x in resultats:
        if not x["retrouve"]:
            k = x["cle"]
            groupes[(k[0], k[3], k[2], k[6], x["regle"], x["attendu"])].append(x)
    if groupes:
        lignes += ["Ratios non retrouvés :", ""]
    for (source, concept, perimetre, unite, regle, attendu), liste in sorted(groupes.items()):
        fonctions = {x["cle"][4] for x in liste}
        detail = ""
        if fonctions - {""}:
            detail = f" ({'ensemble des fonctions et ' if '' in fonctions else ''}{len(fonctions - {''})} fonctions COFOG)"
        un = len(liste) == 1
        ratio = f"{len(liste)} ratio{'' if un else 's'}{detail}"
        constat = {"indique": f"{'n’est' if un else 'ne sont'} pas retrouvé{'' if un else 's'} avec le PIB indiqué, celui de {attendu}",
                   "depense": f"{'n’est' if un else 'ne sont'} pas retrouvé{'' if un else 's'} avec la dépense totale de la même source",
                   "libre": f"{'n’est' if un else 'ne sont'} retrouvé{'' if un else 's'} avec aucune des séries de PIB enregistrées"}[regle]
        lignes.append(f"- **{source}, {concept}, {perimetre}, en {NOMS_RATIOS[unite]}** : {ratio} {constat}, "
                      f"pour {plage([x['cle'][7] for x in liste])}.")
        for s, compte in collections.Counter(s for x in liste for s in x["par"]).most_common():
            lignes.append(f"  Avec le PIB de {s}, {compte} {'est retrouvé' if compte == 1 else 'sont retrouvés'}.")
        aucun = collections.defaultdict(list)
        for x in liste:
            if not x["par"] and x["implicite"]:
                aucun[x["cle"][7]].append(x)
        for annee, xs in sorted(aucun.items()):
            bas, haut = max(x["implicite"][0] for x in xs), min(x["implicite"][1] for x in xs)
            pronom = "le" if len(xs) == 1 else "les"
            if bas > haut:
                texte = f"aucun dénominateur unique ne {pronom} reproduit"
            else:
                denominateur = "un PIB" if unite == "PC_PIB" else "une dépense totale"
                # Bornes arrondies vers l'extérieur, au million d'euros : l'intervalle affiché contient le vrai.
                texte = (f"il faudrait {denominateur} compris entre {fr(math.floor(bas / 1e6) / 1e3, 3)} et "
                         f"{fr(math.ceil(haut / 1e6) / 1e3, 3)} Md€")
            enregistres = " ; ".join(f"{s} {fr(v / 1e9, 3)} Md€" for s, (v, _) in sorted(xs[0]["pib"].items()))
            lignes.append(f"  En {annee}, aucune série enregistrée ne {pronom} retrouve ; {texte}"
                          + (f" (PIB enregistrés : {enregistres})." if enregistres else "."))
    return lignes + [""]


def partie_concordances(derniers):
    paires = concordances(derniers)
    lignes = ["## 4. Écarts entre sources pour une même grandeur", "",
              "Même concept, même périmètre, même fonction, même année, montants convertis dans la même unité. "
              "Les montants d'Eurostat convertis en écus avant 1999 ne sont pas comparés : ce sont les mêmes données "
              "que ses montants en euros, converties autrement.", "",
              "| Source A | Source B | Comparaisons | Écarts | Plus grand écart (A − B) |", "|---|---|---|---|---|"]
    resume = collections.defaultdict(lambda: {"comparaisons": 0, "ecarts": collections.defaultdict(list)})
    for (a, b, grandeur), p in paires.items():
        resume[(a, b)]["comparaisons"] += p["comparaisons"]
        resume[(a, b)]["ecarts"][grandeur[5]] += p["ecarts"]
    for (a, b), r in sorted(resume.items()):
        n = sum(len(liste) for liste in r["ecarts"].values())
        textes = []
        for unite, liste in sorted(r["ecarts"].items()):
            if liste:
                annee, ecart = max(liste, key=lambda e: abs(e[1]))
                textes.append(f"{ecart_lisible(ecart, unite)} en {annee}")
        lignes.append(f"| {a} | {b} | {r['comparaisons']} | {n} | {' ; '.join(textes) or 'aucun'} |")
    lignes += ["", "Détail des grandeurs en écart :", "",
               "| Source A | Source B | Grandeur | Années en écart | Plus grand écart (A − B) |", "|---|---|---|---|---|"]
    for (a, b, grandeur), p in sorted(paires.items()):
        if p["ecarts"]:
            zone, perimetre, concept, fonction, traitements, unite = grandeur
            annee, ecart = max(p["ecarts"], key=lambda e: abs(e[1]))
            libelle = " ".join(x for x in (zone, perimetre, concept, fonction, traitements) if x)
            libelle += f", en {NOMS_RATIOS[unite]}" if unite in NOMS_RATIOS else ""
            lignes.append(f"| {a} | {b} | {libelle} | {plage([e[0] for e in p['ecarts']])} | "
                          f"{ecart_lisible(ecart, unite)} en {annee} |")
    return lignes + [""]


def ecrire_rapport(derniers):
    lignes = ["# Cohérence des chiffres enregistrés", "",
              "Fichier généré par `outils/controler_coherence.py` à partir de la base : ne pas le modifier à la main.", "",
              "Un écart n'est signalé que s'il dépasse ce que peuvent expliquer les arrondis de publication : la "
              "demi-unité de la dernière décimale de chaque valeur en jeu. Une incohérence signalée ici est un constat "
              "sur la source, pas une erreur d'enregistrement : chaque chiffre a été relu dans sa copie archivée.", ""]
    lignes += partie_sources(derniers) + partie_sommes(derniers) + partie_soldes(derniers)
    lignes += partie_ratios(derniers) + partie_concordances(derniers)
    RAPPORT.parent.mkdir(exist_ok=True)
    RAPPORT.write_text("\n".join(lignes).rstrip("\n") + "\n", encoding="utf-8")
    print(f"écrit : {RAPPORT.relative_to(RACINE)}")


if __name__ == "__main__":
    ecrire_rapport(charger())
