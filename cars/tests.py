import json
import jwt

from django.test import TestCase, Client

from users.models import User
from cars.models  import Car, Trim, Tire
from my_settings  import MY_SECRET_KEY, ALGORITHM


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
        User.objects.create(id="test8", password="abcABC8#")
        
        User.objects.create(id="test9", password="abcABC9#")

        self.access_token8 = jwt.encode({"id" : "test8"}, MY_SECRET_KEY, ALGORITHM)
        
        self.access_token9 = jwt.encode({"id" : "test9"}, MY_SECRET_KEY, ALGORITHM)

        Car.objects.create(id=1, brand="KIA", model="오피러스", submodel="오피러스", year=2004)

        Trim.objects.create(id=1, user_id="test8", car_id=1)

        Tire.objects.create(name="타이어 전", width=205, aspect_ratio=75, wheel_size=18, trim_id=1)
        
        Tire.objects.create(name="타이어 후", width=205, aspect_ratio=75, wheel_size=18, trim_id=1)

    def tearDown(self):
        Tire.objects.all().delete()
        Trim.objects.all().delete()
        Car.objects.all().delete()
        User.objects.all().delete()

    def test_get_tire_info_success(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token8}"}

        response = self.client.get(
            "/cars/tire-info", content_type="application/json", **header
        )

        data = [
            {
                "name": "타이어 전",
                "width": 205,
                "aspect_ratio": 75,
                "wheel_size": 18
            },
            {
                "name": "타이어 후",
                "width": 205,
                "aspect_ratio": 75,
                "wheel_size": 18
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"tire_info": data})

    def test_get_tire_info_trim_does_not_exist(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token9}"}

        response = self.client.get(
            "/cars/tire-info", content_type="application/json", **header
        )

        self.assertEqual(response.json(), {"message": "TRIM_DOES_NOT_EXIST"})
        self.assertEqual(response.status_code, 400)

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

