
import unittest
from db_database import db, app, UserModel, SessionModel, EmailCaptchaModel, FriendListModel, MessageModel, GroupModel, GroupMemberModel, GroupMessageModel
from flask import jsonify
import json
from faker import Faker

class TestClass(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app_db = app
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



if __name__ == '__main__':
    unittest.main()