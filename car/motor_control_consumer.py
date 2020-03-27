import traceback
import socket
import pigpio

def set_left_motors(value):
    if value < 0:
        motor_value = map_to_dutycycle(value * -1)
        PI.set_PWM_dutycycle(16, motor_value)
        PI.set_PWM_dutycycle(19, 0)
        PI.set_PWM_dutycycle(2, motor_value)
        PI.set_PWM_dutycycle(3, 0)
    else:
        motor_value = map_to_dutycycle(value)
        PI.set_PWM_dutycycle(19, motor_value)
        PI.set_PWM_dutycycle(16, 0)
        PI.set_PWM_dutycycle(3, motor_value)
        PI.set_PWM_dutycycle(2, 0)

def set_right_motors(value):
    if value < 0:
        motor_value = map_to_dutycycle(value * -1)
        PI.set_PWM_dutycycle(20, motor_value)
        PI.set_PWM_dutycycle(26, 0)
        PI.set_PWM_dutycycle(27, motor_value)
        PI.set_PWM_dutycycle(17, 0)
    else:
        motor_value = map_to_dutycycle(value)
        PI.set_PWM_dutycycle(26, motor_value)
        PI.set_PWM_dutycycle(20, 0)
        PI.set_PWM_dutycycle(17, motor_value)
        PI.set_PWM_dutycycle(27, 0)

def map_to_dutycycle(value):
    return 255 * value

def on_message(body):
    set_left_motors(float(body[1:5]))
    set_right_motors(float(body[7:11]))

try:
    PI = pigpio.pi()

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect(("192.168.50.237", 8080))
    print("Connected")
    serversocket.send('CONSUMER,MOTOR_DATA'.encode())
    print("Registered")
    while True:
        data = serversocket.recv(13)
        # print("received data:", data)
        on_message(data)
except Exception as err:
    print('Error starting controller')
    traceback.print_tb(err)
finally:
    serversocket.close()