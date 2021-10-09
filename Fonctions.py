# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:02:44 2021

@author: zkw, lepercq, louesdon
"""

import time
import pandas as pd
from termcolor import colored
from riotwatcher import  ApiError


def requestSummonerData(summonerName, lol_watcher):
    """Renvoie les données de compte du joueur vi summonerName"""
    try:
        return lol_watcher.summoner.by_name('euw1', summonerName)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestSummonerData(summonerName, lol_watcher)
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.1')
            return {}
        elif err.response.status_code >= 500:
            print("[API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
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
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestSummonerData2(puuid, lol_watcher)
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous puuid not found. 2')
        elif err.response.status_code >= 500:
            print("[API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
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
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestRankedData(ID, lol_watcher)
        elif err.response.status_code == 404:
            print('Ranked data not found.')
        elif err.response.status_code >= 500:
            print("[API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
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
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestGamesPlayed(puuid, lol_watcher, queueId, nbGames)
        elif err.response.status_code == 404:
            print('Matchs list not found.')
        elif err.response.status_code >= 500:
            print("[API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
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
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            time.sleep(int(err.response.headers['Retry-After'])+1)
            requestMatchData(matchId, lol_watcher)
        elif err.response.status_code == 404:
            print('Match data not found.')
        elif err.response.status_code >= 500:
            print("[API Error "+str(err.response.status_code)+"] - Waiting 5 seconds")
            time.sleep(5)
            requestMatchData(matchId, lol_watcher)
        else:
            print("C'est la merde pour requestMatchData.", err.response.status_code)
            raise

def getPlayerList(summonerName, playerList, queue, nbGames, nbMaxPlayer, lol_watcher):
    """Renvoie une liste des joueurs apparu dans les parties des joueurs
    rencontrés par le SummonerName choisi.
    La liste n'excedant pas 10 000 joueurs est exporté en fichier plat."""
    if len(playerList) == 0:
        print("starting a new list")
        matchList = requestGamesPlayed(requestSummonerData(summonerName, lol_watcher)["puuid"], lol_watcher, queue, nbGames)
        playerList = []
        for matchId in matchList:
            matchData = requestMatchData(matchId, lol_watcher)
            if matchData:
                playerList += matchData['metadata']['participants']
                playerList = list(dict.fromkeys(playerList))
                
    playerList_new = []
    start = True      
    print("List length:", len(playerList)) 
    while len(playerList) < nbMaxPlayer:
        print("starting over...adding more players to the list")
        if start:
            playerList_new = playerList
            start = False
        
        matchList = []
        for player in playerList_new:
            matchList += requestGamesPlayed(player, lol_watcher, queue, nbGames)
        
        print("collecting players id from", len(matchList), "games")
        playerList_new = []    
        for matchId in matchList:
            matchData = requestMatchData(matchId, lol_watcher)
            if matchData:
                playerList_new += matchData['metadata']['participants']
                playerList_new = list(dict.fromkeys(playerList_new))
            if (len(playerList)+len(playerList_new)) > nbMaxPlayer:
                break
                 
        playerList += playerList_new
        playerList = list(dict.fromkeys(playerList))
        print("adding", len(playerList_new), "players\nList length:", len(playerList)) 
                
                               
    return list(dict.fromkeys(playerList))

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
    for i in range(10):
        participants.append(str(matchData['info']['participants'][i]['summonerId']))
        position.append(getPosition(matchData['info']['participants'][i]['teamPosition']))
        team.append(matchData['info']['participants'][i]['teamId'])
        champion.append(matchData['info']['participants'][i]['championId'])

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
                if rankedData[0]['queueType'] == "RANKED_SOLO_SR":
                    elo.append(getElo(rankedData[0]['tier'], getRank(rankedData[0]['rank'])))
                    if rankedData[0]['hotStreak']:
                        streak.append(1)
                    else:
                        streak.append(0)
                    #il faut que le joueur ait joué au moins 10 partie
                    if (rankedData[0]['wins'] + rankedData[0]['losses']) > 10 :
                        winrate.append(round(rankedData[0]['wins']/(rankedData[0]['wins'] + rankedData[0]['losses']),2))
                    else: winrate.append(0.5)
                elif len(rankedData)>1:
                    elo.append(getElo(rankedData[1]['tier'], getRank(rankedData[1]['rank'])))
                    if rankedData[1]['hotStreak']:
                        streak.append(1)
                    else:
                        streak.append(0)
                    #il faut que le joueur ait joué au moins 10 partie
                    if (rankedData[1]['wins'] + rankedData[1]['losses']) > 10 :
                        winrate.append(round(rankedData[1]['wins']/(rankedData[1]['wins'] + rankedData[1]['losses']),2))
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
            print("Not a player")


    eloDiff = round((sum(elo[0:4])/5) - (sum(elo[5:9])/5),2)

    ListFinale = {"Rank_0": elo[0], "streak_0": streak[0],
                  "winratePlayer_0": winrate[0], "Team_0": team[0],
                  "Champion_0": champion[0], "Position_0": position[0],
                  "Rank_1": elo[1], "streak_1": streak[1],
                  "winratePlayer_1": winrate[1], "Team_1": team[1],
                  "Champion_1": champion[1], "Position_1": position[1],
                  "Rank_2": elo[2], "streak_2": streak[2],
                  "winratePlayer_2": winrate[2], "Team_2": team[2],
                  "Champion_2": champion[2], "Position_2": position[2],
                  "Rank_3": elo[3], "streak_3": streak[3],
                  "winratePlayer_3": winrate[3], "Team_3": team[3],
                  "Champion_3": champion[3], "Position_3": position[3],
                  "Rank_4": elo[4], "streak_4": streak[4],
                  "winratePlayer_4": winrate[4], "Team_4": team[4],
                  "Champion_4": champion[4], "Position_4": position[4],
                  "Rank_5": elo[5], "streak_5": streak[5],
                  "winratePlayer_5": winrate[5], "Team_5": team[5],
                  "Champion_5": champion[5], "Position_5": position[5],
                  "Rank_6": elo[6], "streak_6": streak[6],
                  "winratePlayer_6": winrate[6], "Team_6": team[6],
                  "Champion_6": champion[6], "Position_6": position[6],
                  "Rank_7": elo[7], "streak_7": streak[7],
                  "winratePlayer_7": winrate[7], "Team_7": team[7],
                  "Champion_7": champion[7], "Position_7": position[7],
                  "Rank_8": elo[8], "streak_8": streak[8],
                  "winratePlayer_8": winrate[8], "Team_8": team[8],
                  "Champion_8": champion[8], "Position_8": position[8],
                  "Rank_9": elo[9], "streak_9": streak[9],
                  "winratePlayer_9": winrate[9], "Team_9": team[9],
                  "Champion_9": champion[9], "Position_9": position[9],
                  "EloDiff": eloDiff, "Patch": patch, "matchId": matchId,
                  "Win": win}

    return ListFinale



