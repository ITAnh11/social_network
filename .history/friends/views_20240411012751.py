from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime

from common_functions.common_function import getUser, getUserProfileForPosts
from users.models import User
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer
# Create your views here.
# friend_request.status = 'accepted'  # Cập nhật trạng thái của yêu cầu kết bạn thành 'accepted'
# friend_request.save()  # Lưu thay đổi vào cơ sở dữ liệu
# friend_request.delete()  # Xóa yêu cầu kết bạn khỏi cơ sở dữ liệu


class FriendsRequestsView(APIView):
    def get(self,request):
        user = getUser(request)
        
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request,'friends/friend.html')

class  SentFriendRequestView(APIView):
    def post(self, request, friend_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return Response({'error': 'Friend not found'}, status=404)
        
        existing_request = FriendRequest.objects.filter(from_id=user, to_id=friend).exists()
        
        if existing_request:
            return Response({'error': 'Friend request already sent'}, status=400)
        
        FriendRequest.objects.create(from_id=user, to_id=friend, status='pending')
        
        return Response({'success': 'Friend request sent successfully'})
    
class DeleteFriendRequestView(APIView):
    def post(self, request, friend_request_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=404)
        
        if friend_request.from_id != user:
            return Response({'error': 'Permission denied'}, status=403)
        
        friend_request.delete()
        
        return Response({'success': 'Friend request deleted successfully'})
    
class AcceptFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        print(request.data)
        # try:
        #     friend_request = FriendRequest.objects.create(
        #         from_id = request.data.get('st'),
        #         to_id = user,
                
        #     )
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=404)
        
        if friend_request.to_id != user:
            return Response({'error': 'Permission denied'}, status=403)
        
        friend_request.status = 'accepted'
        friend_request.save()
        
        Friendship.objects.create(user_id1=friend_request.from_id, user_id2=user)
        
        return Response({'success': 'Friend request accepted successfully'})

class DenineFriendRequestView(APIView):
    def post(self, request, friend_request_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=404)
        
        if friend_request.status == 'accepted':
            return Response({'error': 'Friend request accepted'}, status=409)
        
        if friend_request.to_id != user:
            return Response({'error': 'Permission denied'}, status=403)
        
        friend_request.status = 'denied'
        friend_request.save()
        
        return Response({'success': 'Friend request denied successfully'})
    
class DeleteFriendShip(APIView):
    def post(self, request, friendship_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friendship = Friendship.objects.get(id=friendship_id)
        except Friendship.DoesNotExist:
            return Response({'error': 'Friendship not found'}, status=404)
        
        if user != friendship.user_id1 and user != friendship.user_id2:
            return Response({'error': 'Permission denied'}, status=403)
        
        friendship.delete()
        
        return Response({'success': 'Friendship deleted successfully'})
    
class GetSentFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        list_friend_requests_sent = FriendRequest.objects.filter(from_id=user)
        print(list_friend_requests_sent)
        for friend_request_sent in list_friend_requests_sent:
            serializer = FriendRequestSerializer(friend_request_sent)
            print(serializer)
            
            friend_request = {
                "friend_request_sent" : serializer.data,
                "friend_request_profile": getUserProfileForPosts(friend_request_sent.to_id)
            }
            data.append(friend_request)
        return Response({
            "data" : data
        })

class  GetReceivedFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        list_friend_requests_received = FriendRequest.objects.filter(to_id=user)
        print(list_friend_requests_received)
        for friend_request_received in list_friend_requests_received:
            serializer = FriendRequestSerializer(friend_request_received)
            print(serializer)
            
            friend_request = {
                "friend_request_received" : serializer.data,
                "friend_request_profile": getUserProfileForPosts(friend_request_received.from_id)
            }

            data.append(friend_request)

        return Response({
            "data": data
            })

class GetListFriendView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        friendships = Friendship.objects.filter(user_id1=user) | Friendship.objects.filter(user_id2=user)
        
        serializer = FriendshipSerializer(friendships, many=True)
        
        return Response(serializer.data)