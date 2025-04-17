import re

# Define water container sizes in ml
CONTAINER_ML = {
    "sip": 50,
    "glass": 250,
    "cup": 200,
    "bottle": 500,
    "small bottle": 330,
    "large bottle": 1000,
    "jug": 1500,
    "mug": 300
}

def extract_water_intake(text):
    text = text.lower()
    estimated_ml = 0
    found = False

    # Regular expression to match numbers and containers
    pattern = r"(\d+)?\s*(sip|glass|cup|bottle|small bottle|large bottle|jug|mug)"
    matches = re.findall(pattern, text)

    for match in matches:
        # Extract number and container
        count = int(match[0]) if match[0] else 1  # Default count is 1 if no number is specified
        container = match[1]

        # Add the corresponding water intake
        if container in CONTAINER_ML:
            estimated_ml += count * CONTAINER_ML[container]
            found = True

    # Fallback if "drank water" is mentioned but no container
    if "drank water" in text and not found:
        estimated_ml += 250  # Default one glass

    # Additional fallback handling for cases where we can infer hydration (e.g., "I drank a lot of water")
    if "a lot of water" in text:
        estimated_ml += 1000  # Assume a large bottle

    return estimated_ml
