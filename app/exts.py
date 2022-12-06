from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_restful import Api
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins='*')
db = SQLAlchemy()
mail = Mail()
api = Api()