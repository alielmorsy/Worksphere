from django.contrib import admin
from django.urls import path, include
from .views import Login , verify
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView , TokenVerifyView

urlpatterns = [
    path("", csrf_exempt(Login.as_view())),
    path("verify/",csrf_exempt(verify.as_view())),
]
