from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from rest_framework import serializers

from user import models


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

        if not user:
            message = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(message, code="authentication")

        attrs["user"] = user
        return attrs


class CustomerSerializer(serializers.ModelSerializer):
    """serializes customer obj"""

    class Meta:
        model = models.Customer
        fields = "__all__"
        read_only_fields = ("user", "id", "created_on", "updated_on", "created_by", "updated_by")
        depth = 1

    def validate(self, attrs):
        """Validates the data before creating"""
        full_name = attrs.get("full_name")
        display_name = attrs.get("display_name")
        if not full_name and not display_name:
            message = _("At least full name or display name is required to create the user")
            return serializers.ValidationError(message)

        return attrs

    def create(self, validated_data):
        """creates a new customer in db"""
        user = get_user_model().objects.create_user(**validated_data)
        validated_data["updated_on"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
        else:
            request_user = validated_data.pop("request_user")
        validated_data["created_by"] = request_user.id
        validated_data["updated_by"] = request_user.id
        validated_data["user"] = user
        customer = models.Customer.objects.create(**validated_data)
        return customer

    def update(self, instance, validated_data):
        """updates a customer obj"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
        else:
            request_user = validated_data.pop("request_user")
        for key in validated_data:
            instance[key] = validated_data.get(key, instance[key])

        instance["updated_by"] = request_user.id
        instance["updated_on"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        print(validated_data)
        instance.save()

        return instance
