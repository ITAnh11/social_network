from django.test import TestCase
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class RedisConnectionTest(TestCase):
    def test_redis_connection(self):
        channel_layer = get_channel_layer("redis")
        async_to_sync(channel_layer.send)('test_channel', {'type': 'test.message', 'text': 'Hello, Redis!'})