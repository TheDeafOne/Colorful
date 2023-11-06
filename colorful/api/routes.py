from flask import render_template, Response, request
from flask_login import current_user, login_required

from colorful.db import Status, db
from datetime import datetime

from . import api_bp

@api_bp.post('/setStatus/')
@login_required
def set_status():
    print("here")
    status = request.json['status']

    print(status)

    if(status is None):
        return Response(status=400)

    user_id = int(current_user.get_id())
    print(user_id)

    # dbStatus = Status(time=str(datetime.now()), text = status, color = "White", user = user_id)

    # db.session.add(dbStatus)
    # db.session.commit()

    return Response(status=200)
