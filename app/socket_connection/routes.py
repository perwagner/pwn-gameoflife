from flask_socketio import send, emit

from . import socketio
from app.models import GameOfLifeGame, db
from app.socket_connection.gameoflife.gamelogic import delete_game
from app.socket_connection.gameoflife.tasks import add_together


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
    print("CELL CLICKED")
    print(cell_x, cell_y)
    add_together.delay(1,4)

@socketio.on('updateTurn')
def handle_update_turn(json):
    print(f"Updating turn: {json['data']}")




@socketio.on('clickButton')
def handle_click_button(json):
    print(json)

    emit('updateClicks', 1)


@socketio.on('restartGame')
def handle_restart_game():
    game = GameOfLifeGame.query.first()

    if game is not None:
        delete_game(game)  

    print("A")
    add_together.delay(1,4)
    print("B")
