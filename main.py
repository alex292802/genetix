import numpy as np
import random as rd
import puzzle as pz
import puzzle_samples as pzs
import Parser as pr

#On récupére le puzzle à l'aide du Parser
data=pr.parse("benchEternity2.txt")
#On transforme la data en une liste de liste
pi = np.array([np.array(i) for i in data])
for i in range(len(pi)):
    print(pi[i])

obj = pz.puzzle(16, pieces = pi)
obj.render()

'''print(obj.r,obj.fit)
obj.best_render()

pu = pz.puzzle(16, pi)
#pu.render()
pu.mutation_swap()
#pu.render()

'''