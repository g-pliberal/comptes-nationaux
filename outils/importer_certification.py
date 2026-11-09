#!/usr/bin/env python3
"""Enregistre dans la base le détail des engagements hors bilan de l'État, tel que le donne le tableau des principaux
engagements hors bilan du compte général de l'État que la Cour des comptes reproduit en annexe de son rapport de
certification des comptes de l'État (article 58, 5° de la loi organique relative aux lois de finances), dans le PDF
archivé de ce rapport.

    python3 outils/importer_certification.py <fichier_id>

Le compte général de l'État lui-même est sur budget.gouv.fr, qui refuse les robots ; les balances des comptes de l'État
que la base lit déjà ne donnent les engagements hors bilan que par grande catégorie, et ne portent pas ceux que l'État
n'inscrit pas dans ses comptes de la classe 8 (les engagements de retraite, notamment). Le tableau que reproduit la
Cour a deux parties, les engagements donnés et les engagements reçus, chacune sous un en-tête qui nomme l'exercice et
le précédent (« 31/12/2024 », « 31/12/2023 retraité », « Variation »). Chaque ligne porte un libellé et, à droite, le
montant à la clôture de l'exercice, celui de la clôture précédente et leur variation ; une ligne de titre n'a pas de
montant. Le retrait du libellé dit de quelle ligne elle dépend : la ligne qui la précède avec un retrait moindre.
Un libellé trop long tient sur deux lignes, de part et d'autre de celle de ses montants.

Une ligne du tableau est la fonction COMPTES_ETAT.EHB.<DONNES|RECUS>.<…>, formée de son libellé et de ceux des lignes
dont elle dépend, créée s'il le faut : les libellés changent d'un rapport à l'autre (« Dette garantie par l'État »,
puis « Dette garantie par l'État - Encours »), et la base garde ceux de chaque rapport. Le chiffre est le montant de la
ligne à la clôture de l'exercice du rapport (COMPTES_ETAT.ENGAGEMENTS_HORS_BILAN_DONNES ou _RECUS), dans l'unité que dit
le tableau (milliards d'euros dans le rapport sur 2016, millions ensuite). Le montant de la clôture précédente, que le
rapport dit souvent « retraité », est enregistré avec le traitement « retraite_exercice_suivant ». Chaque ligne est
contrôlée : son montant, moins celui de la clôture précédente, doit égaler sa variation, à une unité près (les trois
sont arrondis). Ce contrôle sépare aussi les trois nombres quand la page les colle, entre eux ou à la fin du libellé
(commun.montants_lies_pdf) ; les lignes où le rapport ne donne pas les trois nombres sont déclarées (SANS_VARIATION).
Une ligne dont le montant est remplacé par la marque d'un engagement éteint (« ext ») ou par un appel de note n'a pas
de chiffre. Une ligne qui ne se plie pas au contrôle, un tableau sans l'une de ses deux parties, sans unité ou dont
l'en-tête ne nomme pas l'exercice arrêtent l'import. Les sommes (une ligne et celles qui en dépendent) ne sont pas
refaites ici : le rapport de cohérence les fait, et rapproche le tableau des balances des comptes de l'État.

Les rapports sur 2021 et 2025 donnent ce tableau en image, que la base ne sait pas lire ; ceux sur 2013 et les années
d'avant ne le reproduisent pas, et la Cour ne publie pas à l'adresse des autres ceux sur 2012, 2014 et 2015. L'exercice
2021 n'est donc connu que retraité, par le rapport sur 2022, et l'exercice 2015 par celui sur 2016. L'emplacement d'un
chiffre est sa page, le rang de sa ligne dans la page et l'étendue des abscisses de son montant (commun.montant_pdf),
ou celle des trois nombres et son rang parmi eux quand la page les colle ;
sa période est l'exercice, sa version la date de modification du PDF.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_pdf,
                    montant_pdf, montants_lies_pdf, table_des_chiffres, texte_pdf)
from importer_lois_resultats import code_lolf

SOURCE = re.compile(r"ccomptes\.certification-([0-9]{4})")
RACINE = "COMPTES_ETAT.EHB"
PARTIES = {"DONNES": ("COMPTES_ETAT.ENGAGEMENTS_HORS_BILAN_DONNES", re.compile(r"engagements donnés", re.I)),
           "RECUS": ("COMPTES_ETAT.ENGAGEMENTS_HORS_BILAN_RECUS", re.compile(r"engagements re[cç]us", re.I))}
TRAITEMENT_RETRAITE = "retraite_exercice_suivant"
# Un nombre du tableau : chiffres groupés par trois, signe moins compris.
NOMBRE = re.compile(r"[-‑−]?[0-9]{1,3}(?: [0-9]{3})*")
FIN = re.compile(r"^(Source|Certification des comptes|\(a\)|n\.a\.|\*)")
# (exercice du rapport, partie, libellé) des lignes où le rapport ne donne pas ses trois nombres : la clôture
# précédente y est remplacée par un appel de note.
SANS_VARIATION = {(2019, "DONNES", "Engagement de reprise par l’État de la dette de SNCF Réseau")}


def entier(texte):
    return int(texte.replace(" ", "").replace("‑", "-").replace("−", "-"))


def unite_du_tableau(textes):
    """L'unité que disent les lignes d'en-tête : « (en Md€) », « exprimés en M€ »."""
    for t in textes:
        t = t.replace(" ", "")
        if "enMd€" in t:
            return "MD_EUR"
        if "enM€" in t:
            return "MIO_EUR"
    return None


# Les lignes qui entourent l'en-tête d'une partie et n'en sont pas : dates des colonnes, « retraité », unité.
ENTETE = re.compile(r"(3 ?1/12/[0-9]{4}.*|re ?traité|Variation|Note|exprimés en M ?€ ?\*? ?(retraité)?|\(en Md€\))")
# À la place du montant à la clôture : la marque d'un engagement éteint, ou l'appel d'une note qui dit pourquoi le
# rapport ne le chiffre pas.
SANS_MONTANT = {"ext", "(a)", "(b)"}


def parties_du_rapport(pages, exercice, lieu):
    """L'unité du tableau et ses deux parties : partie → [(page, rang, morceaux)]. L'en-tête d'une partie commence par
    son nom ; l'exercice est nommé sur sa ligne ou sur l'une des deux qui la précèdent."""
    trouvees, unite = {}, None
    for p, page in enumerate(pages, start=1):
        courante = None
        for rang, (_, morceaux) in enumerate(page, start=1):
            texte = texte_pdf(morceaux)
            entete = next((nom for nom, (_, motif) in PARTIES.items() if motif.match(texte)), None)
            voisines = [texte_pdf(m) for _, m in page[max(0, rang - 7):rang + 2]]
            if entete and entete not in trouvees and len(texte) < 80 \
                    and any(str(exercice) in v for v in voisines[-5:-1]):
                unite = unite_du_tableau(voisines) or unite
                courante = trouvees.setdefault(entete, [])
                continue
            if courante is None:
                continue
            if FIN.match(texte):
                courante = None
                continue
            if texte and not ENTETE.fullmatch(texte):
                courante.append((p, rang, morceaux))
    if set(trouvees) != set(PARTIES) or not all(trouvees.values()):
        sys.exit(f"{lieu} : tableau des engagements hors bilan introuvable ou sans l'une de ses deux parties")
    if unite is None:
        sys.exit(f"{lieu} : le tableau des engagements hors bilan ne dit pas son unité")
    return unite, trouvees


def seuil_des_montants(lignes):
    """L'abscisse où commencent les montants : un peu à gauche du premier morceau, sur une ligne, qui est un nombre de
    trois chiffres au moins et que suit un autre morceau de nombres ; None si la partie n'en a pas."""
    candidats = []
    for _, _, morceaux in lignes:
        nombres = [(x, " ".join(t.split())) for x, t in morceaux if re.fullmatch(r"[-0-9 \u2011\u2212]+", t.strip())]
        nombres = [(x, t) for x, t in nombres if t]
        if len(nombres) >= 2 and len(nombres[0][1]) > 2 and NOMBRE.fullmatch(nombres[0][1]):
            candidats.append(nombres[0][0])
    return min(candidats) - 12 if candidats else None


