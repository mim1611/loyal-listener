from flask import Blueprint, render_template, request, redirect, session
from website import get_token, search_for_artist
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import requests

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

# Authorization URL
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Scopes
SCOPES = 'user-library-read'

home = Blueprint("home", __name__)

@home.route("/")
def home_blueprint():
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    return redirect(auth_url)


@home.route("/songs.html")
def songs_blueprint():
    token = get_token()
    artist = search_for_artist(token, "keshi")
    hi = artist
    return render_template("songs.html", hello=hi)

@home.route('/callback')
def callback():
    code = request.args.get('code')
    
    # Exchange the authorization code for an access token
    token_data = {
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode(),
    }
    
    response = requests.post(TOKEN_URL, data=token_data, headers=headers)
    token_info = response.json()
    
    # Store the token info in the session or a database
    session['token_info'] = token_info
    
    return 'Authenticated! You can now make API requests.'

@home.route('/api_request')
def api_request():
    # Retrieve the access token from the session or your database
    token_info = session.get('token_info')
    access_token = token_info.get('access_token')
    
    # Make API requests using the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    # Example API request to get a user's saved tracks
    response = requests.get('https://api.spotify.com/v1/me/tracks', headers=headers)
    data = response.json()
    
    return data