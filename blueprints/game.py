from flask import Blueprint, render_template, redirect, url_for
from flask_login.utils import login_required, current_user

game = Blueprint('game', __name__)


#swap both
@game.route('/hostgame')
@login_required
def hostgame():
    if not current_user.is_guest():
        return render_template('hostgame.html')
    else:
        return redirect(url_for('main.index'))

@game.route('/joingame')
@login_required
def joingame():
    return render_template('joingame.html')
    

#Add joingame POST and hostgame POST