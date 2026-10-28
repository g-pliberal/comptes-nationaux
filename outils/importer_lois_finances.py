#!/usr/bin/env python3
"""Enregistre dans la base les crédits qu'ouvre une loi de finances initiale, à partir de son texte définitif, tel que
le publie l'assemblée qui l'a adopté en dernier (page HTML archivée du Sénat ou de l'Assemblée nationale).

    python3 outils/importer_lois_finances.py <fichier_id>

Tableaux lus : les états qui répartissent par mission et par programme les autorisations d'engagement et les crédits
de paiement que la loi ouvre : l'état B pour le budget général, l'état C pour les budgets annexes, l'état D pour les
comptes d'affectation spéciale puis pour les comptes de concours financiers. Sous un programme, une ligne « dont
titre 2 » (« dont charges de personnel » pour un budget annexe, jusqu'aux lois pour 2022) donne la part de ses crédits
qui va aux dépenses de personnel. L'article d'équilibre, l'état A (les recettes) et l'état E (les autorisations de
découvert) ne sont pas lus.

Un état se reconnaît à son intitulé (« ÉTAT B (Article 167 de la loi) »), et les catégories de crédits qu'il répartit
à son titre (« … des crédits du budget général »). Ses tableaux sont ceux qui s'ouvrent entre son intitulé et celui de
l'état suivant, hors ceux qui portent l'intitulé d'un état ; un tableau que la page coupe en plusieurs continue jusqu'à
sa ligne de total, et chaque catégorie a le sien, dans l'ordre du titre.

Une mission égale la somme de ses programmes, en autorisations d'engagement comme en crédits de paiement. Quand un
tableau met des lignes en gras, ses missions sont ces lignes, ou, dans le texte pour 2009, celles qui ne le sont pas ;
certaines pages de l'Assemblée nationale ne marquant pas le gras, les missions se reconnaissent sinon à leurs montants :
une mission se ferme dès que ses programmes font son montant, et une ligne nulle qui la suit est un programme de plus,
sauf si c'est une mission que la base connaît déjà. Un tableau qui ne donne que des missions, comme celui du budget
général dans le texte de la commission mixte paritaire de 2006, se reconnaît à ce que ses lignes font ensemble son
total. Une ligne « (ligne supprimée) » n'est pas un programme. La somme des missions doit faire la ligne de total, et
celle-ci le montant que l'article de la loi ouvre pour la catégorie (« Il est ouvert aux ministres, pour 2024, au titre
du budget général, des autorisations d'engagement et des crédits de paiement s'élevant respectivement aux montants de
… € et de … € ») ; jusqu'aux lois pour 2019, un seul article ouvre ensemble les crédits des comptes d'affectation
spéciale et ceux des comptes de concours financiers. Une case « » » ne porte pas de chiffre : elle vaut zéro dans ces
sommes. Une colonne ou une ligne « dont » inconnue, ou une somme qui ne tombe pas juste, arrête l'import, sauf une
coquille de la page que ses propres sommes démontrent, déclarée dans COQUILLES.

Les missions, les budgets annexes, les comptes spéciaux et leurs programmes sont les fonctions de la norme LOLF, sous
l'identifiant que leur donne l'import des lois d'approbation des comptes (outils/importer_lois_resultats.py) : le
budget voté se compare ainsi, mission par mission, au budget exécuté. La version d'un chiffre est la date que le texte
porte ; les crédits ouverts sont des autorisations, sans statut de prévision ou d'exécution.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_page_html,
                    lire_texte_html, nombre_texte, table_des_chiffres, texte_html)
from importer_lois_resultats import code_lolf, colonnes, montants, propre, unite

# Catégories de crédits, telles que le titre d'un état et l'article de la loi les nomment.
CATEGORIES = {"BG": r"budget général", "BA": r"budgets annexes", "CAS": r"comptes d[’']affectation spéciale",
              "CCF": r"comptes de concours financiers"}
# Catégorie (ou catégories ouvertes ensemble par un même article) → montants de l'article de la loi.
ARTICLES = {("BG",): r"du budget général", ("BA",): r"des budgets annexes", ("CAS",): r"des comptes d[’']affectation spéciale",
            ("CCF",): r"des comptes de concours financiers",
            ("CAS", "CCF"): r"des comptes d[’']affectation spéciale et des comptes de concours financiers"}
COLONNES = {"Autorisations d’engagement": "AE", "Crédits de paiement": "CP"}
DONT = r"dont (?:titre 2|charges de personnel)"
# Coquilles d'une page, que ses propres sommes démontrent : (source, libellé de la ligne, colonne) → (montant de la
# page, montant juste). Le chiffre garde le montant de la page, avec une note ; les sommes de l'import prennent le
# montant juste.
COQUILLES = {
    ("an.ta13-0808", "Gestion du patrimoine immobilier de l’État", "CP"): (5130000000, 513000000),
}
NEANT = {"»", "-", "–", "—"}
ETAT = r"[ÉE][Tt][Aa][Tt]\s+([A-G])\s*\(\s*[Aa]rticles?\s+[0-9]"


def concept(categorie, colonne, dont):
    return f"LOLF.{categorie}_{colonne}_LFI" + ("_TITRE_2" if dont else "")


def nom(libelle):
    """Le nom d'une mission ou d'un programme, d'après son libellé : un trait d'union insécable est un trait d'union,
    et la mention « (intitulé modifié) », que porte un texte qui l'a changé, n'en fait pas partie."""
    return re.sub(r"\s*\(\s*intitulé modifié\s*\)", "", libelle.replace("\u2011", "-").replace("\u2010", "-"))


def cle_titre(texte):
    return re.sub(r"\s+", " ", texte.replace("'", "’")).lower()


def montant(texte):
    """Le nombre d'une case, 0 pour une case « néant », None pour une case vide."""
    if texte.strip() in NEANT:
        return 0
    n = nombre_texte(texte)
    return float(n[0]) if n else None


