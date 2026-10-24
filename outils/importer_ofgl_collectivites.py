#!/usr/bin/env python3
"""Inscrit dans la base les comptes de chaque collectivité que publie data.ofgl.fr, le portail de l'Observatoire des
finances et de la gestion publique locales (OFGL), à partir des copies archivées de ses exports.

    python3 outils/importer_ofgl_collectivites.py --requetes <source_id> <exercice>   # les requêtes à archiver
    python3 outils/importer_ofgl_collectivites.py <fichier_id>

Les jeux de données des comptes consolidés de l'OFGL donnent, pour chaque collectivité, chaque exercice et chaque agrégat
financier, le montant de son budget principal, celui de ses budgets annexes, les flux croisés entre eux et le montant
consolidé (budget principal plus budgets annexes moins flux croisés), en euros, calculés d'après les balances comptables
de la DGFiP. Trois exports d'un jeu sont archivés, compressés, et s'importent dans cet ordre :
- l'inventaire : le nombre de lignes de chaque exercice du jeu ;
- pour chaque exercice, les montants : une ligne par collectivité et par agrégat ;
- pour chaque exercice, les collectivités : nom, catégorie, territoire et population.
Les comptes des services départementaux d'incendie et de secours et ceux des centres d'action sociale ne sont publiés
que budget par budget, sans consolidation : chaque ligne des montants donne, pour un budget, désigné par son numéro
SIRET, et un agrégat, le montant de ce budget, et la liste est celle des budgets, avec leur collectivité.
Le portail publie aussi, d'après les fichiers de répartition de la DGCL, les dotations que l'État notifie à chaque
commune, à chaque groupement à fiscalité propre et à chaque département : une ligne par collectivité et par variable. On
en lit le montant notifié de la dotation globale de fonctionnement et celui de chacune de ses parts ; la collectivité y
est désignée par son code Insee, son numéro Siren ou son code de département.
Ces copies sont les chiffres eux-mêmes : la base ne les recopie pas, elle les lit. L'import vérifie chaque ligne
(agrégat connu de tables/agregats_ofgl.csv, ou variable attendue, montants numériques, une seule ligne par collectivité,
ou par budget, et par agrégat ou variable), que les montants ont le nombre de lignes de l'inventaire et que la liste des
collectivités, ou des budgets, est celle des montants, puis inscrit la copie dans tables/fichiers_collectivites.csv. La
version d'une copie est la date de
modification du jeu de données qu'annonce le portail ; la copie qui en contrôle une autre est la plus récente de même
source dont la version ne la dépasse pas. Le dernier exercice de l'inventaire est provisoire, les autres définitifs.
"""

import collections
import math
import re
import sys
import urllib.parse

from commun import BASE, champs, ecrire, lire, lire_export_ofgl

