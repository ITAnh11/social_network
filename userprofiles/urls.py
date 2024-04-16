from django.urls import path
from .views import ProfileView, EditProfileView, EditStoryView, ListFriendsView, SetUserProfileView, SetImageProfileView, GetProfileView, GetPostsView, GetUserProfileBasicView

from chat.views import ProfileDetail
app_name = 'userprofiles'
urlpatterns = [
        path('', ProfileView.as_view(), name='profile'),
        path('editProfile/', EditProfileView.as_view(), name='editProfile'),
        path('editStory/', EditStoryView.as_view(), name='editStory'),
        path('listFriends/', ListFriendsView.as_view(), name='listFriends'),
        path('set_userprofile/', SetUserProfileView.as_view(), name='set_userprofile'),
        path('set_imageprofile/', SetImageProfileView.as_view(), name='set_imageprofile'),
        path('get_profile/', GetProfileView.as_view(), name='get_profile'),
        path('get_posts/', GetPostsView.as_view(), name='get_posts'),
        path('get_profile_basic/', GetUserProfileBasicView.as_view(), name='get_profile_basic'),
        path('<int:pk>',ProfileDetail.as_view()),

    ]