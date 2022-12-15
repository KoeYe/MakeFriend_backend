from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
app = Flask(__name__)

class Config(object):
    """配置参数"""
    # 设置sqlalchemy自动跟踪数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Test.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    app.config['SECRET_KEY'] = 'secret_key'

app.config.from_object(Config)

db = SQLAlchemy(app)

class UserModel(db.Model):
    '''用户表'''
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    register_datetime = db.Column(db.DateTime, default=datetime.now)
    state = db.Column(db.Boolean, default=False)
    friends_id = db.Column(db.Integer, db.ForeignKey('friend.id'))
    address = db.Column(db.String(200), default="Nowhere")
    remarks= db.Column(db.Integer, default="0")
    place = db.Column(db.String(200), default="Secret")
    tel = db.Column(db.String(200), default="(+86)888 8888 8888")
    # friends = db.relationship('FriendListModel', backref='user', uselist=True, foreign_keys=[friends_id])

class FriendListModel(db.Model):
    '''好友表'''
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    # session = db.relationship('SessionModel', backref='friend', uselist=True, foreign_keys=[session_id])

class SessionModel(db.Model):
    '''会话表'''
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer)
    user2_id = db.Column(db.Integer)
    # message_history = db.relationship('MessageModel', backref='session', uselist=True)

class MessageModel(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    content = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    year = db.Column(db.Integer)
    month= db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    min = db.Column(db.Integer)
    sec = db.Column(db.Integer)
    state = db.Column(db.Integer)
    url = db.Column(db.String(200))
    type = db.Column(db.String(20))
    filename = db.Column(db.String(200))

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class GroupModel(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

class GroupMemberModel(db.Model):
    __tablename__ = "group_member"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

class GroupMessageModel(db.Model):
    __tablename__ = "group_message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(200))
    year = db.Column(db.Integer)
    month= db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    min = db.Column(db.Integer)
    sec = db.Column(db.Integer)
    state = db.Column(db.Integer)
    url = db.Column(db.String(200))
    type = db.Column(db.String(20))
    filename = db.Column(db.String(200))
