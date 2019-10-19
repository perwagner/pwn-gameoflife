import os

from . import website



@website.route('/')
def index():
    print(os.getenv('SQLALCHEMY_DATABASE_URI_TEST', 'test'))
    return "HELLO WORLD"
