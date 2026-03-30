import sys
import os
import difflib


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, send_from_directory, request, redirect, session, jsonify
from flask_cors import CORS
from datetime import timedelta
import datetime

from api.prediction_api import prediction_bp
from api.xray_api import xray_bp
from database.db import get_connection, init_db
from openai import OpenAI

app = Flask(__name__)

# Initialize database
init_db()

app.secret_key = "osteoporosis_secret_key"

# Remember login for 7 days
app.permanent_session_lifetime = timedelta(days=7)

CORS(app)

# Register APIs
app.register_blueprint(prediction_bp)
app.register_blueprint(xray_bp)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --------------------------------
# AUTH PAGE
# --------------------------------
@app.route("/")
def auth():
    return render_template("auth.html")

# --------------------------------
# REGISTER USER
# --------------------------------
@app.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        name = data.get("name")
        email = data.get("email", "").strip()
        password = data.get("password")
        role = data.get("role")
        specialization = data.get("specialization")

        if role == "patient":
            specialization = None

        conn = get_connection()

        existing = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if existing:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Email already registered"
            })

        conn.execute(
            """
            INSERT INTO users (name,email,password,role,specialization)
            VALUES (?,?,?,?,?)
            """,
            (name, email, password, role, specialization)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "registered",
            "message": "Account created successfully"
        })

    except Exception as e:

        print("REGISTER ERROR:", e)

        return jsonify({
            "status": "error",
            "message": "Registration failed"
        })

# --------------------------------
# LOGIN USER
# --------------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password")
    remember = data.get("remember")

    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    if not user:
        conn.close()
        return jsonify({
            "status": "fail",
            "message": "Email not registered"
        })

    if user["password"] != password:
        conn.close()
        return jsonify({
            "status": "fail",
            "message": "Incorrect password"
        })

    if remember:
        session.permanent = True
    else:
        session.permanent = False

    session["user"] = email
    session["role"] = user["role"]
    session["specialization"] = user["specialization"]

    conn.close()

    return jsonify({"status": "success"})

# --------------------------------
# LOGOUT
# --------------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# --------------------------------
# DASHBOARD
# --------------------------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    conn = get_connection()

    role = session.get("role")
    specialization = session.get("specialization")

    total = conn.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    high = conn.execute(
        "SELECT COUNT(*) FROM patients WHERE prediction LIKE '%High%'"
    ).fetchone()[0]

    low = conn.execute(
        "SELECT COUNT(*) FROM patients WHERE prediction LIKE '%Low%'"
    ).fetchone()[0]

    avg_density = conn.execute(
        "SELECT AVG(bone_density) FROM patients"
    ).fetchone()[0]

    patients = []

    if role == "doctor":

        patients = conn.execute(
            """
            SELECT * FROM patients
            WHERE LOWER(bone_type) = LOWER(?)
            """,
            (specialization,)
        ).fetchall()

    conn.close()

    welcome = f"Welcome {role.title()} {session.get('user')}"

    data = {
        "total": total or 0,
        "high": high or 0,
        "low": low or 0,
        "avg_density": round(avg_density or 0, 2),
        "patients": patients,
        "role": role,
        "welcome": welcome
    }

    return render_template("dashboard.html", data=data)

# --------------------------------
# UPLOAD PAGE
# --------------------------------
@app.route("/upload")
def upload():

    if "user" not in session:
        return redirect("/")

    return render_template("upload.html")

# --------------------------------
# RESULT PAGE
# --------------------------------
@app.route("/result")
def result():

    if "user" not in session:
        return redirect("/")

    return render_template("result.html")

# --------------------------------
# XRAY UPLOAD PAGE
# --------------------------------
@app.route("/upload_xray")
def upload_xray():

    if "user" not in session:
        return redirect("/")

    return render_template("upload_xray.html")

# --------------------------------
# SERVE UPLOADED FILE
# --------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# --------------------------------
# AI BONE HEALTH CHAT ASSISTANT
# --------------------------------
@app.route("/chatbot", methods=["POST"])
def chatbot():

    data = request.get_json()
    msg = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant specialized in bone health, osteoporosis, diet, and exercise."
                },
                {
                    "role": "user",
                    "content": msg
                }
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})
# --------------------------------
# RUN SERVER
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)