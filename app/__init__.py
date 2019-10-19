import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO

from app.api_v1 import api_v1 as api_v1_blueprint
from app.website import website as website_blueprint
from app.socket_connection import socketio_blueprint, socketio
from app.models import db

from config import config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_app(env="local", additional_settings={}):
    logger.info('Environment in __init__: "%s"', env)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[env])

    config[env].init_app(app)
    app.config.update(additional_settings)

    db.init_app(app)
    socketio.init_app(app)

    # Blueprints
    app.register_blueprint(website_blueprint, url_prefix='/')
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
    app.register_blueprint(socketio_blueprint)

    return app


app = create_app((os.getenv("ENV") or "local").lower())
migrate = Migrate(app, db)

