from database import User, db
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/api/login", methods=["POST"])
def login_post():
    username = request.json.get("username")
    password = request.json.get("password")
    remember = bool(request.json.get("remember"))

    if username is None or username == "":
        return jsonify(Error="username is required")

    if password is None or password == "":
        return jsonify(Error="Password is required")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify(Error="Please check your login details and try again.")

    login_user(user, remember=remember)
    return jsonify(Success="Logged in.")


@auth.route("/api/signup", methods=["POST"])
def signup():
    # code to validate and add user to database goes here
    password = request.json.get("password")
    username = request.json.get("username")

    print(password, username)

    if username is None or username == "":
        return jsonify(Error="Username is required")

    if password is None or password == "":
        return jsonify(Error="Password is required")

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(Error="User already exists")

    new_user = User(
        username=username,
        password=generate_password_hash(password, method="scrypt"),
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(Success="User created")


@auth.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify(Success="Logged out")


@auth.route("/api/profile", methods=["GET"])
@login_required
def get_profile():
    return jsonify(
        {
            "id": current_user.id,
            "username": current_user.username,
            "is_admin": current_user.is_admin,
            "avatar": current_user.avatar,
        }
    )
