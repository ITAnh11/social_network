from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt

from users.views import LogoutView

from posts.models import Posts, MediaOfPosts
from posts.serializers import PostsSerializer, MediaOfPostsSerializer

from userprofiles.serializers import UserProfileSerializer, ImageProfileSerializer

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
     
        posts = Posts.objects.prefetch_related('user_id__userprofile_set', 'user_id__imageprofile_set', 'mediaofposts_set').order_by('-created_at')[:50]

        for post in posts:
            
            posts_data = PostsSerializer(post).data

            userProfile = UserProfileSerializer(post.user_id.userprofile_set.first())
            imageProfile = ImageProfileSerializer(post.user_id.imageprofile_set.first())

            userDataForPosts = {
                "id": post.user_id.id,
                "name": f"{userProfile.data.get('first_name')} {userProfile.data.get('last_name')}",
                "avatar": imageProfile.data.get('avatar')
            }
            
            # media = posts.mediaofposts_set.all()
            media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts
            posts_data['created_at'] = getTimeDuration(post.created_at)
        
            data.append(posts_data)
            
        reponse.data = {
            'posts': data
        }

        return reponse