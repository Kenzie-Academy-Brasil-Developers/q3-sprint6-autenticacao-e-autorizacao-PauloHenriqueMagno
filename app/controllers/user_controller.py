from flask import current_app, jsonify, request
from app.models.user_model import UserModel
import secrets
from app.configs.auth import auth
from sqlalchemy.exc import IntegrityError

@auth.login_required
def get_user():
  user = auth.current_user()

  return jsonify(user), 200

def create_user():
  data: dict = request.json
  try:

    user = UserModel(**data)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user), 201

  except IntegrityError:
    email = data.get("email")

    return jsonify({
      "msg": f"{email} is already in use!"
    }), 409

def login_user():
  data: dict = request.json
  try:
    user: UserModel = UserModel.query.filter_by(email = data["email"]).first()

    if not user:
      raise ValueError("email and password mismatch")

    if not user.check_password(data["password"]):
      raise ValueError("email and password mismatch")

    token = secrets.token_hex(20)

    user.api_key = token

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify({"token": token}), 200

  except ValueError as err:
    return jsonify({"msg": err.args[0]}), 400

@auth.login_required
def delete_user():
  user = auth.current_user()

  current_app.db.session.delete(user)
  current_app.db.session.commit()

  return jsonify({
    "msg": f"User {user.name} has been deleted."
  }), 204

@auth.login_required
def modify_user():
  try:
    data = request.json

    user: UserModel = auth.current_user()

    user.modify_user_data(user, data)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user), 200

  except IntegrityError:
    email = data.get("email")

    return jsonify({
      "msg": f"{email} is already in use!"
    }), 409