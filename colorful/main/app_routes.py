from flask import render_template
from flask_login import current_user
from . import main_bp

@main_bp.get('/app/')
def app_home():
    return render_template("app/home.html", current_user=current_user)