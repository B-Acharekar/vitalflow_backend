from flask import request, jsonify
from config import mongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def register_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data or "password" not in data or "security_question" not in data or "security_answer" not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    users_collection = mongo.db.users
    existing_user = users_collection.find_one({"email": data["email"]})

    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400

    # Hash the security answer
    hashed_answer = bcrypt.generate_password_hash(data["security_answer"]).decode('utf-8')
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    
    user_id = users_collection.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password,
        "security_question": data["security_question"],  # Store security question
        "security_answer": hashed_answer  # Store hashed answer
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

def forgot_password():
    data = request.get_json()

    if not data or "email" not in data or "security_answer" not in data or "new_password" not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    users_collection = mongo.db.users
    user = users_collection.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the security answer matches
    if not bcrypt.check_password_hash(user["security_answer"], data["security_answer"]):
        return jsonify({"error": "Incorrect security answer"}), 400

    # Hash the new password and update it in the database
    hashed_new_password = bcrypt.generate_password_hash(data["new_password"]).decode('utf-8')

    # Update the user's password
    users_collection.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_new_password}})

    return jsonify({"message": "Password updated successfully"}), 200


def get_username_by_id(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return {"name": user.get("name", "Unknown")}, 200
        else:
            return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    

def get_all_users():
    users_collection = mongo.db.users
    users = users_collection.find()

    users_list = [{
        "id": str(user["_id"]),
        "name": user.get("name", "Unknown"),
        "email": user.get("email", "No Email")
    } for user in users]

    return jsonify({"users": users_list}), 200

