import uuid
from . import socketio
from flask_socketio import Namespace, emit, join_room, leave_room, close_room
from .game import EvaluateWarGame, getAchievementDescriptions
from .db import get_username, get_missing_achievements, get_achievements, get_user, get_user_profile, update_profile

rooms = {}
games = {}

class MainNamespace(Namespace):
    def create_room(self, room_id):
        rooms[room_id] = {
            'players': [],
            'leader': '',
            'state': 'waiting',  # or 'playing'
        }

    def create_game(self, room_id, players):
        games[room_id] = {
            'round': 1,
            'mode': 'default',
            'players': {},
            'moves': {},
            'alive': {},
            'profiles': {},
            'achievements': {},
            'achievementDescriptions': getAchievementDescriptions()
        }

        for player_obj in players:
            player_id = player_obj['player_id']

            games[room_id]['players'][player_id] = {
                'Username': player_obj['username'],
                'Charges': 0,
                'Blocks': 0,
                'Magical Shards': 0,
                'Fumes': 0,
                'Doubles': 0,
                'Pew-Charge': 1,
            }

            user = get_user_profile(player_id)
            games[room_id]['profiles'][player_id] = {
                'Wins': user[2], 
                'Losses': user[3], 
                'Total Kills': user[4], 
                'Total Assists': user[5],
                'Charges Acquired': user[6],
                'Blocks Acquired': user[7]
            }

            missing = get_missing_achievements(player_id)
            games[room_id]['achievements'][player_id] = {}
            for achievement in missing:
                games[room_id]['achievements'][player_id][achievement['Title']] = False
            
            games[room_id]['moves'][player_id] = None
            games[room_id]['alive'][player_id] = True


    def on_create_room(self, data):
        room_id = str(uuid.uuid4())
        print(room_id)
        player_id = data['player_id']

        if room_id not in rooms:
            self.create_room(room_id)
            username = get_username(player_id)

            rooms[room_id]['players'].append({ 'player_id': player_id, 'username': username })
            rooms[room_id]['leader'] = player_id
            join_room(room_id)
            emit('room_joined', { 'room_id': room_id, 'leader': player_id })
            emit('player_joined', {'player_id': player_id, 'username': username}, room=room_id)
        else:
            emit('error', {'message': 'Room already exists'})

    def on_join_room(self, data):
        room_id = data['room_id']
        player_id = data['player_id']

        room = rooms.get(room_id)
        if room:
            username = get_username(player_id)
            emit('player_joined', {'player_id': player_id, 'username': username}, room=room_id)
            
            join_room(room_id)
            
            room['players'].append({ 'player_id': player_id, 'username': username })
            emit('room_joined', { 
                'room_id': room_id, 
                'players': room['players'],
                'leader': room['leader']
            })
        else:
            # Handle room not found
            pass

    def on_leave_room(self, data):
        room_id = data['room_id']
        player_id = data['player_id']

        room = rooms.get(room_id)
        if room:
            emit('room_left')
            leave_room(room_id)
            room['players'] = [player for player in room['players'] if player['player_id'] != player_id]
            emit('player_left', {'player_id': player_id}, room=room_id)

            if(len(room['players']) == 0):
                close_room(room_id)
                del rooms[room_id]
            
    def on_get_user(self):
        user = get_user()
        if user:
            emit('user', {'id': user[0], 'username': user[1]})
        

    def on_get_rooms(self):
        available_rooms = [room_id for room_id, room in rooms.items() if room['state'] == 'waiting']
        emit('rooms_list', available_rooms)

    def on_start_game(self, data):
        room_id = data['room_id']
        rooms[room_id]['state'] = 'playing'
        self.create_game(room_id, rooms[room_id]['players'])

        emit('start_game', {}, room=room_id)
        emit('update_game', games[room_id], room=room_id)

    def on_get_achievements(self, data):
        emit('update_achievements', [dict(row) for row in get_achievements(data['player_id'])])

    def on_submit_move(self, data):
        room_id = data['room_id']
        player_id = data['player_id']

        game = games[room_id]
        game['moves'][player_id] = { 'Moves': data['moves'], 'Target': data['target'] }
        
        # Check if all players have submitted their moves
        if all(m is not None for m in game['moves'].values()):
            self.process_moves(game)
            '''INSERT DISPLAY MOVES HERE'''
            game['round'] += 1
            emit('update_game', game, room=room_id)
            game['moves'] = dict.fromkeys(game['moves'], None)

            alive_players = [player_id for player_id, alive in game['alive'].items() if alive]
            if len(alive_players) <= 1:
                self.end_game(room_id, alive_players)

    def end_game(self, room_id, alive_players):
        self.update_profiles(games[room_id]['profiles'])
        emit('end_game', {
            'winner': alive_players[0]
        } if len(alive_players) == 1 else {}, room=room_id)
        del games[room_id]
        rooms[room_id]['state'] = 'waiting'

    def update_profiles(self, profiles):
        for id, profile in profiles.items():
            update_profile(id, profile)
            

    def process_moves(self, game):
        ReturnInfo = EvaluateWarGame(
            game['mode'], 
            [player for player in game['alive'] if game['alive'][player] == True], 
            [player['player_id'] for player in game['players']], 
            game['moves'], 
            game['profiles'], 
            game['achievements']
        )
        #Update game alive, players, and profiles
        game['alive'] = {
            player: True if player in ReturnInfo['Remaining Players'] 
                else False for player in game['alive']
        }
        game['players'] = {
            player: ReturnInfo['Remaining Player Resources'][player] 
                if player in ReturnInfo['Remaining Players'] 
                else game['players'][player] for player in game['alive']
        }
        game['profiles'] = {
            player: ReturnInfo['Updated Player Profiles'][player] 
                if player in ReturnInfo['Updated Player Profiles'] 
                else game['profiles'][player] for player in game['alive']
        }
        game['achievements'] = {
            player: ReturnInfo['Updated Player Achievements'][player] 
                if player in ReturnInfo['Updated Player Achievements'] 
                else game['achievements'][player] for player in game['alive']
        }
        print(game['alive'])
        print(game['players'])
        print(game['profiles'])
        
        for key, player in game['moves'].items():
            print(key)
            for move in player['Moves']:
                print(move)
