from flask_socketio import send, emit
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError

from application import celery
from application.models import db, GameOfLifeGame, GameOfLifeCell
from application.gameoflife.gamelogic import update_game_round


@celery.task(name='game_turn', ignore_result=True)
def game_turn():
    logger.info("## GAME TURN ##")

    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return
        
    try:        
        update_game_round()
    except (ObjectDeletedError, StaleDataError):
        # Might happen if game is reset and someone clicks on the grid
        print("Game has been deleted")


@celery.task(name='cell_clicked')
def cell_clicked(cell_update):
    logger.info("*** cell clicked ***")

    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return

    game = GameOfLifeGame.query.first()
    cell = GameOfLifeCell.query.filter_by(
        game=game, 
        x=cell_update['x'], 
        y=cell_update['y']
    ).update(dict(is_alive=True, color=cell_update['color']))

    db.session.commit()
