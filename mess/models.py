from django.db import models

class Conversation(models.Model):
    conversation_id = models.IntegerField(unique=True)
    title = models.TextField(max_length=255)
    
