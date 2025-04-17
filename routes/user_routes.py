from flask import Blueprint, request, jsonify
from services.user_services import forgot_password, get_username_by_id, register_user, login_user, get_all_users  # Import service functions

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    return register_user()

@user_routes.route('/login', methods=['POST'])
def login():
    return login_user()

@user_routes.route('/forgot_password', methods=['POST'])
def forgot_password_route():
    return forgot_password()

@user_routes.route('/users', methods=['GET'])
def get_users():
    return get_all_users()

@user_routes.route('/get_username', methods=['POST'])
def get_username():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    response, status_code = get_username_by_id(user_id)
    return jsonify(response), status_code