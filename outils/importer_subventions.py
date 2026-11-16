#!/usr/bin/env python3
"""Inscrit dans la base les subventions d'investissement que l'État accorde à chaque collectivité, projet par projet,
d'après la liste que publie la Direction générale des collectivités locales (DGCL) sur data.gouv.fr, à partir de la
copie archivée du fichier d'un exercice.

    python3 outils/importer_subventions.py <fichier_id>

Chaque fichier donne, pour un exercice depuis 2018, une ligne par subvention accordée à un projet d'investissement au
titre d'une dotation du programme 119 : dotation d'équipement des territoires ruraux (DETR), dotation de soutien à
l'investissement local (DSIL), dotation politique de la ville (DPV), dotation de soutien à l'investissement des
départements (DSID), et leurs enveloppes exceptionnelles de 2020 et 2021. Chaque ligne nomme le bénéficiaire (type,
Siren, département, nom, code Insee d'une commune), le projet, son coût hors taxe, la subvention et son taux, en euros.
Ce sont des engagements : l'exercice est celui de l'engagement budgétaire de la subvention, que l'État paie ensuite au
fil des travaux.

Ces copies sont les chiffres eux-mêmes : la base ne les recopie pas, elle les lit. L'import vérifie l'en-tête, que
chaque ligne a autant de champs que lui, est de l'exercice du fichier, et porte une dotation que décrit
tables/dispositifs_subventions.csv, avec son programme. Il compte, sans s'arrêter, ce que la source donne mal : une
subvention ou un coût illisible ou absent, un bénéficiaire qu'aucun code ne désigne (ni code Insee d'une commune, ni
numéro Siren de neuf chiffres), une subvention qui dépasse le coût du projet. Puis il inscrit la copie dans
tables/fichiers_subventions.csv, avec le nombre de ses projets, de leurs bénéficiaires et le total des subventions. La
version d'une copie est la date de dépôt du fichier sur data.gouv.fr.
"""

import csv
import decimal
import io
import re
import sys

from commun import BASE, champs, ecrire, lire, ouvrir_copie

SOURCE = "dgcl.subventions-investissement"
ENTETE = ["exercice", "dispositif", "programme", "beneficiaire_type", "beneficiaire_siren", "beneficiaire_dep",
          "beneficiaire_nom", "beneficiaire_code_insee", "intitule", "cout_ht", "subvention", "taux"]
COMMUNE = r"[0-9][0-9AB][0-9]{3}"  # code Insee d'une commune
SIREN = r"[0-9]{9}"
MONTANT = re.compile(r"-?[0-9]+(,[0-9]+)?")


def montant(texte):
    """Un montant en euros de la source (virgule décimale), en Decimal, ou None s'il est absent ou illisible."""
    texte = texte.strip()
    return decimal.Decimal(texte.replace(",", ".")) if MONTANT.fullmatch(texte) else None


def beneficiaire(ligne):
    """Le code qui désigne le bénéficiaire : le code Insee d'une commune, sinon son numéro Siren, sinon rien."""
    insee, siren = ligne["beneficiaire_code_insee"].strip(), ligne["beneficiaire_siren"].strip()
    if ligne["beneficiaire_type"] == "commune" and re.fullmatch(COMMUNE, insee):
        return insee
    return siren if re.fullmatch(SIREN, siren) else ""


