// Get access token from the hash query parameters and send them to the server
(function () {
    var access_token_key = '#access_token=';

    var sliced = window.location.hash.slice(window.location.hash.indexOf(access_token_key) + access_token_key.length);
    var access_token = sliced.slice(0, sliced.indexOf('&'));

    var jsonToSend = {
        'access_token': access_token
    };

    // Send access token to server
    $.ajax('http://localhost:8080/post_access_token', {
        data: JSON.stringify(jsonToSend),
        contentType: 'application/json',
        type: 'POST'
    });
})();