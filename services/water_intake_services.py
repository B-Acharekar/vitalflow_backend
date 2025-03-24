from flask import jsonify
from datetime import datetime
from config import mongo  # Ensure this is correctly set up

# Reference to the hydration collection in MongoDB
water_collection = mongo.db.hydration  

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_water_intake(user_id, water_intake_ml):
    """Logs user's water intake into MongoDB."""
    try:
        water_entry = {
            "user_id": user_id,
            "water_intake_ml": water_intake_ml,
            "timestamp": timestamp()  # Add timestamp
        }
        water_collection.insert_one(water_entry)
        return jsonify({"message": "Water intake logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_water_intake(user_id):
    """Fetches today's water intake records for a user."""
    try:
        today = datetime.today().strftime('%Y-%m-%d')

        # Query records where the timestamp starts with today's date (YYYY-MM-DD)
        records = list(water_collection.find(
            {"user_id": user_id, "timestamp": {"$regex": f"^{today}"}},  # ✅ Fix
            {"_id": 0}  # Hide _id field
        ))

        return jsonify({"water_intake": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

