from flask import Blueprint
from flask_socketio import SocketIO

socketio_blueprint = Blueprint('socketio', __name__)
socketio = SocketIO()

from . import routes


