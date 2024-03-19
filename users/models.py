from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255, null=False)
    confirm_password = models.CharField(max_length=255, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserProfile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=255, blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', blank=True)
    background_url = models.ImageField(upload_to='backgrounds/', blank=True)
    bio = models.TextField(blank=True)
    school = models.CharField(max_length=255, blank=True)
    work = models.CharField(max_length=255, blank=True)