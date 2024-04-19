from typing import Any
from  django import forms
from django.forms import ModelForm

from .models import ImageProfile
from .models import Image

class ImageProfileForm(ModelForm):
    class Meta:
        model = ImageProfile
        fields = ['avatar', 'background']
    
    def save(self, user):
        imageprofile = ImageProfile.objects.create( user_id=user,
                                                    avatar=self.cleaned_data.get('avatar'),
                                                    background=self.cleaned_data.get('background')
                                                )
        return imageprofile
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file',)