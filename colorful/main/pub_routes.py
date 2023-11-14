from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from colorful.db import User
from colorful.forms import ProfileForm

from . import main_bp


@main_bp.get('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.app_home'))
    return render_template("pub/splash.html")


@main_bp.get('/about/')
def get_about():
    return render_template("pub/about.html")


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
    form = ProfileForm()
    return render_template("editProfile.html", user=user, form=form)


@main_bp.post('/edit-profile/')
def post_edit_profile():
    form = ProfileForm()
    if form.validate():
        user: User = User.query.get(current_user.get_id())
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data

            return redirect(url_for("main.get_profile"))
        else:
            print('old incorrect')
            flash('Old Password Incorrect')
            return redirect(url_for("main.get_edit_profile"))
    else:
        print('flashing')
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('main.get_edit_profile'))
