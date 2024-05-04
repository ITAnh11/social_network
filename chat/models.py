from django.db import models
from users.models import User
from userprofiles.models import UserProfile

from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField

# Create your models here.
class Participants(Document):
    channel_id = fields.IntField()
    user_id = fields.IntField()

    def __str__(self):
        return f"c_{self.channel_id}_u_{self.user_id}"
    meta = {
        'db': 'social_network',
        'collection': 'participants',
    }

class UserMess(EmbeddedDocument):
    user_id = fields.IntField()
    name = fields.StringField()
    avatar = fields.StringField()

    def __str__(self):
        return f"{self.user_id}_{self.name}"

class Channel(Document):
    channel_id = fields.SequenceField(primary_key=True)
    created_at = fields.DateTimeField()
    capacity = fields.IntField()
    meta = {
        'db': 'social_network',
        'collection': 'channels',
    }
    def __str__(self):
        return f"channel_{self.channel_id}"

class Messeeji(Document):
    message_id = fields.SequenceField(primary_key=True)
    sender_id = fields.IntField()
    channel_id = fields.IntField()
    message_content = fields.StringField()
    is_read = fields.BooleanField(default=False)
    status = fields.StringField()
    created_at = fields.DateTimeField()

    meta = {
        'db': 'social_network',
        'collection': 'messeejis',
        'indexes': [
        ]
    }
    def __str__(self):
        return f"{self.message_id}_{self.sender.__str__}_{self.channel_id}_{self.message_content}"


class Conversation(models.Model):
    conversation_id = models.IntegerField()
    title = models.TextField(max_length=50)
    status = models.CharField(max_length=10, default='visible') 

    class Meta:
        verbose_name_plural = "Conversation"

    def __str__(self):
        return f"{self.title}"

class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="conv")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    content = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=10, default='visible')
    is_read = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.receiver}"
    
    def sender_info(self):
        sender_info = UserProfile.objects.get(user_id=self.sender)
        return sender_info
    
    def receiver_info(self):
        receiver_info = UserProfile.objects.get(user_id=self.receiver)
        return receiver_info
    
