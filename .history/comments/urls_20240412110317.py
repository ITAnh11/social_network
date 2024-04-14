from django.urls import path

from .views import GetCommentsForPost, GetCommentsForComment, CreateCommentForPost, CreateCommentForComment

app_name = 'comments'
urlpatterns = [
    path('get_comments_for_post/', GetCommentsForPost.as_view(), name='get_comments_for_post'),
    path('get_comments_for_comment/', GetCommentsForComment.as_view(), name='get_comments_for_comment'),
    path('create_comment_for_post/', CreateCommentForPost.as_view(), name='create_comment_for_post'),
    path('create_comment_for_comment/', CreateCommentForComment.as_view(), name='create_comment_for_comment')
    
]