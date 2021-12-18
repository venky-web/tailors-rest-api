import json
import requests

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import pyrebase

import env_variables

# firebase config
firebase = pyrebase.initialize_app(env_variables.FIREBASE_CONFIG)
firebase_auth = firebase.auth()
f_db = firebase.database()


class SignUp(APIView):
    """Creates a new user
                Inputs: email, password, name
    """
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        name = request.data["name"]

        if not email or not password:
            return Response("Email or password is missing", status=status.HTTP_400_BAD_REQUEST)

        email = email.lower()
        try:
            user = firebase_auth.create_user_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            message = "Invalid request"
            if error == "EMAIL_EXISTS":
                message = "Email already exists"
            elif error == "OPERATION_NOT_ALLOWED":
                message = "Operation not allowed"
            elif error == "TOO_MANY_ATTEMPTS_TRY_LATER":
                message = "Too many requests. Please try again later"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            message = "Invalid request"
            return Response({"message": message, "error": e}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": user}, status=status.HTTP_201_CREATED)


class Login(APIView):
    """Login user to firebase
        Inputs: email, password
    """
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        if not email or not password:
            return Response("Email or password is missing", status=status.HTTP_400_BAD_REQUEST)

        email = email.lower()
        try:
            user = firebase_auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            print(e)
            error_json = e.args[1]
            print(error_json)
            message = "Email or password is incorrect"
            return Response(
                f"'message': '{message}', 'error': '{e}'",
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as e:
            message = "Invalid request"
            return Response({"message": message, "error": e}, status=status.HTTP_400_BAD_REQUEST)

        except TypeError as e:
            message = "Internal server error"
            return Response(
                {"message": message, "error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            message = 'Internal Server Error'
            return Response(
                {"message": message, "error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"user": user}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_users(request):
    """Return list of users"""
    users = f_db.child("users").get()
    return Response({"users": users.val()}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_orders(request):
    """Return list of orders"""
    orders = f_db.child("orders").get()
    return Response({"orders": orders.val()}, status=status.HTTP_200_OK)