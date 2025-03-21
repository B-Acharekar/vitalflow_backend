from flask import jsonify
from datetime import date
from config import mongo  # Ensure this is correctly set up

# Reference to the hydration collection in MongoDB
health_log_collection = mongo.db.health_logs  

def today():
    return date.today().strftime("%Y-%m-%d")

def health_log(user_id,weight,height):
    try:
        health_log_entry = {
            "user_id": user_id,
            "weight": weight,
            "height": height,
            "date": today()
        }
        health_log_collection.insert_one(health_log_entry)
        return jsonify({"message": "Health logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_health_log(user_id):
    try:
        records = list(health_log_collection.find(
            {"user_id": user_id}, {"_id": 0}  # Exclude `_id`
        ))
        return jsonify({"health_log": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
