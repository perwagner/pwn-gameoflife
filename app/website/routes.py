import os

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from . import website
from .forms import SignupForm, LoginForm
from app.models import User, db, GameOfLifeGame
from app.gameoflife.gamelogic import create_new_game


@website.route('/')
def index():
    env = (os.getenv("ENV") or "local").lower()


    return render_template("index.html", title="HOME", env=env)


@website.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None:
            flash('User does not exist, please create one')
            return redirect(url_for('website.signup'))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('website.login'))

        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')

        return redirect(url_for('website.index'))
    return render_template('login.html', title='Sign In', form=form)


@website.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('website.index'))
    
    form = SignupForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('website.login'))
    return render_template('signup.html', title='Signup', form=form)


@website.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for('website.index'))


@website.route('/gameoflife')
@login_required
def gameoflife():
    game = GameOfLifeGame.query.first()
    if game is None:
        game = create_new_game(current_user, 10, 10)

    print(game)

    return render_template("gameoflife.html")


