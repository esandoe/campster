import os
import random
import string
import sys
from threading import Thread

from auth import admin_required
from database import User, avatar_path, db
from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

settings = Blueprint("settings", __name__)


@login_required
@settings.route("/api/profile/avatar", methods=["POST"])
def update_avatar():
    body = request.get_json()

    current_user.avatar = body["avatar"]
    db.session.commit()

    return jsonify(current_user.avatar)


@login_required
@settings.route("/api/list-avatars", methods=["GET"])
def list_avatars():
    return jsonify([avatar for avatar in avatar_path])


@settings.route("/api/settings/user/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.json
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    confirm_new_password = data.get("confirm_new_password")

    if not old_password or not new_password or not confirm_new_password:
        return jsonify(Error="Fyll nå ut alle felter og prøv igjen."), 400

    if new_password != confirm_new_password:
        return jsonify(Error="Nye passord er ikke like."), 400

    user = User.query.get(current_user.id)

    if not check_password_hash(user.password, old_password):
        return jsonify(Error="Det gamle passordet er feil."), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify(success=True), 200


@admin_required
@settings.route("/api/settings/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(
        [
            {"id": user.id, "username": user.username, "is_admin": user.is_admin}
            for user in users
        ]
    )


@admin_required
@settings.route("/api/settings/users", methods=["POST"])
def add_user():
    body = request.get_json()
    username = body["username"]
    password = body["temp_password"]

    if not username or not password:
        return jsonify(Error="Username and password are required"), 400

    if password.strip() == "":
        return jsonify(Error="Password cannot be empty or whitespace"), 400

    if username.strip() == "":
        return jsonify(Error="Username cannot be empty or whitespace"), 400

    if len(password) < 8:
        return jsonify(Error="Password must be at least 8 characters"), 400

    if len(username) < 3:
        return jsonify(Error="Username must be at least 3 characters"), 400

    if username == "admin":
        return jsonify(Error="Username cannot be admin"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(Error="Username already exists"), 400

    password_hashed = generate_password_hash(password)
    new_user = User(username=username, password=password_hashed, is_pending=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(Success="User created")


@admin_required
@settings.route("/api/settings/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id == current_user.id:
        abort(400, "Cannot delete yourself")
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify(Success="User deleted")


@admin_required
@settings.route("/api/settings/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    body = request.get_json()

    if user_id == current_user.id and not body["is_admin"]:
        abort(400, "Cannot demote yourself")

    user.is_admin = body["is_admin"]
    db.session.commit()

    return jsonify(Success="User updated")


@admin_required
@settings.route("/api/settings/users/<int:user_id>/password-reset", methods=["PUT"])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)

    if user_id == current_user.id:
        abort(400, "Cannot reset your own password.")

    password = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )
    password_hashed = generate_password_hash(password)

    user.password = password_hashed
    user.is_pending = True
    db.session.commit()

    return jsonify(Success="Password reset", TemporaryPassword=password)


@admin_required
@settings.route("/api/settings/server/update", methods=["POST"])
def update_server():
    from git import Repo

    print("Pulling latest changes")
    repo = Repo("..")
    repo.remotes.origin.pull()

    print("Building frontend...")
    from pynpm import NPMPackage

    pkg = (
        NPMPackage(
            "../client/package.json", shell=True
        )  # Have to use shell=True on Windows
        if os.name == "nt"
        else NPMPackage("../client")
    )
    pkg.build()

    def restart():
        # wait a couple seconds before restarting
        import time

        time.sleep(2)

        print("Restarting server...")
        os.execv(sys.argv[0], sys.argv)

    # Start a new thread to restart the server, so we can return a response to the client first
    thread = Thread(target=restart)
    thread.start()

    return jsonify("Ok")
