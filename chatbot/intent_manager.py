import json
import random
from pathlib import Path

class IntentManager:
    def __init__(self, intents_file: str = "data/intents.json"):
        self.intents = self._load_intents(intents_file)

    def _load_intents(self, file_path: str) -> dict:
        """Loads intents from JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Intent file not found at {file_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON in {file_path}")

    def classify_intent(self, user_input: str) -> str:
        """Simple keyword-based intent classifier (upgrade to NLP later)."""
        user_input = user_input.lower()
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                if pattern.lower() in user_input:
                    return intent["tag"]
        return "unknown"

    def get_response(self, intent_tag: str) -> str:
        """Returns a random response for the matched intent."""
        for intent in self.intents["intents"]:
            if intent["tag"] == intent_tag:
                return random.choice(intent["responses"])
        return "I'm not sure how to help with that. Could you rephrase?"

# Example test
if __name__ == "__main__":
    intent_manager = IntentManager()
    test_questions = [
        "What is PCOS?",
        "Tell me about PCOS diets",
        "Random question"
    ]
    for question in test_questions:
        intent = intent_manager.classify_intent(question)
        response = intent_manager.get_response(intent)
        print(f"Q: {question}\nA: {response}\n")