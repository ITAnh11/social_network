# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from userprofiles.models import UserProfile

class navbarView(APIView):     
    def navbar(request):
        return render(request, "navbar/navbar.html")

class searchListView(APIView):
    def post(self, request):
        print(request.data)
        return render(request.data)


    