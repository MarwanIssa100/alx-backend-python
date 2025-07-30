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
