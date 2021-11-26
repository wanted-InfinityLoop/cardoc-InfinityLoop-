import json

from django.test import TestCase, Client

from users.models import User


class TireInfoView(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.bulk_create(
            [
                User(id="test1", password="abcABC1#"),
                User(id="test2", password="abcABC2#"),
                User(id="test3", password="abcABC3#"),
                User(id="test4", password="abcABC4#"),
                User(id="test5", password="abcABC5#"),
                User(id="test6", password="abcABC6#"),
            ]
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_post_tire_info_success(self):
        data = [
            {
                "id" : "test1",
                "trimId" : 5000
            },
            {
                "id" : "test2",
                "trimId" : 9000
            },
            {
                "id" : "test3",
                "trimId" : 11000
            },
            {
                "id" : "test4",
                "trimId" : 15000
            },
            {
                "id" : "test5",
                "trimId" : 16000
            },
        ]

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_post_tire_info_invalid_data_length(self):
        data = [
            {
                "id" : "test1",
                "trimId" : 5000
            },
            {
                "ids" : "test2",
                "trimId" : 9000
            },
            {
                "id" : "test3",
                "trimId" : 11000
            },
            {
                "id" : "test4",
                "trimId" : 15000
            },
            {
                "id" : "test5",
                "trimId" : 16000
            },
            {
                "id" : "test6",
                "trimId" : 17000
            },
        ]

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_DATA_LENGTH"})

    def test_post_tire_info_user_does_not_exist(self):
        data = [
            {
                "id" : "test1",
                "trimId" : 5000
            },
            {
                "id" : "test2",
                "trimId" : 9000
            },
            {
                "id" : "test3",
                "trimId" : 11000
            },
            {
                "id" : "test4",
                "trimId" : 15000
            },
            {
                "id" : "test7",
                "trimId" : 16000
            },
        ]

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "USER_DOES_NOT_EXIST"})

    def test_post_tire_info_key_error(self):
        data = [
            {
                "id" : "test1",
                "trimId" : 5000
            },
            {
                "ids" : "test2",
                "trimId" : 9000
            },
            {
                "id" : "test3",
                "trimId" : 11000
            },
            {
                "id" : "test4",
                "trimId" : 15000
            },
            {
                "id" : "test7",
                "trimId" : 16000
            },
        ]

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

