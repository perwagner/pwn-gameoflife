from app.app_setup import celery


@celery.task()
def add_together(a, b):
    return a + b
