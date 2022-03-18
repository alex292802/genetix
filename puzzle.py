import random as rd
import numpy as np
import piece as pc


class puzzle:
    
    #pieces représente le puzzle complet 
    def __init__(self, size=int, pieces=np.ndarray):
        #On récupére la taille du puzzle 
        self.s = size
        
        # Notre nouvelle configuration de puzzle :
        new_conf = np.empty(0, dtype=pc.piece)
        
        #On crée une liste des indices correspondant à chaque pièce et on la mélange 
        in_coins = [0,1,2,3]
        in_bords = [i for i in range(4,60)]
        in_milieu = [i for i in range(60, 256)]
    
        
        np.random.shuffle(in_coins)
        np.random.shuffle(in_bords)
        np.random.shuffle(in_milieu)
        
        #On crée une nouvelle configuration en prenant aléatoirement une nouvelle pièce, on la tourne aléatoirement
        for i in range(256):
            
            if i in [i for i in range(1,15)]:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 0, new_conf.size, self.s))
                
            elif i in [i*16+15 for i in range(1,15)]:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 3, new_conf.size, self.s))
                    
            elif i in [i for i in range(241,255)]:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 2, new_conf.size, self.s))
                
            elif i in [i*16 for i in range(1,15)]:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_bords.pop()]), 1, new_conf.size, self.s))
                
            elif i == 0:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 1, new_conf.size, self.s))
                
            elif i == 15:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 0, new_conf.size, self.s))
            
            elif i == 255:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 3, new_conf.size, self.s))
                    
            elif i == 240:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_coins.pop()]), 2, new_conf.size, self.s))
                
            else:
                new_conf = np.append(new_conf, pc.piece(np.array(pieces[in_milieu.pop()]), rd.randrange(4), new_conf.size, self.s))

        self.conf = new_conf
        for i in range(15):
            print(self.conf[i].nord)
        self.eval = self.evaluation()

    #On échange 2 pièces à partir de leurs indices 
    def mutation_swap(self):
        a,b = rd.randrange(self.s**2),rd.randrange(self.s**2)
        self.conf[b],self.conf[a] = self.conf[a],self.conf[b]
    
    #On tourne la pièce une fois dans le sens trigonomètrique 
    def mutation_rotation(self):
        a = rd.randrange(self.s**2)
        self.conf[a].rotate()
        
    #On évalue le score de notre config 
    def evaluation(self):
        score = 0
        score_ = 0
        
        #On regarde chaque pièce 
        for piece in self.conf:
            #Si la pièce est sur le bord supérieur
            if piece.y == 0:
                #Si le haut de la pièce correspond à une bordure 
                score += int(piece.nord == 0)
                score_ += int(piece.nord != 0)
                
            else:
                #On récupère la pièce d'au dessus :
                piece_ = self.conf[piece.x + self.s * (piece.y - 1)]
                #On compare le sud de la pièce d'au dessus avec le nord de la pièce qui nous intéresse
                score += int(piece.nord == piece_.sud and piece.nord != 0)
                score_ += int(piece.nord != piece_.sud or piece.nord == 0)
            
            #Si la pièce est sur le bord inférieur
            if piece.y == self.s - 1:
                #Si le bas de la pièce correspond à une bordure 
                score += int(piece.sud == 0)
                score_ += int(piece.sud != 0)

            #Si la pièce est sur le bord gauche
            if piece.x == 0:
                #Si la gauche de la pièce correspond à une bordure
                score += int(piece.ouest == 0)
                score_ += int(piece.ouest != 0)

            else:
                piece__ = self.conf[piece.x - 1 + self.s * piece.y]
                score += int(piece.ouest == piece__.est and piece.ouest != 0)
                score_ += int(piece.ouest != piece__.est or piece.ouest == 0)
            
            #Si la pièce est sur le bord droit 
            if piece.x == self.s - 1:
                #Si la droite de la pièce correspond à une bordure
                score += int(piece.est == 0)
                score_ += int(piece.est != 0)
                
        return score_
    

    #Affichage de la configuration 
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
