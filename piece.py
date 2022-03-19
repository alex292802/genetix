import numpy as np


class piece:
    #borders : pièce en question
    #psize : taille du puzzle
    #rotation : de combien ou tourne la pièce 
    #no : numéro de la pièce 
    def __init__(self, borders=np.ndarray, rotation=int, no=int, psize=int):
        
        self.data = borders 
        self.nord = borders[rotation]
        self.est = borders[(rotation + 1) % 4]
        self.sud = borders[(rotation + 2) % 4]
        self.ouest = borders[(rotation + 3) % 4]
        #coordonnées en x et y de la pièce
        self.x = no % psize
        self.y = no // psize
        #si cat vaut 2 c'est un coin, si cat vaut 1 c'est un bord, sinon c'est une pièce du milieu 
        self.cat = (borders==0).sum()

    def rotate(self):
        #Tourne la pièce dans le sens trigonomètrique 
        x = self.ouest
        self.ouest = self.sud
        self.sud = self.est
        self.est = self.nord
        self.nord = x

