import logging

from flask_socketio import send, emit

from app.app_setup import celery
from app.models import db, GameOfLifeGame, GameOfLifeCell
from app.gameoflife.gamelogic import update_game_round


logger = logging.getLogger("TESTER")


@celery.task(name='game_beat_1_second')
def game_beat_1_second():
    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return
        
    update_game_round()


@celery.task(name='cell_clicked')
def cell_clicked(cell_update):
    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return

    game = GameOfLifeGame.query.first()
    cell = GameOfLifeCell.query.filter_by(
        game=game, 
        x=cell_update['x'], 
        y=cell_update['y']
    ).update(dict(is_alive=True))

    db.session.commit()
