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

    def __repr__(self):
        return f"User #{self.id}: {self.username}, {self.email}, {self.first_name} {self.last_name}"

class Sit(db.Model):

    __tablename__ = 'sit_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', nullable=False))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    sit_title = db.Column(db.Text, nullable=False)
    sit_body = db.Column(db.Text, nullable=False)
    sit_rating = db.Column(db.Integer, nullable=False)
