import logging
import os

import click

from app.models import db
from app import app
from app import socketio

logging.basicConfig(level=logging.INFO)


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


if __name__ == '__main__':
    socketio.run(app, debug=True)