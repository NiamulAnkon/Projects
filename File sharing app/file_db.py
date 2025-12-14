import sqlite3
from datetime import datetime

DB_NAME = 'files.db'


def init_db(db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_username TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            is_folder INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_username TEXT NOT NULL,
            target_username TEXT NOT NULL,
            file_path TEXT NOT NULL,
            shared_at TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def insert_file(owner_username: str, file_name: str, file_path: str, is_folder: bool, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (owner_username, file_name, file_path, is_folder, created_at) VALUES (?, ?, ?, ?, ?)",
        (owner_username, file_name, file_path, 1 if is_folder else 0, datetime.now()),
    )
    conn.commit()
    last = cursor.lastrowid
    conn.close()
    return last


def delete_file_by_path(file_path: str, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE file_path = ?", (file_path,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return changes


def list_files_by_owner(owner_username: str, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, file_name, file_path, is_folder, created_at FROM files WHERE owner_username = ? ORDER BY created_at DESC",
        (owner_username,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_file_by_path(file_path: str, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, owner_username, file_name, file_path, is_folder, created_at FROM files WHERE file_path = ?", (file_path,))
    row = cursor.fetchone()
    conn.close()
    return row


def share_file(owner_username: str, file_path: str, target_username: str, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shares (owner_username, target_username, file_path, shared_at) VALUES (?, ?, ?, ?)",
                   (owner_username, target_username, file_path, datetime.now()))
    conn.commit()
    last = cursor.lastrowid
    conn.close()
    return last


def list_shared_with_user(target_username: str, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, owner_username, target_username, file_path, shared_at FROM shares WHERE target_username = ? ORDER BY shared_at DESC",
                   (target_username,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_share_by_id(share_id: int, db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shares WHERE id = ?", (share_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return changes
