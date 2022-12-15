from functools import wraps
from urllib import request
from flask import jsonify, request
from authlib.jose import jwt, JoseError
from config import SECRET_KEY
from models import UserModel

def verifyEmployeeToken(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        tokenStr = request.headers.get('token')
        print(tokenStr)
        # print(request.headers)
        if tokenStr is None:
            return jsonify({'code': 410, 'message': 'Please log in first!'})
        token = tokenStr
        token = bytes(token, encoding="utf8")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                user = UserModel.query.filter_by(id=payload['id']).first()
                if user:
                    return func(self, *args, **kwargs)
                else:
                    return jsonify({'code': 410, 'message': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'code': 409, 'message': 'Please log in first!'})
        else:
            return jsonify({'code': 410, 'message': 'Please log in first!'})
    return wrapper

def generateToken(id):
    header = {'alg': 'HS256'}
    payload = {'id': id}
    token = jwt.encode(header, payload, SECRET_KEY)
    tokenStr = str(token, encoding='utf-8')
    return tokenStr

def decodeToken(token):
    token = bytes(token, encoding="utf8")
    payload = jwt.decode(token, SECRET_KEY)
    return payload
