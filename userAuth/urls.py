from django.urls import path, include

from userAuth.views import *

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("test/", test.as_view()),
    path("register/", RegisterView.as_view())
]
