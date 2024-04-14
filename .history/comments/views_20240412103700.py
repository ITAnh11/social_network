from rest_framework.views import APIView
from rest_framework.response import Response

from mongoengine.queryset.visitor import Q

from comments.models import Comments
from .serializers import CommentsSerializer

from common_functions.common_function import getUser   

import datetime

# Create your views here.
class GetCommentsForPost(APIView):
    def get(self, request):
        
        # print(request.data)
        
        response = Response()
        
        posts_id = request.data.get('posts_id')
        
        comments = Comments.objects(__raw__={'to_posts_id': posts_id})
        
        list_comments = []
        for comment in comments:
            serializer = CommentsSerializer(comment)
            # print(serializer.data)
            list_comments.append(serializer.data)
        
        response.data = {
            'comments': list_comments
        }
        return response

class GetCommentsForComment(APIView):
    def post(self, request):
        response = Response()
        
        comment_id = request.data.get('comment_id')
        
        comments = Comments.objects(__raw__={'to_comment_id': comment_id})
        
        list_comments = []
        for comment in comments:
            serializer = CommentsSerializer(comment)
            # print(serializer.data)
            list_comments.append(serializer.data)
        
        response.data = {
            'comments': list_comments
        }
        
        return response

class CreateCommentForPost(APIView):
    def post(self, request):
        user = getUser()
        
        if not user:
            return Response({
                "message": "Unauthorized"
                },status=401)
        
        response = Response()
        
        user_id = user.id
        post_id = request.data.get('to_posts_id')
        content = request.data.get('content')
        
        comment = Comments(to_posts_id=post_id, to_comment_id=-1, content=content, user_id=user_id, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        comment.save()
        
        response.data = {
            "success": "Comment created successfully"
        }
        
        return response

class CreateCommentForComment(APIView):
    def post(self, request):
        user = getUser()
        
        if not user:
            return Response({
                "message": "Unauthorized"
                },status=401)
        
        response = Response()
        
        user_id = user.id
        post_id = request.data.get('to_comment_id')
        content = request.data.get('content')
        
        
        comment = Comments(to_posts_id=post_id, to_comment_id=-1, content=content, user_id=user_id, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        comment.save()
        
        response.data = {
            "success": "Comment created successfully"
        }
        
        return response