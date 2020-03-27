import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(("192.168.50.237", 8080))
print("Connected")
server_socket.send('CONSUMER,DISTANCE_SENSOR_DATA'.encode())
print("Registered")

while True:
    data = server_socket.recv(32)
    print(data.decode("utf-8"))
server_socket.close()