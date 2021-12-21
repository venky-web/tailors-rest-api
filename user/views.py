from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

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


class UserList(generics.ListAPIView):
    """View to list users"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
