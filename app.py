from flask import Flask
from flask_login import LoginManager , UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle

# init SQLAlchemy so we can use it later in our models
    
def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretweewooa8gn(^(_g0m9z8u2nnmxv!w$75yf5wx#3als9a)9hmdc&&=+za'
    app.debug=True
    
    
    assets = Environment(app)
    
    assets.register('scss_all', 'sass/_basics.scss', 'sass/button.scss', filters='pyscss', output='static/css/all.css')
    print('re')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You must login to access this page!'
    login_manager.init_app(app)
    
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
    
    # blueprint for auth routes in our app
    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



