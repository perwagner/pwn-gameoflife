import os

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user

from . import website
from .forms import SignupForm, LoginForm
from app.models import User, db



@website.route('/')
def index():
    return render_template("index.html", title="HOME", user="PER")


@website.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f"login requested for user {form.username.data}, \
        remember me={form.remember_me.data}")

        return redirect(url_for('website.index'))
    return render_template('login.html', title='Sign In', form=form)


@website.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('website.login'))
    return render_template('signup.html', title='Signup', form=form)
