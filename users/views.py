from .serializers import UserSerializer
from .models import User
from userprofiles.views import SetUserProfileView, SetImageProfileView


import jwt
import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from common_functions.common_function import getUser

logger = logging.getLogger(__name__) 
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
        logger.info('User attempts to access the login page.')
        # print(request.COOKIES.get('jwt'))
        
        response.delete_cookie('jwt')
        
        return response
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            logger.warning('User not found!')
            return Response({'warning': 'User not found!'})

        if not user.check_password(password):
            logger.warning('Incorrect password for user')
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
        logger.info('User successfully logged in')
        
        return response
  
class RegisterView(APIView):
    def get(self, request):
        # Log khi phương thức GET được gọi
        logger.info("GET request received in RegisterView")
        
        response = render(request, 'users/register.html')
        print(request.COOKIES.get('jwt'))
        response.delete_cookie('jwt')
        
        return response
            
    def post(self, request):
        try:
            # Log khi phương thức POST được gọi
            logger.info("POST request received in RegisterView")
            
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    user = serializer.save()
                    # Ghi log khi save thành công
                    logger.info('User successfully registered')
                    
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
                    logger.info('User successfully registered')
                    return response
                except Exception as save_error:
                    # Ghi log khi save thất bại
                    logger.error("Failed to register user: %s", save_error)
                    return Response({'error': 'Failed to register user. Please try again.'})

            
        except ValidationError as e:
            if e.detail.get('email'):
                logger.warning('User needs to register with email')
                return Response({'warning': e.detail.get('email')})
            if e.detail.get('comfirm_password'):
                logger.warning('User needs to enter password')
                return Response({'warning': e.detail.get('comfirm_password')})
            if e.detail.get('check_password'):
                logger.warning('User needs to enter the same email')
                return Response({'warning': e.detail.get('check_password')})
        except Exception as e:
            # Log khi có lỗi xảy ra trong phương thức POST
            logger.exception("An error occurred in RegisterView")
            return Response({'error': 'Something went wrong. Please try again.'})

class LogoutView(APIView):
    def post(self, request):
        # Log khi phương thức POST của LogoutView được gọi
        logger.info("POST request received in LogoutView")
        
        response = HttpResponseRedirect(reverse('users:login'))
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response
    
class ChangePasswordView(APIView):
    def post(self, request):
        # Log khi phương thức POST của ChangePasswordView được gọi
        logger.info("POST request received in ChangePasswordView")
        
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized!'}, status=401)
        
        old_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not user.check_password(old_password):
            logger.warning('User needs to enter the correct password')
            return Response({'warning': 'Current password is incorrect!'})
        
        if new_password != confirm_password:
            logger.warning('User needs to enter the same password')
            return Response({'warning': 'Password and comfirm password not match!'})
        
        if not UserSerializer().check_password(new_password):
            logger.warning('The password needs to be in the correct form')
            return Response({'warning': 'Password does not meet the requirements!\nPassword must be at least 8 characters long!\nPassword must not contain any spaces!'})
        
        user.set_password(new_password)
        user.confirm_password = user.password
        try:
            user.save()
            logger.info('User successfully changed password.')
            return Response({'success': 'Change password success!'})
        except Exception as e:
            logger.error('Failed to save user to the database: %s', e)
            return Response({'error': 'Failed to save user to the database!'})
    
    