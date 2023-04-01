from django.contrib.auth import authenticate, get_user_model
from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User
from .exceptions import InvalidCredentialsException, RegisterException


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
    username = serializers.CharField(max_length=32)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password=validated_data['password'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        email=validated_data['email'])
        return user

    def validate_username(self, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            pass
        if user:
            raise RegisterException()
        return username

    class Meta:
        model = get_user_model()
        fields = ["username", "password", "first_name", "last_name", "email"]
        write_only_fields = ('password',)
        read_only_fields = ('_id',)
