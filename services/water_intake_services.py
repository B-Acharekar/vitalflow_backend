from flask import jsonify
from datetime import datetime, timedelta
from config import mongo

water_collection = mongo.db.hydration

def log_water_intake(user_id, water_intake_ml, note=None, log_time=None):
    """
    Logs user's water intake into MongoDB.
    :param user_id: str
    :param water_intake_ml: int
    :param note: str (optional) - Original note provided by user
    :param log_time: datetime (optional)
    """
    try:
        water_entry = {
            "user_id": user_id,
            "water_intake_ml": water_intake_ml,
            "timestamp": log_time or datetime.now(),
        }
        if note:
            water_entry["note"] = note  # Store original note for insight/debugging

        # Insert water entry into MongoDB
        water_collection.insert_one(water_entry)

        return jsonify({
            "message": "Water intake logged successfully",
            "logged_ml": water_intake_ml,
            "note": note,
            "timestamp": water_entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_water_intake(user_id, range_type="today"):
    """
    Fetches water intake records for user based on time range.
    :param user_id: str
    :param range_type: str ('today', 'week', 'month')
    """
    try:
        now = datetime.now()
        start_time = None
        end_time = now

        if range_type == "today":
            start_time = datetime(now.year, now.month, now.day)

        elif range_type == "week":
            start_time = now - timedelta(days=7)

        elif range_type == "month":
            start_time = datetime(now.year, now.month, 1)

        else:
            return jsonify({"error": "Invalid range type"}), 400

        query_filter = {
            "user_id": user_id,
            "timestamp": {"$gte": start_time, "$lte": end_time}
        }

        records = list(water_collection.find(query_filter, {"_id": 0}))
        for rec in records:
            rec["timestamp"] = rec["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify({"water_intake": records}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
