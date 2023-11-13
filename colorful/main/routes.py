from flask import redirect, render_template, url_for
from flask_login import current_user

from colorful.db import User

from . import main_bp


@main_bp.get('/')
def index():
    if (current_user.is_authenticated):
        return render_template("home.html", current_user=current_user)

    return render_template("index.html", current_user=current_user)


@main_bp.get('/about/')
def get_about():
    return render_template("about.html")


@main_bp.get('/profile/')
@main_bp.get('/profile/<string:id>/')
def get_self_profile(id=None):
    user_id = current_user.get_id() if not id else id
    user = User.query.get(user_id)
    if user:
        return render_template("profile.html", user=user, is_same_user=user_id == current_user.get_id())
    return render_template("noProfileFound.html")


@main_bp.get('/edit-profile/')
def get_edit_profile():
    user = User.query.get(current_user.get_id())
    return render_template("editProfile.html", user=user)
