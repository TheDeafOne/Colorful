from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='templates')

from . import app_routes
from . import pub_routes