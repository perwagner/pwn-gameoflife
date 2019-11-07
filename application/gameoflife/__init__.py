from flask import Blueprint


gameoflife_blueprint = Blueprint('gameoflife', __name__)

from . import routes


