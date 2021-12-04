from flask import Flask, redirect, url_for, render_template, request
import json

app = Flask(__name__)
logged_in = False
access_token = None


@app.route('/')
def home():
    global logged_in, access_token
    access_token = request.args.get('access_token')
    if access_token is not None:
        # Assumes that the access_token is valid
        logged_in = True
    if not logged_in:
        return redirect(url_for('login'))
    else:
        print('[SERVER] Login succeeded')
        return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html', client_id=getClientId())


def getClientId():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['spotify']['client_id']


if __name__ == '__main__':
    app.run()
