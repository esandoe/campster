from datetime import date
from functools import wraps
from logging.config import dictConfig

from database import (
    ParticipantItem,
    SupplyTarget,
    Trip,
    TripParticipant,
    User,
    db,
    is_initialized,
    migrate,
)
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required
from setup.initial_setup import intial_setup

# Configure logging format and set log level to INFO
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


# instantiate the app
def create_app():
    app = Flask(__name__)

    app.config.from_object(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campster.db"
    app.config["SECRET_KEY"] = "super-secret-key"

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from auth import auth as auth_blueprint
    from settings import settings as settings_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(settings_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        if not is_initialized():
            app.logger.info("Initializing the application for first startup...")
            intial_setup()

    return app


app = create_app()

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


def participant_or_admin_required(f):
    """Decorator to check if the current user is a participant of the trip or an admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        trip_id = kwargs.get("trip_id")
        trip = Trip.query.filter_by(id=trip_id).first_or_404()
        if current_user.is_admin or trip.has_participant(current_user):
            return f(*args, **kwargs)
        return jsonify(Error="Unauthorized")

    return decorated_function


@app.route("/api/trips", methods=["GET"])
@login_required
def get_trips():
    trips = Trip.query.all()
    return jsonify(trips)


@app.route("/api/trips", methods=["POST"])
@login_required
def add_trip():
    trip = Trip(
        name=request.json["name"],
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify(trip)


@app.route("/api/trips/<trip_id>", methods=["GET"])
@login_required
def get_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id).first_or_404()

    return jsonify(
        {
            "id": trip.id,
            "name": trip.name,
            "start_date": trip.start_date.isoformat() if trip.start_date else None,
            "end_date": trip.end_date.isoformat() if trip.end_date else None,
            "location": trip.location,
            "participants": [
                {
                    "id": participant.id,
                    "user_id": participant.user.id,
                    "username": participant.user.username,
                    "avatar": participant.user.avatar,
                }
                for participant in trip.participants
            ],
        }
    )


@app.route("/api/trips/<trip_id>", methods=["PUT"])
@login_required
@participant_or_admin_required
def update_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id).first_or_404()

    if "name" in request.json:
        trip.name = request.json["name"]
    if "start_date" in request.json:
        trip.start_date = date.fromisoformat(request.json["start_date"])
    if "end_date" in request.json:
        trip.end_date = date.fromisoformat(request.json["end_date"])
    if "location" in request.json:
        trip.location = request.json["location"]

    db.session.commit()

    return jsonify(
        {
            "id": trip.id,
            "name": trip.name,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "location": trip.location,
        }
    )


@app.route("/api/trip/<trip_id>/participants", methods=["GET"])
@login_required
def get_participants(trip_id):
    participants = (
        TripParticipant.query.filter_by(trip_id=trip_id)
        .join(TripParticipant.user)
        .all()
    )
    participants = [
        {
            "id": participant.id,
            "user_id": participant.user.id,
            "username": participant.user.username,
            "avatar": participant.user.avatar,
        }
        for participant in participants
    ]
    return jsonify(participants)


@app.route("/api/trips/<trip_id>/join", methods=["POST"])
@login_required
def join_trip(trip_id):
    user_id = current_user.id

    if TripParticipant.query.filter_by(trip_id=trip_id, user_id=user_id).first():
        return jsonify(Error="User is already a participant of the trip")

    participant = TripParticipant(trip_id=trip_id, user_id=user_id)
    db.session.add(participant)
    db.session.commit()

    return jsonify(
        {
            "id": participant.id,
            "user_id": participant.user.id,
            "username": participant.user.username,
            "avatar": participant.user.avatar,
        }
    )


@app.route("/api/trip/<trip_id>/supply-targets", methods=["GET"])
@login_required
def get_supply_targets(trip_id):
    targets = SupplyTarget.query.filter_by(trip_id=trip_id).all()

    return jsonify(
        [
            {
                "id": target.id,
                "name": target.name,
                "target_quantity": target.target_quantity,
                "items": [
                    {"id": item.id, "name": item.name, "quantity": item.quantity}
                    for item in ParticipantItem.query.filter_by(
                        supply_target=target
                    ).all()
                ],
            }
            for target in targets
        ]
    )


@app.route("/api/trip/<trip_id>/supply-targets/<supply_target_id>", methods=["DELETE"])
@login_required
@participant_or_admin_required
def delete_supply_target(trip_id, supply_target_id):
    target = SupplyTarget.query.filter_by(
        id=supply_target_id, trip_id=trip_id
    ).first_or_404()
    db.session.delete(target)
    db.session.commit()
    return jsonify(success=True)


@app.route("/api/trip/<trip_id>/supply-targets", methods=["POST"])
@login_required
@participant_or_admin_required
def add_supply_target(trip_id):
    target = SupplyTarget(
        trip_id=trip_id,
        name=request.json["name"],
        target_quantity=request.json["target_quantity"],
    )
    db.session.add(target)
    db.session.commit()
    return jsonify(target)


@app.route("/api/trip/<trip_id>/participant/<participant_id>/items", methods=["GET"])
@login_required
def get_participant_items(trip_id, participant_id):
    items = (
        TripParticipant.query.filter_by(trip_id=trip_id, id=participant_id)
        .first_or_404()
        .items
    )

    return jsonify(items)


@app.route("/api/participant/<participant_id>/items", methods=["POST"])
@login_required
@participant_or_admin_required
def add_participant_item(participant_id):
    participant = TripParticipant.query.filter_by(id=participant_id).first_or_404()

    item = ParticipantItem(participant_id=participant_id, name=request.json["name"])
    participant.items.append(item)
    db.session.commit()
    return jsonify(item)


@app.route("/api/participant/<participant_id>/items/<item_id>", methods=["PUT"])
@login_required
@participant_or_admin_required
def update_participant_item(participant_id, item_id):
    item = ParticipantItem.query.filter_by(
        id=item_id, participant_id=participant_id
    ).first_or_404()

    item.index = request.json["index"]
    item.supply_target_id = request.json["supply_target_id"]
    item.name = request.json["name"]
    item.quantity = request.json["quantity"]
    item.packed = request.json["packed"]

    db.session.commit()
    return jsonify(
        {
            "index": item.index,
            "supply_target_id": item.supply_target_id,
            "name": item.name,
            "quantity": item.quantity,
            "packed": item.packed,
        }
    )


@app.route("/api/participant/<participant_id>/items", methods=["DELETE"])
@login_required
@participant_or_admin_required
def delete_participant_item(participant_id):
    item = ParticipantItem.query.filter_by(
        participant_id=participant_id, id=request.json["id"]
    ).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)


@app.route("/avatars/<filename>", methods=["GET"])
@login_required
def get_avatar(filename):
    return send_from_directory("avatars", filename)


if __name__ == "__main__":
    app.run()
