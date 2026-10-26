#!/usr/bin/env python3
"""Inscrit dans la base les balances des comptes de l'État que publie la DGFiP sur data.economie.gouv.fr, à partir des
copies archivées des exports de son jeu de données et de ses pièces jointes.

    python3 outils/importer_balances_etat.py --requetes <guide|plan|inventaire|balance>
    python3 outils/importer_balances_etat.py <fichier_id>

Le jeu « Données de comptabilité générale de l'État sur dix ans » réunit les balances générales des comptes qui ont
servi à produire le compte général de l'État, de 2016 à 2025, telles qu'elles étaient à la clôture de chaque exercice :
pour chaque exercice, une ligne par compte du plan comptable de l'État, mission, programme et nature budgétaire, avec son
solde de sortie en euros. La DGFiP rattache chaque ligne à une catégorie (actif, passif, situation nette, charges,
produits, engagements hors bilan), à un poste et à un sous-poste des états financiers du compte général, à un indicateur
de synthèse, qui distingue en outre le montant brut d'un actif de ses amortissements et dépréciations, et à un
indicateur de détail.

Quatre sortes de copies sont archivées, et s'importent dans cet ordre :
- le guide de lecture joint au jeu, dont l'import vérifie qu'il énonce la convention de signe que la base applique : un
  solde créditeur est négatif ;
- le plan comptable de l'État joint au jeu, qui donne le libellé de chaque compte ;
- l'inventaire du jeu : le nombre de lignes de chaque exercice ;
- pour chaque exercice, la balance : les champs qui désignent et décrivent chaque ligne, et son solde.
L'import vérifie que chaque ligne d'une balance est de l'exercice et que son compte, sa mission, son programme et sa
nature budgétaire n'y désignent qu'elle ; que son solde est un montant au centime (le jeu en écrit quelques-uns avec
des décimales parasites, « 58196841.8299982 », « 1.13686837721616e-13 », que la base arrondit) ; que son indicateur
de synthèse est l'un de ceux que tables/indicateurs_balances_etat.csv rattache aux états financiers pour l'exercice,
sous la catégorie et le poste qu'il leur donne ; et que la copie a le nombre de lignes que l'inventaire annonce. Il
inscrit la copie dans tables/fichiers_balances_etat.csv. La version d'une copie d'un export est la date de modification
du jeu de données qu'annonce le portail, celle d'une pièce jointe la date de modification inscrite dans le fichier ;
l'inventaire qui contrôle une balance est le plus récent dont la version ne dépasse pas la sienne. Ces copies sont les
chiffres eux-mêmes : la base ne les recopie pas, elle les lit.
"""

import decimal
import re
import sys
import urllib.parse

from commun import BASE, champs, ecrire, lire, lire_export_ofgl, lire_pdf, lire_xlsx, texte_pdf

PORTAIL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
SOURCE = "dgfip.balances-comptes-etat"
JEU = "balances_des_comptes_etat"
EXERCICES = [str(a) for a in range(2016, 2026)]
GUIDE = "guide_de_lecture_des_balances_comptables_de_letat_pdf"
PLAN = "plan_comptable_de_letatxlsx"
FEUILLE_PLAN = "PCE_(Plan_de_comptes)"
ENTETE_PLAN = ["Numéro de compte", "Libellé complet du Plan comptable de l'Etat"]
CONVENTION = "Un solde créditeur est signé négativement."
# Champs lus de chaque ligne d'une balance, dans l'ordre de l'export : l'exercice, ceux qui désignent la ligne et ceux qui
# la décrivent, son solde.
CHAMPS = ["annee", "compte", "mission", "libellemission", "programme", "nature_budgetaire", "libelle_ministere",
          "categorie", "postes", "sous_postes", "indicateurs_de_synthese", "indicateurs_de_detail", "balance_sortie"]
CLE = ["compte", "mission", "programme", "nature_budgetaire"]
COMPTE = re.compile(r"[0-9]{10}")
MONTANT = re.compile(r"-?[0-9]+(?:\.[0-9]+)?(?:e[-+]?[0-9]+)?")
# L'inventaire écrit chaque exercice comme une date, le 1er janvier à minuit.
EXERCICE_INVENTAIRE = re.compile(r"([0-9]{4})-01-01 00:00:00\+00:00")
CENTIME = decimal.Decimal("0.01")
# Au-delà d'un centième de centime, une décimale après les centimes ne serait plus un artefact : les écarts au centime
# des balances, des sommes en virgule flottante, ne dépassent pas deux millionièmes d'euro.
PARASITE = decimal.Decimal("0.0001")


def requete(**parametres):
    return PORTAIL + JEU + "/exports/csv?" + urllib.parse.urlencode(parametres, quote_via=urllib.parse.quote, safe=",*()")


def requetes(contenu):
    """Les requêtes à archiver pour une sorte de copie : {requête: exercice}."""
    if contenu in ("guide", "plan"):
        return {f"{PORTAIL}{JEU}/attachments/{GUIDE if contenu == 'guide' else PLAN}": ""}
    if contenu == "inventaire":
        return {requete(select="annee,count(*) as lignes", group_by="annee", order_by="annee"): ""}
    return {requete(select=",".join(CHAMPS), where=f"year(annee)={a}", order_by=",".join(CLE)): a for a in EXERCICES}


