#--------------------------------------#
# -*- coding: utf-8 -*-
# @Time    : 2022/12/15 15:00
# @Author  : Prosperous
# @File    : admin.py
# @Software: VSCode
# @Description: this file is about the admin
# @Version: 1.0
#--------------------------------------#
from app import db
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from flask_restful import Resource, Api
import json
from app.models import UserModel

bp = Blueprint("admin", __name__, url_prefix="/api/admin")
api = Api(bp)
class Users(Resource):
    def get(self):
        users = UserModel.query.all()
        user_r = []
        for user in users:
            user_r.append({"id": user.id,"username": user.username, "email": user.email, "address": user.address, "phone": user.tel, "remarks": user.remarks })
        return jsonify({'users': user_r})
    def post(self):
        id = request.json.get('id')
        user = UserModel.query.filter(UserModel.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "Delete user successfully!", 200
        else:
            return "Error deleting user!", 404

class Statistics(Resource):
    def get(self):
        users = UserModel.query.all()
        remarks = [0, 0]
        address = []
        address_number = []
        for user in users:
            if user.remarks == "0":
                remarks[0] += 1
            else:
                remarks[1] += 1
            if user.address not in address:
                address.append(user.address)
                address_number.append(1)
            else:
                address_number[address.index(user.address)] += 1
        return jsonify({"user_num": len(users), "remarks": remarks, "address": address, "address_number": address_number})

class Log(Resource):
    def get(self):
        log = open("./logs/flask.log", "r")
        log_r = log.read()
        res = []
        for line in log_r.split("\n"):
            if line != "":
                time = line.split("[")[1].split(",")[0]
                # print(time)
                path = line.split("[")[2].split("]")[0]
                # print(path)
                level = line.split("[")[3].split("]")[0]
                # print(level)
                address = line.split("[")[4].split("]")[0]
                message = line.split("[")[5].split("]")[0]
                line_j = {"time": time, "path": path, "level": level, "message": message, "address": address}
                res.append(line_j)
        log.close()
        return jsonify(res)

api.add_resource(Statistics, "/statistics")
api.add_resource(Users, "/all_users")
api.add_resource(Log, "/log")

