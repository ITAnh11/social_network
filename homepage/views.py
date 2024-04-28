from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt

from users.views import LogoutView

from posts.models import Posts, PostsInfo
from posts.serializers import PostsSerializer, MediaOfPostsSerializer, PostsInfoSerializer

from userprofiles.serializers import UserProfileSerializer, ImageProfileSerializer

from common_functions.common_function import getUser, getTimeDuration

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
    def post(self, request):
        
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        reponse = Response()
        
        data = []
        
        num_posts = Posts.objects.count()
        currentNumberOfPosts = int(request.data.get('current_number_of_posts'))
        
        if currentNumberOfPosts >= num_posts:
            return Response({'error': 'No more posts available'}, status=400)
        # print(num_posts, currentNumberOfPosts)
     
        posts = Posts.objects.prefetch_related('user_id__userprofile_set', 
                                               'user_id__imageprofile_set', 
                                               'mediaofposts_set').order_by('-created_at')[currentNumberOfPosts:currentNumberOfPosts+10]

        try: 
            for post in posts:
                
                posts_data = PostsSerializer(post).data

                userProfile = UserProfileSerializer(post.user_id.userprofile_set.first())
                imageProfile = ImageProfileSerializer(post.user_id.imageprofile_set.first())

                userDataForPosts = {
                    "id": post.user_id.id,
                    "name": f"{userProfile.data.get('first_name')} {userProfile.data.get('last_name')}",
                    "avatar": imageProfile.data.get('avatar')
                }
                
                postsInfo = PostsInfo.objects(__raw__={'posts_id': post.id}).first()
                
                # media = posts.mediaofposts_set.all()
                media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
                
                posts_data['media'] = media_data
                posts_data['user'] = userDataForPosts
                posts_data['created_at'] = getTimeDuration(post.created_at)
                posts_data['posts_info'] = PostsInfoSerializer(postsInfo).data
            
                data.append(posts_data)
        except Exception as e:
            print(e)
            
        reponse.data = {
            'posts': data
        }

        return reponse