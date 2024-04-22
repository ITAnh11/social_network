from django.db import models
from users.models import User

# Create your models here.
class Posts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['id'])
        ]


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return 'media/posts/post_{0}/{1}'.format(instance.post_id.id, filename)

class MediaOfPosts(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    media = models.FileField(null=True, blank=True)
        
    class Meta:
        indexes = [
            models.Index(fields=['post_id'])
        ]