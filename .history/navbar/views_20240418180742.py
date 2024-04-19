# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from userprofiles.models import UserProfile

from django.db.models import Q
from .serializers import UserInfoSerializer, ImageSerializer
from rest_framework import generics
class navbarView(APIView):     
    def navbar(request):
        return render(request, "navbar/navbar.html")

class searchListView(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()

    def list(self, request, *args, **kwargs):
        print("list func called")
        username = request.query_params.get('username', '')
        print(UserProfile.objects.all())
        users = UserProfile.objects.filter(
            Q(user_id__email__icontains=username) |
            Q(first_name__icontains=username) |
            Q(last_name__icontains=username) 
        )
        print(users)
        if not users.exists():
            return Response(
                {"detail" : "No user found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)


    