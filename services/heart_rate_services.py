from flask import jsonify
from datetime import datetime
from config import mongo  

heart_rate_collection = mongo.db.heart_rate  

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def heart_rate_log(user_id,heart_rate_bpm):
    try:
        heart_rate_entry = {
            "user_id": user_id,
            "heart_rate_bpm": heart_rate_bpm,
            "date": today()
        }
        heart_rate_collection.insert_one(heart_rate_entry)
        return jsonify({"message": "Heart Rate logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_heart_rate_log(user_id):
    try:
        records = list(heart_rate_collection.find(
            {"user_id": user_id}, {"_id": 0} 
        ))
        return jsonify({"heart_rate_log": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
