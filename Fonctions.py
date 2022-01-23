# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:02:44 2021

@author: zkw, lepercq, louesdon
"""

import time
import pandas as pd
from termcolor import colored
from riotwatcher import  ApiError
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def championName(championName):    
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


def requestSummonerData(summonerName, lol_watcher):
    """Renvoie les données de compte du joueur vi summonerName"""
    try:
        return lol_watcher.summoner.by_name('euw1', summonerName)
    except ApiError as err:
        if err.response.status_code == 429:
            print("[requestSummonerData - API Error "+str(err.response.status_code)+'] - We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestSummonerData(summonerName, lol_watcher)
        elif err.response.status_code == 404:
            print("[requestSummonerData - API Error "+str(err.response.status_code)+"] - "+ summonerName +" Summoner with that ridiculous name not found.")
            return {}
        elif err.response.status_code >= 500:
            print("[requestSummonerData - API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
            time.sleep(5)
            requestSummonerData(summonerName, lol_watcher)
        else:
            print("C'est la merde pour requestSummonerData.", err.response.status_code)
            raise

def requestSummonerData2(puuid, lol_watcher):
    """Renvoie les données de compte du joueur via puuid"""
    try:
        return lol_watcher.summoner.by_puuid('euw1', puuid)
    except ApiError as err:
        if err.response.status_code == 429:
            print("[requestSummonerData2- API Error "+str(err.response.status_code)+'] - We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestSummonerData2(puuid, lol_watcher)
        elif err.response.status_code == 404:
            print("[requestSummonerData2 - API Error "+str(err.response.status_code)+"] - "+ puuid +" Summoner with that ridiculous puuid not found.")
        elif err.response.status_code >= 500:
            print("[requestSummonerData2 - API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
            time.sleep(5)
            requestSummonerData2(puuid, lol_watcher)
        else:
            print("C'est la merde pour requestSummonerData2.", err.response.status_code)
            raise

def requestRankedData(ID, lol_watcher):
    """Renvoie les données de classement du joueur"""
    try:
        return lol_watcher.league.by_summoner('euw1', ID)
    except ApiError as err:
        if err.response.status_code == 429:
            print("[requestRankedData - API Error "+str(err.response.status_code)+'] - We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestRankedData(ID, lol_watcher)
        elif err.response.status_code == 404:
            print("[requestRankedData - API Error "+str(err.response.status_code)+"] - Ranked data not found.")
        elif err.response.status_code >= 500:
            print("[requestRankedData - API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
            time.sleep(5)
            requestRankedData(ID, lol_watcher)
        else:
            print("C'est la merde pour requestRankedData.", err.response.status_code)
            raise

def requestGamesPlayed(puuid, lol_watcher, queueId, nbGames):
    """Renvoie la liste des games jouées du joueur"""
    try:
        return lol_watcher.match_v5.matchlist_by_puuid('EUROPE',
                                                       puuid,
                                                       queue = queueId,
                                                       count = nbGames)
    except ApiError as err:
        if err.response.status_code == 429:
            print("[requestGamesPlayed - API Error "+str(err.response.status_code)+'] - We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestGamesPlayed(puuid, lol_watcher, queueId, nbGames)
        elif err.response.status_code == 404:
            print("[requestGamesPlayed - API Error "+str(err.response.status_code)+"] - Matchs list not found")
        elif err.response.status_code >= 500:
            print("[requestGamesPlayed - API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
            time.sleep(5)
            requestGamesPlayed(puuid, lol_watcher, queueId, nbGames)
        else:
            print("C'est la merde pour requestGamesPlayed.", err.response.status_code)
            raise

def requestMatchData(matchId, lol_watcher):
    """Renvoie les données du match"""
    try:
        return lol_watcher.match_v5.by_id('EUROPE',matchId)
    except ApiError as err:
        if err.response.status_code == 429:
            print("[requestMatchData - API Error "+str(err.response.status_code)+'] - We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestMatchData(matchId, lol_watcher)
        elif err.response.status_code == 404:
            print("[requestMatchData - API Error "+str(err.response.status_code)+"] - Match data not found")
        elif err.response.status_code >= 500:
            print("[requestMatchData - API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
            time.sleep(5)
            requestMatchData(matchId, lol_watcher)
        else:
            print("C'est la merde pour requestMatchData.", err.response.status_code)
            raise

def getPlayerList(summonerName, playerList, queue, nbGames, nbMaxPlayer, lol_watcher):
    """Renvoie une liste des joueurs apparu dans les parties des joueurs
    rencontrés par le SummonerName choisi.
    La liste n'excedant pas 10 000 joueurs est exporté en fichier plat."""
    
    cpt = 0
    nbPlayer = 2500
                
    while len(playerList) < nbMaxPlayer:
        
        if len(playerList) == 0:
            print("starting a new list")
            matchList = requestGamesPlayed(requestSummonerData(summonerName, lol_watcher)["puuid"], lol_watcher, queue, nbGames)
            playerList = []
            for matchId in matchList:
                matchData = requestMatchData(matchId, lol_watcher)
                if matchData:
                    playerList += matchData['metadata']['participants']
                    playerList = list(dict.fromkeys(playerList))
                         
        cpt += 1
        lng = len(playerList)
        print(f"[step {cpt}] - max found : {lng} < {nbMaxPlayer}")
                    
        matchList = []
        playerList_new = []           
        for player in  playerList:
            matchList = requestGamesPlayed(player, lol_watcher, queue, nbGames)
            if matchList:
                for matchId in matchList:
                    matchData = requestMatchData(matchId, lol_watcher)
                    if matchData:
                        playerList_new += matchData['metadata']['participants']
                        playerList_new = list(dict.fromkeys(playerList_new))
                        
                lng = len(playerList_new)
                print(f"[step {cpt}] - players found : {lng}")
            
            if lng > nbMaxPlayer:
                break
            
            if lng > nbPlayer:
                print(f"[step {cpt}] - saving {lng} puuid")
                if nbPlayer == 2500:
                    playerList_temp = []
                else:
                    with open('listPUUID.csv', newline='', encoding='UTF8') as f:
                        playerList_temp = list(csv.reader(f))[0]
        
                playerList_temp += playerList_new
                playerList_temp = list(dict.fromkeys(playerList_temp))
                
                with open("listPUUID.csv", 'w', newline='', encoding='UTF8') as f:
                    csv.writer(f, quoting=csv.QUOTE_ALL).writerow(playerList_temp)
                    
                nbPlayer += 2500
                
        print(f"[step {cpt}] - saving {lng} puuid")
        if nbPlayer == 2500:
            playerList_temp = []
        else:
            with open('listPUUID.csv', newline='', encoding='UTF8') as f:
                playerList_temp = list(csv.reader(f))[0]

        playerList_temp += playerList_new
        playerList_temp = list(dict.fromkeys(playerList_temp))
        
        with open("listPUUID.csv", 'w', newline='', encoding='UTF8') as f:
            csv.writer(f, quoting=csv.QUOTE_ALL).writerow(playerList_temp)
            
        playerList = playerList_new
        
    return list(dict.fromkeys(playerList))

