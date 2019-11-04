from app.gameoflife.gamelogic import (
    create_new_game,
    delete_game,
    update_game_round,
)
from app.models import User, db, GameOfLifeCell, GameOfLifeGame
from tests.factories import UserFactory


def test_status_return_value(session):
    # user = User(username="Per", email="per@per.dk")
    # user.set_password("PASSME")
    # session.add(user)
    # session.commit()
    user = UserFactory()
    print(user)

    game = create_new_game(user, 10, 10)

    print(game)
    assert False