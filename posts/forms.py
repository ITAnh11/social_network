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

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['content', 'status']
        
    def save(self, user):
        content = self.cleaned_data['content']
        
        post = Posts.objects.create(
            user_id=user,
            content=content,
            status='public'
        )
        
        return post