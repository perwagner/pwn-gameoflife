from flask import Blueprint

socketio_blueprint = Blueprint('socketio', __name__)


from . import routes


