from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message, user
from .serializers import ConversationSerializer, MessageSerializer
# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user_id = self.request.user.user_id
        return self.queryset.filter(participants__user_id=user_id)
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return self.queryset.filter(conversation__conversation_id=conversation_id)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)