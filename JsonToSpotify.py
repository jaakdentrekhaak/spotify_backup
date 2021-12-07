import json
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

    def getUserName(self):
        return self.user_name

    def getUserId(self):
        return self.user_id
