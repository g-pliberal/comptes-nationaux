#!/usr/bin/env python3
"""Enregistre dans la base les crédits qu'ouvre et qu'annule une loi de finances rectificative, ou de fin de gestion,
les évaluations de recettes qu'elle révise et les soldes qu'elle modifie, à partir de son texte définitif, tel que le
publie l'assemblée qui l'a adopté en dernier (page HTML archivée du Sénat ou de l'Assemblée nationale).

    python3 outils/importer_lois_rectificatives.py <fichier_id>

Tableaux lus : les états qui répartissent, par mission et par programme, les autorisations d'engagement et les crédits
de paiement que la loi ouvre (« supplémentaires ») et ceux qu'elle annule : budget général, budgets annexes, comptes
d'affectation spéciale et comptes de concours financiers. Jusqu'à la deuxième loi de 2009, un état donne les ouvertures
(B, C, D) et un autre les annulations (B', C', D') ; depuis, un même état donne les deux, en quatre colonnes. La lettre
d'un état ne dit pas toujours sa catégorie (l'état C est celui des comptes spéciaux quand la loi n'a pas d'état des
budgets annexes) : la catégorie d'un tableau est la dernière que nomment le titre de l'état et les intertitres qui le
précèdent (« I. – Comptes d'affectation spéciale »). Sous un programme, une ligne « dont titre 2 » (« dont charges de
personnel ») donne la part des crédits qui va aux dépenses de personnel. L'état A révisé donne ce que la loi change
aux évaluations de recettes, ligne par ligne, et le tableau de son article d'équilibre, en millions d'euros, ce qu'elle
change aux ressources, aux charges et aux soldes ; le tableau de financement, les plafonds de la dette et des emplois et
les autorisations de découvert ne sont pas lus.

Un état se reconnaît à son intitulé (« ÉTAT B (Article 7 de la loi) »). Ses tableaux sont ceux qui s'ouvrent entre son
intitulé et celui de l'état suivant, hors ceux qui portent l'intitulé d'un état ; un tableau que la page coupe en
plusieurs continue jusqu'à sa ligne de total. Chaque colonne doit être l'une des quatre que l'import connaît (COLONNES),
et l'unité, l'euro (une page qui ne l'annonce pas se déclare dans UNITE_TUE). Une mission égale la somme de ses
programmes, et la ligne de total celle des missions, dans chaque colonne ; une case vide, nulle ou « néant » vaut zéro
dans ces sommes, et ne donne pas de chiffre. Les missions sont les lignes en gras quand le tableau en marque, sinon elles
se reconnaissent à leurs montants, comme dans outils/importer_lois_finances.py ; une mission dont la page n'imprime pas
le montant vaut la somme de ses programmes. Jusqu'en 2009, chaque budget annexe ouvre sur une ligne à son nom, sans
montant, et se ferme sur une ligne « Totaux hors amortissement », qui donne son montant et doit égaler ses programmes.
Une ligne « dont » ne peut dépasser le programme qu'elle détaille.

Le total de chaque tableau doit égaler ce que les articles de la loi ouvrent ou annulent pour sa catégorie et son état
(« Il est annulé pour 2024, au titre du budget général, des autorisations d'engagement et des crédits de paiement
s'élevant respectivement aux montants de … € et de … €, conformément à la répartition par mission donnée à l'état B
annexé à la présente loi ») ; plusieurs articles qui renvoient au même état s'additionnent, et un article « au titre
des comptes spéciaux » couvre les deux catégories de comptes. Un article que l'import ne sait pas lire, un tableau dont
un total n'a pas d'article, ou un article sans tableau, arrête l'import ; « un crédit » (« des crédits ») est un
montant de crédits de paiement, avec autant d'autorisations d'engagement ou aucune, ce que le tableau doit dire. Une page
qui ne reproduit pas les articles de la loi, ou pas ses états, se déclare dans SANS_ARTICLES ou SANS_ETATS ; dans le
second cas, les totaux de chaque catégorie se lisent dans les articles, chacun dans la phrase qui l'énonce. Un état dont
les crédits s'ajoutent à ceux d'un autre état de la même catégorie, sur les mêmes missions (l'état B'' de 2009), donne
ses chiffres sous un traitement, déclaré dans TRAITEMENTS.

Les missions, les budgets annexes, les comptes spéciaux et leurs programmes sont les fonctions de la norme LOLF, sous
l'identifiant que leur donnent les imports des lois d'approbation des comptes et des lois de finances initiales ; un
libellé qu'un état écrit autrement que ces lois la même année se déclare dans LIBELLES. La période d'un chiffre est
l'année de la loi, sa version la date du texte ; les crédits ouverts et annulés sont des autorisations, sans statut de
prévision ou d'exécution, et les révisions, des évaluations.

L'état A révisé (« Voies et moyens pour 2024 révisés ») se lit comme celui d'une loi de finances initiale
(outils/importer_lois_finances.py), dans sa colonne « Révision des évaluations pour 2024 » : un tableau du budget
général par division et par ligne, la récapitulation de ses catégories et de ses divisions, puis les budgets annexes,
les comptes d'affectation spéciale et les comptes de concours financiers. La loi n'y donne que ce qu'elle révise : une
catégorie, une division, un budget annexe ou un compte qu'elle ne révise pas n'y figure pas, et compte pour zéro. Une
partie s'annonce par son intitulé, quel que soit son numéro, avant son premier tableau, dans ses premières lignes ou
dans une ligne du tableau précédent (PARTIES_A) ; un tableau qui n'annonce pas son unité garde celle du précédent. Chaque
division égale la somme de ses lignes, chaque catégorie de la récapitulation celle de ses divisions, que le tableau
détaillé doit donner aux mêmes montants, chaque total de la récapitulation celle des catégories qu'il compte, chaque
compte et chaque section la somme de leurs lignes, aux arrondis près, sauf un écart déclaré dans
importer_lois_finances.ECARTS_A. Un budget annexe s'ouvre sur son nom, avec ou sans montant, et se ferme sur son total
quand il n'a pas de montant ; jusqu'en 2008, une ligne « Total des recettes brutes en fonctionnement » (en capital) ferme
une section (SECTIONS_BA). Une ligne qui réunit le nom d'un compte et l'intitulé de sa section se lit comme ces deux
lignes, au même montant. Les recettes fiscales sont brutes jusqu'en 2022, nettes depuis, comme dans l'état A des lois de
finances initiales. Les divisions, les lignes, les comptes et les sections prennent les identifiants de l'import des lois
de finances initiales ; un libellé que l'état A écrit autrement que la loi de finances initiale de l'année, pour la même
division ou la même ligne, se déclare dans LIBELLES.

Le tableau de l'article d'équilibre suit la phrase « Pour 2024, l'ajustement des ressources tel qu'il résulte des
évaluations révisées figurant à l'état A … et la variation des charges du budget de l'État sont fixés aux montants
suivants » ; ses lignes sont celles des lois de finances initiales (EQUILIBRE). Il ne donne que des variations : une case
vide ou « néant » ne donne pas de montant, et compte pour zéro dans ses sommes, qui doivent tomber juste à l'arrondi au
million près de chacun de leurs montants. Ses ressources doivent égaler, au million près, celles que donne l'état A,
zéro pour ce qu'il ne révise pas ; ses charges, les crédits de paiement que la loi ouvre moins ceux qu'elle annule, dans
chaque catégorie et chaque budget annexe, nets des remboursements et dégrèvements de leur mission jusqu'en 2022, de ceux
d'impôts d'État depuis, sauf un écart déclaré dans ECARTS_CHARGES ; et chaque solde, celui que donnent les états. Ce que
l'état A donne à l'euro, ou que les états de crédits donnent déjà (VERIFIES_SEULEMENT), ne s'enregistre pas ; le reste
s'enregistre, en millions d'euros. Une page dont le tableau est une image se déclare dans EQUILIBRE_EN_IMAGE ; quand la
page ne reproduit pas l'état A (SANS_ETATS), le tableau en donne les recettes. Une case nulle ne donne pas de chiffre.
"""

import re
import sys

from commun import (BASE, aujourdhui, champs, champs_chiffres, ecrire, fusionner, identifiant, lire, lire_page_html,
                    lire_texte_html, nombre_de_phrase, nombre_texte, table_des_chiffres, texte_html)
import importer_lois_finances as lf
from importer_lois_finances import cle_titre, montant, nom
from importer_lois_resultats import code_lolf, colonnes, propre, unite_annoncee

# Catégories de crédits, telles que les nomment le titre d'un état, ses intertitres et les articles de la loi.
NOMS_CATEGORIES = {"BG": r"budget général", "BA": r"budgets? annexes?", "CAS": r"comptes? d’affectation spéciale",
                   "CCF": r"comptes? de concours financiers"}
# Intitulé d'une colonne → (autorisations d'engagement ou crédits de paiement, ouvertures ou annulations).
COLONNES = {r"Autorisations d’engagement supplémentaires (?:accordées|ouvertes)": ("AE", "OUVERTURES"),
            r"Crédits de paiement supplémentaires ouverts": ("CP", "OUVERTURES"),
            r"Autorisations d’engagement annulées": ("AE", "ANNULATIONS"),
            r"Crédits de paiement annulés": ("CP", "ANNULATIONS")}
