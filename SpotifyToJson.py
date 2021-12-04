import json
from typing import Dict, List
import requests


class SpotifyToJson:
    access_token = None
    user_id = None
    user_name = None
    user_playlists = None

    def __init__(self, access_token) -> None:
        self.access_token = access_token
        temp = self.getUserProfile()
        self.user_id = temp['id']
        self.user_name = temp['display_name']
        self.user_playlists = self.getUserPlaylists()

    def getUserProfile(self):
        return json.loads(requests.get('https://api.spotify.com/v1/me', headers=self.createHeaders()).content)

    def getUserPlaylists(self):
        items = []

        playlist_response = requests.get(
            'https://api.spotify.com/v1/me/playlists', headers=self.createHeaders())
        response_json = json.loads(playlist_response.content)
        items.extend(response_json['items'])

        while response_json['next'] is not None:
            playlist_response = requests.get(
                response_json['next'], headers=self.createHeaders())
            response_json = json.loads(playlist_response.content)
            items.extend(response_json['items'])

        return items

    def getOutputJson(self, playlist_indices: List[str]):
        playlists_to_parse = []
        for i in playlist_indices:
            playlists_to_parse.append(self.user_playlists[int(i)])
        # TODO: parse list to store as JSON file

    def createHeaders(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

    def getUserName(self):
        return self.user_name

    def getUserId(self):
        return self.user_id

    def getUserPlaylistsNamesAndSizes(self):
        result = []
        for item in self.user_playlists:
            result.append((item['name'], item['tracks']['total']))
        return result
