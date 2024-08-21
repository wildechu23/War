import uuid
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from game import EvaluateWarGame


app = Flask(__name__)
app.config['SECRET_KEY'] = '17190874a96010c7f46d80aa94a4c3662eeed60fa14ae121'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

rooms = {}
games = {}

def create_room(room_id):
    rooms[room_id] = {
        'players': [],
        'leader': '',
        'state': 'waiting',  # or 'playing', 'finished', etc.
    }

def create_game(room_id, players):
    games[room_id] = {
        'round': 1,
        'mode': 'default',
        'players': {},
        'moves': {},
        'alive': {},
        'profiles': {},
        'achievements':{}
    }
    for player in players:
        games[room_id]['players'][player] = {
            'Charges': 0,
            'Blocks': 0,
            'Magical Shards': 0,
            'Fumes': 0,
            'Doubles': 0,
            'Pew-Charge': 1,
        }
        games[room_id]['profiles'][player] = {
            'Wins': 0, 
            'Losses': 0, 
            'Total Kills': 0, 
            'Total Assists': 0,
            'Charges Acquired': 0,
            'Blocks Acquired': 0
        }
        games[room_id]['achievements'][player]= {
            'Noob': [],
            'Taste of Blood': [],
            'Enemy of my Enemy': [],
            'To the Victors': [],
            'Mutually Assured Destruction': [],
            'Close Call': [],
            'Sabotoge': [],
            'Thumbs Up!': [],
            'Bruh': [],
            'Stormtrooper': [],
            'Jack of All Trades': [],
            'Lack of All Trades': []
        }
        games[room_id]['moves'][player] = None
        games[room_id]['alive'][player] = True


@socketio.on('create_room')
def on_create_room(data):
    room_id = str(uuid.uuid4())
    print(room_id)
    player_id = data['player_id']

    if room_id not in rooms:
        create_room(room_id)
        rooms[room_id]['players'].append(player_id)
        rooms[room_id]['leader'] = player_id
        join_room(room_id)
        emit('room_joined', { 'room_id': room_id, 'leader': player_id })
        emit('player_joined', {'player_id': player_id, }, room=room_id)
    else:
        emit('error', {'message': 'Room already exists'})

@socketio.on('join_room')
def on_join(data):
    room_id = data['room_id']
    player_id = data['player_id']

    room = rooms.get(room_id)
    if room:
        emit('player_joined', {'player_id': player_id}, room=room_id)
        
        join_room(room_id)
        room['players'].append(player_id)
        emit('room_joined', { 
            'room_id': room_id, 
            'players': room['players'],
            'leader': room['leader']
        })
    else:
        # Handle room not found
        pass

@socketio.on('leave_room')
def on_leave(data):
    room_id = data['room_id']
    player_id = data['player_id']

    room = rooms.get(room_id)
    if room:
        emit('room_left')
        leave_room(room_id)
        room['players'].remove(player_id)
        emit('player_left', {'player_id': player_id}, room=room_id)

        if(len(room['players']) == 0):
            close_room(room_id)
            del rooms[room_id]
        

@socketio.on('get_rooms')
def on_get_rooms():
    available_rooms = [room_id for room_id, room in rooms.items() if room['state'] == 'waiting']
    emit('rooms_list', available_rooms)

@socketio.on('start_game')
def on_start_game(data):
    room_id = data['room_id']
    rooms[room_id]['state'] = 'playing'
    create_game(room_id, rooms[room_id]['players'])
    emit('start_game', {'players': rooms[room_id]['players']}, room=room_id)
    emit('update_game', games[room_id], room=room_id)

@socketio.on('submit_move')        
def on_submit_move(data):
    room_id = data['room_id']
    player_id = data['player_id']

    game = games[room_id]
    game['moves'][player_id] = { 'Moves': data['moves'], 'Target': data['target'] }
    
    # Check if all players have submitted their moves
    if all(m is not None for m in game['moves'].values()):
        process_moves(game)
        '''INSERT DISPLAY MOVES HERE'''
        game['round'] += 1
        emit('update_game', game, room=room_id)
        game['moves'] = dict.fromkeys(game['moves'], None)

        alive_players = [player_id for player_id, alive in game['alive'].items() if alive]
        if len(alive_players) <= 1:
            end_game(room_id, alive_players)

def end_game(room_id, alive_players):
    emit('end_game', {
        'winner': alive_players[0]
    } if len(alive_players) == 1 else {}, room=room_id)
    del games[room_id]
    rooms[room_id]['state'] = 'waiting'
        

def process_moves(game):
    ReturnInfo = EvaluateWarGame(game['mode'], [player for player in game['alive'] if game['alive'][player] == True], game['players'], game['moves'], game['profiles'], game['achievements'])
    #Update game alive, players, and profiles
    game['alive'] = {player: True if player in ReturnInfo['Remaining Players'] else False for player in game['alive']}
    game['players'] = {player: ReturnInfo['Remaining Player Resources'][player] if player in ReturnInfo['Remaining Players'] else game['players'][player] for player in game['alive']}
    game['profiles'] = {player: ReturnInfo['Updated Player Profiles'][player] if player in ReturnInfo['Updated Player Profiles'] else game['profiles'][player] for player in game['alive']}
    game['achievements'] = {player: ReturnInfo['Updated Player Achievements'][player] if player in ReturnInfo['Updated Player Achievements'] else game['achievements'][player] for player in game['alive']}
    print(game['alive'])
    print(game['players'])
    print(game['profiles'])
    
    for key, player in game['moves'].items():
        print(key)
        for move in player['Moves']:
            print(move)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
