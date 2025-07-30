from django.db import models

class UnreadMessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)