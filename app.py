from flask import Flask, jsonify
from routes import init_routes
from dotenv import load_dotenv
import os
from flask import send_from_directory

app = Flask(__name__)
load_dotenv()
app.secret_key = "SECRET"
init_routes(app)

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.route('/get-map-token')
def get_map_token():
    # Add any security checks here (rate limiting, authentication, etc.)
    return jsonify({'key': GOOGLE_MAPS_API_KEY})

@app.route('/data/fitness_data.json')
def serve_fitness_data():
    return send_from_directory('data', 'fitness_data.json')

# In your app.py, add this temporary route to debug:
@app.route('/debug-key')
def debug_key():
    return jsonify({
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY"),
        "loaded_key": GOOGLE_MAPS_API_KEY
    })

if __name__ == "__main__":
    app.run(debug=True)