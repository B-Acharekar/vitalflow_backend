import nltk
from flask import jsonify, request
from datetime import datetime, timedelta
from config import mongo  # Ensure this is correctly set up
from bson import ObjectId  # Import ObjectId for conversion
from analyze.stress_analyzer import analyze_stress #Import NLP for analysis

# Reference to the stress_logs collection in MongoDB
stress_collection = mongo.db.stress 

def timestamp():
    """Generate a UTC timestamp in ISO format."""
    return datetime.utcnow()

def add_stress_log(user_id, stress_level=None, note=""):
    """Add a new stress log entry to the database."""
    try:
        user_id = str(user_id)  # Ensure user_id is a string
        
        # ✅ Use refined stress analysis
        if not stress_level and note:
            stress_category, stress_score = analyze_stress(note)
            stress_level = round(stress_score)  # ✅ Convert to integer (0-100)
        else:
            stress_level = int(stress_level)

        # ✅ Validate stress level range
        if stress_level < 0 or stress_level > 100:
            return jsonify({"error": "Stress level must be between 0 and 100"}), 400

        stress_entry = {
            "user_id": user_id,
            "stress_level": stress_level,
            "note": note,
            "category": stress_category,  # ✅ Store category in DB
            "timestamp": timestamp()
        }

        inserted = stress_collection.insert_one(stress_entry)
        stress_entry["_id"] = str(inserted.inserted_id)  # Convert ObjectId to string

        return jsonify({"message": "Stress log added successfully", "data": stress_entry}), 201

    except ValueError:
        return jsonify({"error": "Invalid stress level. It must be an integer."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_stress_log(user_id, time_range="today"):
    """Fetch stress logs for today, week, or month"""
    try:
        now = datetime.utcnow()
        user_id = str(user_id)  # Ensure user_id matches stored format

        if time_range == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == "week":
            start_date = now - timedelta(days=7)
        elif time_range == "month":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return jsonify({"error": "Invalid time range"}), 400

        stress_logs = list(stress_collection.find(
            {"user_id": user_id, "timestamp": {"$gte": start_date}}
        ))

        # Convert ObjectId to string
        for log in stress_logs:
            log["_id"] = str(log["_id"])

        return jsonify({"stress_logs": stress_logs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

