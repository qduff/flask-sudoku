from flask import Flask
from flask_login import LoginManager 
from flask_assets import Environment

    
def create_app():
    #Create Flask App
    
    app = Flask(__name__)
    app.logger.disabled = True
    app.secret_key = 'secretweewooa8gn(^(_g0m9z8u2nnmxv!w$75yf5wx#3als9a)9hmdc&&=+za'
    app.debug=True
    #SASS assets
    assets = Environment(app)
    assets.register('scss_all', 'sass/main.scss', filters='pyscss', output='static/css/all.css') # you can add more scss files
    
    #Loginmanager init
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You must login to access this page!'
    login_manager.init_app(app)
    
    #User model
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
    
    # blueprint for auth routes in app
    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from blueprints.game import game as game_blueprint
    app.register_blueprint(game_blueprint)
    
    return app
