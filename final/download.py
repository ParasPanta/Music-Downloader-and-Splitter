from pytube import YouTube,Playlist
from art import *
import re
import os
from pathlib import Path

# Change for saving in a different directory
output_dir_PL = 'downloadPL/'



# Links from Playlist Part

def get_pl(playlists):
    urls = []

    for playlist in playlists:
        playlist_urls = Playlist(playlist)

        for url in playlist_urls:
            urls.append(url)

    return urls

def get_urls_pl(playlist_url):
    urls = []

    playlist_urls = Playlist(playlist_url)

    for url in playlist_urls:
        urls.append(url)
    
    return urls

# Download Part

def clean_saved_dir(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    print(f"Removed all files from dir: {dir}")

def download_youtube_mp3_from_video_id(id, output_dir):
    base_url = 'https://www.youtube.com/watch?v='
    url = f'{base_url}{id}'
    yt = YouTube(url)
    status = yt.vid_info['playabilityStatus']['status']
    if status == "UNPLAYABLE":
        print(f"video_id {id} is not playable, cannot download.")
        return

    try: isinstance(yt.length, int)
    except:
        print(f"Could not get video length for {id}. Skipping download.")
        return

    # create condition - if the yt.length > 600 (10 mins), then don't download it
    if yt.length > 600:
        print(f"video_id {id} is longer than 10 minutes, will not download.")
        return

    video = yt.streams.filter(only_audio=True).first()

    try: song_title_raw = yt.title
    except:
        print(f'Unable to get title for id {id}. Skipping download.')
        return
    song_title = re.sub('\W+',' ', song_title_raw).lower().strip()
    song_path = f"{song_title}"

    # download_path = f"saved_mp3s/{song_path}"
    download_path = f"{output_dir}{song_path}"
    out_file = video.download(download_path)

    # save the file (which will be mp4 format)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # move the mp3 to the root dir
    p = Path(new_file).absolute()
    parent_dir = p.parents[1]
    p.rename(parent_dir / p.name)

    # delete the child dir
    os.rmdir(download_path)

    # result of success
    print(f"{song_path} has been successfully downloaded. Video id: {id}")

def manage_download_of_ids(video_ids, output_dir):
    for id in video_ids:
        try: download_youtube_mp3_from_video_id(id, output_dir)
        except: print(f'Failed to download video id: {id}')

def check_if_dir_exists(dir_path):
    dir_exists = os.path.isdir(dir_path)
    if not dir_exists:
        os.mkdir(path=dir_path)


def run_playlist():
    output_dir = output_dir_PL

    test = input("Playlist Link : ")

    urls = get_urls_pl(test)

    video_ids = []

    for url in urls:
        id = url.split('?v=')

        video_ids.append(id[1])

    check_if_dir_exists(dir_path=output_dir)
    clean_saved_dir(dir=output_dir)
    manage_download_of_ids(video_ids, output_dir)

    print('Successfully downloaded ' + str(len(video_ids)) + ' songs in mp3 format.')

def run_link():
    output_dir = 'download/'

    test = input("Link : ")

    video_id = test.split('?v=')

    id = video_id[1]

    download_youtube_mp3_from_video_id(id, output_dir)


def run():
    print('1. Download Playlist')
    print('2. Download One Song')
    choice = int(input('Choice :'))

    if choice == 1:
        run_playlist()
    
    elif choice == 2:
        run_link()
    else:
        exit()

run()