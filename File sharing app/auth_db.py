import sqlite3
import bcrypt
from datetime import datetime

DB_NAME = 'auth.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def register_user(username: str, email: str, password: str) -> bool:
    try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # check duplicate username/email
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                return False, "Username or email already exists."

            # hash password
            password_hash = hash_password(password)

            cursor.execute("""
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, datetime.now()))

            conn.commit()
            return True, "Registration successful."

    except Exception as e:
        return False, f"Error: {str(e)}"

    finally:
        conn.close()

def login_user(username: str, password: str) -> bool:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, email, password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return False, "User not found.", {}

        user_id, db_username, db_email, db_hash = row

        if not verify_password(password, db_hash):
            return False, "Invalid password.", {}

        # login success
        user_data = {
            "id": user_id,
            "username": db_username,
            "email": db_email
        }
        return True, "Login successful.", user_data

    except Exception as e:
        return False, f"Error: {str(e)}", {}

    finally:
        conn.close()