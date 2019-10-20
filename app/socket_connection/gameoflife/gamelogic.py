from app.models import GameOfLifeGame, GameOfLifeCell, db


def create_new_game(owner, width, height):
    game = GameOfLifeGame(owner=owner)
    db.session.add(game)
    
    for y in range(height):
        for x in range(width):
            cell = GameOfLifeCell(
                game=game,
                x=x + 1,
                y=y + 1,
            )
            db.session.add(cell)
    
    db.session.commit()

    return game


def delete_game(game):
    try:
        cells_to_delete = GameOfLifeCell.query.filter_by(game=game).all()
        db.session.delete(cells_to_delete)
        db.session.delete(game)
        db.session.commit()
    except Exception as E:
        print(E)
        db.session.rollback()

