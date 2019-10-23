import logging

from app.app_setup import celery


logger = logging.getLogger("TESTER")


@celery.task()
def add_together(a, b):
    return a + b


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(2.0, test.s('hello'), name='add every 10')


@celery.task(name='test')
def test(arg):
    logger.critical("HELP ME HERE")
    return(arg)
