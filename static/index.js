var socket = io();
var player_id = '';
var current_room = '';

socket.on('connect', function() {
    console.log("stinky");
    socket.emit('get_rooms');
});

socket.on('rooms_list', function(rooms) {
    var roomsListElement = document.getElementById('rooms_list');
    roomsListElement.innerHTML = '';
    rooms.forEach(function(room) {
        var li = document.createElement('li');
        li.textContent = room;
        
        var button = document.createElement("button");
        button.innerHTML = "Join Room";
        button.addEventListener('click', () => join_room(room));
        li.appendChild(button);

        roomsListElement.appendChild(li);
    });
});

function join_room(room_id) {
    if(!player_id) {
        alert("Invalid player id")
    } else {
        socket.emit('join_room', {room_id: room_id, player_id: player_id});
    }
}

function leave_room() {
    socket.emit('leave_room', {room_id: current_room, player_id: player_id});
}

function create_room() {
    if(!player_id) {
        alert("Invalid player id")
    } else {
        socket.emit('create_room', {player_id: player_id});
    }
}

socket.on('room_joined', function(data) {
    var players = data.players;
    var room_id = data.room_id;
    current_room = room_id;

    // change ui
    document.getElementById('login').style.display = 'none';
    document.getElementById('room').style.display = 'block';
    document.getElementById('current_room').textContent = 'Room ID: ' + current_room;
    
    var playerList = document.getElementById('player_list');
    playerList.innerHTML = '';
    if(players) {
        players.forEach(function(player) {
            var li = document.createElement('li');
            li.textContent = player;
            playerList.appendChild(li);
        });
    }
})

socket.on('room_left', function() {
    current_room = '';
    
    document.getElementById('login').style.display = 'block';
    document.getElementById('room').style.display = 'none';

    socket.emit('get_rooms');
})

socket.on('player_joined', function(data) {
    var new_player_id = data.player_id;

    // Add the player who joined
    var playerListElement = document.getElementById('player_list');
    var li = document.createElement('li');
    li.textContent = new_player_id;
    li.id = 'player-' + new_player_id;

    playerListElement.appendChild(li);
});

socket.on('player_left', function(data) {
    var left_player_id = data.player_id;

    // Remove the player who left
    var playerListElement = document.getElementById('player_list');
    var li = document.getElementById('player-' + left_player_id);

    if (li) {
        playerListElement.removeChild(li);
    }
});


document.getElementById('create_room').addEventListener('click', () => create_room());
document.getElementById('refresh_rooms').addEventListener('click', () => socket.emit('get_rooms'));
document.getElementById('leave_room').addEventListener('click', () => leave_room());
document.getElementById('player_id').addEventListener('change', function() {
    player_id = this.value;
});
