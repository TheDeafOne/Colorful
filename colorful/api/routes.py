from datetime import datetime

from flask import Response, jsonify, render_template, request
from flask_login import current_user, login_required

import colorful.db as database

from . import api_bp


@api_bp.post('/setStatus/')
@login_required
def set_status():
    status = request.json['status']
    print(request.json)
    if (status is None):
        return Response(status=400)

    user_id = int(current_user.get_id())

    dbStatus = database.Status(
        time=str(datetime.now()), text=status, color="White", user=user_id)
    database.db.session.add(dbStatus)
    database.db.session.commit()

    user = database.User.query.get(user_id)
    user.currentStatusID = dbStatus.id
    database.db.session.add(user)
    database.db.session.commit()

    return Response(status=200)


@api_bp.get('/getStatusList/')
@login_required
def get_status_list():
    user_id = int(current_user.get_id())

    users = database.User.query.all()

    stati = {}

    for u in users:
        stati[u.username] = u.currentStatus.text

    return jsonify(stati)
