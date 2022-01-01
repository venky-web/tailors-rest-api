from django.conf import settings
from django.contrib.auth import get_user_model
import datetime

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


def generate_access_token(user):
    """Generates a new access token"""
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5)
    utc_time = datetime.datetime.utcnow()
    access_token_payload = {
        "user_id": user["id"],
        "expiry": expiry_time.timestamp() * 1000,
        "iat": utc_time.timestamp() * 1000
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")

    return access_token


def generate_refresh_token(user):
    """Generates a new refresh token"""
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    utc_time = datetime.datetime.utcnow().timestamp() * 1000
    refresh_token_payload = {
        "user_id": user["id"],
        "expiry": expiry_time.timestamp() * 1000,
        "iat": utc_time
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token


# class CSRFCheck(CsrfViewMiddleware):
#     """CSRF Middleware to check CSRF COOKIE"""
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def _reject(self, request, reason):
#         return reason


class JWTAuthentication(BaseAuthentication):
    """Authenticates every request"""
    def authenticate(self, request):
        auth_headers = request.headers.get("Authorization")
        if not auth_headers:
            return None

        try:
            access_token = auth_headers.split(" ")[1]
            jwt_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access token is expired")
        except IndexError:
            raise exceptions.AuthenticationFailed("Access token prefix is missing")

        user = get_user_model().objects.filter(id=jwt_payload["user_id"]).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is not active")

        # self.enforce_csrf(request)
        return user, None

    # def enforce_csrf(self, request):
    #     check = CSRFCheck()
    #     check.process_request(request)
    #     reason = check.process_view(request, None, (), {})
    #     print(reason)
    #     if reason:
    #         raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