def projets(fichier, referentiel=None):
    """(exercice, lignes) d'une copie : chaque ligne, un dictionnaire des champs de la source, avec `cle`, le code du
    bénéficiaire, et les montants lus (`cout`, `montant`, Decimal ou None)."""
    if fichier["source_id"] != SOURCE:
        sys.exit(f"{fichier['id']} : la source {fichier['source_id']} n'est pas lue par cet import")
    referentiel = referentiel or lire("tables/dispositifs_subventions.csv")
    programmes = {d["dispositif"]: d["programme"] for d in referentiel}
    with ouvrir_copie(BASE / fichier["chemin"]) as f:
        texte = f.read().decode("utf-8-sig")
    lecteur = csv.reader(io.StringIO(texte, newline=""), delimiter=";")
    entete = next(lecteur, None)
    if entete != ENTETE:
        sys.exit(f"{fichier['id']} : en-tête inattendu ({entete})")
    exercices, lignes = set(), []
    for n, champs_ in enumerate(lecteur, start=2):
        lieu = f"{fichier['id']}, ligne {n}"
        if len(champs_) != len(ENTETE):
            sys.exit(f"{lieu} : {len(champs_)} champs au lieu de {len(ENTETE)}")
        ligne = dict(zip(ENTETE, champs_))
        if not re.fullmatch(r"20[0-9]{2}", ligne["exercice"]):
            sys.exit(f"{lieu} : exercice illisible (« {ligne['exercice']} »)")
        exercices.add(ligne["exercice"])
        if ligne["dispositif"] not in programmes:
            sys.exit(f"{lieu} : dotation inconnue (« {ligne['dispositif']} »), à décrire dans "
                     "tables/dispositifs_subventions.csv")
        if ligne["programme"] != programmes[ligne["dispositif"]]:
            sys.exit(f"{lieu} : la {ligne['dispositif']} relève du programme {programmes[ligne['dispositif']]}, pas du "
                     f"programme {ligne['programme']}")
        ligne["cle"] = beneficiaire(ligne)
        ligne["cout"], ligne["montant"] = montant(ligne["cout_ht"]), montant(ligne["subvention"])
        lignes.append(ligne)
    if len(exercices) != 1:
        sys.exit(f"{fichier['id']} : {len(exercices)} exercices dans le fichier ({', '.join(sorted(exercices))})")
    return exercices.pop(), lignes


def inscription(fichier):
    """La ligne de tables/fichiers_subventions.csv d'une copie, après contrôle de tout son contenu."""
    version = fichier["mis_a_jour_source"][:10]
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", version):
        sys.exit(f"{fichier['id']} : la copie ne dit pas la date de son dépôt")
    exercice, lignes = projets(fichier)
    if not lignes:
        sys.exit(f"{fichier['id']} : aucun projet")
    illisibles = sum(l["montant"] is None or l["cout"] is None for l in lignes)
    depassements = sum(l["montant"] is not None and l["cout"] is not None and l["montant"] > l["cout"] for l in lignes)
    total = sum((l["montant"] for l in lignes if l["montant"] is not None), decimal.Decimal(0))
    return {"fichier_id": fichier["id"], "exercice": exercice, "version": version, "projets": str(len(lignes)),
            "beneficiaires": str(len({l["cle"] for l in lignes if l["cle"]})),
            "sans_beneficiaire": str(sum(not l["cle"] for l in lignes)), "montants_illisibles": str(illisibles),
            "depassements": str(depassements), "subventions": f"{total:.2f}"}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fichiers = {f["id"]: f for f in lire("tables/fichiers.csv")}
    if sys.argv[1] not in fichiers:
        sys.exit(f"copie archivée inconnue : {sys.argv[1]}")
    inscrits = [i for i in lire("tables/fichiers_subventions.csv") if i["fichier_id"] != sys.argv[1]]
    ligne = inscription(fichiers[sys.argv[1]])
    if any(i["exercice"] == ligne["exercice"] and i["version"] == ligne["version"] for i in inscrits):
        sys.exit(f"{sys.argv[1]} : une copie de {ligne['exercice']} de même version est déjà inscrite")
    ecrire("tables/fichiers_subventions.csv", champs("fichiers_subventions"), inscrits + [ligne], cle="fichier_id")
    print(f"{ligne['fichier_id']} : subventions de {ligne['exercice']} ({ligne['version']}), {ligne['projets']} "
          f"projets, {ligne['beneficiaires']} bénéficiaires, {ligne['subventions']} euros ; "
          f"{ligne['sans_beneficiaire']} projets "
          f"sans bénéficiaire désigné, {ligne['montants_illisibles']} montants illisibles, {ligne['depassements']} "
          "subventions supérieures au coût du projet")


if __name__ == "__main__":
    main()
