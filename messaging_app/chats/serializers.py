from .models import Conversation, Message, user
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'address', 'phone_number']
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'conversation', 'sender', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'created_at', 'participants', 'message']
        read_only_fields = ['conversation_id', 'created_at']
        
