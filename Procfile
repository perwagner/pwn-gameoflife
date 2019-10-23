web: gunicorn --worker-class eventlet -w 1 autoapp:app
# worker: celery worker -A app.celery --loglevel=info
# beat: celery worker -A app.celery --loglevel=info -B

beat: celery worker -A celery_worker.celery --beat --loglevel=info