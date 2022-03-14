import random as rd
import numpy as np
import piece as pc


class puzzle:

    def __init__(self, size=int, tools=np.ndarray):
        self.s = size

        new_conf = np.empty(0, dtype=pc.piece)# notre nouvelle configuration de puzzle
        print (new_conf)
        indices = np.arange(size ** 2)
        np.random.shuffle(indices)

        for i in indices[:size ** 2]:
            print(new_conf)
            new_conf = np.append(new_conf, pc.piece(np.array(tools[i]), rd.randrange(4), new_conf.size, self.s))

        self.conf = new_conf
        self.eval = self.evaluation()

    def mutation_swap(self):
        a,b = rd.randrange(self.s**2),rd.randrange(self.s**2)
        self.conf[b],self.conf[a] = self.conf[a],self.conf[b]

    def mutation_rotation(self):
        a = rd.randrange(self.s**2)
        self.conf[a].rotate()

    def evaluation(self):
        score = 0
        score_ = 0

        for piece in self.conf:
            if piece.y == 0:
                score += int(piece.nord == 0)
                score_ += int(piece.nord != 0)
            else:
                piece_ = self.conf[piece.x + self.s * (piece.y - 1)]
                score += int(piece.nord == piece_.sud and piece.nord != 0)
                score_ += int(piece.nord != piece_.sud or piece.nord == 0)

            if piece.y == self.s - 1:
                score += int(piece.sud == 0)
                score_ += int(piece.sud != 0)

            if piece.x == 0:
                score += int(piece.ouest == 0)
                score_ += int(piece.ouest != 0)

            else:
                piece__ = self.conf[piece.x - 1 + self.s * piece.y]
                score += int(piece.ouest == piece__.est and piece.ouest != 0)
                score_ += int(piece.ouest != piece__.est or piece.ouest == 0)

            if piece.x == self.s - 1:
                score += int(piece.est == 0)
                score_ += int(piece.est != 0)
        return score_

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
