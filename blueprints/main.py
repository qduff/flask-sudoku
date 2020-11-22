from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from flask_login import current_user
import os
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

