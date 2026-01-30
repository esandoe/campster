from functools import wraps

from database import ParticipantItem, TripParticipant, User, db
from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify(Error="Unauthorized"), 403
        return func(*args, **kwargs)

    return wrapper


def participant_self_required(f):
    """Decorator to make sure the current user is the same as the participant referenced, or an admin."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "participant_id" not in kwargs:
            raise ValueError(
                "user_id is required when decorated by `participant_self_required`"
            )

        participant_id = kwargs.get("participant_id")
        participant = TripParticipant.query.filter(
            TripParticipant.id == participant_id,
            TripParticipant.user_id == current_user.id,
        ).first()
        if current_user.is_admin or participant:
            return f(*args, **kwargs)

        abort(403)

    return decorated_function


def participant_of_trip_required(f):
    """Decorator to make sure the current user is a participant of the trip (or is an admin)."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "trip_id" not in kwargs:
            raise ValueError(
                "trip_id is required when decorated by `participant_required`"
            )

        trip_id = kwargs.get("trip_id")
        participant = TripParticipant.query.filter(
            TripParticipant.trip_id == trip_id,
            TripParticipant.user_id == current_user.id,
        ).first()
        if current_user.is_admin or participant:
            return f(*args, **kwargs)

        abort(403)

    return decorated_function


def item_owner_required(f):
    """Decorator to make sure the item belongs to the participant."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "participant_id" not in kwargs or "item_id" not in kwargs:
            raise ValueError(
                "participant_id and item_id are required when decorated by `item_owner_required`"
            )

        participant_id = kwargs.get("participant_id")
        item_id = kwargs.get("item_id")
        participant = TripParticipant.query.filter(
            TripParticipant.id == participant_id,
            TripParticipant.user_id == current_user.id,
        ).first()

        item = ParticipantItem.query.filter(
            ParticipantItem.participant_id == participant_id,
            ParticipantItem.id == item_id,
        ).first()

        if current_user.is_admin or (participant and item):
            return f(*args, **kwargs)

        abort(403)

    return decorated_function


@auth.route("/api/login", methods=["POST"])
def login_post():
    username = request.json.get("username")
    password = request.json.get("password")
    remember = bool(request.json.get("remember"))

    if username is None or username == "":
        return jsonify(Error="Brukernavn er påkrevd.")

    if password is None or password == "":
        return jsonify(Error="Passord er påkrevd.")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify(Error="Feil brukernavn eller passord.")

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
            "is_pending": current_user.is_pending,
            "avatar": current_user.avatar,
        }
    )
