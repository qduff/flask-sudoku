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
        
        #Redirect to main page after guest login
        return redirect(url_for('main.index'))
    else:
        #if already loggen in maybe check if guest idk?
        return redirect(url_for('main.index'))


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

    print(f"Login entered= {username=},{password=},{remember=},{user=},{credscorrect=}")

    if not credscorrect:
        #Refreshes page with message
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.login'))
    else:
        #Log in the user
        usermodel = User(user[0])
        login_user(usermodel, remember=remember)
        return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])        # !NOT YET REIMPLEMENTED!!!
def signup_post():
    # Get form contents
    # Todo: clean this up
    # Todo: also make it work
    username = request.form.get('username')
    password = request.form.get('password')

    # Check presence of username and password
    if not username and not password:
        flash('A username and password is required')
        return render_template('signup.html')
    if not username:
        flash('A username is required')
        return render_template('signup.html')
    if not password:
        flash('A password is required')
        return render_template('signup.html')

    # Check if username already exists
    usernameexistence = dbsearch(key='username', value=username)

    # If it does, flask warning and refresh.
    if usernameexistence:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))
    
    if len(password) < 8:
        flash('Password must be at least eight characters long')
        return render_template('signup.html')

    # ! CREATEACCOUNT - not yet reimplemented

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
    if not current_user.is_guest():
        return render_template('profile.html')
    else:   
        return render_template('guesterror.html')