PORTAIL = "https://data.ofgl.fr/api/explore/v2.1/catalog/datasets/"
# Jeux de données lus : source → (jeu de données du portail, champs de la liste des collectivités).
JEUX = {
    "ofgl.base-gfp-consolidee": ("ofgl-base-gfp-consolidee", ["siren", "lbudg", "categ", "nat_juridique",
                                                              "mode_financement", "dep_code", "reg_code", "ptot"]),
    "ofgl.base-communes-consolidee": ("ofgl-base-communes-consolidee", ["siren", "insee", "com_code", "lbudg", "categ",
                                                                        "dep_code", "reg_code", "epci_code", "ptot"]),
    "ofgl.base-departements-consolidee": ("ofgl-base-departements-consolidee", ["siren", "lbudg", "categ", "dep_code",
                                                                                "reg_code", "ptot"]),
    "ofgl.base-regions-consolidee": ("ofgl-base-regions-consolidee", ["siren", "lbudg", "categ", "reg_code", "ptot"]),
    "ofgl.base-syndicats-consolidee": ("ofgl-base-syndicats-consolidee", ["siren", "lbudg", "categ", "categorie_synd",
                                                                          "dep_current_code", "reg_code"]),
    "ofgl.base-epl-consolidee": ("ofgl-base-epl-consolidee", ["siren", "nom_epl", "lbudg", "categ", "categorie_epl_abr",
                                                              "libelle_cacti_simplifie", "dep_code", "reg_code"]),
    "ofgl.base-sdis": ("ofgl-base-sdis", ["siren", "ident", "lbudg", "cbudg", "nomen", "categorie_sdis", "code_dep",
                                          "code_region", "population_totale"]),
    "ofgl.base-ccas-cias": ("ofgl-base-ccas-cias", ["siren", "ident", "lbudg", "nom_ccas", "type", "type_de_budget",
                                                    "nomen", "ctype", "code_dep", "code_reg"]),
    "ofgl.dotations-communes": ("dotations-communes", ["exercice", "code_insee", "commune", "code_departement",
                                                       "siren_epci"]),
    "ofgl.dotations-gfp": ("dotations-gfp", ["exercice", "siren", "nom_epci", "nature_juridique", "code_departement"]),
    "ofgl.dotations-departements": ("dotations-departements", ["exercice", "code_departement", "nom_departement"]),
}
# Jeux des dotations notifiées : source → (champ qui désigne la collectivité, sa forme, variables lues, en euros : le
# montant notifié de la dotation globale de fonctionnement, puis celui de chacune de ses parts). Leurs listes portent
# l'exercice, pour que deux listes identiques d'une année à l'autre restent deux copies. Le jeu des départements
# désigne aussi la collectivité de Corse (« 20 »), la Collectivité européenne d'Alsace (« 67A ») et la métropole de
# Lyon (« MET69 »).
DOTATIONS = {
    "ofgl.dotations-communes": ("code_insee", r"[0-9][0-9AB][0-9]{3}",
                                ["Montant Dotation DGF", "Montant Dotation forfaitaire", "Montant Dotation DSU",
                                 "Montant Dotation DSR", "Montant Dotation DNP", "Montant Dotation DACOM",
                                 "Montant Dotation d'amorçage"]),
    "ofgl.dotations-gfp": ("siren", r"[0-9]{9}",
                           ["Montant DGF", "Montant Dotation intercommunalité", "Montant Dotation de compensation",
                            "Montant Dotation des groupements touristiques"]),
    "ofgl.dotations-departements": ("code_departement", r"[0-9]{2,3}|[0-9]{2}A|2[AB]|MET69",
                                    ["Montant DGF notifiée totale", "Montant Dotation forfaitaire",
                                     "Montant Dotation de compensation", "Montant Dotation de fonctionnement minimale",
                                     "Montant Dotation de péréquation urbaine"]),
}
INVENTAIRE_DOTATIONS = ["exercice", "lignes"]
MONTANTS = ["siren", "agregat", "montant_bp", "montant_ba", "montant_flux", "montant"]
# Jeux publiés budget par budget, sans consolidation : une ligne par budget, désigné par son numéro SIRET (« ident »),
# et par agrégat ; leur liste est celle des budgets.
PAR_BUDGET = {"ofgl.base-sdis", "ofgl.base-ccas-cias"}
MONTANTS_BUDGETS = ["siren", "ident", "agregat", "montant"]
INVENTAIRE = ["exer", "lignes"]
# Champs qu'une collectivité peut avoir plusieurs fois, une ligne par valeur : un groupement s'étend sur plusieurs
# départements, voire plusieurs régions.
MULTIPLES = {"dep_code", "reg_code"}
POPULATIONS = {"ptot", "population_totale"}
CLES = {}  # copie de montants → numéros Siren, ou SIRET des budgets, qu'elle porte, pour contrôler la liste sans la relire


def requete(jeu, **parametres):
    return PORTAIL + jeu + "/exports/csv?" + urllib.parse.urlencode(parametres, quote_via=urllib.parse.quote, safe=",*()")


def requetes(source_id, exercice):
    """Les trois exports à archiver pour un exercice d'un jeu de données : inventaire, montants, collectivités."""
    jeu, champs_collectivites = JEUX[source_id]
    if source_id in DOTATIONS:
        cle, _, variables = DOTATIONS[source_id]
        lues, filtre = "variable in (" + ", ".join(f'"{v}"' for v in variables) + ")", f"exercice=date'{exercice}'"
        return {"inventaire": requete(jeu, select="exercice,count(*) as lignes", where=lues, group_by="exercice",
                                      order_by="exercice"),
                "montants": requete(jeu, select=f"{cle},variable,valeur", where=f"{filtre} and {lues}",
                                    order_by=f"{cle},variable"),
                "collectivites": requete(jeu, select=",".join(champs_collectivites), where=f"{filtre} and {lues}",
                                         group_by=",".join(champs_collectivites), order_by=",".join(champs_collectivites))}
    filtre = f"exer=date'{exercice}'"
    champs_montants = MONTANTS_BUDGETS if source_id in PAR_BUDGET else MONTANTS
    ordre = "siren,ident,agregat" if source_id in PAR_BUDGET else "siren,agregat"
    return {"inventaire": requete(jeu, select="exer,count(*) as lignes", group_by="exer", order_by="exer"),
            "montants": requete(jeu, select=",".join(champs_montants), where=filtre, order_by=ordre),
            "collectivites": requete(jeu, select=",".join(champs_collectivites), where=filtre,
                                     group_by=",".join(champs_collectivites), order_by=",".join(champs_collectivites))}


