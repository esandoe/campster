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


@login_required
@settings.route("/api/settings/users", methods=["GET"])
def get_users():
    if not current_user.is_admin:
        return abort(403)

    users = User.query.all()
    return jsonify(
        [
            {"id": user.id, "username": user.username, "is_admin": user.is_admin}
            for user in users
        ]
    )
