from os import path
from flask import Flask

app = Flask(__name__)

@app.route("/")
def control_monitor():
    if not path.exists("/tmp/control_consume"):
        return "down", 500
    if not path.exists("/tmp/distance_produce"):
        return "down", 500
    return "up", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
