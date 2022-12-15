
import unittest
from flask import jsonify
import json
from faker import Faker
from app import app

class TestClass(unittest.TestCase):
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
        print(type(res))
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
        print(data_list)
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

    # def test_register(self):
    #     self.app.post('/api/user/captcha', data=json.dumps({'email': 'test@test.com', 'operation': 'register'}), content_type='application/json')
    #     captcha = EmailCaptchaModel.query.filter_by(EmailCaptchaModel.email=='test@test.com').first().captcha
    #     data = {
    #         'email': '2826232264@qq.com',
    #         'password': '200212',
    #         'captcha': captcha,
    #         'password_confirm': '200212',
    #         'username': 'test'
    #     }
    #     res = self.app.post('/api/user/register', data=json.dumps(data), content_type='application/json')
    #     res_dict = json.loads(res.data)
    #     self.assertIn('code', res_dict)
    #     self.assertEqual(res_dict['code'], 200)


if __name__ == '__main__':
    unittest.main()