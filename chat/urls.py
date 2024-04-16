# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_conversations/", views.ConversationView.as_view()),
    path("create_conversations/", views.CreateConversationView.as_view()),
    
    path("<sender_id>/<receiver_id>/", views.GetMessages.as_view()),
    # path("<str:room_name>/", views.room, name="room"),
]