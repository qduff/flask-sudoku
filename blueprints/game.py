from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask.helpers import flash
from flask_login.utils import login_required, current_user

import random 

game = Blueprint('game', __name__)

games = {1234:{'started':False,'players':[]}}

#swap both
@game.route('/hostgame')
@login_required
def hostgame():
    if not current_user.is_guest():
        return render_template('hostgame.html')
    else:
        return redirect(url_for('main.index'))
    
@game.route('/hostgame', methods=['POST'])
def hostgame_post():
    roomname = request.form.get('roomname')
    codelen = 10
    roomcode = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, codelen)])

@game.route('/joingame')
@login_required
def joingame():
    return render_template('joingame.html')

@game.route('/joingame', methods=['POST'])
def joingame_post():
    try:
        return redirect(url_for('game.gamepage',id=int(request.form.get('gamecode'))))#+'/'+request.form.get('gamecode'))
    except:
        flash('Invalid input!')
        return redirect(url_for('game.joingame'))


@game.route('/game/<id>')
@login_required
def gamepage(id):
    global games
    print(id,games)
    if int(id) in games:
        return render_template('sudoku.html')
    else:
        flash('That game ID does not exist!')
        return redirect(url_for('game.joingame'))
    

#Add joingame POST and hostgame POST