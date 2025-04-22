from flask import Blueprint, request, jsonify, render_template
import requests
import os

gynecologist_bp = Blueprint('gynecologist', __name__)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@gynecologist_bp.route('/gynecologist')
def gynecologist():
    return render_template('gynecologist.html', api_key=GOOGLE_MAPS_API_KEY)

@gynecologist_bp.route('/gyne', methods=['GET', 'POST'])
def get_gynecologists():
    # Get parameters from either GET or POST
    if request.method == 'GET':
        lat = request.args.get('lat', '12.9716')
        lng = request.args.get('lng', '77.5946')
    else:
        data = request.get_json() or {}
        lat = data.get('lat', '12.9716')
        lng = data.get('lng', '77.5946')
    
    params = {
        "location": f"{lat},{lng}",
        "radius": 3000,
        "keyword": "gynecologist",
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=params
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "error": str(e),
            "params_used": params,
            "key_used": GOOGLE_MAPS_API_KEY[-6:] + "..."  # Show last chars for verification
        }), 500