from django.urls import path
from.views import AddFriendView, FriendRequestsListView, FriendsView
app_name = 'friends'
urlpatterns = [
    path('',FriendsView.as_view(), name="friend"),
    path('addfriend/',AddFriendView.as_view(), name="addfriend"),
    path('friendrequestslist/',FriendRequestsListView.as_view(), name="friendrequestslist")
]