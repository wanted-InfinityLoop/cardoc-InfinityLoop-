import json
import bcrypt
import jwt
from datetime import datetime, timedelta

from django.test import TestCase, Client

from my_settings import MY_SECRET_KEY, ALGORITHM
from .models     import User


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(
            id      ="테스트유저1",
            password="asdfA3df@sdf"
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_post_signup_success(self):
        data = {
            "id"      : "테스트유저",
            "password": "xcFv3zAf@s"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_post_signup_registered_user(self):
        data = {
            "id"      : "테스트유저1",
            "password": "xcFv3zAf@s"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "REGISTERED_USER"})

    def test_post_signup_invalid_password_format(self):
        data = {
            "id"      : "테스트유저",
            "password": "xcFvzAfs"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_FORMAT"})

    def test_post_signup_key_error(self):
        data = {
            "ids"     : "테스트유저1",
            "password": "xcFv3zAf@s"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create(
            id      ="테스트유저1",
            password=bcrypt.hashpw("asdfA3df@sdf".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        )

        self.access_token = jwt.encode({
            "id"  : user.id,
            "exp" : datetime.now() + timedelta(hours=6) 
            }, MY_SECRET_KEY, ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()

    def test_post_login_success(self):
        data = {
            "id"      : "테스트유저1",
            "password": "asdfA3df@sdf"
        }

        response = self.client.post(
            "/users/login", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS", "token": self.access_token})
    
    def test_post_user_does_not_exist(self):
        data = {
            "id"      : "테스트유저",
            "password": "asdfA3df@sdf"
        }

        response = self.client.post(
            "/users/login", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "USER_DOES_NOT_EXIST"})
    
    def test_post_login_failed(self):
        data = {
            "id"      : "테스트유저1",
            "password": "asdfA3df@sdf1"
        }

        response = self.client.post(
            "/users/login", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "LOGIN_FAILED"})

    def test_post_key_error(self):
        data = {
            "ids"     : "테스트유저1",
            "password": "asdfA3df@sdf1"
        }

        response = self.client.post(
            "/users/login", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
