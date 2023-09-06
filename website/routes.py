from flask import Blueprint, render_template, request, session, redirect
from website import get_token, search_for_artist, get_auth_header, get_albums_by_artist, get_songs_from_album
from dotenv import load_dotenv
import os
import base64
import requests


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
token = get_token()

# URLs
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = "http://localhost:5000/callback"

SCOPES = 'user-library-read'

home = Blueprint("home", __name__)

    
@home.route("/")
def home_blueprint():
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    return render_template("index.html", hi=auth_url)


@home.route('/callback')
def callback():
    code = request.args.get('code')
    
    # Exchange the authorization code for an access token
    token_data = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
    }
    
    response = requests.post(TOKEN_URL, data=token_data, headers=headers)
    token_info = response.json()
    
    # Store the token info in the session or a database
    session["token_info"] = token_info
    
    return redirect("/search.html")

# ensure user is logged in before performing any queries
def is_logged_in():
    if session.get("token_info"):
        return True

@home.route("/search.html")
def search():
    if not is_logged_in():
        return redirect("/")

    global artist_search
    artist_search = request.args.get('artist_search')
    if artist_search and search_for_artist(token, artist_search):
        return redirect("/artists.html")
    
    return render_template("search.html")

@home.route("/artists.html")
def artists_blueprint():
    if not is_logged_in():
        return redirect("/")
    
    global artist_id
    artist_id = request.args.get('artist_id')
    if artist_id:
        return redirect("/songs.html")
    
    artist = search_for_artist(token, artist_search)
    return render_template("artists.html", hello=artist)

@home.route("/songs.html")
def songs_blueprint():
    albums = get_albums_by_artist(token, artist_id)
    return render_template("songs.html", hello=albums)

@home.route('/api_request')
def api_request():
    # get access token from session
    token_info = session.get('token_info')
    access_token = token_info.get('access_token')
    
    headers = get_auth_header(access_token)
    
    # Example API request to get a user's saved tracks
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    data = response.json()
    
    return f"<p>{data}</p>"