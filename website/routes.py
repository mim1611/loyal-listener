from flask import Blueprint, render_template, request, session, redirect
from website import search_for_artist, get_auth_header, get_albums_by_artist, get_songs_from_album, artist_name, create_playlist, populate_playlist
from dotenv import load_dotenv
import os
import base64
import requests
import json


load_dotenv()


# global variables for sending api requests
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# token = get_token()

# urls
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = "http://localhost:5000/callback"

SCOPES = "user-library-read"
HI = "playlist-modify-public"

home = Blueprint("home", __name__)


# ensure user is logged in before performing any queries
def is_logged_in():
    if session.get("token_info"):
        return True
    
def get_user_id():
    token_info = session.get("token_info")
    global access_token
    access_token = token_info.get("access_token")
    headers = get_auth_header(access_token)
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    response_json = json.loads(response.content)
    return response_json["id"]
    
@home.route("/")
def home_blueprint():
    # redirect to search page if already logged in
    if is_logged_in():
        return redirect("/search.html")
    
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES},{HI}"
    return render_template("index.html", auth_url=auth_url)

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

@home.route("/search.html")
def search():
    if not is_logged_in():
        return redirect("/")
    
    global user_id
    user_id = get_user_id()

    global artist_search
    artist_search = request.args.get('artist_search')
    if artist_search and search_for_artist(access_token, artist_search):
        return redirect("/artists.html")
    
    return render_template("search.html")

@home.route("/artists.html")
def artists_blueprint():
    if not is_logged_in():
        return redirect("/")
    
    global artist_id
    artist_id = request.args.get("artist_id")
    
    artist = search_for_artist(access_token, artist_search)
    
    if artist_id:
        global playlist_name
        playlist_name = artist_name(access_token, artist_id)
        return redirect("/songs.html")
    
    artists = search_for_artist(access_token, artist_search)
    return render_template("artists.html", artists=artists)

@home.route("/songs.html", methods=["GET", "POST"])
def songs_blueprint():
    albums = get_albums_by_artist(access_token, artist_id)
    global songs
    songs = []
    global uri_list
    uri_list = []
    for item in albums:
        album_songs = get_songs_from_album(access_token, item["id"])
        for song in album_songs:
            uri_list.append(song["uri"])
            songs.append(song)

    new_playlist = create_playlist(access_token, user_id, playlist_name)
    populate_playlist(access_token, new_playlist["id"], uri_list)
    
    return render_template("songs.html")