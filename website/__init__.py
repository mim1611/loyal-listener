from flask import Flask
from .spotify_api import get_token, get_auth_header, search_for_artist, get_songs_by_artist

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "aksjndf ;alsdaon"
    
    from .routes import home
    
    app.register_blueprint(home, url_prefix="/")
    
    return app