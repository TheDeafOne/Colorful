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

    # Can't drop tables... So this doesn't do anything

    # if(os.getenv("FILL_DB") == "True"):
    #     print("Reloading DB...")
    #     database.db.drop_all()
    #     database.db.create_all()
    #     try:
    #         database.db.session.add(database.User(username="UserA", email="a@a.a", password=12345678))
    #         users = [
    #             database.User(username="UserA", email="a@a.a", password=12345678),
    #             database.User(username="UserB", email="b@b.b", password=12345678),
    #             database.User(username="UserE", email="e@e.e", password=12345678)
    #         ]
    #         database.db.session.add_all(users)
    #         database.db.session.commit()
    #         stati = [
    #             database.Status(
    #                 time="2022-09-20 10:27:21.240752",
    #                 text="Hi",
    #                 latitude=50,
    #                 longitude=50,
    #                 color= "#FF0000",
    #                 user=users[0].id),
    #             database.Status(
    #                 time="2022-10-20 10:27:21.240752",
    #                 text="Hello",
    #                 latitude=60,
    #                 longitude=60,
    #                 color= "#00FF00",
    #                 user=users[1].id),
    #             database.Status(
    #                 time="2022-11-20 10:27:21.240752",
    #                 text="Hello There",
    #                 latitude=50,
    #                 longitude=80,
    #                 color= "#0000FF",
    #                 user=users[2].id)
    #         ]
    #     except:
    #         print("Database Re-Population Failed")

    # else:

    database.db.create_all()  # this is only needed if the database doesn't already exist


if __name__ == "__main__":
    app.run()
