from flask import jsonify
from datetime import datetime, timedelta
from config import mongo  

# Reference to the heart_rate collection in MongoDB
heart_rate_collection = mongo.db.heart_rate  

def timestamp():
    """Generate a timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use timestamps

def heart_rate_log(user_id, heart_rate_bpm):
    try:
        heart_rate_entry = {
            "user_id": str(user_id),  # Ensure consistent user_id type
            "heart_rate_bpm": heart_rate_bpm,
            "date": datetime.now()  # Store as Python datetime (not string)
        }
        heart_rate_collection.insert_one(heart_rate_entry)
        return jsonify({"message": "Heart Rate logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_heart_rate(user_id, range_type='today'):
    try:
        now = datetime.now()  # Use local time (no UTC)
        user_id = str(user_id)  # Ensure user_id is a string

        if range_type == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        elif range_type == "week":
            start_date = now - timedelta(days=7)
        
        elif range_type == "month":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        else:
            return jsonify({"error": "Invalid range type"}), 400

        query_filter = {"date": {"$gte": start_date}}

        records = list(heart_rate_collection.find(
            {"user_id": user_id, **query_filter}, {"_id": 0}  # Exclude `_id`
        ))

        return jsonify({"heart_rate_log": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
