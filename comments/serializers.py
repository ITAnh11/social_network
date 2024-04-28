from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Comments

class CommentsSerializer(DocumentSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'user', 'content', 'to_posts_id', 'to_comment_id', 'created_at']
    