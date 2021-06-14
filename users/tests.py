from codecs import decode, encode
import json
from os import access
import re
import unittest
import bcrypt
import jwt

from django.test import (
        TestCase, 
        Client
        )
from unittest.mock import MagicMock, patch
from .models import User

from my_settings import SECRET_KEY, algorithm

class SignUpTest(TestCase):
    def setUp(self):
        
        User.objects.create(
            email          = 'test1@test.com',
            password       = '12341234',
            name           = '김김김'
        )

    def tearDown(self):
        User.objects.all().delete()
        
    def test_success_signup(self):
        client = Client()        
        
        data = {
                'email'          : 'test2@gmail.com', 
                'password'       : '12341234', 
                'password_check' : '12341234', 
                'name'           : '김김김'
                }

        response = client.post('/users/users', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : "SUCCESS"})

    def test_fail_email_exist(self):
        client = Client()
        
        data = {
                'email'          : 'test1@test.com',
                'password'       : '12341234',
                'password_check' : '12341234',   
                'name'           : '김김김'
                }

        response = client.post('/users/users', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'EXIST_EMAIL'})

    def test_fail_password_check(self):
        client = Client()

        data = {
                'email' : 'wecode1@gmail.com',
                'password' : '12341234',
                'password_check' : '123412',
                'name' : '김김김'
                }

        response = client.post('/users/users', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'CHECK_YOUR_INPUT'})

    def test_email_vaildation_check(self):
        client = Client()
        data = {
                'email' : 'wecode2gmail.com',
                'password' : '12341234',
                'password_check' : '12341234',
                'name' : '김김김'
                }

        response = client.post('/users/users', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_EMAIL_FORM'})

    def test_password_vaildation_check(self):
        client = Client()
        data = {
                'email' : 'wecode2@gmail.com',
                'password' : '!!!!!!!',
                'password_check' : '!!!!!!!',
                'name' : '김김김'
                }

        response = client.post('/users/users', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_PASSWORD_FORM'})

class LoginTest(TestCase):
    def setUp(self):
        User.objects.create(
                email = 'test1@test.com',
                password = bcrypt.hashpw('12341234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name = '고양이'
                )

    def tearDown(self):
        User.objects.all().delete()

    def test_success_signin(self):
        client = Client()

        data = {
                'email' : 'test1@test.com',
                'password' : '12341234'
                }

        user_email = User.objects.get(email='test1@test.com')
        access_token = jwt.encode({'id' : user_email.id}, SECRET_KEY, algorithm)

        response = client.post('/users/login', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'access_token' : access_token,
            'message' : 'SUCCESS'
            }
        )

    def test_fail_signin_not_match_email(self):
        client = Client()

        data = {
                'email' : 'we@gmail.com',
                'password' : '12341234'
                }
        response = client.post('/users/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_EMAIL'})

    def test_fail_signin_not_match_password(self):
        client = Client()

        data = {
                'email' : 'test1@test.com',
                'password' : '1234123'
                }

        response = client.post('/users/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_PASSWORD'})
        
    def test_fail_signin_not_input_email(self):
        client = Client()
            
        data = {
            'email' : '',
            'password' : '12341234'
            }
            
        response = client.post('/users/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
            
    def test_fail_signin_not_input_password(self):
       client = Client()
       
       data = {
           'email' : 'test1@gmail.com',
           'password' : ''
           }
       
       response = client.post('/users/login', json.dumps(data), content_type='application/json')
       self.assertEqual(response.status_code, 400)




class KakaoTestCase(TestCase):
    def setUp(self):
        User.objects.create(
                email = 'test@gmail.com',
                password = bcrypt.hashpw('12341234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name = '유동헌'
                )
        
    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_success_kakao_signin(self, mocked_requests):
        client = Client()

        class FakeResponse:
            def json(self):
                return {
                    "id" : "1234",
                    "properties"    : {
                        "nickname" : "유동헌" 
                        },
                    "kakao_account" : {
                        "email" : "test@gmail.com" 
                        }
                    }
        print(json)
                
        mocked_requests.post = MagicMock(return_value = FakeResponse())
        # access_token = jwt.encode({'id' : User.objects.get(email='test@gmail.com').id}, SECRET_KEY, algorithm)
        # access_token = jwt.encode({'id' : '1234'}, SECRET_KEY, algorithm)
        # access_token = jwt.encode({'id' : User.objects.get(id=FakeResponse.json(self)['id']).id}, SECRET_KEY, algorithm)
        header   = {'HTTP_Authorization' : 'access_token'}
        
        response = client.post('/users/kakaosignin', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "access_token": response.json()['access_token']
            }
        )
        print(response.json())
        # self.assertEqual(response.json(),
        #         {
        #             "access_token" : access_token,
        #         }
        # )
        
    # @patch("users.views.requests")
    # def test_fail_kakao_signin_invalid_token(self, mocked_requests):
    #     client = Client()
    #     class FakeResponse:
    #         def json(self):
    #             return(
    #                 {
    #             }
    #                 )
                
    #     mocked_requests.post = MagicMock(return_value = FakeResponse())
        
    #     header       = {'HTTP_Authorization' : 'token'}
    #     response     = client.post('/users/kakaosignin', content_type='application/json', **header)
        
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(),
    #             {
    #                 "message" : "INVALID_TOKEN",
    #             }
    #     )
        
if __name__ == '__main__':
    unittest.main