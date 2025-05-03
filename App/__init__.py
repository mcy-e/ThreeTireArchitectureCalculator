from flask import Flask, send_from_directory
from .routes import bp
import os

def create_app():
    app = Flask(__name__, static_folder='../static')
    
    app.register_blueprint(bp)
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    return app