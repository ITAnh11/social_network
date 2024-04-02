from django.urls import path
from .views import HomePageView, getPostsView

app_name = 'homepage'
urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('get_posts/', getPostsView.as_view(), name='get_posts')
]