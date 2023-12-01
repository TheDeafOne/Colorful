from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from flask import Response, abort, jsonify, render_template, request
from flask_login import current_user, login_required

import colorful.db as database

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

    possibleColors = ["#FF0000", "#00FF00", "#0000FF"]
    hashVal = hash(status)
    color = possibleColors[hashVal % len(possibleColors)]
    return color


@api_bp.get('/getStatusList/')
@login_required
def get_status_list():
    users = database.User.query.all()

    stati = []
    user: database.User
    for user in users:
        if user.currentStatusID:
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
    database.User.query.get(other_id).num_followers += 1
    database.User.query.get(current_user_id).num_following += 1
    database.db.session.commit()
    return Response(status=200)
