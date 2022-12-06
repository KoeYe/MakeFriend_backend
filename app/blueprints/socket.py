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
from flask_socketio import emit, Namespace
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from app.models import EmailCaptchaModel, UserModel, SessionModel

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('send')
def handle_se(data):
    print('received message: ' + data)