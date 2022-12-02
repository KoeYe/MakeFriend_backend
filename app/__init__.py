from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from .exts import db, mail, api
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Resource
from .blueprints import user_bp, admin_bp, session_bp
from flask_cors import CORS

app = Flask(__name__)

class Test(Resource):
    def get(self):
        return 'test', 200

api.init_app(app)
api.add_resource(Test, '/test')

app.config.from_object('config')
CORS(app, supports_credentials=True)
db.init_app(app)

# manager = Manager(app)
migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)

mail.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(session_bp)

from app import views, models
