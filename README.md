# pwn-gameoflife
Inspired by this competition: https://hackmd.io/@terminal1/assessment-conway


# Heroku Setup
You must set the following config variables:
* SQLALCHEMY_DATABASE_URI
* DEBUG
* ENV = prod
* CELERY_BROKER_URL
* CELERY_RESULT_BACKEND
* CLOUDAMQP_APIKEY
* CLOUDAMQP_URL
* DATABASE_URL
* SQLALCHEMY_DATABASE_URI

on Heroku, you will need a:
* Heroku Postgres (or alternative Postgres db)
* CloudAMQP

From the heroku cli run the following to apply migrations after deployment:
```
heroku run -a <appname> flask db upgrade
```

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