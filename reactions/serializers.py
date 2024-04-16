from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Reactions

class ReactionsSerializer(DocumentSerializer):
    class Meta:
        model = Reactions
        fields = '__all__'
    