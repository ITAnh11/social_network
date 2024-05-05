from .models import ReactNotifitions, CommentNotifications, AddFriendNotifications, Notifications
from posts.models import Posts
from comments.models import Comments
from users.models import User
from userprofiles.models import UserProfile, UserBasicInfo, ImageProfile

from .serializers import ReactNotifitionsSerializer, CommentNotificationsSerializer, AddFriendNotificationsSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common_functions.common_function import getUser, getTimeDuration

import json
from social_network.redis_conn import redis_server

import datetime
import random
import logging
logger = logging.getLogger(__name__)
LENGTH_OF_CONTENT = 50
EX_TIME = 60
INT_FROM = 0
INT_TO = 100

def appendNotifications(user_id, notification):
    print('Append Notifications')
    # Get the current notifications from Redis
    notifications = redis_server.get(f'notifications_{user_id}')

    if notifications is not None:
        # If there are notifications, load them from the stored JSON
        notifications = json.loads(notifications)
    else:
        # If there are no notifications, return
        return

    # Add the new notification to the list
    notifications.append(notification.to_json())
    
    time_to_live = EX_TIME + random.randint(INT_FROM, INT_TO)

    # Store the updated list in Redis
    redis_server.setex(f'notifications_{user_id}', time_to_live, json.dumps(notifications))
        

def addContent(content, contentOf):
    if contentOf is None:
        content += '.'
    elif len(contentOf) > LENGTH_OF_CONTENT:
        contentOf = contentOf[:LENGTH_OF_CONTENT]
        content += f': {contentOf}...'
    elif len(contentOf) <= LENGTH_OF_CONTENT:
        content += f': {contentOf}'
    return content

def createReactNotification(forReaction):
    try:
        is_for_post = (forReaction.to_comment_id < 0)
        content = f'reacted {forReaction.type} to your'
        content += ' post' if forReaction.to_comment_id < 0 else ' comment'
        
        if is_for_post:
            posts = Posts.objects.get(id=forReaction.to_posts_id)
            contentOf = posts.content
            to_user = User.objects.get(id=posts.user_id.id)
            
        elif is_for_post == False:
            comment = Comments.objects(__raw__={'_id': forReaction.to_comment_id}).first()
            contentOf = comment.content
            to_user = User.objects.get(id=comment.user.id)
        
        if to_user.id == forReaction.user.id:    
            return
        
        content = addContent(content, contentOf)
        
        notification = ReactNotifitions(type='reaction', 
                         user=forReaction.user, 
                         content=content, 
                         type_reaction=forReaction.type, 
                         to_posts_id=forReaction.to_posts_id, 
                         to_comment_id=forReaction.to_comment_id, 
                         to_user_id=to_user.id, 
                         created_at=forReaction.created_at) 
        
        notification.save() 
        logger.info("Notification created successfully")
        appendNotifications(to_user.id, notification)
        
    except Exception as e:
        logger.error('error while creating notifications')
        print("createReactNotification", e)


def createCommentNotification(forcomment):
    try:
        is_for_post = (forcomment.to_comment_id < 0)
        if is_for_post:
            content = f'commented on your'
        elif is_for_post == False:
            content = f'replied to your'
            
        content += ' post' if is_for_post else ' comment'
        
        if is_for_post:
            posts = Posts.objects.get(id=forcomment.to_posts_id)
            if posts is None:
                print('Posts not found')
                return
            contentOf = posts.content
            to_user = User.objects.get(id=posts.user_id.id)
            
        elif is_for_post == False:
            # print(forcomment.to_comment_id)
            comment = Comments.objects(__raw__={'_id': forcomment.to_comment_id}).first()
            if comment is None:
                print('Comment not found')
                return
            contentOf = comment.content
            to_user = User.objects.get(id=comment.user.id)
        
        if to_user.id == forcomment.user.id:    
            return
        
        content = addContent(content, contentOf)
        
        notification = CommentNotifications(type='comment', 
                         user=forcomment.user, 
                         content=content, 
                         to_posts_id=forcomment.to_posts_id, 
                         to_comment_id=forcomment.to_comment_id, 
                         to_user_id=to_user.id, 
                         created_at=forcomment.created_at) 
        
        notification.save() 
        logger.info('creat cmt notiies successfully')
        appendNotifications(to_user.id, notification)
        
    except Exception as e:
        logger.error('error while creating cmtNotifications')
        print("createCommentNotification", e)

def createAddFriendNotification(forFriendRequest):
    try:
        content = f'sent you a friend request.'
        
        userprofile = UserProfile.objects.get(user_id=forFriendRequest.from_id)
        imageprofile = ImageProfile.objects.get(user_id=forFriendRequest.from_id)
        userbasicinfo = UserBasicInfo(id=userprofile.user_id.id, 
                                      name=f'{userprofile.first_name} {userprofile.last_name}', 
                                      avatar=imageprofile.avatar.url)
        
        notification = AddFriendNotifications(type='add_friend', 
                         user=userbasicinfo, 
                         content=content, 
                         id_friend_request=forFriendRequest.id,
                         status_request=forFriendRequest.status,
                         to_user_id=forFriendRequest.to_id.id, 
                         created_at=forFriendRequest.created_at) 
        
        notification.save() 
        logger.info('created addFr notifications successfully')
        appendNotifications(forFriendRequest.to_id.id, notification)
        
    except Exception as e:
        logger.error('can not creat addFrNotif huhu')
        print("createAddFriendNotification", e)

class GetNotifications(APIView):
    def getNotifications(self, user_id):
        logger.info("Fetching notifications")
        notifications = redis_server.get(f'notifications_{user_id}')
        
        if notifications is None:
            logger.info("Fetching notifications from MongoDB")
            
            # order_by('created_at') is used to sort the notifications by the created_at field in ascending order
            notifications = Notifications.objects(__raw__={'to_user_id': user_id}).order_by('created_at')
            
            time_to_live = EX_TIME + random.randint(INT_FROM, INT_TO)

            redis_server.setex(f'notifications_{user_id}', time_to_live, json.dumps([notification.to_json() for notification in notifications]))
        else:
            logger.info("Fetching notifications from Redis")
            notifications = [Notifications.from_json(notification) for notification in json.loads(notifications)]
        
        return notifications
    
    def serializeNotifications(self, notifications):
        logger.info("Serializing notifications")
        list_notifications = []
        
        for notification in notifications:
            if notification.type == 'reaction':
                dataNotification = ReactNotifitionsSerializer(notification).data
            elif notification.type == 'comment':
                dataNotification = CommentNotificationsSerializer(notification).data
            elif notification.type == 'add_friend':
                dataNotification = AddFriendNotificationsSerializer(notification).data
            
            dataNotification['created_at'] = getTimeDuration(notification.created_at)
                        
            list_notifications.append(dataNotification)
        
        return list_notifications
    
    def get(self, request):
        logger.info("GET request received in GetNotifications")
        
        time_start = datetime.datetime.now()
        
        user = getUser(request)
        if isinstance(user, User) == False:
            logger.warning("Unauthorized access detected in GetNotifications")
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        notifications = self.getNotifications(user.id)
            
        list_notifications = self.serializeNotifications(notifications)
        
        response.data = {
            'notifications': list_notifications
        }
        
        time_end = datetime.datetime.now()
        
        logger.info(f"GetNotifications execution time: {time_end - time_start}")
        
        return response
