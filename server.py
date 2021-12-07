from flask import Flask, redirect, url_for, render_template, request, Response
import json
from SpotifyToJson import SpotifyToJson

app = Flask(__name__)
logged_in = False
access_token = None
scope = 'user-read-private user-read-email playlist-modify-private playlist-read-private playlist-modify-public'
spotify_to_json: SpotifyToJson = None


# TODO: create Spotify playlist from JSON
# TODO: create frontpage where you have to choose if you want to do Spotify -> JSON or JSON -> Spotify and redirect buttons to different URLs
#   spotify to json is the current implementatino; json to spotify should not get the information of all the playlists of the user
@app.route('/')
def home():
    # TODO: should login when on main page (so before pressing the buttons to spotifytojson and jsontospotify!), but not do SpotifyToJson in this function
    # TODO: improve login logic: everything with access_token should be in this function
    #   The functions spotifytojson and jsontospotify should only have: if not logged_in -> redirect to login page
    return render_template('index.html')


@app.route('/login')
def login():
    # TODO: prompt login if spotifytojson button is pressed on home page instead of redirecting to login.html file
    global scope
    return render_template('login.html', client_id=getClientId(), scope=scope)


@app.route('/spotifytojson', methods=['GET', 'POST'])
def spotify_to_json_method():
    if request.method == 'GET':
        global logged_in, access_token, spotify_to_json
        access_token = request.args.get('access_token')
        if access_token is not None:
            # Assumes that the access_token is valid
            logged_in = True
            spotify_to_json = SpotifyToJson(access_token)
        if not logged_in:
            return redirect(url_for('login'))
        else:
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
    return render_template('jsontospotify.html')


def getClientId():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['spotify']['client_id']


if __name__ == '__main__':
    app.run()
