from django.urls import path, include, re_path

from .views import *

channel_patterns = [
    path("create/", CreateChannelView.as_view()),
    re_path(r"<str:company_id>",GetAllChannels.as_view()),
    re_path(r"<str:channel_id>/<int:page>",GetChannelMessagesView.as_view()),

]


urlpatterns = [
    path("channels/", include(channel_patterns)),
    #path("message/", SendMessageView.as_view()),
]
