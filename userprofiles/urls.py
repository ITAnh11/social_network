from django.urls import path
from .views import ProfileView, SetUserProfileView, SetImageProfileView, GetProfileView

app_name = 'userprofiles'
urlpatterns = [
        path('', ProfileView.as_view(), name='profile'),
        path('setuserprofile/', SetUserProfileView.as_view(), name='setuserprofile'),
        path('setimageprofile/', SetImageProfileView.as_view(), name='setimageprofile'),
        path('getprofile/', GetProfileView.as_view(), name='getprofile'),
    ]