from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from .exts import db, mail, api, socketio
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Resource
from .blueprints import user_bp, admin_bp, session_bp
from flask_cors import CORS
import logging.config
from logging.handlers import TimedRotatingFileHandler
handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "info.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8",
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "debug.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "my_module": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "debug_file_handler"],
        },
    }
)
app = Flask(__name__)
handler = logging.FileHandler('flask.log')
app.logger.addHandler(handler)
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
