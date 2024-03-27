from django.urls import path

from .views import PostsView, PostsPageView

app_name = 'posts'
urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    path('page/', PostsPageView.as_view(), name='posts_page'),
]