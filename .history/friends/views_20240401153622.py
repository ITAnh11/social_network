from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt
class FriendsView(APIView):
    def get(self,request):
       return render(request,'friends/friend.html')
class  AddFriendView(APIView):
    def post(self, request):
        