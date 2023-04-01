from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .seralizers import LoginSerializer, RegisterSerializer
from .services.loginService import LoginService


class LoginView(APIView):
    """
    Login API End Point get should return a bad HTML PAGE.
    The Posted Data should be username, and password it uses
    LoginSerializer to validate the request and  authenticate the user.
    Then Create A token and send it with the refresh token.

    @author Ali Elmorsy
    """

    raise_exception = True

    def __init__(self):
        super().__init__()
        self.service = LoginService()

    def get(self, request):
        return render(request, "As.html")

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        response = {
            "access": token.access_token,
            "refresh": str(token)
        }
        return Response(response)


class RegisterView(APIView):
    raise_exception = True

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        return Response("asdwd")


class test(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'message': 'success'})
