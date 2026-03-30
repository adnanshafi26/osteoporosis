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

    file.save(file_path)

    result = analyze_xray(file_path)

    pdf_path = generate_xray_report(result)

    return jsonify({
        "bone": result["bone"],
        "fracture": result["fracture"],
        "osteoporosis": result["osteoporosis"],
        "future_risk": result["future_risk"],
        "image": "/uploads/marked_xray.jpg",
        "report": "/" + pdf_path
    })