def entete(tableau):
    """Nombre de lignes d'en-tête d'un tableau de crédits : jusqu'à celle qui nomme les deux colonnes ; None si le
    tableau n'en a pas."""
    for r, ligne in enumerate(tableau[:4]):
        textes = {propre(x) for x in ligne}
        if any(t.startswith("Autorisations d") for t in textes) and "Crédits de paiement" in textes:
            return r + 1
    return None


def article(texte, annee, motif):
    """(autorisations d'engagement, crédits de paiement) que l'article de la loi ouvre pour une catégorie, ou None.
    Les apostrophes s'y lisent d'une seule façon, sans les blancs que certaines pages laissent autour d'elles ou
    devant une virgule."""
    texte = re.sub(r"\s+,", ",", re.sub(r"\s*’\s*", "’", texte.replace("'", "’")))
    trouve = re.findall(rf"Il est ouvert aux ministres, pour {annee},? au titre {motif}, des autorisations d’engagement "
                        rf"et des crédits de paiement s’élevant,? respectivement,? aux montants de ([0-9][0-9 ]*[0-9]) ?€? "
                        rf"et de ([0-9][0-9 ]*[0-9]) ?€?", texte)
    if len(trouve) > 1:
        sys.exit(f"{len(trouve)} articles ouvrent les crédits {motif}")
    return tuple(float(x.replace(" ", "")) for x in trouve[0]) if trouve else None


