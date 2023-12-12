from django.contrib.auth.models import User
from django.db import models
from users.models import MyUser


class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} ({self.timestamp})"
