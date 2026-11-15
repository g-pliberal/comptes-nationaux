"""Les formules par lesquelles l'Observatoire des finances et de la gestion publique locales (OFGL) tire ses agrégats
financiers des balances comptables des collectivités, et leur calcul.

Le jeu de données « Méthodologie OFGL - Formules des agrégats financiers » donne, pour chaque catégorie de collectivités,
chaque exercice depuis 2012, chaque agrégat, chaque sorte de calcul, chaque sorte de budget (principal, annexe) et chaque
nomenclature budgétaire et comptable, une formule, et une remarque quand elle ne vaut que pour certaines collectivités.
Une formule est une somme de termes, chacun ajouté ou retranché :
- une grandeur de la balance et un compte, qui désigne ce compte et tous ceux dont le numéro le prolonge : « DN6 » est la
  somme des comptes de la classe 6 ;
- un autre agrégat, sous son nom, parfois suivi d'une explication entre parenthèses : « Remboursements d'emprunts hors
  GAD (gestion active de la dette) » ;
- le plus petit de deux termes : « minimum(D16449 ; C16449) » ;
- une somme de termes entre parenthèses.
Une formule de flux croisés qui commence par « Flux croisés sur : » se calcule avec les formules de flux croisés des
agrégats qu'elle nomme.

Le jeu ne dit pas ce que mesure chaque grandeur. La base en retient le sens qui redonne au centime les agrégats publiés
par l'OFGL, montré par le rapport de cohérence : les opérations sont réelles, c'est-à-dire les opérations budgétaires de
l'exercice moins les opérations d'ordre budgétaires.
- D, C : opérations réelles au débit, au crédit ;
- DN, CN : opérations réelles au débit moins celles au crédit, et l'inverse ;
- SD, SC : solde de sortie débiteur, créditeur ; SDN, SCN : le premier moins le second, et l'inverse ;
- OOC : opérations d'ordre budgétaires au crédit.
Un agrégat qu'une formule nomme et qui n'a pas de formule pour la sorte de budget et la nomenclature est nul.
"""

import collections
import re
import sys

from commun import BASE, lire_export_ofgl

ENTETE = ["type_collectivite", "annee", "agregat", "type_calcul", "budgets", "nomenclatures", "ensemble_collectivites",
          "remarques", "formule"]
BRUT, FLUX = "Agrégat brut", "Flux croisé BP-BA neutralisé"
CALCULS = {BRUT, FLUX, "Flux croisé communes-GFP neutralisé"}
SORTES = {"Budgets principaux": "principal", "Budgets annexes": "annexe"}
PREFIXE_FLUX = "Flux croisés sur :"
# Grandeur → fonction des montants d'une ligne de balance, en centimes, dans l'ordre des fichiers : balance d'entrée,
# opérations budgétaires, opérations non budgétaires, opérations d'ordre budgétaires, au débit et au crédit, solde de
# sortie débiteur et créditeur.
GRANDEURS = {
    "D": lambda m: m[2] - m[6], "C": lambda m: m[3] - m[7],
    "DN": lambda m: m[2] - m[6] - m[3] + m[7], "CN": lambda m: m[3] - m[7] - m[2] + m[6],
    "SD": lambda m: m[8], "SC": lambda m: m[9], "SDN": lambda m: m[8] - m[9], "SCN": lambda m: m[9] - m[8],
    "OOC": lambda m: m[7],
}
TERME_COMPTE = re.compile(r"(SDN|SCN|OOC|DN|CN|SD|SC|D|C)([0-9]+[0-9A-Z]*)(?![\w'])")
# Collectivités que désignent les remarques des formules, par numéro Siren.
CTU_GUYANE_MARTINIQUE = {"200052678", "200055507"}
CORSE = {"200076958"}
ILE_DE_FRANCE = {"237500079"}
PARIS = {"217500016"}
METROPOLE_DE_LYON = {"200046977"}
# Les onze établissements publics territoriaux de la Métropole du Grand Paris.
EPT = {"200057867", "200057875", "200057941", "200057966", "200057974", "200057982", "200057990", "200058006",
       "200058014", "200058097", "200058790"}
# Les communes de la Métropole du Grand Paris : celles de Paris et des trois départements de la petite couronne, et sept
# communes de l'Essonne et du Val-d'Oise (Athis-Mons, Juvisy-sur-Orge, Morangis, Paray-Vieille-Poste, Savigny-sur-Orge,
# Viry-Châtillon, Argenteuil).
PETITE_COURONNE = {"75", "92", "93", "94"}
GRAND_PARIS_AU_DELA = {"219100278", "219103264", "219104320", "219104791", "219105897", "219106879", "219500188"}


