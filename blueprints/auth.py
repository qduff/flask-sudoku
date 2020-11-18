from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from tinydb.queries import where
from werkzeug.security import check_password_hash
from datetime import timedelta
import random
from db import open_db
from models import User


auth = Blueprint('auth', __name__)


@open_db
def dbsearch(db, key, value):
    return db.search(where(key) == value)


@auth.route('/login')
def login():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        return redirect(url_for('auth.profile'))


@auth.route('/loginguest')
def loginguest():
    if not current_user.is_authenticated:
        
        #Generate a nickname
        words = ['cat', 'dog', 'word','game']
        nick = ''.join(random.choices(words, k=2))
        
        #Log in this user
        usermodel = User({'username': f"{nick}", 'guest': True})
        login_user(usermodel, remember=False, duration=timedelta(hours=1))
        
        #Redirect to profile page
        return redirect(url_for('auth.profile'))
    else:
        return redirect(url_for('auth.profile'))


@auth.route('/login', methods=['POST'])
def login_post():
    #Get form contents
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #see if values are existent
    if not username or not password:
        flash('Username and password are required.')
        return redirect(url_for('auth.login'))

    #Check if user exists
    try:
        user = dbsearch(key='username', value=username)
    except:
        user = False

    #If user exists, check password
    if user:
        credscorrect = check_password_hash(user[0]['password'], password)
    else:
        credscorrect = False

    if not credscorrect:
        #Refreshes page with message
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.login'))
    else:
        #Log in the user
        usermodel = User(user[0])
        login_user(usermodel, remember=remember)
        return redirect(url_for('auth.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])        #!NOT YET REIMPLEMENTED!!!
def signup_post():
    #Get form contents
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('signup.html', message='A username and password is required')

    usernameexistence = dbsearch(key='username', value=username)

    if usernameexistence:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    #! CREATEACCOUNT - not yet reimplemented

    flash('Account created')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    #Log out the user
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