def getPlayerStatsOnChampion(summonerName, championName):
    """Renvoie les statistiques du joueur sélectionné pour le champion sélectionné.
    Exemple de retour : Nb games jouées : 33 (int), Winrate : 63.2 (float)
    exemple pour KhaZix et MonkeyKing : EUW1_5448612206"""
    if championName.lower() == "monkeyking":
        championName = "wukong"
    url = 'https://www.leagueofgraphs.com/fr/summoner/champions/'+championName+'/euw/'+summonerName
    session = HTMLSession()
    response = session.get(url)
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    gamesPlayedOnChampion = 0
    winrateOnChampion = 50
    listgraph = ["graphDD53", "graphDD54", "graphDD55", "graphDD56", "graphDD57", "graphDD58", "graphDD59"]  #list of graphs to check for the player data
    for graph in listgraph:
        if soup.find(id=graph):
            if right(soup.find(id=graph).string.strip(), 1) == "%":
                winrateOnChampion = float(left(soup.find(id=graph).string.strip(), len(soup.find(id=graph).string.strip())-1))
            elif len(soup.find(id=graph).string.strip()) > 0:
                gamesPlayedOnChampion = int(soup.find(id=graph).string.strip())
    return gamesPlayedOnChampion, winrateOnChampion  

def getRank(rank):
    """Renvoie le rank du jouer en int"""
    if rank == "I":
        r = 1
    if rank == "II":
        r = 2
    if rank == "III":
        r = 3
    if rank == "IV":
        r = 4
    return r

def getElo(tier, rank):
    """Renvoie l'elo du joueur en int"""
    if tier == "CHALLENGER":
        r = 1
    if tier == "GRANDMASTER":
        r = 2
    if tier == "MASTER":
        r = 3
    if tier == "DIAMOND":
        r = 3 + rank
    if tier == "PLATINUM":
        r = 7 + rank
    if tier == "GOLD":
        r = 11 + rank
    if tier == "SILVER":
        r = 15 + rank
    if tier == "BRONZE":
        r = 19 + rank
    if tier == "IRON":
        r = 23 + rank
    return r

