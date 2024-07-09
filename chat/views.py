import datetime
import logging
import json
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Subquery, OuterRef, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .serializers import UserInfoSerializer, ChannelSerializer, MesseejiSerializer

from users.models import User
from userprofiles.models import UserProfile

from .models import Channel, Messeeji, Participants

from common_functions.common_function import getUserProfileForPosts, getTimeDuration, getUser
from django.shortcuts import render, redirect
from mongoengine.errors import DoesNotExist


from django.views.decorators.cache import cache_page
from social_network.redis_conn import redis_server
from mongoengine import connect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache

from rest_framework.pagination import PageNumberPagination


logger=logging.getLogger(__name__)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class ChatTestView(APIView):

    def post(self, request):

        try:
            username = request.POST.get('username')
            list_users = SearchUser.search(SearchUser, username)
            user_ids = [user.user_id.id for user in list_users]
            # list_channels = Channel.objects(user_id__in=user_ids)
            
            return render(request, "chat/index.html")
        
        except Channel.DoesNotExist:
            logger.exception("Channel does not exist")
            CreateChannel.create(request)

    def showAllChannel(request, list_channels):
        response = Response()

        data = []
        for channel in list_channels:
            data.append(ChannelSerializer(channel).data)
        
        response.data = {
            'channel' : data
        }
        return response

    def get(self, request):
        context = {}
        return render(request, "chat/index.html", context)

class GetMesseeji(APIView):
    def post(self, request):
        try:
            channel_id = request.data.get('channel_id')
            key = f"all_chat_channel_{channel_id}"
            if (cache.get(key)):
                all_messeeji = cache.get(key)
            else: 
                all_messeeji = Messeeji.objects(channel_id=channel_id)
                cache.set(f"all_chat_channel_{channel_id}", all_messeeji)
            
            response = Response()
            data = []
            
            if not all_messeeji:
                response.data = {
                    "status" : "no messeeji found!",
                    "data" : []
                }
            else:
                for messeeji in all_messeeji:
                    messeeji_data = MesseejiSerializer(messeeji).data
                    data.append(messeeji_data)
                response.data = {
                    'status' : "messeeji found! bandai",
                    'data' : data
                }
            return response
        except Exception as e:
            print(f"exception: {e}")
            logger.exception(f"Error fetching messeeji: {str(e)}")


class GetChannels(APIView):
    def get_channels_by(query):
        channels = Channel.objects(query)
        
        list_channels = []
        for c in channels:
            list_channels.append(ChannelSerializer(c))
        return list_channels

    def get(self, request):
        response = Response()
        try:
            channel_id = int(request.data.get('post_id'))
            list_channels = self.get_channels_by(__raw__={'channel_id':channel_id})

            response.data = {
                'channel' : list_channels
            }
        except Exception as e:
            logger.exception(f"Error fetching channels: {str(e)}")
        return response
    
class CreateMesseeji(APIView):
    def create(self, request):
        return Messeeji(
            sender_id=int(request.data.get('user_id')),
            channel_id=request.data.get('channel_id'),
            message_content=request.data.get('message_content'),
            status=request.data.get('status'),
            created_at=datetime.datetime.now(),
        )

    def post(self, request):
        try:
            user = getUser(request)
            if not user:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            response = Response()

            messeeji = self.create(request)
            messeeji.save()
            logger.info('created messeeji successfully')
            response.data = {
                "status": "new messeeji created!",
                "data": [MesseejiSerializer(messeeji).data]
            }
            return response
        except Exception as e:
            logger.exception(f"Error creating messeeji: {str(e)}")

