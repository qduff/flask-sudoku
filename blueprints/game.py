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
    
@game.route('/hostgame', methods=['POST'])
def hostgame_post():
    if not current_user.is_guest():
        difficulty = request.form['difficulty']
        username= current_user.id['username']
        password = request.form.get('password')
        roomname = request.form.get('roomname')
        autoclear = False if (request.form.get('autoclear') == None) else True
        
        print(autoclear)
        
        if not password: password = None # unneccessary but whatever

        roomcode = addGame(roomname=roomname,gametype='sudoku',password=password,playersrequired=2, autoclear=autoclear, difficulty=difficulty)
        addUser(username=username,roomcode=roomcode,role='admin')
                
        return redirect(url_for('game.lobby',roomcode=roomcode))
    else:
        return render_template('guesterror.html')
    
@game.route('/joingame')
@login_required
def joingame():
    return render_template('joingame.html')

@game.route('/joingame', methods=['POST'])
def joingame_post():
    try:
        return redirect(url_for('game.lobby',roomcode=request.form.get('gamecode')))
    except:
        flash('Invalid input!')
        return redirect(url_for('game.joingame'))

@game.route('/authgame/<roomcode>', methods=['POST'])
def auth_post(roomcode):
    username = current_user.id['username']
    pw = request.form.get('gamepass')
            
    if pw == getGameProperty(roomcode,'password'): 
        addUser(username=username,roomcode=roomcode,role='default')
        
    return redirect(url_for('game.lobby',roomcode=roomcode)) #not efficitent but works


@game.route('/game/<roomcode>')
@login_required
def lobby(roomcode):
    username = current_user.id['username']

    try:
        if gameExists(roomcode):
            if  getGameProperty(roomcode,'started') == True:
                flash('That game has already started!')
                return redirect(url_for('game.joingame'))
            else:                
                if not playerExists(username=username, roomcode=roomcode):
                    if getGameProperty(roomcode, 'password') != None:
                        return render_template('enterpass.html', roomcode=roomcode)
                    else:
                        addUser(username,roomcode,'default')
                if playerRole(username, roomcode) == 'admin':
                    admin = True
                else:
                    admin = False
                return render_template('lobby.html', gamecode = roomcode, admin = admin, roomname = getGameProperty(roomcode, 'name'))
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
    username =  current_user.dict['username']
    try:
        if gameExists(roomcode):
            if getGameProperty(roomcode,'started') == True:
                if playerExists(username=username, roomcode=roomcode):
                    return render_template('sudoku.html',gamecode = roomcode)
                else:
                    return redirect(url_for('game.lobby',roomcode=roomcode))
            else:
                flash("That game hasn't started!")
                return redirect(url_for('game.lobby',roomcode=roomcode))
        else:
            flash('That game ID does not exist!')
            return redirect(url_for('game.joingame'))
    except ValueError:
        flash('That game ID is not valid!')
        return redirect(url_for('game.joingame'))