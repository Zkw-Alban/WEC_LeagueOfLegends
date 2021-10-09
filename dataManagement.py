# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:02:44 2021

@author: zkw, lepercq, louesdon
"""

import os
import csv
from datetime import date
from riotwatcher import LolWatcher
import Fonctions as fc


## 1 - Initialisation
os.chdir(r"D:\Antoine\CNAM\3A\WEC")
SUMMONERNAME = r"0 5 A"
lol_watcher = LolWatcher('RGAPI-1497b4c3-048f-4d37-b2f6-c397facefde7')
QUEUE = 420 #soloQ
NBGAMES = 3 #nb de parties à ramener à chaque requête
NBMAXPLAYER = 1000 #= nb max de joueurs dans la liste
NEWLIST = False #False=reprend la liste enregistrée et l'aggrandi jusqu'a NBMAXPLAYER si True=repars de 0.


## 2 - On récupère la liste des joueurs puis les infos de leurs parties
# et on stock ces parties dans des fichiers csv
# on peut repartir du fichier CSV si on veut pas requêter de nouveaux joueurs

if NEWLIST:
    playerList = []
else:
    with open('listPUUID.csv', newline='') as f:
        playerList = list(csv.reader(f))[0]

playerList = []
playerList = fc.getPlayerList(SUMMONERNAME, playerList, QUEUE, NBGAMES, NBMAXPLAYER, lol_watcher)

#On exporte la liste des joueurs
with open("listPUUID.csv", 'w', newline='') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL).writerow(playerList)
        
#on peut repartir du fichier CSV si on veut pas requêter de nouveaux joueurs
with open('listPUUID.csv', newline='') as f:
    playerList = list(csv.reader(f))[0]

## 3 - On récupère les données des parties de joueurs
matchListHistory = []
today = date.today().strftime("%Y-%m-%d")
for i,p in enumerate(playerList):
    chemin_export = "sampleGameData/" + today + "_tonsOfData" + p
    matchListHistory = fc.tonsOfData(p, QUEUE, NBGAMES, chemin_export,
                                     lol_watcher, matchListHistory)
    print(str(round(i/len(playerList)*100,2))+" % des parties chargées.")

## on garde la liste des match étudiés dans un fichier csv
with open("matchListHistory.csv", 'w', newline='') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(matchListHistory)
      