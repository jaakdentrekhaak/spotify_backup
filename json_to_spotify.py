import requests
import json
from spotify_to_json import get_access_token


def create_playlist(user_id: str, name: str):
    api_create_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }

    body = {
        'name': name,
        'public': False,
    }

    res = requests.post(api_create_playlist_url, json=body, headers=headers)

    print(json.loads(res.content))


def add_tracks_to_playlist():
    pass


def login():
    with open('config.json', 'r') as config_file:
        config = json.loads(config_file)
        client_id = config['spotify']['client_id']
    response_type = 'token'
    redirect_uri = 'https://example.com/not_used'

    auth_url = 'https://accounts.spotify.com/authorize'
    auth_url += '?response_type=' + response_type
    auth_url += '&client_id=' + client_id
    auth_url += '&redirect_uri=' + redirect_uri

    res = requests.get(auth_url)

    print(res.content)


# create_playlist('jens.borlo', 'Testing...')

login()
