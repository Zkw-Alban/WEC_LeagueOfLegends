import os
import csv
from datetime import date
from riotwatcher import LolWatcher
import Fonctions as fc


## 1 - Initialisation
os.chdir(os.getcwd())
SUMMONERNAME = r"Oups ça a craqué"
lol_watcher = LolWatcher('RGAPI-1497b4c3-048f-4d37-b2f6-c397facefde7')
QUEUE = 420 #soloQ
NBGAMES = 5 #nb de parties à ramener à chaque requête
#NBMAXPLAYER = 1000 #= nb max de joueurs dans la liste

#-----------------------------------------------------------------------------------------------------------------------
#on peut repartir du fichier CSV si on veut pas requêter de nouveaux joueurs
with open('listPUUID.csv', newline='') as f:
    playerList = list(csv.reader(f))[0]

path = os.getcwd()

## 3 - On récupère les données des parties de joueurs
matchListHistory = []
today = date.today().strftime("%Y-%m-%d")
for i,p in enumerate(playerList):
    chemin_export = "samplegamedata/" + today + "_tonsOfData" + p
    matchListHistory = fc.tonsOfData(p, QUEUE, NBGAMES, chemin_export,
                                     lol_watcher, matchListHistory)
    playerList.remove(p)
    with open("listPUUID.csv", 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(playerList)
    print(str(round(i/len(playerList)*100,2))+" % des parties chargées.")


## on garde la liste des match étudiés dans un fichier csv
#with open("matchListHistory.csv", 'w', newline='') as f:
#    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
#    wr.writerow(matchListHistory)
      