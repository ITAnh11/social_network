from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt

from users.views import LogoutView

from posts.models import Posts, PostsInfo, PostIsWatched
from posts.serializers import PostsSerializer, MediaOfPostsSerializer, PostsInfoSerializer

from userprofiles.serializers import UserProfileSerializer, ImageProfileSerializer

from common_functions.common_function import getUser, getTimeDuration
import logging

logger = logging.getLogger(__name__)
# Create your views here.
class HomePageView(APIView):
    def get(self, request):
        logger.info("GET request received in HomePageView")
        
        token = request.COOKIES.get('jwt')  
            
        if not token:
            logger.warning("No JWT token found in cookies")
            return HttpResponseRedirect(reverse('users:login'))

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
        except jwt.ExpiredSignatureError:
            logger.error("Expired JWT token")
            LogoutView().post(request)
            return HttpResponseRedirect(reverse('users:login'))
            
        logger.info("Rendering homepage")
        return render(request, 'homepage/index.html')

class GetPostsView(APIView):
    def post(self, request):
        logger.info("POST request received in GetPostsView")
        
        user = getUser(request)
        
        if not user:
            logger.warning("Unauthorized access")
            return Response({'error': 'Unauthorized'}, status=401)
        
        reponse = Response()
        data = []

        posts = self.filterPosts(user.id)

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

                media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
                
                posts_data['media'] = media_data
                posts_data['user'] = userDataForPosts
                posts_data['created_at'] = getTimeDuration(post.created_at)
                posts_data['posts_info'] = PostsInfoSerializer(postsInfo).data
            
                data.append(posts_data)
        except Exception as e:
            logger.error(f"Error: {e}")
            
        reponse.data = {'posts': data}

        return reponse
    
    def checkEnableLoadMore(self, request):
        logger.info("Checking if load more is enabled")
        try:
            num_posts = Posts.objects.count()
            currentNumberOfPosts = int(request.data.get('current_number_of_posts'))
            
            if currentNumberOfPosts >= num_posts:
                return -1
        except Exception as e:
            logger.error(f"Error: {e}")
            return -1

        return currentNumberOfPosts
    
    def filterPosts(self, user_id):
        logger.info("Filtering posts")
        try:
            posts = Posts.objects.raw(f"""
                        SELECT posts_posts.*, posts_postiswatched.user_id_id 
                        FROM posts_posts
                        LEFT JOIN public.posts_postiswatched ON posts_postiswatched.post_id_id = posts_posts.id AND posts_postiswatched.user_id_id = {user_id}
                        ORDER BY (posts_postiswatched.user_id_id IS NULL) DESC, posts_posts.created_at DESC
                        LIMIT 10
                        """)

        except Exception as e:
            logger.error(f"Error: {e}")
            return []
        return posts