def tonsOfData(puuid, queue, nbGames, chemin_export, lol_watcher, matchListHistory):
    matchList = requestGamesPlayed(puuid, lol_watcher, queue, nbGames)
    Colunms_Name = ["Rank_0", "streak_0", "winratePlayer_0", "Team_0", "Champion_0", "Position_0",
                   "Rank_1", "streak_1", "winratePlayer_1", "Team_1", "Champion_1", "Position_1",
                   "Rank_2", "streak_2", "winratePlayer_2", "Team_2", "Champion_2", "Position_2",
                   "Rank_3", "streak_3", "winratePlayer_3", "Team_3", "Champion_3", "Position_3",
                   "Rank_4", "streak_4", "winratePlayer_4", "Team_4", "Champion_4", "Position_4",
                   "Rank_5", "streak_5", "winratePlayer_5", "Team_5", "Champion_5", "Position_5",
                   "Rank_6", "streak_6", "winratePlayer_6", "Team_6", "Champion_6", "Position_6",
                   "Rank_7", "streak_7", "winratePlayer_7", "Team_7", "Champion_7", "Position_7",
                   "Rank_8", "streak_8", "winratePlayer_8", "Team_8", "Champion_8", "Position_8",
                   "Rank_9", "streak_9", "winratePlayer_9", "Team_9", "Champion_9", "Position_9",
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
