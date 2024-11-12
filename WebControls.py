from flask import Flask, render_template, request, redirect, url_for
import urllib.parse
import requests
import pickle
import subprocess
import os

app = Flask(__name__)

client_id = 'INSERT CLIENT ID'
client_secret = 'INSERT CLIENT SECRET'
redirect_uri = 'INSERT REDIRECT URI'
scope = 'user-read-currently-playing user-top-read'

# File to store process ID
pid_file = 'spotipi.pid'

def generate_auth_url():
    auth_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(
        {
            'response_type': 'code',
            'client_id': client_id,
            'scope': scope,
            'redirect_uri': redirect_uri,
        })
    return auth_url

def parse_token_url(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    code = query_params.get('code', [None])[0]

    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)
    response_data = response.json()

    access_token = response_data.get('access_token')
    refresh_token = response_data.get('refresh_token')
    if access_token and refresh_token:
        store_tokens(access_token, refresh_token)
        print("Tokens stored successfully.")
    else:
        print("Failed to get tokens. Please try again.")

def store_tokens(access_token, refresh_token):
    tokens = {'access_token': access_token, 'refresh_token': refresh_token}
    with open('tokens.pkl', 'wb') as file:
        pickle.dump(tokens, file)

def start_spotipi_script():
    if os.path.exists(pid_file):
        print("Script is already running.")
        return

    script_path = 'INSERT_MAIN_PROGRAM_PATH.py'
    process = subprocess.Popen(['python3', script_path])
    with open(pid_file, 'w') as f:
        f.write(str(process.pid))

def stop_spotipi_script():
    if not os.path.exists(pid_file):
        print("No running script to stop.")
        return

    with open(pid_file, 'r') as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, subprocess.signal.SIGTERM)
        print("Script stopped successfully.")
    except ProcessLookupError:
        print("Process not found.")

    os.remove(pid_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'start':
            start_spotipi_script()
        elif action == 'stop':
            stop_spotipi_script()
        else:
            redirect_url = request.form.get('redirect_url')
            parse_token_url(redirect_url)
            return redirect(url_for('index'))

    auth_url = generate_auth_url()
    return render_template('index.html', auth_url=auth_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
