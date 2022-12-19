#---------------------------------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2022/12/15 15:00
# @Author  : Prosperous
# @File    : users.py
# @Software: VSCode
# @Description: this file is about the user's operation
# @Version: 1.0
#----------------------------------------------------------------#
import random
from datetime import datetime
from this import s
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, make_response, current_app
from flask_mail import Message
from forms import LoginForm, RegisterForm, ProfileForm
from flask_restful import Resource, Api
import string
from util import verifyEmployeeToken, generateToken, decodeToken
from config import SECRET_KEY
from app import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from models import EmailCaptchaModel, UserModel, FriendListModel, SessionModel, MessageModel, GroupMemberModel, GroupMemberModel, GroupModel, GroupMessageModel
from authlib.jose import jwt, JoseError
# 注册了一个bp，名字叫user，前置路径是/user
bp = Blueprint("user", __name__, url_prefix="/api/user")
# 将bp挂载到api上
api = Api(bp)

class Captcha(Resource):
    def post(self):
        # print(request.json)
        email = request.json.get("email")
        operation = request.json.get("operation")
        letters = string.ascii_letters + string.digits
        captcha = "".join(random.sample(letters, 4))
        # print(email)
        if email:
            print("验证码:" + captcha)
            message = Message(
                subject="Captcha Sending",
                recipients=[email],
                html=render_template(
                    'captcha.html', operation=operation, captcha=captcha),
                charset='utf-8'
            )
            mail.send(message)
            captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
            if captcha_model:
                captcha_model.captcha = captcha
                captcha_model.create_time = datetime.now()
                db.session.commit()
            else:
                captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
                db.session.add(captcha_model)
                db.session.commit()
            return jsonify({'message':"Send captcha successfully!",'code': 200})
        else:
            return jsonify({'message':"Please enter your email address!", 'code':400})

# 注册
class Register(Resource):
    def post(self):
        # print(request.json)
        form = RegisterForm.from_json(request.json)
        # print(form.email.data)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            register_datetime = datetime.now()
            hash_password = generate_password_hash(password)  # 存入hash形式的密码
            user = UserModel(
                email=email,
                username=username,
                password=hash_password,
                register_datetime=register_datetime
            )
            db.session.add(user)
            db.session.commit()
            print("注册成功")
            session['email'] = email
            session['password'] = password
            session.permanent = True
            return jsonify({'message':"Register successfully!", 'code':200})
        else:
            print("注册失败")
            return jsonify({'message':"Register failed!", 'code':400})

# 登陆
class Login(Resource):
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Login")
        form = LoginForm.from_json(request.json)
        if form.validate():
            email = request.json.get("email")
            if not email or email == "":
                return jsonify({"message": "Please enter your email address!", "code": 400})
            password = request.json.get("password")
            if not password or password == "":
                return jsonify({"message": "Please enter your password!", "code": 400})
            if email == "admin@admin.com" and password == "admin":
                return jsonify({"message": "Welcome to administration page!", "id":0, "username": "admin", "code":200})
            user_model = UserModel.query.filter_by(email=email).first()
            if user_model:
                if check_password_hash(user_model.password, password):
                    try:
                        print(datetime.now)
                        user_model.state = True  # 更新用户状态
                        # db.session.add(user_model)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e
                    id = user_model.id
                    print(user_model.email)
                    token = generateToken(user_model.id)
                    admin = user_model.admin
                    if admin:
                        current_app.logger.info(str(request.remote_addr)+"][User:admin Login Successfully")
                        return jsonify({"token":token,"message": "Welcome to administration page!", "id":0, "username": "admin", "code":200})
                    else:
                        # return jsonify({"code": 200})
                        current_app.logger.info(str(request.remote_addr)+"][User:"+str(id)+" Login Successfully")
                        return jsonify({"token":token,"message": "Login successfully!", "id":id, "username": user_model.username, "code":200})
                else:
                    # print(url_for("user.login"))
                    current_app.logger.info(str(request.remote_addr)+"][Login Failed")
                    return jsonify({"message":"Email or password incorrect!", "code": 400})
            else:
                current_app.logger.info("["+str(request.remote_addr)+"][Login Failed]")
                return jsonify({"message":"Email or password incorrect!", "code": 400})
        else:
            # print(url_for("user.login"))
            current_app.logger.info(str(request.remote_addr)+"][Login Failed")
            return jsonify({"message": "Please enter form", "code": 400})

