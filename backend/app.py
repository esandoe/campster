from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from database import ParticipantItem, db, Trip, TripParticipant, SupplyTarget

from sample_data import sample_trips


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campster.db"
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

    for trip in sample_trips:
        db.session.add(trip)
    db.session.commit()


# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/api/trips", methods=["GET"])
def get_trips():
    trips = Trip.query.all()
    return jsonify(trips)


@app.route("/api/trips/<trip_id>", methods=["GET"])
def get_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id).first_or_404()

    return jsonify(
        {
            "id": trip.id,
            "name": trip.name,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "location": trip.location,
            "participants": [participant.user for participant in trip.participants],
        }
    )


@app.route("/api/trip/<trip_id>/participants", methods=["GET"])
def get_trip_participants(trip_id):
    participants = (
        TripParticipant.query.filter_by(trip_id=trip_id)
        .join(TripParticipant.user)
        .all()
    )
    users = [participant.user for participant in participants]
    return jsonify(users)


@app.route("/api/trip/<trip_id>/supply-targets", methods=["GET"])
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


@app.route("/api/trip/<trip_id>/participant/<participant_id>/items", methods=["GET"])
def get_participant_items(trip_id, participant_id):
    items = (
        TripParticipant.query.filter_by(trip_id=trip_id, id=participant_id)
        .first_or_404()
        .items
    )

    return jsonify(items)


@app.route("/api/participant/<participant_id>/items", methods=["POST"])
def add_participant_item(participant_id):
    participant = TripParticipant.query.filter_by(id=participant_id).first_or_404()

    item = ParticipantItem(participant_id=participant_id, name=request.json["name"])
    participant.items.append(item)
    db.session.commit()
    return jsonify(item)


@app.route("/api/participant/<participant_id>/items/<item_id>", methods=["PUT"])
def update_participant_item(participant_id, item_id):
    item = ParticipantItem.query.filter_by(
        id=item_id, participant_id=participant_id
    ).first_or_404()

    item.name = request.json["name"]
    item.quantity = request.json["quantity"]
    item.packed = request.json["packed"]

    db.session.commit()
    return jsonify(
        {"name": item.name, "quantity": item.quantity, "packed": item.packed}
    )


@app.route("/api/participant/<participant_id>/items", methods=["DELETE"])
def delete_participant_item(participant_id):
    item = ParticipantItem.query.filter_by(
        participant_id=participant_id, id=request.json["id"]
    ).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)


@app.route("/avatars/<filename>", methods=["GET"])
def get_avatar(filename):
    return send_from_directory("avatars", filename)


if __name__ == "__main__":
    app.run()