ETAT = r"[ÉE][Tt][Aa][Tt]\s+([A-G])\s*(['’′″]{0,2})\s*\(\s*(?:[Aa]rticles?|ARTICLES?)\s+[0-9]"
DONT = r"dont (?:titre 2|charges de personnel)"
SOUS_TOTAL = r"totaux hors amortissements?"
# Caractères invisibles que certaines pages laissent dans le texte : marques de direction, espaces sans chasse, et
# symboles de mise en page d'une police de la zone d'usage privé d'Unicode.
INVISIBLES = re.compile(r"[​-‏‪-‮⁠-⁩﻿-]")
# Pages qui ne reproduisent pas tout le texte de la loi : source → ce qui manque, dit dans la note de chaque chiffre.
SANS_ARTICLES = {
    "an.ta15-0032": "Dans la page de l’Assemblée nationale, 245 760 octets nuls recouvrent les articles de la loi et son "
                    "état A : le total de l’état n’a pas pu être comparé à l’article qui ouvre et annule ces crédits.",
}
# États dont les crédits s'ajoutent à ceux d'un autre état de la même catégorie, sur les mêmes missions : (source,
# état) → traitement qui les distingue (table des traitements).
TRAITEMENTS = {("senat.tas08-076", "B''"): "lfr_2009_04_etat_b_seconde"}
# Libellés qu'un état écrit autrement que la loi de finances initiale et la loi d'approbation des comptes de la même
# année, pour la même mission ou le même programme : (source, libellé de la page) → libellé de ces lois. Le chiffre
# prend la fonction du second ; son emplacement garde le libellé de la page. Un libellé déclaré que la page ne porte
# pas arrête l'import.
LIBELLES = {
    ("senat.tas06-037", "Remboursements et dégrèvements d’impôts d’État (crédits évaluatifs)"):
        "Remboursements et dégrèvements d’impôts d’État",
    ("senat.tas06-037", "Remboursements et dégrèvements d’impôts locaux (crédits évaluatifs)"):
        "Remboursements et dégrèvements d’impôts locaux",
    ("senat.tas07-043", "Enseignement privé du premier et du second degré"):
        "Enseignement privé du premier et du second degrés",
    ("senat.tas08-037", "Sécurité et qualité sanitaire de l’alimentation"):
        "Sécurité et qualité sanitaires de l’alimentation",
    ("senat.tas08-076", "Prêt pour le développement économique et social"):
        "Prêts pour le développement économique et social",
    ("senat.tas08-076", "Concours spécifiques et administrations"): "Concours spécifiques et administration",
    ("senat.tas09-079", "Démonstrateurs et plateformes technologiques en énergies renouvelables et décarbonées et "
                        "chimie verte"):
        "Démonstrateurs et plates-formes technologiques en énergies renouvelables et décarbonées et chimie verte",
    ("senat.tas09-104", "Enseignement scolaire public du premier degrés"): "Enseignement scolaire public du premier degré",
    ("senat.tas09-104", "Recherche dans le domaine de l’énergie, du développement et de l’aménagement durables"):
        "Recherche dans les domaines de l’énergie, du développement et de l’aménagement durables",
    ("an.ta14-0268", "Versement de la France à la Grèce au titre de la restitution à cet État des revenus perçus par la "
                     "Banque de France sur les titres grecs"):
        "Versement de la France à la Grèce au titre de la restitution à cet État des revenus perçus par la Banque de "
        "France sur les titres grecs détenus en compte propre",
    ("an.ta14-0460", "Services nationaux de transport conventionnés"):
        "Services nationaux de transport conventionnés de voyageurs",
    ("an.ta14-0460", "Exploitation des services nationaux de transport conventionnés de voyageurs"):
        "Exploitation des services nationaux de transport conventionnés",
    ("an.ta15-0067", "Dotation du Mécanisme européen de stabilité"):
        "Dotation en capital du Mécanisme européen de stabilité",
    ("senat.tas20-025", "Avances remboursables de droits de mutation à titre onéreux destinées à soutenir les départements "
                        "et d’autres collectivités affectés par les conséquences économiques de l’épidémie de covid-19"):
        "Avances remboursables de droits de mutation à titre onéreux destinées à soutenir les départements et d’autres "
        "collectivités territoriales affectés par les conséquences économiques de l’épidémie de covid-19",
    ("senat.tas23-024", "Avances remboursables et prêts bonifiés aux entreprises touchées par la crise de la covid-19 ou "
                        "par le conflit en Ukraine"):
        "Avances remboursables et prêts bonifiés aux entreprises touchées par la crise de la Covid-19",
    # État A : divisions et lignes de recettes.
    ("senat.tas08-037", "Dotation régionale d’équipement scolaire (ligne nouvelle)"):
        "Dotation régionale d’équipement scolaire",
    ("senat.tas09-050", "Produits de cessions immobilières"): "Produits des cessions immobilières",
    ("senat.tas10-038", "17. Enregistrement, timbre, autres contributionset taxes indirectes"):
        "17. Enregistrement, timbre, autres contributions et taxes indirectes",
    ("an.ta14-0071", "Amendes forfaitaires de la police de la circulation et amendes forfaitaires majorées issues des "
                     "infractions constatées par la voie du système de contrôle-sanction automatisé et des infractions aux "
                     "règles de la police de circulation"):
        "Amendes forfaitaires de la police de la circulation et amendes forfaitaires majorées issues des infractions "
        "constatées par la voie du système de contrôle-sanction automatisé et des infractions aux règles de la police "
        "de la circulation",
    ("senat.tas11-138", "Retenue à la source et prélèvements sur les revenus de capitaux mobiliers et le prélèvement sur "
                        "les bons anonymes"):
        "Retenues à la source et prélèvements sur les revenus de capitaux mobiliers et le prélèvement sur les bons "
        "anonymes",
    ("an.ta14-0877", "PSR au titre de la compensation des pertes de recettes liées au relèvement du seuil "
                     "d’assujettissement des entreprises au versement transport"):
        "Prélèvement sur les recettes de l’État au titre de la compensation des pertes de recettes liées au relèvement "
        "du seuil d’assujettissement des entreprises au versement transport",
    ("senat.tas19-030", "Produits exceptionnels hors cession"): "Produits exceptionnels hors cession d’actif",
    ("senat.tas19-078", "Produit de cession des immobilisations affectées à la dette (article 61 de la loi de finances pour "
                        "2011)"):
        "Produit de cession des immobilisations affectées à la dette (art. 61 de la loi de finances pour 2011)",
    ("senat.tas22-028", "15. Taxe intérieure de consommation sur les produits énergétiques nette"):
        "15. Taxe intérieure de consommation sur les produits énergétiques",
    ("senat.tas22-028", "16. Taxe sur la valeur ajoutée nette"): "16. Taxe sur la valeur ajoutée",
}
LIBELLES_VUS = set()
# Pages qui n'annoncent pas l'unité d'un état : ses totaux égalent alors, à l'euro, les montants des articles.
UNITE_TUE = {"senat.tas20-136"}
SANS_ETATS = {
    "senat.tas08-001": "Le texte définitif ne reproduit pas les états de la loi : le montant est celui de l’article "
                       "qui ouvre ou annule ces crédits, pour toute la catégorie.",
}

# État A, les voies et moyens révisés : ses parties, chacune annoncée par son intitulé avant son premier tableau, dans
# les premières lignes de celui-ci ou dans une ligne du tableau qui précède ; leur numéro change d'une loi à l'autre.
PARTIES_A = (("RECAPITULATION", r"récapitulation des (?:révisions de )?recettes du budget général"),
             ("BG", r"(?<!recettes du )budget général"),
             ("BA", r"budgets annexes"),
             ("CAS", r"comptes d’affectation spéciale"),
             ("CCF", r"comptes de concours financiers"))
COLONNE_A = r"r[ée]vision des [ée]valuations pour"  # colonne des montants, suivie de l'année de la loi
# Jusqu'en 2008, une ligne « Total des recettes brutes en fonctionnement » (en capital) ferme une section d'un budget
# annexe ; la section prend le nom que lui donne la loi de finances initiale, quand la page ne l'imprime pas.
SECTIONS_BA = {"fonctionnement": "Section des opérations courantes", "capital": "Section des opérations en capital"}
TOTAL_BA = r"Total(?: des recettes)?"
# Concept de chaque catégorie de recettes du budget général, comme dans la loi de finances initiale ; les recettes
# fiscales sont brutes jusqu'en 2022, nettes des remboursements et dégrèvements depuis.
RECETTES_BG = {c: v.replace("_LFI", "_LFR") for c, v in lf.RECETTES_BG.items()}
NOMS_RECETTES_BG = {"1": "BG_RECETTES_FISCALES_{}", "2": "BG_RECETTES_NON_FISCALES", "3": "BG_PRELEVEMENTS_SUR_RECETTES",
                    "4": "BG_FONDS_DE_CONCOURS_RECETTES"}
PREMIERE_ANNEE_NETTES = 2023

# Article d'équilibre : la phrase qui annonce son tableau, et les libellés de ce tableau, ceux des lois de finances
# initiales (importer_lois_finances.EQUILIBRE) et quelques variantes. Le solde que certaines lois portent sur la ligne
# des montants nets y compris fonds de concours est celui du budget général, les fonds de concours s'équilibrant.
PHRASE_EQUILIBRE = (r"Pour {annee},? l’ajustement des ressources tel qu’il résulte des évaluations révisées figurant "
                    r"à l’état A")
EQUILIBRE = {bloc: dict(lignes) for bloc, lignes in lf.EQUILIBRE.items()}
EQUILIBRE["BG"].update({
    "Recettes totales nettes": ("BG_RECETTES_NETTES_HORS_FDC", None, None),
    "Montants nets pour le budget général, y compris fonds de concours": ("BG_RECETTES_NETTES", "BG_DEPENSES_NETTES",
                                                                         "SOLDE_BUDGET_GENERAL"),
    "Montants nets pour le budget général y compris fonds de concours": ("BG_RECETTES_NETTES", "BG_DEPENSES_NETTES",
                                                                        "SOLDE_BUDGET_GENERAL")})
EQUILIBRE["BA_FDC"]["Totaux pour les budgets annexes, y compris fond de concours"] = ("BA_RECETTES", "BA_CHARGES",
                                                                                     "SOLDE_BUDGETS_ANNEXES")
