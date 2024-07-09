from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import ReactNotifitions, CommentNotifications, AddFriendNotifications

class ReactNotifitionsSerializer(DocumentSerializer):
    class Meta:
        model = ReactNotifitions
        fields = '__all__'

class CommentNotificationsSerializer(DocumentSerializer):
    class Meta:
        model = CommentNotifications
        fields = '__all__'

class AddFriendNotificationsSerializer(DocumentSerializer):
    class Meta:
        model = AddFriendNotifications
        fields = '__all__'