from os import path
from flask import Flask

app = Flask(__name__)

@app.route("/")
def control_monitor():
    motor_pid = open("/tmp/motor_control_consumer.pid", "r").read().rstrip()
    if not path.exists("/proc/" + motor_pid):
        return "down", 500
    distance_pid = open("/tmp/distance_producer.pid", "r").read().rstrip()
    if not path.exists("/proc/" + distance_pid):
        return "down", 500
    camera_pid = open("/tmp/camera_producer.pid", "r").read().rstrip()
    if not path.exists("/proc/" + camera_pid):
        return "down", 500
    return "up", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
