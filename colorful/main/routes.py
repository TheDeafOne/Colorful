from flask import render_template
from . import main_bp

@main_bp.get('/')
def index():
    return render_template("index.html")

@main_bp.get('/about/')
def get_about():
    return render_template("about.html")