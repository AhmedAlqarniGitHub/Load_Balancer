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

def get_alive_servers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers")
    alive_servers = cursor.fetchall()
    conn.close()
    return alive_servers

def get_distance( code_1, code_2):
    #to be implemented 
    code_1 = int(code_1)
    code_2 = int(code_2)
    distance = abs(code_2 - code_1)
    print("distance = ",distance)
    return distance    

def get_next_server():
    global servers
    print(servers)
    if not servers:
        while True:
            servers = get_alive_servers()
            if servers:
                break
            time.sleep(1)
    print(servers)
    selected = servers[0]
    selected_index = 0
    minimum_distance = get_distance(str(selected[4]), str(client["location"]["code"]))

    for index, server in enumerate(servers):
        distance = get_distance(str(server[4]), str(client["location"]["code"]))
        if distance < minimum_distance:
            selected = server
            selected_index = index
            minimum_distance = distance

    servers.pop(selected_index)
    return selected

# def checkServersHealth():
    ## send a get request to all servers
    ## false => change is_alive in db to be 0, remove from local list that called servers

def checkServersHealth():
    global servers
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("hello bander")
    # Iterate over servers
    for i, server in enumerate(servers):
        try:
            # Send GET request to the server
            response = requests.get(f'http://{server[1]}:{server[2]}')
            print( "reponse : ",response , file=sys.stderr)
            # Check response status
            if response.status_code != 200:
                raise Exception(f'Server returned status code {response.status_code}')
            cursor.execute("UPDATE servers SET is_alive = 1 WHERE id = ?", (server[0],))
            
        except Exception as e:
            print(f'Error checking health of server at {server[1]}:{server[2]}: {e}', file=sys.stderr)
            
            # Update is_alive status in the database
            cursor.execute("UPDATE servers SET is_alive = 0 WHERE id = ?", (server[0],))
            conn.commit()

            # Remove server from servers list
            servers.pop(i)
    print ("hello list => ", servers)
    conn.close()

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
    
    url = "http://" + server[1] + ":" + server[2]
    # url = "http://" + "127.0.0.1" + ":" + "5001"

    print('\nRedirecting client to: ' + url, flush=True)

    return redirect(url, code=302)

# @app.route('/run')
# def run():
#     health_check_thread = threading.Thread(target=server_health_check_loop)
#     health_check_thread.start()


def server_health_check_loop():
    while True:
        checkServersHealth()
        time.sleep(1)

if __name__ == '__main__':
    health_check_thread = threading.Thread(target=server_health_check_loop)
    health_check_thread.start()
    app.run(host='0.0.0.0', port=80)
    

