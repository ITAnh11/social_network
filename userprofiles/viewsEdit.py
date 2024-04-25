from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt 

from users.models import User

from .models import UserProfile, ImageProfile
from .serializers import ImageProfileSerializer
from .forms import ImageProfileForm


from posts.views import CreatePostsAfterSetImageProfileView

# from users.views import LoginView

from common_functions.common_function import getUser, getTimeDuration, getUserProfileForPosts

import time

class EditImagePage(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)                    
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401)
            return render(request, 'userprofiles/editImages.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editImagesPage') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

class EditAvatarView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            imageprofile = ImageProfile.objects.get(user_id=user)
            
            avatar = request.data.get('avatar')
            
            imageprofileForm = ImageProfileForm(request.data, request.FILES)
            if not imageprofileForm.is_valid():
                return Response({'error': imageprofileForm.errors}, status=404)
            
            imageprofile.avatar = avatar    
            imageprofile.save()
            
            CreatePostsAfterSetImageProfileView().createUpdateImageProfilePosts(user, 
                                                                                'avatar', 
                                                                                imageprofile.avatar
                                                                                )
            
            return Response({'success': 'Your avatar image updated successfully!',
                             'avatar': imageprofile.avatar.url,
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        
        except Exception as e:
            return Response({'error': str(e)}, status=404)
    
class EditCoverView(APIView):

    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            imageprofile = ImageProfile.objects.get(user_id=user)
            
            background = request.data.get('background')
        
            imageprofileForm = ImageProfileForm(request.data, request.FILES)
            if not imageprofileForm.is_valid():
                return Response({'error': imageprofileForm.errors}, status=404)
                
            imageprofile.background = background    
            imageprofile.save()
            
            CreatePostsAfterSetImageProfileView().createUpdateImageProfilePosts(user, 
                                                                                'background', 
                                                                                imageprofileForm.cleaned_data.get('background'))
            
            return Response({'success': 'Your cover image updated successfully!',
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        
        except Exception as e:
            return Response({'error': str(e)}, status=404)
    
class EditProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401)
            return render(request, 'userprofiles/editProfile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editProfile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            userprofile = UserProfile.objects.get(user_id=user)
            
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            
            if not first_name or not last_name:
                return Response({'warning': 'First name and last name are required!'}, status=404)
            
            userprofile.first_name = first_name
            userprofile.last_name = last_name
            userprofile.phone = request.data.get('phone') or ''
            userprofile.birth_date = request.data.get('birth_date') or None
        
            userprofile.save()
            
            return Response({'success': 'User profile updated successfully!',
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        
        except Exception as e:
            return Response({'error': str(e)}, status=404)
        
class EditStoryView(APIView):
    def get(self, request):
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401) 
            return render(request, 'userprofiles/editStory.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editStory') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
    def post(self, request):
        print(request.data)
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            userprofile = UserProfile.objects.get(user_id=user)
            
            userprofile.bio = request.data.get('bio')
            userprofile.work = request.data.get('work')
            userprofile.address_work = request.data.get('address_work')
            userprofile.address = request.data.get('address')
            userprofile.place_birth = request.data.get('place_birth')
            userprofile.social_link = request.data.get('social_link')
            
            userprofile.save()
            
            return Response({'success': 'User profile updated successfully!',
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        except Exception as e:
            return Response({'error': str(e)}, status=404)