def getPosition(position):
    """Renvoie la position du joueur en int"""
    if position == "TOP":
        r = 1
    if position == "JUNGLE":
        r = 2
    if position == "MIDDLE":
        r = 3
    if position == "BOTTOM":
        r = 4
    else:
        r = 5
    return r


def getGameData(matchId, lol_watcher):
    """Permet de récupérer les infos d'une game qui serviront de base
    d'entrainnement de nos modèles"""
    matchData = requestMatchData(matchId, lol_watcher)

    #Informations globales du match
    patch = matchData['info']['gameVersion']
    if ((matchData['info']['teams'][0]['teamId'] == 100 and matchData['info']['teams'][0]['win']) or (matchData['info']['teams'][0]['teamId'] == 200 and not matchData['info']['teams'][0]['win'])):
        win = 100
    else:
        win = 200

    #Informations des joueurs inGame
    participants = []
    team = []
    champion = []
    position = []
    championName = []
    summonerName = []
    for i in range(10):
        participants.append(str(matchData['info']['participants'][i]['summonerId']))
        position.append(getPosition(matchData['info']['participants'][i]['teamPosition']))
        team.append(matchData['info']['participants'][i]['teamId'])
        champion.append(matchData['info']['participants'][i]['championId'])
        championName.append(matchData['info']['participants'][i]['championName'].lower())
        summonerName.append(matchData['info']['participants'][i]['summonerName'])

    #Informations des joueurs en ranked
    elo = []
    streak = []
    winrate = []
    for sumID in participants:
        #On vérifie que le summoner est un joueur        
        if sumID:            
            rankedData = requestRankedData(sumID, lol_watcher)
            #On vérifie que le summoner a joué en ranked
            if rankedData:
                if rankedData[0]['queueType'] == "RANKED_SOLO_5x5":
                    elo.append(getElo(rankedData[0]['tier'], getRank(rankedData[0]['rank'])))
                    if rankedData[0]['hotStreak']:
                        streak.append(1)
                    else:
                        streak.append(0)
                    #il faut que le joueur ait joué au moins 10 partie
                    if (rankedData[0]['wins'] + rankedData[0]['losses']) > 10 :
                        winrate.append(round(rankedData[0]['wins']/(rankedData[0]['wins'] + rankedData[0]['losses']), 2))
                    else: winrate.append(0.5)
                elif len(rankedData) > 1:
                    if rankedData[1]['queueType'] == "RANKED_SOLO_5x5":                    
                        elo.append(getElo(rankedData[1]['tier'], getRank(rankedData[1]['rank'])))
                        if rankedData[1]['hotStreak']:
                            streak.append(1)
                        else:
                            streak.append(0)
                        #il faut que le joueur ait joué au moins 10 partie
                        if (rankedData[1]['wins'] + rankedData[1]['losses']) > 10 :
                            winrate.append(round(rankedData[1]['wins']/(rankedData[1]['wins'] + rankedData[1]['losses']), 2))
                        else: winrate.append(0.5)
                    elif len(rankedData) == 3:
                        if rankedData[2]['queueType'] == "RANKED_SOLO_5x5":
                            elo.append(getElo(rankedData[2]['tier'], getRank(rankedData[2]['rank'])))
                            if rankedData[2]['hotStreak']:
                                streak.append(1)
                            else:
                                streak.append(0)
                            #il faut que le joueur ait joué au moins 10 partie
                            if (rankedData[2]['wins'] + rankedData[2]['losses']) > 10 :
                                winrate.append(round(rankedData[1]['wins']/(rankedData[1]['wins'] + rankedData[2]['losses']), 2))
                            else: winrate.append(0.5)
                        else:
                            elo.append(19)
                            streak.append(0)
                            winrate.append(0.5)
                    else:
                        elo.append(19)
                        streak.append(0)
                        winrate.append(0.5)
                else:
                    elo.append(19)
                    streak.append(0)
                    winrate.append(0.5)
            else:
                elo.append(19)
                streak.append(0)
                winrate.append(0.5)
        else:
            print("Not a player.")

    winrateOnChampion = []
    i = 0
    for i in range(0,10):
        gamesPlayedOnChampion, wr = getPlayerStatsOnChampion(summonerName[i], championName[i])
        if gamesPlayedOnChampion > 5:
            winrateOnChampion.append(wr)
        else:
            winrateOnChampion.append(50)
        
    eloDiff = round((sum(elo[0:4])/5) - (sum(elo[5:9])/5),2)

    ListFinale = {"Rank_0": elo[0], "streak_0": streak[0],
                  "winratePlayer_0": winrate[0], "Team_0": team[0],
                  "Champion_0": champion[0], "Position_0": position[0],
                  "winrateOnChampion_0": winrateOnChampion[0],
                  "Rank_1": elo[1], "streak_1": streak[1],
                  "winratePlayer_1": winrate[1], "Team_1": team[1],
                  "Champion_1": champion[1], "Position_1": position[1],
                  "winrateOnChampion_1": winrateOnChampion[1],
                  "Rank_2": elo[2], "streak_2": streak[2],
                  "winratePlayer_2": winrate[2], "Team_2": team[2],
                  "Champion_2": champion[2], "Position_2": position[2],
                  "winrateOnChampion_2": winrateOnChampion[2],
                  "Rank_3": elo[3], "streak_3": streak[3],
                  "winratePlayer_3": winrate[3], "Team_3": team[3],
                  "Champion_3": champion[3], "Position_3": position[3],
                  "winrateOnChampion_3": winrateOnChampion[3],
                  "Rank_4": elo[4], "streak_4": streak[4],
                  "winratePlayer_4": winrate[4], "Team_4": team[4],
                  "Champion_4": champion[4], "Position_4": position[4],
                  "winrateOnChampion_4": winrateOnChampion[4],
                  "Rank_5": elo[5], "streak_5": streak[5],
                  "winratePlayer_5": winrate[5], "Team_5": team[5],
                  "Champion_5": champion[5], "Position_5": position[5],
                  "winrateOnChampion_5": winrateOnChampion[5],
                  "Rank_6": elo[6], "streak_6": streak[6],
                  "winratePlayer_6": winrate[6], "Team_6": team[6],
                  "Champion_6": champion[6], "Position_6": position[6],
                  "winrateOnChampion_6" :winrateOnChampion[6],
                  "Rank_7": elo[7], "streak_7": streak[7],
                  "winratePlayer_7": winrate[7], "Team_7": team[7],
                  "Champion_7": champion[7], "Position_7": position[7],
                  "winrateOnChampion_7": winrateOnChampion[7],
                  "Rank_8": elo[8], "streak_8": streak[8],
                  "winratePlayer_8": winrate[8], "Team_8": team[8],
                  "Champion_8": champion[8], "Position_8": position[8],
                  "winrateOnChampion_8": winrateOnChampion[8],
                  "Rank_9": elo[9], "streak_9": streak[9],
                  "winratePlayer_9": winrate[9], "Team_9": team[9],
                  "Champion_9": champion[9], "Position_9": position[9],
                  "winrateOnChampion_9": winrateOnChampion[9],
                  "EloDiff": eloDiff, "Patch": patch, "matchId": matchId,
                  "Win": win}

    return ListFinale


