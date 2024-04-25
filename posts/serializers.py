from rest_framework import serializers
from .models import Posts, MediaOfPosts

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'title', 'content', 'status', 'created_at']

class MediaOfPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaOfPosts
        fields = ['id', 'media']
        

# Serializers for mongodb
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import PostsInfo

class PostsInfoSerializer(DocumentSerializer):
    class Meta:
        model = PostsInfo
        fields = ['number_of_reactions', 'number_of_comments', 'number_of_shares']
    