# 忘记密码
class ForgetPassword(Resource):
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Forget Password")
        try:
            email  = request.json.get('email')
            user = UserModel.query.filter_by(email=email).first()
        except:
            return jsonify({"message": "Please enter your email address!", "code": 400})
        captcha = request.json.get("captcha")
        email = user.email
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            return jsonify({"message": "Captcha incorrect!", "code": 400})
        new_password = request.json.get("password")
        password_confirm = request.json.get("password_confirm")
        if not new_password == password_confirm:
            print(new_password)
            print(password_confirm)
            return "Please confirm your new password", 400
        hash_password = generate_password_hash(new_password)  # 存入hash形式的密码
        user.password = hash_password
        db.session.commit()
        print("修改密码成功")
        current_app.logger.warning(str(request.remote_addr)+"][User:"+str(user.id)+" Change password successfully")
        session.permanent = True
        return jsonify({"message": "Change password successfully!", "code": 200})

# 登出
class Logout(Resource):
    @verifyEmployeeToken
    def post(self):
        id = decodeToken(request.headers.get("token")).get("id")
        current_app.logger.info(str(request.remote_addr)+"][User:"+str(id)+" Logout")
        user = UserModel.query.filter_by(id=id).first()
        if id:
            user.state = False
            db.session.commit()
            return jsonify({"message": "Logout successfully!", "code": 200})
        else:
            return jsonify({"message": "Logout failed!", "code": 400})

# 用户名
class UserName(Resource):
    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Username")
        user_id = request.values.get("id")
        user = UserModel.query.filter(UserModel.id==user_id).first()
        if user:
            username = user.username
            return jsonify({"username": username, "code": 200})
        else:
            return jsonify({"message": "User not found!", "code": 400})

# 好友信息
class theFriends(Resource):
    @verifyEmployeeToken
    def post(self):
        user1_id = str(request.json.get("user1_id"))
        user2_id = request.json.get("user2_id")
        if user1_id == None or user2_id == None or user1_id == "" or user2_id == "":
            return jsonify({"message": "Please enter your id!", "code": 400})
        if user1_id==user2_id:
            return jsonify({"message": "You can't add yourself as a friend!", "code": 400})
        session_id = request.json.get("session_id")
        friendship = FriendListModel.query.filter(or_(and_(FriendListModel.friend_id==user1_id, FriendListModel.user_id==user2_id), and_(FriendListModel.friend_id==user2_id, FriendListModel.user_id==user1_id))).first()
        if friendship:
            return jsonify({"message": "You are already friends!", "code": 400})
        else:
            n_friendship = FriendListModel(
                user_id = user2_id,
                friend_id = user1_id,
                session_id = session_id
            )
            try:
                db.session.add(n_friendship)
                db.session.commit()
                current_app.logger.info(str(request.remote_addr)+"][User:"+str(user1_id)+" and User:"+str(user2_id)+" Make Friends")
            except Exception as e:
                return e, 400
            return jsonify({"message": "Make friends successfully!", "code": 200})

    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Friends")
        user1_id = request.values.get("user1_id")
        user2_id = request.values.get("user2_id")
        friendship = FriendListModel.query.filter(or_(and_(FriendListModel.friend_id==user1_id, FriendListModel.user_id==user2_id),
                                                and_(FriendListModel.friend_id==user2_id, FriendListModel.user_id==user1_id))).first()
        if friendship:
            return 1
        else:
            return 0

    @verifyEmployeeToken
    def delete(self):
        user1_id = request.values.get("user1_id")
        user2_id = request.values.get("user2_id")
        if user1_id == None or user2_id == None or user1_id == "" or user2_id == "":
            return jsonify({"message": "Please enter your id!", "code": 400})
        current_app.logger.warning(str(request.remote_addr)+"][User:"+str(user1_id)+" and User:"+str(user2_id)+" Delete Friends")
        friendship = FriendListModel.query.filter(or_(and_(FriendListModel.friend_id==user1_id, FriendListModel.user_id==user2_id), and_(FriendListModel.friend_id==user2_id, FriendListModel.user_id==user1_id))).first()
        if friendship:
            try:
                db.session.delete(friendship)
                db.session.commit()
                return jsonify({"message": "Delete friends successfully!", "code": 200})
            except Exception as e:
                return e, 200
        else:
            return jsonify({"message": "You are not friends!", "code": 400})

