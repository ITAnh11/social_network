from rest_framework import serializers
from .models import Message, Conversation
from userprofiles.models import UserProfile, ImageProfile

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProfile
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    receiver_info = UserInfoSerializer()
    sender_info = UserInfoSerializer()
    receiver_pic = ImageSerializer()
    sender_pic = ImageSerializer()

    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'user', 'sender', 'sender_info', 'sender_pic', 'receiver', 'receiver_info', 'receiver_pic', 'content', 'status', 'is_read', 'created_at']