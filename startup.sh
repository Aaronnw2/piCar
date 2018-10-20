#!/bin/bash

docker stop rabbit
docker wait rabbit
docker rm rabbit
docker run -d --hostname rabbit -p 8080:15672 -p 5672:5672 --name rabbit rabbitmq:3-management

#echo "Rebooting pi..."

#ssh pi@192.168.50.69 << EOF
#  sudo reboot
#EOF

echo "Waiting RabbitMq web interface to launch on 8080..."

while ! curl --output /dev/null --silent --head --fail http://localhost:8080; do sleep 1 && echo -n .; done;

scp car/web_monitor.py pi@piCar.local:/home/pi
scp car/motor_control.py pi@piCar.local:/home/pi
scp car/distance_sensor_producer.py pi@piCar.local:/home/pi

ssh pi@192.168.50.69 << EOF
  killall -9 python3
  python3 web_monitor.py > /dev/null 2>&1 &
  python3 motor_control.py > control.txt &
  python3 distance_sensor_producer.py &
EOF

echo "Waiting for piCar to launch"
while ! curl --output /dev/null --silent --head --fail http://192.168.50.69:5000; do sleep 1 && echo -n .; done;

python3 server/gamepad.py