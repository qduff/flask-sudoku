import random
from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask.helpers import flash
from flask_login.utils import login_required, current_user
from werkzeug.urls import iri_to_uri

game = Blueprint('game', __name__)

from gamesdb import *

@game.route('/hostgame')
@login_required
def hostgame():
    if not current_user.is_guest():
        
        return render_template('hostgame.html')
    else:
        return render_template('guesterror.html')
        #return redirect(url_for('main.index'))
    
@game.route('/hostgame', methods=['POST'])
def hostgame_post():
    if not current_user.is_guest():
        password = request.form.get('password')
        roomname = request.form.get('roomname')
        codelen = 4
        roomcode = 0
        # Make roomcode
        while roomcode == 0 or roomcode in games:
            roomcode = ''.join(["{}".format(random.randint(1, 9)) for num in range(0, codelen)])
        print(f"New Room ({roomname}) created by {current_user.id['username']}\tCode:{roomcode}")

        
        if not password: password = None

        
        games.update({roomcode:{'name':roomname,'password':password,'started':False,'playersrequired':2,'players':{current_user.id['username']:{'completed':False,'timestarted':None,'role':'admin'}}}})
        #TODO add to ./gamesdb.py
        
        return redirect(url_for('game.lobby',roomcode=roomcode))
    else:
        return render_template('guesterror.html')
        #return redirect(url_for('main.index'))
    
@game.route('/joingame')
@login_required
def joingame():
    return render_template('joingame.html')

@game.route('/joingame', methods=['POST'])
def joingame_post():
    try:
        #Send to lobby with code
        return redirect(url_for('game.lobby',roomcode=request.form.get('gamecode')))#+'/'+request.form.get('gamecode'))
    except Exception as e:
        flash('Invalid input!')
        return redirect(url_for('game.joingame'))

@game.route('/authgame/<roomcode>', methods=['POST'])
def auth_post(roomcode):
    pw = request.form.get('gamepass')
    
    print(pw,games[roomcode]['password'] )
    
    if pw == games[roomcode]['password']: #TODO Getgameattr

        addUser(current_user.id['username'],roomcode,'default')
        #games[id]['players'].update({current_user.id['username']:{'completed':False,'role':'default'}})
    
    return redirect(url_for('game.lobby',roomcode=roomcode)) #not efficitent but works


@game.route('/game/<roomcode>')
@login_required
def lobby(roomcode):
    username = current_user.id['username']
    global games
    
    #if roomcode in games:
    #    print('YEAS!')
    
    try:
        print(f"{games=},{roomcode=}")
        if gameExists(roomcode):
            #Check if game has started
            if games[roomcode]['started'] == True:
                flash('That game has already started!')
                return redirect(url_for('game.joingame'))
            
            #If not...
            else:                
                
                #If user has never joined this game, he will be added to dict.
                if username not in games[roomcode]['players']:
                    
                    if games[roomcode]['password'] != None:
                        #Test if user has authed into the games
                        return render_template('enterpass.html', roomcode=roomcode)
                        #redirect(url_for('auth.authgame'))                   
                    else:
                        #games[roomcode]['players'].update({current_user.id['username']:{'completed':False,'role':'default','timestarted':None}})
                        addUser(username,roomcode,'default')
                        
                if playerRole(username, roomcode) == 'admin':
                    admin = True
                else:
                    admin = False
                
                return render_template('lobby.html', gamecode = roomcode, admin = admin,roomname = games[roomcode]['name'])
        else:
            flash('That game ID does not exist!')
            return redirect(url_for('game.joingame'))
    except ValueError:
        flash('That game ID is not valid!')
        return redirect(url_for('game.joingame'))


@game.route('/sudoku')
@login_required
def sudokutest():
    return render_template('sudoku.html')

@game.route('/play/<roomcode>')
@login_required
def playpage(roomcode):
    global games
    try:
    # Check if game exists
        if roomcode in games:
            # check if game has started
            if games[roomcode]['started'] == True:
                if current_user.dict['username'] in games[roomcode]['players']:
                    return render_template('sudoku.html',gamecode = roomcode)
                else:
                    return redirect(url_for('game.lobby',roomcode=roomcode))
            else:
                # If not started, send to lobby with same id
                flash("That game hasn't started!")
                return redirect(url_for('game.lobby',roomcode=roomcode))
        else:
            flash('That game ID does not exist!')
            return redirect(url_for('game.joingame'))
    except ValueError:
        flash('That game ID is not valid!')
        return redirect(url_for('game.joingame'))