from django.db import models
from users.models import User

# Create your models here.
class Posts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return 'post_{0}/{1}'.format(instance.post_id.id, filename)

class MediaOfPosts(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    media = models.FileField(upload_to=post_directory_path)

    def __str__(self):
        return self.post_id.title