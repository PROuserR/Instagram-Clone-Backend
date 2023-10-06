from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<peer_id>\w+)/(?P<my_id>)\w+/$', consumers.ChatRoomConsumer.as_asgi()),
    path('ws/online_users', consumers.OnlineUsersConsumer.as_asgi()),
    ]