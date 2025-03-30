from datetime import datetime, timedelta
from config import mongo  # Ensure this points to your MongoDB config
from flask import jsonify

day_rating_collection = mongo.db.dayRating  # New collection

def timestamp():
    """Generate a UTC timestamp in ISO format."""
    return datetime.utcnow()

def add_day_rating(user_id, day_rating):
    """Add a day rating log to the database."""
    try:
        user_id = str(user_id)  # Ensure consistent format
        day_rating = float(day_rating)  # Ensure it's a float

        if day_rating < 0 or day_rating > 10:
            return jsonify({"error": "Day rating must be between 0 and 10"}), 400

        rating_entry = {
            "user_id": user_id,
            "day_rating": day_rating,
            "timestamp": timestamp()
        }

        inserted = day_rating_collection.insert_one(rating_entry)
        rating_entry["_id"] = str(inserted.inserted_id)

        return jsonify({"message": "Day rating added successfully", "data": rating_entry}), 201
    except ValueError:
        return jsonify({"error": "Invalid day rating. It must be a number."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_day_rating(user_id, time_range="today"):
    """Calculate day rating for today, week, or month"""
    try:
        now = datetime.utcnow()
        user_id = str(user_id)  # Ensure string format

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
