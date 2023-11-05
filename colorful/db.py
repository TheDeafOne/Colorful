from __future__ import annotations
from flask import current_app
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from dotenv import load_dotenv
from colorful.auth.hasher import UpdatedHasher

load_dotenv()
db = SQLAlchemy()
pepper_key = os.getenv('PEPPER_KEY')
password_hasher = UpdatedHasher(pepper_key=pepper_key)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary) # hash is a binary attribute

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
    
