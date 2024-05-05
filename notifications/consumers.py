import json

from channels.generic.websocket import AsyncWebsocketConsumer
class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.group_name = None
        self.channel_layer_alias = 'redis'
    
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"notification_{self.user_id}"

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        
        print(f"Connected to WebSocket. Group name: {self.group_name}")
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"Disconnected from WebSocket. Group name: {self.group_name}")

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_notification',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            print(f"Invalid JSON: {text_data}")

    # Receive message from room group
    async def send_notification(self, event):
        print(f"Received event: {event}")
        try:
            message = event['message']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({'message': message}))
        except Exception as e:
            print("Invalid event: ", e) 