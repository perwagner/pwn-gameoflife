from flask_socketio import send, emit

from . import socketio
from app.models import GameOfLifeGame, db, User, GameOfLifeCell
from app.socket_connection.gameoflife.gamelogic import (
    create_new_game,
    delete_game,
)
from app.socket_connection.gameoflife.tasks import cell_clicked


@socketio.on('message')
def handle_message(message):
    print("XXXXXXXXXXXXXXXXXX")
    print('received message: ' + message)


@socketio.on('connectionEstablished')
def handle_connection_established(json):
    print(f"Message is now: {json['data']}")


@socketio.on('cellClick')
def handle_cell_click(json):
    cell_x = json['cellX']
    cell_y = json['cellY']
    cell = dict()
    cell['x'] = cell_x
    cell['y'] = cell_y

    print(cell)
    cell_clicked(cell)


@socketio.on('updateTurn')
def handle_update_turn(json):
    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        if "user" in json:
            user_id = json['user']
            user = User.query.filter_by(id=user_id).first()
            new_game = create_new_game(user, 10, 10)
            print(f"New game created: {new_game}")
    else:
        print("Fetch updated game info")
        game = GameOfLifeGame.query.first()
        print(f"game stored: {game}")
        cells = GameOfLifeCell.query.filter_by(game=game).all()
        game_cells = list()

        for cell in cells:
            alive = 1 if cell.is_alive else 0
            game_cells.append((cell.x, cell.y, alive))

        emit('gameUpdate', game_cells, broadcast=True)


@socketio.on('restartGame')
def handle_restart_game():
    game = GameOfLifeGame.query.first()

    if game is not None:
        delete_game(game)  
      