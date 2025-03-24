from flask import jsonify
from datetime import datetime
from config import mongo  # Ensure this is correctly set up

# Reference to the steps collection in MongoDB
steps_collection = mongo.db.steps  

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_steps(user_id,steps_count,steps_goal):
    try:
        steps_entry = {
            "user_id": user_id,
            "steps_count": steps_count,
            "steps_goal": steps_goal,
            "timestamp": timestamp()  # Add timestamp
        }
        steps_collection.insert_one(steps_entry)
        return jsonify({"message": "Steps logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_steps(user_id):
    try:
        records = list(steps_collection.find(
            {"user_id": user_id}, {"_id": 0}  # Exclude `_id`
        ))
        return jsonify({"steps": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
