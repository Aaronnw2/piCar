import os
import traceback
import pika
import serial
from os import path

SER = serial.Serial('/dev/serial0')
SER.baudrate = 9600

CON = pika.BlockingConnection(pika.ConnectionParameters("192.168.50.238"))
CHAN = CON.channel()
CHAN.queue_declare(queue="distances")

def maybe_update_vehicle_status(currentCarState):
    servicesUp = 0
    if path.exists("/tmp/control_consume"):
        servicesUp += 1
    if path.exists("/tmp/distance_produce"):
        servicesUp += 1
    if currentCarState != servicesUp:
        SER.write(str(servicesUp).encode('utf-8'))
        currentCarState = servicesUp
    return currentCarState

try:
    currentCarState = 0
    while True:
        if SER.inWaiting():
            open("/tmp/distance_produce", "w+").close()
            MESSAGE = SER.readline().decode('utf-8').split('\r\n')[0]
            print(MESSAGE)
            CHAN.basic_publish(exchange="",
                               routing_key="distances",
                               body=MESSAGE)
        currentCarState = maybe_update_vehicle_status(currentCarState)
except Exception as err:
    print('Error starting controller')
    traceback.print_tb(err)
finally:
    try:
        os.remove('/tmp/distance_produce')
    except:
        print('No distance_produce file created')
