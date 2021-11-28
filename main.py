from typing import Dict, List
import requests
import json
import base64
import os

JSON_FILE_NAME = 'playlists_info.json'


def get_access_token() -> str:
    '''Retrieve the access token needed for communicating with the Spotify API.
    The client-id and the client-secret from the config.json file are used for this (also see README).
    More information about this process can be found here: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow.

    Returns:
        string: Spotify API access token
    '''
    with open('config.json', 'r') as config_file:
        conf = json.load(config_file)
        client_id = conf['spotify']['client_id']
        client_secret = conf['spotify']['client_secret']
    auth = f'{client_id}:{client_secret}'
    auth_bytes = auth.encode('ascii')
    auth_base64_bytes = base64.b64encode(auth_bytes)
    auth_base64 = auth_base64_bytes.decode('ascii')

    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data='grant_type=client_credentials',
        headers=headers
    )
    return json.loads(response.content)['access_token']


def handle_playlist(playlist_url: str) -> None:
    """Main function which handles the whole process for storing information about all songs
    in the playlist corresponding to the given Spotify playlist URL.

    Args:
        playlist_url (str): Spotify playlist URL
    """
    playlist_id = playlist_url_to_id(playlist_url)
    api_playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    token = get_access_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Get playlist name
    playlist_name_response = requests.get(api_playlist_url, headers=headers)
    playlist_name_json = json.loads(playlist_name_response.content)
    playlist_name = playlist_name_json['name']

    items = get_items_in_playlist(api_playlist_url, headers)

    write_to_storage(playlist_name, items)


def get_items_in_playlist(api_playlist_url: str, headers: Dict) -> List[Dict]:
    """Send a GET request to the Spotify API to get information about all the songs in the playlist corresponding to the given playlist url.
    The response contains a list of items which we return.

    Args:
        api_playlist_url (str): API URL for a Spotify playlist
        headers (Dict): A dictionary with HTTP headers containing the authorization token

    Returns:
        List[Dict]: [description]
    """
    api_playlist_tracks_url = api_playlist_url + '/tracks'

    items = []

    playlist_response = requests.get(api_playlist_tracks_url, headers=headers)
    response_json = json.loads(playlist_response.content)
    items.extend(response_json['items'])

    while response_json['next'] is not None:
        playlist_response = requests.get(
            response_json['next'], headers=headers)
        response_json = json.loads(playlist_response.content)
        items.extend(response_json['items'])

    return items


def write_to_storage(playlist_name: str, items: List[Dict]) -> None:
    """Store the given items to the JSON file. If the JSON file does not yet exist, create a new file.
    If the JSON file exists, we update the contents with the new data.

    Args:
        playlist_name (str): name of the playlist that gets used as a key in the JSON file
        items (List[Dict]): a list of items that need to be stored in the JSON file
    """
    playlists_info = {}
    if os.path.exists(JSON_FILE_NAME):
        with open(JSON_FILE_NAME, 'r') as playlists_info_file:
            playlists_info = json.load(playlists_info_file)

    playlists_info[playlist_name] = items

    with open(JSON_FILE_NAME, 'w') as playlists_info_file:
        playlists_info_file.write(json.dumps(
            playlists_info, indent=4, sort_keys=True))


def playlist_url_to_id(playlist_url: str) -> str:
    """Convert a Spotify playlist URL into the playlist ID

    Args:
        playlist_url (str): Spotify playlist URL (e.g. https://open.spotify.com/playlist/7IwSRHmGNEd0dZSDx4XTUr?si=aqgG4feLSbaG106O88G3AA)

    Raises:
        Exception: Raise Exception if the given URL could not be parsed

    Returns:
        str: Spotify playlist ID
    """
    if 'https://open.spotify.com/playlist/' not in playlist_url or '?' not in playlist_url:
        raise Exception('Could not parse the given playlist URL')
    result = playlist_url.replace('https://open.spotify.com/playlist/', '')
    return result[:result.index('?')]


if __name__ == '__main__':
    print('Exit program with CTRL+C')
    while True:
        handle_playlist(input('Spotify playlist URL: '))
