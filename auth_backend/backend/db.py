# db.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .config import DATABASE_URI

db = SQLAlchemy()

def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
