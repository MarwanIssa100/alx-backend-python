from .models import Message , Notification ,MessageEditHistory
from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver



@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    if instance.edited:
        MessageEditHistory.objects.create(message=instance, old_content=instance.content, new_content=instance.edited_content)
        print(f"Message edited: {instance.content} to {instance.edited_content} by {instance.sender.all()}")
    else:
        print(f"New message being created: {instance.content} from {instance.sender.all()} to {instance.receiver.all()}")


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