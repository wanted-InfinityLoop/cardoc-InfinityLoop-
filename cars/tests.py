import json
import jwt
import bcrypt

from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from users.models import User
from cars.models  import Car, Trim, Tire
from my_settings  import MY_SECRET_KEY, ALGORITHM


class TireInfoView(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.bulk_create(
            [
                User(id="test1", password=bcrypt.hashpw("abcABC1#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")),
                User(id="test2", password=bcrypt.hashpw("abcABC2#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")),
                User(id="test3", password=bcrypt.hashpw("abcABC3#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")),
                User(id="test4", password=bcrypt.hashpw("abcABC4#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")),
                User(id="test5", password=bcrypt.hashpw("abcABC5#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")),
                User(id="test6", password=bcrypt.hashpw("abcABC6#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")),
            ]
        )
        User.objects.create(id="test8", password=bcrypt.hashpw("abcABC8#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
        
        User.objects.create(id="test9", password=bcrypt.hashpw("abcABC9#".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))

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
        self.assertEqual(response.status_code, 500)

    @patch("cars.views.requests")
    def test_post_tire_info_success(self, mock_request):
        class TireInfoMockResponse:
            def json(self):
                return {
                    "brandName": "기아",
                    "modelName": "오피러스",
                    "submodelGroupName": "오피러스",
                    "yearType": "2004",
                    "spec" : {
                        "driving": {
                            "frontTire" : {
                                "name": "타이어 전",
                                "value": "225/60R16",
                            },
                            "rearTire" : {
                                "name": "타이어 후",
                                "value": "225/60R16",
                            },
                        }
                    }
                }

        data = [{"id" : "test1", "trimId" : 5000}]

        mock_request.get = MagicMock(return_value=TireInfoMockResponse())

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    @patch("cars.views.requests")
    def test_post_tire_invalid_format(self, mock_request):
        class TireInfoMockResponse:
            def json(self):
                return {
                    "brandName": "기아",
                    "modelName": "오피러스",
                    "submodelGroupName": "오피러스",
                    "yearType": "2004",
                    "spec" : {
                        "driving": {
                            "frontTire" : {
                                "name": "타이어 전",
                                "value": "22560R16",
                            },
                            "rearTire" : {
                                "name": "타이어 후",
                                "value": "22560R16",
                            },
                        }
                    }
                }

        data = [{"id" : "test1", "trimId" : 5000}]

        mock_request.get = MagicMock(return_value=TireInfoMockResponse())

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "INVALID FORMAT"})

    @patch("cars.views.requests")
    def test_post_tire_info_user_does_not_exist(self, mock_request):
        class TireInfoMockResponse:
            def json(self):
                return {
                    "brandName": "기아",
                    "modelName": "오피러스",
                    "submodelGroupName": "오피러스",
                    "yearType": "2004",
                    "spec" : {
                        "driving": {
                            "frontTire" : {
                                "name": "타이어 전",
                                "value": "225/60R16",
                            },
                            "rearTire" : {
                                "name": "타이어 후",
                                "value": "225/60R16",
                            },
                        }
                    }
                }

        data = [{"id" : "test7", "trimId" : 5000}]

        mock_request.get = MagicMock(return_value=TireInfoMockResponse())

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "USER_DOES_NOT_EXIST"})

    @patch("cars.views.requests")
    def test_post_tire_info_key_error(self, mock_request):
        class TireInfoMockResponse:
            def json(self):
                return {
                    "brandName": "기아",
                    "modelName": "오피러스",
                    "submodelGroupName": "오피러스",
                    "yearType": "2004",
                    "spec" : {
                        "driving": {
                            "frontTire" : {
                                "name": "타이어 전",
                                "value": "225/60R16",
                            },
                            "rearTire" : {
                                "name": "타이어 후",
                                "value": "225/60R16",
                            },
                        }
                    }
                }

        data = [{"id" : "test1", "trim_Id" : 5000}]

        mock_request.get = MagicMock(return_value=TireInfoMockResponse())

        response = self.client.post(
            "/cars/tire-info", json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
