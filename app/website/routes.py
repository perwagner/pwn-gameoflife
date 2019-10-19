import os

from . import website



@website.route('/')
def index():
    print(os.getenv('SQLALCHEMY_DATABASE_URI', 'aaaa'))
    return "HELLO WORLD"
