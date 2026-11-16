"""Lecture des archives RAR (format 2.9, celui de WinRAR 3 à 4) sans bibliothèque extérieure.

La DGFiP a publié en RAR les balances comptables de 2016 des groupements à fiscalité propre, des syndicats et des
établissements publics locaux. Python ne sait pas ouvrir ce format, et la bibliothèque libarchive des systèmes Linux
courants en tire un contenu faux pour ces fichiers (son contrôle d'intégrité le refuse). Ce module décompresse
lui-même la méthode d'Eugene Roshal : un codage LZ77 de Huffman, les tables de codes changeant de bloc en bloc. Il ne
sait pas lire les blocs PPMd ni les filtres de la machine virtuelle de RAR, que ces fichiers n'emploient pas : s'il en
rencontre, il s'arrête. Le contenu décompressé n'est rendu que si sa taille et son empreinte CRC-32 sont celles
qu'inscrit l'archive : une erreur de décompression ne peut pas passer inaperçue.

    nom, contenu = rar.extraire(chemin)   # le seul fichier d'une archive
"""

import struct
import zlib

SIGNATURE = b"Rar!\x1a\x07\x00"
NC, DC, LDC, RC = 299, 60, 17, 28  # tailles des quatre tables : littéraux et longueurs, distances, bas des distances,
BC = 20                            # longueurs répétées ; table des longueurs de codes
LDECODE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224]
LBITS = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]
SDDECODE = [0, 4, 8, 16, 32, 64, 128, 192]
SDBITS = [2, 2, 3, 4, 5, 6, 6, 6]
DDECODE, DBITS = [], []
_distance = 0
for _bits, _nombre in enumerate([4] + [2] * 15 + [14, 0, 12]):
    for _ in range(_nombre):
        if len(DDECODE) < DC:
            DDECODE.append(_distance)
            DBITS.append(_bits)
        _distance += 1 << _bits
MAXBITS = 15


class ErreurRar(Exception):
    pass


def entetes(donnees):
    """(nom du fichier, taille compressée, taille décompressée, CRC-32, début des données compressées, drapeaux) du seul
    fichier d'une archive RAR 2.9."""
    if not donnees.startswith(SIGNATURE):
        raise ErreurRar("pas une archive RAR 2.9 (signature)")
    i, fichiers = len(SIGNATURE), []
    while i + 7 <= len(donnees):
        _, genre, drapeaux, taille = struct.unpack_from("<HBHH", donnees, i)
        if genre == 0x7B:  # fin d'archive
            break
        suite = struct.unpack_from("<I", donnees, i + 7)[0] if drapeaux & 0x8000 else 0
        if genre == 0x74:  # fichier
            compresse, decompresse, _, crc, _, version, methode, longueur_nom, _ = struct.unpack_from(
                "<IIBIIBBHI", donnees, i + 7)
            debut_nom = i + 32
            if drapeaux & 0x100:
                haut_c, haut_d = struct.unpack_from("<II", donnees, debut_nom)
                compresse += haut_c << 32
                decompresse += haut_d << 32
                debut_nom += 8
            nom = donnees[debut_nom:debut_nom + longueur_nom].split(b"\x00")[0].decode("latin-1")
            if drapeaux & 0x04:
                raise ErreurRar(f"{nom} : fichier chiffré")
            if drapeaux & 0x13:
                raise ErreurRar(f"{nom} : archive en plusieurs volumes ou « solide », que ce module ne lit pas")
            if version != 29 and methode != 0x30:
                raise ErreurRar(f"{nom} : version de compression {version} que ce module ne lit pas")
            fichiers.append((nom, compresse, decompresse, crc, i + taille, methode))
            i += taille + compresse
            continue
        i += taille + suite
    return fichiers


class _Bits:
    """Les bits d'un flux, du plus fort au plus faible de chaque octet."""

    def __init__(self, donnees):
        self.donnees = bytes(donnees) + b"\x00" * 8
        self.position = 0  # en bits

    def lire16(self):
        p = self.position
        return (int.from_bytes(self.donnees[p >> 3:(p >> 3) + 3], "big") >> (8 - (p & 7))) & 0xFFFF

    def avancer(self, n):
        self.position += n

    def prendre(self, n):
        valeur = self.lire16() >> (16 - n)
        self.position += n
        return valeur


