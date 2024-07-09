from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt

from users.views import LogoutView
from users.models import User

import logging

logger = logging.getLogger(__name__)
# Create your views here.
class HomePageView(APIView):
    def get(self, request):
        logger.info("GET request received in HomePageView")
        
        token = request.COOKIES.get('jwt')  
            
        if not token:
            logger.warning("No JWT token found in cookies")
            return HttpResponseRedirect(reverse('users:login'))

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
        except jwt.ExpiredSignatureError:
            logger.error("Expired JWT token")
            LogoutView().post(request)
            return HttpResponseRedirect(reverse('users:login'))
        
        try:
            user = User.objects.get(id=user_id)
            if not user:
                logger.error("User not found")
                return HttpResponseRedirect(reverse('users:login'))
            
        except User.DoesNotExist:
            logger.error("User not found")
            return HttpResponseRedirect(reverse('users:login'))
        
        logger.info("Rendering homepage")
        return render(request, 'homepage/index.html')
