document.getElementById('button_generate_json-button').addEventListener('click', function () {
    document.getElementById('error_url').hidden = true;

    const spotifyPlaylistUrl = document.getElementById('input_spotify_playlist_url');

    if (!spotifyPlaylistUrl.contains('https://open.spotify.com/playlist/') || !spotifyPlaylistUrl.contains('?')) {
        document.getElementById('error_url').hidden = false;
        return;
    }

    var jsonToSend = {
        'playlist_url': spotifyPlaylistUrl
    };

    // Send playlist url to server
    $.ajax('http://localhost:5000/handle_playlist_url', {
        data: JSON.stringify(jsonToSend),
        contentType: 'application/json',
        type: 'POST'
    });
}, false);