def appel_de_note(x, texte, seuil):
    """Vrai pour l'appel de note que certains rapports placent entre le libellé et les montants : un nombre d'un ou
    deux chiffres, à gauche de tous les montants."""
    return seuil - 25 <= x < seuil + 12 and re.fullmatch(r"[0-9]{1,2}", texte.strip()) is not None


def lignes_de_partie(lignes, seuil):
    """Les lignes d'une partie : (page, rang de la ligne des montants, abscisse du libellé, libellé, morceaux des
    montants). Un libellé sur deux lignes entoure celle de ses montants."""
    decoupees = []
    for p, rang, morceaux in lignes:
        morceaux = [(x, t) for x, t in morceaux if t.strip() and not appel_de_note(x, t, seuil)]
        gauche = [(x, t) for x, t in morceaux if x < seuil]
        droite = [(x, " ".join(t.split())) for x, t in morceaux if x >= seuil]
        if gauche or droite:
            decoupees.append((p, rang, gauche, droite))
    i, resultat = 0, []
    while i < len(decoupees):
        p, rang, gauche, droite = decoupees[i]
        if not gauche:
            return None, f"page {p}, ligne {rang} : des montants sans libellé"
        if not droite and i + 2 < len(decoupees) and not decoupees[i + 1][2] and decoupees[i + 2][2] \
                and not decoupees[i + 2][3]:
            libelle = texte_pdf(gauche) + " " + texte_pdf(decoupees[i + 2][2])
            resultat.append((decoupees[i + 1][0], decoupees[i + 1][1], gauche[0][0], libelle, decoupees[i + 1][3]))
            i += 3
            continue
        resultat.append((p, rang, gauche[0][0], texte_pdf(gauche), droite))
        i += 1
    return resultat, None


