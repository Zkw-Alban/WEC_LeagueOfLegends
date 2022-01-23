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
SUMMONERNAME = r"BOUCHER NOIR"
lol_watcher = LolWatcher('RGAPI-1497b4c3-048f-4d37-b2f6-c397facefde7')
QUEUE = 420 #soloQ
NBGAMES = 3 #nb de parties à ramener à chaque requête
NBMAXPLAYER = 300 #= nb max de joueurs dans la liste
NEWLIST = True #False=reprend la liste enregistrée et l'aggrandi jusqu'a NBMAXPLAYER si True=repars de 0.


## 2 - On récupère la liste des joueurs puis les infos de leurs parties
# et on stock ces parties dans des fichiers csv
# on peut repartir du fichier CSV si on veut pas requêter de nouveaux joueurs

if NEWLIST:
    playerList = []
else:
    with open('listPUUID.csv', newline='', encoding='UTF8') as f:
        playerList = list(csv.reader(f))[0]

playerList = []
playerList = fc.getPlayerList(SUMMONERNAME, playerList, QUEUE, NBGAMES, NBMAXPLAYER, lol_watcher)

## 3 - On exporte la liste des joueurs
with open("listPUUID.csv", 'w', newline='', encoding='UTF8') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL).writerow(playerList)