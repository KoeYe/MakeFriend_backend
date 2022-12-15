#-------------------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2022/12/15 15:00
# @Author  : Prosperous
# @File    : forms.py
# @Software: VSCode
# @Description: this file is about the forms of the website
# @Version: 1.0
#-------------------------------------------------#
import wtforms
from flask_wtf import FlaskForm
import wtforms_json
from wtforms.validators import DataRequired, length, email, EqualTo

from models import EmailCaptchaModel, UserModel
# from models import EmailCaptchaModel, UserModel

wtforms_json.init()

class CalculatorForm(FlaskForm):
    number1 = wtforms.IntegerField('number1', validators=[DataRequired()])
    number2 = wtforms.IntegerField('number2', validators=[DataRequired()])


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[length(min=5, max=20), email()])
    password = wtforms.StringField(validators=[length(min=1, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=1, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=1, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # print(email)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            print(captcha_model)
            # print(captcha_model.captcha.lower())
            # print(captcha.lower())
            print("邮箱验证码错误！")
            raise wtforms.ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            print("邮箱已经存在！")
            raise wtforms.ValidationError("邮箱已经存在！")

class ProfileForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=1, max=20)])
    address = wtforms.StringField(validators=[length(min=1, max=200)])
    place = wtforms.StringField(validators=[length(min=1, max=20)])
    tel = wtforms.StringField(validators=[length(min=1, max=20)])
