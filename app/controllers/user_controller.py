from datetime import timedelta
from flask import current_app, jsonify, request
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

@jwt_required()
def get_user():
  user: UserModel = get_jwt_identity()

  user = UserModel.query.filter_by(email = user["email"]).first()

  return jsonify(user), 200

def create_user():
  data: dict = request.json

  try:
    user: UserModel = UserModel(**data)

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
    user: UserModel = UserModel.query.filter_by(email = data.get("email")).first()

    if not user:
      raise ValueError("email and password mismatch")

    if not user.check_password(data.get("password")):
      raise ValueError("email and password mismatch")

    token = create_access_token(user, expires_delta = timedelta(hours=5))

    return jsonify({"access_token": token}), 200

  except ValueError as err:
    return jsonify({"msg": err.args[0]}), 400

@jwt_required()
def delete_user():
  user = get_jwt_identity()

  user = UserModel.query.filter_by(email = user["email"]).first()

  current_app.db.session.delete(user)
  current_app.db.session.commit()

  return jsonify({
    "msg": f"User {user.name} has been deleted."
  }), 200

@jwt_required()
def modify_user():
  data = request.json
  
  try:
    user: UserModel = get_jwt_identity()

    user = UserModel.query.filter_by(email = user["email"]).first()

    UserModel.modify_user_data(user, data)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user), 200

  except IntegrityError:
    email = data.get("email")

    return jsonify({
      "msg": f"{email} is already in use!"
    }), 409