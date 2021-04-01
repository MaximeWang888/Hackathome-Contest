import csv
lst_serveur = []
with open('servers_catalog.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    spamreader = list(spamreader)
    for i in range(len(spamreader)):
        lst_serveur.append(spamreader[i][0].split(","))


lst_input = []
with open('ctstfr0280_input_6.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    spamreader = list(spamreader)
    n = int(spamreader[0][0])
    for i in range(1, len(list(spamreader))):
        lst_input.append(spamreader[i][0].split(","))


# passe de string en int
for i in range(1, len(lst_serveur)):
    for j in range(1, len(lst_serveur[i])):
        lst_serveur[i][j] = int(lst_serveur[i][j])

for i in range(len(lst_input)):
    for j in range(1, len(lst_input[i])):
        lst_input[i][j] = int(lst_input[i][j])


def score(lst):
    Score = 0
    SmallerScore = float("inf")
    SmallestScoreIdx = 0
    for i in range(1, len(lst)):
        Score = lst[i][1] + n * lst[i][2]
        if SmallerScore > Score:
            SmallerScore = Score
            smallestScoreIdx = i
    return smallestScoreIdx


def creer_dico(lst_serveur):
    dico = {}
    for i in range(1, len(lst_serveur)):
        dico[lst_serveur[i][0]] = [[], [0, 0, 0], 0]

    return dico


def pgq(dico, lst_input, lst_serveur):
#plus grand que

    if dico[lst[score(lst)][0]][2] == 1:
        return False
    if lst_serveur[3] > dico[lst_serveur[0]][1][0] + lst_input[1] and lst_serveur[4] > dico[lst_serveur[0]][1][1] + lst_input[2] and lst_serveur[5] > dico[lst_serveur[0]][1][2] + lst_input[3]:
        dico[lst_serveur[0]][1][0] += lst_input[1]
        dico[lst_serveur[0]][1][1] += lst_input[2]
        dico[lst_serveur[0]][1][2] += lst_input[3]
        return True
    else:
        return False


dico = creer_dico(lst_serveur)


lst = []
for i in range(len(lst_input)):
    stockage = lst_input[i][1]
    ram = lst_input[i][2]
    cpu = lst_input[i][3]
    lst = [lst_input[i][0]]
    for ii in range(1, len(lst_serveur)):
        if lst_serveur[ii][3] != "disk":
            modele_stockage = lst_serveur[ii][3]
            modele_ram = lst_serveur[ii][4]
            modele_cpu = lst_serveur[ii][5]
            if stockage <= modele_stockage and ram <= modele_ram and cpu <= modele_cpu:
                lst.append(lst_serveur[ii])

    while pgq(dico, lst_input[i], lst_serveur[ii]):
        dico[lst[score(lst)][0]][2] = 1


    dico[lst[score(lst)][0]][0].append(lst_input[i])
    dico[lst[score(lst)][0]][1][0] += stockage
    dico[lst[score(lst)][0]][1][1] += ram
    dico[lst[score(lst)][0]][1][2] += cpu


with open('fichier1.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for x in dico:
        if len(dico[x][0]) > 0:
            if len(dico[x][0]) > 0:
                print(x, dico[x][0][0][0])
                spamwriter.writerow(x)


with open('fichier2.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for x in dico:
        if len(dico[x][0]) > 0:
            if len(dico[x][0]) > 0:
                print(x, dico[x][0][0][0])
                spamwriter.writerow(dico[x][0][0][0])

















#
