
import datetime
import unittest
from db_database import db, app, UserModel, SessionModel, EmailCaptchaModel, FriendListModel, MessageModel, GroupModel, GroupMemberModel, GroupMessageModel
from flask import jsonify
import json
from faker import Faker

class TestClass(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        db.create_all()

        # add data to the database before all tests
        user1 = UserModel(id=1, username='mn20xx', email='mn20xx@leeds.ac.uk',password='test')
        db.session.add(user1)

        user2 = UserModel(id=2, username='mn20yy', email='mn20yy@leeds.ac.uk', password='test')
        db.session.add(user2)

        user3 = UserModel(id=3, username='mn20zz', email='mn20zz@leeds.ac.uk', password='test')
        db.session.add(user3)

        session1 = SessionModel(id=1, user1_id=1, user2_id=2)
        db.session.add(session1)

        captcha1 = EmailCaptchaModel(id=1, email='mn20xx', captcha='1234')
        db.session.add(captcha1)

        friend_list1 = FriendListModel(id=1, user_id=1, friend_id=2)
        db.session.add(friend_list1)

        message1 = MessageModel(id=1, user_id=1, session_id=1 ,content='hello')
        db.session.add(message1)

        group1 = GroupModel(id=1, name='test', owner_id=1)
        db.session.add(group1)

        group_member1 = GroupMemberModel(id=1, group_id=1, user_id=1)
        db.session.add(group_member1)

        group_message1 = GroupMessageModel(id=1, group_id=1, user_id=1, content='hello')
        db.session.add(group_message1)

        db.session.commit()

    def tearDown(self):
        # delete all data in the database after all tests
        db.session.remove()
        db.drop_all()

    def test_append_data(self):
        # user
        user = UserModel(id=4, username='mn20ww', email='mn20ww@leeds.ac.uk', password='test')
        db.session.add(user)
        db.session.commit()
        user_info = UserModel.query.filter_by(id=4).first()
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info.id, 4)
        self.assertEqual(user_info.username, 'mn20ww')
        self.assertEqual(user_info.password, 'test')

        # session
        session = SessionModel(id=2, user1_id=2,user2_id=3)
        db.session.add(session)
        db.session.commit()
        session_info = SessionModel.query.filter_by(id=2).first()
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.id, 2)
        self.assertEqual(session_info.user1_id, 2)
        self.assertEqual(session_info.user2_id, 3)

        # email_captcha
        email_captcha = EmailCaptchaModel(id=2, email='mn20yy', captcha='1234')
        db.session.add(email_captcha)
        db.session.commit()
        email_captcha_info = EmailCaptchaModel.query.filter_by(id=2).first()
        self.assertIsNotNone(email_captcha_info)
        self.assertEqual(email_captcha_info.id, 2)
        self.assertEqual(email_captcha_info.email, 'mn20yy')
        self.assertEqual(email_captcha_info.captcha, '1234')

        # friend_list
        friend_list = FriendListModel(id=2, user_id=2, friend_id=3, session_id=2)
        db.session.add(friend_list)
        db.session.commit()
        friend_list_info = FriendListModel.query.filter_by(id=2).first()
        self.assertIsNotNone(friend_list_info)
        self.assertEqual(friend_list_info.id, 2)
        self.assertEqual(friend_list_info.user_id, 2)
        self.assertEqual(friend_list_info.friend_id, 3)
        self.assertEqual(friend_list_info.session_id, 2)

        # message
        message = MessageModel(id=2, user_id=2, content='test', session_id=2)
        db.session.add(message)
        db.session.commit()
        message_info = MessageModel.query.filter_by(id=2).first()
        self.assertIsNotNone(message_info)
        self.assertEqual(message_info.id, 2)
        self.assertEqual(message_info.user_id, 2)
        self.assertEqual(message_info.content, 'test')
        self.assertEqual(message_info.session_id, 2)

        # group
        group = GroupModel(id=2, name='test2', owner_id=1,)
        db.session.add(group)
        db.session.commit()
        group_info = GroupModel.query.filter_by(id=2).first()
        self.assertIsNotNone(group_info)
        self.assertEqual(group_info.id, 2)
        self.assertEqual(group_info.name, 'test2')
        self.assertEqual(group_info.owner_id, 1)


        # group_member
        group_member = GroupMemberModel(id=2, group_id=2, user_id=3)
        db.session.add(group_member)
        db.session.commit()
        group_member_info = GroupMemberModel.query.filter_by(id=2).first()
        self.assertIsNotNone(group_member_info)
        self.assertEqual(group_member_info.id, 2)
        self.assertEqual(group_member_info.group_id, 2)
        self.assertEqual(group_member_info.user_id, 3)

        # group_message
        group_message = GroupMessageModel(id=2, group_id=2, user_id=3, content='test')
        db.session.add(group_message)
        db.session.commit()
        group_message_info = GroupMessageModel.query.filter_by(id=1).first()
        self.assertIsNotNone(group_message_info)
        self.assertEqual(group_message_info.id, 1)
        self.assertEqual(group_message_info.group_id, 1)
        self.assertEqual(group_message_info.user_id, 1)
        self.assertEqual(group_message_info.content, 'hello')


    def test_update_data(self):
        # user
        user = UserModel.query.filter_by(id=1).first()
        user.username = 'test'
        db.session.commit()
        user_info = UserModel.query.filter_by(id=1).first()
        self.assertEqual(user_info.username, 'test')

        # session
        session = SessionModel.query.filter_by(id=1).first()
        session.user1_id = 3
        db.session.commit()
        session_info = SessionModel.query.filter_by(id=1).first()
        self.assertEqual(session_info.user1_id, 3)


        # email_captcha
        email_captcha = EmailCaptchaModel.query.filter_by(id=1).first()
        email_captcha.captcha = 'test'
        db.session.commit()
        email_captcha_info = EmailCaptchaModel.query.filter_by(id=1).first()
        self.assertEqual(email_captcha_info.captcha, 'test')

        # friend_list
        friend_list = FriendListModel.query.filter_by(id=1).first()
        friend_list.friend_id = 2
        db.session.commit()
        friend_list_info = FriendListModel.query.filter_by(id=1).first()
        self.assertEqual(friend_list_info.friend_id, 2)

        # message
        message = MessageModel.query.filter_by(id=1).first()
        message.content = 'test'
        db.session.commit()
        message_info = MessageModel.query.filter_by(id=1).first()
        self.assertEqual(message_info.content, 'test')

        # group
        group = GroupModel.query.filter_by(id=1).first()
        group.name = 'test'
        db.session.commit()
        group_info = GroupModel.query.filter_by(id=1).first()
        self.assertEqual(group_info.name, 'test')

        # group_member
        group_member = GroupMemberModel.query.filter_by(id=1).first()
        group_member.user_id = 2
        db.session.commit()
        group_member_info = GroupMemberModel.query.filter_by(id=1).first()
        self.assertEqual(group_member_info.user_id, 2)

        # group_message
        group_message = GroupMessageModel.query.filter_by(id=1).first()
        group_message.content = 'test'
        db.session.commit()
        group_message_info = GroupMessageModel.query.filter_by(id=1).first()
        self.assertEqual(group_message_info.content, 'test')

    def test_delete_data(self):
        # user
        user = UserModel.query.filter_by(id=1).first()
        db.session.delete(user)
        db.session.commit()
        user_info = UserModel.query.filter_by(id=1).first()
        self.assertIsNone(user_info)

        # session
        session = SessionModel.query.filter_by(id=1).first()
        db.session.delete(session)
        db.session.commit()
        session_info = SessionModel.query.filter_by(id=1).first()
        self.assertIsNone(session_info)

        # email_captcha
        email_captcha = EmailCaptchaModel.query.filter_by(id=1).first()
        db.session.delete(email_captcha)
        db.session.commit()
        email_captcha_info = EmailCaptchaModel.query.filter_by(id=1).first()
        self.assertIsNone(email_captcha_info)

        # friend_list
        friend_list = FriendListModel.query.filter_by(id=1).first()
        db.session.delete(friend_list)
        db.session.commit()
        friend_list_info = FriendListModel.query.filter_by(id=1).first()
        self.assertIsNone(friend_list_info)

        # message
        message = MessageModel.query.filter_by(id=1).first()
        db.session.delete(message)
        db.session.commit()
        message_info = MessageModel.query.filter_by(id=1).first()
        self.assertIsNone(message_info)

        # group
        group = GroupModel.query.filter_by(id=1).first()
        db.session.delete(group)
        db.session.commit()
        group_info = GroupModel.query.filter_by(id=1).first()
        self.assertIsNone(group_info)

        # group_member
        group_member = GroupMemberModel.query.filter_by(id=1).first()
        db.session.delete(group_member)
        db.session.commit()
        group_member_info = GroupMemberModel.query.filter_by(id=1).first()
        self.assertIsNone(group_member_info)

        # group_message
        group_message = GroupMessageModel.query.filter_by(id=1).first()
        db.session.delete(group_message)
        db.session.commit()
        group_message_info = GroupMessageModel.query.filter_by(id=1).first()
        self.assertIsNone(group_message_info)



if __name__ == '__main__':
    unittest.main()