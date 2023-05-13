from flask import Flask, request, jsonify, redirect
import sqlite3
import os
from collections import defaultdict
import time
import requests
import sys
import threading
import http.client
import subprocess

app = Flask(__name__)
DB_FILE = os.path.join("/db", "servers.db")

def get_alive_servers():
    conn = sqlite3.connect(DB_FILE, timeout=15)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers WHERE is_alive = 1")
    alive_servers = cursor.fetchall()
    conn.close()
    return alive_servers

def get_all_servers():
    conn = sqlite3.connect(DB_FILE, timeout=15)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers")
    alive_servers = cursor.fetchall()
    conn.close()
    return alive_servers

servers = get_alive_servers()

client = {
    "url": "http://127.0.0.0:5555",
    "location": {
        "code": "AS",
    },
}

# def get_alive_servers():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM servers")
#     alive_servers = cursor.fetchall()
#     conn.close()
#     return alive_servers

def getContinentId(code):
    if code == 'AF':
        return 1
    elif code == 'AN':
        return 2
    elif code == 'AS':
        return 3
    elif code == 'EU':
        return 4
    elif code == 'NA':
        return 5
    elif code == 'OC':
        return 6
    elif code == 'SA':
        return 7
    else:
        return 0

def get_distance( code_1, code_2):
    code_1 = getContinentId(code_1)
    code_2 = getContinentId(code_2)
    distance = abs(code_2 - code_1)
    return distance    

def get_next_server():
    global servers
    print(servers)
    if not servers:
        while True:
            servers = get_alive_servers()
            checkServersHealth()
            if servers:
                break
            time.sleep(1)
    print(servers)
    selected = servers[0]
    selected_index = 0
    minimum_distance = get_distance(str(selected[5]), str(client["location"]["code"]))
    for index, server in enumerate(servers):
        distance = get_distance(str(server[5]), str(client["location"]["code"]))
        if distance < minimum_distance:
            selected = server
            selected_index = index
            minimum_distance = distance

    if not (not servers or len(servers) < selected_index):
        servers.pop(selected_index)
    return selected

def checkServersHealth():
    global servers
    all_servers = servers
    conn = sqlite3.connect(DB_FILE, timeout=15)
    cursor = conn.cursor()
    if not servers:
        all_servers = get_all_servers()

    for i, server in enumerate(all_servers):
        try:
            response = requests.get(f'http://{server[1]}:5000', timeout=5)
            if response.status_code != 200:
                raise Exception(f'Server returned status code {response.status_code}')
            print( f'http://{server[1]}:5000'+" is Alive Now ",file=sys.stderr)
            cursor.execute("UPDATE servers SET is_alive = 1 WHERE id = ?", (server[0],))
            conn.commit()
        except Exception as e:
            print(f'the following server is not alive : {server[1]}:5000',file=sys.stderr)
            cursor.execute("UPDATE servers SET is_alive = 0 WHERE id = ?", (server[0],))
            conn.commit()
            all_servers.pop(i)
    print ("hello list => ", all_servers)
    conn.close()
    servers = all_servers

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
    server = get_next_server()
    print(server)
    if not server:
        return jsonify({"error": "No alive servers found"}), 404
    
    url = "http://" + server[2] + ":" + server[3]

    print('\nRedirecting client to: ' + url, flush=True)

    return redirect(url, code=302) 


def server_health_check_loop():
    while True:
        checkServersHealth()
        time.sleep(10)

if __name__ == '__main__':
    health_check_thread = threading.Thread(target=server_health_check_loop)
    health_check_thread.start()
    app.run(host='0.0.0.0', port=80)
    

