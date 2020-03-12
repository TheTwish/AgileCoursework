import jwt
from time import time
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# timestamp to be inherited by other class models
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

# User class
class User(db.Model, TimestampMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    validated = db.Column(db.Boolean,default=True)
    admin = db.Column(db.Integer, default=0)
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    event = db.relationship('Event', backref='user', lazy='dynamic')

    # print to console username created
    def __repr__(self):
        return f'<User {self.username}>'
    # generate user password i.e. hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_validated(self, value):
        self.validated = value;
    # check user password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # for reseting a user password
    def get_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    # verify token generated for resetting password
    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_token_user(self, expires_in=600):
        return jwt.encode(
            {'confirm_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    # verify token generated for resetting password
    @staticmethod
    def verify_token_user(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Event class
class Event(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    host = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    #date = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.Text)
    image = db.Column(db.String(30))
    price = db.Column(db.Float, default=1.99)
    reviews = db.relationship('Review', backref='event', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Event {self.name}>'

# belongs to user and event
class Review(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))