def nature(fichier):
    """(contenu, exercice) de la requête qui a produit la copie : l'une de celles que cet import sait lire."""
    if fichier["source_id"] not in JEUX:
        sys.exit(f"{fichier['id']} : la source {fichier['source_id']} n'est pas lue par cet import")
    trouve = re.search(r"where=exer(?:cice)?%3Ddate%27([0-9]{4})%27", fichier["url"])
    exercice = trouve.group(1) if trouve else "0000"
    for contenu, url in requetes(fichier["source_id"], exercice).items():
        if url == fichier["url"]:
            return contenu, "" if contenu == "inventaire" else exercice
    sys.exit(f"{fichier['id']} : requête que cet import ne sait pas lire ({fichier['url']})")


def montant(texte, lieu):
    try:
        valeur = float(texte)
    except ValueError:
        sys.exit(f"{lieu} : montant illisible « {texte} »")
    if not math.isfinite(valeur):
        sys.exit(f"{lieu} : montant illisible « {texte} »")
    return valeur


def lignes(fichier, attendu):
    """Les lignes d'une copie, après contrôle de son en-tête."""
    entete, contenu = lire_export_ofgl(BASE / fichier["chemin"])
    if entete != attendu:
        sys.exit(f"{fichier['id']} : en-tête {entete}, attendu {attendu}")
    for n, ligne in enumerate(contenu, start=2):
        if len(ligne) != len(attendu):
            sys.exit(f"{fichier['id']}, ligne {n} : {len(ligne)} champs au lieu de {len(attendu)}")
    return contenu


def inventaire(fichier):
    """{exercice: nombre de lignes}. Le portail regroupe les exercices par date : « 2024-01-01 00:00:00+00:00 »."""
    resultat = {}
    attendu = INVENTAIRE_DOTATIONS if fichier["source_id"] in DOTATIONS else INVENTAIRE
    for n, (exer, nombre) in enumerate(lignes(fichier, attendu), start=2):
        annee = re.fullmatch(r"([0-9]{4})(?:-01-01 00:00:00\+00:00)?", exer)
        if annee is None or annee.group(1) in resultat or not nombre.isdigit():
            sys.exit(f"{fichier['id']}, ligne {n} : ligne d'inventaire illisible")
        resultat[annee.group(1)] = int(nombre)
    if not resultat:
        sys.exit(f"{fichier['id']} : inventaire vide")
    return resultat


def marge(texte):
    """Demi-unité de la dernière décimale d'un montant publié, sans les zéros finaux (« 1103074315.0 » est un montant
    à l'euro), au centime au plus fin : les montants de 2022 n'ont que dix chiffres significatifs, ceux des autres
    exercices portent parfois des décimales de calcul au-delà du centime. Un montant nul est exact."""
    if "e" in texte.lower() or float(texte) == 0:
        return 0.005
    decimales = len(texte.split(".")[1].rstrip("0")) if "." in texte else 0
    return 0.5 * 10 ** -min(decimales, 2)


