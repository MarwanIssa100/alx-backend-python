from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    sender  = models.ManyToManyField(User, related_name='sent_messages')
    receiver = models.ManyToManyField(User, related_name='received_messages')
    content = models.TextField()
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    new_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)

