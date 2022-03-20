import numpy as np


class piece:

    def __init__(self, borders=np.ndarray, rotation=int, no=int, psize=int):
        self.type = (borders[:4] == 0).sum()

        self.data = borders[0] + borders[1] * 100 + borders[0] *10000 + borders[0] *10000000
        self.nord = borders[rotation]
        self.est = borders[(rotation + 1) % 4]
        self.sud = borders[(rotation + 2) % 4]
        self.ouest = borders[(rotation + 3) % 4]

        self.x = no % psize
        self.y = no // psize

    def rotate(self):
        x = self.ouest
        self.ouest = self.sud
        self.sud = self.est
        self.est = self.nord
        self.nord = x