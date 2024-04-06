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

class ProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        return render(request, 'userprofiles/profile.html')
    
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
            return HttpResponseRedirect(reverse('users:login'))
        
        id_requested = request.GET.get('id') or user.id
        
        userprofile = UserProfile.objects.filter(user_id=id_requested).first()
        imageprofile = ImageProfile.objects.filter(user_id=id_requested).first()
        enable_edit = user.id == id_requested
        
        context = {
            'user': UserSerializer(user).data,
            'userprofile': UserProfileSerializer(userprofile).data,
            'imageprofile': ImageProfileSerializer(imageprofile).data,
            'enable_edit': enable_edit
        }
                
        return Response(context)
       
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
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        reponse = Response()
        
        data = []
        
        userDataForPosts = getUserProfileForPosts(user)
        
        posts = Posts.objects.filter(user_id=user).values('id', 'title', 'content', 'status', 'created_at').all().order_by('-created_at')    
        
        for post in posts:
            posts_data = PostsSerializer(post).data
            media = MediaOfPosts.objects.filter(post_id=post.get('id')).all()
            media_data = MediaOfPostsSerializer(media, many=True).data
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts

            posts_data['created_at'] = getTimeDuration(post.get('created_at'))
        
            data.append(posts_data)
            
        reponse.data = {
            'posts': data
        }

        return reponse