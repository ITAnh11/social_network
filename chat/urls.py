# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatTestView.as_view(), name="chat-page"),
    path("get_channels/", views.GetChannels.as_view()),
    path("get_messeeji/",views.GetMesseeji.as_view()),

    path("create_channel/", views.CreateChannel.as_view()),
    
    path("create_messeeji/", views.CreateMesseeji.as_view()),  
      
    path("get_conversations/", views.ConversationView.as_view()),
    path("create_conversations/<int:receiver_id>/", views.CreateConversationView.as_view()),
    path("create_init_message/<int:receiver_id>/",views.MessageView.as_view()),
    path("<sender_id>/<receiver_id>/", views.GetMessages.as_view()),
    # path("<str:room_name>/", views.room, name="room"),
]