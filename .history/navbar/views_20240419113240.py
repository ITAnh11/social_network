# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common_functions.common_function import getUser, getUserProfileForPosts
from users.models import User
from userprofiles.models import UserProfile

from django.db.models import Q
from .serializers import UserInfoSerializer, ImageSerializer
from rest_framework import generics

class navbarView(APIView):     
    def navbar(request):
        return render(request, "navbar/navbar.html")


class SearchListView(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('name')
        #username = self.request.query_params.get('name', '')
        # username = self.kwargs['username']
        print(username)
        users =  UserProfile.objects.filter(
            Q(first_name__icontains=username) |
            Q(last_name__icontains=username)
        ).order_by('first_name')
        #print(users)
        if not users.exists():
            return Response({"detail": "Không tìm thấy người dùng"})
        data =[]
        for user in users:
            data.append({
                "search user": getUserProfileForPosts(user.user_id)
            })
        #serializer = UserInfoSerializer(users,  many=True)
        return Response(data)
    
    

    



    