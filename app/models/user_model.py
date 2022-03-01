from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class UserModel(db.Model):
  __tablename__ = "users"

  id = Column(Integer, primary_key = True)
  name: str = Column(String(127), nullable = False)
  last_name: str = Column(String(511), nullable = False)
  email: str = Column(String(255), nullable = False, unique = True)
  password_hash = Column(String(511), nullable = False)

  @property
  def password(self):
    raise AttributeError("Password is not accessible")

  @password.setter
  def password(self, password_to_hash):
    self.password_hash = generate_password_hash(password_to_hash)

  def check_password(self, password_to_compare):
    return check_password_hash(self.password_hash, password_to_compare)

  @staticmethod
  def modify_user_data(user, new_data):
    avaliable_values: dict = {"name": str, "last_name": str, "email": str, "password": str}

    for key, value in new_data.items():
      if key in avaliable_values:
        setattr(user, key, value)
