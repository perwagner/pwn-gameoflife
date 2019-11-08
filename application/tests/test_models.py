import pytest

from application.models import (
    GameOfLifeCell, 
    GameOfLifeGame,
    load_user,
    User,
)

from application.tests.factories import (
    UserFactory,
    GameOfLifeGameFactory,
)


class TestUserModel:
    def test__user_can_instantiate(self, db):
        user = User(username="Test", email="email@email.com")
        db.session.add(user)
        db.session.commit()

        getuser = User.query.filter_by(username=user.username).first()

        assert getuser is user

    def test__check_password__password_check_checks_out(self, db):
        user = User(username="Test", email="email@email.com")
        user.set_password("abcdef")
        assert user.check_password("abcdef") is True



    def test__load_user__loads_user(self, db):
        user = UserFactory()

        loaded_user = load_user(user.id)
        assert loaded_user is user


class TestGameOfLifeGameModel:
    def test__gameoflifegame_model_can_instantiate(self, db):
        user = UserFactory()
        golg = GameOfLifeGame(owner=user)
        db.session.add(golg)
        db.session.commit()

        get_golg = GameOfLifeGame.query.filter_by(owner=user).first()

        assert get_golg is golg


class TestGameOfLifeCellModel:
    def test__gameoflifecell_model_can_instantiate(self, db):
        game = GameOfLifeGameFactory()

        cell = GameOfLifeCell(
            game=game,
            x=1,
            y=1,
            is_alive=True,
            color="#AAABBC",
        )
        db.session.add(cell)
        db.session.commit()

        get_cell = GameOfLifeCell.query.filter_by(game=game).first()

        assert get_cell is cell