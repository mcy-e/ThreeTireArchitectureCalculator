from flask import Flask, send_from_directory
from flask_session import Session
from .routes import bp
from .authentication import auth_bp
import os
from config import Config
from .db import init_db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800
    Session(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    with app.app_context():
        init_db()
        db.create_all()

    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    @app.errorhandler(404)
    def not_found(error):
        return send_from_directory(app.static_folder, 'index.html')
    
    return app