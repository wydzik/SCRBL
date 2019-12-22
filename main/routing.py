from django.urls import re_path

from main import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<gameroom_name>\w+)/$', consumers.GameConsumer),
]