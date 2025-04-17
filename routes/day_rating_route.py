from flask import Blueprint, request
from services.day_rating_service import add_day_rating, get_day_rating

day_rating_bp = Blueprint("day_rating", __name__)

@day_rating_bp.route("/day-rating/log", methods=["POST"])
def log_day_rating():
    """API to log a new day rating"""
    data = request.get_json()
    user_id = data.get("user_id")
    user_note = data.get("user_note", "")  # Optional note from the user

    if not user_id:
        return {"error": "user_id is required"}, 400

    return add_day_rating(user_id, user_note)

@day_rating_bp.route("/day-rating/get", methods=["GET"])
def fetch_day_rating():
    """API to get day rating"""
    user_id = request.args.get("user_id")
    time_range = request.args.get("time_range", "today")

    if not user_id:
        return {"error": "user_id is required"}, 400

    return get_day_rating(user_id, time_range)
