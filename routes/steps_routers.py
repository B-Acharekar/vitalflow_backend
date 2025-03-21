from flask import Blueprint, request, jsonify
from services.steps_services import log_steps, get_steps

steps_bp = Blueprint("steps", __name__)

@steps_bp.route('/log-steps', methods=['POST'])
def log_steps_routes():
    data = request.json
    user_id = data.get("user_id")  
    steps_count = data.get("steps_count")

    if not user_id or not steps_count:
        return jsonify({"error": "Missing user_id or steps"}), 400
    
    return log_steps(user_id,steps_count)  # Directly returning response

@steps_bp.route('/get-steps/<user_id>', methods=['GET'])
def get_steps_routes(user_id):
    return get_steps(user_id)  # ✅ Removed incorrect dictionary placement
