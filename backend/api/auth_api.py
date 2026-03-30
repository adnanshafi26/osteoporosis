from flask import Blueprint, request, jsonify
from database.db import get_connection

auth_bp = Blueprint("auth", __name__)

# ---------------------
# Register
# ---------------------

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    conn = get_connection()

    conn.execute(
        "INSERT INTO users(name,email,password) VALUES(?,?,?)",
        (name,email,password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"User registered successfully"})


# ---------------------
# Login
# ---------------------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    ).fetchone()

    conn.close()

    if user:

        return jsonify({"status":"success"})

    else:

        return jsonify({"status":"invalid"})