# 好友列表
class Friends(Resource):
    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Friends")
        id = decodeToken(request.headers.get("token")).get("id")
        Friends = FriendListModel.query.filter(or_(FriendListModel.user_id==id, FriendListModel.friend_id==id)).all()
        friends_id_list = []
        for friend in Friends:
            if str(id) == str(friend.friend_id):
                friends_id_list.append(friend.user_id)
            else:
                friends_id_list.append(friend.friend_id)
        friends_list = []
        if len(friends_id_list) == 0:
            current_app.logger.info(str(request.remote_addr)+"][Get Friends Successfully")
            return jsonify({"find":len(friends_list),"friends": friends_list})
        for f_id in friends_id_list:
            user = UserModel.query.filter(UserModel.id==f_id).first()
            if not user:
                current_app.logger.info(str(request.remote_addr)+"][Get Friends Failed")
                return "User not found", 400
            session = SessionModel.query.filter(or_(and_(SessionModel.user1_id==id, SessionModel.user2_id==user.id),and_(SessionModel.user2_id==id, SessionModel.user1_id==user.id))).first()
            last_massage = MessageModel.query.filter(MessageModel.session_id==session.id).order_by(-MessageModel.id).first()
            if last_massage:
                count = 0;
                messages = MessageModel.query.filter(and_(MessageModel.session_id==session.id, MessageModel.state==0)).all()
                for message in messages:
                    if str(message.user_id) != str(id):
                        count += 1
                friends_list.append({"message_number": count,"username": user.username, "id": user.id, "avatar": "/api/user/avatar?id=%s" % user.id, "last_message": {"date":str(last_massage.year)+"/"+str(last_massage.month)+"/"+str(last_massage.day) ,"content": last_massage.content, "user": last_massage.user_id}})
            else:
                friends_list.append({"message_number": 0,"username": user.username, "id": user.id, "avatar": "/api/user/avatar?id=%s" % user.id, "last_message": {"date":"","content":"","user":""}})
        current_app.logger.info(str(request.remote_addr)+"][Get Friends Successfully")
        return jsonify({"code":200,"find":len(friends_list),"friends": friends_list})

# 用户头像
class Avatar(Resource):
    def post(self):
        current_app.logger.info(str(request.remote_addr)+"][Updating Avatar")
        file = request.files.get('file')
        if not file:
            return jsonify({"message": "Please upload your avatar!", "code": 400})
        user_id = decodeToken(request.headers.get("token")).get("id")
        file_name = str(user_id) + ".jpg"
        file.save("./asset/avatar/"+file_name)
        return jsonify({"message": "Update avatar successfully!", "code": 200})
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Avatar")
        uid = request.args.get('id')
        img_local_path = "./asset/avatar/" + uid + ".jpg"
        img_f = open(img_local_path, 'rb')
        res = make_response(img_f.read())   # 用flask提供的make_response 方法来自定义自己的response对象
        res.headers['Content-Type'] = 'image/jpg'   # 设置response对象的请求头属性'Content-Type'为图片格式
        img_f.close()
        return res

