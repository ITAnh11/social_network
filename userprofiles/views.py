from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer
from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer, ImageProfileSerializer
from .forms import ImageProfileForm

from common_functions.common_function import getUser

from social_network.redis_conn import redis_server

import random
import time
import json

EX_TIME = 60 * 10
INT_FROM = 0
INT_TO = EX_TIME // 3

class ProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/profile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:profile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
        
class ListFriendsView(APIView):
    def get(self, request):
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/listFriends.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:listFriends') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

class GetProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)

        # print(request.query_params.get('id'))
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id
        
        try:
            context = self.getProfile(idUserRequested)
        except Exception as e:
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
    # create a new user profile
    def post(self, request, user):
        userprofile = UserProfile.objects.create(   user_id=user,
                                                    first_name=request.data.get('first_name'),
                                                    last_name=request.data.get('last_name'),
                                                    gender=request.data.get('gender'),
                                                    phone=request.data.get('phone'),
                                                    birth_date=request.data.get('birth_date') or None,
                                                )

        userprofile.save()

        return Response({'message': 'User profile created successfully!'})
class SetImageProfileView(APIView):    
    def post(self, request, user):
        imageProfileForm = ImageProfileForm(request.POST or None, request.FILES or None)
        if imageProfileForm.is_valid():
            imageProfileForm.save(user)
                              
        return Response({'message': 'Image profile created successfully!'})
    
class UserProfileBasicView(APIView):
    def resetUserProfileBasic(self, user):
        redis_server.delete(f'userprofile_basic_{user.id}')
        
        userprofile = UserProfile.objects.filter(user_id=user).first()
        imageprofile = ImageProfile.objects.filter(user_id=user).first()
        
        profileSerializer = UserProfileSerializer(userprofile)
        imageSerializer = ImageProfileSerializer(imageprofile)
        
        context = {
            'id': user.id,
            'name': f"{profileSerializer.data.get('first_name')} {profileSerializer.data.get('last_name')}",
            'avatar': imageSerializer.data.get('avatar')
        }
        
        time_to_live = EX_TIME + random.randint(INT_FROM, INT_TO)
        
        redis_server.setex(f'userprofile_basic_{user.id}', time_to_live , json.dumps(context))
        
        return context
        
    def getUserProfileBasic(self, user):
        userprofileBasic = redis_server.get(f'userprofile_basic_{user.id}')
        
        if userprofileBasic is None:
            userprofile = UserProfile.objects.filter(user_id=user).first()
            imageprofile = ImageProfile.objects.filter(user_id=user).first()
            
            profileSerializer = UserProfileSerializer(userprofile)
            imageSerializer = ImageProfileSerializer(imageprofile)
            
            context = {
                'id': user.id,
                'name': f"{profileSerializer.data.get('first_name')} {profileSerializer.data.get('last_name')}",
                'avatar': imageSerializer.data.get('avatar')
            }
            
            time_to_live = EX_TIME + random.randint(INT_FROM, INT_TO)
            
            redis_server.setex(f'userprofile_basic_{user.id}', time_to_live , json.dumps(context))
        else :
            context = json.loads(userprofileBasic)
            
        return context
    
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        context = self.getUserProfileBasic(user)

        return Response(context)
    
