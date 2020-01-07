import logging
import os

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

from config import config


ENV = os.getenv("ENV", "local")
login_manager = LoginManager()
db = SQLAlchemy()
celery = Celery(__name__, broker=config[ENV].CELERY_BROKER_URL)
socketio = SocketIO()
migrate = Migrate()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_app(env="local", additional_settings={}, **kwargs):
    logger.info(f"Environment in __init__: {env}")
    logger.info(f"env from env variable: {ENV}")

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[env])
    app.config.update(additional_settings)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, message_queue=config[env].CELERY_BROKER_URL, logger=logger)
    celery.conf.update(app.config)
    migrate.init_app(app, db)

    with app.app_context():
        from application.api_v1 import api_v1 as api_v1_blueprint
        from application.website import website as website_blueprint
        from application.gameoflife import gameoflife_blueprint

        app.register_blueprint(website_blueprint, url_prefix='/')
        app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
        app.register_blueprint(gameoflife_blueprint)

        return app
