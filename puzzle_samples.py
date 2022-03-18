import puzzle as pz
import numpy as np
import random as rd

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

    def hybrydation(self, sample_size):


        return

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

