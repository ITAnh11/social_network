from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt 
import logging
from users.models import User
from friends.models import Friendship, FriendRequest
from users.serializers import UserSerializer
from friends.serializers import FriendshipSerializer

from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer, ImageProfileSerializer
from .forms import ImageProfileForm

from posts.models import Posts
from posts.serializers import PostsSerializer, MediaOfPostsSerializer

from posts.views import CreatePostsAfterSetImageProfileView

from posts.models import PostsInfo
from posts.serializers import PostsInfoSerializer

# from users.views import LoginView

from common_functions.common_function import getUser, getTimeDuration, getUserProfileForPosts

import time
logger = logging.getLogger(__name__)

class ProfileView(APIView):
    def get(self, request):
        logger.info("GET request received in ProfileView")
        user = getUser(request)
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in ProfileView")
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            logger.info('check profile')
            return render(request, 'userprofiles/profile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:profile') + '?id=' + str(id_requested)
        return HttpResponseRedirect(path)
        
class ListFriendsView(APIView):
    def get(self, request):
        logger.info("GET request received in ListFriendsView")
        user = getUser(request)
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in ListFriendsView")
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            logger.info('check listFr of User')
            return render(request, 'userprofiles/listFriends.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:listFriends') + '?id=' + str(id_requested)
        return HttpResponseRedirect(path)

class GetProfileView(APIView):
    def get(self, request):
        logger.info("GET request received in GetProfileView")
        user = getUser(request)
        
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in GetProfileView")
            return Response({'error': 'Unauthorized'}, status=401)

        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id
        
        try:
            context = self.getProfile(idUserRequested)
        except Exception as e:
            logger.exception("An error occurred in GetProfileView")
            return Response({'error': str(e)}, status=404)
        
        context['isOwner'] = True if user.id == idUserRequested else False
                
        return Response(context)
    
    def getProfile(self, id):
        try:
            user = User.objects.get(id=id)
            userprofile = UserProfile.objects.get(user_id=id)
            imageprofile = ImageProfile.objects.get(user_id=id)
            
            context = {
                'user': UserSerializer(user).data,
                'userprofile': UserProfileSerializer(userprofile).data,
                'imageprofile': ImageProfileSerializer(imageprofile).data
            }
            
            return context
        except Exception as e:
            raise e
    
class SetUserProfileView(APIView):    
    def post(self, request, user):
        try:
            logger.info("POST request received in SetUserProfileView")
            userprofile = UserProfile.objects.create(   user_id=user,
                                                        first_name=request.data.get('first_name'),
                                                        last_name=request.data.get('last_name'),
                                                        gender=request.data.get('gender'),
                                                        phone=request.data.get('phone'),
                                                        birth_date=request.data.get('birth_date') or None,
                                                    )
            userprofile.save()
            logger.info('User profile created successfully')
            return Response({'message': 'User profile created successfully!'})
        except Exception as e:
            logger.error('Failed to create user profile: %s', e)
            return Response({'error': 'Failed to create user profile. Please try again.'})
    
class SetImageProfileView(APIView):    
    def post(self, request, user):
        logger.info("POST request received in SetImageProfileView")
        imageProfileForm = ImageProfileForm(request.POST or None, request.FILES or None)
        if imageProfileForm.is_valid():
            imageProfileForm.save(user)
                              
        return Response({'message': 'Image profile created successfully!'})
    
class GetPostsView(APIView):
    def post(self, request):
        logger.info("POST request received in GetPostsView")
        start_time = time.time()
        
        user = getUser(request)
        
        if not user:
            logger.warning("Unauthorized access detected in GetPostsView")
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id

        userRequest = User.objects.filter(id=idUserRequested).first()
        
        if not userRequest:
            logger.warning("User not found in GetPostsView")
            return Response({'error': 'User not found'}, status=404)
        
        userDataForPosts = getUserProfileForPosts(userRequest)
        
        num_posts = Posts.objects.count()
        currentNumberOfPosts = int(request.data.get('current_number_of_posts'))

        if currentNumberOfPosts >= num_posts:
            return Response({'error': 'No more posts available'}, status=400)

        posts = Posts.objects.filter(user_id=userRequest).prefetch_related('user_id__userprofile_set', 
                                               'user_id__imageprofile_set', 
                                               'mediaofposts_set').order_by('-created_at')[currentNumberOfPosts:currentNumberOfPosts+10]
        
        for post in posts:
            posts_data = PostsSerializer(post).data
            media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
            posts_info = PostsInfo.objects(__raw__={'posts_id': post.id}).first()
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts
            posts_data['posts_info'] = PostsInfoSerializer(posts_info).data

            posts_data['created_at'] = getTimeDuration(post.created_at)
        
            data.append(posts_data)
            
        reponse = Response()
        
        reponse.data = {
            'posts': data,
            'isOwner': True if user.id == idUserRequested else False
        }
        
        end_time = time.time()  
        execution_time = end_time - start_time  
        logger.info(f"GetPostsView executed in {execution_time} seconds")

        return reponse
    
class GetUserProfileBasicView(APIView):
    def get(self, request):
        logger.info("GET request received in GetUserProfileBasicView")
        user = getUser(request)
        
        if not user:
            logger.warning("Unauthorized access detected in GetUserProfileBasicView")
            return Response({'error': 'Unauthorized'}, status=401)
        
        userprofile = UserProfile.objects.filter(user_id=user).first()
        imageprofile = ImageProfile.objects.filter(user_id=user).first()
        
        profileSerializer = UserProfileSerializer(userprofile)
        imageSerializer = ImageProfileSerializer(imageprofile)
        
        context = {
            'user_id': user.id,
            'name': f"{profileSerializer.data.get('first_name')} {profileSerializer.data.get('last_name')}",
            'avatar': imageSerializer.data.get('avatar')
        }
        
        return Response(context)

    