EQUILIBRE["CS"]["Comptes d’opération monétaires (solde)"] = (None, None, "OPERATIONS_MONETAIRES_SOLDE")
# Charges du tableau que donnent les états de la loi, crédits de paiement ouverts moins annulés : elles se vérifient
# contre eux, et ne s'enregistrent pas ; de même les charges des budgets annexes, fonds de concours compris.
VERIFIES_SEULEMENT = {"BG_CP", "BA_CP", "CAS_CP", "CCF_CP", "BA_CHARGES"}
# Ressources du tableau que donne l'état A, quand la page le reproduit.
RECETTES_ETAT_A = {"BG_RECETTES_FISCALES_BRUTES", "BG_RECETTES_FISCALES_NETTES", "BG_RECETTES_NON_FISCALES",
                   "BG_PRELEVEMENTS_SUR_RECETTES", "BG_FONDS_DE_CONCOURS_RECETTES", "BA_RECETTES_HORS_FDC",
                   "CAS_RECETTES", "CCF_RECETTES"}
# Écart déclaré entre les charges du tableau et les crédits que la loi ouvre et annule : (source, charges) → écart
# (tableau moins états), en euros. La note dit d'où il vient ; la portent les chiffres du tableau qu'il touche.
ECARTS_CHARGES = {("senat.tas09-050", "BG_CP"): -65_000_000, ("senat.tas09-050", "CCF_CP"): 65_000_000}
NOTES_EQUILIBRE = {
    "senat.tas09-050": ({"BG_DEPENSES_NETTES_HORS_FDC", "BG_DEPENSES_NETTES", "SOLDE_BUDGET_GENERAL", "CCF_SOLDE",
                         "SOLDE_COMPTES_SPECIAUX"},
                        "Le tableau compte aussi le décret d’avance n° 2009-1512 du 8 décembre 2009 (Journal officiel du "
                        "9 décembre), que ratifie l’article 11 de la loi : il ouvre 65 000 000 € au compte de concours "
                        "financiers « Avances à divers services de l’État ou organismes gérant des services publics » et "
                        "en annule autant au budget général. Les charges du budget général du tableau en ont 65 M€ de "
                        "moins que les états de la loi, celles des comptes de concours financiers 65 M€ de plus."),
}
# Pages dont le tableau de l'article d'équilibre est une image, que la base ne lit pas : source → image.
EQUILIBRE_EN_IMAGE = {"senat.tas10-161": "tas10-1611.gif"}


def normaliser(texte):
    """Le texte d'une page, une seule apostrophe, sans blancs autour d'elle ni devant une virgule, et sans
    caractères invisibles."""
    texte = INVISIBLES.sub("", texte).replace("'", "’")
    return re.sub(r"\s+", " ", re.sub(r"\s+,", ",", re.sub(r"\s*’\s*", "’", texte))).strip()


def lettre_etat(lettre, primes):
    """« B », « B' » ou « B'' », quelle que soit la façon dont la page écrit ses primes."""
    n = len(primes) + primes.count("″")
    return lettre + "'" * n


def cle_colonne(libelle):
    for motif, cle in COLONNES.items():
        if re.fullmatch(motif, libelle.replace("'", "’")):
            return cle
    return None


def entete(tableau):
    """Nombre de lignes d'en-tête d'un tableau de crédits : jusqu'à celle qui nomme ses colonnes d'autorisations
    d'engagement et de crédits de paiement ; None si le tableau n'en a pas."""
    for r, ligne in enumerate(tableau[:4]):
        cles = {cle_colonne(propre(x)) for x in ligne} - {None}
        if {"AE", "CP"} <= {c[0] for c in cles}:
            return r + 1
    return None


def categorie_nommee(texte):
    """La dernière catégorie de crédits que nomme un texte, ou None."""
    trouvees = [(m.start(), c) for c, motif in NOMS_CATEGORIES.items() for m in re.finditer(motif, cle_titre(texte))]
    return max(trouvees)[1] if trouvees else None


def unite_du_tableau(tableau, e, forme, avant, source_id):
    """L'unité des montants d'un tableau, qu'annoncent ses lignes d'en-tête, sa légende ou le texte qui le précède :
    l'euro, seule unité des états de crédits ; une page qui ne l'annonce pas se déclare dans UNITE_TUE."""
    textes = [x for l in tableau[:e] for x in l] + [forme["legende"]] + re.findall(r"\([^()]{0,30}\)", avant[-200:])
    annoncees = {unite_annoncee(x) for x in textes} - {None}
    if annoncees == {"en euros"}:
        return "EUR"
    if not annoncees and source_id in UNITE_TUE:
        return "EUR"
    sys.exit(f"tableau de crédits : unité annoncée inconnue ou absente ({', '.join(sorted(annoncees)) or 'aucune'})")


def montants_des_cases(tableau, entete_, noms, largeurs):
    """(ligne, colonne, nombre) de chaque montant sous l'en-tête ; une case à cheval sur deux colonnes nommées
    différemment arrête l'import (une colonne sans intitulé, que certaines pages ajoutent pour la mise en page, ne
    compte pas)."""
    for r in range(entete_, len(tableau)):
        for c, x in enumerate(tableau[r]):
            nombre = nombre_texte(x) if c > 0 else None
            if c > 0 and not nombre and re.search(r"[0-9]", x):
                sys.exit(f"tableau de crédits, ligne {r} : montant illisible (« {x} »)")
            if not nombre:
                continue
            couvertes = {noms.get(c + dc) for dc in range(largeurs.get((r, c), 1))} - {None}
            if len(couvertes) != 1:
                sys.exit(f"tableau de crédits, ligne {r} : case à cheval sur deux colonnes, ou hors colonne")
            yield r, c, nombre


def blocs_des_etats(grilles, formes, flux, source_id):
    """Les tableaux de crédits de chaque état, chacun avec sa lettre d'état, sa catégorie et ses lignes."""
    intitules = list(re.finditer(ETAT, flux))
    resultat = []
    for n, m in enumerate(intitules):
        etat = lettre_etat(m.group(1), m.group(2))
        fin = intitules[n + 1].start() if n + 1 < len(intitules) else len(flux)
        tableaux = [int(k) for k in re.findall(r"⟦([0-9]+)⟧", flux[m.start():fin])]
        tableaux = [k for k in tableaux if not re.search(ETAT, " ".join(x for l in grilles[k] for x in l))]
        if not any(entete(grilles[k]) for k in tableaux):
            continue  # état sans tableau de crédits : recettes, autorisations de découvert
        ouvert, debut = None, m.start()  # debut : où commence le texte qui précède le prochain tableau
        for k in tableaux:
            t, forme = grilles[k], formes[k]
            e = entete(t)
            if e is None and ouvert is None:
                continue
            if e is not None:
                noms = {c: x for c, x in colonnes(t, e, forme["largeurs"]).items()
                        if categorie_nommee(x) is None or cle_colonne(x)}  # un intertitre n'est pas une colonne
                cles = {c: cle_colonne(x) for c, x in noms.items()}
                inconnues = sorted({x for c, x in noms.items() if cles[c] is None})
                if inconnues:
                    sys.exit(f"état {etat}, tableau {k} : colonne(s) inconnue(s) ({' ; '.join(inconnues)})")
                if ouvert is None:
                    avant = flux[debut:flux.index(f"⟦{k}⟧", debut)]
                    # L'intertitre qui nomme la catégorie précède le tableau, ou en ouvre la première ligne.
                    categorie = categorie_nommee(avant + " " + " ".join(x for l in t[:e] for x in l
                                                                        if not cle_colonne(propre(x))))
                    if categorie is None:
                        sys.exit(f"état {etat}, tableau {k} : catégorie de crédits introuvable")
                    ouvert = {"etat": etat, "categorie": categorie, "lignes": [], "noms": noms, "cles": cles,
                              "unite": unite_du_tableau(t, e, forme, avant, source_id), "total": None, "gras": set()}
                elif set(cles.values()) != set(ouvert["cles"].values()):
                    sys.exit(f"état {etat}, tableau {k} : colonnes autres que celles du tableau qu'il continue")
            else:
                e, noms, cles = 0, ouvert["noms"], ouvert["cles"]
                if max(len(l) for l in t) != max(noms) + 1:
                    sys.exit(f"état {etat}, tableau {k} : {max(len(l) for l in t)} colonnes, quand le tableau qu'il "
                             f"continue en a {max(noms) + 1}")
            textes_entete = {propre(x) for l in t[:e] for x in l if propre(x)} | set(noms.values())
            ouvert["gras"] |= {(k, r) for r, c in forme["gras"] if c == 0}
            par_ligne = {}
            for r, c, nombre in montants_des_cases(t, e, noms, forme["largeurs"]):
                par_ligne.setdefault(r, {})[cles[c]] = (c, nombre)
            for r in range(e, len(t)):
                libelle = propre(t[r][0])
                cases = {}
                for c, x in enumerate(t[r]):
                    if c in cles and not cases.get(cles[c], "").strip():
                        cases[cles[c]] = x  # une case fusionnée sur deux colonnes laisse vide la seconde
                valeurs = {cle: montant(x) for cle, x in cases.items()}
                vide = all(v is None for v in valeurs.values())
                if ouvert is None:
                    if libelle or not vide:
                        sys.exit(f"état {etat}, tableau {k}, ligne {r} : ligne après le total (« {libelle} »)")
                    continue
                if not libelle and vide:
                    continue
                if "(ligne supprimée)" in libelle:
                    if any(valeurs.values()):
                        sys.exit(f"état {etat}, tableau {k}, ligne {r} : ligne supprimée qui porte des crédits")
                    continue
                if vide and {propre(x) for x in t[r] if propre(x)} <= textes_entete:
                    continue  # en-tête répété
                if not libelle:
                    sys.exit(f"état {etat}, tableau {k}, ligne {r} : montants sans libellé")
                genre = "total" if re.fullmatch(r"(?i)totaux?|total", libelle) else \
                    "sous_total" if re.fullmatch(rf"(?i){SOUS_TOTAL}", libelle) else \
                    "dont" if re.fullmatch(rf"(?i){DONT}", libelle) else None
                if genre is None and re.match(r"(?i)(dont|totaux?|sous-total)\b", libelle):
                    sys.exit(f"état {etat}, tableau {k}, ligne {r} : ligne « {libelle} » inconnue")
                if genre == "dont" and vide:
                    continue  # une ligne « dont » sans montant : le programme ne touche pas aux dépenses de personnel
                if genre in ("total", "sous_total") and vide:
                    sys.exit(f"état {etat}, tableau {k}, ligne {r} : total sans montant")
                ligne = {"tableau": k, "ligne": r, "libelle": libelle, "nom": nom(libelle), "genre": genre,
                         "valeurs": {cle: v or 0 for cle, v in valeurs.items()}, "cases": par_ligne.get(r, {}),
                         "noms": noms, "vide": vide}
                ouvert["lignes"].append(ligne)
                if genre == "total":
                    ouvert["total"] = ligne
                    resultat.append(ouvert)
                    ouvert = None
            debut = flux.index(f"⟦/{k}⟧", debut) if f"⟦/{k}⟧" in flux[debut:] else debut
        if ouvert is not None:
            sys.exit(f"état {etat} : tableau sans ligne de total")
    return resultat


