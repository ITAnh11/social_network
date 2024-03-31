from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.views import APIView

import jwt

from users.models import User

# Create your views here.

def getUser(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
    except jwt.ExpiredSignatureError:
        return None
    
    user = User.objects.get(id=user_id)
    
    return user
    
class HomePageView(APIView):
    def get(self, request):
<<<<<<< HEAD
        token = request.COOKIES.get('jwt')  

=======
        token = request.COOKIES.get('jwt')
>>>>>>> b1fe0668ed6cc27ae242694dcacfec6d10e6d287
        if not token:
            return HttpResponseRedirect('/users/login/')
            
        return render(request, 'homepage/index.html')

class getPostsView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return HttpResponseRedirect('/users/login/')
            
        return render(request, 'homepage/getPosts.html')