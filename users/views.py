import json
import bcrypt
import jwt
from datetime import timedelta, datetime

from django.views import View
from django.http  import JsonResponse

from my_settings    import MY_SECRET_KEY, ALGORITHM
from core.validator import password_validator
from .models        import User


class SignupView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user_id      = data['id']
            raw_password = data['password']

            if User.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "REGISTERED_USER"}, status=400)

            if not password_validator(raw_password):
                return JsonResponse({"message": "INVALID_FORMAT"}, status=400)

            salted_password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(id=user_id, password=salted_password)

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(id=data['id'])

            if not bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message": "LOGIN_FAILED"}, status=400)

            access_token = jwt.encode({
                "id" : user.id,
                "exp" : datetime.now() + timedelta(hours=6) 
            }, MY_SECRET_KEY, ALGORITHM)

            return JsonResponse({"message": "SUCCESS", "token": access_token}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "USER_DOES_NOT_EXIST"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


