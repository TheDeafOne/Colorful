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
    login_manager.login_view = 'auth.get_login'  # type: ignore

    # function that takes a user id and
    @login_manager.user_loader
    def load_user(uid: int) -> database.User:
        return database.User.query.get(int(uid))  # type: ignore

def _setup_db(app: Flask):
    with app.app_context():
        database.db.init_app(app)

        # Reloads DB if the .env contains: RELOAD_DB="True"

        if(os.getenv("RELOAD_DB") == "True"):
            print("Reloading DB...\n") #
            database.db.drop_all()
            print("\n ^^^NOT AN ACTUAL ERROR^^^\n\nDatabases Dropped")
            database.db.create_all()
            try:
                # database.db.session.add(database.User(username="UserA", email="a@a.a", password=12345678))
                users = [
                    database.User(username="UserA", email="a@a.a", password="12345678"),
                    database.User(username="UserB", email="b@b.b", password="12345678"),
                    database.User(username="UserE", email="e@e.e", password="12345678")
                ]
                database.db.session.add_all(users)
                database.db.session.commit()
                stati = [
                    database.Status(
                        time="2022-09-20 10:27:21.240752",
                        text="Hi",
                        latitude="50",
                        longitude="50",
                        color= "#FF0000",
                        user=users[0].id),
                    database.Status(
                        time="2022-10-20 10:27:21.240752",
                        text="Hello",
                        latitude="60",
                        longitude="60",
                        color= "#00FF00",
                        user=users[1].id),
                    database.Status(
                        time="2022-11-20 10:27:21.240752",
                        text="Hello There",
                        latitude="50",
                        longitude="80",
                        color= "#0000FF",
                        user=users[2].id)
                ]
                database.db.session.add_all(stati)
                database.db.session.commit()

                for i in range(3):
                    users[i].currentStatusID = stati[i].id
                
                database.db.session.add_all(users)
                database.db.session.commit()

                print("Database Loaded")
            except:
                print("Database Re-Population Failed")

        else:
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