def egal(a, b):
    return all(abs(a.get(c, 0) - b.get(c, 0)) < 0.5 for c in set(a) | set(b))


def somme(lignes):
    total = {}
    for l in lignes:
        for c, v in l["valeurs"].items():
            total[c] = total.get(c, 0) + v
    return total


def nulle(ligne):
    return not any(ligne["valeurs"].values())


def montant_mission(mission, programmes):
    """Le montant d'une mission : celui de sa ligne, ou, quand la page ne l'imprime pas, celui de ses programmes."""
    return somme(programmes) if mission["vide"] else mission["valeurs"]


def par_marque(ordinaires, marquees):
    """[(mission, programmes)] si les lignes marquées (en gras, ou au contraire non en gras) sont les missions : la
    première ligne en est une, et chacune égale la somme des lignes qui la suivent jusqu'à la suivante, sauf si la page
    n'imprime pas son montant ; None sinon."""
    if not ordinaires or (ordinaires[0]["tableau"], ordinaires[0]["ligne"]) not in marquees:
        return None
    missions = []
    for l in ordinaires:
        if (l["tableau"], l["ligne"]) in marquees:
            missions.append((l, []))
        else:
            missions[-1][1].append(l)
    return missions if all(programmes and (m["vide"] or egal(somme(programmes), m["valeurs"]))
                           for m, programmes in missions) else None


def par_sommes(quoi, ordinaires, missions_connues):
    """[(mission, programmes)] d'après les seuls montants : une mission se ferme dès que ses programmes font son
    montant dans chaque colonne ; une ligne nulle qui suit est un programme de plus, sauf si c'est une mission connue
    de la base."""
    missions, i = [], 0
    while i < len(ordinaires):
        mission, programmes = ordinaires[i], []
        if mission["vide"]:
            sys.exit(f"{quoi} : la ligne « {mission['libelle']} », sans montant, ouvre une mission que rien ne marque")
        i += 1
        while not (programmes and egal(somme(programmes), mission["valeurs"])):
            if i == len(ordinaires):
                sys.exit(f"{quoi} : les programmes de la mission « {mission['libelle']} » ne font pas son montant")
            programmes.append(ordinaires[i])
            i += 1
        while i < len(ordinaires) and nulle(ordinaires[i]) and \
                f"LOLF.{code_lolf(ordinaires[i]['nom'])}" not in missions_connues:
            programmes.append(ordinaires[i])
            i += 1
        missions.append((mission, programmes))
    return missions


def par_sous_totaux(quoi, lignes):
    """[(mission, programmes, sous-total)] d'un état des budgets annexes jusqu'en 2009 : chaque budget annexe ouvre
    sur une ligne à son nom, sans montant, et se ferme sur sa ligne « Totaux hors amortissement », qui donne son
    montant et doit égaler la somme de ses programmes."""
    missions, courant = [], []
    for l in lignes:
        if l["genre"] is None:
            courant.append(l)
        elif l["genre"] == "sous_total":
            if len(courant) < 2 or not egal(somme(courant[1:]), l["valeurs"]) or \
                    not (courant[0]["vide"] or egal(courant[0]["valeurs"], l["valeurs"])):
                sys.exit(f"{quoi} : la ligne « {l['libelle']} » n'égale pas la somme des programmes qui la précèdent")
            missions.append((courant[0], courant[1:], l))
            courant = []
    if courant:
        sys.exit(f"{quoi} : des lignes après le dernier sous-total (« {courant[0]['libelle']} »)")
    return missions


def structure(bloc, missions_connues):
    """Rattache chaque ligne d'un tableau à sa mission : {(tableau, ligne) : (libellé, mission ou "")} ; vérifie les
    sommes. Les missions sont les lignes en gras, ou les autres, quand le tableau en marque ; sinon, elles se déduisent
    des montants (par_sommes)."""
    quoi = f"état {bloc['etat']}, {bloc['categorie']}"
    ordinaires = [l for l in bloc["lignes"] if l["genre"] is None]
    total = bloc["total"]["valeurs"]
    cles = {(l["tableau"], l["ligne"]) for l in ordinaires}
    gras = cles & bloc["gras"]
    rattache = {}
    if any(l["genre"] == "sous_total" for l in bloc["lignes"]):
        missions = []
        for mission, programmes, sous_total in par_sous_totaux(quoi, bloc["lignes"]):
            missions.append((mission, programmes))
            rattache[(sous_total["tableau"], sous_total["ligne"])] = (mission["nom"], "")
    else:
        missions = None
        if gras:
            for marquees in (gras, cles - gras):
                missions = par_marque(ordinaires, marquees)
                if missions and egal(somme([{"valeurs": montant_mission(m, p)} for m, p in missions]), total):
                    break
                missions = None
        if missions is None:
            if any(l["vide"] and not nulle(l) for l in ordinaires):
                sys.exit(f"{quoi} : ligne sans montant")
            if egal(somme(ordinaires), total):  # des missions seules
                if gras and gras != cles:
                    sys.exit(f"{quoi} : des missions seules, dont certaines seulement en gras")
                missions = [(l, []) for l in ordinaires]
            elif egal({c: v / 2 for c, v in somme(ordinaires).items()}, total):
                missions = par_sommes(quoi, ordinaires, missions_connues)
            else:
                sys.exit(f"{quoi} : ses lignes ne font ni son total ni deux fois son total")
    if not egal(somme([{"valeurs": montant_mission(m, p)} for m, p in missions]), total):
        sys.exit(f"{quoi} : la somme des missions ne fait pas le total")
    for mission, programmes in missions:
        for p in programmes:
            if nulle(p) and f"LOLF.{code_lolf(p['nom'])}" in missions_connues and \
                    code_lolf(p["nom"]) != code_lolf(mission["nom"]):
                sys.exit(f"{quoi} : la ligne nulle « {p['libelle']} », une mission connue, se range parmi les "
                         f"programmes de la mission « {mission['libelle']} »")
    for mission, programmes in missions:
        rattache[(mission["tableau"], mission["ligne"])] = (mission["nom"], "")
        for p in programmes:
            rattache[(p["tableau"], p["ligne"])] = (p["nom"], mission["nom"])
    # Une ligne « dont » appartient au programme qui la précède, et ne peut dépasser aucun de ses montants.
    precedent, lignes = None, {(l["tableau"], l["ligne"]): l for l in bloc["lignes"]}
    for l in bloc["lignes"]:
        if l["genre"] == "dont":
            if precedent is None or not rattache[precedent][1]:
                sys.exit(f"{quoi} : ligne « {l['libelle']} » hors programme (tableau {l['tableau']}, ligne {l['ligne']})")
            rattache[(l["tableau"], l["ligne"])] = rattache[precedent]
            programme = lignes[precedent]["valeurs"]
            if any(v > programme.get(c, 0) + 0.5 for c, v in l["valeurs"].items()):
                sys.exit(f"{quoi} : la ligne « {l['libelle']} » dépasse le programme « {lignes[precedent]['libelle']} » "
                         f"qu'elle détaille (tableau {l['tableau']}, ligne {l['ligne']})")
        elif l["genre"] is None:
            precedent = (l["tableau"], l["ligne"])
    return rattache


MONTANT = r"([0-9]{1,3}(?:[   ][0-9]{3})*) ?€"


def lire_montant(texte):
    return float(re.sub(r"\D", "", texte))


