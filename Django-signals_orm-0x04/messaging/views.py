from django.shortcuts import render
from rest_framework.response import Response 
from django.contrib.auth.models import User
from .models import Message 
from .managers import UnreadMessagesManager

# Create your views here.

def delete_user(request, user_id):
    """
    View to delete a user by ID.
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=204)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    
    
def get_messages(request):
    """
    View to get all messages for the authenticated user.
    """
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    serialized_messages = []
    
    for message in messages:
        serialized_messages.append({
            'id': message.id,
            'content': message.content,
            'sender': [user.username for user in message.sender.all()],
            'receiver': [user.username for user in message.receiver.all()],
            'timestamp': message.timestamp,
            'edited': message.edited
        })
    
    return Response({"messages": serialized_messages}, status=200)
def thread_messages(request, message_id):
    """
    View to get the thread of messages for a given message ID.
    """
    try:
        message = Message.objects.filter(sender = request.user , receiver = request.user).select_related('sender', 'receiver')
        thread = message.get_thread()
        return Response({"thread": thread}, status=200)
    except Message.DoesNotExist:
        return Response({"error": "Message not found."}, status=404)

def get_unread_messages(request):
    """
    View to get all unread messages for the authenticated user.
    """
    unread_messages = UnreadMessagesManager().get_queryset().filter(receiver=request.user).only('content', 'sender')
    serialized_unread_messages = []
    
    for message in unread_messages:
        serialized_unread_messages.append({
            'id': message.id,
            'content': message.content,
            'sender': [user.username for user in message.sender.all()],
            'receiver': [user.username for user in message.receiver.all()],
            'timestamp': message.timestamp
        })
    
    return Response({"unread_messages": serialized_unread_messages}, status=200)