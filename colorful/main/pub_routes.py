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

