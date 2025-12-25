import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "student_app.db")

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, 'user')",
            (username, hash_pw(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, hash_pw(password))
    )
    row = cur.fetchone()
    conn.close()
    return row

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def promote(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET role='admin' WHERE username=?", (username,))
    conn.commit()
    conn.close()

def demote(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET role='user' WHERE username=?", (username,))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

def save_prediction(username, h, a, p, score):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO predictions
        (username, study_hours, attendance, participation, predicted_score)
        VALUES (?, ?, ?, ?, ?)
    """, (username, h, a, p, score))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT study_hours, attendance, participation, predicted_score, timestamp
        FROM predictions
        WHERE username=?
        ORDER BY timestamp DESC
    """, (username,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_predictions():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT username, predicted_score, timestamp
        FROM predictions
        ORDER BY timestamp DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
