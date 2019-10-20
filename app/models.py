from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.app_setup import login_manager, db


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameOfLifeGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f"Game {self.id} by {self.owner.username}"


class GameOfLifeCell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game_of_life_game.id'), nullable=False)
    game = db.relationship('GameOfLifeGame', backref=db.backref('cells', lazy=True))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    is_alive = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Game {self.game_id}: ({self.x},{self.y})"