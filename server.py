# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        if self.path == '/login':
            self.path = '/login.html'
        if self.path == '/callback':
            self.path = '/callback.html'
        if self.path == '/getclientid':
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                client_id = config['spotify']['client_id']
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes(client_id, 'utf-8'))
            return
        print(self.path)
        try:
            with open(f'./public/{self.path[1:]}', 'r') as index_file:
                content = index_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))
        except:
            self.send_response(404)

    def do_POST(self):
        # Receive access token from callback.html
        if self.path == '/post_access_token':
            print('POST RECEIVED')
            ctype, _ = cgi.parse_header(self.headers.get('content-type'))

            # refuse to receive non-json content
            if ctype != 'application/json':
                self.send_response(400)
                self.end_headers()
                return

            # read the message and convert it into a python dictionary
            length = int(self.headers.get('content-length'))
            message = json.loads(self.rfile.read(length))

            access_token = message['access_token']

            print('ACCESS TOKEN:', access_token)

            # send the message back
            self.send_response(200)

            # Show the page where playlist id has to be entered
        else:
            self.send_response(404)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
