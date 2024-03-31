from rest_framework import serializers
from .models import Posts, MediaOfPosts

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'content', 'status', 'created_at']

class MediaOfPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaOfPosts
        fields = ['id', 'media']