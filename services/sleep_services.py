from flask import jsonify
from datetime import datetime
from config import mongo  # Ensure this is correctly set up

# Reference to the sleep collection in MongoDB
sleep_collection = mongo.db.sleep  

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_sleep(user_id,sleep_duration_min,sleep_quality,sleep_goal):
    try:
        sleep_entry = {
            "user_id": user_id,
            "sleep_duration_min": sleep_duration_min,
            "sleep_quality": sleep_quality,
            "sleep_goal": sleep_goal,
            "timestamp": timestamp()  # Add timestamp
        }
        sleep_collection.insert_one(sleep_entry)
        return jsonify({"message": "sleep logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sleep(user_id):
    try:
        records = list(sleep_collection.find(
            {"user_id": user_id}, {"_id": 0}  # Exclude `_id`
        ))
        return jsonify({"sleep": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
