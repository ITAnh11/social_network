# consumers.py
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.channel_name = f"user_{self.user.id}"
        self.accept()

    def disconnect(self, close_code):
        pass