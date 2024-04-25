from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt 

from users.models import User
from friends.models import Friendship, FriendRequest
from users.serializers import UserSerializer
from friends.serializers import FriendshipSerializer

from .models import UserProfile, ImageProfile
from .serializers import UserProfileSerializer, ImageProfileSerializer
from .forms import ImageProfileForm

from posts.models import Posts
from posts.serializers import PostsSerializer, MediaOfPostsSerializer

from posts.views import CreatePostsAfterSetImageProfileView

from posts.models import PostsInfo
from posts.serializers import PostsInfoSerializer

# from users.views import LoginView

from common_functions.common_function import getUser, getTimeDuration, getUserProfileForPosts

import time

class ProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/profile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:profile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
        
class ListFriendsView(APIView):
    def get(self, request):
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/listFriends.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:listFriends') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

class GetProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)

        # print(request.query_params.get('id'))
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id
        
        try:
            context = self.getProfile(idUserRequested)
        except Exception as e:
            return Response({'error': str(e)}, status=404)
        
        context['isOwner'] = True if user.id == idUserRequested else False
                
        return Response(context)
    
    def getProfile(self, id):
        try:
            user = User.objects.get(id=id)
            userprofile = UserProfile.objects.get(user_id=id)
            imageprofile = ImageProfile.objects.get(user_id=id)
            
            context = {
                'user': UserSerializer(user).data,
                'userprofile': UserProfileSerializer(userprofile).data,
                'imageprofile': ImageProfileSerializer(imageprofile).data
            }
            
            return context
        except Exception as e:
            raise e
    
class SetUserProfileView(APIView):    
    # create a new user profile
    def post(self, request, user):
        userprofile = UserProfile.objects.create(   user_id=user,
                                                    first_name=request.data.get('first_name'),
                                                    last_name=request.data.get('last_name'),
                                                    gender=request.data.get('gender'),
                                                    phone=request.data.get('phone'),
                                                    birth_date=request.data.get('birth_date') or None,
                                                )

        userprofile.save()

        return Response({'message': 'User profile created successfully!'})
class SetImageProfileView(APIView):    
    def post(self, request, user):
        imageProfileForm = ImageProfileForm(request.POST or None, request.FILES or None)
        if imageProfileForm.is_valid():
            imageProfileForm.save(user)
                              
        return Response({'message': 'Image profile created successfully!'})
    
class GetPostsView(APIView):
    def get(self, request):
        
        start_time = time.time()
        
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        
        # print(request.query_params.get('id'))
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id

        userRequest = User.objects.filter(id=idUserRequested).first()
        
        if not userRequest:
            return Response({'error': 'User not found'}, status=404)
        
        userDataForPosts = getUserProfileForPosts(userRequest)
        
        posts = Posts.objects.filter(user_id=userRequest).prefetch_related('mediaofposts_set').order_by('-created_at')[:10] 
        
        for post in posts:
            posts_data = PostsSerializer(post).data
            media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
            posts_info = PostsInfo.objects(__raw__={'posts_id': post.id}).first()
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts
            posts_data['posts_info'] = PostsInfoSerializer(posts_info).data

            posts_data['created_at'] = getTimeDuration(post.created_at)
        
            data.append(posts_data)
            
        reponse = Response()
        
        reponse.data = {
            'posts': data,
            'isOwner': True if user.id == idUserRequested else False
        }
        
        end_time = time.time()  # lưu thời gian kết thúc

        execution_time = end_time - start_time  # tính thời gian thực thi

        print(f"The function took {execution_time} seconds to complete")

        return reponse
    
class GetUserProfileBasicView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        userprofile = UserProfile.objects.filter(user_id=user).first()
        imageprofile = ImageProfile.objects.filter(user_id=user).first()
        
        profileSerializer = UserProfileSerializer(userprofile)
        imageSerializer = ImageProfileSerializer(imageprofile)
        
        context = {
            'user_id': user.id,
            'name': f"{profileSerializer.data.get('first_name')} {profileSerializer.data.get('last_name')}",
            'avatar': imageSerializer.data.get('avatar')
        }
        
        return Response(context)
    
class GetMutualFriendView(APIView):
        def get(self, request):
            user = getUser(request)
            if not user:
                return Response({'error': 'Unauthorized'}, status=401)
            
            other_user_id = request.query_params.get('id')    #lấy từ fe của user kia, fe gửi lên sever id profile của người đó
            
            print(other_user_id)
            other_user = get_object_or_404(Friendship, Q(user_id1=other_user_id) | Q(user_id2=other_user_id)) # user_id1, user_id2
            
            user_friendships = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
            
            other_user_friendships = Friendship.objects.filter(Q(user_id1=other_user.user_id1) | Q(user_id2=other_user.user_id2))
            
            mutual_friendships = user_friendships.intersection(other_user_friendships)
            
            data = []
            
            for mutual_friendship in mutual_friendships:
                
                friend_profile = getUserProfileForPosts(mutual_friendship.user_id2) if user == mutual_friendship.user_id1 else getUserProfileForPosts(mutual_friendship.user_id1)
                
                data.append({
                "mutual_friendship": FriendshipSerializer(mutual_friendship).data,
                "friend_profile": friend_profile
                })
            
            return Response({
                "data": data
                })

class GetStatusFriend(APIView):
    def get(self, request):
        user = getUser(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id') 
        
        if user == other_user_id : 
            return Response({'status_relationship': 'user'})
        
        status_relationship = FriendRequest.objects.filter(from_id=user, to_id=other_user_id).first()
        
        if not status_relationship :
            return Response({'status_relationship': 'not_friend'})
        
        return Response({
            "status_relationship": status_relationship
        })

class GetFriendShip(APIView):
    def get(self, request):
        user = getUser(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id') 
        
        others_user_friend = get_object_or_404(Friendship, Q(user_id1=other_user_id) | Q(user_id2=other_user_id))
        
        data = []
        for other_user_friend in others_user_friend:
            
            friend_ship = {
                "friend_profile": getUserProfileForPosts(other_user_friend)
            }
            data.append(friend_ship)
            
        return Response({
            "data": data
        })