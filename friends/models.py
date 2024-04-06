from django.db import models
from users.models import User
# Create your models here.
class FriendRequest(models.Model):
    from_id = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_id = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=45, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Friendship(models.Model): 
    user_id1 = models.ForeignKey(User, related_name='friendship_user1', on_delete=models.CASCADE)
    user_id2 = models.ForeignKey(User, related_name='friendship_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)