def blocs_des_etats(grilles, formes, flux, source_id):
    """[(catégorie, bloc)] : pour chaque catégorie de chaque état de crédits, ses lignes, tableau par tableau."""
    intitules = list(re.finditer(ETAT, flux))
    resultat = []
    for n, m in enumerate(intitules):
        fin = intitules[n + 1].start() if n + 1 < len(intitules) else len(flux)
        tableaux = [int(k) for k in re.findall(r"⟦([0-9]+)⟧", flux[m.start():fin])]
        tableaux = [k for k in tableaux if not re.search(ETAT, " ".join(x for l in grilles[k] for x in l))]
        premier = next((k for k in tableaux if entete(grilles[k])), None)
        if premier is None:
            continue  # état sans tableau de crédits (recettes, découverts, objectifs)
        titre = cle_titre(flux[m.start():flux.index(f"⟦{premier}⟧", m.start())])
        categories = sorted((c for c, motif in CATEGORIES.items() if re.search(motif, titre)),
                            key=lambda c: re.search(CATEGORIES[c], titre).start())
        blocs, ouvert = [], None
        for k in tableaux:
            t, forme = grilles[k], formes[k]
            e = entete(t)
            if e is None and ouvert is None:
                continue
            if e is not None:
                noms = colonnes(t, e, forme["largeurs"])
                if ouvert is None:
                    ouvert = {"lignes": [], "noms": noms, "unite": unite(t, e, noms, forme, source_id), "total": None,
                              "gras": set(), "avant": flux[(flux.index(f"⟦/{blocs[-1]['dernier']}⟧") if blocs
                                                            else m.start()):flux.index(f"⟦{k}⟧")]}
                elif set(noms.values()) != set(ouvert["noms"].values()):
                    sys.exit(f"tableau {k} : colonnes autres que celles du tableau qu'il continue")
            else:
                e, noms = 0, ouvert["noms"]
                if max(len(l) for l in t) != max(ouvert["noms"]) + 1:
                    sys.exit(f"tableau {k} : {max(len(l) for l in t)} colonnes, quand le tableau qu'il continue en a "
                             f"{max(ouvert['noms']) + 1}")
            textes_entete = {propre(x) for l in t[:e] for x in l if propre(x)} | set(ouvert["noms"].values())
            ouvert["gras"] |= {(k, r) for r, c in forme["gras"] if c == 0}
            ouvert["dernier"] = k
            par_ligne = {}
            for r, c, nombre in montants(t, e, noms, forme["largeurs"]):
                if noms[c] not in COLONNES:
                    sys.exit(f"tableau {k} : colonne « {noms[c]} » inconnue")
                par_ligne.setdefault(r, {})[COLONNES[noms[c]]] = (c, nombre)
            for r in range(e, len(t)):
                libelle = propre(t[r][0])
                # Une case fusionnée sur deux colonnes de même intitulé laisse vide la seconde.
                cases = {}
                for c, x in enumerate(t[r]):
                    if c in noms and noms[c] in COLONNES and not cases.get(COLONNES[noms[c]], "").strip():
                        cases[COLONNES[noms[c]]] = x
                valeurs = {col: montant(x) for col, x in cases.items()}
                notes = {}
                for col in valeurs:
                    publie, juste = COQUILLES.get((source_id, libelle, col), (None, None))
                    if publie is not None:
                        if valeurs[col] != publie:
                            sys.exit(f"tableau {k}, ligne {r} : coquille déclarée ({publie}) absente ({valeurs[col]})")
                        valeurs[col] = juste
                        lisible = lambda x: f"{x:,}".replace(",", "\u202f")
                        notes[col] = (f"Coquille de la page, qui imprime « {' '.join(cases[col].split())} » : le chiffre "
                                      f"en garde la lecture, {lisible(publie)} €, quand les programmes et le total de "
                                      f"l’état comptent {lisible(juste)} €.")
                if ouvert is None:
                    if libelle or any(v is not None for v in valeurs.values()):
                        sys.exit(f"tableau {k}, ligne {r} : ligne après le total (« {libelle} »)")
                    continue
                if not libelle and all(v is None for v in valeurs.values()):
                    continue
                if "(ligne supprimée)" in libelle:
                    if any(valeurs.values()):
                        sys.exit(f"tableau {k}, ligne {r} : ligne supprimée qui porte des crédits")
                    continue
                if not any(v is not None for v in valeurs.values()):
                    if {propre(x) for x in t[r] if propre(x)} <= textes_entete:
                        continue
                    sys.exit(f"tableau {k}, ligne {r} : ligne sans montant (« {libelle} »)")
                if not libelle or set(valeurs) != {"AE", "CP"} or None in valeurs.values():
                    sys.exit(f"tableau {k}, ligne {r} : ligne incomplète (« {libelle} », {valeurs})")
                genre = "total" if re.fullmatch(r"(?i)total|totaux", libelle) else \
                    "dont" if re.fullmatch(rf"(?i){DONT}", libelle) else None
                if genre is None and re.match(r"(?i)(dont|total)\b", libelle):
                    sys.exit(f"tableau {k}, ligne {r} : ligne « {libelle} » inconnue")
                ligne = {"tableau": k, "ligne": r, "libelle": libelle, "nom": nom(libelle), "valeurs": valeurs,
                         "genre": genre, "cases": par_ligne.get(r, {}), "noms": noms, "unite": ouvert["unite"],
                         "notes": notes}
                ouvert["lignes"].append(ligne)
                if genre == "total":
                    ouvert["total"] = ligne
                    blocs.append(ouvert)
                    ouvert = None
        if ouvert is not None:
            sys.exit(f"état {m.group(1)} : tableau sans ligne de total")
        if len(blocs) != len(categories):
            sys.exit(f"état {m.group(1)} : {len(blocs)} tableau(x) de crédits pour {len(categories)} catégorie(s) "
                     f"({', '.join(categories) or 'aucune'})")
        for categorie, bloc in zip(categories, blocs):
            nommees = {c for c, motif in CATEGORIES.items() if re.search(motif, cle_titre(bloc["avant"]))}
            if len(blocs) > 1 and len(nommees) == 1 and nommees != {categorie}:
                sys.exit(f"état {m.group(1)} : le tableau des crédits {categorie} est précédé du titre {nommees.pop()}")
            resultat.append((categorie, bloc))
    return resultat


def egal(a, b):
    return all(abs(a[c] - b[c]) < 0.5 for c in ("AE", "CP"))


