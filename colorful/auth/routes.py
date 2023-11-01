from flask import render_template

from . import auth_bp

@auth_bp.get('/register/')
def get_register():
    return render_template("register.html")

@auth_bp.get('/login/')
def get_login():
    return render_template("login.html")