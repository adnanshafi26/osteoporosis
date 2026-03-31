import joblib
import numpy as np
from config import MODEL_PATH
from utils.feature_engineering import load_scaler

# Load model
model = joblib.load(MODEL_PATH)

# Load scaler
scaler = load_scaler("model/scaler.pkl")


def get_prediction(features):
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)
    return int(model.predict(features_scaled)[0])


# -----------------------------------------
# Existing Osteoporosis Prediction
# -----------------------------------------
def predict_osteoporosis(features):
    pred = get_prediction(features)
    labels = {1: "High Risk of Osteoporosis", 0: "Low Risk of Osteoporosis"}
    return labels.get(pred)


# -----------------------------------------
# New Feature: Early Fracture Risk Prediction
# -----------------------------------------
def predict_fracture_risk(features):
    pred = get_prediction(features)
    labels = {1: "High Future Fracture Risk", 0: "Low Future Fracture Risk"}
    return labels.get(pred)


# -----------------------------------------
# Multi-Bone Analysis System
# -----------------------------------------
def multi_bone_analysis(bone_predictions):
    counts = list(bone_predictions.values()).count("High Risk of Osteoporosis")
    scores = {
        0: "Healthy Bone Condition",
        1: "Mild Bone Weakness",
        2: "Moderate Bone Weakness"
    }
    return scores.get(counts, "Severe Overall Bone Weakness")


def calculate_bone_health_score(features):
    pred = get_prediction(features)
    scores = {1: 40, 0: 90}
    return scores.get(pred)


# --------------------------------
# Multi-Disease Bone Analysis
# --------------------------------
def predict_bone_diseases(features):
    pred = get_prediction(features)
    diseases = {
        1: ["Osteoporosis", "High Bone Loss Risk"],
        0: ["No major bone disease detected"]
    }
    return diseases.get(pred)