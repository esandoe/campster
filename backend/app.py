from database import ParticipantItem, SupplyTarget, Trip, TripParticipant, db
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from sample_data import sample_trips


# instantiate the app
def create_app():
    app = Flask(__name__)

    app.config.from_object(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campster.db"
    app.config["SECRET_KEY"] = "super-secret-key"

    db.init_app(app)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # Initialize database with dummy data on each restart
    with app.app_context():
        db.drop_all()
        db.create_all()

        for trip in sample_trips:
            db.session.add(trip)
        db.session.commit()

    login_manager = LoginManager()
    login_manager.init_app(app)

    from database import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


app = create_app()

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/api/trips", methods=["GET"])
def get_trips():
    trips = Trip.query.all()
    return jsonify(trips)


@app.route("/api/trips", methods=["POST"])
def add_trip():
    trip = Trip(
        name=request.json["name"],
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify(trip)


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
def get_participants(trip_id):
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


@app.route("/api/trip/<trip_id>/supply-targets/<supply_target_id>", methods=["DELETE"])
def delete_supply_target(trip_id, supply_target_id):
    target = SupplyTarget.query.filter_by(
        id=supply_target_id, trip_id=trip_id
    ).first_or_404()
    db.session.delete(target)
    db.session.commit()
    return jsonify(success=True)


@app.route("/api/trip/<trip_id>/supply-targets", methods=["POST"])
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
