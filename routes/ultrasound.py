from flask import Blueprint, request, jsonify
from predict import predict_ultrasound

ultrasound_api = Blueprint("ultrasound_api", __name__)

@ultrasound_api.route("/api/predict/ultrasound", methods=["POST"])
def predict_ultrasound_api():
    file = request.files["ultrasound_image"]
    prediction = predict_ultrasound(file)
    return jsonify(prediction)
