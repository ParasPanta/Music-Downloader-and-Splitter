from threading import main_thread
from tracemalloc import start
from art import *
import ffmpeg as fm
import os
import sys

main_dir = './music'

output_dir = main_dir + '/output'

sys.path.append(r'/usr/bin')

# ffmpeg -i somefile.mp3 -f segment -segment_time 3 -c copy out%03d.mp3



def split_songs(song_name, root_dir, base_name, dir_path = output_dir):
    
    # print(song_name, dir_path)
    st = fm.input(root_dir + '/' + song_name)

    st_cut = st.audio.filter('atrim', duration = 30, start = 120)

    st = fm.output(st_cut, dir_path + '/' + base_name+'.wav')

    fm.run(st)

def check_if_dir_exists(dir_path):
    dir_exists = os.path.isdir(dir_path)
    if not dir_exists:
        os.mkdir(path=dir_path)
        # print(dir_path + ' not found')'./music'

def list_names(dir):
    for f in os.listdir(dir):

        # splitting file basename and extensions
        base, ext = os.path.splitext(f)

        if ext == '.mp3':

            # loc for creating directory for each song split to 30 sec
            new_dir = dir + '/' + base

            # creation of folder
            # check_if_dir_exists(new_dir)

            # split_songs(str(base+ext), dir, base, new_dir)
            split_songs(str(base+ext), dir, base)

            # print(base)
        


    print(f"\nSplit all filenames: {dir}")
    tprint('FINISH')


list_names(main_dir)