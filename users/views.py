from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer
from .models import UserProfile, User

import jwt, datetime


# Create your views here.
class LoginView(APIView):
    def get(self, request):
        # token = request.COOKIES.get('jwt')
        # if token:
        #     return redirect('users:index')
        
        return render(request, 'users/login_demo.html')
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'warning': 'User not found!'})
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            return Response({'warning': 'Incorrect password!'})
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload=payload, key='secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'success': 'login success',
            'jwt': token,
            'redirect_url': '/'
        }
               
        return response
  
class RegisterView(APIView):
    def get(self, request):
        return render(request, 'users/register_demo.html')
    
    def createProfile(self, request, user_id):
        user_profile = UserProfile()
        user_profile.user_id = user_id
        user_profile.first_name = request.data['first_name']
        user_profile.last_name = request.data['last_name']
        user_profile.birth_date = request.data['birth_date']
        user_profile.gender = request.data['gender']
        
        user_profile.save()
            
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                
                self.createProfile(request, user)
            
                return Response({'success': 'User registered successfully. Please Login.'})
        except ValidationError as e:
            if e.detail.get('email'):
                return Response({'warning': 'Email already exists.'})
            return Response({'warning': 'Passwords must match.'})
        except Exception as e:
            return Response({'error': 'Something went wrong. Please try again.'})

class index(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return HttpResponseRedirect(reverse('users:login'))
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(jwt=token, key='secret', algorithms=['HS256'])  
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect(reverse('users:login'))
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return render(request, 'users/index.html', {"user": serializer.data})

class LogoutView(APIView):
    def post(self, request):
        response = HttpResponseRedirect(reverse('users:login'))
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response
