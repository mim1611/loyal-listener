from flask import Blueprint, render_template
from website import get_token, search_for_artist

home = Blueprint("home", __name__)

@home.route("/")
def home_blueprint():
    token = get_token()
    artist = search_for_artist(token, "keshi")
    hi = artist
    return render_template("index.html", hello=hi)

@home.route("/songs")
def songs_blueprint():
    token = get_token()
    artist = search_for_artist(token, "keshi")
    hi = artist
    return render_template("songs.html", hello=hi)
    