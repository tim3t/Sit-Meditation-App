"""SQLAlchemy models for Sit Meditation App"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)

    sit = db.relationship('Sit', backref='users')


    def __repr__(self):
        return f"User #{self.id}: {self.username}, {self.email}, {self.first_name} {self.last_name}"

    @classmethod
    def signup(cls, username, password, first_name, last_name, email):
        """Sign up user and hash password"""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, password=hashed_pwd, first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with username and password.
        If matched, return user object.
        If no match, return False"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

class Sit(db.Model):

    __tablename__ = 'sit_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    sit_title = db.Column(db.Text, nullable=False)
    sit_body = db.Column(db.Text, nullable=False)
    sit_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Sit #{self.id}, User #{self.user_id}: {self.sit_title}, {self.timestamp}"



def connect_db(app):
    db.app = app
    db.init_app(app)