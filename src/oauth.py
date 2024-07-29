import webbrowser
from requests_oauthlib import OAuth2Session
from flask import Flask, request
import os
import json
from oauthlib.oauth2 import BackendApplicationClient, WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError

app = Flask(__name__)
client_id = '5ee9b18608f470b3506e0eacfb27331449fbdff77a703bb8d6d74bf777c91fcb'
client_secret = 'c75597cff77c007c9aabe6dad3c0d60a3ef058446d14d6b388ae208d64aeddae'
redirect_uri = 'http://localhost:8080/callback'  # Assicurati che questo URI corrisponda a quello configurato su TRAKT
authorization_base_url = 'https://api.trakt.tv/oauth/authorize'
token_url = 'https://api.trakt.tv/oauth/token'
token_file = 'token.json'

def save_token(token):
    with open(token_file, 'w') as f:
        json.dump(token, f)

def load_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return json.load(f)
    return None

@app.route('/callback')
def callback():
    global token
    try:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Disabilita il controllo HTTPS solo per lo sviluppo locale
        trakt = OAuth2Session(client_id, redirect_uri=redirect_uri)
        token = trakt.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)
        save_token(token)
        return "Autenticazione completata! Puoi chiudere questa finestra."
    except InsecureTransportError as e:
        return f"Error: {e}"

def authenticate_trakt():
    token = load_token()
    if not token:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Disabilita il controllo HTTPS solo per lo sviluppo locale
        trakt = OAuth2Session(client_id, redirect_uri=redirect_uri)
        authorization_url, state = trakt.authorization_url(authorization_base_url)
        webbrowser.open(authorization_url)
        from waitress import serve
        serve(app, host='localhost', port=8080)
        token = load_token()
    return token

def refresh_token():
    token = load_token()
    if token and 'refresh_token' in token:
        extra = {
            'client_id': client_id,
            'client_secret': client_secret,
        }
        trakt = OAuth2Session(client_id, token=token)
        new_token = trakt.refresh_token(token_url, **extra)
        save_token(new_token)
        return new_token
    return None

if __name__ == '__main__':
    authenticate_trakt()