class CreateChannel(APIView):
    def check_existing_channel(self, user_id1, user_id2):
        try:
            # Define keys for caching
            key_user1 = f"participants_user_{user_id1}"
            key_user2 = f"participants_user_{user_id2}"

            # Check if data is cached
            cached_part_user1 = cache.get(key_user1)
            cached_part_user2 = cache.get(key_user2)

            # Retrieve data from cache if available
            if cached_part_user1:
                part_user1 = cached_part_user1
            else:
                part_user1 = Participants.objects(user_id=user_id1)
                cache.set(key_user1, part_user1)

            if cache.get(key_user2):
                part_user2 = cached_part_user2
            else:
                part_user2 = Participants.objects(user_id=user_id2)
                cache.set(key_user2, part_user2)

            channels_user1 = [participant.channel_id for participant in part_user1]
            channels_user2 = [participant.channel_id for participant in part_user2]
            common_channels = set(channels_user1) & set(channels_user2)
            if common_channels:
                channel = Channel.objects(channel_id=list(common_channels)[0])
                return True, channel
            else:
                return False, None
        except DoesNotExist:
            return False, None

    def create(self, request):
        try:
            user = getUser(request)
            user_id = user.id
            target_id = request.data.get('target_id')
            existed_channel = self.check_existing_channel(user_id, target_id)
            if existed_channel[0]:
                output_channel = existed_channel[1].first()
                return False, output_channel
            else:
                new_channel =  Channel(
                    created_at = datetime.datetime.now(),
                    capacity = 2,
                )
                part_user = Participants(
                    user_id = user_id,
                    channel_id = new_channel.id,
                )
                part_target = Participants(
                    user_id = target_id,
                    channel_id = new_channel.id
                )
                new_channel.save()
                part_user.save()
                part_target.save()
                logger.info('saved channel succesfully')
            return True, new_channel
        except Exception as e:
            logger.error('can not save channel like I want')
            return False, None
    def post(self, request):
        try:
            user = getUser(request)
            if not user:
                return Response({"message": "Unauthorized"}, status=401)
            
            response = Response()
            success, channel = self.create(request)
            if not channel:
                response.data = {
                    "status" : "no channel created!",
                    "data" : []
                }
            else:
                output_channel = channel

            if success:
                response.data = {
                    "status" : "new channel created!",
                    "data" : [ChannelSerializer(output_channel).data]
                }
            else:
                response.data = {
                    "status" : "existing channel found!",
                    "data" : [ChannelSerializer(output_channel).data]
                }
            return response
        except Exception as e:
            logger.exception(f"Error creating channel: {str(e)}")

