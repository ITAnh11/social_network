from django.urls import path

from .views import CreatePostsView, GetPostsPageView, MarkPostAsWatchedView

app_name = 'posts'
urlpatterns = [
    path('create/', CreatePostsView.as_view(), name='create_posts'),
    path('page/', GetPostsPageView.as_view(), name='posts_page'),
    path('mark_as_watched/', MarkPostAsWatchedView.as_view(), name='mark_as_watched')
]