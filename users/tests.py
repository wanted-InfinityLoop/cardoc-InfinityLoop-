import json
import bcrypt
import jwt

from django.test import TestCase, Client

from .models import User


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(
            id="테스트유저1",
            password="asdfA3df@sdf"
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_post_signup_success(self):
        data = {
            "id": "테스트유저",
            "password": "xcFv3zAf@s"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_post_signup_registered_user(self):
        data = {
            "id": "테스트유저1",
            "password": "xcFv3zAf@s"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "REGISTERED_USER"})

    def test_post_signup_invalid_password_format(self):
        data = {
            "id": "테스트유저",
            "password": "xcFvzAfs"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_FORMAT"})

    def test_post_signup_key_error(self):
        data = {
            "ids": "테스트유저1",
            "password": "xcFv3zAf@s"
        }

        response = self.client.post(
            "/users/signup", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

