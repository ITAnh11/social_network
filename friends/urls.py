from django.urls import path
from.views import FriendsRequestsView, SentFriendRequestView, DeleteFriendRequestView, AcceptFriendRequestView, DenineFriendRequestView, DeleteFriendShip, GetSentFriendRequestsView, GetReceivedFriendRequestsView, GetListFriendView
app_name = 'friends'
urlpatterns = [
    path('',FriendsRequestsView.as_view(), name="friend"),
    path('sent_friendrequest/',SentFriendRequestView.as_view(), name="sent_friendrequest"),
    path('delete_friendrequest/',DeleteFriendRequestView.as_view(), name="delete_friendrequest"),
    path('accept_friendrequest/',AcceptFriendRequestView.as_view(), name="accept_friendrequest"),
    path('denine_friendrequest/',DenineFriendRequestView.as_view(), name="denine_friendrequest"),
    path('delete_friendship/',DeleteFriendShip.as_view(), name="delete_friendship"),
    path('get_sentfriendrequest/',GetSentFriendRequestsView.as_view(), name="get_sentfriendrequest"),
    path('get_receivedfriendrequest/',GetReceivedFriendRequestsView.as_view(), name="get_receivedfriendrequest"),
    path('get_listfriend/',GetListFriendView.as_view(), name="get_listfriend")
]