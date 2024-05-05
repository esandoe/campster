from sre_constants import SUCCESS
from uu import Error
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from database import User, db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "Login"


@auth.route("/api/signup", methods=["POST"])
def signup():
    # code to validate and add user to database goes here
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify(Error="Email is required")

    if name is None or name == "":
        return jsonify(Error="Name is required")

    if password is None or password == "":
        return jsonify(Error="Password is required")

    user = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if user:
        return jsonify(Error="User already exists")

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="scrypt"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify(Success="User created")


@auth.route("/logout")
def logout():
    return "Logout"


@auth.route("/profile")
def profile():
    return "Profile"
