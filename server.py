from flask import Flask, redirect, url_for, render_template, request, Response
import json
from JsonToSpotify import JsonToSpotify
from SpotifyToJson import SpotifyToJson

app = Flask(__name__)
logged_in = False
access_token = None
spotify_to_json: SpotifyToJson = None
json_to_spotify: JsonToSpotify = None


@app.route('/')
def home():
    global logged_in, access_token
    if access_token is None:
        access_token = request.args.get('access_token')
        if access_token is None:
            return redirect(url_for('login'))
        else:
            logged_in = True
    return render_template('index.html')


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-modify-private playlist-read-private playlist-modify-public'
    return render_template('login.html', client_id=getClientId(), scope=scope)


@app.route('/spotifytojson', methods=['GET', 'POST'])
def spotify_to_json_method():
    global logged_in, access_token, spotify_to_json
    if not logged_in:
        return redirect(url_for('login'))
    if spotify_to_json is None:
        spotify_to_json = SpotifyToJson(access_token)
    if request.method == 'GET':
        user_name = spotify_to_json.getUserName()
        user_playlist_names_and_sizes = spotify_to_json.getUserPlaylistsNamesAndSizes()
        return render_template('spotifytojson.html', user_name=user_name, user_playlist_names_and_sizes=user_playlist_names_and_sizes)

    else:
        # Returns dictionary that says which playlists have been selected for converting e.g. {'0': 'on'}
        # (Does not say which playlists have NOT been selected)
        user_playlists = spotify_to_json.getUserPlaylists()
        result = []
        for k in request.form.to_dict().keys():
            result.append(user_playlists[int(k)])
        content = json.dumps(result)
        return Response(
            content,
            mimetype='application/json',
            headers={
                'Content-Disposition': 'attachment;filename=spotify_playlist_backup.json'
            }
        )


@app.route('/jsontospotify', methods=['GET', 'POST'])
def json_to_spotify_method():
    global logged_in, access_token, json_to_spotify
    if not logged_in:
        return redirect(url_for('login'))

    if json_to_spotify is None:
        json_to_spotify = JsonToSpotify(access_token)

    if request.method == 'GET':
        user_name = json_to_spotify.getUserName()
        return render_template('jsontospotify.html', user_name=user_name)
    else:
        json_to_spotify.createPlaylists(request.get_json())
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def getClientId():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['spotify']['client_id']


if __name__ == '__main__':
    app.run()
