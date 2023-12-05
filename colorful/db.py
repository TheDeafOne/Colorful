from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from flask import current_app
from flask_login import LoginManager, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy

from colorful.auth.hasher import UpdatedHasher

load_dotenv()
db = SQLAlchemy()
pepper_key = os.getenv('PEPPER_KEY')
password_hasher = UpdatedHasher(pepper_key=pepper_key)


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    currentStatusID = db.Column(
        db.Integer, db.ForeignKey("Status.id", name="fk_name_user_status"), nullable=True)
    email = db.Column(db.Unicode, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    num_followers = db.Column(db.Integer, nullable=False, default=0)
    num_following = db.Column(db.Integer, nullable=False, default=0)
    # friends = db.Column
    # hash is a binary attribute
    password_hash = db.Column(db.LargeBinary)

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")

    @password.setter
    def password(self, pwd: str) -> None:
        self.password_hash = password_hasher.hash(pwd)

    # add a verify_password convenience method
    def verify_password(self, pwd: str) -> bool:
        return password_hasher.check(pwd, self.password_hash)

    def to_json(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'currentStatusId': self.currentStatusID,
            'email': self.email,
        }


class Status(db.Model):
    __tablename__ = 'Status'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Unicode, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    text = db.Column(db.Unicode, nullable=False)
    color = db.Column(db.Unicode, nullable=False)  # To implement with ML...
    user = db.Column(db.Integer, db.ForeignKey(
        "User.id", name="fk_name_status_user"), nullable=False)
    UserIsCurrentStatus = db.relationship(
        'User', foreign_keys='User.currentStatusID', backref='currentStatus')

    def to_json(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'time': self.time,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'text': self.text,
            'color': self.color,
            'user': self.user,
        }


class UserFollowers(db.Model):
    __tablename__ = 'User_Followers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    follower_id = db.Column(db.Integer, nullable=False)
