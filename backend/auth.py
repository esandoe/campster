from database import User, db
from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/api/login", methods=["POST"])
def login_post():
    email = request.json.get("email")
    password = request.json.get("password")
    remember = bool(request.json.get("remember"))

    if email is None or email == "":
        return jsonify(Error="Email is required")

    if password is None or password == "":
        return jsonify(Error="Password is required")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify(Error="Please check your login details and try again.")

    login_user(user, remember=remember)
    return jsonify(Success="Logged in.")


@auth.route("/api/signup", methods=["POST"])
def signup():
    # code to validate and add user to database goes here
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")

    print(email, password, name)

    if email is None or email == "":
        return jsonify(Error="Email is required")

    if name is None or name == "":
        return jsonify(Error="Name is required")

    if password is None or password == "":
        return jsonify(Error="Password is required")

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(Error="User already exists")

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="scrypt"),
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(Success="User created")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(Success="Logged out")
