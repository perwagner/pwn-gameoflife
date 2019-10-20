import os

from flask_celery import Celery
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

login_manager = LoginManager()
db = SQLAlchemy()
celery = Celery()

