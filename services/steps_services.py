from flask import jsonify
from datetime import datetime, timedelta
from config import mongo  # Ensure this is correctly set up

# Reference to the steps collection in MongoDB
steps_collection = mongo.db.steps  

def timestamp():
    """Generate a UTC timestamp in ISO format."""
    return datetime.utcnow()

def log_steps(user_id, steps_count, steps_goal):
    try:
        steps_entry = {
            "user_id": str(user_id),  # Ensure user_id is a string
            "steps_count": steps_count,
            "steps_goal": steps_goal,
            "timestamp": timestamp()  # Store as ISODate
        }
        steps_collection.insert_one(steps_entry)
        return jsonify({"message": "Steps logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_steps(user_id, range_type="today"):
    try:
        now = datetime.utcnow()
        user_id = str(user_id)  # Ensure user_id matches stored format

        if range_type == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query_filter = {"timestamp": {"$gte": start_date}}

        elif range_type == "week":
            start_date = now - timedelta(days=7)
            query_filter = {"timestamp": {"$gte": start_date}}

        elif range_type == "month":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            query_filter = {"timestamp": {"$gte": start_date}}

        else:
            return jsonify({"error": "Invalid range type"}), 400

        records = list(steps_collection.find(
            {"user_id": user_id, **query_filter}, {"_id": 0}  # Exclude `_id`
        ))

        # Fetch steps_goal from the first record (if available)
        steps_goal = next((record["steps_goal"] for record in records if "steps_goal" in record), 10000)

        return jsonify({"steps": records, "steps_goal": steps_goal}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
