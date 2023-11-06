from flask import render_template
from flask_login import current_user

from . import main_bp


@main_bp.get('/')
def index():
    # if(current_user.is_authenticated):
    #     return render_template("home.html", current_user=current_user)

    return render_template("index.html", current_user=current_user)


@main_bp.get('/about/')
def get_about():
    return render_template("about.html")
