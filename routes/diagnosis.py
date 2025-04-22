from flask import Blueprint, request, jsonify, session
from predict import predict_self_diagnosis

diagnosis_api = Blueprint("diagnosis_api", __name__)

@diagnosis_api.route("/api/predict/self_diagnosis", methods=["POST"])
def predict_self_diagnosis_api():
    form_data = request.form
    prediction = predict_self_diagnosis(form_data)
    print("Prediction output:", prediction)

    # Adjusting to actual keys in the prediction
    session["pcos_result"] = {
        "label": prediction["prediction"]
    }

    return jsonify({
    "prediction": prediction["prediction"]
})

