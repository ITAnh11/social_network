from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Reactions
from .serializers import ReactionsSerializer

from posts.models import PostsInfo
from posts.serializers import PostsInfoSerializer

from comments.models import Comments
from comments.serializers import CommentsSerializer

from userprofiles.models import UserBasicInfo

import datetime

import json
from common_functions.common_function import getUser

# Create your views here.
class GetReactions(APIView):
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # print(request.data)
        
        posts_id = int(request.data.get('posts_id'))
        comments_id = int(request.data.get('comment_id'))
        
        topMostReacted = None
        total = None
        
        if posts_id > 0:
            postsInfo = PostsInfo.objects(__raw__={'posts_id': posts_id}).first()
            if postsInfo is None:
                return Response({'error': 'Posts not found'}, status=status.HTTP_404_NOT_FOUND)
            topMostReacted = postsInfo.getMostUseReactions()
            total = postsInfo.number_of_reactions.total
        elif comments_id > 0:
            comment = Comments.objects(__raw__={'id': comments_id}).first()
            if comment is None:
                return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
            topMostReacted = comment.getMostUseReactions()
            total = comment.number_of_reactions.total
            
        response = Response()
        response.data = {
            'total': total,
            'topMostReacted': topMostReacted,
        }
        return response

class CreateReaction(APIView):
    def createUserBasicInfo(self, request):
        
        return UserBasicInfo(id=request.data.get('user_id'), 
                            name=request.data.get('user_name'), 
                            avatar=request.data.get('user_avatar'))
    
    def createReaction(self, request):
        return Reactions(user=self.createUserBasicInfo(request), 
                         to_posts_id=request.data.get('posts_id'), 
                         to_comment_id=request.data.get('comment_id'), 
                         type=request.data.get('type'),
                         created_at=datetime.datetime.now(), 
                         updated_at=datetime.datetime.now())
    
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.data.get('type') not in ['like', 'love', 'haha', 'wow', 'sad', 'angry', 'care']:
            return Response({'error': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('posts_id') is None and request.data.get('comment_id') is None:
            return Response({'error': 'posts_id or comment_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('user_id') is None or request.data.get('user_name') is None or request.data.get('user_avatar') is None:
            return Response({'error': 'user_id, user_name, user_avatar is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('user_id') != user.id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))
        
        try:
            reaction = self.createReaction(request)
            reaction.save()
            
            if posts_id > 0:
                postsInfo = PostsInfo.objects(posts_id=posts_id).first()
                postsInfo.inc_reaction(reaction.type)
                postsInfo.save()
            elif comment_id > 0:
                comment = Comments.objects(__raw__={'id': comment_id}).first()
                comment.inc_reaction(reaction.type)
                comment.save()
                
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = ReactionsSerializer(reaction)
        
        response.data = {
            'reaction': serializer.data
        }
        return response

class DeleteReaction(APIView):
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        user_id = user.id
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))

        try:
            reaction = Reactions.objects(__raw__={'to_posts_id': posts_id, 
                                                  'to_comment_id': comment_id, 
                                                  'user.id': user_id}).first()
            
            if reaction is None:
                return Response({'error': 'Reaction not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if posts_id > 0:
                postsInfo = PostsInfo.objects(__raw__={'posts_id': posts_id}).first()
                if postsInfo is None:
                    return Response({'error': 'Posts Info not found'}, status=status.HTTP_404_NOT_FOUND)
                postsInfo.dec_reaction(reaction.type)
                postsInfo.save()
            elif comment_id > 0:
                comment = Comments.objects(__raw__={'id': comment_id}).first()
                if comment is None:
                    return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
                comment.dec_reaction(reaction.type)
                comment.save()
                
            reaction.delete()
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response.data = {
            'message': 'Reaction removed'
        }
        return response

class IsReactedView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        user_id = user.id
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))
        
        reaction = Reactions.objects(__raw__={  'to_posts_id': posts_id, 
                                                'to_comment_id': comment_id,
                                                'user.id': user_id})
        
        is_reacted = len(reaction) > 0
        
        response.data = {
            'is_reacted': is_reacted
        }
        
        if is_reacted:
            serializer = ReactionsSerializer(reaction.first())
            response.data['type'] = serializer.data['type'] 
            
        return response