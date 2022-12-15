#-----------------------------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 15:00
# @Author  : Prosperous
# @File    : views.py
# @Software: VSCode
# @Description: this file is about the views
# @Version: 1.0
#-----------------------------------------------------------#
import random
from datetime import datetime
from flask import render_template, flash, request, redirect, url_for, jsonify, session
from app import app, db, mail
# from blueprints.forms import CalculatorForm, RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
from flask_restful import Resource, Api
import string

from sqlalchemy import or_, and_
from util import verifyEmployeeToken
from .models import UserModel, EmailCaptchaModel, SessionModel, MessageModel
api = Api(app)

class Search(Resource):
    @verifyEmployeeToken
    def post(self):
        search_content = request.json.get("search_content")
        id = session.get('id')
        users = UserModel.query.filter(UserModel.username.like('%{0}%'.format(search_content))).all()
        users_ret = []
        for user in users:
            session_ = SessionModel.query.filter(or_(and_(SessionModel.user1_id==id, SessionModel.user2_id==user.id),and_(SessionModel.user2_id==id, SessionModel.user1_id==user.id))).first()
            if session_:
                last_massage = MessageModel.query.filter(MessageModel.session_id==session_.id).order_by(-MessageModel.id).first()
                if last_massage:
                    users_ret.append({"message_number": 0,"username":user.username,"id": user.id,"avatar": "/api/user/avatar?id=%s" % user.id, "last_message": {"date":str(last_massage.year)+"/"+str(last_massage.month)+"/"+str(last_massage.day) ,"content": last_massage.content, "user": last_massage.user_id}})
                else:
                    users_ret.append({"message_number": 0,"username":user.username,"id": user.id,"avatar": "/api/user/avatar?id=%s" % user.id, "last_message": {"date":str(""),"content":"", "user": ""}})
            else:
                users_ret.append({"message_number": 0,"username":user.username,"id": user.id,"avatar": "/api/user/avatar?id=%s" % user.id, "last_message": {"date":str(""),"content":"", "user": ""}})
            if len(users_ret) == 5:
                break # 只取前5个
        if len(users) == 0:
            return jsonify({"find":0})
        else:
            return jsonify({"find":len(users_ret),"users": users_ret})

api.add_resource(Search, "/api/search")

@app.route('/index/?<username>&<id>')
def index(username, id):
    user = {
        'name': username,
        'id' : id
    }
    return render_template('index.html',
                        title = "test",
                        user = user)

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        return render_template('forget_password.html')
    else:
        try:
            email  = request.form.get('email')
            user = UserModel.query.filter_by(email=email).first()
        except:
            return jsonify({"code": 400, "message": "邮箱不存在"})
        captcha = request.form.get("captcha")
        email = user.email
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            return jsonify({"code": 400, "message": "验证码不正确"})
        new_password = request.form.get("new_password")
        password_confirm = request.form.get("password_confirm")
        if not new_password == password_confirm:
            return jsonify({"code": 400, "message": "密码输入不一致"})
        hash_password = generate_password_hash(new_password)  # 存入hash形式的密码
        user.password = hash_password
        db.session.commit()
        print("修改密码成功")
        session.permanent = True
        return redirect(url_for("user.login", email=email))

@app.route("/", methods=["GET", "POST"])
def default():
    return redirect(url_for("user.login"))

@app.route("/nav", methods=["GET"])
def nav():
    print("get nav")
    id = request.values.get("id")
    user = UserModel.query.filter(UserModel.id==id).first()
    return render_template('nav.html', user=user)

@app.route("/home", methods=["GET"])
def home():
    id = session.get("id")
    user = UserModel.query.filter(UserModel.id==id).first()
    print(url_for('index', username=user.username, id=id))
    return url_for('index', username=user.username, id=id)

@app.route("/echart", methods=["GET"])
def echart():
    return render_template('echarts.html')