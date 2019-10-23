import logging

from app.app_setup import celery


logger = logging.getLogger("TESTER")


@celery.task()
def add_together(a, b):
    return a + b


@celery.task(name='test')
def test():
    logger.critical("HELP ME HERE")
    return("SOMETHING")
