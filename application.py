import os

from flask_login import LoginManager

from colorful import create_app
# from colorful.db import db
import colorful.db as database

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "users.sqlite3")

app = create_app()
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'NotDefault'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Prepare and connect the LoginManager to this app
login_manager = LoginManager()
login_manager.init_app(app)
# function name of the route that has the login form (so it can redirect users)
login_manager.login_view = 'colorful.auth.get_login'  # type: ignore

# function that takes a user id and


@login_manager.user_loader
def load_user(uid: int) -> database.User:
    return database.User.query.get(int(uid))  # type: ignore


with app.app_context():
    database.db.init_app(app)
    database.db.create_all()  # this is only needed if the database doesn't already exist

if __name__ == "__main__":
    app.run()
