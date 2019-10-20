web: gunicorn --worker-class eventlet -w 1 autoapp:app
celery: celery worker -A app.celery --loglevel=info