# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:55:58 2021

@author: antoine
"""

import os
import json
import requests
import numpy as np
import Fonctions as fc

os.chdir(os.getcwd())

def championName2(championName):
    """transforme le nom du champion pour qu'il soit harmonisé partout"""
    if "'" in championName:
        championName = championName.replace("'","")
    if "." in championName:
        championName = championName.replace(".","")
    if " " in championName:
        championName = championName.replace(" ","") 
    newName = championName
    if championName == "Wukong":
        newName = "MonkeyKing"
    elif championName == "ChoGath":
        newName = "Chogath"
    elif championName.startswith('Ma') and championName.endswith('Yi'):
        newName = "MasterYi"
    elif championName == "KaiSa":
        newName = "Kaisa"
    elif championName == "LeBlanc":
        newName = "Leblanc"
    elif championName == "Zeri":
        newName = "Zoe"
    return newName

def getChampionList():
    """récupère la liste des noms de tous les champions du jeu pour le patch en cours"""
    file = open(os.getcwd()+"/ressources/dataDragon/12.1.1/data/en_GB/champion.json",'r',encoding="utf-8")
    jsonn = json.load(file)
    championList = []
    for elemen in jsonn["data"]:
        championList.append(jsonn["data"][elemen]["name"])
    championList.sort()
    return championList
    
def requestLiveGameData(URL):
    """Renvoie le fichier JSON associé à la game en cours"""
    return requests.get(URL, verify=False).json()


