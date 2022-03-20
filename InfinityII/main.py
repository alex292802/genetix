import numpy as np
import random as rd
import puzzle as pz
import puzzle_samples as pzs
import Parser as pr

data = pr.parse("C://Users//gviol//genetix//InfinityII//init.txt")
pi = np.array([np.array(i) for i in data])
obj = pzs.puzzle_sample(10, 16, pieces = pi)
print(obj.r,obj.fit)
obj.best_render()

pu = pz.puzzle(2, pi)
pu.render()
pu.mutation_swap()
pu.render()