def grand_paris(fiche):
    """Vrai pour une commune de la Métropole du Grand Paris ; les balances écrivent le département sur deux ou trois
    chiffres (« 92 », « 092 »)."""
    departement = fiche["departement"]
    if len(departement) == 3 and departement.startswith("0"):
        departement = departement[1:]
    return departement in PETITE_COURONNE or fiche["siren"] in GRAND_PARIS_AU_DELA


# Remarque → la condition, sur la fiche d'un budget (son numéro Siren, son département), d'une collectivité à qui la
# formule s'applique.
REMARQUES = {
    "": lambda fiche: True,
    "formule spécifique aux CTU de Guyane et de Martinique et à la Collectivité Corse":
        lambda fiche: fiche["siren"] in CTU_GUYANE_MARTINIQUE | CORSE,
    "formule applicable aux régions à l'exclusion des CTU de Guyane et de Martinique et de la Collectivité Corse":
        lambda fiche: fiche["siren"] not in CTU_GUYANE_MARTINIQUE | CORSE,
    "formule spécifique aux CTU de Guyane et de Martinique": lambda fiche: fiche["siren"] in CTU_GUYANE_MARTINIQUE,
    "formule applicable aux régions à l'exclusion des CTU de Guyane et de Martinique":
        lambda fiche: fiche["siren"] not in CTU_GUYANE_MARTINIQUE,
    "formule spécifique à la région Ile-de-France": lambda fiche: fiche["siren"] in ILE_DE_FRANCE,
    "formule applicable aux régions à l'exclusion de la région Ile-de-France":
        lambda fiche: fiche["siren"] not in ILE_DE_FRANCE,
    "formule spécifique à la Ville de Paris": lambda fiche: fiche["siren"] in PARIS,
    "formule spécifique aux communes de la Métropole du Grand Paris": grand_paris,
    "formule applicable aux communes à l'exclusion des communes appartenant à la Métropole du Grand Paris":
        lambda fiche: not grand_paris(fiche),
    "formule spécifique à la Métropole de Lyon": lambda fiche: fiche["siren"] in METROPOLE_DE_LYON,
    "formule spécifique aux établissements publics territoriaux de la Métropole du Grand Paris":
        lambda fiche: fiche["siren"] in EPT,
    "formule applicable aux Groupements à fiscalité propre à l'exclusion des établissements publics territoriaux de "
    "la Métropole du Grand Paris": lambda fiche: fiche["siren"] not in EPT,
}
# Fiches témoins sur lesquelles se vérifie qu'une seule formule s'applique : une collectivité de chaque groupe que nomme
# une remarque, et une autre.
TEMOINS = [{"siren": s, "departement": d} for s, d in
           [("200052678", "973"), ("200055507", "972"), ("200076958", "2A"), ("237500079", "75"),
            ("217500016", "75"), ("219200045", "92"), ("219100278", "91"), ("200046977", "69"), ("200057867", "93"),
            ("000000000", "01")]]
# Catégories de collectivités dont la base recalcule les agrégats : celles dont elle a les balances.
RECALCULEES = {"Départements", "Régions", "Communes", "Groupements à fiscalité propre", "Syndicats", "EPL"}


