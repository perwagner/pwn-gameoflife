import os

import factory
from factory.alchemy import SQLAlchemyModelFactory
import pytest

from application import db
from application.models import User, GameOfLifeGame, GameOfLifeCell


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: u'User %d' % n)
    email = factory.Sequence(lambda n: "user{0}@example.com".format(n))
    password_hash = factory.PostGenerationMethodCall("set_password", "example")


class GameOfLifeGameFactory(BaseFactory):
    class Meta:
        model = GameOfLifeGame

    owner = factory.SubFactory(UserFactory)
