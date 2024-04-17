from django.contrib import admin
from .models import UserProfile, ImageProfile, Image
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ImageProfile)
admin.site.register(Image)