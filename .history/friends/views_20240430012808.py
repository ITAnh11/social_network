from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
import jwt, datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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

class SentFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        to_user_id = request.data.get('id')
        print(request.data)
        to_user = get_object_or_404(User, id = to_user_id)
        try:
            friend_request = FriendRequest.objects.create(
                from_id = user,
                to_id = to_user,
                status = 'pending'
            )
            friend_request.save()
        except :
            return Response({'error': 'Friend Request can not create'}, status=404)
        
        return Response({'success': 'Friend request sent successfully'})
    
class RevokeFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            to_id = request.data.get('id')
            #print(to_id)
            friend_request = get_object_or_404(FriendRequest, from_id=user, to_id=to_id)
            
            friend_request.delete()
            #print(user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=404)
        
        return Response({'success': 'Friend request revoked successfully'})
    
class AcceptFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        
        try:
                friend_request_id = request.data.get('id')
                friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
                
                friend_request.status = 'accepted'
                friend_request.save()
                
                friend_ship = Friendship.objects.create(
                user_id1 = user,
                user_id2 = friend_request.from_id                 
                )

                friend_ship.save()    
                 
                data = []
                
                accepted_friend_request = {
                "friend_profile" : getUserProfileForPosts(friend_request.from_id)
                }
                data.append(accepted_friend_request)
                return Response ({
                    'accepted_friend_request': data,
                    'success': 'Friend request processed successfully'
                    })
            
        except:
            return Response({'error': 'Error while saving friend request'}, status=400)

class DenineFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        # print(request.data)
        
        try:
                friend_request_id = request.data.get('id')
                friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
                
                #friend_request.status = 'pending'
                friend_request.status = 'denined'
                friend_request.save()  
                
                return Response({'success': 'Friend request processed successfully'})
            
        except:
            return Response({'error': 'Error while saving friend request'}, status=400)
    
