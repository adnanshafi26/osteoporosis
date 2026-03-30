import sqlite3

conn = sqlite3.connect("database/osteoporosis.db")

cursor = conn.cursor()

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

print("Database table created successfully")