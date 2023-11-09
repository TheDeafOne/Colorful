from . import auth_bp
from flask import flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

# from colorful.db import User, db
import colorful.db as database

from colorful.forms import LoginForm, RegisterForm



@auth_bp.get('/register/')
def get_register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@auth_bp.post('/register/')
def post_register():
    form = RegisterForm()
    if form.validate():
        # check if there is already a user with this email address
        user = database.User.query.filter_by(email=form.email.data).first()
        # if the email address is free, create a new user and send to login
        if user is None:
            user = database.User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)  # type:ignore
            database.db.session.add(user)
            database.db.session.commit()
            return redirect(url_for('auth.get_login'))
        else:  # if the user already exists
            # flash a warning message and redirect to get registration form
            flash('There is already an account with that email address')
            return redirect(url_for('auth.get_register'))
    else:  # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('auth.get_register'))


@auth_bp.get('/login/')
def get_login():
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_bp.post('/login/')
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this email address
        user = database.User.query.filter_by(email=form.email.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        else:  # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid email address or password')
            return redirect(url_for('auth.get_login'))
    else:  # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('auth.get_login'))


@auth_bp.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))