def articles(texte, annee):
    """[(état, catégories, sens, {colonne : montant}, phrase)] : ce qu'ouvre ou annule chaque article de la loi qui
    renvoie à un état. La phrase va de « Il est ouvert » (« Sont ouverts », « Il est annulé »…) à l'état ; une
    autorisation de découvert n'est pas un crédit."""
    lus = []
    for m in re.finditer(r"(?:Il est|Sont) (ouverts et annulés|ouvert|ouverts|ouvertes|annulé|annulés|annulées)\b", texte):
        fin = re.search(r"l’état ([A-G])((?:’|′|″){0,2}) ?annexé", texte[m.end():m.end() + 700])
        if fin is None:
            continue  # un article qui ne renvoie pas à un état : ouverture d'un compte, ratification d'un décret
        phrase = texte[m.start():m.end() + fin.end()]
        if re.search(r"(?:Il est|Sont) (?:ouvert|annul)", phrase[2:]):
            sys.exit(f"deux articles avant l'état qu'ils annoncent : « {phrase} »")
        if "découvert" in phrase:
            continue
        sens = {"OUVERTURES", "ANNULATIONS"} if "et annulés" in m.group(1) else \
            {"OUVERTURES"} if m.group(1).startswith("ouvert") else {"ANNULATIONS"}
        annees = set(re.findall(r"pour ([0-9]{4})", phrase))
        if annees - {annee}:  # un article peut taire l'année, que dit celui qui le précède
            sys.exit(f"article pour {', '.join(sorted(annees)) or 'aucune année'} dans une loi pour {annee} : « {phrase} »")
        titre = re.search(r"\b(?:au titre (?:des missions )?(?:du|des)|au) (budget général|budgets annexes|budget "
                          r"annexe «|comptes d’affectation spéciale|compte d’affectation spéciale «|comptes de concours "
                          r"financiers|compte de concours financiers «|comptes spéciaux)", phrase)
        if titre is None:
            sys.exit(f"article sans catégorie de crédits connue : « {phrase} »")
        categories = ("CAS", "CCF") if titre.group(1) == "comptes spéciaux" else \
            tuple(c for c, motif in NOMS_CATEGORIES.items() if re.search(motif, titre.group(1)))
        nombres = [lire_montant(x) for x in re.findall(MONTANT, phrase)]
        deux = re.search(r"des autorisations d’engagement et des crédits de paiement|une autorisation d’engagement et un "
                         r"crédit de paiement", phrase)
        separes = re.search(rf"des autorisations d’engagement (?:supplémentaires )?s’élevant à {MONTANT} et des crédits "
                            rf"de paiement (?:supplémentaires )?s’élevant à {MONTANT}", phrase)
        if deux and len(nombres) == 2 and "respectivement" in phrase:
            montants_ = {"AE": nombres[0], "CP": nombres[1]}
        elif deux and len(nombres) == 1:
            montants_ = {"AE": nombres[0], "CP": nombres[0]}
        elif separes and len(nombres) == 2:
            montants_ = {"AE": nombres[0], "CP": nombres[1]}
        elif re.search(r"(?:des autorisations|une autorisation) d’engagement", phrase) and \
                "crédit" not in re.split(r"autorisations? d’engagement", phrase, maxsplit=1)[1] and len(nombres) == 1:
            montants_ = {"AE": nombres[0]}
        elif re.search(r"\bdes crédits de paiement\b", phrase) and "autorisation" not in phrase and len(nombres) == 1:
            montants_ = {"CP": nombres[0]}
        elif re.search(r"\b(?:un crédit|des crédits) (?:supplémentaires? )?(?:de|s’élevant)", phrase) and \
                "autorisation" not in phrase and len(nombres) == 1:
            montants_ = {"CP": nombres[0], "un crédit": True}
        else:
            sys.exit(f"article illisible : « {phrase} »")
        lus.append((lettre_etat(fin.group(1), fin.group(2)), categories, sens, montants_, phrase))
    return lus


def verifier_articles(blocs, lus, source_id):
    """Le total de chaque tableau contre ce qu'ouvrent et annulent les articles qui renvoient à son état. Un article
    qui n'ouvre que des autorisations d'engagement laisse nuls les crédits de paiement, et inversement ; « un crédit »
    est un montant de crédits de paiement, avec autant d'autorisations d'engagement ou aucune."""
    attendus, libres = {}, set()  # (état, catégories) → {(colonne, sens) : montant} ; colonnes que l'article ne fixe pas
    for etat, categories, sens, montants_, phrase in lus:
        cible = attendus.setdefault((etat, categories), {})
        for s in sens:
            for colonne in ("AE", "CP"):
                if colonne in montants_:
                    cible[(colonne, s)] = cible.get((colonne, s), 0) + montants_[colonne]
                elif montants_.get("un crédit"):
                    libres.add((etat, categories, colonne, s))
                    cible.setdefault((colonne, s), 0)
                else:
                    cible.setdefault((colonne, s), 0)
    vus = set()
    for (etat, categories), montants_ in attendus.items():
        concernes = [b for b in blocs if b["etat"] == etat and b["categorie"] in categories]
        if not concernes:
            sys.exit(f"{source_id} : un article renvoie à l'état {etat} ({'+'.join(categories)}), qui n'a pas de tableau "
                     f"de ces crédits")
        for b in concernes:
            vus.add(id(b))
        for (colonne, s), attendu in montants_.items():
            lu = sum(b["total"]["valeurs"].get((colonne, s), 0) for b in concernes)
            if (etat, categories, colonne, s) in libres:
                cp = sum(b["total"]["valeurs"].get(("CP", s), 0) for b in concernes)
                if min(abs(lu), abs(lu - cp)) >= 0.5:
                    sys.exit(f"{source_id} : « un crédit » de l'état {etat} ({'+'.join(categories)}), avec {lu:,.0f} € "
                             f"d'autorisations d'engagement {s.lower()} dans l'état, ni zéro ni {cp:,.0f} €")
            elif abs(lu - attendu) >= 0.5:
                sys.exit(f"{source_id} : état {etat} ({'+'.join(categories)}), {colonne} {s.lower()} : {lu:,.0f} € dans "
                         f"l'état, {attendu:,.0f} € dans les articles")
    for b in blocs:
        if id(b) not in vus and any(b["total"]["valeurs"].values()):
            sys.exit(f"{source_id} : état {b['etat']}, {b['categorie']} : aucun article n'ouvre ni n'annule ces crédits")


def concept(categorie, colonne, sens, dont):
    return f"LOLF.{categorie}_{colonne}_LFR_{sens}" + ("_TITRE_2" if dont else "")


def chiffre(fichier, annee, concept_, fonction, unite_, nombre, emplacement, note="", traitement=""):
    ligne = {
        "source_id": fichier["source_id"], "fichier_id": fichier["id"], "emplacement": emplacement,
        "zone": "FR", "perimetre_id": "ETAT_LF", "concept_id": concept_, "fonction_id": fonction,
        "traitements": traitement,
        "unite_id": unite_, "periode": annee, "valeur": nombre[0], "decimales": nombre[1], "statut": "non_precise",
        "drapeau_source": "", "version": fichier["mis_a_jour_source"][:10], "consolidation": "non_consolide",
        "denominateur_id": "", "nature": "publie", "calcul_id": "", "saisi_le": aujourdhui(), "notes": note,
    }
    ligne["id"] = identifiant(ligne)
    return ligne


def partie_annoncee(texte, seule=False):
    """La partie de l'état A (PARTIES_A) que nomme un texte, la dernière qu'il nomme, ou None ; `seule` : le texte
    n'est que l'intitulé de la partie, précédé ou non de son numéro (« II. – Budgets annexes »)."""
    texte = normaliser(texte)
    if seule:
        return next((nom_ for nom_, motif in PARTIES_A
                     if re.fullmatch(rf"(?:[IVX]+\s*\.\s*[-–]\s*)?{motif}", texte, re.I)), None)
    trouvees = [(m.start(), nom_) for nom_, motif in PARTIES_A for m in re.finditer(motif, texte, re.I)]
    return max(trouvees)[1] if trouvees else None


def tableaux_etat_a(grilles, flux, annee, source_id):
    """{partie : [rangée]} : les rangées des tableaux de chaque partie de l'état A révisé, dans l'ordre, comme les lit
    importer_lois_finances.tableaux_etat_a, dans la colonne de la révision des évaluations pour l'année de la loi. Un
    tableau qui n'annonce pas son unité garde celle du tableau précédent. Une rangée sans numéro ni montant qui n'est
    que l'intitulé d'une partie ouvre cette partie ; une ligne « (ligne supprimée) », sans montant, n'est pas une
    rangée."""
    intitules = list(re.finditer(ETAT, flux))
    a = [n for n, m in enumerate(intitules) if m.group(1) == "A" and not m.group(2)]
    if len(a) != 1:
        sys.exit(f"{len(a)} états A")
    debut = intitules[a[0]].start()
    fin = intitules[a[0] + 1].start() if a[0] + 1 < len(intitules) else len(flux)
    if not re.search(rf"(?i)voies et moyens pour {annee} révisés", normaliser(flux[debut:debut + 400])):
        sys.exit(f"l'état A n'est pas celui des voies et moyens pour {annee} révisés")
    parties, partie, unite_, avant = {}, None, None, debut
    for m in re.finditer(r"⟦([0-9]+)⟧", flux[debut:fin]):
        k, p = int(m.group(1)), debut + m.start()
        tableau = grilles[k]
        if re.search(ETAT, " ".join(x for l in tableau for x in l)):
            continue  # intitulé de l'état suivant, mis dans un tableau
        entre, avant = flux[avant:p], flux.index(f"⟦/{k}⟧", p)
        partie, unite_ = partie_annoncee(entre) or partie, lf.unite_a(entre) or unite_
        e = lf.entete_a(tableau, annee, COLONNE_A)
        if e is None:
            textes = [propre(x) for l in tableau for x in l if propre(x)]
            if textes and all(re.fullmatch(lf.UNITE_A, x.replace("'", "’"), re.I) for x in textes):
                unite_ = lf.unite_a(" ".join(textes))  # tableau qui ne porte que l'unité des suivants
                continue
            sys.exit(f"état A, tableau {k} : ni en-tête ni unité")
        tete = " ".join(x for l in tableau[:e[0]] for x in l)
        partie, unite_ = partie_annoncee(tete) or partie, lf.unite_a(tete) or unite_
        if partie is None or unite_ is None:
            sys.exit(f"état A, tableau {k} : {'partie' if partie is None else 'unité'} inconnue")
        for g in lf.rangees_a(tableau, k, e, unite_, source_id, COLONNE_A):
            g["libelle"] = re.sub(r"\s*’\s*", "’", g["libelle"])  # « de l’ État »
            if not g["numero"] and g["valeur"] is None and (titre := partie_annoncee(g["libelle"], seule=True)):
                partie = titre
            elif "(ligne supprimée)" in g["libelle"]:
                if g["valeur"] is not None:
                    sys.exit(f"état A, {lf.ou(g)} : ligne supprimée qui porte un montant")
            else:
                parties.setdefault(partie, []).append(g)
    return parties


