import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "student_app.db")

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# PREDICTIONS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    study_hours REAL,
    attendance REAL,
    participation REAL,
    predicted_score REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# CREATE ADMIN (FORCE)
cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES (?, ?, ?)
""", ("aasini", hash_pw("admin123"), "admin"))

conn.commit()
conn.close()

print("Database initialized successfully")
