from flask import render_template
from flask_login import current_user

from . import main_bp


@main_bp.get('/')
def index():
    return render_template("index.html", current_user=current_user)


@main_bp.get('/about/')
def get_about():
    return render_template("about.html")
