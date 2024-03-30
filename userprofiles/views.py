from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt

from users.models import User
from users.serializers import UserSerializer

from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer, ImageProfileSerializer
from .forms import ImageProfileForm

def getUser(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return None

    try:
        payload = jwt.decode(jwt=token, key='secret', algorithms=['HS256'])  
    except jwt.ExpiredSignatureError:
        return None
    
    return User.objects.filter(id=payload['id']).first()
    

class ProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))

        return render(request, 'userprofiles/profile.html')

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
        
        # print(context)
        
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

        return HttpResponseRedirect(reverse('userprofiles:profile'))
    
    def post(self, request, user):
        imageProfileForm = ImageProfileForm(request.POST or None, request.FILES or None)
        if imageProfileForm.is_valid():
            imageProfileForm.save(user)
        
        return Response({'message': 'Image profile created successfully!'})