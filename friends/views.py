from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
import jwt, datetime
import logging
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from common_functions.common_function import getUser, getUserProfileForPosts
from users.models import User
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer

from notifications.views import createAddFriendNotification, GetNotifications
from notifications.models import AddFriendNotifications

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
# Create your views here.
# friend_request.status = 'accepted'  # Cập nhật trạng thái của yêu cầu kết bạn thành 'accepted'
# friend_request.save()  # Lưu thay đổi vào cơ sở dữ liệu
# friend_request.delete()  # Xóa yêu cầu kết bạn khỏi cơ sở dữ liệu
from django.db import connection
from django.db import transaction

logger = logging.getLogger(__name__)

class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class FriendsRequestsView(APIView):
    def get(self, request):
        try:
            user = getUser(request)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('users:login'))
        
        if not user:
            logger.warning("Unauthorized access to FriendsRequestsView. Redirecting to login page.")
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request,'friends/friend.html')

# class SentFriendRequestView(APIView):
#     def post(self, request):
#         user = getUser(request)
        
#         if not user:
#             logger.error("Unauthorized access to SentFriendRequestView. Returning 401 error.")
#             return Response({'error': 'Unauthorized'}, status=401)
        
#         to_user_id = request.data.get('id')
#         logger.info(f"Sending friend request to user {to_user_id}.")
#         print(request.data)
#         to_user = get_object_or_404(User, id = to_user_id)
#         try:
#             friend_request = FriendRequest.objects.create(
#                 from_id = user,
#                 to_id = to_user,
#                 status = 'pending'
#             )
#             friend_request.save()
            
#             createAddFriendNotification(friend_request)
#             logger.info("Friend request sent successfully.")
#         except Exception as e:
#             logger.error(f"Failed to send friend request: {str(e)}")
#             return Response({'error': 'Friend Request can not create'}, status=404)
        
#         return Response({'success': 'Friend request sent successfully'})
class SentFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to SentFriendRequestView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)

        to_user_id = request.data.get('id')
        logger.info(f"Sending friend request to user {to_user_id}.")
        
        # Gọi hàm procedure để kiểm tra giới hạn số lượng bạn bè
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute('CALL check_friend_limit(%s)', [to_user_id])
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=400)
        
        try:
            # Thêm yêu cầu kết bạn vào cơ sở dữ liệu
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO friends_friendrequest (from_id_id, to_id_id, status, created_at, updated_at) "
                        "VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                        [user.id, to_user_id, 'pending']
                    )
            for friend_request in FriendRequest.objects.raw("SELECT * FROM friends_friendrequest WHERE from_id_id = %s AND to_id_id = %s AND status = %s",
                                            [user.id, to_user_id, 'pending']) :
                    createAddFriendNotification(friend_request)
                    logger.info("Friend request sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send friend request: {str(e)}")
            return Response({'error': str(e)}, status=400)
        
        return Response({'success': 'Friend request sent successfully'})
    
# class RevokeFriendRequestView(APIView):
#     def post(self, request):
#         user = getUser(request)
        
#         if not user:
#             logger.error("Unauthorized access to RevokeFriendRequestView. Returning 401 error.")
#             return Response({'error': 'Unauthorized'}, status=401)
        
#         try:
#             to_id = request.data.get('id')
#             #print(to_id)
#             friend_request = get_object_or_404(FriendRequest, from_id=user, to_id=to_id)
            
#             friend_request.delete()
#             logger.info("Friend request revoked successfully.")
#             #print(user)
#         except FriendRequest.DoesNotExist:
#             logger.warning("Friend request not found.")
#             return Response({'error': 'Friend request not found'}, status=404)
        
#         return Response({'success': 'Friend request revoked successfully'})
    
class RevokeFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to RevokeFriendRequestView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            to_id = request.data.get('id')
            logger.info("Friend request revoked successfully.")

            with connection.cursor() as cursor:
                cursor.execute(
                "DELETE FROM friends_friendrequest WHERE from_id_id = %s AND to_id_id = %s AND status = %s",
                [user.id, to_id, 'pending']
                )
                
        except FriendRequest.DoesNotExist:
            logger.warning("Friend request not found.")
            return Response({'error': 'Friend request not found'}, status=404)
        
        return Response({'success': 'Friend request revoked successfully'})
    
# class AcceptFriendRequestView(APIView):
#     def post(self, request):
#         user = getUser(request)
        
