
from io import BytesIO
import unittest
from flask import jsonify
import json
from faker import Faker
from app import app

class TestLoginClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_login(self):
        # admin login
        data = {
            'email': 'admin@admin.com',
            'password': 'admin'
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # user login
        data = {
            'email': '2826232264@qq.com',
            'password': '200212'
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        data = {
            'email': '2826232264@qq.com',
            'password':'123456'
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '2826232264@qq.com',
            'password': ''
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        # print(type(res))
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '',
            'password': 'password',
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '',
            'password': '',
        }
        res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        faker_en = Faker('en_US')
        data_list = []
        for i in range(100):
            data_list.append({
                'email': str(faker_en.email()),
                'password': str(faker_en.password())
            })
        # print(data_list)
        for data in data_list:
            res = self.app.post('/api/user/login', data=json.dumps(data), content_type='application/json')
            res_dict = json.loads(res.data)
            self.assertIn('code', res_dict)
            self.assertEqual(res_dict['code'], 400)

    def test_captcha(self):
        data = {
            'email': 'test@test.com',
        }
        res = self.app.post('/api/user/captcha', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        data = {
            'email': '',
        }
        res = self.app.post('/api/user/captcha', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_register(self):
        data = {
            'email': '',
            'password': '',
            'captcha': '',
        }
        res = self.app.post('/api/user/register', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'email': '',
            'password': '',
            'captcha': '',
        }
        res = self.app.post('/api/user/register', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

class TestIndexClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        email = '2826232264@qq.com'
        res = self.app.post('/api/user/login', data=json.dumps({'email': email, 'password': '200212'}),
                                content_type='application/json')
        res_dict = json.loads(res.data)
        print("res_dict:", res_dict)
        self.token = res_dict['token']

    def tearDown(self):
        pass

    def test_logout(self):
        res = self.app.post('/api/user/logout', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        res = self.app.post('/api/user/logout')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

    def test_username(self):
        res = self.app.get('/api/user/username?id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        res = self.app.get('/api/user/username?id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        res = self.app.get('/api/user/username?id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.get('/api/user/username?id=1')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        res = self.app.get('/api/user/username?id=')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

    def test_make_friend(self):

        # 删除好友
        self.app.delete('/api/user/make_friend?user1_id=1&user2_id=2',headers={'token': self.token}, content_type='application/json')
        che = self.app.get('/api/user/make_friend?user1_id=1&user2_id=2', headers={'token': self.token}, content_type='application/json')
        self.assertEqual(che.data, b'0\n') #检查是否删除好友成功

        # 添加好友
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend',data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 检查是否添加好友成功
        che = self.app.get('/api/user/make_friend?user1_id=1&user2_id=2', headers={'token': self.token}, content_type='application/json')
        self.assertEqual(che.data, b'1\n')

        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend',data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试删除好友
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.delete('/api/user/make_friend?user1_id=1&user2_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试删除好友之后是否可以再次添加
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试添加好友之后是否可以重复添加
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend',data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试不带token
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试是否可以添加自己为好友
        data = {
            'user1_id': '1',
            'user2_id': '1',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)
        self.assertEqual(res_dict['message'], "You can't add yourself as a friend!")

        # 测试是否可以添加不存在的用户为好友
        data = {
            'user1_id': '',
            'user2_id': '2',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'user1_id': '1',
            'user2_id': '',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        data = {
            'user1_id': '',
            'user2_id': '',
        }
        res = self.app.post('/api/user/make_friend', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试是否可以删除不存在的好友
        res = self.app.delete('/api/user/make_friend?user1_id=&user2_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.delete('/api/user/make_friend?user1_id=1&user2_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.delete('/api/user/make_friend?user1_id=&user2_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_friends(self):
        # 测试获取好友列表
        res = self.app.get('/api/user/friends', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试不带token
        res = self.app.get('/api/user/friends', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

    def test_avatar(self):
        # 测试上传头像
        data = {
            'file': (BytesIO(b"abcdef"), 'test.jpg'),
        }
        res = self.app.post('/api/user/avatar', data=data, headers={'token': self.token}, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试不带token
        data = {
            'file': (BytesIO(b"abcdef"), 'test.jpg'),
        }
        res = self.app.post('/api/user/avatar', data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试不带文件
        res = self.app.post('/api/user/avatar', headers={'token': self.token}, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_profile(self):
        # 测试获取用户信息
        res = self.app.get('/api/user/profile?id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试不带token
        res = self.app.get('/api/user/profile?id=1', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试不带user_id
        res = self.app.get('/api/user/profile', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取不存在的用户信息
        res = self.app.get('/api/user/profile?id=100', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试修改用户信息
        data = {
            'id' : '1',
            'username' : 'test',
            'address' : 'test',
            'tel' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试不带token
        data = {
            'id'    : '1',
            'username' : 'test',
            'address' : 'test',
            'tel' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试不带参数
        data = {
            'id'    : '',
            'username' : '',
            'address' : '',
            'tel' : '',
            'remarks' : '',
            'place': '',
        }
        res = self.app.post('/api/user/profile',data = json.dumps(data) ,headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试修改不存在的用户信息
        data = {
            'id'    : '100',
            'username' : 'test',
            'address' : 'test',
            'phone' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试修改用户信息，不带id
        data = {
            'id' : '',
            'username' : 'test',
            'address' : 'test',
            'phone' : 'test',
            'remarks' : 'test',
            'place': 'test',
        }
        res = self.app.post('/api/user/profile', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_group(self):
        # 测试获取用户组
        res = self.app.get('/api/user/group', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试不带token
        res = self.app.get('/api/user/group', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

class TestSession(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        email = '2826232264@qq.com'
        res = self.app.post('/api/user/login', data=json.dumps({'email': email, 'password': '200212'}),
                                content_type='application/json')
        res_dict = json.loads(res.data)
        print("res_dict:", res_dict)
        self.token = res_dict['token']

    def tearDown(self):
        pass

    def test_session(self):
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试不带token
        data = {
            'user1_id': '1',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试不带参数
        data = {
            'user1_id': '',
            'user2_id': '',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试不带user1_id
        data = {
            'user1_id': '',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试不带user2_id
        data = {
            'user1_id': '1',
            'user2_id': '',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试user1_id不存在
        data = {
            'user1_id': '100',
            'user2_id': '2',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试user2_id不存在
        data = {
            'user1_id': '1',
            'user2_id': '100',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试user1_id和user2_id相同
        data = {
            'user1_id': '1',
            'user2_id': '1',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试user1_id和user2_id都不存在
        data = {
            'user1_id': '100',
            'user2_id': '100',
        }
        res = self.app.post('/api/session/session', data=json.dumps(data), headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表
        res = self.app.get('/api/session/session?session_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试获取会话列表不带token
        res = self.app.get('/api/session/session?session_id=2', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试获取会话列表不带session_id
        res = self.app.get('/api/session/session', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id不存在
        res = self.app.get('/api/session/session?session_id=100', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id不是数字
        res = self.app.get('/api/session/session?session_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id是小数
        res = self.app.get('/api/session/session?session_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id是负数
        res = self.app.get('/api/session/session?session_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id是0
        res = self.app.get('/api/session/session?session_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id是空字符串
        res = self.app.get('/api/session/session?session_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id是空格
        res = self.app.get('/api/session/session?session_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取会话列表session_id是字符串
        res = self.app.get('/api/session/session?session_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_message(self):
        # 测试获取消息
        res = self.app.get('/api/session/message?session_id=2', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试获取消息不带token
        res = self.app.get('/api/session/message?session_id=2', content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试获取消息不带session_id
        res = self.app.get('/api/session/message', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id不存在
        res = self.app.get('/api/session/message?session_id=100', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id不是数字
        res = self.app.get('/api/session/message?session_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id是小数
        res = self.app.get('/api/session/message?session_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id是负数
        res = self.app.get('/api/session/message?session_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id是0
        res = self.app.get('/api/session/message?session_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id是空字符串
        res = self.app.get('/api/session/message?session_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取消息session_id是空格
        res = self.app.get('/api/session/message?session_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息
        data = {
            'session_id': '2',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息不带token
        res = self.app.post('/api/session/message', data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 410)

        # 测试发送消息不带session_id
        data = {
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息不带content
        data = {
            'session_id': '2'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id不存在
        data = {
            'session_id': '100',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id不是数字
        data = {
            'session_id': 'abc',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id是小数
        data = {
            'session_id': '1.1',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id是负数
        data = {
            'session_id': '-1',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id是0
        data = {
            'session_id': '0',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id是空字符串
        data = {
            'session_id': '',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息session_id是空格
        data = {
            'session_id': ' ',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息content是空字符串
        data = {
            'session_id': '2',
            'content': ''
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息content是空格
        data = {
            'session_id': '2',
            'content': ' '
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是空
        data = {
            'session_id': '2',
            'content': None
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送消息content是数字
        data = {
            'session_id': '2',
            'content': '123'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是小数
        data = {
            'session_id': '2',
            'content': '1.1'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是负数
        data = {
            'session_id': '2',
            'content': '-1'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是特殊字符
        data = {
            'session_id': '2',
            'content': '!@#$%^&*()_+'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是中文
        data = {
            'session_id': '2',
            'content': '测试'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是英文
        data = {
            'session_id': '2',
            'content': 'test'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是英文和数字
        data = {
            'session_id': '2',
            'content': 'test123'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是英文和特殊字符
        data = {
            'session_id': '2',
            'content': 'test!@#$%^&*()_+'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是英文和中文
        data = {
            'session_id': '2',
            'content': 'test测试'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是数字和特殊字符
        data = {
            'session_id': '2',
            'content': '123!@#$%^&*()_+'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是数字和中文
        data = {
            'session_id': '2',
            'content': '123测试'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是特殊字符和中文
        data = {
            'session_id': '2',
            'content': '!@#$%^&*()_+测试'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送消息content是英文、数字、特殊字符和中文
        data = {
            'session_id': '2',
            'content': 'test123!@#$%^&*()_+测试'
        }
        res = self.app.post('/api/session/message', headers={'token': self.token}, data=json.dumps(data), content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试撤回消息
        res = self.app.delete('/api/session/message?message_id=6', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id不存在
        res = self.app.delete('/api/session/message?message_id=10000', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id不是数字
        res = self.app.delete('/api/session/message?message_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为空
        res = self.app.delete('/api/session/message?message_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为负数
        res = self.app.delete('/api/session/message?message_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为0
        res = self.app.delete('/api/session/message?message_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为小数
        res = self.app.delete('/api/session/message?message_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为字符串
        res = self.app.delete('/api/session/message?message_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为特殊字符
        res = self.app.delete('/api/session/message?message_id=!@#$%^&*()_+', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为中文
        res = self.app.delete('/api/session/message?message_id=测试', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为英文、数字、特殊字符和中文
        res = self.app.delete('/api/session/message?message_id=test123!@#$%^&*()_+测试', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload(self):
        # 测试上传文件
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"11"}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试上传文件session_id不存在
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"10000"}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件session_id不是数字
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"abc"}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件session_id为空
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        res = self.app.post('/api/session/upload', headers={'token': self.token, 'id':"  "}, data=data, content_type='multipart/form-data')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload_file_content(self):
        # 测试上传文件内容
        data = {
            'content': "test",
            'session_id': "2",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试上传文件内容session_id不存在
        data = {
            'content': "test",
            'session_id': "1000",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件内容session_id为空
        data = {
            'content': "test",
            'session_id': "  ",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件内容session_id不是数字
        data = {
            'content': "test",
            'session_id': "abc",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件内容content为空
        data = {
            'content': "  ",
            'session_id': "2",
        }
        res = self.app.post('/api/session/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

class TestGroup(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        email = '2826232264@qq.com'
        res = self.app.post('/api/user/login', data=json.dumps({'email': email, 'password': '200212'}),
                                content_type='application/json')
        res_dict = json.loads(res.data)
        print("res_dict:", res_dict)
        self.token = res_dict['token']

    def tearDown(self):
        pass

    def test_create_group(self):
        # 测试创建群组
        data = {
            "users": [11, 12, 13],
            "name": "test",
            "user2_id": "11",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试创建群组users为空
        data = {
            "users": [],
            "name": "test",
            "user2_id": "1",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试创建群组users不是数组
        data = {
            "users": "1",
            "name": "test",
            "user2_id": "1",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试创建群组user2_id不是数字
        data = {
            "users": [1, 2, 3],
            "name": "test",
            "user2_id": "abc",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试创建群组user2_id为空
        data = {
            "users": [1, 2, 3],
            "name": "test",
            "user2_id": "  ",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试创建群组name为空
        data = {
            "users": [1, 2, 3],
            "name": "  ",
            "user2_id": "1",
        }
        res = self.app.post('/api/group/group', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        res = self.app.get('/api/group/group?group_id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试获取不存在的group_id
        res = self.app.get('/api/group/group?group_id=200', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取group_id为空格
        res = self.app.get('/api/group/group?group_id=  ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取group_id不是数字
        res = self.app.get('/api/group/group?group_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取group_id为空
        res = self.app.get('/api/group/group?group_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_message(self):
        # 测试获取群组消息
        res = self.app.get('/api/group/message?group_id=1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试获取不存在的group_id
        res = self.app.get('/api/group/message?group_id=200', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取group_id为空格
        res = self.app.get('/api/group/message?group_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取group_id不是数字
        res = self.app.get('/api/group/message?group_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试获取group_id为空
        res = self.app.get('/api/group/message?group_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送群组消息
        data = {
            "group_id": 1,
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送不存在的group_id
        data = {
            "group_id": 200,
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送group_id为空格
        data = {
            "group_id": " ",
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送group_id不是数字
        data = {
            "group_id": "abc",
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送group_id为空
        data = {
            "group_id": "",
            "content": "test",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送content为空
        data = {
            "group_id": 1,
            "content": "",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送content为空格
        data = {
            "group_id": 1,
            "content": " ",
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试发送content为None
        data = {
            "group_id": 1,
            "content": None,
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试发送content为数字
        data = {
            "group_id": 1,
            "content": 123,
        }
        res = self.app.post('/api/group/message', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试撤回消息
        res = self.app.delete('/api/group/message?message_id=12', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试撤回不存在的消息
        res = self.app.delete('/api/group/message?message_id=1000', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为空
        res = self.app.delete('/api/group/message?message_id=', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为空格
        res = self.app.delete('/api/group/message?message_id= ', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为None
        res = self.app.delete('/api/group/message?message_id=None', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为字符串
        res = self.app.delete('/api/group/message?message_id=abc', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为小数
        res = self.app.delete('/api/group/message?message_id=1.1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为负数
        res = self.app.delete('/api/group/message?message_id=-1', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试撤回消息message_id为0
        res = self.app.delete('/api/group/message?message_id=0', headers={'token': self.token}, content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload(self):
        # 测试上传文件
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '11'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试上传文件group_id不存在
        data = {
            "group_id": 1000,
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为空
        data = {
            "group_id": "",
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为空格
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': ' '}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为None
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': None}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为字符串
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': 'abc'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为小数
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '1.1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为负数
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '-1'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件group_id为0
        data = {
            "file": (BytesIO(b"abcdef"), "test.txt")
        }
        res = self.app.post('/api/group/upload', headers={'token': self.token, 'id': '0'}, data=data)
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

    def test_upload_file_content(self):
        # 测试上传文件内容
        data = {
            'content': "test",
            'group_id': "2",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)

        # 测试上传文件内容group_id不存在
        data = {
            'content': "test",
            'group_id': "1000",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件内容group_id为空
        data = {
            'content': "test",
            'group_id': "  ",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件内容group_id不是数字
        data = {
            'content': "test",
            'group_id': "abc",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 400)

        # 测试上传文件内容content为空
        data = {
            'content': "  ",
            'group_id': "2",
        }
        res = self.app.post('/api/group/update_file_content', headers={'token': self.token}, data=json.dumps(data)
                            , content_type='application/json')
        res_dict = json.loads(res.data)
        self.assertIn('code', res_dict)
        self.assertEqual(res_dict['code'], 200)


if __name__ == '__main__':
    unittest.main()