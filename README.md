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
python3 main.py
```

The program will then ask to enter the Spotify URL for the playlist you want to create a backup for. The results will be stored in a JSON file called `playlist_info.json`.

To stop the program, press `CTRL+C` in the terminal.

NOTE: the program currently only works if your playlists are public.

# Development
## TODO
- remove redundant information from JSON file
- make GUI
- create playlists given