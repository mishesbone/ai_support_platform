# ai_support_platform/app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from logging.config import dictConfig

# Initialize extensions
db = SQLAlchemy()
socketio = SocketIO()
jwt = JWTManager()
migrate = Migrate()

# Function for logging setup (optional)
def setup_logging():
    """
    Configures logging for the application.
    Logs to a file and prints to console for easy debugging.
    """
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            }
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'default',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'flask.app': {
                'level': 'DEBUG',
                'handlers': ['file', 'console'],
            },
        }
    })
from flask import Flask
from app.routes import chat, call, ticket, crm, auth, dashboard

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    # Register Blueprints with their respective URL prefixes
    app.register_blueprint(chat, url_prefix="/api/chat")
    app.register_blueprint(call, url_prefix="/api/call")
    app.register_blueprint(ticket, url_prefix="/api/ticket")
    app.register_blueprint(crm, url_prefix="/api/crm")
    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(dashboard, url_prefix="/api/dashboard")

    # Other app setup code, like database initialization, error handling, etc.

    return app
