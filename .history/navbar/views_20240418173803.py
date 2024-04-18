# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from userprofiles.models import UserProfile

def navbar(request):
    return render(request, "navbar/navbar.html")

class searchList(APIView()):
    def post(self, request):
        return render(request.data)

class getSearchList(APIView()):
    def get(self, request):
        return Response('Ok')
    