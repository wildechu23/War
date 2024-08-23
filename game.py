# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 15:29:45 2024

@author: detec
"""


'''War Game'''
import pandas as pd
from copy import deepcopy

#%%

#Dictionary containing all move data
Movedata = {
    'Charge': {'Cost': {}, 'TargetType': 'All'},
    'Block': {'Cost': {}, 'TargetType': 'All', 'Shield': 1.5},
    'Reflect': {'Cost': {'Charges': 1}, 'TargetType': 'All'},
    'Portal': {'Cost': {'Magical Shards': 3}, 'TargetType': 'All'},
    'Invincible': {'Cost': {'Charges': 2}, 'TargetType': 'All', 'Shield': 4},
    'Smoke': {'Cost': {'Blocks': 2}, 'TargetType': 'All'},
    'Smoke Machine': {'Cost': {'Fumes': 2}, 'TargetType': 'All', 'Damage': 1},
    
    'Ghostgun': {'Cost': {'Charges': 2}, 'TargetType': 'Single', 'Damage': 1},
    'Flaming': {'Cost': {'Charges': 2}, 'TargetType': 'Single', 'Damage': 2.5},
    'Pew': {'Cost': {'Charges': 1}, 'TargetType': 'Single', 'Damage': 1},
    'Pew-Charge': {'Cost': {'Pew-Charge': 1}, 'TargetType': 'Single', 'Damage': 1},
    'Unbreakable': {'Cost': {'Doubles': 1}, 'TargetType': 'Single', 'Damage': 1},
    'Bazooka': {'Cost': {'Blocks': 2}, 'TargetType': 'Single', 'Damage': 1} ,
    'Sniper': {'Cost': {'Blocks': 2}, 'TargetType': 'Single', 'Damage': 1},
    
    #'Disable': {'Cost': ('2 Blocks', '2 Charges'), 'TargetType': 'Single'}
    }
ResourceMovesList = ['Charge', 'Block', 'Reflect', 'Smoke', 'Invincible', 'Pew-Charge']
ResourceGainList = ['Charges', 'Blocks', 'Magical Shards', 'Fumes', 'Doubles', 'Charges']

AchievementDescriptions = {
    'Noob': 'Make your first legal move!',
    'Taste of Blood': 'Get your first kill',
    'Enemy of my Enemy': 'Get your first assist',
    'To the Victors': 'Win your first game',
    'Mutually Assured Destruction': 'Be one of the last players standing when a game ends with no winner',
    'Close Call': 'Attack a player using portal and survive',
    'Sabotoge': 'Use Disable',
    'Thumbs Up!': 'Win the game while using Charge',
    'Bruh': 'Use Bazooka, Flaming, and Unbreakable in one turn',
    'Stormtrooper': 'Fail to get kill credit (kills/assists) with 5 pews/pew-charges in a row',
    'Jack of All Trades': 'Win with every move',
    'Lack of All Trades': 'Lose with every move'
    }

#%%
def EvaluateAchievements(PlayerAchievements, PlayerList, NonEliminatedPlayers, EliminatedPlayers, IllegalElimination, OriginalMoves, PlayerMoves, PlayerProfiles, KillCredits):
    for player in PlayerList:
        for achievement in PlayerAchievements[player]:
            #Only update achievement if it hasn't been acquired
            if PlayerAchievements[player][achievement] != "Unlocked":
                #First Move
                if achievement == 'Noob':
                    if player not in IllegalElimination:
                        PlayerAchievements[player][achievement] = "Unlocked"
                #First Kill
                if achievement == 'Taste of Blood':
                    if PlayerProfiles[player]["Total Kills"] > 0:
                        PlayerAchievements[player][achievement] = "Unlocked"
                        
                #First Assist
                elif achievement == 'Enemy of my Enemy':
                    if PlayerProfiles[player]["Total Assists"] > 0:
                        PlayerAchievements[player][achievement] = "Unlocked"
                
                #First Win
                elif achievement == 'To the Victors':
                    if [player] == NonEliminatedPlayers:
                        PlayerAchievements[player][achievement] = "Unlocked"
                
                #Nobody Wins
                elif achievement == 'Mutually Assured Destruction':
                    if NonEliminatedPlayers == []:
                        PlayerAchievements[player][achievement] = "Unlocked"
                
                #Survive Attacking Portal
                elif achievement == 'Close Call':
                    if player in NonEliminatedPlayers and OriginalMoves[player]['Target'] != '':
                        if 'Portal' in PlayerMoves[OriginalMoves[player]['Target']]['Moves']:
                            PlayerAchievements[player][achievement] = "Unlocked"
                
                #Use Disable
                elif achievement == 'Sabotoge':
                    if 'Disable' in PlayerMoves[player]['Moves'] and player not in IllegalElimination:
                        PlayerAchievements[player][achievement] = "Unlocked"
                        
                #Win with Charge
                elif achievement == 'Thumbs Up!':
                    if [player] == NonEliminatedPlayers and 'Charge' in PlayerMoves[player]['Moves']:
                        PlayerAchievements[player][achievement] = "Unlocked"    
                        
                #Bazooka-Flaming-Unbreakable
                elif achievement == 'Bruh':
                    if player not in IllegalElimination and 'Bazooka' in PlayerMoves[player]['Moves'] and 'Flaming' in PlayerMoves[player]['Moves'] and 'Unbreakable' in PlayerMoves[player]['Moves']:
                        PlayerAchievements[player][achievement] = "Unlocked"  
                
                #Miss 5 pew/pew-charges in a row
                elif achievement == 'StormTrooper':
                    #Has to be legal
                    if 'Pew-Charge' in PlayerMoves[player]['Moves'] or 'Pew' in PlayerMoves[player]['Moves']:
                        IncreaseMissCount = 1
                        for eliminatedplayer in EliminatedPlayers:
                            if eliminatedplayer not in IllegalElimination and player in KillCredits[eliminatedplayer]:
                                IncreaseMissCount = 0
                                PlayerAchievements[player][achievement] = [0]
                        if IncreaseMissCount == 1:
                            PlayerAchievements[player][achievement] = [PlayerAchievements[player][achievement][0] + 1]
                    if PlayerAchievements[player][achievement] == 5:
                        PlayerAchievements[player][achievement] = "Unlocked" 
                
                elif achievement == 'Jack of All Trades':
                    Changed = 0
                    if [player] == NonEliminatedPlayers:
                        for move in OriginalMoves[player]['Moves']:
                            if move not in PlayerAchievements[player][achievement]:
                                PlayerAchievements[player][achievement] = PlayerAchievements[player][achievement] + [move]
                                Changed = 1
                    if Changed == 1 and 0 not in [1 if move in PlayerAchievements[player][achievement] else 0 for move in Movedata]:
                        PlayerAchievements[player][achievement] = "Unlocked" 
                
                elif achievement == 'Lack of All Trades':
                    Changed = 0
                    if player in EliminatedPlayers:
                        for move in OriginalMoves[player]['Moves']:
                            if move not in PlayerAchievements[player][achievement]:
                                PlayerAchievements[player][achievement] = PlayerAchievements[player][achievement] + [move]
                                Changed = 1
                    if Changed == 1 and 0 not in [1 if move in PlayerAchievements[player][achievement] else 0 for move in Movedata]:
                        PlayerAchievements[player][achievement] = "Unlocked"   
                        
                if PlayerAchievements[player][achievement] == "Unlocked":
                    print(player, "has unlocked the achievement", achievement, ": " + AchievementDescriptions[achievement])

#%%                    
def EvaluateWarGame(GameMode, PlayerList, PlayerResources, PlayerMoves, PlayerProfiles, PlayerAchievements):
    '''Start of Round'''
    EliminatedPlayers = []
    NonEliminatedPlayers = PlayerList
    
    OriginalMoves = deepcopy(PlayerMoves)
    
    Smoked = 0
    SmokeMachined = 0
    NumSmokeMachinePlayers = 0
    
    KillCredits = {PlayerList[i]: [] for i in range (0,len(PlayerList))}

    #initialize a table of players and their interactions with other players. start at 0.
    PlayerDataframe = pd.DataFrame(
        [{PlayerList[i]: float(0) for i in range (0, len(PlayerList))} for j in range (0, len(PlayerList) + 1)], 
        index = [PlayerList[i] for i in range (0, len(PlayerList))] + ['Total']
        )
    #First check validity of moves
    #Reasons for invalidity: Cost, Combination, Inputs
    for player in PlayerMoves:
        if player in NonEliminatedPlayers:
            #Cost and Combination Verification
            CurrentPlayerResources = PlayerResources[player]
            PlayerMoveTypes = []
            Eliminated = 0
            for move in PlayerMoves[player]['Moves']:
                if move in Movedata.keys():
                    MoveCost = Movedata[move]['Cost']
                    PlayerMoveTypes = PlayerMoveTypes + [Movedata[move]['TargetType']]
                    
                    #Cost Check
                    for resource in MoveCost:
                        ResourcesRemaining = CurrentPlayerResources[resource] - MoveCost[resource]
                        CurrentPlayerResources[resource] = ResourcesRemaining
                        if ResourcesRemaining < 0:
                            print(player, 'is eliminated: Not Enough Resources')
                            Eliminated = Eliminated + 1
                #Valid Input Check
                else:
                    print(player, 'is eliminated: Non-valid Move Input')
                    Eliminated = Eliminated + 1
            
            #Combination Check
            if 'All' in PlayerMoveTypes:
                if 'Single' in PlayerMoveTypes:
                    print(player, 'is eliminated: Can not combine Neutral and Attacking Moves')
                    Eliminated = Eliminated + 1
                elif len(PlayerMoveTypes) > 1 and len(PlayerMoveTypes) != PlayerMoves[player]["Moves"].count('Smoke Machine'):
                    print(player, 'is eliminated: Can not use Neutral moves together unless the combined moves are all smoke machines')
                    Eliminated = Eliminated + 1
            else:
                if 'Ghostgun' in PlayerMoves[player]["Moves"] and len(PlayerMoveTypes) != 1:
                    print(player, 'is eliminated: Ghostgun can not be combined with other weapons')
                    Eliminated = Eliminated + 1
                
            #Target Check
            if 'All' in PlayerMoveTypes and PlayerMoves[player]["Target"] != "":
                print(player, 'is eliminated: Can not target on a neutral move')
                Eliminated = Eliminated + 1
            elif 'Single' in PlayerMoveTypes and PlayerMoves[player]["Target"] not in NonEliminatedPlayers:
                print(player, 'is eliminated: Must have 1 (and only 1) valid target')
                Eliminated = Eliminated + 1
            
            #If inputs were invalid for any reason, the player is eliminated.
            if Eliminated > 0:
                EliminatedPlayers = EliminatedPlayers + [player]
            #If not eliminated, look at smokes/smokemachines
            elif 'Smoke' in PlayerMoves[player]["Moves"]:
                Smoked = Smoked + PlayerMoves[player]["Moves"].count('Smoke')
            elif 'Smoke Machine' in PlayerMoves[player]:
                SmokeMachined = SmokeMachined + PlayerMoves[player]["Moves"].count('Smoke Machine')
                NumSmokeMachinePlayers = NumSmokeMachinePlayers + 1
                
    IllegalElimination = deepcopy(EliminatedPlayers)
    
    #Give the people their money (resources)
    for player in NonEliminatedPlayers:
        for move in PlayerMoves[player]["Moves"]:
            if move in ResourceMovesList:
                PlayerResources[player][ResourceGainList[ResourceMovesList.index(move)]] = PlayerResources[player][ResourceGainList[ResourceMovesList.index(move)]] + 1
            if move == 'Charge' or move == 'Pew-Charge':
                PlayerProfiles[player]['Charges Acquired'] = PlayerProfiles[player]['Charges Acquired'] + 1
            if move == 'Block':
                PlayerProfiles[player]['Blocks Acquired'] = PlayerProfiles[player]['Blocks Acquired'] + 1
    
    #Cancelling all moves due to smoke or smoke machine
    if Smoked > 0 or SmokeMachined > 0:
        for player in PlayerMoves:
            removelist = []
            for move in PlayerMoves[player]["Moves"]:
                #normal weapons are smoked out
                if move in Movedata:
                    if move != "Sniper" and move != "Ghostgun" and (Movedata[move]['TargetType'] == 'Single'):
                        removelist = removelist + [move]
                #smoke machine gets smoked out
                if move == 'Smoke Machine' and (Smoked > 0 or NumSmokeMachinePlayers > 1):
                    removelist = removelist + [move]
                #at 3 smokes, sniper is cancelled
                if move == 'Sniper' and Smoked + SmokeMachined >= 3:
                    removelist = removelist + [move]
            PlayerMoves[player]["Moves"] = [move for move in PlayerMoves[player]["Moves"] if move not in removelist]
    #Now determine damage amounts
    #Note, targeting players eliminated this round is still valid (since you can't predict their elimination)
    #However when we consider moves, only consider players who did legal moves
    for player in NonEliminatedPlayers:
        if player not in EliminatedPlayers:
            for move in PlayerMoves[player]["Moves"]:
                if move in Movedata:
                    if 'Shield' in Movedata[move].keys():
                        PlayerDataframe.loc['Total', player] = PlayerDataframe.loc['Total', player] + float(Movedata[move]['Shield'])
                    if 'Damage' in Movedata[move].keys():
                        if move == 'Smoke Machine':
                            for affectedplayer in NonEliminatedPlayers:
                                if affectedplayer != player and 'Reflect' not in PlayerMoves[affectedplayer]["Moves"] and 'Portal' not in PlayerMoves[affectedplayer]["Moves"]:
                                    PlayerDataframe.loc['Total', affectedplayer] = PlayerDataframe.loc['Total', affectedplayer] - float(Movedata[move]['Damage'])
                                    KillCredits[affectedplayer] = KillCredits[affectedplayer] + [player]
                        else:
                            TargetPlayer = PlayerMoves[player]["Target"]
                            #If we are ghostgun and they shoot at us (legally), ghostgun damage is ignored. 
                            #As long as that is not the case...
                            if move != 'Ghostgun' or player != PlayerMoves[TargetPlayer]["Target"] or player in EliminatedPlayers:
                                #Standard Considerations
                                
                                #If reflected or portaled, attacker takes damage. Do not add as shielding for target player.
                                if 'Reflect' in PlayerMoves[TargetPlayer]["Moves"] and TargetPlayer not in EliminatedPlayers and move != 'Ghostgun':
                                    PlayerDataframe.loc[TargetPlayer, player] = PlayerDataframe.loc[TargetPlayer, player] - float(Movedata[move]['Damage'])
                                    KillCredits[player] = KillCredits[player] + [TargetPlayer]
                                elif 'Portal' in PlayerMoves[TargetPlayer]["Moves"] and TargetPlayer not in EliminatedPlayers:
                                    PlayerDataframe.loc[TargetPlayer, player] = PlayerDataframe.loc[TargetPlayer, player] - float(Movedata[move]['Damage'])
                                    KillCredits[player] = KillCredits[player] + [TargetPlayer]
                                else:
                                    #Add damage to target player
                                    PlayerDataframe.loc[player, TargetPlayer] = PlayerDataframe.loc[player, TargetPlayer] - float(Movedata[move]['Damage'])
                                    #Also add shield in that direction only
                                    PlayerDataframe.loc[TargetPlayer, player] = PlayerDataframe.loc[TargetPlayer, player] + float(Movedata[move]['Damage'])   
                                    KillCredits[TargetPlayer] = KillCredits[TargetPlayer] + [player]
    for player in NonEliminatedPlayers:
        if player not in EliminatedPlayers:
            if PlayerDataframe.loc['Total', player] <= 0:
                if (PlayerDataframe.get(player).values < 0).any() ==True:
                    EliminatedPlayers = EliminatedPlayers + [player]   
            elif PlayerDataframe[player].sum() < 0:
                EliminatedPlayers = EliminatedPlayers + [player]
    
    #Remove all eliminated players
    NonEliminatedPlayers = [player for player in NonEliminatedPlayers if player not in EliminatedPlayers]
    
    for player in EliminatedPlayers:
        #Update profile to have loss
        PlayerProfiles[player]['Losses'] = PlayerProfiles[player]['Losses'] + 1
        if player not in IllegalElimination:
            for player2 in PlayerList:
                if player2 in KillCredits[player]:
                    if len(KillCredits[player]) == 1:
                        #Update profiles to have kill if they are the only person with kill credit
                        PlayerProfiles[player2]['Total Kills'] = PlayerProfiles[player2]['Total Kills'] + 1
                    else:
                        #Update profiles to have assist if they are not the only person with kill credit
                        PlayerProfiles[player2]['Total Assists'] = PlayerProfiles[player2]['Total Assists'] + 1

    print("Eliminated Players: ", EliminatedPlayers)
    print("Non-Eliminated Players: ", NonEliminatedPlayers)
    
    for player in NonEliminatedPlayers:
        print(player, PlayerResources[player])

    EvaluateAchievements(PlayerAchievements, PlayerList, NonEliminatedPlayers, EliminatedPlayers, IllegalElimination, OriginalMoves, PlayerMoves, PlayerProfiles, KillCredits)
    
    if len(NonEliminatedPlayers) == 1:
        #Update win
        PlayerProfiles[NonEliminatedPlayers[0]]['Wins'] = PlayerProfiles[NonEliminatedPlayers[0]]['Wins'] + 1
    
    return ({'Game State': 'Game is Ongoing', 'Eliminated Players': EliminatedPlayers, 'Remaining Players': NonEliminatedPlayers, 'Remaining Player Resources': PlayerResources, 'Updated Player Profiles': PlayerProfiles, 'Updated Player Achievements': PlayerAchievements})

#%%
# =============================================================================
# '''Test Example (Gamemode, PlayerList, PlayerProfiles, PlayerResources, PlayerMoves, PlayerAchievements)'''
# 
# NumPlayers = 3
# 
# ExamplePlayerList = ["Player " + str(i+1) for i in range (0, NumPlayers)]
# ExamplePlayerProfiles = {ExamplePlayerList[i]: {'Wins': 0, 'Losses': 0, 'Total Kills': 0, 'Total Assists': 0, 'Charges Acquired': 0, 'Blocks Acquired': 0} for i in range (0,NumPlayers)}
# ExamplePlayerAchievements = {ExamplePlayerList[i]: 
#                              {
#                                  'Noob': [],
#                                  'Taste of Blood': [],
#                                  'Enemy of my Enemy': [],
#                                  'To the Victors': [],
#                                  'Mutually Assured Destruction': [],
#                                  'Close Call': [],
#                                  'Sabotoge': [],
#                                  'Thumbs Up!': [],
#                                  'Bruh': [],
#                                  'Stormtrooper': [],
#                                  'Jack of All Trades': [],
#                                  'Lack of All Trades': []
#                                  }
#                                  for i in range (0,NumPlayers)
#                              }
# #Standard Starting Resources
# #ExamplePlayerResources = {PlayerList[i]: {'Charges': 0, 'Blocks': 0, 'Fumes': 0, 'Magical Shards': 0, 'Doubles': 0, 'Pew-Charge': 1} for i in range (0, NumPlayers)}
# 
# #Test Resources
# ExamplePlayerResources = {ExamplePlayerList[i]: {'Charges': 2, 'Blocks': 4, 'Magical Shards': 3, 'Fumes': 6, 'Doubles': 0, 'Pew-Charge': 1} for i in range (0, NumPlayers)}
# 
# #template
# #ExamplePlayerMoves = {'Player 1': {'Moves':[], 'Target': ''}, 'Player 2': {'Moves':[], 'Target': ''}, 'Player 3': {'Moves':[], 'Target': ''}}
# 
# #examples
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke'], 'Target': ''}, 'Player 2': {'Moves':['Pew-Charge'], 'Target': 'Player 1'}, 'Player 3': {'Moves':['Pew-Charge'], 'Target': 'Player 2'}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Block'], 'Target': ''}, 'Player 2': {'Moves':['Pew-Charge'], 'Target': 'Player 1'}, 'Player 3': {'Moves':['Pew-Charge'], 'Target': 'Player 2'}}
# ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke'], 'Target': ''}, 'Player 2': {'Moves':['Sniper', 'Pew-Charge'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Bazooka'], 'Target': 'Player 2'}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke'], 'Target': ''}, 'Player 2': {'Moves':['Ghostgun'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Portal'], 'Target': ''}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Block'], 'Target': ''}, 'Player 2': {'Moves':['Sniper'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Smoke Machine'], 'Target': ''}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke Machine'], 'Target': ''}, 'Player 2': {'Moves':['Sniper', 'Sniper'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Smoke Machine'], 'Target': ''}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke Machine'], 'Target': ''}, 'Player 2': {'Moves':['Sniper'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Reflect'], 'Target': ''}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke'], 'Target': ''}, 'Player 2': {'Moves':['Sniper'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Sniper'], 'Target': 'Player 2'}}
# #ExamplePlayerMoves = {'Player 1': {'Moves':['Smoke'], 'Target': ''}, 'Player 2': {'Moves':['Sniper'], 'Target': 'Player 3'}, 'Player 3': {'Moves':['Ghostgun'], 'Target': 'Player 2'}}
# 
# ExampleGameMode = 'Default'
# ExampleOutputData = EvaluateWarGame(ExampleGameMode, ExamplePlayerList, ExamplePlayerResources, ExamplePlayerMoves, ExamplePlayerProfiles, ExamplePlayerAchievements)
# =============================================================================
      
'''Future Notes'''
#Implement different game modes (i.e. Share War)  