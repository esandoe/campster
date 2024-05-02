from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class avatar_path(str, Enum):
    FNIBS = "fnibs.png"
    GRETP = "gretp.png"
    KLERB = "klerb.png"
    RTYNM = "rtynm.png"


@dataclass
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    avatar: Mapped[avatar_path] = mapped_column(default=avatar_path.FNIBS)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)


@dataclass
class ParticipantItem(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("trip_participant.id"))
    supply_target: Mapped["SupplyTarget"] = relationship("SupplyTarget")
    supply_target_id: Mapped[int] = mapped_column(
        ForeignKey("supply_target.id"), nullable=True
    )
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column(default=0)
    packed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)


@dataclass
class TripParticipant(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(User)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    items: Mapped[list[ParticipantItem]] = relationship("ParticipantItem")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)


@dataclass
class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participants: Mapped[list[TripParticipant]] = relationship(TripParticipant)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)


@dataclass
class SupplyTarget(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    name: Mapped[str] = mapped_column(unique=True)
    target_quantity: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
