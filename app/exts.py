from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_restful import Api

db = SQLAlchemy()
mail = Mail()
api = Api()