def lignes_du_fichier(fichier, fonctions):
    trouve = SOURCE.fullmatch(fichier["source_id"])
    if trouve is None or not fichier["chemin"].endswith(".pdf"):
        sys.exit(f"{fichier['id']} : la copie n'est pas le PDF d'un rapport de certification")
    exercice, lieu = int(trouve.group(1)), fichier["id"]
    pages = lire_pdf(BASE / fichier["chemin"])
    unite, parties = parties_du_rapport(pages, exercice, lieu)
    seuils = {partie: seuil_des_montants(lignes) for partie, lignes in parties.items()}
    for partie, lignes in parties.items():
        concept = PARTIES[partie][0]
        # Une partie dont aucun montant n'a trois chiffres prend le seuil de l'autre : les colonnes sont les mêmes.
        seuil = seuils[partie] or next((v for v in seuils.values() if v), None)
        if seuil is None:
            sys.exit(f"{lieu} : aucune ligne de montants dans le tableau des engagements hors bilan")
        tableau, erreur = lignes_de_partie(lignes, seuil)
        if erreur:
            sys.exit(f"{lieu}, {erreur}")
        pile = []  # [(abscisse, identifiant de la fonction)] des lignes dont dépend la ligne courante
        for p, rang, x, libelle, droite in tableau:
            morceaux = [(x_, t) for x_, t in pages[p - 1][rang - 1][1] if not appel_de_note(x_, t, seuil)]
            sans_montant = not droite or droite[0][1] in SANS_MONTANT or [t for _, t in droite] == ["0"]
            lies = None
            if not sans_montant:
                debut, fin = int(droite[0][0]), int(droite[-1][0]) + 200
                if (exercice, partie, libelle) in SANS_VARIATION:
                    if not NOMBRE.fullmatch(droite[0][1]):
                        sys.exit(f"{lieu}, page {p}, ligne {rang} : montant mal formé « {droite[0][1]} » ({libelle})")
                    lies = (entier(droite[0][1]), None, None)
                else:
                    lies = montants_lies_pdf(morceaux, debut, fin)
                    if lies is None:
                        # La page écrit parfois les premiers montants dans le morceau du libellé.
                        debut, lies = 0, montants_lies_pdf(morceaux, 0, fin)
                        colles = re.search(r"[-0-9 \u2011\u2212]*$", libelle).group(0)
                        if lies is None or not colles.strip():
                            sys.exit(f"{lieu}, page {p}, ligne {rang} : {libelle} : les montants "
                                     f"« {texte_pdf(droite)} » ne se lisent pas comme un montant, celui de la clôture "
                                     "précédente et leur variation")
                        libelle = libelle[:len(libelle) - len(colles)].strip()
            while pile and pile[-1][0] >= x - 0.9:
                pile.pop()
            parent = pile[-1][1] if pile else f"{RACINE}.{partie}"
            fonction = f"{parent}.{code_lolf(libelle)}"
            if fonction not in fonctions:
                fonctions[fonction] = {"id": fonction, "libelle": libelle, "norme_id": "COMPTES_ETAT",
                                       "parent_id": parent}
            pile.append((x, fonction))
            if lies is None:
                # Une ligne de titre (certaines portent un « 0 » dans la seule colonne de la variation), un engagement
                # éteint à la clôture ou que le rapport ne chiffre pas.
                continue
            # Un montant que la page écrit à part se désigne par l'étendue de ses abscisses ; un montant collé aux
            # autres, par l'étendue des trois et son rang.
            note = (f"Montant à la clôture de {exercice - 1} tel que le présente le rapport sur {exercice} "
                    "(« retraité » quand il a été corrigé depuis).")
            lus = []
            for k, (periode, traitement, note_) in enumerate(((str(exercice), "", ""),
                                                              (str(exercice - 1), TRAITEMENT_RETRAITE, note))):
                if lies[k] is None:
                    continue
                if debut and len(droite) > k and all(NOMBRE.fullmatch(t) and entier(t) == lies[i]
                                                     for i, (_, t) in enumerate(droite[:k + 1])):
                    fin_k = int(droite[k + 1][0]) if len(droite) > k + 1 else fin
                    lus.append((periode, traitement, f"x={int(droite[k][0])}-{fin_k}", lies[k], note_))
                else:
                    lus.append((periode, traitement, f"x={debut}-{fin};rang={k + 1}", lies[k], note_))
            for periode, traitement, etendue, valeur, note in lus:
                emplacement = f"page={p};ligne={rang};{etendue}"
                if ";rang=" in etendue:
                    relu = [str(v) for v in lies]
                    relu = (relu[int(etendue[-1]) - 1],)
                else:
                    x1, x2 = (int(v) for v in etendue[2:].split("-"))
                    relu = montant_pdf(morceaux, x1, x2)
                if relu is None or int(relu[0]) != valeur:
                    sys.exit(f"{lieu}, {emplacement} : le montant {valeur} ne se relit pas ({relu})")
                chiffre = {
                    "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement,
                    "zone": "FR", "perimetre_id": "ETAT_CGE", "concept_id": concept,
                    "fonction_id": fonction, "traitements": traitement, "unite_id": unite, "periode": periode,
                    "valeur": str(valeur), "decimales": 0, "statut": "definitif", "drapeau_source": "",
                    "version": fichier["mis_a_jour_source"][:10], "consolidation": "sans_objet",
                    "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(),
                    "notes": note,
                }
                chiffre["id"] = identifiant(chiffre)
                yield chiffre


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichier = next((f for f in lire("tables/fichiers.csv") if f["id"] == sys.argv[1]), None)
    if fichier is None:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    fonctions = {f["id"]: f for f in lire("tables/fonctions.csv")}
    for racine in (RACINE, f"{RACINE}.DONNES", f"{RACINE}.RECUS"):
        if racine not in fonctions:
            sys.exit(f"fonction {racine} absente de tables/fonctions.csv")
    avant = set(fonctions)
    nouveaux = list(lignes_du_fichier(fichier, fonctions))
    cible = table_des_chiffres(fichier["source_id"])
    existants = {l["id"]: l for l in lire(cible)}
    ajoutes, inchanges = fusionner(existants, nouveaux, fichier["id"])
    ecrire("tables/fonctions.csv", champs("fonctions"), fonctions.values())
    ecrire(cible, champs_chiffres(), existants.values())
    print(f"{fichier['id']} : {ajoutes} chiffres ajoutés, {inchanges} déjà enregistrés ; {cible} en compte "
          f"{len(existants)} ; {len(set(fonctions) - avant)} fonctions nouvelles")


if __name__ == "__main__":
    main()
