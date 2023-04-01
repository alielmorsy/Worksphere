from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User
from .exceptions import InvalidCredentialsException


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def _validate_user(self, username, password):
        if not (username or password):
            raise serializers.ValidationError("Enter a phone number or an email and password.")

        return authenticate(username=username, password=password)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = self._validate_user(username, password)
        if not user:
            raise InvalidCredentialsException()

        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]
