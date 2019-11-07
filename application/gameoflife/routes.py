import logging
import random

from flask import current_app
from flask_socketio import send, emit

from application import socketio
from application.models import GameOfLifeGame, db, User, GameOfLifeCell
from application.gameoflife.gamelogic import (
    broadcast_game_state,
    create_new_game,
    delete_game,
)
from application.gameoflife.tasks import cell_clicked


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@socketio.on('connectionEstablished')
def handle_connection_established():
    color_rgb = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    color_hex = '#%02x%02x%02x' % (color_rgb[0], color_rgb[1], color_rgb[2])
    emit('getColor', color_hex)
    broadcast_game_state()



@socketio.on('cellClick')
def handle_cell_click(json):
    cell = dict()

    color = json['color']
    cell_x = json['cellX']
    cell_y = json['cellY']
    cell['x'] = cell_x
    cell['y'] = cell_y
    cell['color'] = color

    cell_clicked(cell)


@socketio.on('restartGame')
def handle_restart_game(json):
    game = GameOfLifeGame.query.first()

    if "user_id" not in json:
        logger.error("No user_id in json payload in handle_restart_game")
        return

    user_id = json['user_id']
    user = User.query.filter_by(id=user_id).first()
    game_width = current_app.config['GAME_OF_LIFE_WIDTH']
    game_height = current_app.config['GAME_OF_LIFE_HEIGHT']

    if game is not None:
        delete_game(game)

    create_new_game(user, game_width, game_height)
    
      