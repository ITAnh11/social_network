from django import forms

from .models import MediaOfPosts, Posts

class MediaPostsForm(forms.ModelForm):
    class Meta:
        model = MediaOfPosts
        fields = ['__all__']
        
    def save(self, post):
        media = self.cleaned_data.items()[1]
        
        mediaPosts = MediaOfPosts.objects.create(
            post_id=post,
            media=media
        )
        
        return mediaPosts