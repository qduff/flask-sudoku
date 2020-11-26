import random
from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask.helpers import flash
from flask_login.utils import login_required, current_user
from werkzeug.urls import iri_to_uri

game = Blueprint('game', __name__)

from gamesdb import games

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
        #Create a room in the games dict
        
        if not password: password = None
        print(password)
        
        games.update({int(roomcode):{'name':roomname,'password':password,'started':False,'playersrequired':2,'players':{current_user.id['username']:{'completed':False,'timestarted':None,'admin':True}}}})
        
        #redirect to lobby
        return redirect(url_for('game.lobby',id=roomcode))
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
        return redirect(url_for('game.lobby',id=int(request.form.get('gamecode'))))#+'/'+request.form.get('gamecode'))
    except Exception as e:
        flash('Invalid input!')
        return redirect(url_for('game.joingame'))

@game.route('/authgame/<id>', methods=['POST'])
def auth_post(id):
    pw = request.form.get('gamepass')
    if pw == games[int(id)]['password']:
        games[int(id)]['players'].update({current_user.id['username']:{'completed':False,'admin':False}})
    
    return redirect(url_for('game.lobby',id=id)) #not efficitent but works


@game.route('/game/<id>')
@login_required
def lobby(id:int):
    global games
    
    try:
        if int(id) in games:
            #Check if game has started
            if games[int(id)]['started'] == True:
                flash('That game has already started!')
                return redirect(url_for('game.joingame'))
            
            #If not...
            else:                
                
                #If user has never joined this game, he will be added to dict.
                if current_user.dict['username'] not in games[int(id)]['players']:
                    
                    if games[int(id)]['password'] != None:
                        #Test if user has authed into the games
                        return render_template('enterpass.html', code=id)
                    else:
                        games[int(id)]['players'].update({current_user.id['username']:{'completed':False,'admin':False,'timestarted':None}})
                #If he is the admin, then he will get admin stuff!
                if games[int(id)]['players'][current_user.dict['username']]['admin'] == True:
                    admin = True
                else:
                    admin = False
                
                return render_template('lobby.html', gamecode = id, admin = admin,roomname =games[int(id)]['name'])
        else:
            flash('That game ID does not exist!')
            return redirect(url_for('game.joingame'))
    except:
        flash('That game ID is not valid!')
        return redirect(url_for('game.joingame'))


@game.route('/sudoku')
@login_required
def sudokutest():
    return render_template('sudoku.html')

@game.route('/play/<id>')
@login_required
def playpage(id):
    global games
    try:
    # Check if game exists
        if int(id) in games:
            # check if game has started
            if games[int(id)]['started'] == True:
                if current_user.dict['username'] in games[int(id)]['players']:
                    return render_template('sudoku.html',gamecode = id)
                else:
                    return redirect(url_for('game.lobby',id=id))
            else:
                # If not started, send to lobby with same id
                flash("That game hasn't started!")
                return redirect(url_for('game.lobby',id=id))
        else:
            flash('That game ID does not exist!')
            return redirect(url_for('game.joingame'))
    except:
        flash('That game ID is not valid!')
        return redirect(url_for('game.joingame'))