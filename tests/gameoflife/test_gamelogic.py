from application.gameoflife.gamelogic import (
    create_new_game,
    delete_game,
    update_game_round,
)
from application.models import GameOfLifeCell, GameOfLifeGame, User
from tests.factories import UserFactory


def test_status_return_value(db):
    user = UserFactory()
    game = create_new_game(user, 10, 10)

    assert isinstance(user, User)