def _table(longueurs):
    """La table de décodage d'un code de Huffman canonique : pour chaque valeur des MAXBITS bits à venir, (symbole,
    longueur de son code)."""
    nombres = [0] * (MAXBITS + 1)
    for n in longueurs:
        if n:
            nombres[n] += 1
    code, premiers = 0, [0] * (MAXBITS + 2)
    for n in range(1, MAXBITS + 1):
        premiers[n] = code
        code = (code + nombres[n]) << 1
    table = [None] * (1 << MAXBITS)
    suivants = premiers[:]
    for symbole, n in enumerate(longueurs):
        if not n:
            continue
        c = suivants[n]
        suivants[n] += 1
        debut = c << (MAXBITS - n)
        entree = (symbole, n)
        for k in range(debut, debut + (1 << (MAXBITS - n))):
            table[k] = entree
    return table


def _decoder(bits, table):
    entree = table[bits.lire16() >> 1]
    if entree is None:
        raise ErreurRar("code de Huffman invalide")
    bits.position += entree[1]
    return entree[0]


class _Decompression:
    def __init__(self, donnees):
        self.bits = _Bits(donnees)
        self.anciennes = [0] * (NC + DC + LDC + RC)
        self.distances = [0, 0, 0, 0]
        self.derniere_longueur = 0
        self.bas_precedent = 0
        self.repetitions_bas = 0

    def lire_tables(self):
        b = self.bits
        if b.position & 7:
            b.avancer(8 - (b.position & 7))
        champ = b.lire16()
        if champ & 0x8000:
            raise ErreurRar("bloc PPMd, que ce module ne lit pas")
        self.bas_precedent, self.repetitions_bas = 0, 0
        if not champ & 0x4000:
            self.anciennes = [0] * len(self.anciennes)
        b.avancer(2)
        longueurs_bc, i = [0] * BC, 0
        while i < BC:
            n = b.prendre(4)
            if n == 15:
                zeros = b.prendre(4)
                if zeros == 0:
                    longueurs_bc[i] = 15
                else:
                    for _ in range(zeros + 2):
                        if i >= BC:
                            break
                        longueurs_bc[i] = 0
                        i += 1
                    continue
            else:
                longueurs_bc[i] = n
            i += 1
        table_bc = _table(longueurs_bc)
        taille = NC + DC + LDC + RC
        longueurs, i = [0] * taille, 0
        while i < taille:
            n = _decoder(b, table_bc)
            if n < 16:
                longueurs[i] = (n + self.anciennes[i]) & 0xF
                i += 1
            elif n < 18:
                repete = b.prendre(3) + 3 if n == 16 else b.prendre(7) + 11
                if i == 0:
                    raise ErreurRar("table de codes invalide")
                for _ in range(repete):
                    if i >= taille:
                        break
                    longueurs[i] = longueurs[i - 1]
                    i += 1
            else:
                repete = b.prendre(3) + 3 if n == 18 else b.prendre(7) + 11
                for _ in range(repete):
                    if i >= taille:
                        break
                    longueurs[i] = 0
                    i += 1
        self.anciennes = longueurs
        self.ld = _table(longueurs[:NC])
        self.dd = _table(longueurs[NC:NC + DC])
        self.ldd = _table(longueurs[NC + DC:NC + DC + LDC])
        self.rd = _table(longueurs[NC + DC + LDC:])

    def fin_de_bloc(self):
        """Faux à la fin du fichier ; vrai si le flux continue, avec de nouvelles tables au besoin."""
        b = self.bits
        champ = b.lire16()
        if champ & 0x8000:
            nouvelles, fin = True, False
            b.avancer(1)
        else:
            nouvelles, fin = bool(champ & 0x4000), True
            b.avancer(2)
        if fin:
            return False
        if nouvelles:
            self.lire_tables()
        return True

    def decompresser(self, taille):
        sortie = bytearray()
        b, distances = self.bits, self.distances
        self.lire_tables()
        limite = len(b.donnees) * 8 - 64
        while len(sortie) < taille:
            if b.position > limite:
                raise ErreurRar("données compressées tronquées")
            entree = self.ld[b.lire16() >> 1]
            if entree is None:
                raise ErreurRar("code de Huffman invalide")
            b.position += entree[1]
            n = entree[0]
            if n < 256:
                sortie.append(n)
                continue
            if n >= 271:
                n -= 271
                longueur = LDECODE[n] + 3
                if LBITS[n]:
                    longueur += b.prendre(LBITS[n])
                k = _decoder(b, self.dd)
                distance = DDECODE[k] + 1
                nb = DBITS[k]
                if nb:
                    if k > 9:
                        if nb > 4:
                            distance += (b.lire16() >> (20 - nb)) << 4
                            b.avancer(nb - 4)
                        if self.repetitions_bas > 0:
                            self.repetitions_bas -= 1
                            distance += self.bas_precedent
                        else:
                            bas = _decoder(b, self.ldd)
                            if bas == 16:
                                self.repetitions_bas = 15
                                distance += self.bas_precedent
                            else:
                                distance += bas
                                self.bas_precedent = bas
                    else:
                        distance += b.prendre(nb)
                if distance >= 0x2000:
                    longueur += 1
                    if distance >= 0x40000:
                        longueur += 1
                distances[3], distances[2], distances[1], distances[0] = distances[2], distances[1], distances[0], distance
                self.derniere_longueur = longueur
                copier(sortie, longueur, distance)
            elif n == 256:
                if not self.fin_de_bloc():
                    break
            elif n == 257:
                raise ErreurRar("filtre de la machine virtuelle de RAR, que ce module ne lit pas")
            elif n == 258:
                if self.derniere_longueur:
                    copier(sortie, self.derniere_longueur, distances[0])
            elif n < 263:
                k = n - 259
                distance = distances[k]
                for j in range(k, 0, -1):
                    distances[j] = distances[j - 1]
                distances[0] = distance
                m = _decoder(b, self.rd)
                longueur = LDECODE[m] + 2
                if LBITS[m]:
                    longueur += b.prendre(LBITS[m])
                self.derniere_longueur = longueur
                copier(sortie, longueur, distance)
            else:
                k = n - 263
                distance = SDDECODE[k] + 1
                if SDBITS[k]:
                    distance += b.prendre(SDBITS[k])
                distances[3], distances[2], distances[1], distances[0] = distances[2], distances[1], distances[0], distance
                self.derniere_longueur = 2
                copier(sortie, 2, distance)
        return sortie


