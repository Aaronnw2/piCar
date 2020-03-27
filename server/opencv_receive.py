""" Start and read in from an ffmpeg stream and start object tracking """
# pylint: disable=C0103, C0325, E0401
import subprocess as sp
import argparse
#import track
#import train
import display

FFMPEG_BIN = "ffmpeg"
COMMAND = [FFMPEG_BIN,
           '-i', 'buffer',         # buffer is the named pipe
           '-pix_fmt', 'bgr24',    # opencv uses bgr24 pixel format.
           '-vcodec', 'rawvideo',
           '-an', '-sn',           # no audio
           '-f', 'image2pipe', '-']
pipe = sp.Popen(COMMAND, stdout=sp.PIPE, bufsize=10**8)

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=True, help="mode to start up")
args = vars(ap.parse_args())
mode = args["mode"]

#if mode == 'track':
#    track.track_video(pipe)
#elif mode == 'train':
#    train.start_training_capture(pipe)
if mode == 'display':
    display.display_video(pipe)
else:
    print('Must give mode parameter (-m, --mode) of either train or track')
