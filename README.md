# About
The purpose of this program is to store information of Spotify playlists to a JSON file so that you can later restore this data to create playlists (possibly on another account).

# Requirements
## Spotify
To interact with the Spotify API, you need a client_id and client_secret. This can be found on the Spotify developers dashboard after creating an application: https://developer.spotify.com/dashboard/applications. The client_id and client_secret need to be added to the `config.json` file in the root folder like this, where you have to replace the values:
```json
{
    "spotify": {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET"
    }
}
```
More information about the authorization can be found [here](https://developer.spotify.com/documentation/general/guides/authorization-guide/).

## Python libraries
The only library that is required is `requests` which can be installed with pip by typing in the terminal:
```bash
pip install requests
```

# How it works
After reading the requirements, you can run the program from the terminal (depending on your operating system):
```python
python3 spotify_to_json.py
```

The program will then ask to enter the Spotify URL for the playlist you want to create a backup for. The results will be stored in a JSON file called `playlist_info.json`.

To stop the program, press `CTRL+C` in the terminal.

# Development
## Explanation Spotify authorization
When a client goes to `/login`, he gets prompted with the `login.html` page from [this example](https://github.com/spotify/web-api-auth-examples/blob/master/implicit_grant/templates/index.html). Before the login button works, the client first has to get the client ID from this registered Spotify application (found in the `config.json` file). This client ID is passed to the login.html file via Jinja syntax ({{}}).

After pressing the login button, the client is redirected to the Spotify login page where he has to login. When pressing login on the official Spotify login page, Spotify redirects the user to our `/login` page. Spotify also appends a hash fragment with data encoded as a query string (e.g. `/login#access_token=blabla&token_type=Bearer&expires_in=3600`). Our server CANNOT read these parameters after the #, only the client can see these. The file `login.js` then extracts the access token from the hash fragment and makes a GET request with as query parameter this access token to our server.

We need to be able to receive the playlists of the user and also be able to edit these playlists. We can ask for permission by using a scope, explained [here](https://developer.spotify.com/documentation/general/guides/authorization/scopes/). These scopes are set in the server and sent to client side. The scopes we need are:
- user-read-private: to get the current user ID
- user-read-email: to get user information, which is needed to get the user ID
- playlist-modify-private: to create and modify user private playlists
- playlist-read-private: to get the playlists of the current user
- playlist-modify-public: to create and modify user public playlists

At this point our server has the access token of the logged-in client and can make further requests such as creating a playlist etc.

NOTE: if new users want to use this program, they need to be given access to the application in the Spotify dashboard