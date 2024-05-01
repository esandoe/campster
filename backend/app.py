from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Table
from sample_data import sample_trip_item_data, sample_list_entry_data, sample_trip_data


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


trip_participants = Table(
    "trip_participants",
    db.Model.metadata,
    Column("trip_id", ForeignKey("trip.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)


@dataclass
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


@dataclass
class Item(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    name: Mapped[str] = mapped_column(unique=True)
    shared_target: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime]

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class ListEntry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    amount: Mapped[int]
    shared_amount: Mapped[int]
    packed: Mapped[bool]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    participants: Mapped[list[User]] = relationship(secondary=trip_participants)
    items: Mapped[list[Item]] = relationship(Item)
    listEntries: Mapped[list[ListEntry]] = relationship(ListEntry)


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campster.db"
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

    for trip in sample_trip_data:
        new_trip = Trip(name=trip["name"])
        trip_participants = [User(id=user_id) for user_id in trip["participants"]]
        db.session.add(new_trip)
    for item in sample_trip_item_data:
        trip_item = Item(
            name=item["name"],
            trip_id=1,
            shared_target=item.get("shared_target", 0),
            created_at=datetime.now(),
        )
        db.session.add(trip_item)
    db.session.commit()

    for entry in sample_list_entry_data:
        list_entry = ListEntry(
            item_id=entry["item_id"],
            user_id=entry["user_id"],
            trip_id=entry["trip_id"],
            amount=entry["amount"],
            shared_amount=entry["shared_amount"],
            packed=entry["packed"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.session.add(list_entry)
    db.session.commit()

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/api/trips", methods=["GET"])
def get_trips():
    trips = Trip.query.all()
    return jsonify(trips)


@app.route("/api/trip/<trip_id>/items", methods=["GET"])
def get_trip_items(trip_id):
    items = Trip.query.filter_by(id=trip_id).first().items
    return jsonify(items)


@app.route("/api/trip/<trip_id>/user/<user_id>/entries", methods=["GET"])
def get_trip_list_entries(trip_id, user_id):
    entries = ListEntry.query.filter_by(trip_id=trip_id, user_id=user_id).all()
    return jsonify(entries)


if __name__ == "__main__":
    app.run()
