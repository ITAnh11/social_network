from django.urls import path
from.views import FriendsRequestsView, SentFriendRequestView, RevokeFriendRequestView, AcceptFriendRequestView, DenineFriendRequestView, DeleteFriendShip, GetSentFriendRequestsView, GetReceivedFriendRequestsView, GetListFriendView, GetMutualFriendView, GetSuggestionFriendView
app_name = 'friends'
urlpatterns = [
    path('',FriendsRequestsView.as_view(), name="friend"),
    path('sent_friendrequest/',SentFriendRequestView.as_view(), name="sent_friendrequest"),#gui loi moi ket ban , st: "pending" , to_id: "..."
    path('revoke_friendrequest/',RevokeFriendRequestView.as_view(), name="revoke_friendrequest"),#thu hoi loi moi ket ban , st:"revoke", to_id:"..."
    path('accept_friendrequest/',AcceptFriendRequestView.as_view(), name="accept_friendrequest"),#An nut xac nhan, st:"accepted", friendRequest_id:"..."
    path('denine_friendrequest/',DenineFriendRequestView.as_view(), name="denine_friendrequest"),#Tu choi ,st: "denined",friendRequest_id:"...";
    path('delete_friendship/',DeleteFriendShip.as_view(), name="delete_friendship"),#xoa ban be ,st: "deleted", to_id:" "
    path('get_sentfriendrequest/',GetSentFriendRequestsView.as_view(), name="get_sentfriendrequest"),
    path('get_receivedfriendrequest/',GetReceivedFriendRequestsView.as_view(), name="get_receivedfriendrequest"),
    path('get_listfriend/',GetListFriendView.as_view(), name="get_listfriend"),#lay danh sach ban be
    path('get_mutualfriend/',GetMutualFriendView.as_view(), name='get_mutualfriend'), #lay ds cac ban be chung cua 2 user
    path('get_suggestionfriend/',GetSuggestionFriendView.as_view(), name='get_suggestionfriend') # gợi ý kết bạn
]