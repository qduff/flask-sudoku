from app import create_app
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_login import current_user
from gamesdb import games
from flask.helpers import url_for
from sudokutools.generate import generate

app = create_app()

socketio = SocketIO(app)

###############################################
#################    LOBBY   ##################
###############################################

@socketio.on('getusers')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json)+' from '+current_user.dict['username'])
    print('sending user')
    socketio.emit('my response', json)
    
@socketio.on('join')
def on_join(data):    
    username = current_user.dict['username']
    room = data['room']
    join_room(room)
    #whyh is the pla
    if int(room) in games:
        userdict = genuserdict(room)
        print(games[int(room)]['players'])
        print('userupdate')
        emit('userupdate',userdict, room=room, json=True)
    else:
        return False
    
@socketio.on('leave')
def on_leave(data):
    username = current_user.dict['username']
    room = data['room']
    print('leave event triggered by '+username)
    leave_room(room)    
    if int(room) in games:
        if username in games[int(room)]['players']:
            if games[int(room)]['players'][current_user.dict['username']]['admin'] == True:
                if len(games[int(room)]['players']) >= 2:
                    print('move admin to antoher player')
                    for username  in games[int(room)]['players']:
                        print(games[int(room)]['players'][username]['admin'])
                        if games[int(room)]['players'][username]['admin'] == False:
                            games[int(room)]['players'][username]['admin'] = True
            print(f"popping {current_user.dict['username']}")
            games[int(room)]['players'].pop(current_user.dict['username'])        
        if len(games[int(room)]['players']) == 0:
            games.pop(int(room))
        if int(room) in games and len(games[int(room)]['players']) != 0:
            userdict = genuserdict(room)
            print(userdict)
            emit('userupdate',userdict, room=room, json=True)
        else:
            return False
        send(username + ' has left the room.', room=room)
    
@socketio.on('requestgamestart')
def onrequestgamestart(data):
    username = current_user.dict['username']
    room = data['room']
    print('starrt event triggered by '+username)
    if int(room) in games:
        nplayers = len(games[int(room)]['players'])
        if nplayers >=2:
            if games[int(room)]['players'][username]['admin'] == True:
                print('you may start!, sending start')
                url = str(url_for('game.playpage', id=room))
                json = {'url':url}
                json['players'] = genuserdict(room)
                games[int(room)]['started'] = True
                
                #sudoku, sol = generate()
                #GEN SUDOKU
                
                emit('startgame',json, room=room, json=True)
            else: return emit('cannotstart',{'msg':f'You are not an admin.'}, json=True)
        else: emit('cannotstart',{'msg':f"At least {games[int(room)]['playersrequired']} Players required to start, only {nplayers} in the lobby."}, json=True)
   
      
      
      
###############################################
#################    GAME   ###################
############################################### 
      

@socketio.on('requestsudoku')
def onrequestgamestart(data):
    #send the sudoku, and start the timer. 
    emit('sudokustr',{'content':f'sudstring'}, json=True)
    




def genuserdict(room):
    userdict = {}
    for i, item in enumerate(games[int(room)]['players']):
        if games[int(room)]['players'][item]['admin'] == True:
            role = 'admin'
        else:
            role = 'default'
        userdict.update({str(item):str(role)})
    return userdict