from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Q

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import MessageSerializer, UserInfoSerializer, ConversationSerializer

from users.models import User
from userprofiles.models import UserProfile

from .models import Conversation, Message

from common_functions.common_function import getUserProfileForPosts, getTimeDuration, getUser


class CreateConversationView(APIView):
    def createConversation(self, request):
        try:
            conversation = Conversation.objects.create(
                conversation_id = 1,
                title = request.data.get('title') or None,
                status='visible'
            )
            conversation.save()
        except:
            return Response({'error':'error when creating Conversation'})
        return conversation
    def post(self, request):
        conversation = self.createConversation(request)
        data = []

        conversation_data = ConversationSerializer(conversation).data

        data.append(conversation_data)

        return Response({'success': 'Conversation created!',
                         'conversation': data})

class ConversationView(APIView):
    serializer_class = ConversationSerializer

    def get(self, request):
        response = Response()
        user = getUser(request)
        
        convs = Conversation.objects.filter(
            Q(conv__sender=user) | Q(conv__receiver=user)
        ).distinct()
        data = []
        for conv in convs:
            conv_data = ConversationSerializer(conv).data
            print(conv_data)
            data.append(conv_data)

        response.data = {
            "conversations" : data
        }
        
        return response

class MessageView(generics.ListAPIView):
    
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

class SearchUser(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("list func called")
        username = self.kwargs['username']
        # logged_in_user = self.request.user
        print(UserProfile.objects.all())
        users = UserProfile.objects.filter(
            Q(user_id__email__icontains=username) |
            Q(first_name__icontains=username) |
            Q(last_name__icontains=username) 
            # &-Q(user=logged_in_user),
        )
        print(users)
        if not users.exists():
            return Response(
                {"detail" : "No user found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})