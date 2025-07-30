from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(unread=True)
    
    def unread_for_user(self, user):
        """
        Get all unread messages for a specific user.
        """
        return self.get_queryset().filter(receiver=user)