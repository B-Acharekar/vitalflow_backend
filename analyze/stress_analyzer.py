import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

# Download required resources
nltk.download('vader_lexicon')
nltk.download('punkt')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Define Negation Words
NEGATION_WORDS = {"not", "never", "no", "n't", "hardly", "barely", "scarcely"}

def adjust_for_negation(note, stress_score):
    """Reduces stress score if negations are present near stress words."""
    words = word_tokenize(note.lower())

    # Check if a negation appears before a stress-related word
    for i, word in enumerate(words):
        if word in NEGATION_WORDS and i < len(words) - 1:
            return max(stress_score - 20, 0)  # Reduce by 20%, min 0 stress
    
    return stress_score  # No change if no negation found

def analyze_stress(note):
    """Analyze stress level based on sentiment score with custom scaling."""
    try:
        sentiment_score = sia.polarity_scores(note)["compound"]

        # ✅ Improved stress mapping
        if sentiment_score >= 0.2:
            stress_level = 0 + (20 * (1 - sentiment_score))  # Low Stress
            category = "Low Stress"
        elif 0.0 <= sentiment_score < 0.2:
            stress_level = 20 + (20 * (0.2 - sentiment_score) / 0.2)  # Mild Stress
            category = "Mild Stress"
        elif -0.2 <= sentiment_score < 0.0:
            stress_level = 40 + (20 * abs(sentiment_score) / 0.2)  # Moderate Stress
            category = "Moderate Stress"
        elif -0.5 <= sentiment_score < -0.2:
            stress_level = 60 + (20 * abs(sentiment_score + 0.2) / 0.3)  # High Stress
            category = "High Stress"
        else:
            stress_level = 80 + (20 * abs(sentiment_score + 0.5) / 0.5)  # Severe Stress
            category = "Severe Stress"

        # ✅ Adjust for negation
        adjusted_stress = adjust_for_negation(note, round(stress_level))

        return category, adjusted_stress

    except Exception as e:
        print(f"Error in analyze_stress: {e}")
        return "Unknown", 0
