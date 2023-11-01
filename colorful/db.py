from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)

class Account(db.Model):
    __tablename__ = "Accounts"

class Status(db.Model):
    __tablename__ = "Status"