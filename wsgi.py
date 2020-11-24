from flask.globals import current_app
from app import create_app
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_login import current_user

from gamesdb import games

import logging

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = create_app()
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('getusers')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json)+' from '+current_user.dict['username'])
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('join')
def on_join(data):    
    username = current_user.dict['username']
    room = data['room']
    join_room(room)
    
    if int(room) in games:
        
        userdict = genuserdict(room)
        
        emit('userupdate',userdict, room=room, json=True)
    else:
        return False

def ack():
    print('message was received!')


@socketio.on('leave')
def on_leave(data):
    username = current_user.dict['username']
    room = data['room']
    print('leave event triggered by '+username)
    leave_room(room)
    
        #pop from arr - check admin stat, or if no players will be left

    
    if int(room) in games:
        if username in games[int(room)]['players']:
            if games[int(room)]['players'][current_user.dict['username']]['admin'] == True:
                if len(games[int(room)]['players']) >= 2:
                    print('move admin to antoher player')
                    for username  in games[int(room)]['players']:
                        print(games[int(room)]['players'][username]['admin'])
                        if games[int(room)]['players'][username]['admin'] == False:
                            games[int(room)]['players'][username]['admin'] = True
            print(games)
            print(f"popping{current_user.dict['username']}")
            games[int(room)]['players'].pop(current_user.dict['username'])
            print(games)
        
        if len(games[int(room)]['players']) == 0:
            games.pop(int(room))
        

        if int(room) in games and len(games[int(room)]['players']) != 0:
            userdict = genuserdict(room)
            print(userdict)
            emit('userupdate',userdict, room=room, json=True)
        else:
            return False

        send(username + ' has left the room.', room=room)
    

def genuserdict(room):
    userdict = {}
    for i, item in enumerate(games[int(room)]['players']):
        if games[int(room)]['players'][item]['admin'] == True:
            role = 'admin'
        else:
            role = 'default'
        userdict.update({str(item):str(role)})
    return userdict

if __name__ == "__main__":
    print('\n\n\nRunning\n-----------------')
    socketio.run(app, host='0.0.0.0', port=80)