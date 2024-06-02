from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from database import User, db
from flask import request
from flask import jsonify


settings = Blueprint("settings", __name__)


@settings.route("/api/profile/avatar", methods=["POST"])
@login_required
def update_avatar():
    body = request.get_json()

    current_user.avatar = body["avatar"]
    db.session.commit()

    return jsonify(current_user.avatar)
