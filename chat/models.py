from django.db import models
from users.models import User
from userprofiles.models import UserProfile
# Create your models here.

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
    
