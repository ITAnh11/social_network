from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

from users.models import User
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer
# Create your views here.
def get_user(request):
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

class FriendsView(APIView):
    def get(self,request):
        user = get_user(request)
        
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request,'friends/friend.html')

class  AddFriendView(APIView):
    def post(self, request, friend_id):
        user = get_user(request)
        
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
        user = get_user(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        friend_requests_received = FriendRequest.objects.filter(to_id=user)
        serializer = FriendRequestSerializer(friend_requests_received, many=True)
        
        return Response(serializer.data)
