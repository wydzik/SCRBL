from django.urls import re_path

from main import consumers

channel_routing = {
    'websocket.connect': consumers.GameConsumer.connect,
    'websocket.receive': consumers.GameConsumer.receive,
    'websocket.disconnect': consumers.GameConsumer.disconnect
}

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<gameroom_name>\w+)/$', consumers.GameConsumer),
]