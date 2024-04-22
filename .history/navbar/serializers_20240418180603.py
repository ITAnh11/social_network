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



