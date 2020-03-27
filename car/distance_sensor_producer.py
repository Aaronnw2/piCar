import os
import traceback
import socket
import serial
from os import path
import time

SER = serial.Serial('/dev/serial0')
SER.baudrate = 9600

def maybe_update_vehicle_status(currentCarState):
    servicesUp = 0
    motor_pid = open("/tmp/motor_control_consumer.pid", "r").read().rstrip()
    if path.exists("/proc/" + motor_pid):
        servicesUp += 1
    camera_pid = open("/tmp/camera_producer.pid", "r").read().rstrip()
    if path.exists("/proc/" + camera_pid):
        servicesUp += 1
    if currentCarState != servicesUp:
        print('Setting car status: ' + str(servicesUp))
        SER.write(str(servicesUp).encode('utf-8'))
    return servicesUp

try:
    currentCarState = 0
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect(("192.168.50.237", 8080))
    print("Connected")
    serversocket.send('PRODUCER,DISTANCE_SENSOR_DATA'.encode())
    print("Registered")
    while True:
        currentCarState = maybe_update_vehicle_status(currentCarState)
        time.sleep(0.1)
        if SER.inWaiting():
            MESSAGE = SER.readline().decode('utf-8').split('\r\n')[0]
            serversocket.send(MESSAGE.encode())
except Exception as err:
    traceback.print_tb(err)
finally:
    SER.write('0'.encode('utf-8'))
    SER.close()