def nature(fichier):
    """(contenu, exercice) de la requête qui a produit la copie : l'une de celles que cet import sait lire."""
    if fichier["source_id"] != SOURCE:
        sys.exit(f"{fichier['id']} : la source {fichier['source_id']} n'est pas lue par cet import")
    for contenu in ("guide", "plan", "inventaire", "balance"):
        if fichier["url"] in (connues := requetes(contenu)):
            return contenu, connues[fichier["url"]]
    sys.exit(f"{fichier['id']} : requête que cet import ne sait pas lire ({fichier['url']})")


def lignes(fichier, attendu):
    """Les lignes d'un export, après contrôle de son en-tête."""
    entete, contenu = lire_export_ofgl(BASE / fichier["chemin"])
    if entete != attendu:
        sys.exit(f"{fichier['id']} : en-tête {entete}, attendu {attendu}")
    for n, ligne in enumerate(contenu, start=2):
        if len(ligne) != len(attendu):
            sys.exit(f"{fichier['id']}, ligne {n} : {len(ligne)} champs au lieu de {len(attendu)}")
    return contenu


def guide(fichier):
    """Le nombre de pages du guide de lecture, qui doit énoncer la convention de signe des balances."""
    pages = lire_pdf(BASE / fichier["chemin"])
    texte = " ".join(texte_pdf(morceaux) for page in pages for _, morceaux in page)
    if CONVENTION not in " ".join(texte.split()):
        sys.exit(f"{fichier['id']} : le guide n'énonce plus « {CONVENTION} »")
    return len(pages)


def plan(fichier):
    """{compte: libellé} : les comptes du plan comptable de l'État et leurs regroupements (classes, comptes de deux à neuf
    chiffres). Le classeur écrit en nombre un numéro de dix chiffres, en texte la plupart des autres ; quelques
    regroupements n'y ont pas de libellé, mais chaque compte en a un."""
    _, cellules = lire_xlsx(BASE / fichier["chemin"], FEUILLE_PLAN)
    rangees = {}
    for reference, valeur in cellules.items():
        colonne, rang = re.fullmatch(r"([A-Z]+)([0-9]+)", reference).groups()
        rangees.setdefault(int(rang), {})[colonne] = valeur
    entete = min(rangees)
    if [rangees[entete].get(c) for c in ("A", "B")] != ENTETE_PLAN:
        sys.exit(f"{fichier['id']} : en-tête de la feuille {FEUILLE_PLAN} inattendu")
    resultat = {}
    for rang in sorted(rangees)[1:]:
        numero, libelle = rangees[rang].get("A"), rangees[rang].get("B", "")
        if isinstance(numero, float) and numero == int(numero):
            numero = str(int(numero))
        if (not isinstance(numero, str) or not re.fullmatch(r"[0-9]{1,10}", numero.strip())
                or len(numero.strip()) == 10 and not str(libelle).strip()):
            sys.exit(f"{fichier['id']}, ligne {rang} : compte illisible « {numero} » « {libelle} »")
        if numero.strip() in resultat:
            sys.exit(f"{fichier['id']}, ligne {rang} : deuxième ligne pour le compte {numero}")
        resultat[numero.strip()] = " ".join(str(libelle).split())
    return resultat


def inventaire(fichier):
    """{exercice: nombre de lignes}."""
    resultat = {}
    for n, (annee, nombre) in enumerate(lignes(fichier, ["annee", "lignes"]), start=2):
        trouve = EXERCICE_INVENTAIRE.fullmatch(annee)
        if trouve is None or trouve.group(1) in resultat or not nombre.isdigit():
            sys.exit(f"{fichier['id']}, ligne {n} : ligne d'inventaire illisible")
        resultat[trouve.group(1)] = int(nombre)
    return resultat


def indicateurs_de(exercice, referentiel):
    """{indicateur de synthèse: ligne du référentiel} pour un exercice."""
    resultat = {}
    for i in referentiel:
        if i["premier_exercice"] <= exercice <= i["dernier_exercice"]:
            if i["indicateur"] in resultat:
                sys.exit(f"tables/indicateurs_balances_etat.csv : deux lignes de {i['indicateur']} couvrent {exercice}")
            resultat[i["indicateur"]] = i
    return resultat