def montants(fichier, agregats, marges=False):
    """Les lignes de montants : [(siren, agrégat, budget principal, budgets annexes, flux croisés, consolidé)], et, si
    `marges`, la marge d'arrondi de chacun des quatre montants à la suite."""
    resultat, vues = [], set()
    for n, (siren, agregat, *valeurs) in enumerate(lignes(fichier, MONTANTS), start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        if not re.fullmatch(r"[0-9]{9}", siren):
            sys.exit(f"{lieu} : numéro Siren illisible « {siren} »")
        if agregat not in agregats:
            sys.exit(f"{lieu} : agrégat inconnu « {agregat} » (le déclarer dans tables/agregats_ofgl.csv)")
        if (siren, agregat) in vues:
            sys.exit(f"{lieu} : deuxième ligne pour {siren} et « {agregat} »")
        vues.add((siren, agregat))
        resultat.append((siren, agregat, *(montant(v, lieu) for v in valeurs))
                        + (tuple(marge(v) for v in valeurs) if marges else ()))
    return resultat


def montants_budgets(fichier, agregats, marges=False):
    """Les lignes de montants d'un jeu publié budget par budget : [(siren, SIRET du budget, agrégat, montant)], et, si
    `marges`, la marge d'arrondi du montant à la suite."""
    resultat, vues = [], set()
    for n, (siren, budget, agregat, texte) in enumerate(lignes(fichier, MONTANTS_BUDGETS), start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        if not re.fullmatch(r"[0-9]{9}", siren) or not re.fullmatch(siren + r"[0-9]{5}", budget):
            sys.exit(f"{lieu} : numéro Siren ou SIRET du budget illisible « {siren} », « {budget} »")
        if agregat not in agregats:
            sys.exit(f"{lieu} : agrégat inconnu « {agregat} » (le déclarer dans tables/agregats_ofgl.csv)")
        if (budget, agregat) in vues:
            sys.exit(f"{lieu} : deuxième ligne pour le budget {budget} et « {agregat} »")
        vues.add((budget, agregat))
        resultat.append((siren, budget, agregat, montant(texte, lieu)) + ((marge(texte),) if marges else ()))
    return resultat


def montants_dotations(fichier, marges=False):
    """Les lignes de montants d'un jeu des dotations : [(collectivité, variable, montant)], et, si `marges`, la marge
    d'arrondi du montant à la suite."""
    cle, forme, variables = DOTATIONS[fichier["source_id"]]
    resultat, vues = [], set()
    for n, (code, variable, texte) in enumerate(lignes(fichier, [cle, "variable", "valeur"]), start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        if not re.fullmatch(forme, code):
            sys.exit(f"{lieu} : collectivité illisible « {code} »")
        if variable not in variables:
            sys.exit(f"{lieu} : variable inattendue « {variable} »")
        if (code, variable) in vues:
            sys.exit(f"{lieu} : deuxième ligne pour {code} et « {variable} »")
        vues.add((code, variable))
        resultat.append((code, variable, montant(texte, lieu)) + ((marge(texte),) if marges else ()))
    return resultat


def collectivites(fichier):
    """({siren: {champ: valeur}}, nombre de lignes), les valeurs d'un champ multiple réunies, triées, séparées par
    « ; » ; pour un jeu publié budget par budget, la fiche de chaque budget, sous son SIRET ; pour un jeu des
    dotations, celle de chaque collectivité, sous le champ qui la désigne."""
    source = fichier["source_id"]
    champs_ = JEUX[source][1]
    cle = DOTATIONS[source][0] if source in DOTATIONS else "ident" if source in PAR_BUDGET else "siren"
    par_cle = collections.defaultdict(list)
    contenu = lignes(fichier, champs_)
    for n, ligne in enumerate(contenu, start=2):
        valeurs = dict(zip(champs_, ligne))
        if source in DOTATIONS:
            if not re.fullmatch(DOTATIONS[source][1], valeurs[cle]):
                sys.exit(f"{fichier['id']}, ligne {n} : collectivité illisible « {valeurs[cle]} »")
        elif not re.fullmatch(r"[0-9]{9}", valeurs["siren"]) or cle == "ident" and \
                not re.fullmatch(valeurs["siren"] + r"[0-9]{5}", valeurs["ident"]):
            sys.exit(f"{fichier['id']}, ligne {n} : numéro Siren ou SIRET illisible « {valeurs['siren']} »")
        for c in POPULATIONS & set(valeurs):
            if valeurs[c] and not valeurs[c].isdigit():
                sys.exit(f"{fichier['id']}, ligne {n} : population illisible « {valeurs[c]} »")
        par_cle[valeurs[cle]].append(valeurs)
    resultat = {}
    for identifiant, liste in par_cle.items():
        fiche = {}
        for c in champs_:
            distinctes = sorted({v[c] for v in liste})
            if len(distinctes) > 1 and c not in MULTIPLES:
                sys.exit(f"{fichier['id']} : {identifiant} a plusieurs valeurs de {c} ({distinctes})")
            fiche[c] = ";".join(distinctes)
        resultat[identifiant] = fiche
    return resultat, len(contenu)


def cles_montants(fichier, agregats):
    """Les numéros Siren, ou pour un jeu publié budget par budget les SIRET des budgets, pour un jeu des dotations les
    collectivités, d'une copie de montants."""
    if fichier["source_id"] in DOTATIONS:
        return {l[0] for l in montants_dotations(fichier)}
    if fichier["source_id"] in PAR_BUDGET:
        return {l[1] for l in montants_budgets(fichier, agregats)}
    return {l[0] for l in montants(fichier, agregats)}


def controleur(fichier, inscrits, contenu, exercice=""):
    """La copie inscrite qui en contrôle une autre : de même source, du contenu demandé (et du même exercice), la plus
    récente dont la version ne dépasse pas la sienne."""
    version = fichier["mis_a_jour_source"][:10]
    candidats = [i for i in inscrits if i["source_id"] == fichier["source_id"] and i["contenu"] == contenu
                 and i["exercice"] == exercice and i["version"] <= version]
    if not candidats:
        sys.exit(f"{fichier['id']} : aucune copie de {contenu} {exercice} inscrite pour cette source à cette version "
                 "(l'importer d'abord)")
    return max(candidats, key=lambda i: i["version"])["fichier_id"]


def inscription(fichier, inscrits, fichiers, agregats):
    """La ligne de tables/fichiers_collectivites.csv d'une copie, après contrôle de son contenu ; `inscrits` est la
    table déjà écrite, où l'on cherche les copies qui la contrôlent."""
    contenu, exercice = nature(fichier)
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas la date de modification du jeu de données")
    ligne = {"fichier_id": fichier["id"], "source_id": fichier["source_id"], "contenu": contenu, "exercice": exercice,
             "version": version, "statut": "", "lignes": "", "collectivites": ""}
    if contenu == "inventaire":
        ligne["lignes"] = str(len(inventaire(fichier)))
        return ligne
    exercices = inventaire(fichiers[controleur(fichier, inscrits, "inventaire")])
    if exercice not in exercices:
        sys.exit(f"{fichier['id']} : l'exercice {exercice} manque à l'inventaire")
    par_budget, dotations = fichier["source_id"] in PAR_BUDGET, fichier["source_id"] in DOTATIONS
    if contenu == "montants":
        lues = (montants_dotations(fichier) if dotations else montants_budgets(fichier, agregats) if par_budget
                else montants(fichier, agregats))
        if len(lues) != exercices[exercice]:
            sys.exit(f"{fichier['id']} : {len(lues)} lignes, l'inventaire en annonce {exercices[exercice]}")
        nombre, sirens = len(lues), {l[0] for l in lues}
        CLES[fichier["id"]] = {l[1] for l in lues} if par_budget else sirens
    else:
        fiches, nombre = collectivites(fichier)
        sirens = set(fiches) if dotations else {f["siren"] for f in fiches.values()}
        if dotations and any(not f["exercice"].startswith(exercice) for f in fiches.values()):
            sys.exit(f"{fichier['id']} : la liste porte un autre exercice que {exercice}")
        temoin = controleur(fichier, inscrits, "montants", exercice)
        if temoin not in CLES:
            CLES[temoin] = cles_montants(fichiers[temoin], agregats)
        attendus = CLES[temoin]
        if set(fiches) != attendus:
            sys.exit(f"{fichier['id']} : la liste des {'budgets' if par_budget else 'collectivités'} n'est pas celle "
                     f"des montants ({len(set(fiches) - attendus)} en plus, {len(attendus - set(fiches))} en moins)")
    ligne.update(statut="provisoire" if exercice == max(exercices) else "definitif", lignes=str(nombre),
                 collectivites=str(len(sirens)))
    return ligne


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--requetes":
        for url in requetes(sys.argv[2], sys.argv[3]).values():
            print(url)
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    agregats = {a["agregat"]: a for a in lire("tables/agregats_ofgl.csv")}
    inscrits = [i for i in lire("tables/fichiers_collectivites.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]], inscrits, fichiers, agregats)
    ecrire("tables/fichiers_collectivites.csv", champs("fichiers_collectivites"), inscrits + [ligne], cle="fichier_id")
    print(f"{ligne['fichier_id']} : {ligne['contenu']} {ligne['exercice']} ({ligne['version']}, {ligne['statut'] or '—'}), "
          f"{ligne['lignes']} lignes" + (f", {ligne['collectivites']} collectivités" if ligne["collectivites"] else ""))


if __name__ == "__main__":
    main()
