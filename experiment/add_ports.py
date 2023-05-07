import sqlite3
import os

DB_FILE = os.path.join("/db", "servers.db")


def add_server(port, is_alive):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO servers (port, is_alive) VALUES (?, ?)", (port, is_alive))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    for port in range(5001, 5006):
        add_server(port, 1)
    print("Added servers with ports 5001 to 5005 in the database.")