class MarkReadMesseeji(APIView):

    def mark_message_as_read(self, messeeji_ids):
        try:
            # print("im first")     
            # Get the MongoDB collection object
            collection = Messeeji._get_collection()
            # print("done collection")
            # Write your raw MongoDB update query
            raw_query = {
                "_id": {"$in": messeeji_ids}
            }
            # print(f"Raw query: {raw_query}")
            update_query = {
                "$set": {"is_read": True}
            }
            # Execute the raw update query
            result = collection.update_many(raw_query, update_query)
            # print(f"result: {result}")
            # Check if the update was successful
            if result.matched_count > 0:
                return "Message marked as read successfully"
            else:
                return "Message does not exist"
        except Exception as e:
            return f"Error occurred: {e}"

    def filter_unread_messeejis(self, channel_id, sender_id):
        try:
            # Get the MongoDB collection object
            collection = Messeeji._get_collection()
            # print(f"collection: {collection}")
            # Write your raw MongoDB find query
            raw_query = {
                'channel_id': channel_id,
                'sender_id': sender_id,
                'is_read': False
            }

            # Execute the raw find query
            unread_messeejis = collection.find(raw_query)

            data = []
            for messeeji in unread_messeejis:
                # Process your data here
                data.append(messeeji)

            response = {
                'status': 'Unread messeejis found!' if data else 'No unread Messeejis found.',
                'data' : data,
            }
            return response
        except Exception as e:
            print(f"Error occurred: {e}")

    def post(self, request):
        try:
            # Extract channel_id and sender_id from the request
            channel_id = request.data.get('channel_id')
            sender_id = request.data.get('sender_id')

            # print(f"sender: {sender_id}, channel: {channel_id}")
            
            # Filter unread messeejis
            unread_messeejis_data = self.filter_unread_messeejis(channel_id, sender_id)
            # print(f"unread_m_data: {unread_messeejis_data}")
            # Mark unread messeejis as read
            # print(f"2. {unread_messeejis_data['data']}")
            
            unread_messeeji_ids = [messeeji['_id'] for messeeji in unread_messeejis_data['data']]
            # print(f"unread_m_ids: {unread_messeeji_ids}")
            mark_status = self.mark_message_as_read(unread_messeeji_ids)

            return Response({
                'status': mark_status,
                'unread_messeejis': unread_messeejis_data
            })
        except Exception as e:
            return Response({'error': f"Error occurred: {e}"}, status=500)

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchUser(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    #queryset = UserProfile.objects.all()
    pagination_class = CustomPagination

    def search(self, username):
        # Define cache key
        cache_key = f"user_search_{username}"

        # Check if data is cached
        cached_result = cache.get(cache_key)

        # Retrieve data from cache if available
        if cached_result:
            users = cached_result
        else:
            if username != '@':
                users = UserProfile.objects.filter(
                    Q(user_id__email__icontains=username) |
                    Q(first_name__icontains=username) |
                    Q(last_name__icontains=username)
                )
            else:
                users = UserProfile.objects.all()[:10]

            # Set cache
            cache.set(cache_key, users)

        return users
    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        users = self.search(username)
        current_user = getUser(request)
        current_user_id = current_user.id

        page = self.paginate_queryset(users)

        if not users:
            return Response(
                {"detail" : "No user found"},
                status=status.HTTP_404_NOT_FOUND
            )
        page = [user for user in page if user.id != current_user_id]
        data = []
        serializer = UserInfoSerializer(page, many=True)
    
        for user in serializer.data:
            user_img = getUserProfileForPosts(User.objects.get(id=user['id']))['avatar']
            user['avatar'] = user_img
            data.append(user)
        return self.get_paginated_response({
            "list_users": data,
            "current_user": current_user_id,
        })
    

class ContactUsers(generics.ListAPIView):
    pagination_class = CustomPagination

    def get_nearest_unread_messeeji(self, channel_id, current_user_id):
        collection = Messeeji._get_collection()
        # Write your raw MongoDB find query
            # print(f"collection: {collection}")
            # Write your raw MongoDB find query
        raw_query = {
            'channel_id': channel_id,
            'sender_id': {
                '$ne' : current_user_id
            },
            'is_read': False
        }

        num_documents = collection.count_documents(raw_query)
        # Execute the raw find query
        unread_messeejis = collection.find_one(raw_query, sort=[('created_at', 1)])
        if (not num_documents):
            num_documents = 0
        return unread_messeejis, num_documents

    def list(self, request, *args, **kwargs):
        user = getUser(request)
        if not user:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        current_user_id = user.id
        # Filter all channels that the current user joins
        user_channels = Participants.objects(user_id=current_user_id)
        # print("a")
        # print(f"all parti: {user_channels}")

        # Find the newest unread Messeeji and its sender from each channel, where the sender is not the current user
        senders_list_info = []
        for channel in user_channels:
            res = self.get_nearest_unread_messeeji(channel.channel_id, current_user_id)
            newest_unread_messeeji = res[0]
            unread_amount = res[1]
            # print(f"new new new: {newest_unread_messeeji}")
            if newest_unread_messeeji:
                sender_profile = UserProfile.objects.get(user_id=newest_unread_messeeji['sender_id'])
                senders_list_info.append({
                    'sender': sender_profile,
                    'channel_id': channel.channel_id,
                    'created_at': newest_unread_messeeji['created_at'],
                    'unread_amount' : unread_amount 
                })

        # print(f"sender_list bf: {senders_list_info}")
        # Sort the list of senders by the time of the newest unread Messeeji
        senders_list_info.sort(key=lambda x: x['created_at'] if x['created_at'] else datetime.min, reverse=True)
        # print(f"sender_list af: {senders_list_info}")
        sender_ids = [sender_info['sender'].user_id for sender_info in senders_list_info]

        # Get all user IDs except those in sender_ids
        all_user_ids = UserProfile.objects.exclude(user_id__in=sender_ids).exclude(user_id=current_user_id).values_list('user_id', flat=True)

        sender_ids.extend(all_user_ids)

        senders_queryset = UserProfile.objects.filter(user_id__in=sender_ids)

        page = self.paginate_queryset(senders_queryset)

        data = []
        serializer = UserInfoSerializer(page, many=True)
        # print(f"data is: {serializer.data}")
        # print(f"sender_list: {senders_list_info}")
    
        data = []

        senders_list_info_iter = iter(senders_list_info)
        for user in serializer.data:
            try:
                
                user_img = getUserProfileForPosts(User.objects.get(id=user['id']))['avatar']
                user['avatar'] = user_img
                sender_info = next(senders_list_info_iter)
                user['unread_amount'] = sender_info['unread_amount']
                data.append(user)
            except StopIteration:
                # Handle the case where sender_list_info runs out
                user['unread_amount'] = 0
                data.append(user)
            except UserProfile.DoesNotExist:
                # Handle the case where the sender's profile doesn't exist
                user['unread_amount'] = 0
                data.append(user)


        # print(f"final data: {data}")
        return self.get_paginated_response({
            "list_users": data,
            "current_user": current_user_id,
        })
