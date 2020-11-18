from flask import Blueprint, render_template
from flask_login.utils import login_required

game = Blueprint('game', __name__)

@game.route('/hostgame')
@login_required
def hostgame():
    return render_template('hostgame.html')

@game.route('/joingame')
@login_required
def joingame():
    return render_template('joingame.html')
