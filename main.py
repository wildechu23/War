import uuid
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room

app = Flask(__name__)
app.config['SECRET_KEY'] = '17190874a96010c7f46d80aa94a4c3662eeed60fa14ae121'
socketio = SocketIO(app)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

rooms = {}

def create_room(room_id):
    rooms[room_id] = {
        'players': [],
        'leader': '',
        'state': 'waiting',  # or 'playing', 'finished', etc.
    }

@socketio.on('create_room')
def on_create_room(data):
    room_id = str(uuid.uuid4())
    print(room_id)
    player_id = data['player_id']

    if room_id not in rooms:
        create_room(room_id)
        rooms[room_id]['players'].append(player_id)
        join_room(room_id)
        emit('room_joined', { 'room_id': room_id })
        emit('player_joined', {'player_id': player_id}, room=room_id)
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
            'players': room['players']
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
        

if __name__ == '__main__':
    socketio.run(app, debug=True)
