from django.urls import path
from .views import HomePageView
from posts.views import GetPostsForHomePageView

app_name = 'homepage'
urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('get_posts/', GetPostsForHomePageView.as_view(), name='get_posts')
]