from flask import Flask, send_from_directory
from .routes import bp
from .authentication import auth_bp
import os
import secrets
from config import Config
from .db import init_db

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)

    #* configure session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  
    
    init_db()

    #* Register blueprints
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    return app