from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat_notification/<int:channel_id>/', ChatConsumer.as_asgi()),
]