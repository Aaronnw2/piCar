import os
import traceback
import pika
import serial

SER = serial.Serial('/dev/ttyAMA0')
SER.baudrate = 115200

CON = pika.BlockingConnection(pika.ConnectionParameters("192.168.50.226"))
CHAN = CON.channel()
CHAN.queue_declare(queue="distances")
try:
    while True:
        if SER.inWaiting():
            open("/tmp/distance_produce", "w+").close()
            MESSAGE = SER.readline().decode('utf-8').split('\r\n')[0]
            print(MESSAGE)
            CHAN.basic_publish(exchange="",
                               routing_key="distances",
                               body=MESSAGE)
except Exception as err:
    print('Error starting controller')
    traceback.print_tb(err)
finally:
    try:
        os.remove('/tmp/distance_produce')
    except:
        print('No distance_produce file created')
