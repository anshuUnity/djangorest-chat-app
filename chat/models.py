from django.db import models

# Create your models here.

class Chat(models.Model):
    sender_id = models.IntegerField(blank=True, null=True)
    thread_name = models.CharField(blank=True, null=True, max_length=20)
    message = models.TextField(blank=True, null=True)
    message_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sender_id}'