def budgets_annexes(rangees, connus):
    """Chaque budget annexe de l'état A révisé : {nom, rangee, total, lignes, sections : [{nom, lignes, total}]}, et le
    total de la partie (une rangée, ou None). Un budget annexe s'annonce par son nom, que `connus` (identifiants) doit
    contenir, avec ou sans son montant, ses lignes par leur numéro. Une ligne « Total des recettes » (« Total ») est le
    total du budget annexe qu'elle suit s'il n'a pas de montant, sinon celui de la partie, qui la ferme ; jusqu'en
    2008, une ligne « Total des recettes brutes en fonctionnement » (en capital) ferme une section (SECTIONS_BA). Une
    ligne « Fonds de concours » sans montant ne compte pas. Chaque section, chaque budget annexe et la partie égalent
    la somme de leurs lignes."""
    budgets, budget, total = [], None, None
    for g in rangees:
        libelle, numero = g["libelle"], g["numero"]
        if not libelle and not numero:
            continue
        if total is not None:
            sys.exit(f"état A, {lf.ou(g)} : « {numero} {libelle} » après le total des budgets annexes")
        if not numero and f"LOLF.{code_lolf(libelle)}" in connus:
            budget = {"nom": libelle, "rangee": g, "total": g if g["valeur"] is not None else None, "lignes": [],
                      "sections": [], "ouvertes": [], "ferme": False}
            budgets.append(budget)
        elif not numero and re.fullmatch(lf.FONDS_DE_CONCOURS_A, libelle) and g["valeur"] is None:
            continue
        elif budget is None or (budget["ferme"] and not re.fullmatch(TOTAL_BA, libelle)):
            sys.exit(f"état A, {lf.ou(g)} : « {numero} {libelle} » hors d'un budget annexe")
        elif numero:
            budget["ouvertes"].append(g)
        elif s := re.fullmatch(r"Total des recettes brutes en (fonctionnement|capital)", libelle):
            budget["sections"].append({"nom": SECTIONS_BA[s.group(1)], "lignes": budget["ouvertes"], "total": g})
            budget["ouvertes"] = []
        elif re.fullmatch(TOTAL_BA, libelle):
            if budget["total"] is None:
                budget["total"], budget["ferme"] = g, True
            else:
                total = g
        else:
            sys.exit(f"état A, {lf.ou(g)} : ligne « {numero} {libelle} » d'un budget annexe inconnue")
    parties = []
    for b in budgets:
        b["lignes"] = b.pop("ouvertes")
        for s in b["sections"]:
            lf.verifier_somme(s["total"], s["lignes"], "la section", f"{b['nom']} : {s['nom']}")
        morceaux = [s["total"] for s in b["sections"]] + b["lignes"]
        if b["total"] is not None:
            lf.verifier_somme(b["total"], morceaux, "le budget annexe", b["nom"])
        parties += morceaux
    if total is not None:
        lf.verifier_somme(total, parties, "le total des budgets annexes")
    return budgets, total


def valeur(g):
    """La valeur d'une rangée, en euros, 0 pour une case vide."""
    return g["valeur"] if g and g["valeur"] is not None else 0


def recettes_revisees(parties, sorte, connus):
    """Les montants de l'état A révisé à enregistrer, [(concept, fonction, libellé de la fonction, parent, rangée)], et
    ce qu'ils donnent pour le tableau de l'article d'équilibre, {(concept sans suffixe, fonction) : euros} ; une
    catégorie, un budget annexe ou une catégorie de comptes que l'état A ne révise pas y vaut zéro. `connus` :
    identifiants des missions, budgets annexes et comptes spéciaux. Les identifiants des divisions, des lignes, des
    sections et des comptes sont ceux de l'import des lois de finances initiales."""
    if "BG" not in parties or "RECAPITULATION" not in parties:
        sys.exit("état A sans tableau du budget général ou sans récapitulation")
    divisions, fonds = lf.budget_general_a(parties["BG"])
    if divisions is None:
        sys.exit("état A : tableau du budget général incomplet")
    categories, totaux = lf.recapitulation_a(parties["RECAPITULATION"], complete=False)
    nettes = any(n == "18" for c in categories.values() for n, _, _ in c["divisions"])
    if nettes and sorte != "NETTES":
        sys.exit("état A : division 18 des remboursements et dégrèvements avant 2023")
    recap = {n: g["valeur"] for c in categories.values() for n, _, g in c["divisions"]}
    if recap != {d["numero"]: d["rangee"]["valeur"] for d in divisions}:
        sys.exit("état A : les divisions du tableau détaillé et de la récapitulation diffèrent")
    fdc = [g for g in ([categories["4"]["rangee"]] + categories["4"]["fonds"] if "4" in categories else [])
           if g and g["valeur"] is not None]
    if any(valeur(g) != valeur(fdc[0] if fdc else None) for g in fonds if g["valeur"] is not None):
        sys.exit("état A : fonds de concours du tableau détaillé et de la récapitulation discordants")
    concept_ = lambda c: RECETTES_BG[c].format(sorte)
    montants, attendus = [], {}
    for d in divisions:
        f = f"LOLF.RECETTES.{code_lolf(d['numero'] + ' ' + d['libelle'])}"
        montants.append((concept_(d["categorie"]), f, f"{d['numero']}. {d['libelle']}", "", d["rangee"]))
        for g in d["lignes"]:
            nom_ = f"{g['numero']} {g['libelle']}".strip()
            montants.append((concept_(d["categorie"]), f"{f}.{code_lolf(nom_)}", nom_, f, g))
    for c in ("1", "2", "3", "4"):
        g = (fdc[0] if fdc else None) if c == "4" else categories[c]["rangee"] if c in categories else None
        if g is not None:
            montants.append((concept_(c), "", "", "", g))
        attendus[(NOMS_RECETTES_BG[c].format(sorte), "")] = valeur(g)
    c1, c2, c3 = (valeur(categories[c]["rangee"] if c in categories else None) for c in ("1", "2", "3"))
    if sorte == "NETTES":  # les totaux de la récapitulation s'entendent alors comme ceux de l'exécution
        for cle, nom_, attendu in (("1+2", "BG_RECETTES_NETTES_HORS_FDC", c1 + c2),
                                   ("1+2-3", "BG_RECETTES_NETTES_HORS_PSR", c1 + c2 - c3)):
            if cle in totaux:
                montants.append((f"LOLF.{nom_}_LFR", "", "", "", totaux[cle]))
            attendus[(nom_, "")] = attendu
    budgets, total_ba = budgets_annexes(parties.get("BA", []), connus)
    for b in budgets:
        f = f"LOLF.{code_lolf(b['nom'])}"
        if b["total"] is not None:
            montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFR", f, b["nom"], "", b["total"]))
        groupes = [(f"{f}.{code_lolf(s['nom'])}", s["lignes"]) for s in b["sections"]] + [(f, b["lignes"])]
        for s in b["sections"]:
            montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFR", f"{f}.{code_lolf(s['nom'])}", s["nom"], f, s["total"]))
        for parent, lignes in groupes:
            for g in lignes:
                nom_ = f"{g['numero']} {g['libelle']}".strip()
                montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFR", f"{parent}.{code_lolf(nom_)}", nom_, parent, g))
        attendus[("BA_RECETTES_HORS_FDC", f)] = sum(valeur(g) for g in [s["total"] for s in b["sections"]] + b["lignes"])
    if total_ba is not None:
        montants.append(("LOLF.BA_RECETTES_HORS_FDC_LFR", "", "", "", total_ba))
    attendus[("BA_RECETTES_HORS_FDC", "")] = sum(v for (c, f), v in attendus.items() if c == "BA_RECETTES_HORS_FDC")
    for categorie in ("CAS", "CCF"):
        c_ = f"LOLF.{categorie}_RECETTES_LFR"
        if categorie not in parties:
            attendus[(f"{categorie}_RECETTES", "")] = 0
            continue
        comptes, total = lf.comptes_speciaux_a(compte_et_section(parties[categorie], connus), connus, categorie,
                                               total_requis=False)
        if total is not None:
            montants.append((c_, "", "", "", total))
        for compte in comptes:
            f = f"LOLF.{code_lolf(compte['nom'])}"
            montants.append((c_, f, compte["nom"], "", compte["rangee"]))
            for parent, nom_p, lignes, g_p in [(f, None, compte["lignes"], None)] + \
                    [(f"{f}.{code_lolf(s['nom'])}", s["nom"], s["lignes"], s["rangee"]) for s in compte["sections"]]:
                if nom_p:
                    montants.append((c_, parent, nom_p, f, g_p))
                for g in lignes:
                    nom_ = f"{g['numero']} {g['libelle']}".strip()
                    montants.append((c_, f"{parent}.{code_lolf(nom_)}", nom_, parent, g))
        attendus[(f"{categorie}_RECETTES", "")] = sum(valeur(c["rangee"]) for c in comptes)
    return [m for m in montants if m[4]["nombre"]], attendus


