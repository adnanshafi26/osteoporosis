import sqlite3

DB_NAME = "osteoporosis.db"


# -------------------------------
# Database Connection
# -------------------------------
def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


# -------------------------------
# Initialize Database
# -------------------------------
def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    # USERS TABLE (PATIENTS + DOCTORS)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT,
        specialization TEXT
    )
    """)

    # PATIENT CLINICAL DATA TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender INTEGER,
        bmi REAL,
        bone_density REAL,
        calcium REAL,
        vitamin_d REAL,
        bone_type TEXT,
        prediction TEXT,
        fracture_risk TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # XRAY RESULTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS xray_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        image_path TEXT,
        prediction TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()