def tonsOfData(puuid, queue, nbGames, chemin_export, lol_watcher, matchListHistory):
    matchList = requestGamesPlayed(puuid, lol_watcher, queue, nbGames)
    Colunms_Name = ["Rank_0", "streak_0", "winratePlayer_0", "Team_0", "Champion_0", "Position_0","winrateOnChampion_0",
                   "Rank_1", "streak_1", "winratePlayer_1", "Team_1", "Champion_1", "Position_1","winrateOnChampion_1",
                   "Rank_2", "streak_2", "winratePlayer_2", "Team_2", "Champion_2", "Position_2","winrateOnChampion_2",
                   "Rank_3", "streak_3", "winratePlayer_3", "Team_3", "Champion_3", "Position_3","winrateOnChampion_3",
                   "Rank_4", "streak_4", "winratePlayer_4", "Team_4", "Champion_4", "Position_4","winrateOnChampion_4",
                   "Rank_5", "streak_5", "winratePlayer_5", "Team_5", "Champion_5", "Position_5","winrateOnChampion_5",
                   "Rank_6", "streak_6", "winratePlayer_6", "Team_6", "Champion_6", "Position_6","winrateOnChampion_6",
                   "Rank_7", "streak_7", "winratePlayer_7", "Team_7", "Champion_7", "Position_7","winrateOnChampion_7",
                   "Rank_8", "streak_8", "winratePlayer_8", "Team_8", "Champion_8", "Position_8","winrateOnChampion_8",
                   "Rank_9", "streak_9", "winratePlayer_9", "Team_9", "Champion_9", "Position_9","winrateOnChampion_9",
                   "EloDiff", "Patch", "matchId" ,"Win"
                   ]
    match_Datas = pd.DataFrame(columns = Colunms_Name)
    print("Player: "+puuid)
    for m in matchList:
        if m not in matchListHistory or len(matchListHistory) == 0:
            matchListHistory.append(m)
            print(colored(m, "magenta"))
            if requestMatchData(m, lol_watcher):
                match_Datas = match_Datas.append(getGameData(m, lol_watcher), ignore_index=True)
    if not match_Datas.empty:
        match_Datas.to_csv(chemin_export+".csv", index=False)
    return matchListHistory
