import joblib
import numpy as np
from config import MODEL_PATH
from utils.feature_engineering import load_scaler

# Load model
model = joblib.load(MODEL_PATH)

# Load scaler
scaler = load_scaler("model/scaler.pkl")


# -----------------------------------------
# Existing Osteoporosis Prediction (UNCHANGED)
# -----------------------------------------
def predict_osteoporosis(features):

    features = np.array(features).reshape(1, -1)

    # Scale features before prediction
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)

    if prediction[0] == 1:
        return "High Risk of Osteoporosis"
    else:
        return "Low Risk of Osteoporosis"


# -----------------------------------------
# New Feature: Early Fracture Risk Prediction
# -----------------------------------------
def predict_fracture_risk(features):

    age = float(features[0])
    bmi = float(features[2])
    bone_density = float(features[3])
    calcium = float(features[4])
    vitamin_d = float(features[5])

    score = 0

    # Age factor
    if age > 65:
        score += 2
    elif age > 50:
        score += 1

    # Bone density factor
    if bone_density < 0.60:
        score += 2
    elif bone_density < 0.75:
        score += 1

    # BMI factor
    if bmi < 18.5:
        score += 1

    # Calcium factor
    if calcium < 800:
        score += 1

    # Vitamin D factor
    if vitamin_d < 20:
        score += 1

    if score >= 4:
        return "High Future Fracture Risk"
    elif score >= 2:
        return "Moderate Future Fracture Risk"
    else:
        return "Low Future Fracture Risk"
    
# -----------------------------------------
# Multi-Bone Analysis System
# -----------------------------------------

def multi_bone_analysis(bone_predictions):

    """
    bone_predictions example:
    {
        "hip": "High Risk of Osteoporosis",
        "spine": "Low Risk of Osteoporosis",
        "wrist": "High Risk of Osteoporosis",
        "knee": "Low Risk of Osteoporosis"
    }
    """

    risk_score = 0

    for bone in bone_predictions.values():
        if "High" in bone:
            risk_score += 1

    if risk_score >= 3:
        return "Severe Overall Bone Weakness"
    elif risk_score >= 2:
        return "Moderate Bone Weakness"
    elif risk_score == 1:
        return "Mild Bone Weakness"
    else:
        return "Healthy Bone Condition"

def calculate_bone_health_score(features):

    age = features[0]
    bmi = features[2]
    bone_density = features[3]
    calcium = features[4]
    vitamin_d = features[5]

    score = 100

    # Age factor
    if age > 65:
        score -= 20
    elif age > 50:
        score -= 10

    # BMI factor
    if bmi < 18.5:
        score -= 15
    elif bmi > 30:
        score -= 10

    # Bone density factor
    if bone_density < 0.6:
        score -= 30
    elif bone_density < 0.75:
        score -= 15

    # Calcium intake
    if calcium < 800:
        score -= 10

    # Vitamin D
    if vitamin_d < 600:
        score -= 10

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return score


# --------------------------------
# Multi-Disease Bone Analysis
# --------------------------------
def predict_bone_diseases(features):

    age = features[0]
    bmi = features[2]
    bone_density = features[3]
    calcium = features[4]
    vitamin_d = features[5]

    diseases = []

    # Osteoporosis
    if bone_density < 0.60:
        diseases.append("Osteoporosis")

    # Osteopenia (mild bone loss)
    elif bone_density >= 0.60 and bone_density < 0.75:
        diseases.append("Osteopenia")

    # Arthritis related bone loss
    if age > 50 and bmi > 27:
        diseases.append("Possible Arthritis Related Bone Loss")

    # Bone tumor suspicion
    if bone_density > 1.5:
        diseases.append("Possible Bone Tumor Signs")

    if not diseases:
        diseases.append("No major bone disease detected")

    return diseases