from django.db import models
from accounts.models import Account


class Application(models.Model):
    applicant = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    applying_for = models.CharField(max_length=30)

    def __str__(self):
        return self.applicant.username