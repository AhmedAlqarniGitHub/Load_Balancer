from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_FILE = os.path.join("/db", "servers.db")

def get_alive_servers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE is_alive = 1")
    alive_servers = cursor.fetchall()
    conn.close()
    return alive_servers

@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200

@app.route('/get_server')
def get_server():
    servers = get_alive_servers()
    if not servers:
        return jsonify({"error": "No alive servers found"}), 404
    return jsonify(servers[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
