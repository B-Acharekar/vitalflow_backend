from flask import Response
import json
from datetime import datetime
from textblob import TextBlob  # For sentiment analysis
import logging

# Importing your own services
from services.heart_rate_services import get_heart_rate
from services.sleep_services import get_sleep
from services.water_intake_services import get_water_intake
from services.steps_services import get_steps
from services.stress_log_services import get_stress_log

# Health Goals
GOALS = {
    "steps": 10000,
    "heart_rate": (60, 80),  # Resting HR range
    "water_intake": 2000,    # ml
    "sleep": 8,              # hours
    "stress": 20             # lower = better
}

def calculate_score_from_metric(value, goal, lower_is_better=False):
    """Normalize each health metric to a 0-100 score."""
    if lower_is_better:
        return max(0, 100 - value)
    return min(100, (value / goal) * 100)

def calculate_metrics_score(steps, heart_rate, water, sleep, stress):
    """Combine metric scores using weighted average."""
    steps_score = calculate_score_from_metric(steps, GOALS["steps"])
    heart_rate_score = calculate_score_from_metric(heart_rate, GOALS["heart_rate"][1])  # Use max threshold
    water_score = calculate_score_from_metric(water, GOALS["water_intake"])
    sleep_score = calculate_score_from_metric(sleep, GOALS["sleep"])
    stress_score = calculate_score_from_metric(stress, GOALS["stress"], lower_is_better=True)

    total_score = (
        steps_score * 0.25 +
        heart_rate_score * 0.2 +
        water_score * 0.2 +
        sleep_score * 0.2 +
        stress_score * 0.15
    )
    return total_score

def analyze_sentiment(note):
    """Use TextBlob to score sentiment in user's note."""
    if not note:
        return 0  # Neutral
    blob = TextBlob(note)
    return blob.sentiment.polarity  # -1 to 1

def extract_data(response_tuple):
    """Helper to extract JSON from Flask Response."""
    response, status = response_tuple
    if isinstance(response, Response):
        return json.loads(response.get_data(as_text=True))
    return {}

def summarize_stress_logs(logs):
    """Calculate average stress level if logs exist."""
    levels = [log.get("stress_level", 0) for log in logs.get("stress_logs", [])]
    return sum(levels) / len(levels) if levels else 0

def average_heart_rate(logs):
    hr_list = [entry.get("bpm", 0) for entry in logs.get("heart_rate_log", [])]
    return sum(hr_list) / len(hr_list) if hr_list else 0

def total_water(logs):
    return sum(entry.get("water_intake_ml", 0) for entry in logs.get("water_intake", []))

def hours_slept(logs):
    sleep_durations = [entry.get("sleep_duration_min", 0) / 60 for entry in logs.get("sleep", [])]  # Convert to hours
    return sum(sleep_durations)

def steps_count(logs):
    steps_data = logs.get("steps", [])
    return sum(entry.get("steps_count", 0) for entry in steps_data)

# Aggregating health data
def fetch_all_health(user_id, date_range):
    """Aggregate all health data into usable values."""
    steps_raw = extract_data(get_steps(user_id, date_range))
    heart_raw = extract_data(get_heart_rate(user_id, date_range))
    water_raw = extract_data(get_water_intake(user_id, date_range))
    sleep_raw = extract_data(get_sleep(user_id, date_range))
    stress_raw = extract_data(get_stress_log(user_id, date_range))

    logging.debug(f"Raw Data: {{'steps_raw': {steps_raw}, 'heart_raw': {heart_raw}, 'water_raw': {water_raw}, 'sleep_raw': {sleep_raw}, 'stress_raw': {stress_raw}}}")
    
    return {
        "steps": steps_count(steps_raw),
        "heart_rate": average_heart_rate(heart_raw),
        "water": total_water(water_raw),
        "sleep": hours_slept(sleep_raw),
        "stress": summarize_stress_logs(stress_raw),
    }

def calculate_day_rating(user_id, user_note=None):
    """
    Calculates a final day score using:
    - Aggregated metric data (steps, HR, sleep, water, stress)
    - Sentiment analysis on journal/note (optional)
    """
    today = datetime.today().strftime('%Y-%m-%d')

    data = fetch_all_health(user_id, "today")
    logging.debug(f"[Day Rating] Aggregated Data: {data}")

    metrics_score = calculate_metrics_score(
        data["steps"],
        data["heart_rate"],
        data["water"],
        data["sleep"],
        data["stress"]
    )

    sentiment_score = analyze_sentiment(user_note)

    # Adjust the score slightly based on user sentiment
    sentiment_adjustment = 0
    if sentiment_score > 0.2:
        sentiment_adjustment = 5 * sentiment_score  # Scale the positive impact
    elif sentiment_score < -0.2:
        sentiment_adjustment = 5 * sentiment_score  # Scale the negative impact

    metrics_score += sentiment_adjustment

    final_rating = max(0, min(metrics_score, 100))
    return round(final_rating, 2)
