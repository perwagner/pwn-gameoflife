# pwn-gameoflife
Inspired by this competition: https://hackmd.io/@terminal1/assessment-conway


# Local setup
Run this to initialize the database on docker:
```
docker-compose up -d
flask db upgrade
```


## Local celery worker
Run this from local to start a worker locally.
```
celery worker -A celery_worker.celery --loglevel=info --beat
```
And start the flask application:
```
flask run
```

# Testing
Run
```
pytest
```
Coverage report will be available in `/coverage_html_report/index.html`