def compte_et_section(rangees, connus):
    """Les rangées d'une partie des comptes spéciaux, où une ligne qui réunit le nom d'un compte et l'intitulé de sa
    section (« Pensions Section 3 : pensions militaires d'invalidité… ») devient ces deux lignes, au même montant : la
    page ne donne alors que cette section du compte."""
    resultat = []
    for g in rangees:
        m = None if g["numero"] else re.fullmatch(r"(.+?)\s+(Section(?: [0-9]+)?\s*:\s*.+)", g["libelle"])
        if m and f"LOLF.{code_lolf(m.group(1))}" in connus:
            resultat += [{**g, "libelle": m.group(1)}, {**g, "libelle": m.group(2)}]
        else:
            resultat.append(g)
    return resultat


def credits_nets(lignes, fonctions):
    """Ce que les chiffres de crédits d'une loi donnent pour son tableau d'équilibre, en euros, crédits de paiement
    ouverts moins annulés : {(concept sans suffixe, fonction) : euros} pour chaque catégorie, chaque budget annexe, la
    mission des remboursements et dégrèvements et son programme 200 (impôts d'État)."""
    nets = {}
    for l in lignes:
        m = re.fullmatch(r"LOLF\.(BG|BA|CAS|CCF)_CP_LFR_(OUVERTURES|ANNULATIONS)", l["concept_id"])
        if m is None:
            continue
        v = float(l["valeur"]) * (1 if m.group(2) == "OUVERTURES" else -1)
        f, parent = l["fonction_id"], fonctions.get(l["fonction_id"], {}).get("parent_id", "")
        if f == "":
            nets[(f"{m.group(1)}_CP", "")] = nets.get((f"{m.group(1)}_CP", ""), 0) + v
        # Un budget annexe, ou une mission, vaut la somme de ses programmes.
        if parent and m.group(1) == "BA":
            nets[("BA_CP", parent)] = nets.get(("BA_CP", parent), 0) + v
        if parent == "LOLF.REMBOURSEMENTS_ET_DEGREVEMENTS":
            nets[("RD", "")] = nets.get(("RD", ""), 0) + v
            if re.match(r"Remboursements et dégrèvements d[’']impôts d[’']État", fonctions[f]["libelle"]):
                nets[("RD_ETAT", "")] = nets.get(("RD_ETAT", ""), 0) + v
    return nets


def recettes_et_soldes(fichier, annee, grilles, flux, contenu, nets, fonctions, recolle):
    """Les chiffres de l'état A révisé et du tableau de l'article d'équilibre de la loi. `nets` : credits_nets de ses
    états, ou des articles quand la page ne reproduit pas les états (SANS_ETATS), sans le détail des missions."""
    source_id = fichier["source_id"]
    sorte = "NETTES" if int(annee) >= PREMIERE_ANNEE_NETTES else "BRUTES"
    connus = {f for f, l in fonctions.items() if f.startswith("LOLF.") and not l["parent_id"]
              and not f.startswith(("LOLF.RECETTES.", "LOLF.EMPLOIS."))}
    montants, attendus, donnes = [], None, set()
    if source_id in SANS_ARTICLES:  # la page ne reproduit que les états de crédits
        if any(m.group(1) == "A" for m in re.finditer(ETAT, flux)):
            sys.exit(f"{fichier['id']} : la page déclarée sans articles a un état A")
    elif source_id not in SANS_ETATS:
        parties = tableaux_etat_a(grilles, flux, annee, source_id)
        for rangees in parties.values():
            for g in rangees:
                g["libelle"] = g["page"] = recolle(g["libelle"])
                if (source_id, g["libelle"]) in LIBELLES:
                    LIBELLES_VUS.add((source_id, g["libelle"]))
                    g["libelle"] = LIBELLES[(source_id, g["libelle"])]
        montants, attendus = recettes_revisees(parties, sorte, connus)
    for concept_, fonction, libelle, parent, g in montants:
        if (concept_, fonction) in donnes:
            sys.exit(f"état A, {lf.ou(g)} : {concept_} de « {fonction or 'ensemble'} » déjà lu")
        donnes.add((concept_, fonction))
        if fonction:
            fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF", "parent_id": parent})
        if float(g["nombre"][0]) != 0:  # une révision nulle ne donne pas de chiffre
            yield chiffre(fichier, annee, concept_, fonction, g["unite"], g["nombre"],
                          f"tableau={g['tableau']};ligne={g['ligne']};colonne={g['colonne']};"
                          f"libelle={(g['numero'] + ' ' + g.get('page', g['libelle'])).strip()};"
                          f"colonne_libelle={g['colonne_libelle']}", g["note"])
    absents = [n for s, n in lf.ECARTS_A if s == source_id and (s, n) not in lf.ECARTS_VUS]
    if absents:
        sys.exit(f"état A : écart déclaré absent ({', '.join(absents)})")
    # Tableau de l'article d'équilibre, en millions d'euros.
    texte = normaliser(texte_html(contenu))
    annonce = re.search(PHRASE_EQUILIBRE.format(annee=annee), texte)
    if source_id in SANS_ARTICLES or source_id in EQUILIBRE_EN_IMAGE:
        image = EQUILIBRE_EN_IMAGE.get(source_id)
        if source_id in SANS_ARTICLES and annonce:
            sys.exit(f"{fichier['id']} : la page déclarée sans articles a un article d'équilibre")
        if image and not re.search(rf"ajustement des ressources.{{0,800}}<img[^>]*src=\"{re.escape(image)}\"",
                                   contenu, re.S):
            sys.exit(f"{fichier['id']} : l'image déclarée du tableau d'équilibre ne suit pas l'article")
        return
    tableau = lf.equilibre(grilles, flux, annee, PHRASE_EQUILIBRE, EQUILIBRE, variations=True)
    lf.verifier_equilibre(tableau, sorte, EQUILIBRE, variations=True)
    cles = {cle_ for _, cle_, _, _, _ in tableau}
    if ("Recettes fiscales brutes / dépenses brutes" in cles and sorte == "NETTES") or \
            ("Recettes fiscales / dépenses" in cles and sorte == "BRUTES"):
        sys.exit(f"tableau d'équilibre : recettes fiscales brutes ou nettes, autrement que l'état A de {annee}")
    valeurs = {}  # (concept sans suffixe, fonction) → rangée, de sa première ligne
    for bloc, cle_, fonction, cote, g in tableau:
        if fonction and fonction not in connus:
            sys.exit(f"tableau d'équilibre, ligne {g['ligne']} : budget annexe « {g['libelle']} » inconnu")
        c_ = EQUILIBRE[bloc][cle_]["RCS".index(cote)]
        if (c_, fonction) in valeurs and valeurs[(c_, fonction)]["valeur"] != g["valeur"]:
            sys.exit(f"tableau d'équilibre, ligne {g['ligne']} : « {g['libelle']} », {g['valeur']} M€ quand une autre "
                     f"ligne en donne {valeurs[(c_, fonction)]['valeur']} ({c_})")
        valeurs.setdefault((c_, fonction), g)
    du_tableau = lambda c_, f="": valeur(valeurs.get((c_, f))) * 1e6

    def comparer(c_, f, attendu, quoi, marge=1e6):
        if abs(du_tableau(c_, f) - attendu) >= marge:
            sys.exit(f"tableau d'équilibre : {c_} de « {f or 'ensemble'} », {du_tableau(c_, f) / 1e6:,.0f} M€ quand "
                     f"{quoi} {attendu:,.0f} €")
    # Ressources contre l'état A, au million près ; un budget annexe que l'état A ne révise pas n'a pas de ressources.
    if attendus is not None:
        for (c_, f) in set(attendus) | {(c_, f) for c_, f in valeurs if c_ == "BA_RECETTES_HORS_FDC"}:
            comparer(c_, f, attendus.get((c_, f), 0), "l'état A donne")
    # Charges contre les crédits que la loi ouvre et annule, au million près, à l'écart déclaré près.
    detail = source_id not in SANS_ETATS  # les états donnent les missions et les budgets annexes
    budgets = {f for c_, f in list(valeurs) + list(nets) if c_ == "BA_CP" and f}
    charges = {(c_, f): nets.get((c_, f), 0) + ECARTS_CHARGES.get((source_id, c_), 0) * (f == "")
               for c_, f in [("BG_CP", ""), ("BA_CP", ""), ("CAS_CP", ""), ("CCF_CP", "")] +
               [("BA_CP", f) for f in budgets]}
    for (c_, f), attendu in charges.items():
        if (c_, sorte) != ("BG_CP", "NETTES"):  # depuis 2023, le tableau ne donne que des dépenses nettes
            comparer(c_, f, attendu, "les états de la loi donnent")
    # Remboursements et dégrèvements : jusqu'en 2022, le tableau les déduit des recettes et des dépenses, et ce sont les
    # crédits de leur mission ; depuis, ses dépenses sont nettes de ceux d'impôts d'État (programme 200).
    depenses_bg = charges[("BG_CP", "")] - (nets.get(("RD_ETAT", ""), 0) if sorte == "NETTES" else 0)
    if detail and sorte == "BRUTES":
        comparer("BG_REMBOURSEMENTS_DEGREVEMENTS", "", nets.get(("RD", ""), 0),
                 "la mission « Remboursements et dégrèvements » des états en donne")
    elif detail:
        comparer("BG_DEPENSES_NETTES_HORS_FDC", "", depenses_bg,
                 "les états, hors remboursements et dégrèvements d'impôts d'État, en donnent")
    # Soldes contre ceux que donnent les états : la marge d'un demi-million par montant arrondi en jeu, plus un.
    if attendus is not None:
        recettes_bg = sum(attendus[(NOMS_RECETTES_BG[c].format(sorte), "")] * (-1 if c == "3" else 1) for c in "123")
        comparer("SOLDE_BUDGET_GENERAL", "", recettes_bg - depenses_bg, "les états donnent", 0.5e6 * 5)
        soldes = {("BA_SOLDE_HORS_FDC", f): ("BA_RECETTES_HORS_FDC", "BA_CP", f) for c_, f in charges if c_ == "BA_CP"}
        soldes.update({("CAS_SOLDE", ""): ("CAS_RECETTES", "CAS_CP", ""), ("CCF_SOLDE", ""): ("CCF_RECETTES", "CCF_CP", "")})
        for (c_, f), (recettes_, depenses, f_) in soldes.items():
            comparer(c_, f, attendus.get((recettes_, f_), 0) - charges[(depenses, f_)], "les états donnent", 0.5e6 * 3)
    # Ce que le tableau donne seul s'enregistre ; une case nulle ou vide ne donne pas de chiffre. Quand la page ne
    # reproduit pas l'état A, les recettes qu'il donnerait se lisent dans le tableau, et leur note le dit.
    concernes, note_ = NOTES_EQUILIBRE.get(source_id, (set(), ""))
    for (c_, f), g in valeurs.items():
        concept_ = f"LOLF.{c_}_LFR"
        if c_ in VERIFIES_SEULEMENT or (concept_, f) in donnes or not g["nombre"] or g["valeur"] == 0:
            continue
        note = " ".join(n for n in (note_ if c_ in concernes else "",
                                    "Lu dans le tableau de l’article d’équilibre, en millions d’euros : le texte ne "
                                    "reproduit pas l’état A." if source_id in SANS_ETATS and c_ in RECETTES_ETAT_A
                                    else "") if n)
        yield chiffre(fichier, annee, concept_, f, "MIO_EUR", g["nombre"],
                      f"tableau={g['tableau']};ligne={g['ligne']};colonne={g['colonne']};libelle={g['libelle']};"
                      f"colonne_libelle={g['colonne_libelle']}", note)


