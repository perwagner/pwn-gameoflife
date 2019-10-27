from flask import Blueprint
from flask_socketio import SocketIO

gameoflife_blueprint = Blueprint('gameoflife', __name__)
socketio = SocketIO()

from . import routes


