from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Reactions
from .model_inheritance import ReactionNumberInfo

class ReactionsSerializer(DocumentSerializer):
    class Meta:
        model = Reactions
        fields = '__all__'

class ReactionNumberInfoSerializer(DocumentSerializer):
    class Meta:
        model = ReactionNumberInfo
        fields = ['number_of_reactions']