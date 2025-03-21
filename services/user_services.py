from flask import request, jsonify
from config import mongo
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def register_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    users_collection = mongo.db.users
    existing_user = users_collection.find_one({"email": data["email"]})

    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    user_id = users_collection.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password
    }).inserted_id

    return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201


def login_user():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    users_collection = mongo.db.users
    user = users_collection.find_one({"email": data["email"]})

    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid email or password"}), 404

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200


def get_all_users():
    users_collection = mongo.db.users
    users = users_collection.find()

    users_list = [{
        "id": str(user["_id"]),
        "name": user.get("name", "Unknown"),
        "email": user.get("email", "No Email")
    } for user in users]

    return jsonify({"users": users_list}), 200
