import sqlite3
import os
from auth import hash_pw

DB_PATH = "student_app.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Create predictions table
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

    # Insert default admin if not exists
    cur.execute("SELECT * FROM users WHERE username=?", ("aasini",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("aasini", hash_pw("admin123"), "admin")
        )

    conn.commit()
    conn.close()

