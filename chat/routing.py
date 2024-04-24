from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/notification/<int:channel_id>/', ChatConsumer.as_asgi()),
]