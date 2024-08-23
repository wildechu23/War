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
        li.append(button);

        roomsListElement.append(li);
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
    if(data.leader === player_id) {
        document.getElementById('start_game').disabled = false;
    }
    
    var playerList = document.getElementById('player_list');
    playerList.innerHTML = '';
    if(players) {
        players.forEach(function(player) {
            var li = document.createElement('li');
            li.textContent = player;
            playerList.append(li);
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

    playerListElement.append(li);
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

socket.on('start_game', function(data) {
    document.getElementById('room').style.display = 'none';
    document.getElementById('game').style.display = 'block';
});


socket.on('update_game', function(game) {
    var roundNumber = document.getElementById('round_number');
    roundNumber.innerHTML = 'Round ' + game.round;

    var gameState = document.getElementById('game_state');
    var tbodyRef = gameState.getElementsByTagName('tbody')[0];
    tbodyRef.innerHTML = '';
    for (const [id, player] of Object.entries(game.players)) {
        var tr = document.createElement('tr');
        var idElement = document.createElement('td');
        idElement.textContent = idElement;
        tr.append(id);

        for (const [key, value] of Object.entries(player)) {
            var td = document.createElement('td');
            td.textContent = value;
            tr.append(td);
        }

        var lastMove = document.createElement('td');
        if(game.moves[id]) {
            lastMove.textContent = game.moves[id].Moves.join();
        }
        tr.append(lastMove);
        
        if(game.alive[player_id] == false) {
            tr.style.backgroundColor = 'gray';
            tbodyRef.append(tr);
        } else if(id == player_id) {
            tr.style.backgroundColor = 'rgba(150, 212, 212, 0.4)';
            tbodyRef.prepend(tr);
        } else {
            tbodyRef.append(tr);
        }
    }
    var achievementUpdate = document.getElementById('achievement_ui');
    achievementUpdate.innerHTML = '';
    for ([achievement, progress] of Object.entries(game.achievements[player_id])) {
        var tr = document.createElement('tr');
            var td = document.createElement('td');
            td.style.color = '#f1f1f1'
            td.textContent = achievement
            tr.append(td)
            var td = document.createElement('td');
                if(progress == 'Unlocked'){
                    td.style.color = '#f1f1f1'
                    td.textContent = progress
                    tr.append(td)
                }
                else{
                    td.textContent = 'Locked'
                    tr.append(td)
                }
        achievementUpdate.append(tr)
    }
});

socket.on('end_game', function(data) {
    var winner = data.winner;
    if(winner) {
        alert(winner + " wins!")
    } else {
        alert("No one wins")
    }
    document.getElementById('room').style.display = 'block';
    document.getElementById('game').style.display = 'none';
})

function submit_move() {
    var str = document.getElementById('move_list').value;
    var target = document.getElementById('move_target').value;
    var moves = str.split(',');
    socket.emit('submit_move', {
        room_id: current_room,
        player_id: player_id,
        moves: moves,
        target: target,
    })
}


document.getElementById('player_id').addEventListener('change', function() {
    player_id = this.value;
});

document.getElementById('create_room').addEventListener('click', () => create_room());
document.getElementById('refresh_rooms').addEventListener('click', () => 
    socket.emit('get_rooms')
);

document.getElementById('leave_room').addEventListener('click', () => leave_room());
document.getElementById('start_game').addEventListener('click', () => 
    socket.emit('start_game', {room_id: current_room})
);


document.getElementById('submit_move').addEventListener('click', () => submit_move());