#         if not user:
#             logger.error("Unauthorized access to AcceptFriendRequestView. Returning 401 error.")
#             return Response({'error': 'Unauthorized'}, status=401)
        
        
#         try:
#                 friend_request_id = int(request.data.get('id'))
#                 friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
                
#                 friend_request.status = 'accepted'
#                 friend_request.save()
                
#                 addfriendNotification = AddFriendNotifications.objects(__raw__={'id_friend_request': friend_request_id}).first()
#                 addfriendNotification.setAccept()
#                 addfriendNotification.save()
                
#                 friend_ship = Friendship.objects.create(
#                 user_id1 = user,
#                 user_id2 = friend_request.from_id                 
#                 )

#                 friend_ship.save()    
                 
#                 data = []
                
#                 accepted_friend_request = {
#                 "friend_profile" : getUserProfileForPosts(friend_request.from_id)
#                 }
#                 data.append(accepted_friend_request)
                
#                 GetNotifications().resetNotifications(user.id)
#                 logger.info("Friend request accepted successfully.")
#                 return Response ({
#                     'accepted_friend_request': data,
#                     'success': 'Friend request processed successfully'
#                     })
            
#         except Exception as e:
#             logger.error(f"Error while accepting friend request: {str(e)}")
#             print(e)
#             return Response({'error': 'Error while saving friend request'}, status=400)

class AcceptFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to AcceptFriendRequestView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        
        try:
                friend_request_id = int(request.data.get('id'))
                
                for fr_r in FriendRequest.objects.raw("SELECT * FROM friends_friendrequest WHERE id = %s AND status = 'pending'", [friend_request_id]) :
                    friend_request = fr_r
                
                with connection.cursor() as cursor:
                    cursor.execute(
                    "UPDATE friends_friendrequest SET status = 'accepted' WHERE id = %s AND status = 'pending'",
                    [friend_request_id]
                )
                    
                addfriendNotification = AddFriendNotifications.objects(__raw__={'id_friend_request': friend_request_id}).first()
                addfriendNotification.setAccept()
                addfriendNotification.save()
                   
                
                data = []
                
                accepted_friend_request = {
                "friend_profile" : getUserProfileForPosts(friend_request.from_id)
                }
                data.append(accepted_friend_request)
                return Response ({
                    'accepted_friend_request': data,
                    'success': 'Friend request processed successfully'
                    })
            
        except Exception as e:
            print(e)
            return Response({'error': 'Error while saving friend request'}, status=400)
        
# class DenineFriendRequestView(APIView):
#     def post(self, request):
#         user = getUser(request)
        
#         if not user:
#             logger.error("Unauthorized access to DenyFriendRequestView. Returning 401 error.")
#             return Response({'error': 'Unauthorized'}, status=401)
        
#         # print(request.data)
        
#         try:
#                 friend_request_id = int(request.data.get('id'))
#                 friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
                
#                 #friend_request.status = 'pending'
#                 friend_request.status = 'denined'
#                 friend_request.save()
                
#                 addfriendNotification = AddFriendNotifications.objects(__raw__={'id_friend_request': friend_request_id}).first()
#                 addfriendNotification.setDecline()
#                 addfriendNotification.save()
                
#                 GetNotifications().resetNotifications(user.id)
#                 logger.info("Friend request denied successfully.")
#                 return Response({'success': 'Friend request processed successfully'})
            
#         except Exception as e:
#             logger.error(f"Error while denying friend request: {str(e)}")
#             print(e)
#             return Response({'error': 'Error while saving friend request'}, status=400)

class DenineFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
                friend_request_id = int(request.data.get('id'))
                
                with connection.cursor() as cursor:
                    cursor.execute(
                    "UPDATE friends_friendrequest SET status = 'denied' WHERE id = %s AND status = 'pending'",
                    [friend_request_id]
                )
                addfriendNotification = AddFriendNotifications.objects(__raw__={'id_friend_request': friend_request_id}).first()
                addfriendNotification.setDecline()
                addfriendNotification.save()
                
                return Response({'success': 'Friend request processed successfully'})
            
        except Exception as e:
            print(e)
            return Response({'error': 'Error while saving friend request'}, status=400)
    
# class DeleteFriendShip(APIView):
#     def post(self, request):
#         user = getUser(request)
        
#         if not user:
#             logger.error("Unauthorized access to DeleteFriendship. Returning 401 error.")
#             return Response({'error': 'Unauthorized'}, status=401)
        
