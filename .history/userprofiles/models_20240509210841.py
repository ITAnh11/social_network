from django.db import models

from users.models import User

# Create your models here.
def media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/<filename>
    return 'users/userprofile_{0}/{1}'.format(instance.user_id.id, filename)

class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=15, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    work = models.CharField(max_length=255, blank=True, null=True)
    address_work = models.CharField(max_length=255, blank=True, null=True)
    place_birth = models.CharField(max_length=255, blank=True, null=True)
    social_link = models.CharField(max_length=255, blank=True, null=True)
    _destroy = models.BooleanField(default=False, null = True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id'])
        ]

class ImageProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar= models.ImageField(upload_to=media_directory_path, blank=True, default="users/default/avatar_default.png")
    background = models.ImageField(upload_to=media_directory_path, blank=True, default="users/default/background_default.jpg")
    _destroy = models.BooleanField(default=False, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id'])
        ]
    
# class LinkProfile(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     link = models.CharField(max_length=255, null=False)
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['user_id'])
#         ]

# model mongodb
from django_mongoengine import fields, EmbeddedDocument

class UserBasicInfo(EmbeddedDocument):
    id = fields.IntField()
    name = fields.StringField()
    avatar = fields.StringField()
        