def getGameInfo(playerList, championNameList, lol_watcher):
    """Renvoie dans une liste toutes les infos utiles d'une game"""
    #playerList = []
    #championNameList = []
    positionList = []
    skinList = []
    teamList = []
    championIdList = []
    championWinrateList = []
    tiles = "ressources/dataDragon/img/champion/tiles/"
    #Infos depuis le Client
    for i in range(10):
        with open("ressources/dataDragon/12.1.1/data/fr_FR/champion/"+championName2(championNameList[i])+".json", encoding='utf-8') as json_file:
            championInfo = json.load(json_file)
        playerList.append(playerList[i])
        championNameList.append(championNameList[i])
        positionList.append(i)
        if i < 5:
            teamList.append(100)
        else:
            teamList.append(200)
        championIdList.append(championInfo["data"][championName2(str(championNameList[-1]))]['key'])
        skinList.append(tiles+championName2(championNameList[i]+"_0")+".jpg")

    eloList = []
    rankList = []
    streakList = []
    winrateList = []
    championWinrateList = []

    for i, p in enumerate(playerList):
        teamList.append(100)
        summonerInfo = fc.requestSummonerData(p, lol_watcher)
        #On vérifie que le summoner est un joueur
        if summonerInfo:
            championWinrateList.append(fc.getPlayerStatsOnChampion(playerList[i], championNameList[i])[1])
            summonerRanked = fc.requestRankedData(summonerInfo['id'], lol_watcher)
            #On vérifie que le summoner a joué en ranked
            if summonerRanked:
                #On vérifie que les soloQ sont en 1ère position
                if summonerRanked[0]['queueType'] == "RANKED_SOLO_5x5":
                    eloList.append(fc.getElo(summonerRanked[0]['tier'], fc.getRank(summonerRanked[0]['rank'])))
                    rankList.append(summonerRanked[0]['tier']+" "+summonerRanked[0]['rank'])
                    if summonerRanked[0]['hotStreak']:
                        streakList.append(1)
                    else:
                        streakList.append(0)
                    #il faut que le joueur ait joué au moins 10 parties et en soloQ
                    if (summonerRanked[0]['wins'] + summonerRanked[0]['losses']) > 10 :
                        winrateList.append(round(summonerRanked[0]['wins']/(summonerRanked[0]['wins'] + summonerRanked[0]['losses']),2))
                    else: 
                        winrateList.append(0.5)
                #On vérifie que les soloQ sont en 2e position
                elif len(summonerRanked)>1:
                    eloList.append(fc.getElo(summonerRanked[1]['tier'], fc.getRank(summonerRanked[1]['rank'])))
                    rankList.append(summonerRanked[1]['tier']+" "+summonerRanked[1]['rank'])
                    if summonerRanked[1]['hotStreak']:
                        streakList.append(1)
                    else:
                        streakList.append(0)
                    #il faut que le joueur ait joué au moins 10 partie
                    if (summonerRanked[1]['wins'] + summonerRanked[1]['losses']) > 10 : 
                        winrateList.append(round(summonerRanked[1]['wins']/(summonerRanked[1]['wins'] + summonerRanked[1]['losses']),2))
                    else: 
                        winrateList.append(0.5)
                #Le joueur n'a pas joué en soloQ
                else:
                    eloList.append(19)
                    rankList.append("No SoloQ Data")
                    winrateList.append(0.5)
                    streakList.append(0)
            #Le joueur n'a pas joué en ranked
            else:
                eloList.append(19)
                rankList.append("No Ranked Data")
                winrateList.append(0.5)
                streakList.append(0)
        #Ce n'est pas un joueur
        else:
            eloList.append(19)
            rankList.append("Not a player")
            winrateList.append(0.5)
            streakList.append(0)
            championWinrateList.append(50)
            
    eloDiff = np.sum(eloList[0:5])-np.sum(eloList[5:10])
    
    rankList_tmp = rankList
        
    rankList = [17 if r in ("Not a player", "No Ranked Data", "No SoloQ Data") else r for r in rankList]

    liveData = {"Champion_0": championIdList[0],
                "Champion_1": championIdList[1],
                "Champion_2": championIdList[2],
                "Champion_3": championIdList[3],
                "Champion_4": championIdList[4],
                "Champion_5": championIdList[5],
                "Champion_6": championIdList[6],
                "Champion_7": championIdList[7],
                "Champion_8": championIdList[8],
                "Champion_9": championIdList[9],
                "Rank_0": eloList[0],
                "Rank_1": eloList[1],
                "Rank_2": eloList[2],
                "Rank_3": eloList[3],
                "Rank_4": eloList[4],
                "Rank_5": eloList[5],
                "Rank_6": eloList[6],
                "Rank_7": eloList[7],
                "Rank_8": eloList[8],
                "Rank_9": eloList[9],
                "winrateOnChampion_0": championWinrateList[0],
                "winrateOnChampion_1": championWinrateList[1],
                "winrateOnChampion_2": championWinrateList[2],
                "winrateOnChampion_3": championWinrateList[3],
                "winrateOnChampion_4": championWinrateList[4],
                "winrateOnChampion_5": championWinrateList[5],
                "winrateOnChampion_6": championWinrateList[6],
                "winrateOnChampion_7": championWinrateList[7],
                "winrateOnChampion_8": championWinrateList[8],
                "winrateOnChampion_9": championWinrateList[9],
                "winratePlayer_0": winrateList[0],
                "winratePlayer_1": winrateList[1],
                "winratePlayer_2": winrateList[2],
                "winratePlayer_3": winrateList[3],
                "winratePlayer_4": winrateList[4],
                "winratePlayer_5": winrateList[5],
                "winratePlayer_6": winrateList[6],
                "winratePlayer_7": winrateList[7],
                "winratePlayer_8": winrateList[8],
                "winratePlayer_9": winrateList[9],
                }

    winrateList = [round(e*100,2) for e in winrateList]
    rankList = rankList_tmp
    
    displayInfo = [championNameList, skinList, rankList, winrateList, streakList]
    return liveData, displayInfo

def championName(championName):
    """Renvoie le nom du champion corrigé"""
    if "'" in championName:
        championName = championName.replace("'","")
    if "." in championName:
        championName = championName.replace(".","")
    if " " in championName:
        championName = championName.replace(" ","") 
    newName = championName
    if championName == "Wukong":
        newName = "MonkeyKing"
    elif championName == "ChoGath":
        newName = "Chogath"
    return newName
