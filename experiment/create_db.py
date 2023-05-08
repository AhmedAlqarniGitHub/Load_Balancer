import sqlite3
import os

DB_FILE = os.path.join("db", "servers.db")

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base_url TEXT NOT NULL,
        port TEXT NOT NULL,
        is_alive INTEGER NOT NULL DEFAULT 1,
        location_code TEXT NOT NULL DEFAULT "1"
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
