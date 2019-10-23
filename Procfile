web: gunicorn --worker-class eventlet -w 1 autoapp:app
worker: celery worker -A app.celery --loglevel=info
