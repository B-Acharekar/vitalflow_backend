from flask import Blueprint, request, jsonify
from services.health_log_services import health_log,get_health_log

health_bp = Blueprint("health", __name__)

@health_bp.route('/log-health', methods=['POST'])
def log_health():
    data = request.json
    user_id = data.get("user_id")  
    weight = data.get("weight")
    height = data.get("height")

    if not user_id or not weight or not height:
        return jsonify({"error": "Missing user_id or water_intake_ml"}), 400
    
    return health_log(user_id,weight,height)  # Directly returning response

@health_bp.route('/get-health/<user_id>', methods=['GET'])
def get_health(user_id):
    return get_health_log(user_id)  # ✅ Removed incorrect dictionary placement
