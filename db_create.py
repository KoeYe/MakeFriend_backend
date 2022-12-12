#---------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2022/12/15 15:00
# @Author  : Prosperous
# @File    : db_create.py
# @Software: VSCode
# @Description: this file is about the db create
# @Version: 1.0
#---------------------------------------#
from config import SQLALCHEMY_DATABASE_URI
from app.exts import db
from app import app

with app.app_context():
    db.create_all()
   # db.drop_all()
