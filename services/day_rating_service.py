from datetime import datetime, timedelta
from config import mongo  # Ensure this points to your MongoDB config
from flask import jsonify
from analyze.day_rating_analyzer import calculate_day_rating  # Assuming the analysis functions are moved to metrics_service

day_rating_collection = mongo.db.dayRating  # New collection

def timestamp():
    """Generate a UTC timestamp in ISO format."""
    return datetime.utcnow()

def add_day_rating(user_id, user_note=None):
    """Add a day rating log to the database."""
    try:
        # Perform the day rating calculation
        day_rating = calculate_day_rating(user_id, user_note)
        
        # Insert the rating into the database
        rating_entry = {
            "user_id": str(user_id),
            "day_rating": day_rating,
            "timestamp": timestamp()
        }

        inserted = day_rating_collection.insert_one(rating_entry)
        rating_entry["_id"] = str(inserted.inserted_id)

        return jsonify({"message": "Day rating added successfully", "data": rating_entry}), 201

    except ValueError:
        return jsonify({"error": "Invalid data received for day rating."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_day_rating(user_id, time_range="today"):
    """Calculate day rating for today, week, or month"""
    try:
        now = datetime.utcnow()
        user_id = str(user_id)  # Ensure string format

        # Determine the date range based on the time range
        if time_range == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == "week":
            start_date = now - timedelta(days=7)
        elif time_range == "month":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return jsonify({"error": "Invalid time range"}), 400

        # Aggregate to compute the average day rating in MongoDB
        pipeline = [
            {"$match": {"user_id": user_id, "timestamp": {"$gte": start_date}}}, 
            {"$group": {"_id": None, "avg_rating": {"$avg": "$day_rating"}}}
        ]

        result = list(day_rating_collection.aggregate(pipeline))
        avg_rating = result[0]["avg_rating"] if result else 5.0  # Default if no data

        return jsonify({"day_rating": round(avg_rating, 2)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
