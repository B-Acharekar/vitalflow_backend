from flask import jsonify
from datetime import datetime, timedelta
from config import mongo  # Ensure this is correctly set up

# Reference to the hydration collection in MongoDB
water_collection = mongo.db.hydration  

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use timestamps

def log_water_intake(user_id, water_intake_ml):
    """Logs user's water intake into MongoDB."""
    try:
        water_entry = {
            "user_id": user_id,
            "water_intake_ml": water_intake_ml,
            "timestamp": timestamp()  # Store timestamp as string
        }
        water_collection.insert_one(water_entry)
        return jsonify({"message": "Water intake logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_water_intake(user_id, range_type="today"):
    """Fetches water intake records based on range (today, week, month)."""
    try:
        now = datetime.now()  # Get current time

        if range_type == "today":
            start_date = now.strftime('%Y-%m-%d')
            query_filter = {"timestamp": {"$regex": f"^{start_date}"}}  # Match today's date

        elif range_type == "week":
            start_date = (now - timedelta(days=7)).strftime('%Y-%m-%d')  # 7 days ago
            end_date = now.strftime('%Y-%m-%d')  # Today
            query_filter = {
                "timestamp": {"$gte": start_date, "$lte": end_date}
            }  # Get records between start and end dates

        elif range_type == "month":
            start_date = now.replace(day=1).strftime('%Y-%m-%d')  # First day of the month
            end_date = now.strftime('%Y-%m-%d')  # Today
            query_filter = {
                "timestamp": {"$gte": start_date, "$lte": end_date}
            }  # Get records between start and end dates

        else:
            return jsonify({"error": "Invalid range type"}), 400

        # Query MongoDB with the selected time range
        records = list(water_collection.find(
            {"user_id": user_id, **query_filter},
            {"_id": 0}  # Hide _id field
        ))

        return jsonify({"water_intake": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
