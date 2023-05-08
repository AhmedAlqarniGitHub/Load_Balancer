from flask import request

@app.route('/')
def index():
    url = 'http://freegeoip.net/json/{}'.format(request.remote_addr)
    r = requests.get(url)
    j = json.loads(r.text)
    city = j['city']

    print(city)