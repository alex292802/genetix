def parse(char):
    text_file = open(char, "r")
    data = text_file.read()
    text_file.close()
    data = data.split("\n")  # On sépare chaque ligne d'information pour les mettre dans une liste

    def intl(lis):  # pour avoir des entiers en valeur
        for i in range(len(lis)):
            #print(int(lis[i]))
            lis[i] = int(lis[i])
        return lis

    for i in range(len(data)):
        data[i] = intl(data[i].split(" "))  # On sépare chaque chiffre d'une ligne d'information pour les mettre dans une sous-liste

    return data[4:]