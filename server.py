from flask import Flask, redirect, url_for, render_template, request
import json
from SpotifyToJson import SpotifyToJson

app = Flask(__name__)
logged_in = False
access_token = None
scope = 'user-read-private user-read-email playlist-modify-private playlist-read-private playlist-modify-public'
spotify_to_json = None


@app.route('/')
def home():
    global logged_in, access_token, spotify_to_json
    access_token = request.args.get('access_token')
    if access_token is not None:
        # Assumes that the access_token is valid
        logged_in = True
        spotify_to_json = SpotifyToJson(access_token)
    if not logged_in:
        return redirect(url_for('login'))
    else:
        print('[SERVER] Login succeeded')
        user_name = spotify_to_json.getUserName()
        user_playlist_names_and_sizes = spotify_to_json.getUserPlaylistsNamesAndSizes()
        print(user_name)
        print(user_playlist_names_and_sizes)
        return render_template('index.html')


@app.route('/login')
def login():
    global scope
    return render_template('login.html', client_id=getClientId(), scope=scope)


def getClientId():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['spotify']['client_id']


if __name__ == '__main__':
    app.run()