def analyser(texte, noms, lieu):
    """L'arbre d'une formule : [(signe, terme)], un terme étant ("compte", grandeur, compte), ("agregat", nom),
    ("groupe", arbre) pour une somme entre parenthèses, ou ("minimum", arbre, arbre). Les noms d'agrégats se reconnaissent au plus long de `noms` : certains portent un tiret
    (« Encours de dette - Dépôts et cautionnements reçus »)."""
    texte = " ".join(texte.split())

    def somme(i, fin):
        arbre, signe = [], 1
        while True:
            while i < len(texte) and texte[i] == " ":
                i += 1
            terme, i = un_terme(i)
            arbre.append((signe, terme))
            while i < len(texte) and texte[i] == " ":
                i += 1
            if i >= len(texte) or texte[i] in fin:
                return arbre, i
            if texte[i] not in "+-":
                sys.exit(f"{lieu} : formule illisible à « {texte[i:i + 30]} » ({texte})")
            signe = 1 if texte[i] == "+" else -1
            i += 1

    def un_terme(i):
        if texte.startswith("minimum(", i):
            premier, i = somme(i + len("minimum("), ";")
            if i >= len(texte) or texte[i] != ";":
                sys.exit(f"{lieu} : minimum illisible ({texte})")
            second, i = somme(i + 1, ")")
            if i >= len(texte) or texte[i] != ")":
                sys.exit(f"{lieu} : minimum illisible ({texte})")
            return ("minimum", premier, second), i + 1
        if texte.startswith("(", i):
            groupe, i = somme(i + 1, ")")
            if i >= len(texte) or texte[i] != ")":
                sys.exit(f"{lieu} : parenthèse non fermée ({texte})")
            return ("groupe", groupe), i + 1
        compte = TERME_COMPTE.match(texte, i)
        if compte:
            return ("compte", compte.group(1), compte.group(2)), compte.end()
        nom = max((n for n in noms if texte.startswith(n, i) and (i + len(n) == len(texte) or texte[i + len(n)] in " ;)")),
                  key=len, default=None)
        if nom is None:
            sys.exit(f"{lieu} : terme inconnu à « {texte[i:i + 40]} » ({texte})")
        i += len(nom)
        if texte.startswith(" (", i):  # explication du nom
            fin = texte.find(")", i)
            if fin < 0:
                sys.exit(f"{lieu} : parenthèse non fermée ({texte})")
            i = fin + 1
        return ("agregat", nom), i

    flux = texte.startswith(PREFIXE_FLUX)
    debut = len(PREFIXE_FLUX) if flux else 0
    arbre, fin = somme(debut, "")
    if fin != len(texte):
        sys.exit(f"{lieu} : formule illisible ({texte})")
    return arbre


