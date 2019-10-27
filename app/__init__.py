import logging
import os

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from werkzeug.utils import import_string

from app.api_v1 import api_v1 as api_v1_blueprint
from app.website import website as website_blueprint
from app.gameoflife import gameoflife_blueprint, socketio
from app.app_setup import login_manager, celery
from app.models import db
from config import config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_app(env="local", additional_settings={}, **kwargs):
    logger.info(f"Environment in __init__: {env}")

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[env])
    app.config.update(additional_settings)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    celery.init_app(app)

    # Blueprints
    app.register_blueprint(website_blueprint, url_prefix='/')
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
    app.register_blueprint(gameoflife_blueprint)

    return app

env = (os.getenv("ENV") or "local").lower()
app = create_app(env)
migrate = Migrate(app, db)
