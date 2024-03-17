from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from users.views import LoginView

# Create your views here.
class HomePageView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return HttpResponseRedirect('/users/login/')
            
        return render(request, 'homepage/homepage_demo.html')
