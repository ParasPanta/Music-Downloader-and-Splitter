import ffmpeg as fm
import sys
import os


new_dir = './music'


for f in os.listdir(new_dir):

    base, ext = os.path.splitext(f)

    # print(base, ext)

    if ext == '.mp3':

        print(base, ext)