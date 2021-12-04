(function () {

    /**
     * Obtains parameters from the hash of the URL
     * @return Object
     */
    function getHashParams() {
        var hashParams = {};
        var e, r = /([^&;=]+)=?([^&;]*)/g,
            q = window.location.hash.substring(1);
        while (e = r.exec(q)) {
            hashParams[e[1]] = decodeURIComponent(e[2]);
        }
        return hashParams;
    }

    var params = getHashParams();

    var access_token = params.access_token;

    if (access_token) {
        // If we got the access token, send it to the server to log in
        window.location = 'http://localhost:5000?access_token=' + access_token
    } else {
        document.getElementById('login-button').addEventListener('click', function () {

            var redirect_uri = 'http://localhost:5000/login'; // Where we get access token as hash fragment parameter

            var scope = 'user-read-private user-read-email';

            var url = 'https://accounts.spotify.com/authorize';
            url += '?response_type=token';
            url += '&client_id=' + encodeURIComponent(client_id); // client_id set in login.html
            url += '&scope=' + encodeURIComponent(scope);
            url += '&redirect_uri=' + encodeURIComponent(redirect_uri);

            window.location = url;
        }, false);
    }
})();
