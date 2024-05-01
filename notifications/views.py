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

LENGTH_OF_CONTENT = 50

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
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
        print("createAddFriendNotification", e)

class GetNotifications(APIView):
    def get(self, request):
        user = getUser(request)
        if isinstance(user, User) == False:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()

        notifications = Notifications.objects(__raw__={'to_user_id': user.id}).order_by('-created_at')[:20]
        
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
        
        response.data = {
            'notifications': list_notifications
        }
        
        return response