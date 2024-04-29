# models postgreSQL
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
    return 'posts/post_{0}/{1}'.format(instance.post_id.id, filename)

class MediaOfPosts(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    media = models.FileField(upload_to=post_directory_path, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['post_id'])
        ]


class PostIsWatched(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['post_id', 'user_id'])
        ]
        unique_together = ('post_id', 'user_id')

# model mongodb      
from django_mongoengine import fields
from reactions.models import ReactionNumberInfo
class PostsInfo(ReactionNumberInfo):
    id = fields.SequenceField(primary_key=True)
    posts_id = fields.IntField(default=0)
    number_of_comments = fields.IntField(default=0)
    number_of_shares = fields.IntField(default=0)
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def setPostsId(self, posts_id):
        self.posts_id = posts_id
       
    def inc_comment(self):
        self.update(__raw__={'$inc': {'number_of_comments': 1}})
    
    def inc_share(self):
        self.update(__raw__={'$inc': {'number_of_shares': 1}})
    
    def dec_comment(self):
        self.update(__raw__={'$inc': {'number_of_comments': -1}})        
    
    def dec_share(self):
        self.update(__raw__={'$inc': {'number_of_shares': -1}})
        
    
    meta = {
        'db': 'social_network',
        'collection': 'postsinfo',
        'indexes': [
            'posts_id',
        ]
    }