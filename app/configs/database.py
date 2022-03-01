from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_app(app: Flask):
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
  app.config["JSON_SORT_KEYS"] = False

  db.init_app(app)
  app.db = db

  # Tables

  from app.models.user_model import UserModel