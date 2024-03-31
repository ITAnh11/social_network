from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

from users.models import User
from .models import Posts, MediaOfPosts

from .serializers import PostsSerializer, MediaOfPostsSerializer

# Create your views here.


def get_user(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
    except jwt.ExpiredSignatureError:
        return None
    
    user = User.objects.get(id=user_id)
    
    return user

class PostsPageView(APIView):
    def get(self, request):
        user = get_user(request)
        
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request, 'posts/posts.html')

class CreatePostsView(APIView):
    def post(self, request):
        user = get_user(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        print(request.data)
        print(request.FILES)
        
        post = self.createPost(user, request)
        self.createMediaOfPost(post, request)     
        
        return Response({'success': 'Post created!'})

    def createPost(self, user, request):
        post = Posts.objects.create(
            user_id=user,
            content=request.data['content'],
            status='public'
        )
        
        post.save()
        
        return post
    
    def createMediaOfPost(self, post, request):
        media = request.FILES.getlist('media')
        if not media:
            return None
        for file in media:
            media = MediaOfPosts.objects.create(
                post_id=post,
                media=file
            )
            
            media.save()

