from django.urls import path, include

from .views import *

urlpatterns = [
    path("channel/", CreateChannelView.as_view()),
    path("message/", SendMessageView.as_view()),
    #path("test", test.as_view()),
    #path("register", RegisterView.as_view())
]