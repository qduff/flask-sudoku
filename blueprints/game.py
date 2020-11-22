from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask.helpers import flash
from flask_login.utils import login_required, current_user

import random

#needs to be able to send here

game = Blueprint('game', __name__)

from gamesdb import games
#from wsgi import socketio

@game.route('/hostgame')
@login_required
def hostgame():
    if not current_user.is_guest():
        return render_template('hostgame.html')
    else:
        return redirect(url_for('main.index'))
    
@game.route('/hostgame', methods=['POST'])
def hostgame_post():
    #print(current_user.id['username'])
    roomname = request.form.get('roomname')
    codelen = 4
    roomcode = 0
    while roomcode == 0 or roomcode in games:
        roomcode = ''.join(["{}".format(random.randint(1, 9)) for num in range(0, codelen)])
    print(f"New Room ({roomname}) created by {current_user.id['username']}\tCode:{roomcode}")
    games.update({int(roomcode):{'name':roomname,'started':False,'players':{current_user.id['username']:{'completed':False,'admin':True}}}})
    return redirect(url_for('game.lobby',id=roomcode))
    
    
@game.route('/joingame')
@login_required
def joingame():
    return render_template('joingame.html')

@game.route('/joingame', methods=['POST'])
def joingame_post():
    try:
        return redirect(url_for('game.lobby',id=int(request.form.get('gamecode'))))#+'/'+request.form.get('gamecode'))
    except Exception as e:
        flash('Invalid input!')
        print(e)
        return redirect(url_for('game.joingame'))


@game.route('/game/<id>')
@login_required
def lobby(id:int):
    global games
    #print(id,games)
    if int(id) in games:
        if games[int(id)]['started'] == True:
            flash('That game has already started!')
            return redirect(url_for('game.joingame'))
        else:
            if current_user.dict['username'] not in games[int(id)]['players']:
                games[int(id)]['players'].update({current_user.id['username']:{'completed':False,'admin':False}})
            print(games)
                
            if games[int(id)]['players'][current_user.dict['username']]['admin'] == True:
                admin = True
            else:
                admin = False
            
            return render_template('lobby.html', gamecode = id, admin = admin,roomname =games[int(id)]['name'])
    else:
        flash('That game ID does not exist!')
        return redirect(url_for('game.joingame'))



@game.route('/play/<id>')
@login_required
def playpage(id):
    global games
    print(id,games)
    if int(id) in games:
        if games[int(id)]['started'] == True:
            return render_template('sudoku.html')
        else:
            flash("That game hasn't started!")
            return redirect(url_for('game.lobby',id=id))
    else:
        flash('That game ID does not exist!')
        return redirect(url_for('game.joingame'))
    

#Add joingame POST and hostgame POST

