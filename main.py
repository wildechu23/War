import uuid
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
# from game import *


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
        'players': [],
        'moves': {},
        'alive': {}
    }
    for player in players:
        games[room_id]['players'].append({
            'id': player,
            'charges': 0,
            'blocks': 0,
            'magical shards': 0,
            'fumes': 0,
            'doubles': 0,
            'pew-charge': 1,
        })
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
    game['moves'][player_id] = { 'moves': data['moves'], 'target': data['target'] }
    
    # Check if all players have submitted their moves
    if all(m is not None for m in game['moves'].values()):
        process_moves(game['moves'])
        game['round'] += 1
        emit('update_game', game, room=room_id)
        game['moves'] = {}

        alive_players = [player_id for player_id, alive in game['alive'].items() if alive]
        if len(alive_players) <= 1:
            end_game(room_id, alive_players)

def end_game(room_id, alive_players):
    emit('end_game', {
        'winner': alive_players[0]
    } if alive_players else {
        'winner': {}
    }, room=room_id)
    del games[room_id]
    rooms[room_id]['state'] = 'waiting'
        

def process_moves(moves):
    for key, player in moves.items():
        print(key)
        for move in player['moves']:
            print(move)


if __name__ == '__main__':
    socketio.run(app, debug=True)
