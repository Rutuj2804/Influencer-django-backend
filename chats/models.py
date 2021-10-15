from django.db import models
from accounts.models import Account


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    seen_by_user = models.BooleanField(default=False)


class ChatRoom(models.Model):
    users = models.ManyToManyField(Account)
    created_at = models.DateTimeField(auto_now_add=True)
    chats = models.ManyToManyField(Message)
    last_message = models.TextField(null=True)
    last_conversaion = models.DateTimeField(auto_now=True, null=True)