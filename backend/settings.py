from auth import admin_required
from database import User, avatar_path, db
from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required

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

    new_user = User(username=username, password=password, is_pending=True)
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
