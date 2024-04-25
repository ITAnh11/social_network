from django.urls import path

from .views import CreatePostsView, GetPostsPageView

app_name = 'posts'
urlpatterns = [
    path('create/', CreatePostsView.as_view(), name='create_posts'),
    path('page/', GetPostsPageView.as_view(), name='posts_page'),
]