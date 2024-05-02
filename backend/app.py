from flask import Flask, jsonify
from flask_cors import CORS
from database import db, Trip, TripParticipant, ParticipantItem, User, SupplyTarget

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


@app.route("/api/trip/<trip_id>/participants", methods=["GET"])
def get_trip_participants(trip_id):
    participants = TripParticipant.query.filter_by(trip_id=trip_id).all()
    return jsonify(participants)


@app.route("/api/trip/<trip_id>/supply-targets", methods=["GET"])
def get_supply_targets(trip_id):
    targets = SupplyTarget.query.filter_by(trip_id=trip_id).all()
    return jsonify(targets)


@app.route("/api/trip/<trip_id>/participant/<participant_id>/items", methods=["GET"])
def get_participant_items(trip_id, participant_id):
    items = (
        TripParticipant.query.filter_by(trip_id=trip_id, id=participant_id)
        .first_or_404()
        .items
    )

    return jsonify(items)


if __name__ == "__main__":
    app.run()
