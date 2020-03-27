#!/bin/bash

killall -q python3
rm -f /tmp/distance_producer.pid
rm -f /tmp/motor_control_consumer.pid
rm -f /tmp/camera_producer.pid
rm -f /tmp/web_monitor.pid

python3 web_monitor.py > /dev/null 2>&1 &
pgrep -f 'python3 web_monitor.py' > /tmp/web_monitor.pid
python3 distance_sensor_producer.py > /dev/null 2>&1 &
pgrep -f 'python3 distance_sensor_producer.py' > /tmp/distance_producer.pid
python3 motor_control_consumer.py > /dev/null 2>&1 &
pgrep -f 'python3 motor_control_consumer.py' > /tmp/motor_control_consumer.pid
python3 camera_producer.py > /dev/null 2>&1 &
pgrep -f 'python3 camera_producer.py' > /tmp/camera_producer.pid

echo "Waiting for piCar to launch"
while ! curl --output /dev/null --silent --head --fail http://localhost:5000; do sleep 1 && echo -n .; done;
echo
