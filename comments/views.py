from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from mongoengine.queryset.visitor import Q

from comments.models import Comments
from .serializers import CommentsSerializer

from userprofiles.models import UserBasicInfo

from notifications.views import createCommentNotification

from common_functions.common_function import getUser, getTimeDurationForComment

# Create your views here.

class GetCommentsForPost(APIView):
    def post(self, request):
        
        # print(request.data)
        
        response = Response()
        
        posts_id = int(request.data.get('posts_id'))
        
        # print(type(posts_id))
        
        comments = Comments.objects(__raw__={'to_posts_id': posts_id, 'to_comment_id': -1})
        
        list_comments = []
        for comment in comments:
            dataComment = CommentsSerializer(comment).data
            dataComment['created_at'] = getTimeDurationForComment(comment.created_at)
            dataComment['most_use_reactions'] = comment.getMostUseReactions()
            
            list_comments.append(dataComment)
        
        response.data = {
            'comments': list_comments
        }
        return response

class GetCommentsForComment(APIView):
    def post(self, request):
        response = Response()
        
        comment_id = int(request.data.get('comment_id'))
        
        comments = Comments.objects(__raw__={'to_comment_id': comment_id})
        
        list_comments = []
        for comment in comments:
            dataComment = CommentsSerializer(comment).data
            dataComment['created_at'] = getTimeDurationForComment(comment.created_at)
            dataComment['most_use_reactions'] = comment.getMostUseReactions()

            
            list_comments.append(dataComment)
        
        response.data = {
            'comments': list_comments
        }
        
        return response

class CreateComment(APIView):
    
    def createUserBasicInfo(self, request):        
        return UserBasicInfo(id=int(request.data.get('user_id')), 
                           name=request.data.get('user_name'), 
                           avatar=request.data.get('user_avatar'))
    
    def createComment(self, request):
        return Comments(to_posts_id=request.data.get('posts_id'), 
                        to_comment_id=request.data.get('comment_id'), 
                        content=request.data.get('content'), 
                        user=self.createUserBasicInfo(request), 
                        created_at=timezone.now(), 
                        updated_at=timezone.now())
    
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({
                "message": "Unauthorized"
                },status=401)
        
        response = Response()
        
        # print(request.data)
        
        comment = self.createComment(request)
        comment.save()
        
        createCommentNotification(comment)
        
        dataComment = CommentsSerializer(comment).data
        dataComment['created_at'] = 'Just now'
        dataComment['most_use_reactions'] = comment.getMostUseReactions()

        
        response.data = {
            "success": "Comment created successfully",
            "comments": [dataComment]
        }
        
        return response