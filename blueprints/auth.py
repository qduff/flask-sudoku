from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from tinydb.queries import where
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from datetime import timedelta
import random
from models import User

auth = Blueprint('auth', __name__)

from tinydb import TinyDB


def dbsearch( key, value):
    db = TinyDB('users.json', indent=4)
    resp =  db.search(where(key) == value)
    db.close()
    return resp

def dbadduser( username, password):
    db = TinyDB('users.json', indent=4)
    resp =   db.insert({'username':username,'password':generate_password_hash(password,'sha256')})
    db.close()
    return resp

@auth.route('/login')
def login():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        return redirect(url_for('auth.profile'))


@auth.route('/loginguest')
def loginguest():
    if not current_user.is_authenticated:
        nick = ''.join(random.choices(open('words.txt').read().split(), k=2))+str(random.randint(100,999))
        
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
    
    user = dbsearch(key='username', value=username)
    

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
        
        #Not working apparently
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('main.index'))
        else:
            redirect(next_page)


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
        return redirect(url_for('auth.signup'))
    if not username:
        flash('A username is required')
        return redirect(url_for('auth.signup'))
    if not password:
        flash('A password is required')
        return redirect(url_for('auth.signup'))

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
    dbadduser(username=username, password=password)
    
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