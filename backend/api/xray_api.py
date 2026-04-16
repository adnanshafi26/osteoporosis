from flask import Blueprint, request, jsonify
import os
from image_analysis.xray_predict import analyze_xray
from utils.pdf_report import generate_xray_report

xray_bp = Blueprint("xray", __name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@xray_bp.route("/analyze_xray", methods=["POST"])
def analyze():

    if "xray" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["xray"]

    if file.filename == "":
        return jsonify({"error": "Invalid file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    bone_type = request.form.get("bone_type")

    file.save(file_path)

    result = analyze_xray(file_path, manual_bone=bone_type)

    pdf_path = generate_xray_report(result)

    return jsonify({
        "bone": result["bone"],
        "bmi": result["bmi"],
        "bone_density": result["bone_density"],
        "osteoporosis": result["osteoporosis"],
        "future_risk": result["future_risk"],
        "fracture_status": result["fracture_status"],
        "fracture_confidence": result["fracture_confidence"],
        "confidence": result["confidence"],
        "image": "/uploads/processed_xray.jpg",
        "report": "/" + pdf_path
    })