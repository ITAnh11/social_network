from rest_framework import serializers
from .models import Posts, MediaOfPosts

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class MediaOfPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaOfPosts
        fields = '__all__'