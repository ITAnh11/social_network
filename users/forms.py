from django import forms
from .models import MediaProfile

class MediaProfileForm(forms.ModelForm):
    class Meta:
        model = MediaProfile
        fields = ['avatar', 'background']
        