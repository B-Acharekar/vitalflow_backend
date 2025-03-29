from flask import Blueprint, request, jsonify
from services.water_intake_services import log_water_intake, get_water_intake

water_bp = Blueprint("water", __name__)

@water_bp.route('/log-water', methods=['POST'])
def log_water():
    data = request.json
    user_id = data.get("user_id")  
    water_intake_ml = data.get("water_intake_ml")

    if not user_id or not water_intake_ml:
        return jsonify({"error": "Missing user_id or water_intake_ml"}), 400
    
    return log_water_intake(user_id, water_intake_ml)  # Directly returning response

@water_bp.route('/get-water/<user_id>', methods=['GET'])
def get_water(user_id):
    range_type = request.args.get('range', 'today')  # Default to 'today'
    return get_water_intake(user_id, range_type)