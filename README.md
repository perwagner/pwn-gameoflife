# pwn-gameoflife
Inspired by this competition: https://hackmd.io/@terminal1/assessment-conway


Game of life multiplayer game. You have to signup with to play. Multiple players can play in the same 'world', and each player will get their own color. The Game Of Life continues even if all players are logged off for a period of time, eg. the game runs in a worker process.


# Local setup
Create a virtualenv
```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```


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


# Bugs
**Worker error on first run**  
On just starting up on a clean DB, the worker throws an error and the game of life cannot start until the user clicks the 'restart game' at least once. Afterwards, it works just fine.

# Improvements
**Maintain color for each user**  
If a logged in user refreshes his browser he is assigned a new color. He should maintain his color between refreshes, but still reset the color on a "restart game".

