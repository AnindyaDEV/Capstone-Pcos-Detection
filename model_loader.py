# model_loader.py

import pickle
from joblib import load
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten
from tensorflow.keras.models import Model

# VGG16 model setup
base_model = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False
x = Flatten()(base_model.output)
feature_extractor = Model(inputs=base_model.input, outputs=x)

def extract_vgg16_features(image):
    image = np.expand_dims(image, axis=0)
    features = feature_extractor.predict(image)
    return features

def load_self_diagnosis_model(model_path="models/pcos.pkl"):
    try:
        model = load(model_path)
        print("✅ Self-diagnosis model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading self-diagnosis model: {e}")
        return None

def load_ultrasound_model(model_path="models/ultrasound.pkl"):
    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        print("✅ Ultrasound XGBoost model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading ultrasound model: {e}")
        return None

def load_label_encoder(encoder_path="models/pcos_label_encoder.pkl"):
    try:
        with open(encoder_path, "rb") as file:
            encoder = pickle.load(file)
        print("✅ Label encoder loaded successfully!")
        return encoder
    except Exception as e:
        print(f"❌ Error loading label encoder: {e}")
        return None

# Load models once globally
self_diagnosis_model = load_self_diagnosis_model()
ultrasound_model = load_ultrasound_model()
label_encoder = load_label_encoder()
