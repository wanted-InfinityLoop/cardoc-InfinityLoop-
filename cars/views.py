import json
import requests

from django.views         import View
from django.http.response import JsonResponse
from django.db import transaction

from core.decorators import login_decorator
from core.validator  import tire_validator
from users.models    import User
from cars.models     import Trim, Tire, Car


class TireInfoView(View):
    @login_decorator
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)

            trim = Trim.objects.get(user__id=user.id)

            tires = Tire.objects.filter(trim__id=trim.id)

            data = []

            for tire in tires:
                if tire.name[-1] == "전":
                    front_tire = {
                        "name"         : tire.name,
                        "width"        : tire.width,
                        "aspect_ratio" : tire.aspect_ratio,
                        "wheel_size"   : tire.wheel_size
                    }
                    data.append(front_tire)

                if tire.name[-1] == "후":
                    rear_tire = {
                        "name"         : tire.name,
                        "width"        : tire.width,
                        "aspect_ratio" : tire.aspect_ratio,
                        "wheel_size"   : tire.wheel_size
                    }
                    data.append(rear_tire)

            return JsonResponse({"tire_info" : data}, status=200)

        except Trim.DoesNotExist:
            return JsonResponse({"message": "TRIM_DOES_NOT_EXIST"}, status=500)

    def post(self, request):
        try:
            datas = json.loads(request.body)

            if len(datas) > 5 :
                return JsonResponse({"message": "INVALID_DATA_LENGTH"}, status=400)

            with transaction.atomic():
                for data in datas:
                    user = User.objects.get(id=data["id"])
                    
                    request_tire_info = requests.get(
                        f"https://dev.mycar.cardoc.co.kr/v1/trim/{data['trimId']}",
                        headers={"Accept": "application/json"}
                        )

                    response = request_tire_info.json()
                    
                    brand    = response.get("brandName")
                    model    = response.get("modelName")
                    submodel = response.get("submodelGroupName")
                    year     = response.get("yearType")

                    car, _ = Car.objects.get_or_create(brand=brand, model=model, submodel=submodel, year=year)

                    trim, _ = Trim.objects.get_or_create(id=data["trimId"], user=user, car=car)

                    front_tire       = response.get("spec").get("driving").get("frontTire")
                    front_tire_value = front_tire.get("value")

                    rear_tire       = response.get("spec").get("driving").get("rearTire")
                    rear_tire_value = rear_tire.get("value")

                    if not (tire_validator(front_tire_value) and tire_validator(rear_tire_value)):
                        return JsonResponse({"message": "INVALID FORMAT"}, status=500)

                    front_splited_value = front_tire_value.split("/")

                    rear_splited_value = rear_tire_value.split("/")

                    Tire.objects.get_or_create(
                        name        =front_tire.get("name"),
                        width       =front_splited_value[0],
                        aspect_ratio=front_splited_value[1].split("R")[0],
                        wheel_size  =front_splited_value[1].split("R")[1],
                        trim        =trim
                    )

                    Tire.objects.get_or_create(
                        name        =rear_tire.get("name"),
                        width       =rear_splited_value[0],
                        aspect_ratio=rear_splited_value[1].split("R")[0],
                        wheel_size  =rear_splited_value[1].split("R")[1],
                        trim        =trim
                    )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "USER_DOES_NOT_EXIST"}, status=500)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
