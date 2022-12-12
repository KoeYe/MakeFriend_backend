from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from .exts import db, mail, api, socketio
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Resource
from .blueprints import user_bp, admin_bp, session_bp
from flask_cors import CORS

app = Flask(__name__)

api.init_app(app)
app.config.from_object('config')
# cors is not available in this version, because it is not compatible with Nginx
# CORS(app, supports_credentials=True)
db.init_app(app)

migrate = Migrate(app, db)

mail.init_app(app)
# socketio is not available in this version
# socketio.init_app(app)

# mount bp into app
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(session_bp)

from app import views, models
