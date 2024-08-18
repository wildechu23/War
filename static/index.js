var socket = io();

socket.on('connect', function() {
    console.log("stinky");
});

socket.on('status', function(data) {
    console.log(data.msg);
});

socket.on('update_rooms', function(data) {
    var roomList = document.getElementById("roomList");
    roomList.innerHTML = "";  // Clear the list
    for(const [key] in data.users) {
        var li = document.createElement("li");
        li.textContent = key;
        roomList.appendChild(li);
    };
});

socket.on('update_users', function(data) {
    var userList = document.getElementById("userList");
    userList.innerHTML = "";  // Clear the list
    data.users.forEach(function(user) {
        var li = document.createElement("li");
        li.textContent = user;
        if(data.leader == user) li.classList.add("leader")
        userList.appendChild(li);
    });
});

function join_room(room) {
    socket.emit('join_room', {room: room});
    document.getElementById('login').style.display = 'none';
    document.getElementById('room').style.display = 'block';
    document.getElementById('roomTitle').textContent = "Room: " + room;
}

document.getElementById("button1").onclick = () => join_room(1);
