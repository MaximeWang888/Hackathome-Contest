#===================================================================#
#-------------------------------------------------------------------#
#                        Hackathome Contest                         #
#-------------------------------------------------------------------#
#*******************************************************************#
#   V0.1.1       Audic Xu, Maxime Wang  - 02/04/21                  #
#                                                                   #
#===================================================================#


#--------------------------------------------#
#          Importation des packages          #
#--------------------------------------------#
import csv
import xlsxwriter

#--------------------------------------------#
#                    Code                    #
#--------------------------------------------#

#--------------------------------------------#
#   Créer une liste de tous les serveurs     #
#--------------------------------------------#
def création_serveurs(file_name): # 'servers_catalog.csv'
	lst_serveurs = []
	with open(file_name, newline='') as csvfile:
	    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    spamreader = list(spamreader)
	    for i in range(len(spamreader)):
	        lst_serveurs.append(spamreader[i][0].split(","))
	return lst_serveurs	


#--------------------------------------------#
#   Créer une liste de tous les services     #
#--------------------------------------------#
def création_services(file_name): # 'ctstfr0280_input_2.csv'
	lst_services = []
	with open(file_name, newline='') as csvfile:
	    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    spamreader = list(spamreader)
	    n = int(spamreader[0][0])
	    for i in range(1, len(list(spamreader))):
	        lst_services.append(spamreader[i][0].split(","))
	return lst_services, n	


#--------------------------------------------#
#    Passe les donnéees de String en int     #
#--------------------------------------------#
def passageStringToInt(lst_serveurs, lst_services): 
	for i in range(1, len(lst_serveurs)):
	    for j in range(1, len(lst_serveurs[i])):
	        lst_serveurs[i][j] = int(lst_serveurs[i][j])

	for i in range(len(lst_services)):
	    for j in range(1, len(lst_services[i])):
	        lst_services[i][j] = int(lst_services[i][j])

#--------------------------------------------#
#    Passe les donnéees de String en int     #
#--------------------------------------------#
# Création d'un dictionnaire
def creer_dico(lst_serveurs):
    dico = {}
    for i in range(1, len(lst_serveurs)):
        dico[lst_serveurs[i][0]] = [[], [0, 0, 0]]

    return dico

#--------------------------------------------------------------------------------------#
# Le score pour chaque liste de services est la somme des émissions en GES de chaque   #
# serveur de votre solution. Plus le score est faible, meilleure sera votre solution   #
#                     Renvoi l'indice du serveur le plus apte                          #
#--------------------------------------------------------------------------------------#
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


#----------------------------------------------------------------------------------------------#
#    Permet de nous indiquer si le service peut-être attribué au serveur passé en paramètre    #
#----------------------------------------------------------------------------------------------#
def plusGrandQueCapaMaximal(dico, lst_service, lst_serveur):

    # Si la valeur du dico ajouté à la valeur du service est inférieur à la valeur du serveur 
    # Exemple : Serveur > dico + service
    if lst_serveur[3] > dico[lst_serveur[0]][1][0] + lst_service[1] and \
     lst_serveur[4] > dico[lst_serveur[0]][1][1] + lst_service[2] and \
     lst_serveur[5] > dico[lst_serveur[0]][1][2] + lst_service[3]:
        return True

    # Dans le cas contraire retourne false
    else:
        return False



#--------------------------------------------#
#                    MAIN                    #
#--------------------------------------------#

lst_serveurs = création_serveurs('servers_catalog.csv')

lst_services, n = création_services('ctstfr0280_input_6.csv') 

passageStringToInt(lst_serveurs, lst_services)

# Création du dictionnaire
dico = creer_dico(lst_serveurs)

# Listes des serveurs compatibles avec un service
lst = []

# Listes des services non attribués
lst_services_non_attribuer = []

# Rechercher pour chaque service le serveur le plus adaptée et l'ajouté à lst 
for service in lst_services:

    plusDeServeur = False
    stockage = service[1]
    ram = service[2]
    cpu = service[3]
    lst = [service[0]]

    for i in range(1, len(lst_serveurs)):

        if lst_serveurs[i][3] != "disk":
            modele_stockage = lst_serveurs[i][3]
            modele_ram = lst_serveurs[i][4]
            modele_cpu = lst_serveurs[i][5]
            if stockage <= modele_stockage and ram <= modele_ram and cpu <= modele_cpu:
                lst.append(lst_serveurs[i])
            
    # Tant que l'addition du dico et du service dépasse la capicité du serveur 
    while not plusGrandQueCapaMaximal(dico, service, lst[score(lst)]):
        lst.remove(lst[score(lst)])
        if len(lst) <= 1:
            plusDeServeur = True
            break

    if plusDeServeur:
        lst_services_non_attribuer.append(service[0])
    else:
        dico[lst[score(lst)][0]][0].append(service[0])
        dico[lst[score(lst)][0]][1][0] += stockage
        dico[lst[score(lst)][0]][1][1] += ram
        dico[lst[score(lst)][0]][1][2] += cpu


# Indice de la ligne lors de l'insertion des données dans Excel 
i = 0

# Create file (workbook) and worksheet
ourWorkbook = xlsxwriter.Workbook("output6.csv")
outSheet = ourWorkbook.add_worksheet()

# Write data to file
for element in dico:
	string_service = ""
	outSheet.write(i, 0, element)
	for service in dico[element][0]:
		string_service += service
		if service != dico[element][0][-1]:
		   string_service += ", "

	outSheet.write(i, 1, string_service)
	i += 1

ourWorkbook.close()