# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 15:29:45 2024

@author: detec
"""


'''War Game'''
import numpy as np
import pandas as pd

#%%
NumPlayers = 3

PlayerList = ["Player " + str(i+1) for i in range (0, NumPlayers)]
#Dictionary containing all move data
Movedata = {
    'Charge': {'Cost': {}, 'TargetType': 'All'},
    'Block': {'Cost': {}, 'TargetType': 'All', 'Shield': 1.5},
    'Reflect': {'Cost': {'Charges': 2}, 'TargetType': 'All'},
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
#initialize a table of players and their interactions with other players. start at 0.
PlayerDataframe = pd.DataFrame(
    [{PlayerList[i]: float(0) for i in range (0, NumPlayers)} for j in range (0, NumPlayers + 1)], 
    index = ["Player " + str(i+1) for i in range (0, NumPlayers)] + ['Total']
    )

#Starting Resources
#PlayerResources = {PlayerList[i]: {'Charges': 0, 'Blocks': 0, 'Fumes': 0, 'Magical Shards': 0, 'Doubles': 0, 'Pew-Charge': 1} for i in range (0, NumPlayers)}

#Test Resources
PlayerResources = {PlayerList[i]: {'Charges': 2, 'Blocks': 4, 'Magical Shards': 3, 'Fumes': 6, 'Doubles': 0, 'Pew-Charge': 1} for i in range (0, NumPlayers)}

EliminatedPlayers = []
NonEliminatedPlayers = PlayerList 

#%%
'''Start of Round'''
Smoked = 0
SmokeMachined = 0
NumSmokeMachinePlayers = 0

#testmoves
#PlayerMoves = {'Player 1': ['Smoke'], 'Player 2': ['Pew-Charge', 'Player 1'], 'Player 3': ['Pew-Charge', 'Player 2']}
#PlayerMoves = {'Player 1': ['Block'], 'Player 2': ['Pew-Charge', 'Player 1'], 'Player 3': ['Pew-Charge', 'Player 2']}
#PlayerMoves = {'Player 1': ['Smoke'], 'Player 2': ['Sniper', 'Pew-Charge', 'Player 3'], 'Player 3': ['Bazooka', 'Player 2']}
#PlayerMoves = {'Player 1': ['Smoke'], 'Player 2': ['Ghostgun', 'Player 3'], 'Player 3': ['Portal']}
#PlayerMoves = {'Player 1': ['Block'], 'Player 2': ['Sniper', 'Player 3'], 'Player 3': ['Smoke Machine']}
#PlayerMoves = {'Player 1': ['Smoke Machine'], 'Player 2': ['Sniper', 'Player 3'], 'Player 3': ['Smoke Machine']}
PlayerMoves = {'Player 1': ['Smoke Machine'], 'Player 2': ['Sniper', 'Sniper', 'Player 3'], 'Player 3': ['Smoke Machine', 'Smoke Machine']}
#First check validity of moves

#Reasons for invalidity: Cost, Combination, Inputs

for player in PlayerMoves:
    if player in NonEliminatedPlayers:
        #Cost and Combination Verification
        CurrentPlayerResources = PlayerResources[player]
        PlayerMoveTypes = []
        Eliminated = 0
        for move in PlayerMoves[player]:
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
            elif move not in NonEliminatedPlayers:
                print(player, 'is eliminated: Non-valid Input')
                Eliminated = Eliminated + 1
        
        #Combination Check
        if 'All' in PlayerMoveTypes:
            if 'Single' in PlayerMoveTypes:
                print(player, 'is eliminated: Can not combine Neutral and Attacking Moves')
                Eliminated = Eliminated + 1
            elif len(PlayerMoveTypes) > 1 and len(PlayerMoveTypes) != PlayerMoves[player].count('Smoke Machine'):
                print(player, 'is eliminated: Can not use Neutral moves together unless the combined moves are all smoke machines')
                Eliminated = Eliminated + 1
        else:
            if 'Ghostgun' in PlayerMoves[player] and len(PlayerMoveTypes) != 1:
                print(player, 'is eliminated: Ghostgun can not be combined with other weapons')
                Eliminated = Eliminated + 1
            
        #Target Check
        if 'All' in PlayerMoveTypes and len(PlayerMoveTypes) < len(PlayerMoves[player]):
            print(player, 'is eliminated: Can not target on a neutral move')
            Eliminated = Eliminated + 1
        elif 'Single' in PlayerMoveTypes and len(PlayerMoveTypes) + 1 < len(PlayerMoves[player]):
            print(player, 'is eliminated: Can only have 1 target')
            Eliminated = Eliminated + 1
        
        #If inputs were invalid for any reason, the player is eliminated.
        if Eliminated > 0:
            EliminatedPlayers = EliminatedPlayers + [player]
        #If not eliminated, look at smokes/smokemachines
        elif 'Smoke' in PlayerMoves[player]:
            Smoked = Smoked + PlayerMoves[player].count('Smoke')
        elif 'Smoke Machine' in PlayerMoves[player]:
            SmokeMachined = SmokeMachined + PlayerMoves[player].count('Smoke Machine')
            NumSmokeMachinePlayers = NumSmokeMachinePlayers + 1

#Give the people their money (resources)
for player in NonEliminatedPlayers:
    for move in PlayerMoves[player]:
        if move in ResourceMovesList:
            PlayerResources[player][ResourceGainList[ResourceMovesList.index(move)]] = PlayerResources[player][ResourceGainList[ResourceMovesList.index(move)]] + 1

#Cancelling all moves due to smoke or smoke machine
if Smoked > 0 or SmokeMachined > 0:
    for player in PlayerMoves:
        removelist = []
        for move in PlayerMoves[player]:
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
        PlayerMoves[player] = [move for move in PlayerMoves[player] if move not in removelist]
#Now determine damage amounts
#Note, targeting players eliminated this round is still valid (since you can't predict their elimination)
#However when we consider moves, only consider players who did legal moves
for player in NonEliminatedPlayers:
    if player not in EliminatedPlayers:
        for move in PlayerMoves[player]:
            if move in Movedata:
                if 'Shield' in Movedata[move].keys():
                    PlayerDataframe.loc['Total', player] = PlayerDataframe.loc['Total', player] + float(Movedata[move]['Shield'])
                if 'Damage' in Movedata[move].keys():
                    if move == 'Smoke Machine':
                        for affectedplayer in NonEliminatedPlayers:
                            if affectedplayer != player:
                                PlayerDataframe.loc['Total', affectedplayer] = PlayerDataframe.loc['Total', affectedplayer] - float(Movedata[move]['Damage'])
                    else:
                        TargetPlayer = [move for move in PlayerMoves[player] if move not in Movedata][0]
                        #If we are ghostgun and they shoot at us (legally), we die
                        if move == 'Ghostgun' and player in PlayerMoves[TargetPlayer] and player not in EliminatedPlayers and len(PlayerMoves[TargetPlayer]) > 1:
                            EliminatedPlayers = EliminatedPlayers + [player]
                        #Otherwise, standard considerations
                        else:
                            #If reflected or portaled, attacker takes damage. Do not add as shielding for target player.
                            if 'Reflect' in PlayerMoves[TargetPlayer] and TargetPlayer not in EliminatedPlayers and move != 'Ghostgun':
                                PlayerDataframe.loc[TargetPlayer, player] = PlayerDataframe.loc[TargetPlayer, player] - float(Movedata[move]['Damage'])
                            elif 'Portal' in PlayerMoves[TargetPlayer] and TargetPlayer not in EliminatedPlayers:
                                PlayerDataframe.loc[TargetPlayer, player] = PlayerDataframe.loc[TargetPlayer, player] - float(Movedata[move]['Damage'])
                            else:
                                #Add damage to target player
                                PlayerDataframe.loc[player, TargetPlayer] = PlayerDataframe.loc[player, TargetPlayer] - float(Movedata[move]['Damage'])
                                #Also add shield in that direction only
                                PlayerDataframe.loc[TargetPlayer, player] = PlayerDataframe.loc[TargetPlayer, player] + float(Movedata[move]['Damage'])
    
for player in NonEliminatedPlayers:
    if player not in EliminatedPlayers:
        if PlayerDataframe.loc['Total', player] <= 0:
            if (PlayerDataframe.get(player).values < 0).any() ==True:
                EliminatedPlayers = EliminatedPlayers + [player]   
        elif PlayerDataframe[player].sum() < 0:
            EliminatedPlayers = EliminatedPlayers + [player]

#Remove all eliminated players
NonEliminatedPlayers = [player for player in NonEliminatedPlayers if player not in EliminatedPlayers]

print("Eliminated Players: ", EliminatedPlayers)
print("Non-Eliminated Players: ", NonEliminatedPlayers)


for player in NonEliminatedPlayers:
    print(player, PlayerResources[player])

    
#code in resources
#kill credit
      
            
        

    
    