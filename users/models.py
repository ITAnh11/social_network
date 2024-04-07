from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255, null=False)
    confirm_password = models.CharField(max_length=255, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    _destroy = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]
    
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def set_last_login(self):
        self.last_login = datetime.datetime.now()
  
