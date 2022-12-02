import random
from datetime import datetime
from this import s
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_mail import Message
from app.blueprints.admin import show_all_user
from app.blueprints.forms import LoginForm, RegisterForm
from flask_restful import Resource, Api
import string
from app import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from app.models import EmailCaptchaModel, UserModel, SessionModel

# 注册了一个bp，名字叫user，前置路径是/user
bp = Blueprint("session", __name__, url_prefix="/session")
# 将bp挂载到api上
api = Api(bp)

class SetSession(Resource):
    def post(self):
        user1_id = request.json.get('user1_id') #user_1是对面的
        user2_id = request.json.get('user2_id') #user_2是自己
        print(user1_id, user2_id)
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

api.add_resource(SetSession, "/session")