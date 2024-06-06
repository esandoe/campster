from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
import random
import click
from flask import current_app as app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext

migrate = Migrate()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def is_initialized():
    """
    Checks if the database has been initialized by checking the database migration revision.
    """
    migration_context = MigrationContext.configure(db.engine.connect())
    current_revision = migration_context.get_current_heads()
    app.logger.info(f"Current database head version(s): {current_revision}")
    return len(current_revision) > 0


def _echo_warning(message):
    click.secho(message, bg="yellow", fg="black")


def _echo_error(message):
    click.secho(message, bg="red", fg="white")


def check_pending_migrations():
    """
    Checks if there are any pending database migrations.
    """
    with db.engine.connect() as conn:
        script_ = ScriptDirectory("migrations")
        context = MigrationContext.configure(conn)
        db_revision = context.get_current_heads()[0]
        script_revision = script_.get_heads()[0]

        if db_revision != script_revision:
            _echo_error("The database is not up-to-date. Upgrade the database.")

            click.secho("Missing migrations:", bg="red", fg="white")
            for revision in script_.iterate_revisions(script_revision, db_revision):
                click.secho(f" - {revision}", bg="red", fg="white")

            _echo_warning(
                "The app may not work correctly until the database is upgraded"
            )
            _echo_warning("Run 'flask db upgrade' to upgrade the database.")


class avatar_path(str, Enum):
    AVATAR_0 = "avatar_0.jpg"
    AVATAR_1 = "avatar_1.jpg"
    AVATAR_2 = "avatar_2.jpg"
    AVATAR_3 = "avatar_3.jpg"
    AVATAR_4 = "avatar_4.jpg"
    AVATAR_5 = "avatar_5.jpg"
    AVATAR_6 = "avatar_6.jpg"
    AVATAR_7 = "avatar_7.jpg"
    AVATAR_8 = "avatar_8.jpg"
    AVATAR_9 = "avatar_9.jpg"
    AVATAR_10 = "avatar_10.jpg"
    AVATAR_11 = "avatar_11.jpg"
    AVATAR_12 = "avatar_12.jpg"
    AVATAR_13 = "avatar_13.jpg"
    AVATAR_14 = "avatar_14.jpg"
    AVATAR_15 = "avatar_15.jpg"
    AVATAR_16 = "avatar_16.jpg"
    AVATAR_17 = "avatar_17.jpg"
    AVATAR_18 = "avatar_18.jpg"
    AVATAR_19 = "avatar_19.jpg"
    AVATAR_20 = "avatar_20.jpg"
    FNIBS = "fnibs.png"
    GRETP = "gretp.png"
    KLERB = "klerb.png"
    RTYNM = "rtynm.png"


@dataclass
class User(UserMixin, db.Model):
    """
    User model.

    Args:
        id (int): Primary key.
        username (str): Unique username.
        password (str): Password. Should be hashed using scrypt.
        avatar (avatar_path): Avatar image path.
        is_admin (bool): Is admin.
        is_pending (bool): Is pending a password reset (for newly created users).
        created_at (datetime): Created at.
        updated_at (datetime): Updated at.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    avatar: Mapped[avatar_path] = mapped_column(default=avatar_path.FNIBS)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_pending: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


@dataclass
class ParticipantItem(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    index: Mapped[int] = mapped_column(
        default=lambda: random.randint(1, 1_000_000) * 1000, nullable=False
    )
    participant_id: Mapped[int] = mapped_column(ForeignKey("trip_participant.id"))
    supply_target: Mapped["SupplyTarget"] = relationship(
        "SupplyTarget", backref="participant_items"
    )
    supply_target_id: Mapped[int] = mapped_column(
        ForeignKey("supply_target.id"), nullable=True
    )
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column(default=1)
    packed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


@dataclass
class TripParticipant(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(User, backref="trip_participations")
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    items: Mapped[list[ParticipantItem]] = relationship("ParticipantItem")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


@dataclass
class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participants: Mapped[list[TripParticipant]] = relationship(
        TripParticipant, backref="trip"
    )
    name: Mapped[str] = mapped_column(unique=True)
    start_date: Mapped[date] = mapped_column(nullable=True)
    end_date: Mapped[date] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


@dataclass
class SupplyTarget(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    name: Mapped[str] = mapped_column(unique=True)
    target_quantity: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
