import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from core.validator import password_validator
from .models import User


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data['id']
            raw_password = data['password']

            if User.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "REGISTERED_USER"}, status=400)

            if not password_validator(raw_password):
                return JsonResponse({"message": "INVALID_FORMAT"}, status=400)

            password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            User.objects.create(id=user_id, password=password)

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

