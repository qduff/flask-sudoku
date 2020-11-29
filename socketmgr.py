from os import name
from app import create_app
from flask_socketio import SocketIO, send, join_room, leave_room, emit, rooms
from flask_login import current_user
from gamesdb import *
from flask.helpers import url_for
import datetime
from sudokutools.generate import generate

app = create_app()

socketio = SocketIO(app)

###############################################
#################    LOBBY   ##################
###############################################

#@socketio.on('getusers')
#def handle_my_custom_event(json):
#    socketio.emit('my response', json)
    

@socketio.on('join')
def on_join(data):
    username = current_user.dict['username']
    
    roomcode = data['room']
    
    
    if gameExists(roomcode):
        join_room(roomcode)
        print(f'{username} has joined the room')
        if roomcode in games:  # wut
            userdict = genuserdict(roomcode)
            emit('userupdate', userdict, room=roomcode, json=True)
        else:
            return False


@socketio.on('leave')
def on_leave(data):
    username = current_user.dict['username']
    roomcode = data['room']
    
    leave_room(roomcode)

    if gameExists(roomcode):
        
        #if username in games[roomcode]['players']:
        if playerExists(username, roomcode):
            #if games[roomcode]['players'][current_user.dict['username']]['admin'] == True:
            if playerCount(roomcode) >= 2:

                if playerRole(username, roomcode) == 'admin':

                    #move admin to antoher playre
                    
                    for username in players(roomcode):
                        #print(games[roomcode]['players'][username]['role'])
                        if playerRole(username,roomcode) == 'admin':
                            changeRole(username,roomcode,'admin')

            else:
                removeGame(roomcode)
                #games.pop(roomcode)#remove game
                            
            removeUser(username, roomcode)

              
        if gameExists(roomcode) and playerCount(roomcode) != 0:
            userdict = genuserdict(roomcode)
            emit('userupdate',userdict, room=roomcode, json=True)
        else:
            return False
        send(username + ' has left the room.', room=roomcode)


@socketio.on('requestgamestart')
def onrequestgamestart(data):
    username = current_user.dict['username']
    roomcode = data['room']
    print('starrt event triggered by '+username)
    if roomcode in games:
        nplayers = len(games[roomcode]['players'])
        if nplayers >=2:
            if playerRole(username, roomcode) == 'admin':
                print('you may start!, sending start')
                url = str(url_for('game.playpage', id=roomcode))
                json = {'url':url}
                json['players'] = genuserdict(roomcode)
                games[roomcode]['started'] = True
                
                sudoku, solution = generate()
                #GEN SUDOKU
                games[roomcode]['sudoku'] = sudoku
                games[roomcode]['sudokusol'] = solution


                emit('startgame',json, room=roomcode, json=True)
            else: return emit('cannotstart',{'msg':f'You are not an admin.'}, json=True)
        else: emit('cannotstart',{'msg':f"At least {games[roomcode]['playersrequired']} Players required to start, only {nplayers} in the lobby."}, json=True)

      
###############################################
#################    GAME   ###################
############################################### 
      

@socketio.on('requestsudoku')
def onrequestgamestart(data):
    username = current_user.dict['username']
    roomcode = data['room']
    

    if roomcode == "":
        return

    if roomcode in games:
        
        join_room(roomcode)

        
        if games[roomcode]['players'][username]['timestarted'] == None:
            games[roomcode]['players'][username]['timestarted'] = datetime.datetime.now()

        if games[roomcode]['players'][username]['completed'] == False:
            emit('sudokustr', {'content': games[roomcode]['sudoku']}, json=True)
        else: # Covers refresh case
            emit('completed', getcompletedjson(roomcode,username) ,json=True)

        # send complete table, so the player has a table (DOES _NOT_ have to be to room but might as well)
        emit('tableupdate', gencompletiondict(room=roomcode), json=True, room=roomcode)
        
    else: # Does nothing on client side, futureproofing, i guess
        emit('redirect', {'url': f"/"}, json=True)


@socketio.on('submitsudoku')
def sudokusubmit(data):
    username = current_user.dict['username']
    roomcode = data['room']

    if roomcode == "": 
        return
    
    #check that user has not already completed the sudoku (done), and started
    if games[roomcode]['players'][username]['completed'] == False:  # does this even work? apparently. 
        if int(games[roomcode]['sudokusol']) == int(data['string']):
            time = datetime.datetime.now() - games[roomcode]['players'][username]['timestarted']
            games[roomcode]['players'][username]['completed'] = time
            
            
            emit('completed', getcompletedjson(roomcode,username) ,json=True)

        # send complete table, regardless of correctness
        emit('tableupdate', gencompletiondict(roomcode), json=True, room=roomcode)
            
    else: # If already done (shouldnt happen)
        emit('completed', getcompletedjson(roomcode,username) ,json=True)



def getcompletedjson(room,username):
    return {'place':f'You came in {1} Place!','time': f"Completed in {round(games[room]['players'][username]['completed'].total_seconds(),1)}s!"}
    #TODO DO PLACE FUNCTIONALITY


def gencompletiondict(room):  # do progress also, and order by completion
    completiondict = {}
    for item in games[room]['players']:
        print(item)
        
        if playerRole(item, room) == 'admin':
            role = 'admin'
        else:
            role = 'default'
        
        if games[room]['players'][item]['completed'] == False:
            completed = 'false'
        else:
            completed = str(round(games[room]['players'][item]['completed'].total_seconds(),1))+'s'
        
        tempdict = {'role':str(role), 'completed':completed}
        print(tempdict)
        completiondict[str(item)] = tempdict
        #TODO Progress indicator on server _and_ client

    return completiondict


def genuserdict(room):
    userdict = {}
    for item in games[room]['players']:
        if playerRole(item, room) == 'admin':
            role = 'admin'
        else:
            role = 'default'
        userdict.update({str(item): str(role)})
    return userdict
