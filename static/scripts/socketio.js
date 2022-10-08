document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    let room = "Lounge";
    joinRoom("Lounge");


    //Displays incoming messages
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.username) {
            span_username.innerHTML = data.username;
        span_timestamp.innerHTML = data.time_stamp;
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
        document.querySelector('#display-message-section').append(p);
        } else {
            printSysMsg(data.msg);
        }
    });
 
    //Send message
    document.querySelector('#send-message').onclick = () => {

        const msg_value = document.querySelector('#user-message').value;
        var dict = {
            'msg':msg_value,
            'username' : username, 
            'room': room }
        socket.send(dict);
        //Clear input area
        document.querySelector('#user-message').value = '';

    }
    //Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg= `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom
            }
        }
    });

    //Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room})
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room})
        //Clear message area
        document.querySelector('#display-message-section').innerHTML = '';
        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    //Print system message
    function printSysMsg (msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);

    }

    
})

