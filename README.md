# About
The purpose of this program is to store information of Spotify playlists to a JSON file so that you can later restore this data to create playlists (possibly on another account).

# Requirements
## Spotify
To interact with the Spotify API, you need a client_id for a registrated Spotify application. This can be found on the Spotify developers dashboard after creating an application: https://developer.spotify.com/dashboard/applications. The client_id needs to be added to the `config.json` file in the root folder like this, where you have to replace the values:
```json
{
    "spotify": {
        "client_id": "YOUR_CLIENT_ID"
    }
}
```
More information about the authorization can be found [here](https://developer.spotify.com/documentation/general/guides/authorization-guide/).

## Python libraries
The only libraries that are required are `requests` and `flask` which can be installed with pip by typing in the terminal:
```bash
pip install requests
pip install Flask
```

# How it works
The program creates a local webserver on http://localhost:5000. You can start this webserver by opening a terminal in the root directory of this project and typing `python3 server.py`. Once this server is running, you can connect to that URL with your browser. Upon opening that webpage, you will be asked to login to Spotify and accept to give the permissions for reading, creating and modifying playlists to this application.

On the front page you can choose whether you want to convert your Spotify playlists into a JSON file or create Spotify playlists from a previously generated JSON file. If you press the "Spotify to JSON"-button, the webserver will ask all the information about your playlists to the Spotify servers, this can take a minute. Once the information is received, you will receive a webpage in your browser where the name of all your Spotify playlists and the number of tracks in those playlists will be displayed. You can then choose which playlists you want to save to a JSON file. When you checked all the playlists you want to convert, you press the "Convert"-button. The webserver will then return a downloadable JSON file which you can download and store on your computer. This JSON file contains information about all your selected playlists such as the name and description of the playlist, the tracks inside each playlist and also the names and artists for each track (so you can also use this JSON on other streaming platforms if Spotify doesn't exist anymore).

If you press the "JSON to Spotify"-button, you will see a page where you can upload your JSON file from your computer. If you press the "Create playlists"-button, the webserver will create the playlists inside the JSON file and add all the tracks to these playlists.

# Development
## Explanation Spotify authorization
When a client goes to `/login`, he gets prompted with the `login.html` page from [this example](https://github.com/spotify/web-api-auth-examples/blob/master/implicit_grant/templates/index.html). Before the login button works, the client first has to get the client ID from this registered Spotify application (found in the `config.json` file). This client ID is passed to the login.html file via Jinja syntax ({{}}).

The client is redirected to the Spotify login page where he has to login. When pressing login on the official Spotify login page, Spotify redirects the user to our `/login` page. Spotify also appends a hash fragment with data encoded as a query string (e.g. `/login#access_token=blabla&token_type=Bearer&expires_in=3600`). Our server CANNOT read these parameters after the #, only the client can see these. The file `login.js` then extracts the access token from the hash fragment and makes a GET request with as query parameter this access token to our server. This access token gets temporarily stored on our server.

We need to be able to receive the playlists of the user and also be able to edit these playlists. We can ask for permission by using a scope, explained [here](https://developer.spotify.com/documentation/general/guides/authorization/scopes/). These scopes are set in the server and sent to client side. The scopes we need are:
- user-read-private: to get the current user ID
- user-read-email: to get user information, which is needed to get the user ID
- playlist-modify-private: to create and modify user private playlists
- playlist-read-private: to get the playlists of the current user
- playlist-modify-public: to create and modify user public playlists

At this point our server has the access token of the logged-in client and can make further requests such as reading and creating playlists.

NOTE: if new users want to use this program, they need to be given access to the application in the Spotify dashboard, unless they create their own Spotify application on https://developer.spotify.com/dashboard/applications