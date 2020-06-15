# pylint: disable=C0103, C0325, E0401, E0401
""" Gathers training data """
import cv2
import utility
import numpy as np
import socket
from select import select

FONT_POSITION = (20,30)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255)

def __maybe_update_control_data(socket, current_data):
  r,w,e = select([socket], [], [], 0)
  if len(r) == 1:
    return r[0].recv(13)
  else:
    return current_data

def gather_data(pipe):
    saved_images = []
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8080))
    print("Connected")
    client_socket.send('CONSUMER,MOTOR_DATA'.encode())
    print("Registered")
    control_data = '[+0.00,+0.00]'.encode()
    cv2.namedWindow('Video feed')
    cv2.moveWindow('Video feed', 850, 20)

    while(True):
        control_data = __maybe_update_control_data(client_socket, control_data)
        image = utility.read_image(pipe)
        if image is not None:
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            uncropped_median = np.median(grey_image)
            cropped_image = grey_image[70:240, 0:320]
            blurred_image = cv2.bilateralFilter(cropped_image, 7, 75, 75)
            canny_edge = utility.auto_canny(blurred_image, uncropped_median)
            output = cv2.resize(canny_edge, (160, 85))
            saved_images.append([control_data, output])
            
            display = np.copy(output)
            cv2.putText(display, str(control_data.decode()), FONT_POSITION, FONT, .5, FONT_COLOR)
            cv2.imshow('Video feed', display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pipe.stdout.flush()
    cv2.destroyAllWindows()
    saved_images = np.asarray(saved_images)
    np.savez('/home/aaron/Downloads/training_data.npz', saved_images)