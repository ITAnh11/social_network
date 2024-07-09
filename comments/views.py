from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from comments.models import Comments
from .serializers import CommentsSerializer

from notifications.views import createCommentNotification

from common_functions.common_function import getUser, getTimeDurationForComment
import logging
logger = logging.getLogger(__name__)
from userprofiles.views import UserProfileBasicView
class GetCommentsForPost(APIView):
    def post(self, request):
        try: 
            response = Response()
            
            posts_id = int(request.data.get('posts_id'))

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
        except Exception as e:
            logger.error(f"Error while retrieving comments for comment: {str(e)}")
            return Response({'error': 'Error while retrieving comments for comment'}, status=500)


class GetCommentsForComment(APIView):
    def post(self, request):
        try: 
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
        except Exception as e:
            logger.error(f"Error while retrieving comments for comment: {str(e)}")
            return Response({'error': 'Error while retrieving comments for comment'}, status=500)

class CreateComment(APIView):    
    def createComment(self, request, user):
        return Comments(to_posts_id=request.data.get('posts_id'), 
                        to_comment_id=request.data.get('comment_id'), 
                        content=request.data.get('content'), 
                        user=UserProfileBasicView().getUserProfileBasic(user), 
                        created_at=timezone.now(), 
                        updated_at=timezone.now())
    
    def post(self, request):
        try:

            user = getUser(request)
            
            if not user:
                return Response({
                    "message": "Unauthorized"
                    },status=401)
            
            response = Response()
            
            comment = self.createComment(request, user)
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
        except Exception as e:
            logger.error(f"Error while creating comment: {str(e)}")
            return Response({'error': 'Error while creating comment'}, status=500)