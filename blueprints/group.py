#-----------------------------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2022/12/15 15:00
# @Author  : Prosperous
# @File    : group.py
# @Software: VSCode
# @Description: this file is about the group
# @Version: 1.0
#-----------------------------------------------------------#
import random
from datetime import datetime
from this import s
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, make_response, send_file, current_app
from flask_mail import Message
from forms import LoginForm, RegisterForm
from flask_restful import Resource, Api
import string
from app import db, mail, socketio
from flask_socketio import emit
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from models import EmailCaptchaModel, UserModel, SessionModel, MessageModel, GroupModel, GroupMemberModel, GroupMessageModel
from util import verifyEmployeeToken, decodeToken

# 注册了一个bp，名字叫user，前置路径是/user
bp = Blueprint("group", __name__, url_prefix="/api/group")
# 将bp挂载到api上
api = Api(bp)


class Group(Resource):
    @verifyEmployeeToken
    def post(self):
        users = request.json.get('users')
        user2_id = request.json.get('user2_id') #user2_id is the owner of the group
        current_app.logger.info(str(request.remote_addr)+"][User:"+user2_id+" Create Group")
        user2 = UserModel.query.filter(UserModel.id==user2_id).first()
        name  = request.json.get('name')
        if user2 is None:
            return jsonify({"message":"user not found"})
        group = GroupModel(name=name, owner_id=user2_id, create_time=datetime.now())
        db.session.add(group)
        group_member = GroupMemberModel(user_id=user2_id, group_id=group.id)
        db.session.add(group_member)
        db.session.commit()
        for user in users:
            user = UserModel.query.filter(UserModel.id==user).first()
            if user is None:
                return jsonify({"message":"user not found"})
            group_member = GroupMemberModel(user_id=user.id, group_id=group.id)
            db.session.add(group_member)
            db.session.commit()
        current_app.logger.info(str(request.remote_addr)+"][User:"+user2_id+" Create Group Success")
        return jsonify({"message":"success"})

    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Group")
        group_id = request.values.get("group_id")
        group = GroupModel.query.filter(GroupModel.id==group_id).first()
        if group is None:
            return jsonify({"message":"group not found"})
        members_ = GroupMemberModel.query.filter(GroupMemberModel.group_id==group.id).all()
        members = []
        for member in members_:
            user = UserModel.query.filter(UserModel.id==member.user_id).first()
            members.append({"id":member.user_id, "name":user.username, "avatar": "/api/user/avatar?id=%s" % user.id})
        return jsonify({"group_id":group.id, "name":group.name, "owner_id":group.owner_id, "members":members})


class Message(Resource):
    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Group Message")
        group_id = request.values.get("group_id")
        user_id = decodeToken(request.headers.get("token")).get("id")
        # session = SessionModel.query.filter(SessionModel.id==session_id)
        # messages = MessageModel.query.filter(MessageModel.session_id==session_id).order_by(MessageModel.id).all()
        messages = GroupMessageModel.query.filter(GroupMessageModel.group_id==group_id).order_by(GroupMessageModel.id).all()
        his_messages = []
        for message in messages:
            if(str(message.user_id) != str(user_id)):
                message.state = group_id
                db.session.commit()
            his_messages.append({"filename":message.filename,"id":message.id,"type":message.type,"url":message.url,"content": message.content,"user_avatar":"/api/user/avatar?id=%s" % message.user_id ,"user_id": message.user_id, "year": message.year, "month": message.month, "day": message.day, "hour": message.hour, "minute": message.min, "second": message.sec})
        if len(his_messages) > 50:
            for i in range(0, len(his_messages)-50):
                his_messages.pop(i)
        return jsonify({"messages":his_messages})

    @verifyEmployeeToken
    def post(self):
        group_id = request.json.get("group_id")
        content = request.json.get("content")
        user_id = decodeToken(request.headers.get("token")).get("id")
        dt= datetime.now()
        current_app.logger.info(str(request.remote_addr)+"][User:"+str(user_id)+"Send Message")
        year=dt.year
        month=dt.month
        day=dt.day
        hour=dt.hour
        minute=dt.minute
        second=dt.second
        type = "text"
        state=0
        message = GroupMessageModel(content=content, user_id=user_id, group_id=group_id,
                                year=year, month=month, day=day, hour=hour, min=minute, sec=second,
                                type=type, state=state)
        try:
            db.session.add(message)
            db.session.commit()
            return "Send message successfully!", 200
        except Exception as e:
            return e, 400

    @verifyEmployeeToken
    def delete(self):
        id = request.values.get("message_id")
        message = GroupMessageModel.query.filter(GroupMessageModel.id==id).first()
        current_app.logger.warning(str(request.remote_addr)+"][Delete Message:"+str(id)+"")
        try:
            db.session.delete(message)
            db.session.commit()
            return "Delete message successfully!", 200
        except Exception as e:
            return e, 400


class Upload(Resource):
    @verifyEmployeeToken
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Upload ")
        file = request.files.get('file')
        id = request.headers.get('id')
        filename=file.filename
        filetype=filename.split(".")[-1]
        message = GroupMessageModel.query.filter(GroupMessageModel.id==id).first()
        if filetype == "png" or filetype == "jpg" or filetype == "jpeg":
            file.save("asset/group/files/"+id+"."+filetype)
            type = "image"
            url = "/api/group/upload?filename="+id+"."+filetype
        else:
            file.save("asset/group/files/"+id+"."+filetype)
            type = "file"
            url = "/api/group/upload_file_content?filename="+id+"."+filetype
        message.type=type
        message.filename=filename
        print("filename",filename)
        message.url=url
        try:
            db.session.commit()
            return "Successfully!", 200
        except Exception as e:
            return e, 400

    def get(self):
        filename = request.args.get('filename')
        img_local_path = "./asset/group/files/" + filename
        try:
            img_f = open(img_local_path, 'rb')
            res = make_response(img_f.read())   # 用flask提供的make_response 方法来自定义自己的response对象
            res.headers['Content-Type'] = 'image/jpg'   # 设置response对象的请求头属性'Content-Type'为图片格式
            img_f.close()
            return res
        except:
            return "File not found!", 404

class updateFileContent(Resource):
    @verifyEmployeeToken
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Upload Group file content")
        group_id = request.json.get("group_id")
        content = request.json.get("content")
        user_id = decodeToken(request.headers.get("token")).get("id")
        dt= datetime.now()
        year=dt.year
        month=dt.month
        day=dt.day
        hour=dt.hour
        minute=dt.minute
        second=dt.second
        state=0
        message = GroupMessageModel(content=content, user_id=user_id, group_id=group_id,
                                year=year, month=month, day=day, hour=hour, min=minute, sec=second,
                                state=state)
        try:
            db.session.add(message)
            db.session.commit()
            return jsonify({"id": message.id})
        except Exception as e:
            return e, 400
    @verifyEmployeeToken
    def get(self):
        filename = request.args.get('filename')
        img_local_path = "./asset/group/files/" + filename
        try:
            return send_file(img_local_path, as_attachment=True, attachment_filename=filename)
        except:
            return "File not found!", 404

api.add_resource(Group, "/group")
api.add_resource(Message, "/message")
api.add_resource(Upload, "/upload")
api.add_resource(updateFileContent, "/update_file_content")


