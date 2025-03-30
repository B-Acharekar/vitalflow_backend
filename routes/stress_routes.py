from flask import Blueprint,request,jsonify
from services.stress_log_services import add_stress_log,get_stress_log

stress_bp = Blueprint("stress", __name__)

@stress_bp.route('/log-stress', methods=['POST'])
def add_stress():
    """Route to add a new stress log."""
    data = request.json
    return add_stress_log(data.get("user_id"), data.get("stress_level"), data.get("note", ""))

@stress_bp.route('/get-stress/<user_id>/<time_range>', methods=['GET'])
def get_stress_route(user_id, time_range):
    return get_stress_log(user_id, time_range)

