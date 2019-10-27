import random

from flask import current_app
from flask_socketio import send, emit

from . import socketio
from app.models import GameOfLifeGame, db, User, GameOfLifeCell
from app.gameoflife.gamelogic import (
    create_new_game,
    delete_game,
)
from app.gameoflife.tasks import cell_clicked


@socketio.on('connectionEstablished')
def handle_connection_established():
    color_rgb = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    color_hex = '#%02x%02x%02x' % (color_rgb[0], color_rgb[1], color_rgb[2])
    emit('getColor', color_hex)


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


@socketio.on('updateTurn')
def handle_update_turn(json):
    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        if "user" in json:
            game_width = current_app.config['GAME_OF_LIFE_WIDTH']
            game_height = current_app.config['GAME_OF_LIFE_HEIGHT']

            user_id = json['user']
            user = User.query.filter_by(id=user_id).first()
            new_game = create_new_game(user, game_width, game_height)
    else:
        game = GameOfLifeGame.query.first()
        cells = GameOfLifeCell.query.filter_by(game=game).all()
        game_cells = list()

        for cell in cells:
            alive = 1 if cell.is_alive else 0
            game_cells.append((cell.x, cell.y, alive, cell.color))

        emit('gameUpdate', game_cells, broadcast=True)


@socketio.on('restartGame')
def handle_restart_game():
    game = GameOfLifeGame.query.first()

    if game is not None:
        delete_game(game)  
      