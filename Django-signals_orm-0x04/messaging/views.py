from django.shortcuts import render
from rest_framework.response import Response 
from django.contrib.auth.models import User
from .models import Message

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
    
def thread_messages(request, message_id):
    """
    View to get the thread of messages for a given message ID.
    """
    try:
        message = Message.objects.get(id=message_id)
        thread = message.get_thread()
        return Response({"thread": thread}, status=200)
    except Message.DoesNotExist:
        return Response({"error": "Message not found."}, status=404)
