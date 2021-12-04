from flask import Flask, redirect, url_for, render_template, request
import json
import requests

app = Flask(__name__)
logged_in = False
access_token = None
scope = 'user-read-private user-read-email playlist-modify-private playlist-read-private playlist-modify-public'


@app.route('/')
def home():
    global logged_in, access_token
    access_token = request.args.get('access_token')
    if access_token is not None:
        # Assumes that the access_token is valid
        logged_in = True
    if not logged_in:
        return redirect(url_for('login'))
    else:
        print('[SERVER] Login succeeded')
        user_profile = getUserProfile()
        user_name = user_profile['display_name']
        user_id = user_profile['id']
        user_playlists = getUserPlaylists()
        # TODO: get playlist name, href or id and then get all tracks from this playlist
        return render_template('index.html')


@app.route('/login')
def login():
    global scope
    return render_template('login.html', client_id=getClientId(), scope=scope)


def getClientId():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['spotify']['client_id']


def getUserProfile():
    return json.loads(requests.get('https://api.spotify.com/v1/me', headers=createHeaders()).content)


def getUserPlaylists():
    items = []

    playlist_response = requests.get(
        'https://api.spotify.com/v1/me/playlists', headers=createHeaders())
    response_json = json.loads(playlist_response.content)
    items.extend(response_json['items'])

    while response_json['next'] is not None:
        playlist_response = requests.get(
            response_json['next'], headers=createHeaders())
        response_json = json.loads(playlist_response.content)
        items.extend(response_json['items'])

    return items


def createHeaders():
    global access_token
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }


if __name__ == '__main__':
    app.run()
