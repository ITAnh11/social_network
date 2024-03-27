from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

from users.models import User
from .models import Posts, MediaOfPosts

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

class PostsView(APIView):
    def get(self, request):
        user = get_user(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        posts = Posts.objects.filter(user=user).all()
        
        data = []
        
        for post in posts:
            data.append({
                'content': post.content,
                'user': post.user.username,
                'media': [media.url for media in post.media.all()]
            })
        
        return Response({'posts': data})
    
    def post(self, request):
        user = get_user(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        print(request.data)
        Posts.objects.create(
            user=user,
            content=request.data['content']
        )
        
        return Response({'success': 'Post created!'})

