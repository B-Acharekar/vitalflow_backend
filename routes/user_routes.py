from flask import Blueprint, request, jsonify
from services.user_services import register_user, login_user, get_all_users  # Import service functions

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    return register_user()

@user_routes.route('/login', methods=['POST'])
def login():
    return login_user()

@user_routes.route('/users', methods=['GET'])
def get_users():
    return get_all_users()
