from .serializers import UserSerializer
from .models import User
from userprofiles.views import SetUserProfileView, SetImageProfileView


import jwt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from common_functions.common_function import getUser

# Create your views here.
class LoginView(APIView):
    def makeToken(self, user):
        payload = {
            'id': user.id,
            'exp': timezone.now() + timezone.timedelta(days=1),
            'iat': timezone.now()
        }

        token = jwt.encode(payload=payload, key='secret', algorithm='HS256')
        
        return token
    
    def get(self, request):
        response = render(request, 'users/login.html')
        # print(request.COOKIES.get('jwt'))
        
        response.delete_cookie('jwt')
        
        return response
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'warning': 'User not found!'})

        if not user.check_password(password):
            return Response({'warning': 'Incorrect password!'})
        
        user.set_last_login()
        
        token = self.makeToken(user)
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'success': 'Login success!!!',
            'jwt': token,
            'redirect_url': '/'
        }
        
        return response
  
class RegisterView(APIView):
    def get(self, request):
        
        response = render(request, 'users/register.html')
        print(request.COOKIES.get('jwt'))
        response.delete_cookie('jwt')
        
        return response
            
    def post(self, request):
        # print(request.data)
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                
                SetUserProfileView().post(request, user)
                SetImageProfileView().post(request, user)
                
                # user.set_last_login()
                
                token = LoginView().makeToken(user)
                
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    'success': 'Register success!!! Welcome to the feisubukku!',
                    'jwt': token,
                    'redirect_url': '/userprofiles/' + f"?id={user.id}"
                }
                
                return response
            
        except ValidationError as e:
            if e.detail.get('email'):
                return Response({'warning': e.detail.get('email')})
            if e.detail.get('comfirm_password'):
                return Response({'warning': e.detail.get('comfirm_password')})
            if e.detail.get('check_password'):
                return Response({'warning': e.detail.get('check_password')})
        except Exception as e:
            return Response({'error': 'Something went wrong. Please try again.'})

class LogoutView(APIView):
    def post(self, request):
        response = HttpResponseRedirect(reverse('users:login'))
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response
    
class ChangePasswordView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized!'}, status=401)
        
        old_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        comfirm_password = request.data.get('comfirm_password')
        
        if not user.check_password(old_password):
            return Response({'warning': 'Current password is incorrect!'})
        
        if new_password != comfirm_password:
            return Response({'warning': 'Password and comfirm password not match!'})
        
        if not UserSerializer().check_password(new_password):
            return Response({'warning': 'Password does not meet the requirements!\nPassword must be at least 8 characters long!\nPassword must not contain any spaces!'})
        
        user.set_password(new_password)
        user.confirm_password = user.password
        user.save()
        
        return Response({'success': 'Change password success!'})