def somme(lignes):
    return {c: sum(l["valeurs"][c] for l in lignes) for c in ("AE", "CP")}


def par_marque(ordinaires, marquees):
    """[(mission, programmes)] si les lignes marquées (en gras, ou au contraire non en gras) sont les missions :
    la première ligne en est une, et chacune égale la somme des lignes qui la suivent jusqu'à la suivante ; None
    sinon."""
    if not ordinaires or (ordinaires[0]["tableau"], ordinaires[0]["ligne"]) not in marquees:
        return None
    missions = []
    for l in ordinaires:
        if (l["tableau"], l["ligne"]) in marquees:
            missions.append((l, []))
        else:
            missions[-1][1].append(l)
    return missions if all(programmes and egal(somme(programmes), m["valeurs"]) for m, programmes in missions) else None


def par_sommes(categorie, ordinaires, missions_connues):
    """[(mission, programmes)] d'après les seuls montants : une mission se ferme dès que ses programmes font son
    montant ; une ligne nulle qui suit est un programme de plus, sauf si c'est une mission connue de la base."""
    nulle = lambda l: l["valeurs"]["AE"] == 0 and l["valeurs"]["CP"] == 0
    missions, i = [], 0
    while i < len(ordinaires):
        mission, programmes = ordinaires[i], []
        i += 1
        while not (programmes and egal(somme(programmes), mission["valeurs"])):
            if i == len(ordinaires):
                sys.exit(f"{categorie} : les programmes de la mission « {mission['libelle']} » ne font pas son montant")
            programmes.append(ordinaires[i])
            i += 1
        while i < len(ordinaires) and nulle(ordinaires[i]) and \
                f"LOLF.{code_lolf(ordinaires[i]['nom'])}" not in missions_connues:
            programmes.append(ordinaires[i])
            i += 1
        missions.append((mission, programmes))
    return missions


