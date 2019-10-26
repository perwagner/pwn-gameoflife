import logging

from flask_socketio import send, emit

from app.app_setup import celery
from app.models import db, GameOfLifeGame, GameOfLifeCell


logger = logging.getLogger("TESTER")


@celery.task(name='game_beat_1_second')
def game_beat_1_second():
    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return
    logger.info("Update the game")


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
