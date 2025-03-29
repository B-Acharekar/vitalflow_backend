from flask import Blueprint, request, jsonify
from services.steps_services import log_steps, get_steps

steps_bp = Blueprint("steps", __name__)

@steps_bp.route('/log-steps', methods=['POST'])
def log_steps_routes():
    data = request.json
    user_id = data.get("user_id")  
    steps_count = data.get("steps_count")
    steps_goal = data.get("steps_goal")

    if not user_id or not steps_count:
        return jsonify({"error": "Missing user_id or steps"}), 400
    elif not steps_goal:
        steps_goal = None  # Set steps_goal to None if not provided in request
        
    return log_steps(user_id,steps_count,steps_goal)  # Directly returning response

@steps_bp.route('/get-steps/<user_id>', methods=['GET'])
def get_steps_routes(user_id):
    range_type = request.args.get('range','today')
    return get_steps(user_id,range_type)  # ✅ Removed incorrect dictionary placement
