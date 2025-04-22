import os

folders = [
    "templates",
    "static",
    "models",
    "chatbot/modules"
]

files = [
    
    
    "templates/diet_form.html", "templates/diet_result.html",
    "templates/fitness_form.html", "templates/fitness_result.html",
    "templates/lifestyle_form.html", "templates/lifestyle_result.html",
    "chatbot/cognitive_chat.py", "chatbot/context_manager.py",
    "chatbot/model.py", "chatbot/nltk_utils.py",
    "chatbot/modules/diagnosis.py", "chatbot/modules/ultrasound.py",
    "chatbot/modules/education.py", "chatbot/modules/support.py",
    "chatbot/modules/nutrition.py", "chatbot/modules/fitness.py",
    "chatbot/modules/feedback.py", "chatbot/modules/geolocation.py"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(f"# {file}\n")
print("✅ Project structure created.")
