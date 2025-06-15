from datetime import date
from logging.config import dictConfig
from os import makedirs, path, remove

from auth import (
    item_owner_required,
    participant_of_trip_required,
    participant_self_required,
)
from database import (
    ParticipantItem,
    SupplyTarget,
    Trip,
    TripAttachment,
    TripParticipant,
    User,
    check_pending_migrations,
    db,
    is_initialized,
    migrate,
)
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required
from setup.initial_setup import intial_setup
from werkzeug.utils import secure_filename

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

        if app.debug:
            check_pending_migrations()

    return app


app = create_app()

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/api/trips", methods=["GET"])
@login_required
def get_trips():
    trips = Trip.query.all()
    return jsonify(trips)


@app.route("/api/trips", methods=["POST"])
@login_required
def add_trip():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing required field: name"}), 400
    trip = Trip(
        name=data["name"],
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
@participant_of_trip_required
def update_trip(trip_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON in request body"}), 400
    trip = Trip.query.filter_by(id=trip_id).first_or_404()
    if "name" in data:
        trip.name = data["name"]
    if "start_date" in data:
        trip.start_date = date.fromisoformat(data["start_date"])
    if "end_date" in data:
        trip.end_date = date.fromisoformat(data["end_date"])
    if "location" in data:
        trip.location = data["location"]
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


@app.route("/api/trips/<trip_id>/attachments/", methods=["GET"])
@login_required
def get_attachments(trip_id):
    participants = TripParticipant.query.filter_by(trip_id=trip_id).all()
    attachments = [
        {
            "id": attachment.id,
            "filename": attachment.filename,
            "filepath": f"/trips/{trip_id}/files/{attachment.filename}",
            "text": attachment.text,
            "user": {
                "name": participant.user.username,
                "avatar": participant.user.avatar,
            },
            "created_at": attachment.created_at,
            "updated_at": attachment.updated_at,
        }
        for participant in participants
        for attachment in participant.attachments
    ]
    return jsonify(attachments)


@app.route("/api/trips/<trip_id>/attachments/upload-file/", methods=["POST"])
@login_required
@participant_of_trip_required
def upload_file(trip_id):
    if "file" not in request.files:
        return jsonify(Error="No file part")
    file = request.files["file"]
    if not file or not file.filename:
        return jsonify(Error="No selected file")
    filename = secure_filename(file.filename)
    file_path = f"uploads/trips/{trip_id}/attachments/{filename}"
    if path.exists(file_path):
        return jsonify(Error="File already exists")
    makedirs(f"uploads/trips/{trip_id}/attachments/", exist_ok=True)
    file.save(file_path)
    return jsonify(filename)


@app.route("/api/trips/<trip_id>/attachments/", methods=["POST"])
@login_required
@participant_of_trip_required
def add_attachment(trip_id):
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing required field: text"}), 400
    if "filename" not in data or not data["filename"]:
        return jsonify({"error": "Missing required field: filename"}), 400

    participant = TripParticipant.query.filter_by(
        trip_id=trip_id, user_id=current_user.id
    ).first_or_404()
    attachment = TripAttachment(
        trip_id=trip_id,
        participant_id=participant.id,
        filename=data["filename"],
        text=data["text"],
    )
    db.session.add(attachment)
    db.session.commit()
    return jsonify(
        {
            "id": attachment.id,
            "filename": attachment.filename,
            "filepath": f"/trips/{trip_id}/files/{attachment.filename}",
            "text": attachment.text,
            "user": {
                "name": participant.user.username,
                "avatar": participant.user.avatar,
            },
            "created_at": attachment.created_at,
            "updated_at": attachment.updated_at,
        }
    )


# delete attachment
@app.route("/api/trips/<trip_id>/attachments/<attachment_id>", methods=["DELETE"])
@login_required
@participant_of_trip_required
def delete_attachment(trip_id, attachment_id):
    attachment = TripAttachment.query.filter_by(
        id=attachment_id, trip_id=trip_id
    ).first_or_404()

    if attachment.filename:
        file_path = f"uploads/trips/{trip_id}/attachments/{attachment.filename}"
        if path.exists(file_path):
            remove(file_path)

    db.session.delete(attachment)
    db.session.commit()
    return jsonify(success=True)


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
@participant_of_trip_required
def delete_supply_target(trip_id, supply_target_id):
    target = SupplyTarget.query.filter_by(
        id=supply_target_id, trip_id=trip_id
    ).first_or_404()
    db.session.delete(target)
    db.session.commit()
    return jsonify(success=True)


@app.route("/api/trip/<trip_id>/supply-targets", methods=["POST"])
@login_required
@participant_of_trip_required
def add_supply_target(trip_id):
    data = request.get_json()
    if not data or "name" not in data or "target_quantity" not in data:
        return jsonify({"error": "Missing required fields: name, target_quantity"}), 400
    target = SupplyTarget(
        trip_id=trip_id,
        name=data["name"],
        target_quantity=data["target_quantity"],
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


@app.route(
    "/api/trip/<trip_id>/participant/<participant_id>/autofill", methods=["POST"]
)
@login_required
def autofill_participant_items(trip_id, participant_id):
    """
    Endpoint which autofills the participants list by using the previous trips list
    """
    current_trip = TripParticipant.query.filter_by(
        trip_id=trip_id, id=participant_id
    ).first_or_404()

    if len(current_trip.items) > 0:
        abort(400)

    previous_trip = (
        TripParticipant.query.filter(TripParticipant.user_id == current_trip.user_id)
        .filter(TripParticipant.trip_id != trip_id)
        .filter(TripParticipant.items.any())
        .order_by(TripParticipant.created_at.desc())
        .first_or_404()
    )

    items = [
        ParticipantItem(participant_id=participant_id, name=item.name, index=item.index)
        for item in previous_trip.items
    ]

    current_trip.items.extend(items)
    db.session.commit()
    return jsonify(items)


@app.route("/api/items", methods=["GET"])
@login_required
def get_all_item_names():
    item_names = (
        ParticipantItem.query.with_entities(ParticipantItem.name).distinct().all()
    )
    return jsonify([item_name[0] for item_name in item_names])


@app.route("/api/participant/<participant_id>/items", methods=["POST"])
@login_required
@participant_self_required
def add_participant_item(participant_id):
    data = request.get_json()
    if not data or "name" not in data or "index" not in data:
        return jsonify({"error": "Missing required fields: name, index"}), 400
    participant = TripParticipant.query.filter_by(id=participant_id).first_or_404()
    item = ParticipantItem(
        participant_id=participant_id,
        name=data["name"],
        index=data["index"],
    )
    participant.items.append(item)
    db.session.commit()
    return jsonify(item)


@app.route("/api/participant/<participant_id>/items/<item_id>", methods=["PUT"])
@login_required
@item_owner_required
def update_participant_item(participant_id, item_id):
    data = request.get_json()
    required_fields = ["index", "supply_target_id", "name", "quantity", "packed"]
    if not data or not all(field in data for field in required_fields):
        return (
            jsonify(
                {"error": f"Missing required fields: {', '.join(required_fields)}"}
            ),
            400,
        )
    item = ParticipantItem.query.filter_by(
        id=item_id, participant_id=participant_id
    ).first_or_404()
    item.index = data["index"]
    item.supply_target_id = data["supply_target_id"]
    item.name = data["name"]
    item.quantity = data["quantity"]
    item.packed = data["packed"]
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


@app.route("/api/participant/<participant_id>/items/<item_id>", methods=["DELETE"])
@login_required
@item_owner_required
def delete_participant_item(participant_id, item_id):
    item = ParticipantItem.query.filter_by(
        participant_id=participant_id, id=item_id
    ).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)


@app.route("/avatars/<filename>", methods=["GET"])
@login_required
def get_avatar(filename):
    return send_from_directory("avatars", filename)


@app.route("/trips/<trip_id>/files/<filename>", methods=["GET"])
@login_required
def get_file(trip_id, filename):
    return send_from_directory(f"uploads/trips/{trip_id}/attachments", filename)


if __name__ == "__main__":
    app.run()
