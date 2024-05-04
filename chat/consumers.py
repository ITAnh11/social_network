import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['channel_id']}"
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json
        event = {
            'type' : 'send_message',
            'data' : data,
        }
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['data']
        await self.create_message(data=data)
        response_data = {
            'sender_id': data['sender_id'],
            'channel_id': data['channel_id'],
            'message_content': data['message_content'],
        }
        await self.send(text_data=json.dumps({'data': response_data}))
    
    @database_sync_to_async
    def create_message(self, data):
        if not Messeeji.objects(message_content=data['message_content']).exists():
            # print(f"channel: {data['channel_id']}, content: {data['message_content']}")
            new_message = Messeeji(
                sender_id=data['sender_id'],
                channel_id=data['channel_id'],
                message_content=data['message_content'],
                status='visible',
                created_at=datetime.datetime.now(),
                )
            new_message.save()

      
