from flask import Blueprint, render_template, redirect,url_for, request, flash
from flask_login import login_user, UserMixin, LoginManager,login_required, current_user, logout_user
from db import checkusernameexistence, checklogin, getuserinfo, createaccount

auth = Blueprint('auth', __name__)

from models import User

@auth.route('/login')
def login():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        return redirect(url_for('auth.profile'))

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if not username or not password:
        flash('Username and password are required.')
        return redirect(url_for('auth.login'))
    
    userrow = checklogin(username, password)
    
    if not userrow:
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    else:
        usermodel = User(userrow['id'])
        login_user(usermodel, remember=remember)
        return redirect(url_for('auth.profile'))
    

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    
    if not username or not password:
        return render_template('signup.html',message = 'A username and password is required')

    usernameexistence, emailexistence = checkusernameexistence(username, email)

    if usernameexistence and emailexistence:
        flash('Username & E-Mail already exists')
        return redirect(url_for('auth.signup'))
        
    elif usernameexistence:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))
    elif emailexistence:
        flash('E-Mail already exists')
        return redirect(url_for('auth.signup'))

    #CREATEACCOUNT
    
    
    createaccount(username,password,email,request.remote_addr)
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    #print(email,username,password)

    flash('Account created')
    return redirect(url_for('auth.login'))



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')#, username = current_user.get_key('username'))



@auth.route('/update', methods=['POST'])
@login_required
def update_post():
    return redirect(url_for('auth.profile'))