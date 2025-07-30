from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

# Create your models here.
class Message(models.Model):
    sender  = models.ManyToManyField(User, related_name='sent_messages')
    receiver = models.ManyToManyField(User, related_name='received_messages')
    content = models.TextField()
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    unread = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Custom manager for unread messages
    unread = UnreadMessagesManager()
    
    @classmethod
    def get_replies(cls):
        return cls.objects.select_related('parent_message').filter(parent_message__isnull=False)
    
    def get_thread(self):
        replies = []
        for reply in self.replies.select_related('parent_message').prefetch_related('sender'):
            replies.append({
                'message': reply,
                'replies': reply.get_thread() if reply.replies.exists() else []
            })
        return replies
            
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    new_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)



