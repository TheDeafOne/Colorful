import os

from flask import Flask
from flask_login import LoginManager

from colorful.api import api_bp
from colorful.auth import auth_bp
from colorful.main import main_bp

import colorful.db as database

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "users.sqlite3")

def _setup_login(app: Flask):
    # Prepare and connect the LoginManager to this app
    login_manager = LoginManager()
    login_manager.init_app(app)

    # function name of the route that has the login form (so it can redirect users)
    login_manager.login_view = 'colorful.auth.get_login'  # type: ignore

    # function that takes a user id and
    @login_manager.user_loader
    def load_user(uid: int) -> database.User:
        return database.User.query.get(int(uid))  # type: ignore

def _setup_db(app: Flask):
    with app.app_context():
        database.db.init_app(app)
        database.db.create_all()  # this is only needed if the database doesn't already exist

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SECRET_KEY'] = 'NotDefault'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api/')

    _setup_login(app)
    _setup_db(app)

    return app
