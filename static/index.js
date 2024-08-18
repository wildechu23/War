var socket = io();
var player_id = '';

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
    }
    socket.emit('join_room', {room_id: room_id, player_id: player_id});
}

function create_room() {
    if(!player_id) {
        alert("Invalid player id")
    } else {
        socket.emit('create_room', {player_id: player_id});
    }
}

socket.on('room_joined', function(data) {
    // change ui
    document.getElementById('login').style.display = 'none';
    document.getElementById('room').style.display = 'block';
    document.getElementById('current_room').textContent = 'Room ID: ' + data.room_id;
})

socket.on('player_joined', function(data) {
    var new_player_id = data.player_id;

    // Add the player who joined
    var playerListElement = document.getElementById('player_list');
    var li = document.createElement('li');
    li.textContent = new_player_id;
    playerListElement.appendChild(li);
});


document.getElementById('create_room').addEventListener('click', () => create_room());
document.getElementById('player_id').addEventListener('change', function() {
    player_id = this.value;
});
