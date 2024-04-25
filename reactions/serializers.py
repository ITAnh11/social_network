from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Reactions, ReactionNumber

class ReactionsSerializer(DocumentSerializer):
    class Meta:
        model = Reactions
        fields = '__all__'

class ReactionNumberSerializer(DocumentSerializer):
    class Meta:
        model = ReactionNumber
        fields = '__all__'