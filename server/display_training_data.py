import numpy as np
import cv2
from time import sleep

FONT_POSITION = (20,30)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255)

cv2.namedWindow('frames')
frames = np.load('/home/aaron/Downloads/training_data.npz', allow_pickle=True)['arr_0']
i=0

while True:
    image = frames[i][1]
    scaled_image = cv2.resize(image, (320, 170))
    cv2.putText(scaled_image, str(frames[i][0].decode()) + " " + str(i) + " of " + str(len(frames)), FONT_POSITION, FONT, .5, FONT_COLOR)
    cv2.imshow('frames', scaled_image)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
    i += 1
    if i >= len(frames):
        i = 0

cv2.destroyAllWindows()