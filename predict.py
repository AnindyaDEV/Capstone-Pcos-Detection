import numpy as np
from model_loader import (
    self_diagnosis_model,
    ultrasound_model,
    label_encoder,
    extract_vgg16_features,
)
from PIL import Image
import io
import cv2

# ----- Self Diagnosis Prediction -----
def predict_self_diagnosis(form_data):
    features = [
        float(form_data["Follicle_No_R"]),
        int(form_data["Skin_darkening_YN"]),
        int(form_data["Age_yrs"]),
        float(form_data["BMI"]),
        float(form_data["Weight_Kg"]),
        int(form_data["Hair_loss_YN"]),
        int(form_data["Marraige_Status_Yrs"]),
        float(form_data["Hip_inch"]),
        int(form_data["Weight_gain_YN"]),
        float(form_data["PRG_ng_mL"]),
        int(form_data["Pimples_YN"]),
        int(form_data["No_of_aborptions"]),
        float(form_data["AMH_ng_mL"]),
        float(form_data["Waist_inch"]),
        float(form_data["Follicle_No_L"]),
        int(form_data["Cycle_length_days"]),
        int(form_data["Hair_growth_YN"]),
        float(form_data["Avg_F_size_L_mm"]),
        int(form_data["Fast_food_YN"]),
        int(form_data["Cycle_R_I"]),
    ]

    input_data = np.array(features).reshape(1, -1)
    prediction = self_diagnosis_model.predict(input_data)[0]
    result = "PCOS Detected" if prediction == 1 else "No PCOS Detected"
    return {"prediction": result}


# ----- Ultrasound Image Prediction -----
def predict_ultrasound(file):
    try:
        # Read uploaded image
        image_bytes = file.read()
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            return {"error": "Invalid image format"}

        # Resize and normalize (224x224)
        image = cv2.resize(image, (224, 224))
        image = image / 255.0

        # Extract features using VGG16
        features = extract_vgg16_features(image).reshape(1, -1)

        # Predict with XGBoost
        prediction_prob = ultrasound_model.predict_proba(features)[0]
        predicted_class = np.argmax(prediction_prob)
        confidence = float(np.max(prediction_prob))

        result = "PCOS Detected" if predicted_class == 0 else "No PCOS Detected"

        return {
            "prediction": result,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        return {"error": str(e)}