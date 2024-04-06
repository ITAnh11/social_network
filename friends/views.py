from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

from common_functions.common_function import getUser
from users.models import User
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer
# Create your views here.


class FriendsView(APIView):
    def get(self,request):
        user = getUser(request)
        
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request,'friends/friend.html')

class  AddFriendView(APIView):
    def post(self, request, friend_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        friend = User.objects.filter(id=friend_id).first()
        
        if not friend:
            return Response({'error': 'Friend not found'}, status=404)
        
        existing_request = FriendRequest.objects.filter(from_id=user, to_id=friend).exists()
        
        if existing_request:
            return Response({'error': 'Friend request already sent'}, status=400)
        
        friend_request = FriendRequest.objects.create(from_id=user, to_id=friend, status='pending')
        
        return Response({'success': 'Friend request sent successfully'})
        
class  FriendRequestsListView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        friend_requests_received = FriendRequest.objects.filter(to_id=user)
        serializer = FriendRequestSerializer(friend_requests_received, many=True)
        
        return Response(serializer.data)

class SentFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        friend_requests_sent = FriendRequest.objects.filter(from_id=user)
        serializer = FriendRequestSerializer(friend_requests_sent, many=True)
        
        return Response(serializer.data)
    
    
class GetFriendView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        friend_requests_sent = FriendRequest.objects.filter(from_id=user)
        friend_requests_received = FriendRequest.objects.filter(to_id=user)
        
        friend_requests_sent_serializer = FriendRequestSerializer(friend_requests_sent, many=True)
        friend_requests_received_serializer = FriendRequestSerializer(friend_requests_received, many=True)
        
        context = {
            'friend_requests_sent': friend_requests_sent_serializer.data,
            'friend_requests_received': friend_requests_received_serializer.data
        }
                
        return Response(context)


        