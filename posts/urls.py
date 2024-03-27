from django.urls import path

from .views import PostsView

app_name = 'posts'
urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
]