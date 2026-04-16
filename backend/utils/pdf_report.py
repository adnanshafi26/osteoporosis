from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def bone_precautions(bone):

    bone = str(bone).lower().strip()

    if "hip" in bone:
        bone_key = "hip"
    elif "spine" in bone:
        bone_key = "spine"
    elif "wrist" in bone:
        bone_key = "wrist"
    elif "knee" in bone:
        bone_key = "knee"
    else:
        bone_key = "general"

    precautions = {

        "hip":[
        "Perform regular walking and balance exercises.",
        "Avoid slippery floors to reduce fall risk.",
        "Maintain adequate calcium and Vitamin D intake.",
        "Use handrails while climbing stairs."
        ],

        "spine":[
        "Avoid heavy weight lifting.",
        "Practice posture correction exercises.",
        "Perform stretching or yoga regularly.",
        "Use ergonomic chairs with back support."
        ],

        "wrist":[
        "Avoid sudden impact activities.",
        "Use wrist support during physical activity.",
        "Strengthen forearm muscles gradually.",
        "Maintain strong grip while lifting objects."
        ],

        "knee":[
        "Avoid excessive running or jumping.",
        "Perform knee strengthening exercises.",
        "Maintain healthy body weight.",
        "Use knee support during sports activities."
        ],

        "general":[
        "Maintain a balanced calcium-rich diet.",
        "Ensure adequate Vitamin D intake.",
        "Perform regular physical activity.",
        "Consult a doctor for bone density screening."
        ]
    }

    return precautions[bone_key]


# -----------------------------
# Patient Clinical Report
# -----------------------------
def generate_patient_report(data):

    os.makedirs("uploads", exist_ok=True)

    filepath = "uploads/patient_bone_health_report.pdf"

    c = canvas.Canvas(filepath, pagesize=letter)

    width, height = letter
    y = height - 80

    c.setFont("Helvetica-Bold",22)
    c.drawString(150,y,"Patient Bone Health Report")

    y -= 40

    c.setFont("Helvetica",12)
    c.drawString(50,y,"Report Generated On: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

    y -= 40

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Patient Information")

    y -= 25
    c.setFont("Helvetica",12)

    c.drawString(60,y,f"Age: {data['age']}")
    y -= 20
    gender_text = "Male" if str(data['gender']) == "1" else "Female"
    c.drawString(60,y,f"Gender: {gender_text}")
    y -= 20
    c.drawString(60,y,f"BMI: {data['bmi']}")

    y -= 30

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Bone Analysis")

    y -= 25
    c.setFont("Helvetica",12)

    c.drawString(60,y,f"Bone Type: {data['bone']}")
    y -= 20
    c.drawString(60,y,f"Osteoporosis Risk: {data['prediction']}")
    y -= 20
    c.drawString(60,y,f"Future Fracture Risk: {data['fracture_risk']}")

    y -= 30

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Recommended Nutrition")

    y -= 25
    c.setFont("Helvetica",12)

    c.drawString(60,y,f"Daily Calcium Intake: {data['calcium']} mg")
    y -= 20
    c.drawString(60,y,f"Vitamin D Level: {data['vitamin_d']} IU")

    y -= 30

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Precautions & Safety Guidelines")

    y -= 25
    c.setFont("Helvetica",12)

    precautions = bone_precautions(data['bone'])

    for p in precautions:

        if y < 100:
            c.showPage()
            c.setFont("Helvetica",12)
            y = 750

        c.drawString(60,y,"- " + p)
        y -= 18

    y -= 30

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Medical Advice")

    y -= 25
    c.setFont("Helvetica",12)

    c.drawString(60,y,"• Regular bone density screening is recommended.")
    y -= 18
    c.drawString(60,y,"• Maintain balanced diet rich in calcium.")
    y -= 18
    c.drawString(60,y,"• Engage in moderate physical activity.")

    c.setFont("Helvetica-Oblique",10)
    c.drawString(50,40,"AI-Based Osteoporosis Detection System")

    c.save()

    return filepath


# -----------------------------
# X-ray Report
# -----------------------------
def generate_xray_report(data):

    os.makedirs("uploads", exist_ok=True)

    filepath = "uploads/xray_analysis_report.pdf"

    c = canvas.Canvas(filepath, pagesize=letter)

    width, height = letter
    y = height - 80

    c.setFont("Helvetica-Bold",22)
    c.drawString(150,y,"AI X-ray Bone Analysis Report")

    y -= 40

    c.setFont("Helvetica",12)
    c.drawString(50,y,"Report Generated On: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

    y -= 40

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"X-ray Analysis Result")

    y -= 25
    c.setFont("Helvetica",12)

    c.drawString(60,y,f"Anatomical Bone Region: {data['bone']}")
    y -= 20
    c.drawString(60,y,f"Predicted BMI: {data['bmi']}")
    y -= 20
    c.drawString(60,y,f"Predicted Bone Density (BMD): {data['bone_density']}")
    y -= 20
    c.drawString(60,y,f"Bone Health Status: {data['osteoporosis']}")
    y -= 20
    c.drawString(60,y,f"Future Fracture Risk: {data['future_risk']}")
    y -= 20
    c.drawString(60,y,f"Fracture Detection: {data['fracture_status']} ({data['fracture_confidence']})")
    y -= 20
    c.drawString(60,y,f"Confidence Level: {data['confidence']}")

    y -= 30

    c.setFont("Helvetica-Bold",14)
    c.drawString(50,y,"Recommended Precautions")

    y -= 25
    c.setFont("Helvetica",12)

    precautions = bone_precautions(data['bone'])

    for p in precautions:

        if y < 100:
            c.showPage()
            c.setFont("Helvetica",12)
            y = 750

        c.drawString(60,y,"- " + p)
        y -= 18

    c.setFont("Helvetica-Oblique",10)
    c.drawString(50,40,"AI Radiographic Analysis System")

    c.save()

    return filepath