def formules(fichier):
    """Les formules d'une copie du jeu : [{champ: valeur, "sortes": ensemble des sortes de budget, "nomenclatures":
    ensemble, "arbre": arbre, ou None pour une formule illisible}], après contrôle : pour les catégories que la base
    recalcule, chaque formule se lit ; deux formules qui s'appliquent à la même collectivité pour un exercice, un agrégat,
    une sorte de calcul, une sorte de budget et une nomenclature sont marquées « ambigue »."""
    entete, lignes = lire_export_ofgl(BASE / fichier["chemin"])
    if entete != ENTETE:
        sys.exit(f"{fichier['id']} : en-tête {entete}, attendu {ENTETE}")
    # Une formule peut nommer un agrégat que le jeu ne définit pas pour sa catégorie de collectivités (les travaux en
    # régie des centres d'action sociale) : il y est nul.
    noms = set()
    for ligne in lignes:
        if len(ligne) != len(ENTETE):
            sys.exit(f"{fichier['id']} : ligne de {len(ligne)} champs au lieu de {len(ENTETE)}")
        noms.add(ligne[2])
    resultat, cles = [], collections.defaultdict(list)
    for n, ligne in enumerate(lignes, start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        f = dict(zip(ENTETE, ligne))
        if not re.fullmatch(r"20[0-9]{2}", f["annee"]) or f["type_calcul"] not in CALCULS:
            sys.exit(f"{lieu} : exercice ou sorte de calcul inattendu « {f['annee']} », « {f['type_calcul']} »")
        sortes = {SORTES.get(s) for s in f["budgets"].split(",")}
        if None in sortes:
            sys.exit(f"{lieu} : sorte de budget inattendue « {f['budgets']} »")
        # Quelques formules d'autres catégories ne se lisent pas : celles des SDIS de 2021 nomment
        # « 1impots_locaux1 » ; la base ne les applique pas.
        try:
            arbre = analyser(f["formule"], noms, lieu)
        except SystemExit:
            if f["type_collectivite"] in RECALCULEES:
                raise
            arbre = None
        f.update(sortes=sortes, nomenclatures=set(f["nomenclatures"].split(",")), nomenclatures_texte=f["nomenclatures"],
                 arbre=arbre)
        if f["type_collectivite"] in RECALCULEES:
            if f["remarques"] not in REMARQUES:
                sys.exit(f"{lieu} : remarque que la base ne sait pas appliquer « {f['remarques']} »")
            for sorte in sortes:
                for nomenclature in f["nomenclatures"]:
                    cles[(f["type_collectivite"], f["annee"], f["agregat"], f["type_calcul"], sorte, nomenclature)].append(
                        (n, f["remarques"]))
        resultat.append(f)
    # Deux formules pour la même clé doivent se partager les collectivités : l'une pour celles que nomme la remarque,
    # l'autre pour les autres ; on le vérifie sur les collectivités que désignent les remarques et sur une autre.
    # Le jeu en a parfois deux qui se contredisent (celles des syndicats et des établissements publics locaux de 2016
    # pour la fiscalité reversée, l'une retranchant un compte que l'autre ne retranche pas) : la base n'en applique
    # aucune, et le rapport de cohérence les cite.
    for cle, rangs in cles.items():
        for temoin in TEMOINS:
            applicables = [n for n, remarque in rangs if REMARQUES[remarque](temoin)]
            if len(applicables) > 1:
                for n in applicables:
                    resultat[n - 2]["ambigue"] = True
    return resultat


def ambigues(toutes):
    """[(catégorie, exercice, agrégat, sorte de calcul, nomenclatures)] des formules que la base n'applique pas parce
    qu'une autre formule s'applique aux mêmes collectivités."""
    return sorted({(f["type_collectivite"], f["annee"], f["agregat"], f["type_calcul"], f["nomenclatures_texte"])
                   for f in toutes if f.get("ambigue")})


class Formulaire:
    """Les formules d'une catégorie de collectivités pour un exercice, prêtes à calculer."""

    def __init__(self, toutes, categorie, exercice):
        self.index = collections.defaultdict(list)
        self.agregats = set()
        for f in toutes:
            if f["type_collectivite"] == categorie and f["annee"] == exercice and f["type_calcul"] in (BRUT, FLUX) \
                    and not f.get("ambigue"):
                for sorte in f["sortes"]:
                    for nomenclature in f["nomenclatures"]:
                        self.index[(f["type_calcul"], sorte, nomenclature, f["agregat"])].append(
                            (REMARQUES[f["remarques"]], f["arbre"]))
                if f["type_calcul"] == BRUT:
                    self.agregats.add(f["agregat"])

    def arbre(self, calcul, sorte, nomenclature, agregat, fiche):
        """L'arbre de la formule qui s'applique au budget de fiche `fiche`, ou None."""
        return next((a for s, a in self.index.get((calcul, sorte, nomenclature, agregat), []) if s(fiche)), None)

    def budget(self, fiche, comptes):
        """{agrégat: (montant brut, flux croisés)} d'un budget, en centimes, d'après ses comptes ({compte: montants en
        centimes}) ; un montant est None si aucune formule ne s'applique au budget."""
        # Les montants de chaque début de numéro de compte, sommés sur les comptes qui commencent ainsi ; les grandeurs
        # sont des sommes et des différences de montants : celle d'un regroupement est celle de ses montants sommés.
        prefixes = collections.defaultdict(lambda: [0] * 10)
        for numero, montants in comptes.items():
            for k in range(1, len(numero) + 1):
                somme = prefixes[numero[:k]]
                for i, m in enumerate(montants):
                    somme[i] += m

        def compte(grandeur, numero):
            return GRANDEURS[grandeur](prefixes[numero]) if numero in prefixes else 0

        memoires = {BRUT: {}, FLUX: {}}

        def agregat(calcul, nom):
            memoire = memoires[calcul]
            if nom not in memoire:
                memoire[nom] = None  # garde contre une formule qui se nommerait elle-même
                arbre = self.arbre(calcul, fiche["type_budget"], fiche["nomenclature"], nom, fiche)
                memoire[nom] = None if arbre is None else evaluer(calcul, arbre)
            return memoire[nom]

        def evaluer(calcul, arbre):
            total = 0
            for signe, terme in arbre:
                if terme[0] == "compte":
                    valeur = compte(terme[1], terme[2])
                elif terme[0] == "agregat":
                    valeur = agregat(calcul, terme[1]) or 0
                elif terme[0] == "groupe":
                    valeur = evaluer(calcul, terme[1])
                else:
                    valeur = min(evaluer(calcul, terme[1]), evaluer(calcul, terme[2]))
                total += signe * valeur
            return total

        return {nom: (agregat(BRUT, nom), agregat(FLUX, nom)) for nom in self.agregats}


def recalculer(formulaire, budgets):
    """{agrégat: [budget principal, budgets annexes, flux croisés]} d'une collectivité, en centimes, d'après ses budgets
    [(budget, fiche, {compte: montants})] ; le montant des budgets annexes est la somme de ceux auxquels une formule
    s'applique, celui des flux croisés la somme de ceux de tous les budgets ; un montant est None si aucune formule ne
    s'applique."""
    resultat = collections.defaultdict(lambda: [None, None, None])
    for _, fiche, comptes in budgets:
        k = 0 if fiche["type_budget"] == "principal" else 1
        for nom, (brut, flux) in formulaire.budget(fiche, comptes).items():
            ligne = resultat[nom]
            if brut is not None:
                ligne[k] = (ligne[k] or 0) + brut
            if flux is not None:
                ligne[2] = (ligne[2] or 0) + flux
    return resultat
