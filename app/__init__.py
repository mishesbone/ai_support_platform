from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
socketio = SocketIO()
jwt = JWTManager()

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    socketio.init_app(app)
    jwt.init_app(app)

    from app.routes import chat, call, ticket, crm, auth, dashboard
    app.register_blueprint(chat.bp, url_prefix="/api/chat")
    app.register_blueprint(call.bp, url_prefix="/api/call")
    app.register_blueprint(ticket.bp, url_prefix="/api/ticket")
    app.register_blueprint(crm.bp, url_prefix="/api/crm")
    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(dashboard.bp, url_prefix="/api/dashboard")

    return app
