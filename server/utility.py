# pylint: disable=C0103, C0325, E0401
""" Utility methods for training and detection """
import csv
import numpy
import cv2

def read_image(inpipe):
    """ Reads a new frame from the stream """
    raw_image = inpipe.stdout.read(320*240*3)
    frame = numpy.fromstring(raw_image, dtype='uint8')
    return frame.reshape(240, 320, 3)

def skip_frames(number, inpipe):
    """ Throws out a certain number of frames """
    inpipe.stdout.read(320*240*number)

def write_data_records(records):
    """ writes pairs of image files with controller state to a csv """
    with open('./data/image_data.csv', 'w') as csvfile:
        fieldnames = ['file', 'controller_state_l', 'controller_state_r']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({'file': record['file'], 'boxes': record['boxes']})

def auto_canny(image, median, sigma=0.33):
	lower = int(max(0, (1.0 - sigma) * median))
	upper = int(min(255, (1.0 + sigma) * median))
	edge = cv2.Canny(image, lower, upper)
	return edge