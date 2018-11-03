import json
import os
import traceback
import pika
import pigpio

def set_left_motors(value):
    if value < 0:
        motor_value = map_to_dutycycle(value * -1)
        print('Left motor value: ', motor_value)
        PI.set_PWM_dutycycle(16, motor_value)
        PI.set_PWM_dutycycle(19, 0)
        PI.set_PWM_dutycycle(2, motor_value)
        PI.set_PWM_dutycycle(3, 0)
    else:
        motor_value = map_to_dutycycle(value)
        print('Left motor value: ', motor_value)
        PI.set_PWM_dutycycle(19, motor_value)
        PI.set_PWM_dutycycle(16, 0)
        PI.set_PWM_dutycycle(3, motor_value)
        PI.set_PWM_dutycycle(2, 0)

def set_right_motors(value):
    if value < 0:
        motor_value = map_to_dutycycle(value * -1)
        print('Right motor value: ', motor_value)
        PI.set_PWM_dutycycle(20, motor_value)
        PI.set_PWM_dutycycle(26, 0)
        PI.set_PWM_dutycycle(27, motor_value)
        PI.set_PWM_dutycycle(17, 0)
    else:
        motor_value = map_to_dutycycle(value)
        print('Right motor value: ', motor_value)
        PI.set_PWM_dutycycle(26, motor_value)
        PI.set_PWM_dutycycle(20, 0)
        PI.set_PWM_dutycycle(17, motor_value)
        PI.set_PWM_dutycycle(27, 0)

def map_to_dutycycle(value):
    return 255 * value

def on_message(channel, method, properties, body):
    control_update = json.loads(body.decode('utf-8'))
    set_left_motors(control_update[0])
    set_right_motors(control_update[1])
try:
    PI = pigpio.pi()

    CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('192.168.50.238'))
    CHANNEL = CONNECTION.channel()
    CHANNEL.queue_declare(queue='control')

    CHANNEL.basic_consume(on_message,
                          queue='control',
                          no_ack=True)
    open("/tmp/control_consume", "w+").close()
    CHANNEL.start_consuming()
except Exception as err:
    print('Error starting controller')
    traceback.print_tb(err)
finally:
    try:
        os.remove('/tmp/control_consume')
    except:
        print('No control_consume file created')
