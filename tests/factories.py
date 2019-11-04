import os

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import User
from app.models import db as _db


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = _db.session


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: u'User %d' % n)
    email = factory.Sequence(lambda n: "user{0}@example.com".format(n))
    password_hash = factory.PostGenerationMethodCall("set_password", "example")