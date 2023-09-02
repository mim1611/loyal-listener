from flask import Flask
import spotify_api

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "aksjndf ;alsdaon"
    
    from .home import home
    
    app.register_blueprint(home, url_prefix="/")
    
    return app