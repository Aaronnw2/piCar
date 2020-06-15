#!/bin/bash

pkill -f 'python3 gamepad.py'
pkill -f 'java -jar target/picar-proxy-server-1.0.0.jar'
pkill -f 'python3 opencv_receive.py'
killall -q ffmpeg

cd picar-proxy-server
java -jar target/picar-proxy-server-1.0.0.jar > /dev/null 2>&1 &

ssh -T pi@192.168.50.69 << EOF
  killall -q python3
  killall -q raspivid
  rm -f /tmp/distance_producer.pid
  rm -f /tmp/motor_control_consumer.pid
  rm -f /tmp/camera_producer.pid
  rm -f /tmp/web_monitor.pid
EOF

cd ../server

python3 gamepad.py &
./stream_from_queue.sh train > /dev/null 2>&1 &
cd ..

scp car/web_monitor.py \
  car/motor_control_consumer.py \
  car/distance_sensor_producer.py \
  car/camera_producer.py \
  car/local_start.sh \
  pi@piCar.local:/home/pi

ssh -T pi@192.168.50.69 << EOF
  python3 web_monitor.py > /dev/null 2>&1 &
  pgrep -f 'python3 web_monitor.py' > /tmp/web_monitor.pid
  python3 distance_sensor_producer.py > /dev/null 2>&1 &
  pgrep -f 'python3 distance_sensor_producer.py' > /tmp/distance_producer.pid
  python3 motor_control_consumer.py > /dev/null 2>&1 &
  pgrep -f 'python3 motor_control_consumer.py' > /tmp/motor_control_consumer.pid
  raspivid -t 0 -w 320 -h 240 -fps 30 -br 70 -co 50 -o - | nc 192.168.50.237 2222 > /dev/null 2>&1 &
  pgrep -f 'raspivid' > /tmp/camera_producer.pid
EOF

echo "Waiting for piCar to launch"
while ! curl --output /dev/null --silent --head --fail http://192.168.50.69:5000; do sleep 1 && echo -n .; done;
echo