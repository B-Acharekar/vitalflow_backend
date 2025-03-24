from flask import Blueprint, request, jsonify
from services.sleep_services import log_sleep, get_sleep

sleep_bp = Blueprint("sleep", __name__)

@sleep_bp.route('/log-sleep', methods=['POST'])
def log_sleep_routes():
    data = request.json
    user_id = data.get("user_id")  
    sleep_duration_min = data.get("sleep_duration_min")
    sleep_quality = data.get("sleep_quality")
    sleep_goal = data.get("sleep_goal")

    if not user_id or not sleep_duration_min or not sleep_quality:
        return jsonify({"error": "Missing user_id or sleep"}), 400
    elif not sleep_goal:
        sleep_goal = None
    return log_sleep(user_id,sleep_duration_min,sleep_quality,sleep_goal)  # Directly returning response

@sleep_bp.route('/get-sleep/<user_id>', methods=['GET'])
def get_sleep_routes(user_id):
    return get_sleep(user_id)  # ✅ Removed incorrect dictionary placement
