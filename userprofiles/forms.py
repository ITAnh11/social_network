from django.forms import ModelForm

from .models import ImageProfile

class ImageProfileForm(ModelForm):
    class Meta:
        model = ImageProfile
        fields = ['avatar', 'background']
    