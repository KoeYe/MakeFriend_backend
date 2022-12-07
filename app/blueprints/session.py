import random
from datetime import datetime
from this import s
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_mail import Message
from app.blueprints.admin import show_all_user
from app.blueprints.forms import LoginForm, RegisterForm
from flask_restful import Resource, Api
import string
from app import db, mail, socketio
from flask_socketio import emit
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from app.models import EmailCaptchaModel, UserModel, SessionModel, MessageModel

# 注册了一个bp，名字叫user，前置路径是/user
bp = Blueprint("session", __name__, url_prefix="/api/session")
# 将bp挂载到api上
api = Api(bp)

class SetSession(Resource):
    def post(self):
        user1_id = request.json.get('user1_id') #user_1是对面的
        user2_id = request.json.get('user2_id') #user_2是自己
        session = SessionModel.query.filter(or_(and_(SessionModel.user1_id==user1_id, SessionModel.user2_id==user2_id),and_(SessionModel.user1_id==user2_id,SessionModel.user2_id==user1_id))).first()
        if not session:
            session = SessionModel(
                user1_id = user1_id,
                user2_id = user2_id,
            )
            db.session.add(session)
            try:
                db.session.commit()
            except Exception as e:
                return e, 400
        session_id = session.id
        user1 = UserModel.query.filter(UserModel.id==user1_id).first()
        return jsonify({"session_id": session_id, "user1_name": user1.username})

    def get(self):
        session_id = request.values.get("session_id")
        # print(session_id)
        session_ = SessionModel.query.filter(SessionModel.id==session_id).first()
        user_id = request.values.get("user_id")
        print("[get]user_id ",user_id)
        print("[get]session_user1_id ",session_.user1_id)
        if str(user_id) == str(session_.user1_id):
            return jsonify({"session_id":session_.id, "user1_id": session_.user2_id, "user2_id":session_.user1_id})
        else:
            return jsonify({"session_id":session_.id, "user1_id": session_.user1_id, "user2_id":session_.user2_id})

class Message(Resource):
    def get(self):
        session_id = request.values.get("session_id")
        # session = SessionModel.query.filter(SessionModel.id==session_id)
        messages = MessageModel.query.filter(MessageModel.session_id==session_id).order_by(MessageModel.id).all()
        his_messages = []
        for message in messages:
            his_messages.append({"content": message.content,"user_id": message.user_id, "year": message.year, "month": message.month, "day": message.day, "hour": message.hour, "minute": message.min, "second": message.sec})
        if len(his_messages) > 50:
            for i in range(0, len(his_messages)-50):
                his_messages.pop(i)
        return jsonify({"messages":his_messages})

    def post(self):
        session_id = request.json.get("session_id")
        content = request.json.get("content")
        user_id = session.get("id")
        print(session.get("id"))
        dt= datetime.now()
        year=dt.year
        month=dt.month
        day=dt.day
        hour=dt.hour
        minute=dt.minute
        second=dt.second
        message = MessageModel(content=content, user_id=user_id, session_id=session_id,
                                year=year, month=month, day=day, hour=hour, min=minute, sec=second)
        try:
            db.session.add(message)
            db.session.commit()
            return "Send message successfully!", 200
        except Exception as e:
            return e, 400

api.add_resource(SetSession, "/session")
api.add_resource(Message, "/message")
