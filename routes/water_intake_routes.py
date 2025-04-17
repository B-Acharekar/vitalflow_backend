from flask import Blueprint, request, jsonify
from services.water_intake_services import log_water_intake, get_water_intake
from analyze.water_analyzer import extract_water_intake

water_bp = Blueprint("water", __name__)

@water_bp.route('/log-water', methods=['POST'])
def log_water():
    data = request.json
    user_id = data.get("user_id")
    note = data.get("note")

    if not user_id or not note:
        return jsonify({"error": "Missing user_id or note"}), 400

    # NLP analyzer to convert note -> water intake (ml)
    water_intake_ml = extract_water_intake(note)

    if water_intake_ml <= 0:
        return jsonify({"error": "Could not interpret water intake from note"}), 400

    # Log both ml and original note
    response = log_water_intake(user_id, water_intake_ml, note=note)

    return response

@water_bp.route('/get-water/<user_id>', methods=['GET'])
def get_water(user_id):
    range_type = request.args.get('range', 'today')  # Optional query param
    return get_water_intake(user_id, range_type)
