import json
import jwt

from django.http import JsonResponse

from my_settings  import MY_SECRET_KEY, ALGORITHM
from users.models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            
            if not access_token:
                return JsonResponse({"message": "NOT_FOUND_ACCESS_TOKEN"}, status=400)

            if not access_token.startswith("Bearer "):
                return JsonResponse({"message": "AUTH_ERROR"}, status=401)

            encoded_token = access_token.split(" ")[1]
            payload       = jwt.decode(encoded_token, MY_SECRET_KEY, ALGORITHM)

            user = User.objects.get(id=payload["id"])

            request.user = user

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "TOKEN_EXPIRED"}, status=403)

        except jwt.InvalidAlgorithmError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper
