import socket
import time
import subprocess as sp

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(("192.168.50.237", 8080))
print("Connected")
server_socket.send('PRODUCER,CAMERA_DATA'.encode())
print("Registered")
connection = server_socket.makefile('wb')

#raspivid -t 0 -w 320 -h 240 -ih -fps 30 -o -
try:
    COMMAND = ["raspivid",
           '-t', '0',
           '-w', '320',
           '-h', '240',
           '-fps', '30',
           '-ih', '-o', "-"]
    raspivid = sp.Popen(COMMAND, stdout=sp.PIPE, stderr=sp.STDOUT)
    while True:
        connection.write(raspivid.stdout.read(320 * 240 * 3))
finally:
    connection.close()
    server_socket.close()
    raspivid.terminate()