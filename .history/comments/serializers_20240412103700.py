from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Comments

class CommentsSerializer(DocumentSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
    