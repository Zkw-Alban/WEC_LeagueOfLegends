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
os.chdir(os.getcwd())
SUMMONERNAME = r"BOUCHER NOIR"
API_KEY = 'key'
lol_watcher = LolWatcher(API_KEY)
QUEUE = 420 #soloQ
NBGAMES = 5 #nb de parties à ramener à chaque requête

## 2 - Lecture liste des joueurs
with open('listPUUID.csv', newline='', encoding='UTF8') as f:
    playerList = list(csv.reader(f))[0]
    
path = os.getcwd()

## 3 - On récupère les données des parties de joueurs
matchListHistory = []
today = date.today().strftime("%Y-%m-%d")
for i,p in enumerate(playerList):
    chemin_export = "sampleGameData/" + today + "_tonsOfData" + p
    matchListHistory = fc.tonsOfData(p, QUEUE, NBGAMES, chemin_export,
                                     lol_watcher, matchListHistory)
    print(str(round(i/len(playerList)*100,2))+" % des parties chargées.")
