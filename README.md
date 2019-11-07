# pwn-gameoflife
Inspired by this competition: https://hackmd.io/@terminal1/assessment-conway


# Heroku Setup
You must set the following config variables:
* SQLALCHEMY_DATABASE_URI
* DEBUG
* ENV = prod
* FLASK_APP = autoapp.py

From the heroku cli run the following to apply migrations:
```
heroku run -a <appname> flask db upgrade
```


# Local setup
Run this to initialize the database on docker:
```
docker-compose up -d
flask db upgrade
heroku local
```


## Local celery worker
Run this from local to start a worker locally in case you don't run `heroku local`
```
celery worker -A celery_worker.celery --loglevel=info
```

And for BEAT
```
celery worker -A celery_worker.celery --loglevel=info --beat
```

And start the flask application:
```
flask run
```