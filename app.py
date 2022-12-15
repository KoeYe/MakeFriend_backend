from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from exts import db, mail, api, socketio
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Resource
from blueprints import user_bp, admin_bp, session_bp, group_bp
from flask_cors import CORS
import logging.config
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

app.config.from_object('config')

handler = TimedRotatingFileHandler(
        "./logs/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)

handler = logging.FileHandler('./logs/flask.log')
app.logger.addHandler(handler)
formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]"
)
handler.setFormatter(formatter)


api.init_app(app)
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
app.register_blueprint(group_bp)
