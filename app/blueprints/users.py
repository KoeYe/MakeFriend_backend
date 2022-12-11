import random
from datetime import datetime
from this import s
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, make_response
from flask_mail import Message
from app.blueprints.admin import show_all_user
from app.blueprints.forms import LoginForm, RegisterForm, ProfileForm
from flask_restful import Resource, Api
import string
from app import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from app.models import EmailCaptchaModel, UserModel, FriendListModel, SessionModel, MessageModel

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
            return "Send captcha successfully!", 200
        else:
            return "Please enter your email address!", 400

class Test(Resource):
    def get(self):
        return "test", 200

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
            return "Register Successfully!", 200
        else:
            print("注册失败")
            return "Register failed!", 400

# 登陆
class Login(Resource):
    def post(self):
        form = LoginForm.from_json(request.json)
        if form.validate():
            email = request.json.get("email")
            password = request.json.get("password")
            if email == "admin@admin.com" and password == "admin":
                return "admin", 301
            user_model = UserModel.query.filter_by(email=email).first()
            if user_model:
                if check_password_hash(user_model.password, password):
                    print("登录成功")
                    try:
                        print(datetime.now)
                        user_model.state = True  # 更新用户状态
                        # db.session.add(user_model)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e
                    id = user_model.id
                    session["id"] = id
                    session["username"] = user_model.username
                    session.permanent = True
                    print("id in session:",session.get("id"))
                    admin = user_model.admin
                    if admin:
                        return "admin", 301
                    else:
                        # return jsonify({"code": 200})
                        return jsonify({"message": "Login successfully!", "id":id, "username": user_model.username, "code":200})
                else:
                    # print(url_for("user.login"))
                    print("密码不正确")
                    return "Email or password incorrect!", 400
            else:
                return "Email or password incorrect!", 400
        else:
            # print(url_for("user.login"))
            print("not valid")
            return "Please input form correctly!", 400


class ForgetPassword(Resource):
    def post(self):
        try:
            email  = request.json.get('email')
            user = UserModel.query.filter_by(email=email).first()
        except:
            return "invalid email address", 400
        captcha = request.json.get("captcha")
        email = user.email
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            return "Incorrect captcha", 400
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
        session.permanent = True
        return "Change password successfully!", 200

class Logout(Resource):
    def post(self):
        id = session.get("id")
        print("id: ", id)
        user = UserModel.query.filter_by(id=id).first()
        if id:
            session.pop('id')
            user.state = False
            db.session.commit()
            return "Logout successfully!", 200
        else:
            return "Logout failed", 400


class UserName(Resource):
    def get(self):
        user_id = request.values.get("id")
        print("user_id: ", user_id)
        user = UserModel.query.filter(UserModel.id==user_id).first()
        username = user.username
        return username, 200

class theFriends(Resource):
    def post(self):
        user1_id = str(request.json.get("user1_id"))
        user2_id = request.json.get("user2_id")
        if user1_id==user2_id:
            return "You can't make friend with yourself", 400
        session_id = request.json.get("session_id")
        friendship = FriendListModel.query.filter(or_(and_(FriendListModel.friend_id==user1_id, FriendListModel.user_id==user2_id), and_(FriendListModel.friend_id==user2_id, FriendListModel.user_id==user1_id))).first()
        if friendship:
            return "he/she has been your friend!", 400
        else:
            n_friendship = FriendListModel(
                user_id = user2_id,
                friend_id = user1_id,
                session_id = session_id
            )
            try:
                db.session.add(n_friendship)
                db.session.commit()
            except Exception as e:
                return e, 400
            return "Add friend successfully!", 200

    def get(self):
        user1_id = request.values.get("user1_id")
        user2_id = request.values.get("user2_id")
        print("1:",user1_id, "2:",user2_id)
        friendship = FriendListModel.query.filter(or_(and_(FriendListModel.friend_id==user1_id, FriendListModel.user_id==user2_id),
                                                and_(FriendListModel.friend_id==user2_id, FriendListModel.user_id==user1_id))).first()
        if friendship:
            return 1
        else:
            return 0

    def delete(self):
        user1_id = request.values.get("user1_id")
        user2_id = request.values.get("user2_id")
        friendship = FriendListModel.query.filter(or_(and_(FriendListModel.friend_id==user1_id, FriendListModel.user_id==user2_id), and_(FriendListModel.friend_id==user2_id, FriendListModel.user_id==user1_id))).first()
        if friendship:
            try:
                db.session.delete(friendship)
                db.session.commit()
                return "Delete friend successfully!", 200
            except Exception as e:
                return e, 200
        else:
            return "He is not your friend", 400

class Friends(Resource):
    def get(self):
        id = request.values.get("user2_id")
        # print(id)
        Friends = FriendListModel.query.filter(or_(FriendListModel.user_id==id, FriendListModel.friend_id==id)).all()
        friends_id_list = []
        for friend in Friends:
            if str(id) == str(friend.friend_id):
                friends_id_list.append(friend.user_id)
            else:
                friends_id_list.append(friend.friend_id)
        friends_list = []
        for f_id in friends_id_list:
            user = UserModel.query.filter(UserModel.id==f_id).first()
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
        return jsonify({"find":len(friends_list),"friends": friends_list})

class Avatar(Resource):
    def post(self):
        file = request.files.get('file')
        user_id = session.get('id')
        file_name = str(user_id) + ".jpg"
        file.save("./asset/avatar/"+file_name)
        return "Successfully!", 200
    def get(self):
        uid = request.args.get('id')
        img_local_path = "./asset/avatar/" + uid + ".jpg"
        img_f = open(img_local_path, 'rb')
        res = make_response(img_f.read())   # 用flask提供的make_response 方法来自定义自己的response对象
        res.headers['Content-Type'] = 'image/jpg'   # 设置response对象的请求头属性'Content-Type'为图片格式
        img_f.close()
        return res

class Profile(Resource):
    def get(self):
        id = request.args.get('id')
        user = UserModel.query.filter(UserModel.id==id).first()
        return jsonify({
            "username" : user.username,
            "address" : user.address,
            "tel" : user.tel,
            "remarks": user.remarks,
            "place": user.place,
        })
    def post(self):
        print(request.json)
        form = ProfileForm.from_json(request.json)
        if form.validate():
            id = request.json.get('id')
            user = UserModel.query.filter(UserModel.id==id).first()
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
                return "Edit Profile Successfully!", 200
            except Exception as e:
                return e, 400
        else:
            return "Invalid input", 400


api.add_resource(Test, "/test")
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
