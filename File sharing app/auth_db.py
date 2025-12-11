import sqlite3
import hashlib
import hmac
import os
import base64
from datetime import datetime

DB_NAME = 'auth.db'


SALT_SIZE = 16
ITERATIONS = 100_000
ALGO = 'sha256'


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
    """Hash a password using PBKDF2-HMAC-SHA256 and return an encoded string.

    Format: pbkdf2_<algo>$<iterations>$<salt_b64>$<hash_b64>
    """
    salt = os.urandom(SALT_SIZE)
    dk = hashlib.pbkdf2_hmac(ALGO, password.encode('utf-8'), salt, ITERATIONS)
    return f"pbkdf2_{ALGO}${ITERATIONS}${base64.b64encode(salt).decode('ascii')}${base64.b64encode(dk).decode('ascii')}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a stored hash.

    Supports the new PBKDF2 format produced by `hash_password`.
    If the stored hash appears to be a bcrypt hash and the `bcrypt` package
    is installed, it will attempt bcrypt verification. If `bcrypt` is not
    installed and a bcrypt hash is encountered, a RuntimeError is raised
    (caught by callers).
    """
    # PBKDF2 format: pbkdf2_<algo>$<iterations>$<salt_b64>$<hash_b64>
    if hashed.startswith('pbkdf2_'):
        try:
            prefix, iterations_str, salt_b64, dk_b64 = hashed.split('$')
            algo = prefix.split('_', 1)[1]
            iterations = int(iterations_str)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(dk_b64)
        except Exception:
            return False

        derived = hashlib.pbkdf2_hmac(algo, password.encode('utf-8'), salt, iterations)
        return hmac.compare_digest(derived, expected)

    # Detect common bcrypt hash prefixes and try to use bcrypt only when needed
    if hashed.startswith(('$2b$', '$2a$', '$2y$')):
        try:
            import bcrypt as _bcrypt
        except Exception:
            raise RuntimeError("Stored password uses bcrypt but the `bcrypt` package is not installed. Install it with `pip install bcrypt` to verify existing hashes.")
        return _bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    # Unknown format
    return False


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