from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt 
import logging
from users.models import User

from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer
from .forms import ImageProfileForm


from posts.views import CreatePostsAfterSetImageProfileView

# from users.views import LoginView

from common_functions.common_function import getUser, getTimeDuration, getUserProfileForPosts

import time
logger = logging.getLogger(__name__)

class EditImagesPage(APIView):
    def get(self, request):
        logger.info("GET request received in EditImagesPage")
        user = getUser(request)
        print(user)                    
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditImagesPage")
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                logger.error("you can't editImage with id")
                return Response({'error': 'Unauthorized'}, status=401)
            return render(request, 'userprofiles/editImages.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editImagesPage') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

class EditAvatarView(APIView):
    def post(self, request):
        logger.info("POST request received in EditAvatarView")
        user = getUser(request)
        
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditAvatarView")
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            imageprofile = ImageProfile.objects.get(user_id=user)
            
            avatar = request.data.get('avatar')
            
            imageprofileForm = ImageProfileForm(request.data, request.FILES)
            if not imageprofileForm.is_valid():
                logger.error("Invalid form data in EditAvatarView")
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
            logger.exception("An error occurred in EditAvatarView")
            return Response({'error': str(e)}, status=404)
    
class EditCoverView(APIView):

    def post(self, request):
        logger.info("POST request received in EditCoverView")
        user = getUser(request)
        
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditCoverView")
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            imageprofile = ImageProfile.objects.get(user_id=user)
            
            background = request.data.get('background')
        
            imageprofileForm = ImageProfileForm(request.data, request.FILES)
            if not imageprofileForm.is_valid():
                logger.error("Invalid form data in EditCoverView")
                return Response({'error': imageprofileForm.errors}, status=404)
                
            imageprofile.background = background    
            imageprofile.save()
            
            CreatePostsAfterSetImageProfileView().createUpdateImageProfilePosts(user, 
                                                                                'background', 
                                                                                imageprofileForm.cleaned_data.get('background'))
            
            return Response({'success': 'Your cover image updated successfully!',
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        
        except Exception as e:
            logger.exception("An error occurred in EditCoverView")
            return Response({'error': str(e)}, status=404)
    
class EditProfileView(APIView):
    def get(self, request):
        logger.info("GET request received in EditProfileView")
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditProfileView")
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401)
            return render(request, 'userprofiles/editProfile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editProfile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

    def post(self, request):
        logger.info("POST request received in EditProfileView")
        user = getUser(request)
        
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditProfileView")
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            userprofile = UserProfile.objects.get(user_id=user)
            
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            print(first_name)
            print(last_name)
            if not first_name or not last_name:
                logger.warning("First name and last name are required in EditProfileView")
                return Response({'warning': 'First name and last name are required!'}, status=404)
            
            userprofile.first_name = first_name
            userprofile.last_name = last_name
            userprofile.phone = request.data.get('phone') or ''
            userprofile.birth_date = request.data.get('birth_date') or None
        
            userprofile.save()
            
            return Response({'success': 'User profile updated successfully!',
                             'name': userprofile.first_name + ' ' + userprofile.last_name,
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        
        except Exception as e:
            logger.exception("An error occurred in EditProfileView")
            return Response({'error': str(e)}, status=404) 
        
class EditStoryView(APIView):
    def get(self, request):
        logger.info("GET request received in EditStoryView")
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditStoryView")
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401) 
            
            userprofile = UserProfile.objects.get(user_id=user)

            context = {
                'userprofile': UserProfileSerializer(userprofile).data
            }

            return render(request, 'userprofiles/editStory.html', context=context)
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editStory') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
    
    def post(self, request):
        logger.info("POST request received in EditStoryView")
        print(request.data)
        user = getUser(request)
        
        if not isinstance(user, User):
            logger.warning("Unauthorized access detected in EditStoryView")
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
            
            return Response({'success': 'User story updated successfully!',
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        except Exception as e:
            logger.exception("An error occurred in EditStoryView")
            return Response({'error': str(e)}, status=404)
