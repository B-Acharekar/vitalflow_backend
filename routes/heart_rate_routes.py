from flask import Blueprint, request, jsonify
from services.heart_rate_services import heart_rate_log,get_heart_rate_log

heart_rate_bp = Blueprint("heart_rate", __name__)

@heart_rate_bp.route('/log-heart-rate', methods=['POST'])
def log_heart():
    data = request.json
    user_id = data.get("user_id")  
    heart_rate_bpm = data.get("heart_rate_bpm")

    if not user_id or not heart_rate_bpm:
        return jsonify({"error": "Missing user_id or heart_rate_bpm"}), 400
    
    return heart_rate_log(user_id,heart_rate_bpm)  # Directly returning response

@heart_rate_bp.route('/get-heart-rate/<user_id>', methods=['GET'])
def get_health(user_id):
    return get_heart_rate_log(user_id)  # ✅ Removed incorrect dictionary placement
