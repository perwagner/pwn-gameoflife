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