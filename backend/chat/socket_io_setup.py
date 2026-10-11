# setting up flask-socketIO 
from flask_socketio import SocketIO

socketio = SocketIO()

def register_socketio(app):
    socketio.init_app(app, cors_allowed_origins=app.config['FRONTEND_URL'])