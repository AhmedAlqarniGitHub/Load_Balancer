from flask import Flask, render_template_string

app = Flask(__name__)

# endpoint to check if server running
@app.route("/")
def backend_server():
    team_names = ["Bander AlGhamdi", "Ahmed AlQarni", "Waleed Alfaifi"]
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
        <style>
            table, th, td {
                border: 1px solid black;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to COE-523 Project</h1><br/>
        <h1>Team 3</h1>
        <table>
            <tr>
                <th>Name</th>
            </tr>
            {% for name in names %}
            <tr>
                <td>{{ name }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, names=team_names), 200

if __name__ == "__main__":
    app.run()
