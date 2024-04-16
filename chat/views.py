from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import MessageSerializer

from users.models import User

from .models import Conversation, Message

from common_functions.common_function import getUserProfileForPosts, getTimeDuration, getUser


class ConversationView(generics.ListAPIView):
    
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        
        messages = Message.objects.filter(
            id__in = Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id),
                    Q(receiver__sender=user_id),
                ).distinct().annotate(
                    last_message = Subquery(
                        Message.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id),
                            Q(receiver=OuterRef('id'), sender=user_id),
                        ).order_by("-id")[:1].values_list("id", flat = True)
                    )
                ).values_list("last_message", flat=True).order_by("-id")
            )            
        ).order_by("-id")

        return messages

class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']

        messages = Message.objects.filter(
            sender__in=[sender_id, receiver_id],
            receiver_in=[sender_id, receiver_id],
        )

        return messages

class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer

# class ChatPageView(APIView):
#     def get(self, request):
#         user = getUser(request)
        
#         if not user:
#             return HttpResponseRedirect(reverse('users:login'))
        
#         return render(request, 'chat/chat.html')

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})