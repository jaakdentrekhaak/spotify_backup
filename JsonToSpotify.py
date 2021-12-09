import json
from typing import Dict, List
import requests


class JsonToSpotify():
    access_token = None
    user_id = None
    user_name = None

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        temp = self.getUserProfile()
        self.user_id = temp['id']
        self.user_name = temp['display_name']

    def getUserProfile(self):
        return json.loads(requests.get('https://api.spotify.com/v1/me', headers=self.createHeaders()).content)

    def createHeaders(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

    def createPlaylists(self, playlists: List[Dict]):
        for playlist in playlists:
            new_playlist_href = self.createPlaylist(
                playlist['name'], playlist['description'], playlist['public'])
            self.addTracksToPlaylist(playlist['tracks'], new_playlist_href)

    def createPlaylist(self, name: str, description: str, public: bool) -> str:
        """Send a POST request to Spotify API to create a playlist with the given parameters.
        Return the href of the created playlist.

        Args:
            name (str): name of playlist
            description (str): description of playlist
            public (bool): whether the playlist should be public

        Returns:
            str: href of the created playlist
        """
        url = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'
        data = {
            'name': name,
            'description': description,
            'public': public
        }
        res = requests.post(url, json=data, headers=self.createHeaders())

    def addTracksToPlaylist(self, tracks: List[Dict], playlist_href: str):
        trackURIs = [t['uri'] for t in tracks]
        chunks = [trackURIs[x:x+50] for x in range(0, len(trackURIs), 50)]
        for chunk in chunks:
            requests.post(playlist_href, json={
                'uris': chunk}, headers=self.createHeaders())

    def getUserName(self):
        return self.user_name

    def getUserId(self):
        return self.user_id
