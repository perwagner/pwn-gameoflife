from application.gameoflife.gamelogic import (
    create_new_game,
    delete_game,
    update_game_round,
)
from application.models import GameOfLifeCell, GameOfLifeGame
from tests.factories import UserFactory


def test_status_return_value(session):
    user = UserFactory()
    print(user)

    game = create_new_game(user, 10, 10)

    print(game)
    assert False