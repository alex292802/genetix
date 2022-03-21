import numpy as np
import random as rd
import puzzle as pz
import puzzle_samples as pzs
import Parser as pr

#On récupére le puzzle à l'aide du Parser
data=pr.parse("benchEternity2.txt")

#On transforme la data en une liste de liste
pi = np.array([np.array(i) for i in data])


obj = pzs.puzzle_sample(10, 4, pieces = pi)

obj.ps[0].render()
obj.ps[1].render()

a, b = obj.hybrydation(obj.ps[0], obj.ps[1])

a.render()
b.render()

'''print(obj.r,obj.fit)
obj.best_render()

pu = pz.puzzle(16, pi)
#pu.render()
pu.mutation_swap()
#pu.render()

'''