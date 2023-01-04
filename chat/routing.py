from django.urls import path
from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
  path('ws/<str:room_name>/', consumers.ChatRoomConsumer.as_asgi()),
]