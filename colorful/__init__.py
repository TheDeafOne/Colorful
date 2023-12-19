import os
import random
import string
import urllib.request

import requests
from flask import Flask
from flask_login import LoginManager

import colorful.db as database
from colorful.api import api_bp
from colorful.auth import auth_bp
from colorful.main import main_bp

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


def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


def _add_test_users(num_users: int):
    users = []
    for i in range(num_users):
        print(f'\ruser {i}')
        random_username = f"RandUser_{random_char(8)}"
        random_email = random_username+"@gmail.com"
        user = database.User(username=random_username,
                             email=random_email, password=random_username)
        users.append(user)
    database.db.session.add_all(users)
    database.db.session.commit()

    return users


def _generate_coordinate():
    latitude = random.uniform(-60, 60)
    longitude = random.uniform(-120, 120)
    return latitude, longitude


def _add_test_stati(users: list[database.User]):
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    random_word_set = response.content.splitlines()
    stati = []
    # generate random number of statuses per user
    for user in users:
        for i in range(random.randint(1, 5)):
            random_datetime = f'{random.randint(2019,2023)}-{random.randint(1,12)}-{random.randint(1,28)} {random.randint(0,23)}:{random.randint(0,59)}:21.240752'
            random_text = ' '.join([str(random_word_set[random.randint(0, len(
                random_word_set)-1)]).replace("'b", '').replace("'", '')[1:] for _ in range(random.randint(3, 10))])
            random_lat, random_long = _generate_coordinate()
            random_color = '#' + \
                str(hex(random.randrange(0, 2**24)))[2:].upper()
            new_random_status = database.Status(
                time=random_datetime,
                text=random_text,
                latitude=random_lat,
                longitude=random_long,
                color=random_color,
                user=user.id
            )
            stati.append(new_random_status)
        # set last status added for given user as that users current status

    database.db.session.add_all(stati)
    database.db.session.commit()

    for user in users:
        user.currentStatusID = list(
            filter(lambda status: status.user == user.id, stati))[-1].id

    database.db.session.add_all(users)
    database.db.session.commit()


def _add_test_followers(users: list[database.User]):
    followers = []
    for user in users:
        # random number of followers
        for _ in range(random.randint(0, len(users)-1)):
            random_id = users[random.randint(0, len(users)-1)].id
            followers.append(database.UserFollowers(
                user_id=user.id, follower_id=random_id))

    database.db.session.add_all(followers)
    database.db.session.commit()


def _add_test_data():
    print('adding test users')
    users = _add_test_users(5)
    print('done adding test users')
    print('adding test statuses')
    _add_test_stati(users)
    print('done adding test statuses')
    print('adding test followers')
    _add_test_followers(users)
    print('done adding test followers')


def _setup_db(app: Flask):
    with app.app_context():
        database.db.init_app(app)

        # Reloads DB if the .env contains: RELOAD_DB="True"

        if (os.getenv("RELOAD_DB") == "True"):
            print("Reloading DB...\n")
            database.db.drop_all()
            database.db.create_all()
            # try:
            admin = database.User(
                username='Admin', email='admin@gmail.com', password='aminuser', isAdmin=True)
            database.db.session.add(admin)
            database.db.session.commit()
            database.db.session.add(database.UserFollowers(user_id=admin.id, follower_id=admin.id))
            _add_test_data()

            print("Database Loaded")
            # except Exception as e:
            #     print(e)
            #     print("Database Re-Population Failed")

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
