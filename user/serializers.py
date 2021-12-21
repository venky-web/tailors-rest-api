from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for user objects"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "user_type", "joined_on", "id")
        read_only_fields = ("joined_on", "id")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Creates a new user with validated data"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validates serialized data"""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )
        print(user)

        if not user:
            message = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(message, code="authentication")

        attrs["user"] = user
        return attrs