#         try:
#             friendship_id = request.data.get('id')
            
#             friendship = get_object_or_404(Friendship,Q(user_id1=friendship_id, user_id2=user) | Q(user_id1=user, user_id2=friendship_id))
#             friendrequest = get_object_or_404(FriendRequest,Q(from_id=user, to_id=friendship_id) | Q(from_id=friendship_id, to_id=user))
            
#             friendrequest.delete()
#             friendship.delete()
#             logger.info("Friendship deleted successfully.")
#         except Friendship.DoesNotExist:
#             logger.warning("Friendship not found.")
#             return Response({'error': 'Friendship not found'}, status=404)
         
#         return Response({'success': 'Friendship deleted successfully'})

class DeleteFriendShip(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friend_id = int(request.data.get('id'))
                    
            for fr_r in FriendRequest.objects.raw("SELECT * FROM friends_friendrequest WHERE ((from_id_id = %s AND to_id_id = %s) OR (from_id_id = %s AND to_id_id = %s)) AND status = 'accepted'", 
                                                  [user.id, friend_id, friend_id, user.id]) :
                    friend_request = fr_r
                    
            with connection.cursor() as cursor:
                cursor.execute(
                "DELETE FROM friends_friendrequest WHERE id = %s",
                [friend_request.id]
                )    
        except Friendship.DoesNotExist:
            return Response({'error': 'Friendship not found'}, status=404)
         
        return Response({'success': 'Friendship deleted successfully'})
    
class GetSentFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetSentFriendRequestsView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        try:
            # list_friend_requests_sent = FriendRequest.objects.filter(from_id=user)
            # for friend_request_sent in list_friend_requests_sent:
            #     serializer = FriendRequestSerializer(friend_request_sent)
            #     friend_request = {
            #         "friend_request_sent": serializer.data,
            #         "friend_request_profile": getUserProfileForPosts(friend_request_sent.to_id)
            #     }
            #     data.append(friend_request)
            for friend_request_sent in FriendRequest.objects.raw("SELECT* FROM friends_friendrequest WHERE from_id_id = %s AND status = 'pending'", [user.id]):
                serializer = FriendRequestSerializer(friend_request_sent)
            
                friend_request = {
                    "friend_request_sent" : serializer.data,
                    "friend_request_profile": getUserProfileForPosts(friend_request_sent.to_id)
                }
                data.append(friend_request)
        except Exception as e:
            logger.error(f"Error while retrieving sent friend requests: {str(e)}")
            return Response({'error': 'Error while retrieving sent friend requests'}, status=400)
        
        return Response({"data": data})

class GetReceivedFriendRequestsView(generics.ListAPIView):
    pagination_class = CustomPagination

    # def get(self, request):
    #     user = getUser(request)
        
    #     if not user:
    #         logger.error("Unauthorized access to GetReceivedFriendRequestsView. Returning 401 error.")
    #         return Response({'error': 'Unauthorized'}, status=401)
        
    #     data = []
    #     try:
    #         list_friend_requests_received = FriendRequest.objects.filter(to_id=user)
    #         for friend_request_received in list_friend_requests_received:
    #             serializer = FriendRequestSerializer(friend_request_received)
    #             friend_request = {
    #                 "friend_request_received": serializer.data,
    #                 "friend_request_profile": getUserProfileForPosts(friend_request_received.from_id)
    #             }
    #             data.append(friend_request)
    #     except Exception as e:
    #         logger.error(f"Error while retrieving received friend requests: {str(e)}")
    #         return Response({'error': 'Error while retrieving received friend requests'}, status=400)
        
    #     return Response({"data": data})

    def get_queryset(self):
        user = getUser(self.request)
        
        if not user:
            logger.error("Unauthorized access to GetReceivedFriendRequestsView. Returning 401 error.")
            return FriendRequest.objects.none()
        
        return FriendRequest.objects.filter(to_id=user)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                data = []
                for friend_request_received in page:
                    serializer = FriendRequestSerializer(friend_request_received)
                    friend_request = {
                        "friend_request_received": serializer.data,
                        "friend_request_profile": getUserProfileForPosts(friend_request_received.from_id)
                    }
                    data.append(friend_request)
                return self.get_paginated_response(
                    {
                        "data": data,
                    }
                )

        except Exception as e:
            logger.error(f"Error while retrieving received friend requests: {str(e)}")
            return Response({'error': 'Error while retrieving received friend requests'}, status=400)


class GetListFriendView(generics.ListAPIView):
    pagination_class = CustomPagination

    # def get(self, request):
    #     user = getUser(request)
        
    #     if not user:
    #         logger.error("Unauthorized access to GetListFriendView. Returning 401 error.")
    #         return Response({'error': 'Unauthorized'}, status=401)
        
    #     data = []
    #     try:
    #         list_friend_ship = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
    #         for friend_ship in list_friend_ship:
    #             try:
    #                 friend = {
    #                     "friend_ship": FriendshipSerializer(friend_ship).data,
    #                     "friend_profile": getUserProfileForPosts(friend_ship.user_id2) if user == friend_ship.user_id1 else getUserProfileForPosts(friend_ship.user_id1)
    #                 }
    #                 data.append(friend)
    #             except:
    #                 logger.error("Friendship not found.")
    #                 return Response({'error': 'Friendship not found'}, status=404)
    #     except Exception as e:
    #         logger.error(f"Error while retrieving list of friends: {str(e)}")
    #         return Response({'error': 'Error while retrieving list of friends'}, status=400)
        
    #     return Response({"data": data})

    def list(self, request, *args, **kwargs):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetListFriendView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        try:
            key = f"all_friends_{user.id}"
            if (cache.get(key)): 
                list_friend_ship = cache.get(key) 
            else:
                list_friend_ship = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
                cache.set(key, list_friend_ship)
            
            page = self.paginate_queryset(list_friend_ship)

            for friend_ship in page:
                try:
                    friend = {
                    "friend_ship": FriendshipSerializer(friend_ship).data,
                    "friend_profile": getUserProfileForPosts(friend_ship.user_id2) if user == friend_ship.user_id1 else getUserProfileForPosts(friend_ship.user_id1)
                    }
                    
                    data.append(friend)
                except:
                    logger.error("Friendship not found.")
                    return Response({'error': 'Friendship not found'}, status=404)
        except Exception as e:
            logger.error(f"Error while retrieving list of friends: {str(e)}")
            return Response({'error': 'Error while retrieving list of friends'}, status=400)
        
        return self.get_paginated_response({
            "data": data,
        })

class GetSuggestionFriendView(generics.ListAPIView):
    pagination_class = CustomPagination

    # def get(self, request):
    #     user = getUser(request)
        
    #     if not user:
    #         logger.error("Unauthorized access to GetSuggestionFriendView. Returning 401 error.")
    #         return Response({'error': 'Unauthorized'}, status=401)
        
    #     data = []
        
    #     try:
    #         sent_friend_requests_list = FriendRequest.objects.filter(from_id=user).values_list('to_id', flat=True)
    #         received_friend_requests_list = FriendRequest.objects.filter(to_id=user).values_list('from_id', flat=True)
    #         friend_list_1 = Friendship.objects.filter(user_id1=user).values_list('user_id2', flat=True)
    #         friend_list_2 = Friendship.objects.filter(user_id2=user).values_list('user_id1', flat=True)
    #         not_user = User.objects.filter(email=user).values_list('id', flat=True)
            
    #         sent_set = set(sent_friend_requests_list)
    #         received_set = set(received_friend_requests_list)
    #         friend1_set = set(friend_list_1)
    #         friend2_set = set(friend_list_2)
    #         not_user_set = set(not_user)
            
    #         other_users = list(set(User.objects.all().values_list('id', flat=True)) - (sent_set | received_set | friend1_set | friend2_set | not_user_set))
            
    #         for other_user in other_users:
    #             suggesion = get_object_or_404(User, id=other_user)
    #             suggesions = {
    #                 "suggestions_friend": getUserProfileForPosts(suggesion)
    #             }
    #             data.append(suggesions)
    #     except Exception as e:
    #         logger.error(f"Error while retrieving friend suggestions: {str(e)}")
    #         return Response({'error': 'Error while retrieving friend suggestions'}, status=400)
        
    #     return Response({"suggestions": data})

    def get_queryset(self):
        user = getUser(self.request)

        if not user:
            logger.error("Unauthorized access to GetSuggestionFriendView. Returning 401 error.")
            return User.objects.none()

        sent_friend_requests_list = FriendRequest.objects.filter(from_id=user).values_list('to_id', flat=True)
        received_friend_requests_list = FriendRequest.objects.filter(to_id=user).values_list('from_id', flat=True)
        friend_list_1 = Friendship.objects.filter(user_id1=user).values_list('user_id2', flat=True)
        friend_list_2 = Friendship.objects.filter(user_id2=user).values_list('user_id1', flat=True)
        not_user = User.objects.filter(email=user).values_list('id', flat=True)

        sent_set = set(sent_friend_requests_list)
        received_set = set(received_friend_requests_list)
        friend1_set = set(friend_list_1)
        friend2_set = set(friend_list_2)
        not_user_set = set(not_user)

        other_users = list(set(User.objects.all().values_list('id', flat=True)) - (sent_set | received_set | friend1_set | friend2_set | not_user_set))

        return other_users

    def list(self, request, *args, **kwargs):
        
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetSuggestionFriendView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        
        try:
            queryset = self.get_queryset()

            page = self.paginate_queryset(queryset)
            if page is not None: 
                for other_user in page:
                    suggesion = get_object_or_404(User, id=other_user)
                    suggesions = {
                        "suggestions_friend": getUserProfileForPosts(suggesion)
                    }
                    data.append(suggesions)
        except Exception as e:
            logger.error(f"Error while retrieving friend suggestions: {str(e)}")
            return Response({'error': 'Error while retrieving friend suggestions'}, status=400)
        
        return self.get_paginated_response({"suggestions": data})


class GetMutualFriendView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetMutualFriendView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id')
        
        try:
            other_user = get_object_or_404(Friendship, Q(user_id1=other_user_id) | Q(user_id2=other_user_id))
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
        except Exception as e:
            logger.error(f"Error while retrieving mutual friends: {str(e)}")
            return Response({'error': 'Error while retrieving mutual friends'}, status=400)
        
        return Response({"data": data})

class GetStatusFriendView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetStatusFriendView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id')
        
        try:
            if user == other_user_id: 
                return Response({'status_relationship': 'user'})
            
            # status_relationship_1_2 = FriendRequest.objects.filter(from_id=user, to_id=other_user_id).values_list('status', flat=True).first()
            # status_relationship_2_1 = FriendRequest.objects.filter(from_id=other_user_id, to_id=user).values_list('status', flat=True).first()
            cursor = connection.cursor()
            cursor.execute("SELECT status FROM friends_friendrequest WHERE from_id_id = %s AND to_id_id = %s ORDER BY id DESC LIMIT 1", [user.id, other_user_id])
            status_relationship_1_2_result = cursor.fetchone()
            status_relationship_1_2 = status_relationship_1_2_result[0] if status_relationship_1_2_result else None

            # status_relationship_2_1
            cursor.execute("SELECT status FROM friends_friendrequest WHERE to_id_id = %s AND from_id_id = %s ORDER BY id DESC LIMIT 1", [user.id, other_user_id])
            status_relationship_2_1_result = cursor.fetchone()
            status_relationship_2_1 = status_relationship_2_1_result[0] if status_relationship_2_1_result else None
            
            if status_relationship_1_2 == 'accepted' or status_relationship_2_1 == 'accepted':
                return Response({'status_relationship': 'accepted'})
            elif status_relationship_1_2 == 'denied' or status_relationship_2_1 == 'denied':
                return Response({'status_relationship': 'denied'})
            elif status_relationship_1_2 == 'pending':
                return Response({'status_relationship': 'friendrequestfromuser'})
            elif status_relationship_2_1 == 'pending':
                return Response({'status_relationship': 'friendrequesttouser'})
        except Exception as e:
            logger.error(f"Error while retrieving friend status: {str(e)}")
            return Response({'error': 'Error while retrieving friend status'}, status=400)
        
        return Response({"status_relationship": 'not_friend'})

class GetListFriendOfUserOtherView(generics.ListAPIView):
    pagination_class = CustomPagination

    def get(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetListFriendOfUserOtherView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id') 
        
        try:
            key = f"all_friends_{other_user_id}"
            if (cache.get(key)): 
                others_user_friend = cache.get(key) 
            else:
                others_user_friend = Friendship.objects.filter(Q(user_id1=other_user_id) | Q(user_id2=other_user_id))
                cache.set(key, others_user_friend)

            #page = self.paginate_queryset(others_user_friend)


            data = []
            cursor = connection.cursor()
            cursor.execute("SELECT email FROM users_user "
                                "WHERE id = %s", [other_user_id])
            user_id_result = cursor.fetchone()
            user_id = user_id_result[0] if user_id_result else None
            
            for other_user_friend in Friendship.objects.raw("SELECT * FROM friends_friendship "
                                                            "WHERE user_id1_id = %s OR user_id2_id = %s", [other_user_id, other_user_id]):
                
                if user_id == str(other_user_friend.user_id2):
                    friend_id = other_user_friend.user_id1
                    
                else :
                    friend_id = other_user_friend.user_id2

                friend_ship = {
                    "friend_profile": getUserProfileForPosts(friend_id)
                }
                data.append(friend_ship)
        except Exception as e:
            logger.error(f"Error while retrieving friend list of other user: {str(e)}")
            return Response({'error': 'Error while retrieving friend list of other user'}, status=400)
        
        return Response({"data": data, "number_of_friends": len(data)})

    def list(self, request, *args, **kwargs):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to GetListFriendOfUserOtherView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        other_user_id = request.query_params.get('id') 
        
        try:
            key = f"all_friends_{other_user_id}"
            if (cache.get(key)): 
                others_user_friend = cache.get(key) 
            else:
                others_user_friend = Friendship.objects.filter(Q(user_id1=other_user_id) | Q(user_id2=other_user_id))
                cache.set(key, others_user_friend)

            page = self.paginate_queryset(others_user_friend)

            data = []
            for other_user_friend in page:
                user_id = User.objects.filter(id=other_user_id).values_list('email', flat=True).first()
            
                if user_id == str(other_user_friend.user_id2):
                    friend_id = other_user_friend.user_id1
                else:
                    friend_id = other_user_friend.user_id2

                friend_ship = {
                    "friend_profile": getUserProfileForPosts(friend_id)
                }
                data.append(friend_ship)
        except Exception as e:
            logger.error(f"Error while retrieving friend list of other user: {str(e)}")
            return Response({'error': 'Error while retrieving friend list of other user'}, status=400)
        
        return self.get_paginated_response({
            "data": data, 
            "number_of_friends": len(data)
        })

        

class AcceptFriendRequestProfileView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to AcceptFriendRequestProfileView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            from_user_id = request.data.get('id')
            for fr_r in FriendRequest.objects.raw("SELECT * FROM friends_friendrequest WHERE from_id_id = %s AND to_id_id = %s AND status = 'pending' ", [from_user_id, user.id]) :
                    friend_request = fr_r
               
            with connection.cursor() as cursor:
                cursor.execute(
                "UPDATE friends_friendrequest SET status = 'accepted' WHERE id = %s AND status = 'pending'",
                [friend_request.id]
            )
            
            addfriendNotification = AddFriendNotifications.objects(__raw__={'id_friend_request': friend_request.id}).first()
            addfriendNotification.setAccept()
            addfriendNotification.save()    
             
            data = []
            
            accepted_friend_request = {
                "friend_profile": getUserProfileForPosts(friend_request.from_id)
            }
            data.append(accepted_friend_request)
            
            GetNotifications().resetNotifications(user.id)
            
            logger.info("Friend request accepted successfully.")
            
            return Response({
                'accepted_friend_request': data,
                'success': 'Friend request processed successfully'
            })
        
        except Exception as e:
            logger.error(f"Error while saving friend request: {str(e)}")
            return Response({'error': 'Error while saving friend request'}, status=400)

class DenineFriendRequestProfileView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            logger.error("Unauthorized access to DenyFriendRequestProfileView. Returning 401 error.")
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            from_user_id = request.data.get('id')
            for fr_r in FriendRequest.objects.raw("SELECT * FROM friends_friendrequest WHERE from_id_id = %s AND to_id_id = %s AND status = 'pending' ", [from_user_id, user.id]) :
                    friend_request = fr_r
                
            with connection.cursor() as cursor:
                cursor.execute(
                "UPDATE friends_friendrequest SET status = 'denied' WHERE id = %s AND status = 'pending'",
                [friend_request.id]
            )
            
            addfriendNotification = AddFriendNotifications.objects(__raw__={'id_friend_request': friend_request.id}).first()
            addfriendNotification.setDecline()
            addfriendNotification.save()
            
            GetNotifications().resetNotifications(user.id)
            
            logger.info("Friend request denied successfully.")
            
            return Response({
                'success': 'Friend request processed successfully',
                'redirect_url': reverse('userprofiles:profile') + '?id=' + str(user.id)
            })
        
        except Exception as e:
            logger.error(f"Error while saving friend request: {str(e)}")
            return Response({'error': 'Error while saving friend request'}, status=400)
        
