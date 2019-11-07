import os
from datetime import timedelta


celery_beat_schedule = {
        'run-every-1-second': {
            'task': 'game_turn',
            'schedule': timedelta(seconds=3)
        },
        # 'run-every-2-second': {
        #     'task': 'game_turn',
        #     'schedule': timedelta(seconds=2)
        # },
    }



class Config:
    ENV = os.environ.get('ENV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
    CELERY_RESULT_BACKEND = os.getenv('SQLALCHEMY_DATABASE_URI', '')
    CELERYBEAT_SCHEDULE = celery_beat_schedule

    GAME_OF_LIFE_WIDTH = 32
    GAME_OF_LIFE_HEIGHT = 24
    GAME_OF_LIFE_DEAD_CELL_COLOR = "#444444"

    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI_TEST', 
        'postgresql+psycopg2://tester:12345@localhost:5432/flaskdb'
        )

    CELERY_BROKER_URL = "amqp://user:user@localhost:5672"
    CELERY_RESULT_BACKEND = "amqp://user:user@localhost:5672"  # "postgresql+psycopg2://tester:12345@localhost:5432/flaskdb"  # "amqp://user:user@localhost:5672"

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')


config = {
    'local': LocalConfig,
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
