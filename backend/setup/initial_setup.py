import click
from database import User, db
from flask import current_app as app
from flask_migrate import upgrade
from setup.sample_data import sample_trips
from werkzeug.security import generate_password_hash


def intial_setup():
    # Create the database by running all migrations
    run_database_migrations()

    # To log into the application we need a user! So we create the first admin user right away
    create_admin_user()

    # Initialize database with dummy data
    app.logger.info("Initializing database with sample data")
    for trip in sample_trips:
        db.session.add(trip)
    db.session.commit()

    app.logger.info("Campster has been successfully initialized! Enjoy camping!")


def run_database_migrations():
    """
    Checks for any available migrations and runs them.
    """
    try:
        upgrade()
    except Exception as e:
        raise RuntimeError(f"Error running database migrations: {e}") from e


def create_admin_user():
    """
    Creates an admin user for the application.
    """
    while True:
        username = click.prompt("Enter admin username", type=str)
        password = click.prompt("Password", hide_input=True)
        confirm_password = click.prompt("Confirm password", hide_input=True)

        if password != confirm_password:
            click.echo("Passwords didn't match! Try again:")
        else:
            break

    hashed_password = generate_password_hash(password, method="scrypt")
    admin = User(username=username, password=hashed_password, is_admin=True)
    db.session.add(admin)
    db.session.commit()

    app.logger.info("Admin user successfully created")