def lignes_du_fichier(fichier, fonctions):
    """Les chiffres d'une copie archivée ; `fonctions` (identifiant → ligne) reçoit les missions et les programmes."""
    chemin = BASE / fichier["chemin"]
    source_id = fichier["source_id"]
    grilles, formes, flux = lire_page_html(chemin)
    flux = INVISIBLES.sub("", flux)
    contenu = lire_texte_html(chemin)
    texte_brut = texte_html(contenu)
    # Pour lire les articles, une balise de mise en forme ne coupe pas un mot (« financ<span>iers</span> »).
    texte = normaliser(texte_html(re.sub(r"</?(?:span|a|b|i|em|strong|u|font)\b[^>]*>", "", contenu)))
    annees = set(re.findall(r"(?i)crédits?(?: supplémentaires?)?(?: ouverts?)?(?: et annulés)?(?: annulés)? pour "
                            r"([0-9]{4})|pour ([0-9]{4})(?:,)? par mission", flux))
    annees = {a or b for a, b in annees}
    if source_id in SANS_ETATS:
        annees = set(re.findall(r"Il est ouvert aux ministres, pour ([0-9]{4})", texte))
    if len(annees) != 1 or not fichier["mis_a_jour_source"]:
        sys.exit(f"{fichier['id']} : année de la loi ({', '.join(sorted(annees)) or 'aucune'}) ou date du texte "
                 f"introuvable")
    annee = annees.pop()
    if fichier["mis_a_jour_source"][:4] != annee:
        sys.exit(f"{fichier['id']} : loi de finances rectificative pour {annee} dans un texte daté "
                 f"{fichier['mis_a_jour_source']}")
    lus = [] if source_id in SANS_ARTICLES else articles(texte, annee)
    # Une coupure de mot de fin de ligne du texte imprimé, restée dans la page (« dévelop-pement »), se recolle quand
    # le mot entier figure ailleurs dans le texte.
    mots = set(re.findall(r"\w+", texte.lower()))
    recolle = lambda libelle: re.sub(r"(\w+)-(\w+)", lambda m: m.group(1) + m.group(2) if m.group(1)[-1].islower() and
                                     m.group(2)[0].islower() and (m.group(1) + m.group(2)).lower() in mots
                                     else m.group(0), libelle)
    if source_id in SANS_ETATS:
        credits_ = list(totaux_des_articles(fichier, annee, lus, texte_brut))
    else:
        credits_ = list(credits_des_etats(fichier, annee, grilles, formes, flux, lus, fonctions, recolle))
    yield from credits_
    yield from recettes_et_soldes(fichier, annee, grilles, flux, contenu, credits_nets(credits_, fonctions), fonctions,
                                  recolle)
    absents = [x for s, x in LIBELLES if s == source_id and (s, x) not in LIBELLES_VUS]
    if absents:
        sys.exit(f"{fichier['id']} : libellé déclaré absent de la page ({' ; '.join(absents)})")


def credits_des_etats(fichier, annee, grilles, formes, flux, lus, fonctions, recolle):
    """Les chiffres des états de crédits de la loi (B, C, D, et B', C', D', B'' jusqu'en 2009)."""
    source_id = fichier["source_id"]
    blocs = blocs_des_etats(grilles, formes, flux, source_id)
    if not blocs:
        sys.exit(f"{fichier['id']} : aucun état de crédits")
    if source_id not in SANS_ARTICLES:
        verifier_articles(blocs, lus, source_id)
    missions_connues = {f for f, l in fonctions.items() if f.startswith("LOLF.") and not l["parent_id"]
                        and not f.startswith(("LOLF.RECETTES.", "LOLF.EMPLOIS."))}
    vus = {}
    note_page = SANS_ARTICLES.get(source_id, "")
    for bloc in blocs:
        rattache = structure(bloc, missions_connues)
        traitement = TRAITEMENTS.get((source_id, bloc["etat"]), "")
        note_unite = "La page n’annonce pas l’unité de l’état : ses totaux égalent, à l’euro, les montants des " \
                     "articles de la loi." if source_id in UNITE_TUE else ""
        for l in bloc["lignes"]:
            fonction = ""
            if l["genre"] != "total":
                libelle, mission = (recolle(x) for x in rattache[(l["tableau"], l["ligne"])])
                for x in (libelle, mission):
                    if (source_id, x) in LIBELLES:
                        LIBELLES_VUS.add((source_id, x))
                libelle, mission = (LIBELLES.get((source_id, x), x) for x in (libelle, mission))
                parent = f"LOLF.{code_lolf(mission)}" if mission else ""
                fonction = f"{parent or 'LOLF'}.{code_lolf(libelle)}"
                if parent:
                    fonctions.setdefault(parent, {"id": parent, "libelle": mission, "norme_id": "LOLF", "parent_id": ""})
                fonctions.setdefault(fonction, {"id": fonction, "libelle": libelle, "norme_id": "LOLF",
                                                "parent_id": parent})
            for (colonne, sens), (c, nombre) in sorted(l["cases"].items()):
                if float(nombre[0]) == 0:
                    continue  # une case nulle dit qu'aucun crédit n'est ouvert ou annulé, comme une case vide
                concept_ = concept(bloc["categorie"], colonne, sens, l["genre"] == "dont")
                if (concept_, fonction, traitement) in vus:
                    sys.exit(f"{fichier['id']} : {concept_} de « {fonction or 'ensemble'} » lu deux fois (états "
                             f"{vus[(concept_, fonction, traitement)]} et {bloc['etat']})")
                vus[(concept_, fonction, traitement)] = bloc["etat"]
                yield chiffre(fichier, annee, concept_, fonction, "EUR", nombre,
                              f"tableau={l['tableau']};ligne={l['ligne']};colonne={c};libelle={l['libelle']};"
                              f"colonne_libelle={l['noms'][c]}",
                              " ".join(n for n in (note_unite, note_page) if n), traitement)


def totaux_des_articles(fichier, annee, lus, texte_brut):
    """Quand la page ne reproduit pas les états : le total de chaque catégorie, lu dans la phrase de l'article qui
    l'énonce. La phrase retenue va de la catégorie au montant, pour n'en porter qu'un nombre, et doit figurer telle
    quelle dans la page."""
    note = SANS_ETATS[fichier["source_id"]]
    vus = set()
    for etat, categories, sens, montants_, phrase in lus:
        if len(categories) != 1 or len(sens) != 1 or len({v for c, v in montants_.items() if c in ("AE", "CP")}) != 1:
            sys.exit(f"{fichier['id']} : article que l'import ne sait pas relire sans son état : « {phrase} »")
        montant_ = re.search(MONTANT, phrase)
        # L'extrait commence à la catégorie, ou après l'année quand elle la suit, pour ne porter qu'un nombre.
        debut = max([re.search(r"\bau titre\b|\bau compte\b", phrase).start()] +
                    [m.end() for m in re.finditer(r"pour [0-9]{4},? ", phrase[:montant_.start()])])
        # Le même extrait, tel que l'écrit la page : ses blancs et ses apostrophes peuvent différer du texte normalisé.
        motif = "".join(r"\s*['’]\s*" if x == "’" else r"\s+" if x == " " else re.escape(x)
                        for x in phrase[debut:montant_.end()])
        trouves = [m.group(0) for m in re.finditer(motif, texte_brut)]
        extrait = trouves[0] if len(trouves) == 1 else None
        if extrait is None or nombre_de_phrase(extrait) is None:
            sys.exit(f"{fichier['id']} : phrase introuvable, ou plusieurs fois, dans la page : "
                     f"« {phrase[debut:montant_.end()]} »")
        quoi = "L’article annule « un crédit », que la base lit comme des crédits de paiement. " \
            if montants_.get("un crédit") else ""
        for colonne in ("AE", "CP"):
            if colonne in montants_:
                concept_ = concept(categories[0], colonne, next(iter(sens)), False)
                if concept_ in vus:
                    sys.exit(f"{fichier['id']} : deux articles pour {concept_}")
                vus.add(concept_)
                yield chiffre(fichier, annee, concept_, "", "EUR", nombre_de_phrase(extrait), f"phrase={extrait}",
                              quoi + note)


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
