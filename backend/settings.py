from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from database import db, avatar_path
from flask import request
from flask import jsonify


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
