from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<course_id>\d+)/question/(?P<user_id>\d+)/$', consumers.ChatConsumer),
    re_path(r'ws/chat/(?P<course_id>\d+)/discussion/$', consumers.DiscussionConsumer),
]
