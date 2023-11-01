from flask import Flask, render_template
from colorful.api import api_bp
from colorful.auth import auth_bp
from colorful.main import main_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(api_bp, url_prefix='/api/')
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
