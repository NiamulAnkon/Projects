import sqlite3

DB_NAME = 'tickets.db'

def get_connection(db_name=DB_NAME):
    return sqlite3.connect(db_name)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Open'
        )
    ''')
    conn.commit()
    conn.close()

def add_ticket(conn, title, description):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (title, description) VALUES (?, ?)
    ''', (title, description))
    conn.commit()
    conn.close()
def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM tickets WHERE id = ?
    ''', (ticket_id,))
    conn.commit()
    conn.close()

def get_all_tickets(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, status FROM tickets')
    tickets = cursor.fetchall()
    conn.close()
    return tickets