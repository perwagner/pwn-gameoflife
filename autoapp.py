import logging
import os

import click
from flask_migrate import Migrate
from flask_socketio import SocketIO

from app import create_app
from app.models import db


logging.basicConfig(level=logging.INFO)
app = create_app((os.getenv("ENV") or "local").lower())

migrate = Migrate(app, db)
socketio = SocketIO(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
def test():
    """Run py.test on the full test suite"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    import pytest

    con = psycopg2.connect(
        dbname='postgres', 
        user=os.getenv('POSTGRES_USER', 'tester'), 
        host=os.getenv('POSTGRES_HOST', 'db'),
        password=os.getenv('POSTGRES_PASSWORD', '12345'),
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    try:
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + 'flaskdb_test')
        cur.close()
        con.close()
    except:
        logging.info("Test database already exists")

    pytest.main(['tests', '-v', '-l'])


@socketio.on('message')
def handle_message(message):
    print("XXXXXXXXXXXXXXXXXX")
    print('received message: ' + message)

@socketio.on('my event')
def handle_my_custom_event(json):
    print(type(json))
    print(f"Message is: {json['data']}")

if __name__ == '__main__':
    socketio.run(app, debug=True)