from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User

from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer
from .forms import ImageProfileForm
from .views import UserProfileBasicView

from posts.views import createUpdateImageProfilePosts

from common_functions.common_function import getUser

from notifications.models import updateProfileNotification
from posts.models import updateProfilePosts
from reactions.models import updateProfileReactions
from comments.models import updateProfileComments

def updateAllReferences(user):
    try:
        userprofile = UserProfileBasicView().resetUserProfileBasic(user)
        updateProfilePosts(user.id, userprofile)
        updateProfileComments(user.id, userprofile)
        updateProfileReactions(user.id, userprofile)
        updateProfileNotification(user.id, userprofile)
    except Exception as e:
        print('updateAllReferences', e)
        return False
    return True
    

class EditImagesPage(APIView):
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
            
            old_avatar = imageprofile.avatar
            
            imageprofile.avatar = avatar    
            imageprofile.save()
            
            userprofile = UserProfileBasicView().getUserProfileBasic(user)
            
            post = createUpdateImageProfilePosts(userprofilebasic=userprofile, 
                                                typeImage='avatar',
                                                image=imageprofileForm.cleaned_data.get('avatar'))
        
            if post == False:
                imageprofile.avatar = old_avatar
                imageprofile.save()
                return Response({'error': 'Error while creating post'}, status=400)
            
            updateAllReferences(user)
            
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
            
            old_background = imageprofile.background
                
            imageprofile.background = background    
            imageprofile.save()
            
            userprofile = UserProfileBasicView().getUserProfileBasic(user)
            
            post = createUpdateImageProfilePosts(userprofilebasic=userprofile, 
                                                typeImage='background',
                                                image=imageprofileForm.cleaned_data.get('background'))
        
            if post == False:
                imageprofile.background = old_background
                imageprofile.save()
                return Response({'error': 'Error while creating post'}, status=400)
            
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
            
            updateAllReferences(user)
            
            return Response({'success': 'User profile updated successfully!',
                             'name': userprofile.first_name + ' ' + userprofile.last_name,
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
            
            userprofile = UserProfile.objects.get(user_id=user)

            context = {
                'userprofile': UserProfileSerializer(userprofile).data
            }

            return render(request, 'userprofiles/editStory.html', context=context)
        
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
            
            return Response({'success': 'User story updated successfully!',
                             'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
        except Exception as e:
            return Response({'error': str(e)}, status=404)
