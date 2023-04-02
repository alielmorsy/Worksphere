from django.urls import path, include

from .views import *

urlpatterns = [
    path("channel/", channelView.as_view()),
    path("message/", messageView.as_view()),
    #path("test", test.as_view()),
    #path("register", RegisterView.as_view())
]