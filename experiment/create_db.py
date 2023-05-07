import sqlite3
import os

DB_FILE = os.path.join("db", "servers.db")

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        is_alive INTEGER NOT NULL DEFAULT 1
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
