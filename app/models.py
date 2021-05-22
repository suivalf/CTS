from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    coins = db.relationship('Coin', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def interested_in_coin(self, coin):
        if not self.is_owning(coin):
            self.coins.append(coin)

    def uninterested_in_coin(self, coin):
        if self.is_owning(coin):
            self.coins.remove(coin)

    def followed_coins(self):
        return Coin.query.filter(Coin.user_id==self.id).all()

class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Coin {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