def balance(fichier, referentiel):
    """(exercice, [{champ: texte}, …], [solde, …]) d'une copie de balance : les champs de chaque ligne, sans l'exercice ni
    le solde, et son solde en euros, au centime (decimal.Decimal)."""
    contenu, exercice = nature(fichier)
    if contenu != "balance":
        sys.exit(f"{fichier['id']} : copie de {contenu}, pas de balance")
    rattaches = indicateurs_de(exercice, referentiel)
    decrites, soldes, vues = [], [], set()
    for n, ligne in enumerate(lignes(fichier, CHAMPS), start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        valeurs = dict(zip(CHAMPS, ligne))
        if valeurs["annee"] != exercice:
            sys.exit(f"{lieu} : exercice « {valeurs['annee']} » au lieu de {exercice}")
        if not COMPTE.fullmatch(valeurs["compte"]):
            sys.exit(f"{lieu} : compte illisible « {valeurs['compte']} »")
        cle = tuple(valeurs[c] for c in CLE)
        if cle in vues:
            sys.exit(f"{lieu} : deuxième ligne pour {dict(zip(CLE, cle))}")
        vues.add(cle)
        if not MONTANT.fullmatch(valeurs["balance_sortie"]):
            sys.exit(f"{lieu} : solde illisible « {valeurs['balance_sortie']} »")
        solde = decimal.Decimal(valeurs["balance_sortie"])
        arrondi = solde.quantize(CENTIME, rounding=decimal.ROUND_HALF_EVEN)
        if abs(solde - arrondi) > PARASITE:
            sys.exit(f"{lieu} : solde « {valeurs['balance_sortie']} » qui n'est pas au centime")
        indicateur = rattaches.get(valeurs["indicateurs_de_synthese"])
        if indicateur is None:
            sys.exit(f"{lieu} : indicateur « {valeurs['indicateurs_de_synthese']} » que le référentiel ne rattache pas "
                     f"aux états financiers de {exercice}")
        if (valeurs["categorie"], valeurs["postes"]) != (indicateur["categorie"], indicateur["poste"]):
            sys.exit(f"{lieu} : {indicateur['indicateur']} sous « {valeurs['categorie']} », « {valeurs['postes']} », "
                     f"que le référentiel range sous « {indicateur['categorie']} », « {indicateur['poste']} »")
        decrites.append({c: valeurs[c] for c in CHAMPS[1:-1]})
        soldes.append(arrondi)
    return exercice, decrites, soldes


def controleur(fichier, inscrits):
    """L'inventaire inscrit qui contrôle une balance : le plus récent dont la version ne dépasse pas la sienne."""
    version = fichier["mis_a_jour_source"][:10]
    candidats = [i for i in inscrits if i["contenu"] == "inventaire" and i["version"] <= version]
    if not candidats:
        sys.exit(f"{fichier['id']} : aucun inventaire inscrit à cette version (l'importer d'abord)")
    return max(candidats, key=lambda i: i["version"])["fichier_id"]


def inscription(fichier, inscrits, fichiers, referentiel):
    """La ligne de tables/fichiers_balances_etat.csv d'une copie, après contrôle de son contenu ; `inscrits` est la table
    déjà écrite, où l'on cherche l'inventaire qui la contrôle."""
    contenu, exercice = nature(fichier)
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas sa version")
    ligne = {"fichier_id": fichier["id"], "source_id": fichier["source_id"], "contenu": contenu, "exercice": exercice,
             "version": version, "lignes": "", "comptes": ""}
    if contenu == "guide":
        ligne["lignes"] = str(guide(fichier))
    elif contenu == "plan":
        comptes = plan(fichier)
        ligne.update(lignes=str(len(comptes)), comptes=str(sum(1 for c in comptes if len(c) == 10)))
    elif contenu == "inventaire":
        exercices = inventaire(fichier)
        if sorted(exercices) != EXERCICES:
            sys.exit(f"{fichier['id']} : le jeu porte les exercices {sorted(exercices)}, pas ceux de {EXERCICES[0]} à "
                     f"{EXERCICES[-1]}")
        ligne["lignes"] = str(len(exercices))
    else:
        annonce = inventaire(fichiers[controleur(fichier, inscrits)])
        _, decrites, _ = balance(fichier, referentiel)
        if len(decrites) != annonce[exercice]:
            sys.exit(f"{fichier['id']} : {len(decrites)} lignes, l'inventaire en annonce {annonce[exercice]}")
        ligne.update(lignes=str(len(decrites)), comptes=str(len({d["compte"] for d in decrites})))
    return ligne


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--requetes":
        if sys.argv[2] not in ("guide", "plan", "inventaire", "balance"):
            sys.exit(__doc__)
        for url in requetes(sys.argv[2]):
            print(url)
        return
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    referentiel = lire("tables/indicateurs_balances_etat.csv")
    inscrits = [i for i in lire("tables/fichiers_balances_etat.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]], inscrits, fichiers, referentiel)
    ecrire("tables/fichiers_balances_etat.csv", champs("fichiers_balances_etat"), inscrits + [ligne], cle="fichier_id")
    unite = {"guide": "page", "plan": "entrée", "inventaire": "exercice", "balance": "ligne"}[ligne["contenu"]]
    quoi = " ".join(x for x in (ligne["contenu"], ligne["exercice"]) if x)
    print(f"{ligne['fichier_id']} : {quoi} ({ligne['version']}), {ligne['lignes']} {unite}"
          f"{'s' if int(ligne['lignes']) > 1 else ''}" + (f", {ligne['comptes']} comptes" if ligne["comptes"] else ""))


if __name__ == "__main__":
    main()
