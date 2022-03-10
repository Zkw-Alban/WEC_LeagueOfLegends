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

def championName2(championName):    
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
    return newName

def requestLiveGameData(URL):
    """Renvoie le fichier JSON associé à la game en cours"""
    return requests.get(URL, verify=False).json()


def getGameInfo(gameData, lol_watcher, root):
    """Renvoie dans une liste toutes les infos utiles d'une game"""
    playerList = []
    championNameList = []
    positionList = []
    skinList = []
    teamList = []
    championIdList = []
    championWinrateList = []
    tiles = root+"/ressources/dataDragon/img/champion/tiles/"
    #Infos depuis le Client
    for i in range(10):
        with open(root+"/ressources/dataDragon/12.1.1/data/fr_FR/champion/"+championName2(gameData['allPlayers'][i]['championName'])+".json", encoding='utf-8') as json_file:
            championInfo = json.load(json_file)
        playerList.append(gameData['allPlayers'][i]['summonerName'])
        championNameList.append(gameData['allPlayers'][i]['championName'])
        positionList.append(gameData['allPlayers'][i]['position'])
        teamList.append(gameData['allPlayers'][i]['team'])
        championIdList.append(championInfo["data"][championName2(str(championNameList[-1]))]['key'])
        skinList.append(tiles+championName2(gameData['allPlayers'][i]['championName'])+"_"+str(gameData['allPlayers'][i]['skinID'])+".jpg")
        #Gestion des chromas qui ont un skin id différent mais pas d'image spécifique
        if not os.path.isfile(skinList[-1]):
            skinList[-1] = tiles+gameData['allPlayers'][i]['championName']+"_"+str(0)+".jpg"

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
            championWinrateList.append(fc.getPlayerStatsOnChampion(gameData['allPlayers'][i]['summonerName'], gameData['allPlayers'][i]['championName'])[1])
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
                "Rank_0": rankList[0],
                "Rank_1": rankList[1],
                "Rank_2": rankList[2],
                "Rank_3": rankList[3],
                "Rank_4": rankList[4],
                "Rank_5": rankList[5],
                "Rank_6": rankList[6],
                "Rank_7": rankList[7],
                "Rank_8": rankList[8],
                "Rank_9": rankList[9],
                "winrateOnChampion_": championWinrateList[0],
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
