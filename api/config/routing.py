from django.urls import re_path
from websocket.consumers import CSVDataConsumer

websocket_urlpatterns = [
    re_path("api/v1/ws", CSVDataConsumer.as_asgi()),
]
