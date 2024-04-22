# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

    def get_queryset(self):
        username = self.request.query_params.get('username', '')
        if username:
            return UserProfile.objects.filter(
                Q(user_id__email__icontains=username) |
                Q(first_name__icontains=username) |
                Q(last_name__icontains=username)
            )
        else:
            return UserProfile.objects.none()

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Không tìm thấy người dùng"})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    