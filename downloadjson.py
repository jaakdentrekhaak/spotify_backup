# from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Tk
from tkinter import filedialog
import json
import subprocess
import os
from typing import List
from spotdl.download import DownloadManager
from spotdl.parsers import parse_query
from spotdl.search import SpotifyClient


def controller():
    input('Press enter to select JSON file')
    playlists = open_json()

    input('Press enter to select folder where the playlists will be downloaded')
    download_path = ask_directory()

    # Initialize spotify client
    SpotifyClient.init(
        client_id="5f573c9620494bae87890c0f08a60293",
        client_secret="212476d9b0f3472eaa762d90b19b0ba8",
        user_auth=False,
    )

    for i, pl in enumerate(playlists):
        pl_name = pl['name']
        create_directory(download_path, pl_name)

        # for j, track in enumerate(pl['tracks']):
        #     print_progress(i, len(playlists), j, len(pl['tracks']))
        #     track_uri = extract_track_uri(track['uri'])
        #     download_track(track_uri, f'{download_path}/{pl_name}')
        uris = [extract_track_uri(track['uri']) for track in pl['tracks']]
        download_tracks(uris, f'{download_path}/{pl_name}')


def open_json():
    root = Tk()
    root.withdraw()
    pathname = filedialog.askopenfilename(parent=root)  # TODO: ugly interface
    root.update()
    assert pathname.endswith('.json')
    with open(pathname) as f:
        result = json.load(f)
    return result


def ask_directory():
    root = Tk()
    root.withdraw()
    download_path = filedialog.askdirectory(parent=root)
    root.update()
    assert download_path != ()
    return download_path


def extract_track_uri(track_uri: str):
    temp = track_uri.split(':')
    assert len(temp) == 3
    return temp[-1]


# def download_track(uri: str, playlist_path: str):
#     assert os.path.isdir(playlist_path)
#     bash_command = f'spotdl https://open.spotify.com/track/{uri}'
#     try:
#         process = subprocess.Popen(
#             bash_command.split(), stdout=subprocess.PIPE, cwd=playlist_path)
#         status = process.wait()
#     except OSError:
#         pass
#     except subprocess.CalledProcessError:
#         pass
#     # TODO: subprocess calls other python file which throws error if song already downloaded -> I don't think you can catch this error?


def download_tracks(uris: List[str], playlist_path: str):
    assert os.path.isdir(playlist_path)

    spotdl_opts = {
        "query": uris_to_urls(uris),
        # "output_format": "wav",
        # "download_threads": 6,
        # "use_youtube": False,
        # "generate_m3u": False,
        # "search_threads": 2,
    }

    # Change working directory to download tracks to playlist folder
    os.chdir(playlist_path)

    with DownloadManager(spotdl_opts) as downloader:
        # Get songs
        song_list = parse_query(
            spotdl_opts["query"],
            None,
            None,
            None,
            None,
            None,
            None
        )

        # Start downloading
        if len(song_list) > 0:
            downloader.download_multiple_songs(song_list)
            # TODO: handle OSError (not possible -> temporarily commented out)
            # TODO: create own log that stores already downloaded track uris


def create_directory(root: str, dir_name: str):
    dir_path = f'{root}/{dir_name}'

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def print_progress(curr_pl: int, total_pl: int, curr_track: int, total_track: int):
    print(
        f'Progress: playlist {curr_pl+1}/{total_pl} - track {curr_track+1}/{total_track}', end='\r')


def uris_to_urls(uris: List[str]):
    return [f'https://open.spotify.com/track/{uri}' for uri in uris]


if __name__ == '__main__':
    controller()
