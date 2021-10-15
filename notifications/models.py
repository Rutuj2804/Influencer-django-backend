from django.db import models
from accounts.models import Account


class Notification(models.Model):
    by_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='by_user')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    text_one = models.TextField()
    highlighted_text = models.TextField()
    text_two = models.TextField()
    seen_by_user = models.BooleanField(default=False)

    def __str__(self):
        return self.type