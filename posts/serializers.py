# from rest_framework import serializers
# from .models import Posts, MediaOfPosts

# class PostsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Posts
#         fields = ['id', 'title', 'content', 'status', 'created_at']

# class MediaOfPostsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MediaOfPosts
#         fields = ['id', 'media']
        

# Serializers for mongodb
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import MediaOfPosts, PostIsWatched, Posts
from django.core.files.storage import default_storage
from rest_framework import serializers

class PostsSerializer(DocumentSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'user', 'title', 'content', 'status', 'created_at', 'number_of_comments', 'number_of_shares', 'number_of_reactions']

class MediaOfPostsSerializer(DocumentSerializer):
    media_url = serializers.SerializerMethodField()
    class Meta:
        model = MediaOfPosts
        fields = ['id', 'media', 'media_url']

    def get_media_url(self, obj):
        if obj.media:
            return default_storage.url(obj.media)
        return None

class PostIsWatchedSerializer(DocumentSerializer):
    class Meta:
        model = PostIsWatched
        fields = ['post_id', 'user_id', 'time_watched']