import cv2
import os


def detect_bone_type(image_path):

    filename = os.path.basename(image_path).lower()

    if "spine" in filename:
        return "Spine"

    if "hip" in filename:
        return "Hip Bone"

    if "wrist" in filename:
        return "Wrist Bone"

    if "knee" in filename:
        return "Knee Bone"

    return "Unknown Bone"


def analyze_xray(image_path):

    img = cv2.imread(image_path)

    if img is None:
        raise Exception("Image not loaded")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fracture_detected = False

    for cnt in contours:

        x, y, w, h = cv2.boundingRect(cnt)

        if w > 40 and h < 60:

            fracture_detected = True

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Ensure uploads folder exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    save_path = "uploads/marked_xray.jpg"

    saved = cv2.imwrite(save_path, img)
    print("DEBUG: Image saved =", saved)
    print("DEBUG: Saved path =", save_path)

    bone = detect_bone_type(image_path)

    if fracture_detected:
        fracture = "Possible Minor Fracture"
    else:
        fracture = "No Fracture Detected"

    return {
        "bone": bone,
        "fracture": fracture,
        "osteoporosis": "Early Osteoporosis Signs",
        "future_risk": "Moderate Future Risk",
        "marked_image": save_path
    }