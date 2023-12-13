from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user

from colorful.db import User, UserFollowers, db, Status
from colorful.forms import ProfileForm

from . import main_bp


@main_bp.get('/app/')
def app_home():
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    return render_template("app/home.html", user=user)


@main_bp.get('/app/map/')
def map_view():
    return render_template("app/map.html", user=current_user)


@main_bp.get('/profile/')
@main_bp.get('/profile/<string:id>/')
def get_self_profile(id=None):
    user_id = current_user.get_id() if not id else id
    other_user: User
    # get user by id or name
    if str(user_id).isnumeric():
        other_user = User.query.get(user_id)
    else:
        other_user = User.query.filter_by(username=user_id).first()

    if other_user:
        other_user_following: list[UserFollowers] = UserFollowers.query.filter_by(
            follower_id=other_user.id).all()
        other_user_followers: list[UserFollowers] = UserFollowers.query.filter_by(
            user_id=other_user.id).all()
        num_statuses = len(Status.query.filter_by(user=user_id).all())
        return render_template(
            "app/profile.html",
            other_user=other_user,
            user=User.query.get(current_user.get_id()),
            other_user_followers=other_user_followers,
            other_user_following=other_user_following,
            num_statuses=num_statuses
        )

    return render_template("app/noProfileFound.html")


@main_bp.get('/edit-profile/')
def get_edit_profile():
    user = User.query.get(current_user.get_id())
    form = ProfileForm()
    return render_template("app/editProfile.html", user=user, form=form)


@main_bp.post('/edit-profile/')
def post_edit_profile():
    form = ProfileForm()
    if form.validate():
        error_list = {}
        user: User = User.query.get(current_user.get_id())
        if form.old_password.data or form.confirm_new_password.data:
            # verify old password
            if user.verify_password(form.old_password.data):
                # verify confirm pass
                if form.confirm_new_password.data or form.new_password.data:
                    if form.new_password.data != form.confirm_new_password.data:
                        error_list[form.confirm_new_password] = "Confirmation password does not match"
                    else:
                        user.password = form.new_password.data
            else:
                error_list[form.old_password] = "Old password is incorrect"

        # verify username
        if form.username.data:
            if User.query.filter_by(username=form.username.data).first():
                error_list[form.username] = "Username is taken"
            else:
                user.username = form.username.data

        # verify email
        if form.email.data:
            if User.query.filter_by(email=form.email.data).first():
                error_list[form.email] = "Email is taken"
            else:
                user.email = form.email.data

        print(error_list)
        if error_list:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('main.get_edit_profile'))
        db.session.commit()
        return redirect(url_for('main.get_self_profile'))
    else:
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('main.get_edit_profile'))

@main_bp.get('/admin/')
def admin_portal():
    user = User.query.get(current_user.get_id())
    if(user.isAdmin):
        return render_template("app/adminPortal.html", user=user)
    else:
        abort(403)
        
        
@main_bp.get("/app/grid/")
def get_friends_grid():
    user = User.query.get(current_user.get_id())
    return render_template("app/grid.html", user=user)
    
    