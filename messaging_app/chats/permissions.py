from rest_framework import permissions , BasePermission
from rest_framework.decorators import action

class IsParticipant(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        conversation_id = view.kwargs.get('pk')
        if not conversation_id:
            return False
        
        user = request.user
        return user.is_authenticated and user.conversations.filter(conversation_id=conversation_id).exists()