def copier(sortie, longueur, distance):
    """Recopie à la fin de la sortie `longueur` octets pris `distance` octets plus tôt, qui peuvent se recouvrir."""
    if distance > len(sortie) or distance <= 0:
        raise ErreurRar("distance hors de la fenêtre")
    debut = len(sortie) - distance
    if distance >= longueur:
        sortie += sortie[debut:debut + longueur]
    else:
        motif = sortie[debut:]
        sortie += (motif * (longueur // distance + 1))[:longueur]


def extraire(chemin):
    """(nom, contenu) du seul fichier d'une archive RAR 2.9, après contrôle de sa taille et de son CRC-32."""
    with open(chemin, "rb") as f:
        donnees = f.read()
    fichiers = entetes(donnees)
    if len(fichiers) != 1:
        raise ErreurRar(f"l'archive devait porter un seul fichier, elle en porte {len(fichiers)}")
    nom, compresse, taille, crc, debut, methode = fichiers[0]
    brut = donnees[debut:debut + compresse]
    contenu = bytes(brut) if methode == 0x30 else bytes(_Decompression(brut).decompresser(taille))
    if len(contenu) != taille or zlib.crc32(contenu) != crc:
        raise ErreurRar(f"{nom} : contenu décompressé faux (taille ou CRC-32 autres que ceux de l'archive)")
    return nom, contenu
