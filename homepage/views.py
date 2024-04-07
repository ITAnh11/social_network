from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt

from users.views import LogoutView

from posts.models import Posts, MediaOfPosts
from posts.serializers import PostsSerializer, MediaOfPostsSerializer

from common_functions.common_function import getUserProfileForPosts, getTimeDuration

# Create your views here.
class HomePageView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')  
            
        if not token:
            return HttpResponseRedirect(reverse('users:login'))

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
        except jwt.ExpiredSignatureError:
            LogoutView().post(request)
            return HttpResponseRedirect(reverse('users:login'))
            
        return render(request, 'homepage/index.html')

class GetPostsView(APIView):
    def get(self, request):
        
        reponse = Response()
        
        data = []
        
                
        posts = Posts.objects.values('id', 'title', 'content', 'status', 'created_at').order_by('-created_at')[:50]  
        
        for post in posts:
            
            posts_data = PostsSerializer(post).data
            
            userDataForPosts = getUserProfileForPosts(post.get('user_id'))
            
            media = MediaOfPosts.objects.filter(post_id=post.get('id'))
            media_data = MediaOfPostsSerializer(media, many=True).data
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts
            posts_data['created_at'] = getTimeDuration(post.get('created_at'))
        
            data.append(posts_data)
            
        reponse.data = {
            'posts': data
        }

        return reponse