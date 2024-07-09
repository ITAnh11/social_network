from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime
import logging
logger=logging.getLogger(__name__)
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
    def __str__(self):
        return f"{self.email}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        logger.info(f"Password updated for user: {self.email}")
    
    def check_password(self, raw_password):
        is_valid = check_password(raw_password, self.password)
        if is_valid:
            logger.info(f"Password checked successfully for user: {self.email}")
        else:
            logger.warning(f"Invalid password provided for user: {self.email}")
        return is_valid
    
    def set_last_login(self):
        self.last_login = datetime.datetime.now()
        logger.info(f"Last login updated for user: {self.email}")
  
