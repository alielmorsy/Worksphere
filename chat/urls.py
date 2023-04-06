from django.urls import path, include

from .views import *

channel_patterns = [
    path("create/", CreateChannelView.as_view()),
    path(r"/<str:company_id>",GetAllChannels.as_view())
]

urlpatterns = [
    path("channels", include(channel_patterns)),
    path("message/", SendMessageView.as_view()),
]
