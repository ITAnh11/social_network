from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Reactions, UserReaction
from .serializers import ReactionsSerializer

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
        
        reactions = None
        
        if posts_id > 0:
            reactions = Reactions.objects(__raw__={'to_posts_id': posts_id})
        elif comments_id > 0:
            reactions = Reactions.objects(__raw__={'to_comment_id': comments_id})
        
        # reactions = Reactions.objects(__raw__={'to_posts_id': 65})
        
        list_reactions = []
        for reaction in reactions:
            serializer = ReactionsSerializer(reaction)
            list_reactions.append(serializer.data)
        
        response = Response()
        
        response.data = {
            'reactions': list_reactions,
            'count': len(list_reactions) or 0
        }
        return response

class CreateReaction(APIView):
    def createUserReaction(self, request):
        user = json.loads(request.data.get('user'))
        
        return UserReaction(id=user.get('id'), 
                            name=user.get('name'), 
                            avatar=user.get('avatar'))
    
    def createReaction(self, request):
        return Reactions(user=self.createUserReaction(request), 
                         to_posts_id=request.data.get('posts_id'), 
                         to_comment_id=request.data.get('comment_id'), 
                         type=request.data.get('type'),
                         created_at=datetime.datetime.now(), 
                         updated_at=datetime.datetime.now())
    
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        reaction = self.createReaction(request)
        reaction.save()
        
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
        
        reaction =Reactions.objects(__raw__={'to_posts_id': posts_id, 
                                             'to_comment_id': comment_id,
                                                'user.id': user_id})
        
        reaction.delete()
        
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
        
        response.data = {
            'is_reacted': len(reaction) > 0
        }
        return response