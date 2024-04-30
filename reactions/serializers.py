from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Reactions, ReactionNumberInfo

class ReactionsSerializer(DocumentSerializer):
    class Meta:
        model = Reactions
        fields = '__all__'

class ReactionNumberInfoSerializer(DocumentSerializer):
    class Meta:
        model = ReactionNumberInfo
        fields = '__all__'