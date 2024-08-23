from flask import Flask
from flask_socketio import SocketIO
from .config import Config
from .socketio import MainNamespace
from . import db

socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask-SocketIO
    socketio.init_app(app)
    socketio.on_namespace(MainNamespace('/'))

    # Import and register blueprints or routes
    from . import lobby
    app.register_blueprint(lobby.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)
    
    db.init_app(app)

    return app