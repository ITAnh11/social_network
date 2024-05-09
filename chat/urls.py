# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatTestView.as_view(), name="chat-page"),
    path("get_channels/", views.GetChannels.as_view()),
    path("get_messeeji/",views.GetMesseeji.as_view()),
    path("create_channel/", views.CreateChannel.as_view()),
    path("create_messeeji/", views.CreateMesseeji.as_view()),  
    path("mark_as_read/", views.MarkReadMesseeji.as_view()), 
    path("all_contact_users/", views.ContactUsers.as_view()), 
    
    # path("<str:room_name>/", views.room, name="room"),
]