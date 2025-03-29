from flask import jsonify
from datetime import datetime,timedelta
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

def get_sleep(user_id,range_type = "today"):
    try:
        now = datetime.now()

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

        records = list(sleep_collection.find(
            {"user_id": user_id,**query_filter}, {"_id": 0}  # Exclude `_id`
        ))
        return jsonify({"sleep": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
