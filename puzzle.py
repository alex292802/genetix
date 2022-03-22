import random as rd
import numpy as np
import piece as pc


class puzzle:

    # pieces représente le puzzle complet
    def __init__(self, size=int, pieces=np.ndarray, aleatoire=True):
        # On récupére la taille du puzzle
        self.s = size

        # Notre nouvelle configuration de puzzle :
        new_conf = np.empty(0, dtype=pc.piece)

        if aleatoire:
            # On crée une liste des indices correspondant à chaque pièce et on la mélange
            in_coins = [0, 1, 2, 3]
            in_bords = [i for i in range(4, (self.s - 1) * 4)]
            in_milieu = [i for i in range((self.s - 1) * 4, self.s ** 2)]

            np.random.shuffle(in_coins)
            np.random.shuffle(in_bords)
            np.random.shuffle(in_milieu)

            # On crée une nouvelle configuration en prenant aléatoirement une nouvelle pièce, on la tourne aléatoirement
            for i in range(self.s ** 2):

                if i in [i for i in range(1, self.s - 1)]:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 0, new_conf.size, self.s))

                elif i in [i * self.s + self.s - 1 for i in range(1, self.s - 1)]:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 3, new_conf.size, self.s))

                elif i in [i for i in range(self.s * (self.s - 1) + 1, self.s ** 2 - 1)]:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 2, new_conf.size, self.s))

                elif i in [i * self.s for i in range(1, self.s - 1)]:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 1, new_conf.size, self.s))

                elif i == 0:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 1, new_conf.size, self.s))

                elif i == self.s - 1:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 0, new_conf.size, self.s))

                elif i == self.s ** 2 - 1:
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 3, new_conf.size, self.s))

                elif i == self.s * (self.s - 1):
                    new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 2, new_conf.size, self.s))

                else:
                    new_conf = np.append(new_conf,
                                         pc.piece(np.array(pieces[in_milieu.pop()]), rd.randrange(4), new_conf.size,
                                                  self.s))

        else:
            new_conf = pieces

        self.conf = new_conf
        self.eval = self.evaluation()

        self.inn_coins = [0, self.s - 1, self.s * (self.s - 1), self.s ** 2 - 1]
        self.inn_bords = [i for i in range(1, self.s - 1)] + [i * self.s + self.s - 1 for i in range(1, self.s - 1)] + \
                         [i for i in range(self.s * (self.s - 1) + 1, self.s ** 2 - 1)] + [i * self.s for i in
                                                                                           range(1, self.s - 1)]
        self.inn_milieu = list(
            np.array([[i + self.s * j for i in range(1, self.s - 1)] for j in range(1, self.s - 1)]).flatten())

    def matching_edges(self, piece, piece_):
        return (piece.sud != 0 or piece_.sud == 0) and (piece.nord != 0 or piece_.nord == 0) and \
               (piece.est != 0 or piece_.est == 0) and (piece.ouest != 0 or piece_.ouest == 0)

    # On échange 2 pièces à partir de leurs indices
    def mutation_swap(self):
        a = rd.randrange(self.s ** 2)

        if self.conf[a].cat == 2:
            b = rd.choice(self.inn_coins)
            self.conf[a].x, self.conf[b].x, self.conf[a].y, self.conf[b].y = self.conf[b].x, self.conf[a].x, self.conf[
                b].y, self.conf[a].y

            compteur = 0
            while not self.matching_edges(self.conf[a], self.conf[b]):
                compteur += 1
                self.conf[a].rotate()

            for i in range(4 - compteur):
                self.conf[b].rotate()

        elif self.conf[a].cat == 1:
            b = rd.choice(self.inn_bords)
            print(self.eval, self.conf[a].x, self.conf[b].x, self.conf[a].y, self.conf[b].y)
            self.conf[a].x, self.conf[b].x, self.conf[a].y, self.conf[b].y = self.conf[b].x, self.conf[a].x, self.conf[
                b].y, self.conf[a].y

            compteur = 0
            while not self.matching_edges(self.conf[a], self.conf[b]):
                compteur += 1
                self.conf[a].rotate()

            for i in range(4 - compteur):
                self.conf[b].rotate()

        else:
            b = rd.choice(self.inn_milieu)
            self.conf[a].x, self.conf[b].x, self.conf[a].y, self.conf[b].y = self.conf[b].x, self.conf[a].x, self.conf[
                b].y, self.conf[a].y

        self.conf[b], self.conf[a] = self.conf[a], self.conf[b]
        self.eval = self.evaluation()

    # On tourne la pièce une fois dans le sens trigonomètrique
    def mutation_rotation(self):
        a = rd.choice(self.inn_milieu)
        self.conf[a].rotate()
        self.eval = self.evaluation()

    # On évalue le score de notre config
    def evaluation(self):
        score = 0
        score_ = 0

        # On regarde chaque pièce
        for piece in self.conf:
            if piece.y != 0:
                # On récupère la pièce d'au dessus :
                piece_ = self.conf[piece.x + self.s * (piece.y - 1)]
                # On compare le sud de la pièce d'au dessus avec le nord de la pièce qui nous intéresse
                score += int(piece.nord == piece_.sud)
                score_ += int(piece.nord != piece_.sud)

            # Si la pièce n'est pas sur le bord gauche
            if piece.x != 0:
                # Si la gauche de la pièce correspond à une bordure
                piece__ = self.conf[piece.x - 1 + self.s * piece.y]
                score += int(piece.ouest == piece__.est)
                score_ += int(piece.ouest != piece__.est)

        return score_

    # Affichage de la configuration
    def render(self):
        print("," + ("------," * self.s))
        char_nord = ''
        char_sud = ''
        char_uest = ''
        for i in range(self.s):
            for j in range(self.s):
                char_nord += ("| \\" + str(self.conf[j + self.s * i].nord // 10) + str(
                    self.conf[j + self.s * i].nord % 10) + "/ ")
                char_uest += ("|" + str(self.conf[j + self.s * i].ouest // 10) + str(
                    self.conf[j + self.s * i].ouest % 10) + "||" + str(self.conf[j + self.s * i].est // 10) + str(
                    self.conf[j + self.s * i].est % 10))
                char_sud += ("| /" + str(self.conf[j + self.s * i].sud // 10) + str(
                    self.conf[j + self.s * i].sud % 10) + "\\ ")
            print(char_nord + "|")
            print(char_uest + "|")
            print(char_sud + "|")
            if i != self.s - 1:
                print("|" + ("------|" * self.s))
            else:
                print("'" + ("------'" * self.s))
            char_nord = ''
            char_uest = ''
            char_sud = ''