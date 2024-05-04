# # models postgreSQL
# from django.db import models
# from users.models import User
# # Create your models here.
# class Posts(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, null=True, blank=True)
#     content = models.TextField(null=True, blank=True)
#     status = models.CharField(max_length=10, default='public')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['user_id']),
#             models.Index(fields=['id'])
#         ]


# def post_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
#     return 'posts/post_{0}/{1}'.format(instance.post_id.id, filename)

# class MediaOfPosts(models.Model):
#     post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
#     media = models.FileField(upload_to=post_directory_path, null=True, blank=True)
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['post_id'])
#         ]


# class PostIsWatched(models.Model):
#     post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_watched = models.BooleanField(default=False)
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['post_id', 'user_id'])
#         ]
#         unique_together = ('post_id', 'user_id')

# model mongodb      
from django_mongoengine import fields, Document
from mongoengine.fields import EmbeddedDocumentField
from userprofiles.models import UserBasicInfo
from reactions.model_inheritance import ReactionNumberInfo
from django.core.files.storage import default_storage


class Posts(ReactionNumberInfo):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    
    title = fields.StringField(max_length=100, null=True, blank=True)
    content = fields.StringField(null=True, blank=True)
    status = fields.StringField(max_length=10, default='public') # public, private
    
    number_of_comments = fields.IntField(default=0)
    number_of_shares = fields.IntField(default=0)
    
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        
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
        'collection': 'posts',
        'indexes': [
            'user.id',
            'id'
        ]
    }
    
class PostIsWatched(Document):
    id = fields.SequenceField(primary_key=True)
    post_id = fields.IntField()
    user_id = fields.IntField()
    time_watched = fields.DateTimeField()
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
     
    meta = {
        'db': 'social_network',
        'collection': 'postiswatched',
        'indexes': [
            'post_id',
            'user_id'
        ]
    }

class MediaOfPosts(Document):
    id = fields.SequenceField(primary_key=True)
    post_id = fields.ReferenceField(Posts)
    media = fields.StringField()
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'mediaofposts',
        'indexes': [
            'post_id'
        ]
    }

    def save_media(self, file):
        # Save the file to the default storage
        path = 'posts/post_{0}/{1}'.format(self.post_id.id, file.name)
        
        file_name = default_storage.save(path, file)
        
        # Save the path of the file in the database
        self.media = file_name
        self.save()
    
    def delete_media(self):
        # Delete the file from the storage
        default_storage.delete(self.media)
        
        # Delete the path of the file in the database
        self.delete()


def updateProfilePosts(user_id, userbasicinfo):
    try:
        posts = Posts.objects(__raw__={'user.id': user_id})
        
        for post in posts:
            post.update(__raw__={'$set': {'user': userbasicinfo}})
    except Exception as e:
        print("updateProfileNotification", e)
        return False