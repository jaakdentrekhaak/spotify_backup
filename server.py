# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import spotify_to_json

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    logged_in = False
    access_token = None

    def do_GET(self):
        if self.path == '/':
            if self.logged_in:
                self.send_html('index.html')
            else:
                self.send_html('login.html')
        elif self.path == '/login':
            self.send_html('login.html')
        elif self.path == '/callback':
            self.send_html('callback.html')
        elif self.path == '/getclientid':
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                client_id = config['spotify']['client_id']
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes(client_id, 'utf-8'))
        else:
            self.send_response(404)

    def do_POST(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        if self.path == '/post_access_token':
            # Receive access token from callback.html
            # read the message and convert it into a python dictionary
            length = int(self.headers.get('content-length'))
            message = json.loads(self.rfile.read(length))

            self.access_token = message['access_token']

            self.logged_in = True

            # send the message back
            self.send_response(200)

        elif self.path == 'handle_playlist_url':
            # Convert Spotify URL to JSON file
            length = int(self.headers.get('content-length'))
            message = json.loads(self.rfile.read(length))
            spotify_to_json.handle_playlist(message['playlist_url'])
            self.send_response(200)
        else:
            self.send_response(404)

    def send_html(self, filename):
        with open(f'./public/{filename}', 'r') as index_file:
            content = index_file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(content, 'utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