# 用户信息
class Profile(Resource):
    @verifyEmployeeToken
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Profile")
        id = request.args.get('id')
        if not id:
            return jsonify({"message": "Please input your id!", "code": 400})
        user = UserModel.query.filter(UserModel.id==id).first()
        if not user:
            return jsonify({"message": "User not found!", "code": 400})
        return jsonify({
            "code" : 200,
            "username" : user.username,
            "address" : user.address,
            "tel" : user.tel,
            "remarks": user.remarks,
            "place": user.place,
        })

    @verifyEmployeeToken
    def post(self):
        form = ProfileForm.from_json(request.json)
        if form.validate():
            id = request.json.get('id')
            if not id or id == "":
                return jsonify({"message": "Please input your id!", "code": 400})
            user = UserModel.query.filter(UserModel.id==id).first()
            if not user:
                return jsonify({"message": "User not found!", "code": 400})

            username = form.username.data
            tel = form.tel.data
            address = form.address.data
            place = form.place.data
            remarks = request.json.get('remarks')
            user.address = address
            user.place = place
            user.remarks = remarks
            user.tel = tel
            user.username = username
            try:
                db.session.commit()
                current_app.logger.info(str(request.remote_addr)+"][User:"+str(user.id)+" Update Profile")
                return jsonify({"message": "Update profile successfully!", "code": 200})
            except Exception as e:
                return jsonify({"message": "Update profile failed!", "code": 400})
        else:
            return jsonify({"message": "Update profile failed!", "code": 400})


class Group(Resource):
    def get(self):
        current_app.logger.info(str(request.remote_addr)+"][Get Group")
        id = decodeToken(request.headers.get("token"))
        if not id:
            return jsonify({"code":410,"message":"Please login!"})
        id = id.get("id")
        print("Group user id:"+str(id))
        groups = GroupMemberModel.query.filter(GroupMemberModel.user_id==id).all()
        group_id_list = []
        for group in groups:
            group_id_list.append(group.group_id)
        print(group_id_list)
        groups_list = []
        if len(group_id_list) == 0:
            current_app.logger.info(str(request.remote_addr)+"][Get Group Successfully")
            return jsonify({"code":200,"find":len(groups_list),"groups": groups_list})
        for g_id in group_id_list:
            members_list = []
            #查找group
            group = GroupModel.query.filter(GroupModel.id==g_id).first()
            if not group:
                return jsonify({"code":400,"message":"Group not found!"})
            #查找group的成员
            members = GroupMemberModel.query.filter(GroupMemberModel.group_id==g_id).all()
            for member in members:
                user = UserModel.query.filter(UserModel.id==member.user_id).first()
                members_list.append({"username": user.username, "id": user.id, "avatar": "/api/user/avatar?id=%s" % user.id})
            #查找最后一条消息
            last_massage = GroupMessageModel.query.filter(GroupMessageModel.group_id==group.id).order_by(-GroupMessageModel.id).first()
            if last_massage:
                count = 0;
                messages = GroupMessageModel.query.filter(and_(GroupMessageModel.group_id==group.id, GroupMessageModel.state==0)).all()
                for message in messages:
                    if str(message.user_id) != str(id):
                        count += 1
                groups_list.append({"message_number": count,"group_name": group.name, "id": group.id, 'members':members_list,
                                    "last_message": {"date":str(last_massage.year)+"/"+str(last_massage.month)+"/"+str(last_massage.day) ,"content": last_massage.content, "user": last_massage.user_id}})
            else:
                groups_list.append({"message_number": 0,"group_name": group.name, "id": group.id, 'members':members_list,
                                    "last_message": {"date":"","content":"","user":""}})
        current_app.logger.info(str(request.remote_addr)+"][Get Friends Successfully")
        return jsonify({"code":200,"find":len(groups_list),"groups": groups_list})
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

api.add_resource(Search, "/search")
api.add_resource(Captcha, "/captcha")
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(ForgetPassword, "/forget_password")
api.add_resource(UserName, "/username")
api.add_resource(theFriends, "/make_friend")
api.add_resource(Friends, "/friends")
api.add_resource(Avatar, "/avatar")
api.add_resource(Profile, "/profile")
api.add_resource(Group, "/group")

@bp.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if request.method == "GET":
        id = session.get('id')
        # print('change_password-id in session:',id)
        user = UserModel.query.filter_by(id=id).first()
        return render_template("change_password.html", user=user)
    else:
        try:
            id = session.get('id')
            user = UserModel.query.filter_by(id=id).first()
        except:
            return jsonify({"code": 400, "message": "session失效"})
        old_password = request.form.get('old_password')
        if not check_password_hash(user.password, old_password):
            return jsonify({"code": 400, "message": "密码不正确"})
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
