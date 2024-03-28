from django.urls import path
from.views import FriendsView
app_name = 'friends'
urlpatterns = [
    path('',FriendsView.as_view(), name="friend")
]