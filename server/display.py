# pylint: disable=C0103, C0325, E0401, E0401
""" Displays the video feed """
import cv2
import utility
import numpy as np

def display_video(pipe):
    """ Shows the video feed """
    print('Displaying video feed...')
    cv2.namedWindow('Video feed')
    cv2.moveWindow('Video feed', 850, 20)
    #TODO: next pull in control data and display, maybe show different image layers
    while True:
        image = utility.read_image(pipe)
        if image is not None:
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            uncropped_median = np.median(grey_image)
            cropped_image = grey_image[70:240, 0:320]
            blurred_image = cv2.bilateralFilter(cropped_image, 7, 75, 75)
            canny_edge = auto_canny(blurred_image, uncropped_median)
            combined_images = np.vstack((image, cv2.cvtColor(canny_edge, cv2.COLOR_GRAY2RGB)))
            cv2.imshow('Video feed', combined_images)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pipe.stdout.flush()

    cv2.destroyAllWindows()

def auto_canny(image, median, sigma=0.33):
	lower = int(max(0, (1.0 - sigma) * median))
	upper = int(min(255, (1.0 + sigma) * median))
	edge = cv2.Canny(image, lower, upper)
	return edge