from flask import Flask
from .spotify_artist import get_auth_header, search_for_artist, get_albums_by_artist, get_songs_from_album, artist_name, create_playlist, populate_playlist

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "aksjndf ;alsdaon"
    
    from .routes import home
    
    app.register_blueprint(home, url_prefix="/")
    
    return app