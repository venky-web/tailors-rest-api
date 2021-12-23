from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import exceptions
import jwt

from user.serializers import UserSerializer, AuthTokenSerializer
from user.auth import generate_access_token, generate_refresh_token
from user.models import User


class CreateUserView(generics.CreateAPIView):
    """view to create a new user"""
    authentication_classes = []
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """view to login to app"""
    permission_classes = (AllowAny,)
    authentication_classes = []

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        """Authenticates a user with provided credentials"""
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user = User.objects.filter(email=email).first()
            user = UserSerializer(user).data

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            response = Response()
            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            response.data = {
                'access_token': access_token,
                'user': user,
            }

            return response

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def get_access_token(request):
    """returns refresh token for authenticated users"""
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed("Authentication credentials are not provided")

    try:
        jwt_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Refresh token is expired. Please login again")

    user = get_user_model().objects.filter(id=jwt_payload["user_id"]).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found")
    elif not user.is_active:
        raise exceptions.AuthenticationFailed("User is inactive")

    user = UserSerializer(user).data
    access_token = generate_access_token(user)
    return Response({'access_token': access_token})


class UserList(generics.ListAPIView):
    """View to list users"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
