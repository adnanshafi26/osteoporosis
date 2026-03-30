from flask import Blueprint, request, jsonify
from model.predict import predict_osteoporosis, predict_fracture_risk, predict_bone_diseases
from utils.report_generator import generate_report
from utils.pdf_report import generate_patient_report
from database.db import get_connection

prediction_bp = Blueprint("prediction", __name__)


# -----------------------------
# Prediction API
# -----------------------------
@prediction_bp.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        features = data.get("features")
        bone_type = data.get("bone", "Unknown")

        if not features:
            return jsonify({"error": "No features provided"}), 400

        # Convert to numeric values
        features = [float(x) for x in features]

        age = features[0]
        gender = features[1]
        bmi = features[2]
        bone_density = features[3]
        calcium = features[4]
        vitamin_d = features[5]

        # AI Predictions
        result = predict_osteoporosis(features)
        fracture_risk = predict_fracture_risk(features)
        diseases = predict_bone_diseases(features)

        # Save patient data
        conn = get_connection()

        conn.execute("""
            INSERT INTO patients
            (age, gender, bmi, bone_density, calcium, vitamin_d, bone_type, prediction, fracture_risk)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            age,
            gender,
            bmi,
            bone_density,
            calcium,
            vitamin_d,
            bone_type,
            result,
            fracture_risk
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "prediction": result,
            "fracture_risk": fracture_risk,
            "diseases": diseases
        })

    except Exception as e:

        print("PREDICTION ERROR:", e)

        return jsonify({"error": str(e)}), 500

# -----------------------------
# Medical Report API
# -----------------------------
@prediction_bp.route("/report", methods=["POST"])
def create_report():

    try:

        data = request.json

        features = data.get("features")

        if not features:
            return jsonify({"error": "No patient data received"}), 400

        result = predict_osteoporosis(features)

        patient_data = {
            "age": features[0],
            "gender": features[1],
            "bmi": features[2],
            "boneDensity": features[3],
            "calcium": features[4],
            "vitaminD": features[5]
        }

        generate_report(patient_data, result)

        return jsonify({
            "message": "Medical report generated successfully"
        })

    except Exception as e:

        print("REPORT ERROR:", e)

        return jsonify({"error": str(e)}), 500


# -----------------------------
# Multi-Bone Analysis API
# -----------------------------
@prediction_bp.route("/download_patient_report", methods=["POST"])
def download_patient_report_v2():

    try:

        # Get latest patient from DB
        conn = get_connection()

        patient = conn.execute("""
            SELECT age, gender, bmi, bone_density, calcium, vitamin_d,
                   bone_type, prediction, fracture_risk
            FROM patients
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

        conn.close()

        if not patient:
            return jsonify({"error": "No patient data found"}), 400

        # Prepare data for PDF
        data = {
            "age": patient["age"],
            "gender": patient["gender"],
            "bmi": patient["bmi"],
            "bone": patient["bone_type"],
            "prediction": patient["prediction"],
            "fracture_risk": patient["fracture_risk"],
            "calcium": patient["calcium"],
            "vitamin_d": patient["vitamin_d"]
        }

        pdf_path = generate_patient_report(data)

        return jsonify({
            "report": "/" + pdf_path
        })

    except Exception as e:

        print("PDF ERROR:", e)

        return jsonify({"error": str(e)}), 500
# -----------------------------
# Dashboard Statistics API
# -----------------------------
@prediction_bp.route("/stats", methods=["GET"])
def stats():

    try:

        conn = get_connection()

        total = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]

        high = conn.execute(
            "SELECT COUNT(*) FROM patients WHERE prediction='High Risk of Osteoporosis'"
        ).fetchone()[0]

        low = conn.execute(
            "SELECT COUNT(*) FROM patients WHERE prediction='Low Risk of Osteoporosis'"
        ).fetchone()[0]

        avg_density = conn.execute(
            "SELECT AVG(bone_density) FROM patients"
        ).fetchone()[0]

        bone_osteo = conn.execute("""
            SELECT bone_type, COUNT(*)
            FROM patients
            WHERE prediction='High Risk of Osteoporosis'
            GROUP BY bone_type
        """).fetchall()

        bone_fracture = conn.execute("""
            SELECT bone_type, COUNT(*)
            FROM patients
            WHERE fracture_risk LIKE '%High%'
            GROUP BY bone_type
        """).fetchall()

        conn.close()

        return jsonify({
            "total": total,
            "high": high,
            "low": low,
            "avg_density": round(avg_density or 0, 2),
            "bone_osteoporosis": bone_osteo,
            "bone_fracture": bone_fracture
        })

    except Exception as e:

        print("STATS ERROR:", e)

        return jsonify({"error": str(e)}), 500