class DeleteFriendShip(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friendship_id = request.data.get('id')
            
            friendship = get_object_or_404(Friendship,Q(user_id1=friendship_id, user_id2=user) | Q(user_id1=user, user_id2=friendship_id))
            friendrequest = get_object_or_404(FriendRequest,Q(from_id=user, to_id=friendship_id) | Q(from_id=friendship_id, to_id=user))
            
            friendrequest.delete()
            friendship.delete()
        except Friendship.DoesNotExist:
            return Response({'error': 'Friendship not found'}, status=404)
         
        return Response({'success': 'Friendship deleted successfully'})
    
class GetSentFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        list_friend_requests_sent = FriendRequest.objects.filter(from_id=user)
        #print(list_friend_requests_sent)
        for friend_request_sent in list_friend_requests_sent:
            serializer = FriendRequestSerializer(friend_request_sent)
            #print(serializer)
            
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
        #print(list_friend_requests_received)
        for friend_request_received in list_friend_requests_received:
            serializer = FriendRequestSerializer(friend_request_received)
            #print(serializer)
            
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
        
        data = []
        list_friend_ship = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
        #print(list_friend_ship)
        
        
        for friend_ship in list_friend_ship:
            
            try:
                friend = {
                "friend_ship": FriendshipSerializer(friend_ship).data,
                "friend_profile": getUserProfileForPosts(friend_ship.user_id2) if user == friend_ship.user_id1 else getUserProfileForPosts(friend_ship.user_id1)
                }
                
                data.append(friend)
            except:
                return Response({'error': 'Friendship not found'}, status=404)
        return Response({
            "data": data
            })


class GetSuggestionFriendView(APIView):
        def get(self, request):
            user = getUser(request)
            
            if not user:
                return Response({'error': 'Unauthorized'}, status=401)
            
            
            #dsach bạn bè của mình
            # user_friendships = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
            
            # suggestions = []
            
            # #chạy từng bạn bè của mình
            # for friendship in user_friendships:
            #     #tìm thằng nào là bạn bè của bạn mình
            #     mutual_friendships = Friendship.objects.filter(Q(user_id1=friendship.user_id1) | Q(user_id2=friendship.user_id1)) \
            #                                          .filter(Q(user_id1=friendship.user_id2) | Q(user_id2=friendship.user_id2))
                
            #     mutual_friendships_count = mutual_friendships.exclude(Q(user_id1=user) | Q(user_id2=user)).count()
                
            #     if mutual_friendships_count >= 1:
                    
            #         # friend_profile = getUserProfileForPosts(friendship.user_id2) if user == friendship.user_id1 else getUserProfileForPosts(friendship.user_id1)
            #         for mutual_friendship in mutual_friendships:
            #             #lấy profile của thằng suggest đó
            #             if mutual_friendship.user_id1 == friendship.user_id2 | mutual_friendship.user_id1==friendship.user_id1 :
            #                 mutual_friend_profile = getUserProfileForPosts(mutual_friendship.user_id1) 
                        
            #             elif mutual_friendship.user_id2 == friendship.user_id2 | mutual_friendship.user_id2==friendship.user_id1 :
            #                 getUserProfileForPosts(mutual_friendship.user_id1)
                        
            #             if not Friendship.objects.filter(Q(user_id1=user, user_id2=mutual_friend_profile.user) | Q(user_id1=mutual_friend_profile.user, user_id2=user)).exists():
                            
            #                 suggestions.append({
            #                 "mutual_friendships_count": mutual_friendships_count,
            #                 "mutual_friend_profile": mutual_friend_profile
            #                 })
            data = []
            
            sent_friend_requests_list = (FriendRequest.objects.filter(from_id=user).values_list('to_id', flat=True))
            received_friend_requests_list = (FriendRequest.objects.filter(to_id=user).values_list('from_id', flat=True))
            friend_list_1 = (Friendship.objects.filter(user_id1=user).values_list('user_id2', flat=True))
            friend_list_2 = (Friendship.objects.filter(user_id2=user).values_list('user_id1', flat=True))
            not_user = User.objects.filter(email=user).values_list('id', flat=True)
            
            sent_set = set(sent_friend_requests_list)
            received_set = set(received_friend_requests_list)
            friend1_set = set(friend_list_1)
            friend2_set = set(friend_list_2)
            not_user_set = set(not_user)
            
            #print(sent_set)
            other_users = list(set(User.objects.all().values_list('id', flat=True)) - (sent_set | received_set | friend1_set | friend2_set | not_user_set))
            
            for other_user in other_users:
                suggesion = get_object_or_404(User, id=other_user)
                #print(suggesion)
                suggesions = {
                    "suggestions_friend": getUserProfileForPosts(suggesion)
                }
                data.append(suggesions)
                
            
                
            return Response({
                "suggestions": data
                })

class GetMutualFriendView(APIView):
        def get(self, request):
            user = getUser(request)
            if not user:
                return Response({'error': 'Unauthorized'}, status=401)
            
            other_user_id = request.query_params.get('id')    #lấy từ fe của user kia, fe gửi lên sever id profile của người đó
            
            # print(other_user_id)
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

class GetStatusFriendView(APIView):
    def get(self, request):
        user = getUser(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id')
        print(other_user_id); 
        
        if user == other_user_id : 
            return Response({'status_relationship': 'user'})
        
        status_relationship_1_2 = FriendRequest.objects.filter(from_id=user, to_id=other_user_id).values_list('status', flat=True).first()
        status_relationship_2_1 = FriendRequest.objects.filter(from_id=other_user_id, to_id=user).values_list('status', flat=True).first()
        
        print(status_relationship_1_2, status_relationship_2_1)
        if status_relationship_1_2 == 'accepted' or status_relationship_2_1 == 'accepted' :
            return Response({'status_relationship': 'accepted'})
        elif status_relationship_1_2 == 'denied' or status_relationship_2_1 == 'denied':
            return Response({'status_relationship': 'denied'})
        elif status_relationship_1_2 == 'pending' :
            return Response({'status_relationship': 'friendrequestfromuser'})
        elif status_relationship_2_1 == 'pending' :
            return Response({'status_relationship': 'friendrequesttouser'})
        return Response({
            "status_relationship": 'not_friend'
        })

class GetListFriendOfUserOtherView(APIView):
    def get(self, request):
        user = getUser(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id') 
        # other_user_id = request.data.get('id')
        print(other_user_id)    
       # others_user_friend = get_object_or_404(Friendship, Q(user_id1=other_user_id) | Q(user_id2=other_user_id))
        others_user_friend = Friendship.objects.filter(Q(user_id1=other_user_id) | Q(user_id2=other_user_id))
        print('hi: ',others_user_friend)
        data = []
        for other_user_friend in others_user_friend:
            print(str(other_user_friend.user_id1))
            if other_user_id == str(other_user_friend.user_id2):
                friend_id = other_user_friend.user_id1
                print('ok') 
            else :
                friend_id = other_user_friend.user_id2
                print('okkkk') 

            friend_ship = {
                "friend_profile": getUserProfileForPosts(friend_id)
            }
            data.append(friend_ship)
            
        return Response({
            "data": data
        })
        
# class GetMutualFriendOfUserView(APIView):
#         def get(self, request):
#             user = getUser(request)
#             if not user:
#                 return Response({'error': 'Unauthorized'}, status=401)
            
#             other_user_id = request.get('user_id')    #lấy từ fe của các user
            
#             other_user = get_object_or_404(Friendship, id=other_user_id)
            
#             user_friendships = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
            
#             other_user_friendships = Friendship.objects.filter(Q(user_id1=other_user.user_id1) | Q(user_id2=other_user.user_id2))
            
#             mutual_friendships = user_friendships.intersection(other_user_friendships)
            
#             data = []
            
#             for mutual_friendship in mutual_friendships:
                
#                 friend_profile = getUserProfileForPosts(mutual_friendship.user_id2) if user == mutual_friendship.user_id1 else getUserProfileForPosts(mutual_friendship.user_id1)
                
#                 data.append({
#                 "mutual_friendship": FriendshipSerializer(mutual_friendship).data,
#                 "friend_profile": friend_profile
#                 })
            
#             return Response({
#                 "data": data
#                 })

class AcceptFriendRequestProfileView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        # print(request.data)
        
        try:
                from_user_id = request.data.get('id')
                friend_request = get_object_or_404(FriendRequest, from_id = from_user_id, to_id = user)
                
                #friend_request.status = 'pending'
                friend_request.status = 'accepted'
                friend_request.save()
                
                friend_ship = Friendship.objects.create(
                user_id1 = user,
                user_id2 = friend_request.from_id                 
                )
                # Friendship.objects.all().delete()  
                friend_ship.save()    
                 
                data = []
                
                accepted_friend_request = {
                "friend_profile" : getUserProfileForPosts(friend_request.from_id)
                }
                data.append(accepted_friend_request)
                return Response ({
                    'accepted_friend_request': data,
                    'success': 'Friend request processed successfully'
                    })
                # return Response({'success': 'Friend request processed successfully'})
            
        except:
            return Response({'error': 'Error while saving friend request'}, status=400)
    
class DenineFriendRequestProfileView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        # print(request.data)
        
        try:
                from_user_id = request.data.get('id')
                friend_request = get_object_or_404(FriendRequest, from_id = from_user_id, to_id = user)
                
                #friend_request.status = 'pending'
                friend_request.status = 'denined'
                friend_request.save()  
                
                return Response({'success': 'Friend request processed successfully',
                                 'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)})
            
        except:
            return Response({'error': 'Error while saving friend request'}, status=400)
        
# class DeleteFriendShipProfile(APIView):
#     def post(self, request):
#         user = getUser(request)
        
#         if not user:
#             return Response({'error': 'Unauthorized'}, status=401)
        
#         try:
#             friend_id = request.data.get('id')
#             friendship = get_object_or_404(Friendship, id = friendship_id)
            
#             friendship.delete()
#         except Friendship.DoesNotExist:
#             return Response({'error': 'Friendship not found'}, status=404)
         
#         return Response({'success': 'Friendship deleted successfully'})