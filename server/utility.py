# pylint: disable=C0103, C0325, E0401
""" Utility methods for training and detection """
import csv
import numpy

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
