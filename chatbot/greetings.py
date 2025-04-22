import random
from datetime import datetime

# Custom greeting messages with time awareness
GREETINGS = {
    "morning": [
        "Good morning! 🌞 Ready to boost your PCOS health today?",
        "Rise and shine! Let’s make this a PCOS-friendly day."
    ],
    "afternoon": [
        "Good afternoon! ☀️ Need nutrition or fitness tips?",
        "Hey there! How’s your PCOS journey going this afternoon?"
    ],
    "evening": [
        "Good evening! 🌙 Time to unwind—need stress management tips?",
        "Evening! Ready to plan tomorrow’s PCOS-friendly meals?"
    ],
    "night": [
        "Late night PCOS care? 🌜 I’m here!",
        "Working on your health even at night? That’s dedication!"
    ],
    "general": [
        "Hello! I’m your PCOS Companion. What’s on your mind?",
    ],
    "returning_user": [
        "Welcome back! Want to continue where we left off?",
    ]
}

def get_time_of_day() -> str:
    """Detects current time and returns 'morning', 'afternoon', etc."""
    hour = datetime.now().hour  # Get the current hour
    print(f"Current hour: {hour}")  # Debugging line to check the hour value
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"

def get_greeting(is_returning: bool = False) -> str:
    """Returns a time-aware greeting."""
    if is_returning:
        return random.choice(GREETINGS["returning_user"])
    
    time_key = get_time_of_day()  # Get the correct time of day
    print(f"Time key: {time_key}")  # Debugging line to check the selected time period
    return random.choice(GREETINGS.get(time_key, GREETINGS["general"]))