def structure(categorie, bloc, missions_connues):
    """Rattache chaque ligne à sa mission : {(tableau, ligne) : (libellé, mission ou "")} ; vérifie les sommes. Quand
    le tableau met des lignes en gras, les missions sont ses lignes en gras, ou bien, dans le texte pour 2009, ses
    lignes qui ne le sont pas ; sinon, elles se déduisent des montants (par_sommes)."""
    ordinaires = [l for l in bloc["lignes"] if l["genre"] is None]
    total = bloc["total"]["valeurs"]
    cles = {(l["tableau"], l["ligne"]) for l in ordinaires}
    gras = cles & bloc["gras"]
    if egal(somme(ordinaires), total):  # des missions seules
        if gras and gras != cles:
            sys.exit(f"{categorie} : des missions seules, dont certaines seulement en gras")
        missions = [(l, []) for l in ordinaires]
    elif egal({c: v / 2 for c, v in somme(ordinaires).items()}, total):
        missions = (par_marque(ordinaires, gras) or par_marque(ordinaires, cles - gras)) if gras else \
            par_sommes(categorie, ordinaires, missions_connues)
        if missions is None:
            sys.exit(f"{categorie} : ni ses lignes en gras ni les autres ne sont des missions égales à leurs programmes")
    else:
        sys.exit(f"{categorie} : ses lignes ne font ni son total ni deux fois son total")
    if not egal(somme([m for m, _ in missions]), total):
        sys.exit(f"{categorie} : la somme des missions ne fait pas le total")
    # Une mission sans aucun crédit ne se distingue d'un programme nul que par sa mise en forme : une ligne nulle qui
    # porte le nom d'une mission que la base connaît ne peut pas être un programme d'une autre.
    for mission, programmes in missions:
        for p in programmes:
            if p["valeurs"]["AE"] == 0 and p["valeurs"]["CP"] == 0 and \
                    f"LOLF.{code_lolf(p['nom'])}" in missions_connues and code_lolf(p["nom"]) != code_lolf(mission["nom"]):
                sys.exit(f"{categorie} : la ligne nulle « {p['libelle']} », une mission connue, se range parmi les "
                         f"programmes de la mission « {mission['libelle']} »")
    rattache = {}
    for mission, programmes in missions:
        rattache[(mission["tableau"], mission["ligne"])] = (mission["nom"], "")
        for p in programmes:
            rattache[(p["tableau"], p["ligne"])] = (p["nom"], mission["nom"])
    # Une ligne « dont » appartient au programme qui la précède.
    precedent = None
    for l in bloc["lignes"]:
        if l["genre"] == "dont":
            if precedent is None or not rattache[precedent][1]:
                sys.exit(f"{categorie} : ligne « {l['libelle']} » hors programme (tableau {l['tableau']}, "
                         f"ligne {l['ligne']})")
            rattache[(l["tableau"], l["ligne"])] = rattache[precedent]
        elif l["genre"] is None:
            precedent = (l["tableau"], l["ligne"])
    return rattache


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions et programmes."""
    chemin = BASE / fichier["chemin"]
    texte = texte_html(lire_texte_html(chemin))
    annees = set(re.findall(r"Il est ouvert aux ministres, pour ([0-9]{4}),? au titre du budget général", texte))
    if len(annees) != 1 or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année de la loi ({', '.join(sorted(annees)) or 'aucune'}) ou date du texte "
                 f"introuvable")
    annee = annees.pop()
    if not int(annee) - 1 <= int(fichier["mis_a_jour_source"][:4]) <= int(annee):
        sys.exit(f"{fichier['id']} : loi de finances pour {annee} dans un texte daté {fichier['mis_a_jour_source']}")
    # Une coupure de mot de fin de ligne du texte imprimé, restée dans la page (« dévelop-pement »), se recolle quand
    # le mot entier figure ailleurs dans le texte.
    mots = set(re.findall(r"\w+", texte.lower()))
    recolle = lambda libelle: re.sub(r"(\w+)-(\w+)", lambda m: m.group(1) + m.group(2) if m.group(1)[-1].islower() and
                                     m.group(2)[0].islower() and (m.group(1) + m.group(2)).lower() in mots
                                     else m.group(0), libelle)
    grilles, formes, flux = lire_page_html(chemin)
    blocs = blocs_des_etats(grilles, formes, flux, fichier["source_id"])
    totaux = {c: b["total"]["valeurs"] for c, b in blocs}
    # Chaque article qui ouvre des crédits doit avoir son état ; un texte de commission mixte paritaire, qui ne reproduit
    # que ce qui restait en discussion, n'a l'article que s'il a l'état.
    for categories, motif in ARTICLES.items():
        ouverts = article(texte, annee, motif)
        if ouverts is None:
            continue
        if not all(c in totaux for c in categories):
            sys.exit(f"{fichier['id']} : l'article ouvre des crédits {motif}, dont l'état n'est pas lu")
        for i, colonne in enumerate(("AE", "CP")):
            if abs(sum(totaux[c][colonne] for c in categories) - ouverts[i]) >= 0.5:
                sys.exit(f"{'+'.join(categories)} : l'article ouvre {ouverts[i]:,.0f} € en {colonne}, l'état en "
                         f"totalise {sum(totaux[c][colonne] for c in categories):,.0f}")
    lus = set(totaux)
    if not all(article(texte, annee, ARTICLES[(c,)]) or ("CAS" in lus and "CCF" in lus and
                                                          article(texte, annee, ARTICLES[("CAS", "CCF")]))
               for c in lus):
        sys.exit(f"{fichier['id']} : un état sans l'article qui en ouvre les crédits")
    missions_connues = {f for f, l in fonctions.items() if f.startswith("LOLF.") and not l["parent_id"]}
    for categorie, bloc in blocs:
        rattache = structure(categorie, bloc, missions_connues)
        for l in bloc["lignes"]:
            fonction = ""
            if l["genre"] != "total":
                libelle, mission = (recolle(x) for x in rattache[(l["tableau"], l["ligne"])])
                parent = f"LOLF.{code_lolf(mission)}" if mission else ""
                fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
                if parent:
                    fonctions.setdefault(parent, {"id": parent, "libelle": mission, "norme_id": "LOLF", "parent_id": ""})
                fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF",
                                                "parent_id": parent})
            unite_, note = l["unite"]
            for colonne, (c, nombre) in sorted(l["cases"].items()):
                ligne = {
                    "source_id": fichier["source_id"], "fichier_id": fichier["id"],
                    "emplacement": f"tableau={l['tableau']};ligne={l['ligne']};colonne={c};libelle={l['libelle']};"
                                   f"colonne_libelle={l['noms'][c]}",
                    "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept(categorie, colonne, l["genre"] == "dont"),
                    "fonction_id": fonction, "traitements": "", "unite_id": unite_, "periode": annee,
                    "valeur": nombre[0], "decimales": nombre[1], "statut": "non_precise", "drapeau_source": "",
                    "version": fichier["mis_a_jour_source"][:10], "consolidation": "non_consolide", "denominateur_id": "",
                    "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(),
                    "notes": " ".join(n for n in (note, l["notes"].get(colonne, "")) if n),
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
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    ajoutes, inchanges = fusionner(existants, list(lignes_du_fichier(fichier, fonctions)), fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte {len(existants)}")


if __name__ == "__main__":
    main()
