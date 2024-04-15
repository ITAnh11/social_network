from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt 

from users.models import User
from users.serializers import UserSerializer

from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer, ImageProfileSerializer
from .forms import ImageProfileForm

from posts.models import Posts, MediaOfPosts
from posts.serializers import PostsSerializer, MediaOfPostsSerializer

from posts.views import CreatePostsAfterSetMediaProfileView

from common_functions.common_function import getUser, getTimeDuration, getUserProfileForPosts

import time

class ProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/profile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:profile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
    
class EditProfileView(APIView):
    def get(self, request):
        user = getUser(request)

        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('user:login'))
        return render(request, 'userprofiles/editProfile.html')
    
class ListFriendsView(APIView):
    def get(self, request):
        user = getUser(request)

        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        return render(request, 'userprofiles/listFriends.html')

class GetProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)

        # print(request.query_params.get('id'))
        
        id_requested = request.query_params.get('id') or user.id
        
        context = self.getProfile(id_requested)
        context['enable_edit'] = True if user.id == id_requested else False
                
        return Response(context)
    
    def getProfile(self, id):
        user = User.objects.filter(id=id).first()
        userprofile = UserProfile.objects.filter(user_id=id).first()
        imageprofile = ImageProfile.objects.filter(user_id=id).first()
        
        context = {
            'user': UserSerializer(user).data,
            'userprofile': UserProfileSerializer(userprofile).data,
            'imageprofile': ImageProfileSerializer(imageprofile).data
        }
        
        return context
       
class SetUserProfileView(APIView):
    # update user profile
    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))

        userprofile = UserProfile.objects.filter(user_id=user).first()

        if userprofile:
            userprofile.first_name = request.data.get('first_name')
            userprofile.last_name = request.data.get('last_name')
            userprofile.gender = request.data.get('gender')
            userprofile.birth_date = request.data.get('birth_date')
            userprofile.bio = request.data.get('bio') or None
            userprofile.address = request.data.get('address') or None
            userprofile.school = request.data.get('school') or None
            userprofile.work = request.data.get('work') or None

            userprofile.save()

        return HttpResponseRedirect(reverse('userprofiles:profile'))
    
    # create a new user profile
    def post(self, request, user):
        userprofile = UserProfile.objects.create(   user_id=user,
                                                    first_name=request.data.get('first_name'),
                                                    last_name=request.data.get('last_name'),
                                                    gender=request.data.get('gender'),
                                                    birth_date=request.data.get('birth_date') or None,
                                                )

        userprofile.save()

        return Response({'message': 'User profile created successfully!'})
class SetImageProfileView(APIView):
    # update user profile
    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))

        imageprofile = ImageProfile.objects.filter(user_id=user).first()

        if imageprofile:
            imageprofile.avatar = request.FILES['avatar'] or None
            imageprofile.background = request.FILES['background'] or None
            imageprofile.save()
            
            if imageprofile.avatar:
                CreatePostsAfterSetMediaProfileView().createAvatarPosts(user, imageprofile.avatar)
            
            if imageprofile.background:
                CreatePostsAfterSetMediaProfileView().createBackgroundPosts(user, imageprofile.background)

        return HttpResponseRedirect(reverse('userprofiles:profile'))
    
    def post(self, request, user):
        imageProfileForm = ImageProfileForm(request.POST or None, request.FILES or None)
        if imageProfileForm.is_valid():
            imageProfileForm.save(user)
            
            if imageProfileForm.cleaned_data.get('avatar'):
                CreatePostsAfterSetMediaProfileView().createAvatarPosts(user, imageProfileForm.cleaned_data.get('avatar'))
              
            if imageProfileForm.cleaned_data.get('background'):
                CreatePostsAfterSetMediaProfileView().createBackgroundPosts(user, imageProfileForm.cleaned_data.get('background'))
                  
        return Response({'message': 'Image profile created successfully!'})
class GetPostsView(APIView):
    def get(self, request):
        
        start_time = time.time()
        
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        reponse = Response()
        
        data = []
        
        # print(request.query_params.get('id'))
        
        idUserRequested = int(request.query_params.get('id')) or user.id

        userRequest = User.objects.filter(id=idUserRequested).first()
        
        if not userRequest:
            return Response({'error': 'User not found'}, status=404)
        
        userDataForPosts = getUserProfileForPosts(userRequest)
        
        posts = Posts.objects.filter(user_id=userRequest).prefetch_related('mediaofposts_set').order_by('-created_at')    
        
        for post in posts:
            posts_data = PostsSerializer(post).data
            media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts

            posts_data['created_at'] = getTimeDuration(post.created_at)
        
            data.append(posts_data)
            
        reponse.data = {
            'posts': data,
            'isOwner': True if user.id == idUserRequested else False
        }
        
        # posts = Posts.objects.filter(user_id=user).values('id', 'title', 'content', 'status', 'created_at').all().order_by('-created_at')    
        
        # for post in posts:
        #     posts_data = PostsSerializer(post).data
        #     media = MediaOfPosts.objects.filter(post_id=post.get('id')).all()
        #     if media:
        #         media_data = MediaOfPostsSerializer(media, many=True).data
                
        #         posts_data['media'] = media_data
        #     else:
        #         posts_data['media'] = None
        #     posts_data['user'] = userDataForPosts

        #     posts_data['created_at'] = getTimeDuration(post.get('created_at'))
        
        #     data.append(posts_data)
            
        # reponse.data = {
        #     'posts': data
        # }
        
        end_time = time.time()  # lưu thời gian kết thúc

        execution_time = end_time - start_time  # tính thời gian thực thi

        print(f"The function took {execution_time} seconds to complete")

        return reponse
    
class GetUserProfileBasicView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
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