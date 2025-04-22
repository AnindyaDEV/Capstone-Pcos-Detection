import json
import os

def load_fitness_data():
    json_path = os.path.join("data", "fitness_data.json")
    with open(json_path, "r") as f:
        return json.load(f)

def get_routines_for_constraint(constraint):
    data = load_fitness_data()
    return data.get(constraint.lower(), [])
