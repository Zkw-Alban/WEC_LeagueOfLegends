# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:55:58 2021

@author: antoine
"""

import os
import json
import requests
import Fonctions as fc



def requestLiveGameData(URL):
    """Renvoie le fichier JSON associé à la game en cours"""
    return requests.get(URL, verify=False).json()


def getGameInfo(gameData, lol_watcher):
    """Renvoie dans une liste toutes les infos utiles d'une game"""
    playerList = []
    championNameList = []
    positionList = []
    skinList = []
    teamList = []
    championIdList = []
    tiles = "/ressources/dataDragon/img/champion/tiles/"
    patch = "patch 11.17"
    matchId = "id du match"
    win = 100

    #Infos depuis le Client
    for i in range(10):
        with open("/ressources/dataDragon/11.18.1/data/fr_FR/champion/"+gameData['allPlayers'][i]['championName']+".json") as json_file:
            championInfo = json.load(json_file)
        playerList.append(gameData['allPlayers'][i]['summonerName'])
        championNameList.append(gameData['allPlayers'][i]['championName'])
        positionList.append(gameData['allPlayers'][i]['position'])
        teamList.append(gameData['allPlayers'][i]['team'])
        championIdList.append(championInfo["data"][str(championNameList[-1]).replace("î","i")]['key'])
        if gameData['allPlayers'][i]['championName'] == "Maître Yi":
            skinList.append(tiles+"Maitre Yi"+"_"+str(gameData['allPlayers'][i]['skinID'])+".jpg")
        else:
            skinList.append(tiles+gameData['allPlayers'][i]['championName']+"_"+str(gameData['allPlayers'][i]['skinID'])+".jpg")
        #Festion des chromas qui ont un skin id différent mais pas d'image spécifique
        if not os.path.isfile(tiles+"Maitre Yi"+"_"+str(gameData['allPlayers'][i]['skinID'])+".jpg"):
            skinList[i] = tiles+gameData['allPlayers'][i]['championName']+"_"+str(0)+".jpg"

    eloList = []
    rankList = []
    streakList = []
    winrateList = []

    for i,p in enumerate(playerList):
        teamList.append(100)
        summonerInfo = fc.requestSummonerData(p, lol_watcher)
        #On vérifie que le summoner est un joueur
        if summonerInfo:
            summonerRanked = fc.requestRankedData(summonerInfo['id'], lol_watcher)
            #On vérifie que le summoner a joué en ranked
            if summonerRanked:
                #il faut que le joueur ait joué au moins 10 parties et en soloQ
                if summonerRanked[0]['queueType'] == "RANKED_SOLO_5x5":
                    eloList.append(fc.getElo(summonerRanked[0]['tier'], fc.getRank(summonerRanked[0]['rank'])))
                    if summonerRanked[0]['hotStreak']:
                        streakList.append(1)
                    else:
                        streakList.append(0)
                    if (summonerRanked[0]['wins'] + summonerRanked[0]['losses']) > 10 :
                        winrateList.append(round(summonerRanked[0]['wins']/(summonerRanked[0]['wins'] + summonerRanked[0]['losses']),2))
                    else: winrateList.append(0.5)
                else:
                    eloList.append(fc.getElo(summonerRanked[1]['tier'], fc.getRank(summonerRanked[1]['rank'])))
                    if summonerRanked[1]['hotStreak']:
                        streakList.append(1)
                    else:
                        streakList.append(0)
                    if (summonerRanked[1]['wins'] + summonerRanked[1]['losses']) > 10 : #il faut que le joueur ait joué au moins 10 partie
                        winrateList.append(round(summonerRanked[1]['wins']/(summonerRanked[1]['wins'] + summonerRanked[1]['losses']),2))
                    else: winrateList.append(0.5)
            else:
                eloList.append(19)
                rankList.append("No Data")
                streakList.append(False)
                winrateList.append(50)
        else:
            eloList.append(19)
            rankList.append("Not a player")
            winrateList.append(50)
            streakList.append(False)

    liveData = {"Rank_0": eloList[0], "streak_0": streakList[0],
                "winratePlayer_0": winrateList[0], "Team_0": teamList[0],
                "Champion_0": championIdList[0], "Position_0": positionList[0],
              "Rank_1": eloList[1], "streak_1": streakList[1],
              "winratePlayer_1": winrateList[1], "Team_1": teamList[1],
              "Champion_1": championIdList[1], "Position_1": positionList[1],
              "Rank_2": eloList[2], "streak_2": streakList[2],
              "winratePlayer_2": winrateList[2], "Team_2": teamList[2],
              "Champion_2": championIdList[2], "Position_2": positionList[2],
              "Rank_3": eloList[3], "streak_3": streakList[3],
              "winratePlayer_3": winrateList[3], "Team_3": teamList[3],
              "Champion_3": championIdList[3], "Position_3": positionList[3],
              "Rank_4": eloList[4], "streak_4": streakList[4],
              "winratePlayer_4": winrateList[4], "Team_4": teamList[4],
              "Champion_4": championIdList[4], "Position_4": positionList[4],
              "Rank_5": eloList[5], "streak_5": streakList[5],
              "winratePlayer_5": winrateList[5], "Team_5": teamList[5],
              "Champion_5": championIdList[5], "Position_5": positionList[5],
              "Rank_6": eloList[6], "streak_6": streakList[6],
              "winratePlayer_6": winrateList[6], "Team_6": teamList[6],
              "Champion_6": championIdList[6], "Position_6": positionList[6],
              "Rank_7": eloList[7], "streak_7": streakList[7]
              ,"winratePlayer_7": winrateList[7], "Team_7": teamList[7],
              "Champion_7": championIdList[7], "Position_7": positionList[7],
              "Rank_8": eloList[8], "streak_8": streakList[8],
              "winratePlayer_8": winrateList[8], "Team_8": teamList[8],
              "Champion_8": championIdList[8], "Position_8": positionList[8],
              "Rank_9": eloList[9], "streak_9": streakList[9],
              "winratePlayer_9": winrateList[9], "Team_9": teamList[9],
              "Champion_9": championIdList[9], "Position_9": positionList[9],
              "Patch": patch, "matchId": matchId, "Win": win}

    displayInfo = [championNameList, skinList, rankList, winrateList, streakList]

    return liveData, displayInfo
