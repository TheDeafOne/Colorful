from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from flask import Response, abort, jsonify, render_template, request
from flask_login import current_user, login_required

import colorful.db as database
import colorful.color_map as cm

from . import api_bp

load_dotenv()


@api_bp.post('/setStatus/')
@login_required
def set_status():
    status = request.json['status']
    if (status is None):
        return Response(status=400)

    user_id = int(current_user.get_id())

    dbStatus = database.Status(
        time=str(datetime.now()),
        text=status,
        latitude=request.json['latitude'],
        longitude=request.json['longitude'],
        color=determineColor(status),
        user=user_id)
    database.db.session.add(dbStatus)
    database.db.session.commit()

    user = database.User.query.get(user_id)
    user.currentStatusID = dbStatus.id
    database.db.session.add(user)
    database.db.session.commit()

    return Response(status=200)


def determineColor(status):
    color = cm.color_map[cm.get_text_emotion(status)]
    print(color)
    return color


@api_bp.get('/getStatusList/')
@login_required
def get_status_list():
    users = database.User.query.all()

    stati = []
    user: database.User
    for user in users:
        if user.isMuted:
            status = database.Status.query.get(user.currentStatusID)
            stati.append({
                'name': user.username,
                'status': "Muted",
                'color': "#000000",
                'longitude': status.longitude,
                'latitude': status.latitude,
                'time': status.time
            })
        elif user.currentStatusID:
            status = database.Status.query.get(user.currentStatusID)
            stati.append({
                'name': user.username,
                'status': status.text,
                'color': status.color,
                'longitude': status.longitude,
                'latitude': status.latitude,
                'time': status.time
            })

    return jsonify(stati)


@api_bp.get('/getFriendsStatusList/<int:user_id>/')
@login_required
def get_friends_status_list(user_id: int):
    friends_ids = [friend.user_id for friend in database.UserFollowers.query.filter_by(follower_id=user_id)]
    users = database.User.query.filter(database.User.id.in_(friends_ids)).all()

    stati = []
    user: database.User
    for user in users:
        if user.isMuted:
            status = database.Status.query.get(user.currentStatusID)
            stati.append({
                'name': user.username,
                'status': "Muted",
                'color': "#000000",
                'longitude': status.longitude,
                'latitude': status.latitude,
                'time': status.time
            })
        elif user.currentStatusID:
            status = database.Status.query.get(user.currentStatusID)
            stati.append({
                'name': user.username,
                'status': status.text,
                'color': status.color,
                'longitude': status.longitude,
                'latitude': status.latitude,
                'time': status.time
            })

    return jsonify(stati)

@api_bp.get('/loadmaps.js')
def get_maps_source():
    return Response(render_template('/script/loadmaps.js', api_key=getenv("MAPS_API_KEY")), mimetype="text/javascript")


@login_required
@api_bp.post('/addFollower/')
def add_follower():
    user_id = request.json.get("self")
    other_id = request.json.get("other")
    current_user_id = current_user.get_id()
    if (user_id != current_user_id or other_id == current_user_id):
        abort(403)

    userFollower = database.UserFollowers(
        user_id=int(other_id),
        follower_id=int(user_id)
    )
    database.db.session.add(userFollower)
    database.db.session.commit()
    return Response(status=200)


@login_required
@api_bp.post('/removeFollower/')
def removeFollower():
    user_id = request.json.get("self")
    other_id = request.json.get("other")
    current_user_id = current_user.get_id()
    if (user_id != current_user_id or other_id == current_user_id):
        abort(403)
    # remove this user as a follower to the other user
    database.UserFollowers.query.filter_by(user_id=other_id).delete()
    database.db.session.commit()
    return Response(status=200)


@login_required
@api_bp.get('/searchUser/')
def searchUser():
    query = request.args.get("query")
    similar_users: list[database.User] = database.User.query.filter(
        database.User.username.like('%' + query + '%')).all()
    similar_users: list = [
        {
            "username": user.username,
            "color": color.color if (color := database.Status.query.get(user.currentStatusID)) else '#000'

        }
        for user in similar_users
    ]
    return jsonify(similar_users)


# If this were actually in production, I would put the effort into removing user's sensitive data, ie. location
# But it's not so the admins can have access to it if they Reallly care
# TODO: integrate user search for better admin experience
@login_required
@api_bp.get('/getUsersList/')
def get_user_list():
    user = database.User.query.get(current_user.get_id())
    if (user.isAdmin):
        users = database.User.query.all()
        outputUsers = []
        for u in users:
            userJSON = u.to_json()
            curStatus = database.Status.query.get(u.currentStatusID)
            userJSON["status"] = curStatus.to_json()
            outputUsers.append(userJSON)

        return jsonify(outputUsers)
    else:
        abort(403)


@login_required
@api_bp.post('/toggleMuteForUser/')
def toggle_mute():
    user_id = request.json.get("user")
    user = database.User.query.get(user_id)
    admin = database.User.query.get(current_user.get_id())
    if (not admin.isAdmin or user.isAdmin):
        abort(403)
    user.isMuted = not user.isMuted

    database.db.session.add(user)
    database.db.session.commit()
    return Response(status=200)
