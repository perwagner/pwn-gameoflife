web: gunicorn --worker-class eventlet -w 2 wsgi:app
beat: celery worker -A celery_worker.celery --loglevel=info --beat
