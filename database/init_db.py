import sqlite3
import os

# Database location
db_path = "backend/osteoporosis.db"

# Create connection
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (

id INTEGER PRIMARY KEY AUTOINCREMENT,
age INTEGER,
gender INTEGER,
bmi REAL,
bone_density REAL,
calcium REAL,
vitamin_d REAL,
bone_type TEXT,
prediction TEXT,
fracture_risk TEXT

)
""")

conn.commit()
conn.close()

print("Database created successfully")