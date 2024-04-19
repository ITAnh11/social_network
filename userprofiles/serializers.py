from rest_framework import serializers
from .models import UserProfile, ImageProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id', 'first_name', 'last_name', 'phone', 'birth_date', 'gender', 'address', 'bio', 'school', 'work', 'address_work', 'place_birth', 'social_link']
          
    def create(self, validated_data):
        userprofile = self.Meta.model(**validated_data)
        userprofile.save()
        return userprofile

class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProfile
        fields = ['user_id', 'avatar', 'background']
    
    def create(self, validated_data):
        imageprofile = self.Meta.model(**validated_data)
        imageprofile.save()
        return imageprofile