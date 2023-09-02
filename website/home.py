from flask import Blueprint, render_template
import spotify_api

home = Blueprint("home", __name__)

@home.route("/")
def home():
    token = spotify_api.get_token()
    artist = spotify_api.search_for_artist(token, "keshi")
    hi = artist["href"]
    return render_template("index.html")