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
        self.user_playlists = self.getAndStoreUserPlaylists()

    def getUserProfile(self):
        return json.loads(requests.get('https://api.spotify.com/v1/me', headers=self.createHeaders()).content)

    def getAndStoreUserPlaylists(self) -> List[Dict]:
        """Return a list containing information for all the playlists for the user. The format is like this:
        [
            {
                "description": "",
                "name": "Wednesday after your exam",
                "public": true,
                "uri": "spotify:playlist:1XTokSfNKiPkn2isbRHMJx",
                "tracks": [
                    {
                        "uri": "spotify:track:02MWAaffLxlfxAUY7c5dvx",
                        "name": "Heat Waves",
                        "artists": [
                            "Glass Animals"
                        ]
                    },
                    ...
                ]
            },
            ...
        ]

        Returns:
            List[Dict]: list containing information for all the playlists for the user
        """
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

        result = []

        for i in items:
            parsedEntry = self.parsePlaylistEntry(i)
            if parsedEntry is not None:
                result.append(parsedEntry)

        return result

    def parsePlaylistEntry(self, playlist: Dict):
        """Extract the necessary information from the given playlist entry. Also get the actual data for the tracks.
        If the playlist is not owned by the current user, return None.

        Args:
            playlist (Dict): unparsed playlist entry

        Returns:
            Dict: parsed playlist entry
        """
        if playlist['owner']['id'] != self.user_id:
            return None
        result = {}
        result['description'] = playlist['description']
        result['name'] = playlist['name']
        result['public'] = playlist['public']
        result['uri'] = playlist['uri']
        result['tracks'] = self.getTracksInPlaylist(
            playlist['tracks']['href'])
        return result

    def getTracksInPlaylist(self, api_playlist_url: str) -> List[Dict]:
        """Get track data from the tracks in the given playlist

        Args:
            api_playlist_url (str): API URL for a Spotify playlist

        Returns:
            List[Dict]: list of track data such as URI, name and artist
        """
        api_playlist_url

        items = []

        playlist_response = requests.get(
            api_playlist_url, headers=self.createHeaders())
        response_json = json.loads(playlist_response.content)
        items.extend(response_json['items'])

        while response_json['next'] is not None:
            playlist_response = requests.get(
                response_json['next'], headers=self.createHeaders())
            response_json = json.loads(playlist_response.content)
            items.extend(response_json['items'])

        result = []
        for i in items:
            # Do not store local songs (e.g. spotify:local:::blabla:182)
            if 'track' in i['track']['uri']:
                result.append(
                    {
                        'uri': i['track']['uri'],
                        'name': i['track']['name'],
                        'artists': [a['name'] for a in i['track']['artists']]
                    }
                )

        return result

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
            result.append((item['name'], len(item['tracks'])))
        return result

    def getUserPlaylists(self):
        return self.user_playlists
