from .models import Message , Notification
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def message_saved(sender, instance, created, **kwargs):
    if created:
        for receiver in instance.receiver.all():
            Notification.objects.create(user=receiver, message=instance)
    else:
        print(f"Message updated: {instance.content} from {instance.sender.all()} to {instance.receiver.all()}")
        

@receiver(post_save, sender=Notification)
def notification_saved(sender, instance, created, **kwargs):
    if created:
        print(f"Notification created for user {instance.user.username} : {instance.message.content}")