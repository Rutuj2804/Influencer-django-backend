from django.db import models
from accounts.models import Account


class TimeSpend(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.DecimalField(max_digits=10 ,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username