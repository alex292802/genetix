import puzzle as pz
import numpy as np
import random as rd
import piece as pc

def contains(lis, lofl):
    for i in lofl:
        if (i == lis).sum() == 4:
            return True

    return False

class puzzle_sample:

    def __init__(self, sample_size = int, puzzle_size = int, dlamb = 1.2, dlinear = True, pieces = None, from_zero = True, pus = None):
        
        self.fit = None
        self.s = sample_size
        #Taille du puzzle 
        self.pss = puzzle_size


        if from_zero:
            ps = np.empty(0, dtype = pz.puzzle)

            for i in range(sample_size):
                ps = np.append(ps, pz.puzzle(puzzle_size, pieces))

            self.ps = ps

        else:
            self.ps = pus

        self.r = self.ranking(lamb = dlamb, linear = dlinear)

    def compatible(self,zone1,zone2):
        return (zone1[0] == 2 and zone2[0] == 2) or (zone1[0] == 2 and zone2[0] == 2) or  (zone1[0] == 2 and zone2[0] == 2) or (zone1[0] == 2 and zone2[0] == 2)

    def ranking(self, lamb = float, linear = bool):

        f = lambda x: x.eval
        func = np.vectorize(f)
        eval_tab = func(self.ps)
        rating_tab = eval_tab.argsort()
        rank_tab = rating_tab.argsort()

        if linear:
            f = lambda x : 2 - lamb + 2 * (lamb - 1) * x / (self.s - 1)

        else:
            f = lambda x : lamb**x

        func = np.vectorize(f)
        self.fit = func(rank_tab)

        return rating_tab

    def hybrydation(self, puzzle, puzzle_):
        leng = rd.randrange(1, self.pss // 2 + 1)
        wid = rd.randrange(1, self.pss // 2 + 1)

        #X1 et Y1 sont initialisés de manière à ce que l'aire ne dépasse pas le carré
        x1 = rd.randrange(1, self.pss - leng)
        y1 = rd.randrange(1, self.pss - wid)
        """x1 = rd.randrange(self.pss + 1 -leng)
        y1 = rd.randrange(self.pss + 1 - wid)"""
        data_zone_puzzle = []
        data_zone_puzzle_ = []
        hybr = []
        hybr_ = []
        inter = []
        exclu_puzzle = []
        exclu_puzzle_ = []
        index_exclu_puzzle = []
        index_exclu_puzzle_ = []

        if (x1 == 0 and y1 == 0) or (x1 == 0 and y1 + wid == self.pss) or (x1 + leng == self.pss and y1 == 0) or (x1 + leng == self.pss and y1 + wid == self.pss):
            x2 = rd.choice([0, self.pss - len])
            y2 = rd.randrange([0, self.pss - wid])

            while x1 == x2 and y1 == y2:
                x2 = rd.choice([0, self.pss - len])

                y2 = rd.randrange([0, self.pss - wid])

            for i in range(wid):
                for j in range(leng):
                    data_zone_puzzle.append([np.array(puzzle.conf[x1 + j + self.pss * (y1 + i)].data), puzzle.conf[x1 + j + self.pss * (y1 + i)].rot])
                    data_zone_puzzle_.append([np.array(puzzle_.conf[x2 + j + self.pss * (y2 + i)].data), puzzle_.conf[x2 + j + self.pss * (y2 + i)].rot])

            compteur = 0
            while not compatible(data_zone_puzzle, data_zone_puzzle_):
                rota_zone(data_zone_puzzle)
                compteur += 1

            for i in range(4 - compteur):
                rota_zone(data_zone_puzzle_)

            for i in range(len(data_zone_puzzle)):
                if contains(data_zone_puzzle[i][0], [j[0] for j in data_zone_puzzle_]):
                    inter.append(data_zone_puzzle[i])

                else :
                    exclu_puzzle.append(data_zone_puzzle[i])

            for i in range(len(data_zone_puzzle)):
                if not(contains(data_zone_puzzle_[i][0], [j[0] for j in data_zone_puzzle])):
                    exclu_puzzle_.append(data_zone_puzzle_[i])

                data_zone_puzzle_[i] = pc.piece(np.array(data_zone_puzzle_[i][0]), data_zone_puzzle_[i][1], 0, self.pss)

            for i in range(len(data_zone_puzzle)):
                data_zone_puzzle[i] = pc.piece(np.array(data_zone_puzzle[i][0]), data_zone_puzzle[i][1], 0, self.pss)

            print(exclu_puzzle, exclu_puzzle_)
            for i in range (len(exclu_puzzle)):
                exclu_puzzle[i] = pc.piece(np.array(exclu_puzzle[i][0]), exclu_puzzle[i][1], 0, self.pss)

                for j in range(len(puzzle_.conf)):
                    if (exclu_puzzle[i].data == puzzle_.conf[j].data).sum() == 4:
                        index_exclu_puzzle_.append(j)

            for i in range(len(exclu_puzzle_)):
                exclu_puzzle_[i] = pc.piece(np.array(exclu_puzzle_[i][0]), exclu_puzzle_[i][1], 0, self.pss)

                for j in range(len(puzzle.conf)):
                    if (exclu_puzzle_[i].data == puzzle.conf[j].data).sum() == 4:
                        index_exclu_puzzle.append(j)

        elif x1 == 0 or y1 == 0 or x1 + leng == self.pss or y1 + wid == self.pss:
            print('hjif')

        else:
            x2 = rd.randrange(1, self.pss - leng)
            y2 = rd.randrange(1, self.pss - wid)

            for i in range(wid):
                for j in range(leng):
                    data_zone_puzzle.append([np.array(puzzle.conf[x1 + j + self.pss * (y1 + i)].data), puzzle.conf[x1 + j + self.pss * (y1 + i)].rot])
                    data_zone_puzzle_.append([np.array(puzzle_.conf[x2 + j + self.pss * (y2 + i)].data), puzzle_.conf[x2 + j + self.pss * (y2 + i)].rot])


            for i in range(len(data_zone_puzzle)):
                if contains(data_zone_puzzle[i][0], [j[0] for j in data_zone_puzzle_]):
                    inter.append(data_zone_puzzle[i])

                else :
                    exclu_puzzle.append(data_zone_puzzle[i])

            for i in range(len(data_zone_puzzle)):
                if not(contains(data_zone_puzzle_[i][0], [j[0] for j in data_zone_puzzle])):
                    exclu_puzzle_.append(data_zone_puzzle_[i])

                data_zone_puzzle_[i] = pc.piece(np.array(data_zone_puzzle_[i][0]), data_zone_puzzle_[i][1], 0, self.pss)

            for i in range(len(data_zone_puzzle)):
                data_zone_puzzle[i] = pc.piece(np.array(data_zone_puzzle[i][0]), data_zone_puzzle[i][1], 0, self.pss)

            print(exclu_puzzle, exclu_puzzle_)
            for i in range (len(exclu_puzzle)):
                exclu_puzzle[i] = pc.piece(np.array(exclu_puzzle[i][0]), exclu_puzzle[i][1], 0, self.pss)

                for j in range(len(puzzle_.conf)):
                    if (exclu_puzzle[i].data == puzzle_.conf[j].data).sum() == 4:
                        index_exclu_puzzle_.append(j)

            for i in range(len(exclu_puzzle_)):
                exclu_puzzle_[i] = pc.piece(np.array(exclu_puzzle_[i][0]), exclu_puzzle_[i][1], 0, self.pss)

                for j in range(len(puzzle.conf)):
                    if (exclu_puzzle_[i].data == puzzle.conf[j].data).sum() == 4:
                        index_exclu_puzzle.append(j)


        for i in range(self.pss ** 2):
            if i in index_exclu_puzzle_:
                hybr_.append(exclu_puzzle_.pop(0))

            elif x2 <= (i % self.pss) < x2 + leng and y2 <= (i // self.pss) < y2 + wid:
                hybr_.append(data_zone_puzzle.pop(0))

            else:
                hybr_.append(puzzle_.conf[i])

        for i in range(self.pss ** 2):
            if i in index_exclu_puzzle:
                hybr.append(exclu_puzzle.pop(0))

            elif x1 <= (i % self.pss) < x1 + leng and y1 <= (i // self.pss) < y1 + wid:
                hybr.append(data_zone_puzzle_.pop(0))

            else:
                hybr.append(puzzle.conf[i])

        print(x1,y1,leng,wid,x2,y2,index_exclu_puzzle, index_exclu_puzzle)
        return pz.puzzle(self.pss, hybr, aleatoire = False), pz.puzzle(self.pss, hybr_, aleatoire = False)

    def evolution(self,  gc_sample = int, elitism_rate = float, nb_new_gen = int, mu_rot_rate = float, mu_swap_rate = float):
        new_gen = np.empty(0, dtype = pz.puzzle)
        
        for i in range(nb_new_gen):
            np.append(self.hybrydation(gc_sample))

        for i in range(int(mu_rot_rate * nb_new_gen)):
            new_gen[rd.randrange(nb_new_gen)].mutation_rotation()

        for j in range(int(mu_swap_rate * nb_new_gen)):
            new_gen[rd.randrange(nb_new_gen)].mutation_swap()

        self.ps = np.concatenate(self.ps[self.rank_tab[:int(self.s * elitism_rate)]], new_gen[:ng_rank[:int(self.s (1 - elitism_rate))]])

    def best_render(self):
        self.ps[self.r[0]].render()
        print(self.ps[self.r[0]].eval)

