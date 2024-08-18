from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = '17190874a96010c7f46d80aa94a4c3662eeed60fa14ae121'
socketio = SocketIO(app)

rooms_users = {}
rooms_leaders = {}

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('update_rooms', {'users': rooms_users})
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    if room not in rooms_users:
        rooms_users[room] = []
        rooms_leaders[room] = request.sid
    rooms_users[room].append(request.sid)
    emit('update_users', {
        'users': rooms_users[room],
        'leader': rooms_leaders[room]
    }, room=room)

if __name__ == '__main__':
    socketio.run(app)

