from flask import Flask, request, jsonify, redirect
import sqlite3
import os
from collections import defaultdict
import time
import requests
import sys

app = Flask(__name__)
def get_alive_servers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE is_alive = 1")
    alive_servers = cursor.fetchall()
    conn.close()
    return alive_servers

servers = get_alive_servers()

client = {
    "url": "http://127.0.0.0:5555",
    "location": {
        "code": 7,
    },
}

DB_FILE = os.path.join("/db", "servers.db")

continent_distances = {
    "AS": {"AS": 0, "AF": 1, "EU": 1, "NA": 2, "AU": 1},
    "AF": {"AS": 1, "AF": 0, "EU": 1, "NA": 2, "AU": 2},
    "EU": {"AS": 1, "AF": 1, "EU": 0, "NA": 1, "AU": 2},
    "NA": {"AS": 2, "AF": 2, "EU": 1, "NA": 0, "AU": 1},
    "AU": {"AS": 1, "AF": 2, "EU": 2, "NA": 1, "AU": 0},
}

def get_country_code_by_port(port):
    if port == 5001:
        return "AS"  # Asia
    elif port == 5002:
        return "AF"  # Africa
    elif port == 5003:
        return "EU"  # Europe
    elif port == 5004:
        return "NA"  # North America
    elif port == 5005:
        return "AU"  # Australia
    else:
        return None

def get_client_country_code():
    port = request.environ.get("REMOTE_PORT")
    return get_country_code_by_port(port)

def get_alive_servers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers")
    alive_servers = cursor.fetchall()
    conn.close()
    # for server,index in alive_servers:
    #     #ping server if not respond pop it
    #     url = "http://" + server.base_url + ":" + server.port
    #     is_up = requests.get(url).status_code == 200
    #     if(is_up == False):
    #        alive_servers.pop(index)
    return alive_servers

def get_distance( code_1, code_2):
    #to be implemented 
    code_1 = int(code_1)
    code_2 = int(code_2)
    distance = abs(code_2 - code_1)
    return distance    

def get_next_server():
    global servers

    if not servers:
        while True:
            servers = get_alive_servers()
            if servers:
                break
            time.sleep(1)

    selected = servers[0]
    selected_index = 0
    minimum_distance = get_distance(str(selected[2]), str(client["location"]["code"]))

    for index, server in enumerate(servers):
        distance = get_distance(str(server[2]), str(client["location"]["code"]))
        if distance < minimum_distance:
            selected = server
            selected_index = index
            minimum_distance = distance

    servers.pop(selected_index)
    return selected

@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200

@app.route('/get_server')
def get_server():
    global client

    if(request.args.get('code')):
        code = request.args.get('code')
    else:
        code = 0

    client = {
        "url": request.host,
        "location": {
            "code": code,
        },
    }

    #127.0.0.0:5001
    #5001
    server = get_next_server()
    print(server)
    if not server:
        return jsonify({"error": "No alive servers found"}), 404
    
    url = "http://" + server.base_url + ":" + server.port

    print('\nRedirecting client to: ' + url, flush=True)

    return redirect(url, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
