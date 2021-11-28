(function () {

    var stateKey = 'spotify_auth_state';

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

    var userProfileSource = document.getElementById('user-profile-template').innerHTML,
        userProfileTemplate = Handlebars.compile(userProfileSource),
        userProfilePlaceholder = document.getElementById('user-profile');

    oauthSource = document.getElementById('oauth-template').innerHTML,
        oauthTemplate = Handlebars.compile(oauthSource),
        oauthPlaceholder = document.getElementById('oauth');

    var params = getHashParams();

    var access_token = params.access_token,
        state = params.state,
        storedState = localStorage.getItem(stateKey);

    if (access_token && (state == null || state !== storedState)) {
        alert('There was an error during the authentication');
    } else {
        localStorage.removeItem(stateKey);
        if (access_token) {
            $.ajax({
                url: 'https://api.spotify.com/v1/me',
                headers: {
                    'Authorization': 'Bearer ' + access_token
                },
                success: function (response) {
                    userProfilePlaceholder.innerHTML = userProfileTemplate(response);

                    $('#login').hide();
                    $('#loggedin').show();
                }
            });
        } else {
            $('#login').show();
            $('#loggedin').hide();
        }

        document.getElementById('login-button').addEventListener('click', function () {

            var client_id = null;
            // Ask application's client ID from server
            $.ajax({
                url: "http://localhost:8080/getclientid",
                type: "GET",
                dataType: 'text',
                success: function (res) {
                    client_id = res;
                },
                async: false
            });
            var redirect_uri = 'http://localhost:8080/callback'; // Your redirect uri

            localStorage.setItem(stateKey, state);
            var scope = 'user-read-private user-read-email';

            var url = 'https://accounts.spotify.com/authorize';
            url += '?response_type=token';
            url += '&client_id=' + encodeURIComponent(client_id);
            url += '&scope=' + encodeURIComponent(scope);
            url += '&redirect_uri=' + encodeURIComponent(redirect_uri);

            window.location = url;
        }, false);
    }
})();