# from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Tk
from tkinter import filedialog
import json
import subprocess
import os


def controller():
    input('Press enter to select JSON file')
    playlists = open_json()

    input('Press enter to select folder where the playlists will be downloaded')
    root = Tk()
    root.withdraw()
    download_path = filedialog.askdirectory(parent=root)
    root.update()

    for i, pl in enumerate(playlists):
        pl_name = pl['name']
        create_directory(download_path, pl_name)

        for j, track in enumerate(pl['tracks']):
            print_progress(i, len(playlists), j, len(pl['tracks']))
            track_uri = extract_track_uri(track['uri'])
            download_track(track_uri, f'{download_path}/{pl_name}')


def open_json():
    root = Tk()
    root.withdraw()
    pathname = filedialog.askopenfilename(parent=root)  # TODO: ugly interface
    root.update()
    with open(pathname) as f:
        result = json.load(f)
    return result


def extract_track_uri(track_uri: str):
    temp = track_uri.split(':')
    assert len(temp) == 3
    return temp[-1]


def download_track(uri: str, playlist_path: str):
    assert os.path.isdir(playlist_path)
    bash_command = f'spotdl https://open.spotify.com/track/{uri}'
    try:
        process = subprocess.Popen(
            bash_command.split(), stdout=subprocess.PIPE, cwd=playlist_path)
        status = process.wait()
    except OSError:
        pass
    except subprocess.CalledProcessError:
        pass
    # TODO: subprocess calls other python file which throws error if song already downloaded -> I don't think you can catch this error?


def create_directory(root: str, dir_name: str):
    dir_path = f'{root}/{dir_name}'

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def print_progress(curr_pl: int, total_pl: int, curr_track: int, total_track: int):
    print(
        f'Progress: playlist {curr_pl+1}/{total_pl} - track {curr_track+1}/{total_track}', end='\r')


if __name__ == '__main__':
    controller()
